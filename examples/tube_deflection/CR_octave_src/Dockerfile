FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Warsaw"

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y octave && \
    apt-get install -y nano

COPY /app /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080:8080

CMD ["python3", "main.py"]