# Dockerized Airflow with DBT

This is a dockerized implementation of the open-source job scheduler: [Airflow](https://airflow.apache.org). This uses the Celery message broker with Redis as a backend to support running multiple tasks in parallel.

### Requirements

* Docker

### To Run

* `docker-compose build`
* `docker-compose up --scale worker=2`

This builds the postgres, redis, webserver, scheduler, flower, docs, and 2 worker containers. You can find the web UI for some of these containers at the following addresses:

* airflow webserver: http://localhost:8080
* airflow flower: http://localhost:5555
* dbt docs: http://localhost:8000

You can connect to the postgres data warehouse in one of two ways:
1. By stepping into the container and directly running psql commands
    * `docker exec -it dbtpostgres bash` (to step into the container)
    * `psql -U dbt -d dbt` (to connect to the DB)
1. By connecting through localhost using your favorite database client
    * host: localhost
    * db: dbt
    * port: 5432
    * user: dbt
    * pw: example_pw

### Shutdown

* `docker-compose down`

### Adding new DAGs

Create a new python file in the dags/ directory, making sure that all of the underlying tasks have their upstream dependencies designated correctly, a unique name has been assigned, and that other configuration arguments are set as desired.
