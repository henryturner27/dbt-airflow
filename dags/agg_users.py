from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


dag_name = 'agg_users'
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(seconds=15),
}

with DAG(dag_name, default_args=default_args, schedule_interval=None) as dag:
    start_task = DummyOperator(task_id='start_task')

    stage_task = BashOperator(
        task_id=f'dbt_run-{dag_name}_stage',
        bash_command='cd ~/bungie_dwh && dbt run -m {dag_name}_stage --vars \'{{"ds":"{{{{ ds }}}}"}}\''.format(
            dag_name=dag_name),
        dag=dag)

    test_task = BashOperator(
        task_id=f'dbt_test-{dag_name}',
        bash_command=f'cd ~/bungie_dwh && dbt test -m {dag_name}_stage',
        dag=dag)

    load_task = BashOperator(
        task_id=f'dbt_run-{dag_name}',
        bash_command='cd ~/bungie_dwh && dbt run -m {dag_name} --vars \'{{"ds":"{{{{ ds }}}}"}}\''.format(
            dag_name=dag_name),
        dag=dag)

    end_task = DummyOperator(task_id='end_task')

    start_task >> stage_task >> test_task >> load_task >> end_task
