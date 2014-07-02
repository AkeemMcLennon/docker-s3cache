from flask import Flask, redirect
import boto
import boto.s3
import os
import os.path
import threading
import urllib
from time import time
from boto.s3.key import Key
from flask import make_response
app = Flask(__name__)
app.debug = True

'''Change the constants below to your specific details'''
CACHE_ROOT = "/var/www"
#Timeout in seconds 
CACHE_TIMEOUT = 3600 * 24 * 30
#AWS environment variables
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]

access_times = {}


@app.route("/download/<path:filename>")
def download(filename):
    path = os.path.join(CACHE_ROOT, filename)
    access_times[path] = time()
    # Check if the file exists and a file sync is not in progress
    if os.access(path, os.F_OK) is False and os.access(path + ".lock", os.F_OK) is False:
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(S3_BUCKET)
        k = Key(bucket, filename)
        url = k.generate_url(3600, query_auth=True, force_http=True)
        # Attempt to resync the missing file
        sync_thread = threading.Thread()
        sync_thread.run = lambda: sync_file(url, path)
        sync_thread.start()
        # Clear cache of files that haven't been accessed recently
        clear_thread = threading.Thread()
        clear_thread.run = lambda: clear_cache()
        clear_thread.start()
        return redirect(url, code=302)
    else:
        response = make_response()
        response.headers['Content-Type'] = ""
        response.headers['Content-Disposition'] = 'attachment; filename="%s"' % (os.path.basename(filename),)
        response.headers['X-Accel-Redirect'] = os.path.join("/internal-redirect", filename)

        return response


def sync_file(source, destination):
    if os.access(destination + ".lock", os.F_OK) is False:
        if os.access(os.path.dirname(destination), os.F_OK) is False:
            os.makedirs(os.path.dirname(destination))
        lock = open(destination + ".lock", 'w')
        lock.write("")
        lock.flush()
        lock.close()
        try:
            urllib.urlretrieve(source, destination)
        except Exception as e:
            print(e)
        finally:
            os.remove(destination + ".lock")


def clear_cache():
    ''' Removes files contained within [path] that have not
        been accessed recently within the [timeout] period.
    '''
    for root, dirs, files in os.walk(CACHE_ROOT):
        for name in files:
            path = os.path.join(root, name)
            if name in access_times:
                access_time = access_times[path]
            else:
                access_time = os.stat(path).st_atime
            if (time() - access_time) > CACHE_TIMEOUT:
                os.remove(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
