FROM python:3.10

WORKDIR /docs
RUN useradd -s /bin/bash -d /docs docs

RUN pip install dbt-postgres==1.6

RUN chown -R docs: /docs
