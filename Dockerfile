FROM python:3.8


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN  pip install --upgrade pip && pip install -r requirements.txt 

WORKDIR /code

COPY . /code/

RUN apt update && apt install -y libpq-dev gcc

RUN pip install psycopg2