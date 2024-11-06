#!/bin/sh

alembic init alembic
alembic revision -m "first migrations"
alembic upgrade head
# Start the application
exec "$@"