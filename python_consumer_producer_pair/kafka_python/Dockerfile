FROM python:3.6.8

RUN apt-get update && \
	apt-get -y install bash git ca-certificates

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache -r requirements.txt

COPY applications_and_output/kafka_producer.py kafka_producer.py
COPY applications_and_output/kafka_consumer.py kafka_consumer.py

