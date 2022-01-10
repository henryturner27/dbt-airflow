FROM python:3.9

WORKDIR /docs
RUN useradd -s /bin/bash -d /docs docs

COPY dbt_requirements.txt .
RUN pip install -r dbt_requirements.txt

COPY dwh/ .
COPY profiles.yml .dbt/profiles.yml
COPY wait_for_it.sh dwh/wait_for_it.sh

RUN chown -R docs: /docs
