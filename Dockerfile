FROM ubuntu:focal

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

RUN apt-get update && apt-get upgrade -y

RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

RUN ln -sfn /usr/share/zoneinfo/Europe/Madrid /etc/localtime

RUN apt-get install python3 python3-setuptools python3-pkg-resources \
    python3-pip python3-dev -y

RUN apt-get install libffi-dev build-essential git libxml2-dev libxslt1-dev zlib1g-dev libssl-dev -y

WORKDIR /app

COPY . .


RUN pip3 install -r requirements.txt

CMD [ "flask", "run" ]
