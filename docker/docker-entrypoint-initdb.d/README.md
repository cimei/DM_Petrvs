This directory is mounted into the Superset Postgres container at /docker-entrypoint-initdb.d.

Any .sql or .sh files placed here will be executed by the Postgres image when the database is initialized for the first time.

Current files:
- 01-init-superset.sql: placeholder no-op file. Edit or add additional scripts as needed.