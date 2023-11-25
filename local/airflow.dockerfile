FROM python:3.10

WORKDIR /airflow
RUN useradd -s /bin/bash -d /airflow airflow

ENV AIRFLOW_HOME=/airflow

COPY ../requirements.txt .
COPY constraints.txt .

RUN python -m venv airflow_venv
RUN ./airflow_venv/bin/pip install -r requirements.txt

COPY airflow/airflow.cfg .
COPY profiles.yml .dbt/profiles.yml

RUN chown -R airflow: /airflow
