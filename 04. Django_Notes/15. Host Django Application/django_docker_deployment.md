# Django Docker Deployment Guide 🐳

Simple and dynamic Docker setup for Django with PostgreSQL, Redis, Nginx, and Celery.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Domain & SSL Setup](#-domain--ssl-setup)
- [Useful Commands](#-useful-commands)
- [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone project
git clone YOUR_PROJECT_URL
cd your-project

# Copy environment file
cp .env.example .env

# Development mode
docker compose up -d --build

# Production mode
ENV_MODE=production docker compose up -d --build
```

## 📁 Project Structure

```
django-project/
├── app/
│   ├── core/                    # Django project (settings, urls, wsgi)
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── apps/                    # Your Django apps
│   ├── static/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
├── docker/
│   ├── django/
│   │   └── Dockerfile
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
├── docker-compose.yml           # Single file for all environments
├── .env.example
├── .env                         # Git ignored
└── README.md
```

## 🐳 Docker Configuration

### 1. Django Dockerfile

Create `docker/django/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Build argument for environment mode
ARG ENV_MODE=development

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV_MODE=${ENV_MODE}

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ .

# Create directories
RUN mkdir -p staticfiles media

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Command will be overridden by docker-compose
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. Nginx Dockerfile

Create `docker/nginx/Dockerfile`:

```dockerfile
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/ssl

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Nginx Configuration

Create `docker/nginx/nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

# HTTP Server
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    client_max_body_size 20M;

    # For Let's Encrypt verification
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect to HTTPS if SSL is enabled
    location / {
        # Comment out next line if no SSL
        return 301 https://$host$request_uri;
        
        # Uncomment for HTTP-only mode
        # proxy_pass http://django;
        # proxy_set_header Host $host;
        # proxy_set_header X-Real-IP $remote_addr;
        # proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTPS Server (comment out if no SSL)
server {
    listen 443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};
    client_max_body_size 20M;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /app/media/;
        expires 7d;
    }

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
}
```

### 4. Single Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: django_db_${ENV_MODE:-dev}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${DB_NAME:-django_db}
      POSTGRES_USER: ${DB_USER:-django_user}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${DB_PORT:-5432}:5432"
    restart: ${RESTART_POLICY:-unless-stopped}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-django_user}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - django_network

  redis:
    image: redis:7-alpine
    container_name: django_redis_${ENV_MODE:-dev}
    ports:
      - "${REDIS_PORT:-6379}:6379"
    restart: ${RESTART_POLICY:-unless-stopped}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - django_network

  web:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        ENV_MODE: ${ENV_MODE:-development}
    container_name: django_web_${ENV_MODE:-dev}
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn core.wsgi:application 
             --bind 0.0.0.0:8000 
             --workers ${GUNICORN_WORKERS:-3}
             --timeout ${GUNICORN_TIMEOUT:-120}
             --reload"
    volumes:
      # Mount source code in dev mode only
      - ${DEV_MOUNT:-./app}:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "${WEB_PORT:-8000}:8000"
    environment:
      - ENV_MODE=${ENV_MODE:-development}
      - DEBUG=${DEBUG:-1}
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: ${RESTART_POLICY:-unless-stopped}
    networks:
      - django_network
    deploy:
      resources:
        limits:
          cpus: ${PROD_CPUS:-'2'}
          memory: ${PROD_MEM:-1G}

  nginx:
    build:
      context: .
      dockerfile: docker/nginx/Dockerfile
    container_name: django_nginx_${ENV_MODE:-dev}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./docker/nginx/ssl:/etc/nginx/ssl:ro
      - certbot_www:/var/www/certbot:ro
    ports:
      - "${HTTP_PORT:-80}:80"
      - "${HTTPS_PORT:-443}:443"
    environment:
      - DOMAIN=${DOMAIN:-localhost}
    depends_on:
      - web
    restart: ${RESTART_POLICY:-unless-stopped}
    networks:
      - django_network

  celery:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        ENV_MODE: ${ENV_MODE:-development}
    container_name: django_celery_${ENV_MODE:-dev}
    command: celery -A core worker -l ${CELERY_LOG_LEVEL:-info} --concurrency=${CELERY_WORKERS:-2}
    volumes:
      - ${DEV_MOUNT:-./app}:/app
      - media_volume:/app/media
    environment:
      - ENV_MODE=${ENV_MODE:-development}
      - DEBUG=${DEBUG:-1}
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: ${RESTART_POLICY:-unless-stopped}
    networks:
      - django_network

  celery-beat:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        ENV_MODE: ${ENV_MODE:-development}
    container_name: django_celery_beat_${ENV_MODE:-dev}
    command: celery -A core beat -l ${CELERY_LOG_LEVEL:-info}
    volumes:
      - ${DEV_MOUNT:-./app}:/app
    environment:
      - ENV_MODE=${ENV_MODE:-development}
      - DEBUG=${DEBUG:-1}
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: ${RESTART_POLICY:-unless-stopped}
    networks:
      - django_network

volumes:
  postgres_data:
  static_volume:
  media_volume:
  certbot_www:

networks:
  django_network:
    driver: bridge
```

### 5. Requirements

Create `app/requirements.txt`:

```txt
# Django
Django>=4.2,<5.0
gunicorn>=21.2.0
whitenoise>=6.6.0

# Database
psycopg2-binary>=2.9.0

# Cache & Queue
redis>=5.0.0
django-redis>=5.4.0

# Celery
celery>=5.3.0

# Environment
python-decouple>=3.8

# Optional utilities
pillow>=10.0.0
```

## ⚙️ Configuration

### Environment Variables

Create `.env.example`:

```env
# Environment Mode (development/production)
ENV_MODE=development

# Django Settings
DEBUG=1
SECRET_KEY=change-this-to-a-random-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=change-this-secure-password
DB_PORT=5432

# Redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379/0

# Ports (customize if needed)
WEB_PORT=8000
HTTP_PORT=80
HTTPS_PORT=443

# Domain (for production)
DOMAIN=your-domain.com

# Gunicorn Settings
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120

# Celery Settings
CELERY_WORKERS=2
CELERY_LOG_LEVEL=info

# Docker Settings
RESTART_POLICY=unless-stopped

# Production Resource Limits (leave empty for dev)
PROD_CPUS=2
PROD_MEM=1G

# Development: mount source code (set to empty in production)
DEV_MOUNT=./app
```

### Development .env

```env
ENV_MODE=development
DEBUG=1
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=devpassword123

GUNICORN_WORKERS=2
CELERY_WORKERS=1

DEV_MOUNT=./app
RESTART_POLICY=unless-stopped
```

### Production .env

```env
ENV_MODE=production
DEBUG=0
SECRET_KEY=super-secure-random-production-key-min-50-chars
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

DB_NAME=django_prod_db
DB_USER=django_prod_user
DB_PASSWORD=super-secure-database-password

DOMAIN=your-domain.com

GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
CELERY_WORKERS=4

# Empty to not mount source code in production
DEV_MOUNT=

RESTART_POLICY=always

PROD_CPUS=2
PROD_MEM=2G
```

### Django Settings

Update `app/core/settings.py`:

```python
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment
ENV_MODE = config('ENV_MODE', default='development')
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
    }
}

# Redis & Cache
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

# Production Security
if ENV_MODE == 'production' and not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
    
    CSRF_TRUSTED_ORIGINS = [
        f'https://{config("DOMAIN")}',
        f'https://www.{config("DOMAIN")}',
    ]
```

### Celery Setup

Create `app/core/celery.py`:

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

Update `app/core/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

## 🚀 Deployment

### Development

```bash
# Start all services
docker compose up -d --build

# View logs
docker compose logs -f

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Access at http://localhost:8000
```

### Production

```bash
# Update .env with production values
nano .env

# Build and start with production settings
ENV_MODE=production DEBUG=0 DEV_MOUNT= docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Django application..."

# Pull latest code
git pull origin main

# Rebuild containers
ENV_MODE=production DEBUG=0 DEV_MOUNT= docker compose up -d --build

# Wait for services
sleep 20

# Run migrations
docker compose exec -T web python manage.py migrate --noinput

# Collect static files
docker compose exec -T web python manage.py collectstatic --noinput --clear

# Restart services
docker compose restart web celery celery-beat

echo "✅ Deployment completed!"
```

Make executable:
```bash
chmod +x deploy.sh
```

## 🌐 Domain & SSL Setup

### Step 1: Point Domain to Your Server

Add these DNS records in your domain registrar:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 3600 |
| A | www | YOUR_SERVER_IP | 3600 |

Wait 5-10 minutes for DNS propagation.

### Step 2: Choose SSL Method

---

## 🔒 **Method 1: Certbot (Free SSL) - Recommended**

**Simple 3-step setup:**

```bash
# 1. Install Certbot
sudo apt update && sudo apt install certbot -y

# 2. Stop nginx temporarily
docker compose stop nginx

# 3. Get certificate (replace with your domain and email)
sudo certbot certonly --standalone \
    -d yourdomain.com \
    -d www.yourdomain.com \
    --email your@email.com \
    --agree-tos \
    --non-interactive
```

**Copy certificates to project:**

```bash
# Create SSL directory
mkdir -p ./docker/nginx/ssl

# Copy certificate files
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./docker/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./docker/nginx/ssl/key.pem

# Set permissions
sudo chmod 644 ./docker/nginx/ssl/cert.pem
sudo chmod 600 ./docker/nginx/ssl/key.pem
```

**Update your .env file:**

```bash
nano .env
```

Add/update:
```env
DOMAIN=yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Start nginx:**

```bash
docker compose up -d nginx
```

**Test your site:** https://yourdomain.com

### Auto-Renewal (Set it and forget it)

Create renewal script `ssl-renew.sh`:

```bash
#!/bin/bash
certbot renew --quiet
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /path/to/your/project/docker/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /path/to/your/project/docker/nginx/ssl/key.pem
docker compose -f /path/to/your/project/docker-compose.yml restart nginx
```

Make executable and add to crontab:

```bash
chmod +x ssl-renew.sh
sudo crontab -e

# Add this line (checks twice daily)
0 0,12 * * * /path/to/your/project/ssl-renew.sh
```

---

## 🔒 **Method 2: Cloudflare SSL (Easiest)**

**Best for beginners - No server setup needed!**

### Step-by-Step:

**1. Add domain to Cloudflare**
   - Go to https://cloudflare.com
   - Click "Add Site"
   - Enter your domain
   - Choose Free plan

**2. Update nameservers**
   - Cloudflare will show you 2 nameservers
   - Go to your domain registrar (GoDaddy, Namecheap, etc.)
   - Replace existing nameservers with Cloudflare's
   - Wait 5-30 minutes for propagation

**3. Configure SSL**
   - In Cloudflare dashboard: SSL/TLS → Overview
   - Set encryption mode to: **Full (strict)**

**4. Create origin certificate**
   - Go to: SSL/TLS → Origin Server
   - Click "Create Certificate"
   - Choose "Generate private key and CSR with Cloudflare"
   - Click "Create"

**5. Save certificates**

Copy the **Origin Certificate** and **Private Key**

```bash
# Create SSL directory
mkdir -p ./docker/nginx/ssl

# Create certificate file
nano ./docker/nginx/ssl/cert.pem
# Paste the Origin Certificate, save and exit

# Create key file
nano ./docker/nginx/ssl/key.pem
# Paste the Private Key, save and exit

# Set permissions
chmod 644 ./docker/nginx/ssl/cert.pem
chmod 600 ./docker/nginx/ssl/key.pem
```

**6. Update DNS in Cloudflare**
   - DNS → Records
   - Add A record: `@` → Your server IP → Proxy enabled (orange cloud)
   - Add A record: `www` → Your server IP → Proxy enabled (orange cloud)

**7. Update .env**

```bash
nano .env
```

Add/update:
```env
DOMAIN=yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**8. Restart services**

```bash
docker compose restart nginx web
```

**Benefits:**
- ✅ Free forever
- ✅ Auto-renewal (managed by Cloudflare)
- ✅ DDoS protection
- ✅ CDN included
- ✅ No certificate maintenance

---

## 🔒 **Method 3: Self-Signed (Development Only)**

**Warning:** Browsers will show "Not Secure" - Only for local testing!

```bash
# Generate certificate
mkdir -p ./docker/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ./docker/nginx/ssl/key.pem \
    -out ./docker/nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Dev/CN=localhost"

# Update .env
echo "DOMAIN=localhost" >> .env

# Restart nginx
docker compose restart nginx
```

Access: https://localhost (click "Advanced" → "Proceed to localhost")

---

## 🔍 Verify SSL Setup

```bash
# Check if certificates exist
ls -la ./docker/nginx/ssl/

# Test SSL locally
curl -k https://yourdomain.com

# Check nginx config
docker compose exec nginx nginx -t

# View nginx logs
docker compose logs nginx

# Check certificate expiry (Certbot only)
sudo certbot certificates
```

---

## 🚨 Troubleshooting SSL

**Issue: "SSL certificate not found"**
```bash
# Check if files exist
ls ./docker/nginx/ssl/
# Should show: cert.pem and key.pem

# If missing, repeat certificate creation steps
```

**Issue: "Connection refused"**
```bash
# Check if nginx is running
docker compose ps nginx

# Check firewall
sudo ufw status
sudo ufw allow 443/tcp

# Restart nginx
docker compose restart nginx
```

**Issue: "Certificate expired"**
```bash
# For Certbot - manually renew
sudo certbot renew
# Then copy certificates again

# For Cloudflare - certificates last 15 years
```

**Issue: "Your connection is not private"**
- For Certbot: Check domain DNS is correct
- For Cloudflare: Wait 5 minutes after DNS setup
- For Self-signed: This is normal, click "Advanced" → "Proceed"

## 🛠️ Useful Commands

### Docker Management

```bash
# Development mode
docker compose up -d

# Production mode
ENV_MODE=production DEBUG=0 DEV_MOUNT= docker compose up -d --build

# View logs
docker compose logs -f
docker compose logs -f web
docker compose logs -f celery

# Restart service
docker compose restart web

# Stop all
docker compose down

# Remove everything including volumes (⚠️ DANGEROUS)
docker compose down -v

# View running containers
docker compose ps

# Resource usage
docker stats
```

### Django Commands

```bash
# Run any Django command
docker compose exec web python manage.py <command>

# Migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# User management
docker compose exec web python manage.py createsuperuser

# Shell
docker compose exec web python manage.py shell

# Collect static
docker compose exec web python manage.py collectstatic --noinput
```

### Database Commands

```bash
# Access PostgreSQL
docker compose exec db psql -U django_user -d django_db

# Backup database
docker compose exec db pg_dump -U django_user django_db > backup.sql

# Restore database
cat backup.sql | docker compose exec -T db psql -U django_user -d django_db

# Check database size
docker compose exec db psql -U django_user -d django_db -c "SELECT pg_size_pretty(pg_database_size('django_db'));"
```

### Redis Commands

```bash
# Access Redis CLI
docker compose exec redis redis-cli

# Clear cache
docker compose exec redis redis-cli FLUSHALL

# Monitor Redis
docker compose exec redis redis-cli MONITOR
```

### Celery Commands

```bash
# View active tasks
docker compose exec celery celery -A core inspect active

# Purge all tasks
docker compose exec celery celery -A core purge

# Restart workers
docker compose restart celery celery-beat
```

## 🚨 Troubleshooting

### Check Service Health

```bash
# Check all services
docker compose ps

# Check specific service logs
docker compose logs --tail=100 web

# Check database connection
docker compose exec web python manage.py dbshell

# Test Redis connection
docker compose exec web python -c "from django.core.cache import cache; cache.set('test', 'ok'); print(cache.get('test'))"
```

### Common Issues

**Port already in use:**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Permission denied:**
```bash
sudo chown -R $USER:$USER .
```

**Database won't start:**
```bash
docker compose logs db
docker compose restart db
```

**Static files not loading:**
```bash
docker compose exec web python manage.py collectstatic --noinput --clear
docker compose restart nginx
```

### Reset Everything

```bash
# Stop and remove all containers, volumes, and images
docker compose down -v
docker system prune -af

# Start fresh
docker compose up -d --build
```

## 📚 References

### Official Documentation
- **Django**: https://docs.djangoproject.com/
- **Docker**: https://docs.docker.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Redis**: https://redis.io/documentation
- **Celery**: https://docs.celeryproject.org/
- **Nginx**: https://nginx.org/en/docs/

### Useful Tools
- **Portainer**: Docker management UI - https://www.portainer.io/
- **Lazydocker**: Terminal UI for Docker - https://github.com/jesseduffield/lazydocker
- **Dozzle**: Real-time log viewer - https://dozzle.dev/

---

**🐳 Simple. Dynamic. Production-Ready.**
