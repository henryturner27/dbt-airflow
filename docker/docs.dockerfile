FROM python:3.9

WORKDIR /docs
RUN useradd -s /bin/bash -d /docs docs

RUN pip install dbt-postgres==1.0.0

COPY dwh/ .
COPY profiles.yml .dbt/profiles.yml
COPY docker/wait_for_it.sh dwh/wait_for_it.sh

RUN chown -R docs: /docs
