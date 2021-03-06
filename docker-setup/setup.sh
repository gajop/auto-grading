#!/bin/bash
BASEDIR=$(dirname $0)

#copy files
cp $BASEDIR/../webservice/matlab/invoker.py .
cp $BASEDIR/../webservice/matlab/runner.m .
cp $BASEDIR/../webservice/command.py .

#build docker
docker build -t grading .

#clean up
rm invoker.py
rm runner.m
rm command.py
