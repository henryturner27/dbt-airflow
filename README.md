# Dockerized Airflow with DBT

This is a dockerized implementation of the open-source job scheduler: [Airflow](https://airflow.apache.org) integrated with [DBT](https://www.getdbt.com) to facilitate end-to-end data pipelining.

## Requirements

- Docker

---

## To Run

- `docker-compose build` (this step will take several minutes on the first run)
- `docker-compose up`

This builds the postgres, redis, webserver, scheduler, flower, docs, and worker containers. You can find the web UI for some of these containers at the following addresses:

- airflow webserver: http://localhost:8080
- airflow flower: http://localhost:5555
- dbt docs: http://localhost:8000

You can connect to the postgres data warehouse in one of two ways:

1. By stepping into the container and directly running psql commands
   - `docker exec -it dbtpostgres bash` (to step into the container)
   - `psql -U first_last -d first_last` (to connect to the DB)
1. By connecting through localhost using your favorite database client
   - host: localhost
   - db: first_last
   - port: 5432
   - user: first_last
   - pw: example_pw

### Shutdown

- `docker-compose down`

---

## Contributing

**NOTE:** For the smoothest experience I recommend using the VS Code editor.

In order to contribute you will need to setup your local development environment by installing [python 3.9](https://www.python.org/downloads/release/python-399) and creating a virtual environment at the root directory of this project, like so:

- `python3.9 -m venv airflow_venv`
- `source ./airflow_venv/bin/activate`
- `pip install 'apache-airflow[postgres,celery,redis]==2.2.3' --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.9.txt"`
- `pip install -r local/requirements-dev.txt`

You can now manually set your python interpretor to ./airflow_venv/bin/python, or close and re-open VS Code for it to be automatically set. Following these steps will give you access to intellisense as well as conforming your code to the auto-formatting and linting standards of this project.

### Adding new DAGs

Create a new Airflow DAG in the `airflow/dags/` directory
