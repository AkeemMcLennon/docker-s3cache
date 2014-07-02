/etc/init.d/nginx start
#Used mainly to start the chat socket server and anything else initialized in manage.py
uwsgi uwsgi.ini
tail -f /var/log/nginx/error.log
