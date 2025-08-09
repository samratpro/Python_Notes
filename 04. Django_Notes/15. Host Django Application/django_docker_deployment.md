# Django Docker Deployment Guide 🐳

Complete guide for deploying Django applications using Docker, Docker Compose, Nginx, and PostgreSQL on VPS.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Docker Configuration](#-docker-configuration)
- [Database Setup](#-database-setup)
- [Nginx Configuration](#-nginx-configuration)
- [SSL Certificate](#-ssl-certificate)
- [Production Deployment](#-production-deployment)
- [Environment Variables](#-environment-variables)
- [Useful Commands](#-useful-commands)
- [Monitoring & Logs](#-monitoring--logs)
- [Backup & Restore](#-backup--restore)
- [Troubleshooting](#-troubleshooting)

## Prerequisites

- 🖥️ VPS with Ubuntu/Debian (20.04+ recommended)
- 🔑 Root or sudo access
- 🌐 Domain name (optional but recommended)
- 🐳 Basic knowledge of Docker
- 🐍 Django project ready for deployment

## 🚀 Quick Start

```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo apt install docker-compose -y

# Clone this setup
git clone YOUR_PROJECT_URL
cd your-project
docker-compose up -d --build
```

## 📁 Project Structure

```
your-django-project/
├── app/                          # Your Django application
│   ├── manage.py
│   ├── requirements.txt
│   ├── myproject/
│   └── apps/
├── docker/
│   ├── nginx/
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   └── default.conf
│   └── django/
│       └── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env
├── .env.prod
└── README.md
```

## 🐳 Docker Configuration

### 1. Django Dockerfile

Create `docker/django/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY app/ /app/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

### 2. Requirements.txt

Create `app/requirements.txt`:

```txt
Django>=4.2,<5.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.0
python-decouple>=3.8
whitenoise>=6.5.0
pillow>=10.0.0
redis>=4.6.0
celery>=5.3.0
```

### 3. Docker Compose (Development)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: django_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: django_redis
    restart: unless-stopped

  web:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    container_name: django_web
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  nginx:
    build:
      context: .
      dockerfile: docker/nginx/Dockerfile
    container_name: django_nginx
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: unless-stopped

  celery:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    container_name: django_celery
    command: celery -A myproject worker -l info
    volumes:
      - media_volume:/app/media
    environment:
      - DEBUG=1
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 4. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: django_db_prod
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    restart: unless-stopped
    networks:
      - django_network

  redis:
    image: redis:7-alpine
    container_name: django_redis_prod
    restart: unless-stopped
    networks:
      - django_network

  web:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    container_name: django_web_prod
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - "8000"
    environment:
      - DEBUG=0
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - django_network

  nginx:
    build:
      context: .
      dockerfile: docker/nginx/Dockerfile
    container_name: django_nginx_prod
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./docker/nginx/ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - django_network

  celery:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    container_name: django_celery_prod
    command: celery -A myproject worker -l info
    volumes:
      - media_volume:/app/media
    environment:
      - DEBUG=0
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - django_network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  django_network:
    driver: bridge
```

## 🗃️ Database Setup

### Django Settings for Docker

Update `app/myproject/settings.py`:

```python
import os
from decouple import config

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Redis
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not config('DEBUG', default=False, cast=bool):
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

## 🌐 Nginx Configuration

### 1. Nginx Dockerfile

Create `docker/nginx/Dockerfile`:

```dockerfile
FROM nginx:alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/default.conf /etc/nginx/conf.d/

# Create directories
RUN mkdir -p /etc/nginx/ssl

# Expose ports
EXPOSE 80 443
```

### 2. Main Nginx Config

Create `docker/nginx/nginx.conf`:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    include /etc/nginx/conf.d/*.conf;
}
```

### 3. Site Configuration

Create `docker/nginx/default.conf`:

```nginx
upstream django {
    server web:8000;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    location / {
        proxy_pass http://django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /app/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Favicon
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    # Robots.txt
    location = /robots.txt {
        access_log off;
        log_not_found off;
    }
}
```

## 🔐 SSL Certificate

### Option 1: Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot -y

# Stop nginx temporarily
docker-compose -f docker-compose.prod.yml stop nginx

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Copy certificates to docker volume
sudo mkdir -p ./docker/nginx/ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./docker/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./docker/nginx/ssl/key.pem

# Restart nginx
docker-compose -f docker-compose.prod.yml up -d nginx
```

### Option 2: Using Docker Certbot

Add to `docker-compose.prod.yml`:

```yaml
  certbot:
    image: certbot/certbot
    container_name: django_certbot
    volumes:
      - ./docker/nginx/ssl:/etc/letsencrypt
      - ./docker/nginx/www:/var/www/certbot
    command: certonly --webroot --webroot-path=/var/www/certbot --email your-email@domain.com --agree-tos --no-eff-email -d your-domain.com -d www.your-domain.com
```

## 🚀 Production Deployment

### 1. Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reboot to apply group changes
sudo reboot
```

### 2. Deploy Application

```bash
# Clone your project
git clone YOUR_PROJECT_URL /opt/django-app
cd /opt/django-app

# Create production environment file
cp .env.example .env.prod

# Edit environment variables
nano .env.prod

# Build and run containers
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 🔐 Environment Variables

### Development (.env)

```env
DEBUG=1
SECRET_KEY=your-secret-key-here
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=django_password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (.env.prod)

```env
DEBUG=0
SECRET_KEY=your-super-secret-production-key
DB_NAME=django_prod_db
DB_USER=django_prod_user
DB_PASSWORD=super-secure-password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🛠️ Useful Commands

### Docker Management

```bash
# Build and start services
docker-compose up -d --build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate

# Rebuild specific service
docker-compose up -d --build web

# Remove all containers and volumes (CAUTION!)
docker-compose down -v
docker system prune -a
```

### Django Commands

```bash
# Migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

### Database Commands

```bash
# Access PostgreSQL
docker-compose exec db psql -U django_user -d django_db

# Create database backup
docker-compose exec db pg_dump -U django_user django_db > backup.sql

# Restore database
docker-compose exec -T db psql -U django_user -d django_db < backup.sql
```

## 📊 Monitoring & Logs

### Log Management

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db

# View last N lines
docker-compose logs --tail=100 web

# Filter logs by time
docker-compose logs --since=1h web
```

### Health Checks

Add to your Django `docker-compose.yml`:

```yaml
  web:
    # ... other configurations
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 💾 Backup & Restore

### Automated Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
PROJECT_DIR="/opt/django-app"

mkdir -p $BACKUP_DIR

# Database backup
docker-compose -f $PROJECT_DIR/docker-compose.prod.yml exec -T db pg_dump -U django_user django_db > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
docker run --rm -v django-app_media_volume:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/media_backup_$DATE.tar.gz -C /data .

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### Restore Script

Create `scripts/restore.sh`:

```bash
#!/bin/bash
BACKUP_FILE=$1
MEDIA_BACKUP=$2

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore.sh <backup_file.sql> [media_backup.tar.gz]"
    exit 1
fi

# Restore database
docker-compose -f docker-compose.prod.yml exec -T db psql -U django_user -d django_db < $BACKUP_FILE

# Restore media files (if provided)
if [ ! -z "$MEDIA_BACKUP" ]; then
    docker run --rm -v django-app_media_volume:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/$MEDIA_BACKUP"
fi

echo "Restore completed"
```

## 🚨 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker-compose logs web
   
   # Check container status
   docker-compose ps
   
   # Rebuild container
   docker-compose up -d --build web
   ```

2. **Database connection errors**
   ```bash
   # Check if database is running
   docker-compose ps db
   
   # Check database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

3. **Static files not loading**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   
   # Check nginx logs
   docker-compose logs nginx
   
   # Restart nginx
   docker-compose restart nginx
   ```

4. **Permission issues**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER .
   
   # Check container user
   docker-compose exec web id
   ```

5. **SSL certificate issues**
   ```bash
   # Check certificate files
   ls -la docker/nginx/ssl/
   
   # Test SSL
   openssl s_client -connect your-domain.com:443
   
   # Check nginx SSL config
   docker-compose exec nginx nginx -t
   ```

### Performance Optimization

1. **Docker optimization**
   ```dockerfile
   # Multi-stage build
   FROM python:3.11-slim as builder
   # ... build dependencies
   
   FROM python:3.11-slim as runtime
   # ... copy only needed files
   ```

2. **Database optimization**
   ```yaml
   db:
     # ... other config
     command: postgres -c 'max_connections=200' -c 'shared_buffers=256MB'
   ```

3. **Nginx caching**
   ```nginx
   # Add to nginx config
   location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Best Practices](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Nginx Docker Hub](https://hub.docker.com/_/nginx)

## 🤝 Contributing

Feel free to submit issues and pull requests to improve this guide.

## 📄 License

This guide is available under the MIT License.

---

**🐳 Happy Dockerizing!**