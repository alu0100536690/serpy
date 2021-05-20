FROM ubuntu:focal

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends python3 python3-setuptools python3-pkg-resources \
    libffi-dev build-essential git libxml2-dev libxslt1-dev zlib1g-dev libssl-dev \
    python3-pip python3-dev -y


WORKDIR /app

COPY requirements.txt .


RUN pip3 install -r requirements.txt

COPY . .

CMD [ "flask", "run" ]
