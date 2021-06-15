FROM python:3.8-buster

ADD requirements_docker.txt /tmp/requirements_docker.txt

RUN pip3 install -r /tmp/requirements_docker.txt

COPY app /app/app

COPY config.py /app/config.py
COPY init_db.py /app/init_db.py
COPY wsgi.py /app/wsgi.py
COPY docker_entry.sh /app/docker_entry.sh

WORKDIR /app

RUN chmod +x  docker_entry.sh
CMD ./docker_entry.sh

