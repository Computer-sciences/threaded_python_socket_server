FROM ubuntu

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y make
RUN apt-get install -y python
RUN apt-get install -y pip
RUN pip install -y psutil

VOLUME /root/env
WORKDIR /root/env