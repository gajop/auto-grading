FROM ubuntu

MAINTAINER Gajo Petrovic, gajop01@gmail.com

RUN echo 'deb http://archive.ubuntu.com/ubuntu precise main universe' > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y -q python-pip
RUN apt-get install -y -q octave

ADD invoker.py invoker.py
ADD runner.m runner.m
