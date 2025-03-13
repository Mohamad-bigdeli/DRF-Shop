FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

RUN sed -i 's/http:\/\/[a-zA-Z0-9]*.[a-zA-Z0-9]*.*.com/http:\/\/ir.ubuntu.sindad.cloud/g' /etc/apt/sources.list

COPY requirements.txt /app/

RUN pip3 install --upgrade pip==23.3.1
RUN pip3 install -r requirements.txt 
COPY ./core /app/