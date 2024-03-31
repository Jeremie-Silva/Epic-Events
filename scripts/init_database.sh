#!/bin/bash

# This script will create your postgres user and database based on your .env file
# This end line is for clean warnings messages about permissions : 2>/dev/null

source .env

sudo -u postgres psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';" 2>/dev/null

sudo -u postgres psql -c "ALTER USER ${POSTGRES_USER} CREATEDB;" 2>/dev/null

sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB};" 2>/dev/null

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};" 2>/dev/null

alembic upgrade head