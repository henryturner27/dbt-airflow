FROM python:3.10

WORKDIR /airflow
RUN useradd -s /bin/bash -d /airflow airflow

ENV AIRFLOW_HOME=/airflow

COPY requirements.txt .
COPY constraints.txt .
COPY cfg/local/airflow.cfg .

RUN python -m venv airflow_venv
RUN ./airflow_venv/bin/pip install -r requirements.txt


RUN chown -R airflow: /airflow
