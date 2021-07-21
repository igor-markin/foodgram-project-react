FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update
RUN apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib netcat
RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY /. .
