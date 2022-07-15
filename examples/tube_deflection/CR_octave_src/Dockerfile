FROM ubuntu:20.04

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Warsaw"
ENV PORT=${PORT:-8080}

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y octave && \
    apt-get install -y nano && \
    apt-get clean

COPY /app /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app