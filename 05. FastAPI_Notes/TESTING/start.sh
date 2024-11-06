#!/bin/bash

# Prompt for project name
read -p "Enter project name: " PROJECT_NAME

# Check if project name is provided
if [ -z "$PROJECT_NAME" ]; then
    echo "Project name cannot be empty. Please run the script again and provide a valid project name."
    exit 1
fi

# Create project directories
mkdir -p $PROJECT_NAME/{config,logs,models,routers,schemas,static,templates,user_app,nginx,.github/workflows}

# Create initial files

# Main app file
cat <<EOF > $PROJECT_NAME/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
EOF

# Dockerfile for FastAPI
cat <<EOF > $PROJECT_NAME/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
EOF

# Requirements file
cat <<EOF > $PROJECT_NAME/requirements.txt
fastapi
uvicorn[standard]
psycopg2-binary
celery[redis]
alembic
EOF

# Docker Compose file
cat <<EOF > $PROJECT_NAME/docker-compose.yml
version: '3.9'

services:
  web:
    build: .
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest

  worker:
    build: .
    command: ["celery", "-A", "config.celery_app", "worker", "--loglevel=info"]
    volumes:
      - .:/app
    depends_on:
      - redis
      - db

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/ssl/certs
      - ./nginx/ssl:/etc/ssl/private
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
EOF

# Celery configuration
mkdir -p $PROJECT_NAME/config
cat <<EOF > $PROJECT_NAME/config/celery.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["tasks"]
)

celery_app.conf.task_routes = {
    "tasks.example_task": "main-queue",
}

celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json")

if __name__ == "__main__":
    celery_app.start()
EOF

# Example Celery task
cat <<EOF > $PROJECT_NAME/tasks.py
from config.celery import celery_app

@celery_app.task
def example_task(x, y):
    return x + y
EOF

# Nginx configuration for HTTPS
mkdir -p $PROJECT_NAME/nginx/ssl
cat <<EOF > $PROJECT_NAME/nginx/nginx.conf
events {}

http {
    server {
        listen 80;
        server_name your_domain.com;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }

    server {
        listen 443 ssl;
        server_name your_domain.com;

        ssl_certificate /etc/ssl/certs/fullchain.pem;
        ssl_certificate_key /etc/ssl/private/privkey.pem;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

# Entrypoint script for database migration
cat <<EOF > $PROJECT_NAME/entrypoint.sh
#!/bin/bash

# Wait for the database to be ready
while !</dev/tcp/db/5432; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

# Run database migrations
alembic upgrade head

# Start the application
exec "\$@"
EOF

# Alembic configuration for database migrations
cat <<EOF > $PROJECT_NAME/alembic.ini
[alembic]
script_location = alembic

[alembic:ini]
sqlalchemy.url = postgresql://user:password@db/dbname
EOF

mkdir -p $PROJECT_NAME/alembic
cat <<EOF > $PROJECT_NAME/alembic/env.py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF

# Alembic script for initial migration
mkdir -p $PROJECT_NAME/alembic/versions
cat <<EOF > $PROJECT_NAME/alembic/versions/0001_initial.py
"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2023-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass


def downgrade():
    pass
EOF

# Git ignore file
cat <<EOF > $PROJECT_NAME/.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
*.log
*.pot
*.mo
*.env
.DS_Store
EOF

# Create the directories and initial files as shown in the image
touch $PROJECT_NAME/config/__init__.py
touch $PROJECT_NAME/logs/info.log
touch $PROJECT_NAME/models/database.py
touch $PROJECT_NAME/models/models.py
touch $PROJECT_NAME/routers/__init__.py
touch $PROJECT_NAME/routers/home.py
touch $PROJECT_NAME/routers/users.py
touch $PROJECT_NAME/schemas/items.py
touch $PROJECT_NAME/schemas/users.py
touch $PROJECT_NAME/static/favicon.ico
touch $PROJECT_NAME/templates/base.html
touch $PROJECT_NAME/user_app/login_register.py
touch $PROJECT_NAME/user_app/.env
touch $PROJECT_NAME/readme.md

# GitHub Actions workflow for CI/CD
cat <<EOF > $PROJECT_NAME/.github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: dbname
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:latest
        ports:
          - 6379:6379

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Alembic migrations
      run: |
        alembic upgrade head

    - name: Run tests
      run: |
        # Add your test command here
        echo "Running tests"
EOF

echo "FastAPI project structure with PostgreSQL, Celery, Redis, Nginx, and GitHub Actions for CI/CD has been created."

# Prompt for domain name for Nginx configuration
read -p "Enter your domain name: " DOMAIN_NAME

# Replace placeholder domain in nginx.conf
sed -i "s/your_domain.com/$DOMAIN_NAME/g" $PROJECT_NAME/nginx/nginx.conf

# Install Certbot and obtain SSL certificate
docker run -it --rm --name certbot \
  -v "$(pwd)/$PROJECT_NAME/nginx/ssl:/etc/letsencrypt" \
  certbot/certbot certonly --standalone --preferred-challenges http \
  --agree-tos --no-eff-email --email your_email@example.com -d $DOMAIN_NAME

echo "SSL certificate obtained and saved to nginx/ssl directory."
echo "Project setup is complete. Navigate to the project directory and run 'docker-compose up --build' to start your application."
