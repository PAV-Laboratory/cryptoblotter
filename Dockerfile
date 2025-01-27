FROM python:3.9-slim-buster

ARG PROJECT_ID
ARG SENTRY_DSN

ENV PROJECT_ID $PROJECT_ID
ENV SENTRY_DSN $SENTRY_DSN

ADD requirements.txt /

ADD cryptoblotter /cryptoblotter/
ADD main.py /

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/main.py"]
