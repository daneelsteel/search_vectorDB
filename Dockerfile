FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y -q apt-utils python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY query.py .
#ARG PROJECT=owl
#ARG PROJECT_DIR=/${PROJECT}
#RUN mkdir -p $PROJECT_DIR
#WORKDIR $PROJECT_DIR

#FROM ubuntu:latest

#ENV PATH /usr/local/python3/bin

#RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
#RUN apt-get install -y -q apt-utils python3-pip
#RUN apt-get update && \
#    apt-get install -y gunicorn

#COPY requirements.txt .
#RUN pip install -r requirements.txt

