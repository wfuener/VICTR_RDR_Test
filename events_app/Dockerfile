FROM python:3.10-slim-bookworm

WORKDIR /app
ADD . /app

RUN apt-get update -y
RUN apt-get install gcc python3-dev libpq-dev -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT uvicorn --port 8000 app:api