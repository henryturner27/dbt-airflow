from datetime import datetime, timedelta
from os import getenv

from airflow import DAG
from custom_operators.dbt_run_operator import DBTRunOperator
from custom_operators.dbt_test_operator import DBTTestOperator
from custom_operators.dbt_docs_operator import DBTDocsOperator
from airflow.operators.dummy import DummyOperator


dag_name = 'core__agg_users'
dbt_model = dag_name.split('__')[1]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=15),
}
dag_args = {
    'description': 'Calculates aggregations at the user level.',
    'start_date': datetime(2021, 12, 23),
    'schedule_interval': '@daily',
    'catchup': False,
    'max_active_runs': 10,
}

with DAG(dag_name, default_args=default_args, **dag_args) as dag:
    start_task = DummyOperator(task_id='start_task')

    stage_task = DBTRunOperator(
        task_id=f'dbt_run-{dag_name}_stage',
        dbt_model=f'{dbt_model}_stage',
        dag=dag
    )

    test_task = DBTTestOperator(
        task_id=f'dbt_test-{dag_name}',
        dbt_model=f'{dbt_model}_stage',
        dag=dag
    )

    load_task = DBTRunOperator(
        task_id=f'dbt_run-{dag_name}',
        dbt_model=dbt_model,
        dag=dag
    )

    end_task = DummyOperator(task_id='end_task')

    if (getenv('ENV') == 'dev'):
        update_docs_task = DBTDocsOperator(
            task_id=f'dbt_docs_generate-{dag_name}',
            dag=dag
        )
        load_task >> update_docs_task >> end_task

    start_task >> stage_task >> test_task >> load_task >> end_task
