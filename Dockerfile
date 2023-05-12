FROM python:3.10-alpine

WORKDIR /home/pr_user

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . .

ENV FLASK_APP run.py

EXPOSE 5000
CMD gunicorn