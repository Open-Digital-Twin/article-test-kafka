FROM python:3.6.15-slim

RUN apt-get update && \
	apt-get -y install bash git vim ca-certificates

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache -r requirements.txt

RUN pip3 install kafka

RUN pip3 install kafka-python

COPY /applications/kafka_producer.py kafka_producer.py
COPY /applications/kafka_consumer.py kafka_consumer.py
COPY /applications/kafka_topic_creation.py kafka_topic_creation.py
