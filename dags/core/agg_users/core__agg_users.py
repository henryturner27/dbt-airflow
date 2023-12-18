from datetime import datetime

from airflow import DAG
from operators.dbt_run_operator import DBTRunOperator
from operators.dbt_test_operator import DBTTestOperator
from airflow.operators.empty import EmptyOperator


dag_name = 'core__agg_users'
dbt_model = dag_name.split('__')[1]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': 15,
}
dag_args = {
    'dag_id': dag_name,
    'description': 'Calculates aggregations at the user level.',
    'start_date': datetime(2021, 12, 23),
    'schedule_interval': '@daily',
    'catchup': False,
    'max_active_runs': 10,
}

with DAG(default_args=default_args, **dag_args) as dag:
    start_task = EmptyOperator(task_id='start_task')

    stage_task = DBTRunOperator(
        task_id=f'dbt_run-{dag_name}_stage',
        dbt_model=f'{dbt_model}_stage',
    )

    test_task = DBTTestOperator(
        task_id=f'dbt_test-{dag_name}',
        dbt_model=f'{dbt_model}_stage',
    )

    load_task = DBTRunOperator(
        task_id=f'dbt_run-{dag_name}',
        dbt_model=dbt_model,
    )

    end_task = EmptyOperator(task_id='end_task')

    start_task >> stage_task >> test_task >> load_task >> end_task
