FROM python:3.9 AS base_airflow

WORKDIR /airflow
RUN useradd -s /bin/bash -d /airflow airflow

ENV AIRFLOW_HOME=/airflow

COPY airflow_requirements.txt .

RUN python -m venv airflow_venv
RUN ./airflow_venv/bin/pip install -r airflow_requirements.txt

COPY dbt_requirements.txt dbt_requirements.txt

RUN python -m venv dbt_venv
RUN dbt_venv/bin/pip install -r dbt_requirements.txt

COPY airflow.cfg .
COPY profiles.yml .dbt/profiles.yml
COPY wait_for_it.sh .

ENV PATH="./airflow_venv/bin:$PATH"
RUN chown -R airflow: /airflow
