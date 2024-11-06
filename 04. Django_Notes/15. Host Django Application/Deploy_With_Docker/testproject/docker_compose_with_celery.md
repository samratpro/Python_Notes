version: '3'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user2
      POSTGRES_PASSWORD: password2
      POSTGRES_DB: test_db2
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"

  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: /opt/app/entrypoint.sh
    volumes:
      - .:/opt/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - celery_worker_app1
      - celery_worker_app2
    environment:
      DATABASE_URL: postgres://user2:password2@db:5432/test_db2

  nginx:
    image: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    depends_on:
      - web

  certbot:
    image: certbot/certbot
    volumes:
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait 346{!}; done;'"

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  celery_worker_app1:
    build: .
    command: celery -A testproject worker -Q app1 -l info
    # command: celery -A testproject worker -Q app1 -1 info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user2:password2@db:5432/test_db2
      - REDIS_URL=redis://redis:6379

  celery_worker_app2:
    build: .
    command: celery -A testproject worker -Q app2 --loglevel=info
    # command: celery -A testproject worker -Q app2 --loglevel=info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user2:password2@db:5432/test_db2
      - REDIS_URL=redis://redis:6379

volumes:
  postgres_data:
