#!/usr/bin/env bash
# Runs at postgres container init time (before 01_schema.sql).
# Creates the 'evolution' database for Evolution API.
# The main 'belpro' database is created automatically via POSTGRES_DB.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE evolution;
    GRANT ALL PRIVILEGES ON DATABASE evolution TO $POSTGRES_USER;
    CREATE DATABASE belpro_test_migrations;
    GRANT ALL PRIVILEGES ON DATABASE belpro_test_migrations TO $POSTGRES_USER;
EOSQL
