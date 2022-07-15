FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV PORT=${PORT:-8080}

COPY /app /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir fipy  # somehow doesn't work in requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app