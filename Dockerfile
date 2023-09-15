# syntax=docker/dockerfile:1

FROM python:3.5

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

ENV ENV=DEV
RUN apt-get install -y libgdal-dev
RUN apt-get install -y cron
RUN apt-get install -y vim nano


COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]