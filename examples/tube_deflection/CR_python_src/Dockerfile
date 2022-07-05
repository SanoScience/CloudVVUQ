FROM python:3.10-slim

COPY /app /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080:8080

CMD ["python3", "main.py"]