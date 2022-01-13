from datetime import datetime, timedelta
from json import dumps
from os import getenv

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


dag_name = 'core__agg_users'
dbt_name = dag_name.split('__')[1]

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
json_args = dumps(
    {
        'ds': '{{ ds }}',
        'ds_nodash': '{{ ds_nodash }}',
    }
)

with DAG(dag_name, default_args=default_args, **dag_args) as dag:
    start_task = DummyOperator(task_id='start_task')

    stage_task = BashOperator(
        task_id=f'dbt_run-{dag_name}_stage',
        bash_command=f'''
                cd ~/dwh &&
                dbt run -m {dbt_name}_stage --vars '{json_args}'
            ''',
        dag=dag
    )

    test_task = BashOperator(
        task_id=f'dbt_test-{dag_name}',
        bash_command=f'''
                cd ~/dwh &&
                dbt test -m {dbt_name}_stage --store-failures --vars '{json_args}'
            ''',
        dag=dag
    )

    load_task = BashOperator(
        task_id=f'dbt_run-{dag_name}',
        bash_command=f'''
                cd ~/dwh &&
                dbt run -m {dbt_name} --vars '{json_args}'
            ''',
        dag=dag
    )

    end_task = DummyOperator(task_id='end_task')

    if (getenv('ENV') == 'dev'):
        update_docs_task = BashOperator(
            task_id=f'dbt_docs_generate-{dag_name}',
            bash_command=f'''
                cd ~/dwh &&
                dbt docs generate --vars '{json_args}'
                ''',
            dag=dag
        )
        load_task >> update_docs_task >> end_task

    start_task >> stage_task >> test_task >> load_task >> end_task
