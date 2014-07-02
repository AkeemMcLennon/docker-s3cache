FROM ubuntu:trusty
RUN sudo apt-get update
RUN sudo apt-get -y install build-essential python-pip python-dev
RUN sudo pip install flask boto uwsgi
VOLUME /var/www
RUN mkdir /home/s3cache
RUN sudo apt-get -y install nginx-full
WORKDIR /home/s3cache
ADD download.py /home/s3cache/
ADD s3cache.conf /etc/nginx/sites-enabled/default
ADD uwsgi.ini /home/s3cache/uwsgi.ini
ADD start.sh /home/s3cache/
CMD sh start.sh
EXPOSE 80
