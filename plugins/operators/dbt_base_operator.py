from os import environ

from airflow.compat.functools import cached_property
from airflow.hooks.subprocess import SubprocessHook
from airflow.models import BaseOperator
from airflow.utils.operator_helpers import context_to_airflow_vars


class DBTBaseOperator(BaseOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cwd = '/airflow/plugins/dbt'
        self.output_encoding: str = 'utf-8'
        self.skip_exit_code: int = 99

    @cached_property
    def subprocess_hook(self):
        """Returns hook for running the bash command"""
        return SubprocessHook()

    def get_env(self, context):
        """Builds the set of environment variables to be exposed for the bash command"""
        env = environ.copy()

        airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
        self.log.debug(
            'Exporting the following env vars:\n%s',
            '\n'.join(f"{k}={v}" for k, v in airflow_context_vars.items()),
        )
        env.update(airflow_context_vars)
        return env

    def on_kill(self) -> None:
        self.subprocess_hook.send_sigterm()
