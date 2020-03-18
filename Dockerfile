FROM python:3.7

RUN apt-get update
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN django-admin startproject project .; \
    mv ./project ./origproject
