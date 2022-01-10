from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


dag_name = 'agg_users'
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=15),
}
dag_args = {
    'start_date': datetime(2021, 12, 23),
    'schedule_interval': '@daily',
    'catchup': False,
    'max_active_runs': 10,
}

with DAG(dag_name, default_args=default_args, **dag_args) as dag:
    start_task = DummyOperator(task_id='start_task')

    stage_task = BashOperator(
        task_id=f'dbt_run-{dag_name}_stage',
        bash_command=f'''
                cd ~/dwh &&
                dbt run -m {dag_name}_stage --vars \'{{"ds":"{{{{ ds }}}}","ds_no_dash":"{{{{ ds_nodash }}}}"}}\'
            ''',
        dag=dag)

    test_task = BashOperator(
        task_id=f'dbt_test-{dag_name}',
        bash_command=f'''
            cd ~/dwh &&
            dbt test -m {dag_name}_stage --vars \'{{"ds_no_dash":"{{{{ ds_nodash }}}}"}}\'''',
        dag=dag)

    load_task = BashOperator(
        task_id=f'dbt_run-{dag_name}',
        bash_command=f'''
                cd ~/dwh &&
                dbt run -m {dag_name} --vars \'{{"ds":"{{{{ ds }}}}","ds_no_dash":"{{{{ ds_nodash }}}}"}}\'
            ''',
        dag=dag)

    end_task = DummyOperator(task_id='end_task')

    start_task >> stage_task >> test_task >> load_task >> end_task
