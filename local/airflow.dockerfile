FROM python:3.9 AS base_airflow

WORKDIR /airflow
RUN useradd -s /bin/bash -d /airflow airflow

ENV AIRFLOW_HOME=/airflow

COPY ../requirements.txt .

RUN python -m venv airflow_venv
RUN ./airflow_venv/bin/pip install -r requirements.txt
RUN ./airflow_venv/bin/pip install apache-airflow[postgres,celery,redis]==2.2.3 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.9.txt"

COPY airflow/airflow.cfg .
COPY profiles.yml .dbt/profiles.yml
COPY local/wait_for_it.sh .

ENV PATH="/airflow/airflow_venv/bin:$PATH"
ENV PYTHONPATH="/airflow/custom_operators:$PYTHONPATH"
RUN chown -R airflow: /airflow
