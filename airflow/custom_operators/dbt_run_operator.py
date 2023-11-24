from json import dumps
from typing import Dict

from airflow.exceptions import AirflowException, AirflowSkipException
from custom_operators.dbt_base_operator import DBTBaseOperator


class DBTRunOperator(DBTBaseOperator):
    def __init__(self, dbt_model: str, dbt_args: Dict[str, str] = {}, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dbt_args = dbt_args
        self.dbt_model = dbt_model

    def execute(self, context):
        dbt_args = dumps({'ds': context['ds'],
                          'ds_nodash': context['ds_nodash'],
                          **self.dbt_args})
        env = self.get_env(context)
        result = self.subprocess_hook.run_command(
            command=[
                'bash',
                '-c',
                f'dbt run -m {self.dbt_model} --vars \'{dbt_args}\'',
            ],
            env=env,
            output_encoding=self.output_encoding,
            cwd=self.cwd,
        )
        if self.skip_exit_code is not None and result.exit_code == self.skip_exit_code:
            raise AirflowSkipException(
                f'Bash command returned exit code {self.skip_exit_code}. Skipping.')
        elif result.exit_code != 0:
            raise AirflowException(
                f'''Bash command failed.
                 The command returned a non-zero exit code {result.exit_code}.'''
            )
        return result.output
