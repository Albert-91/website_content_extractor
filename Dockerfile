FROM python:3.7

RUN apt-get update

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    postgresql \
    postgresql-contrib

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY wait_for_postgres.sh .
RUN django-admin startproject project .; \
    mv ./project ./origproject
