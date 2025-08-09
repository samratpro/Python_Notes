# Django VPS Deployment Guide

Complete guide for deploying Django applications on VPS using Gunicorn and Nginx without control panels.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Server Setup](#1-initial-server-setup)
- [Django Project Setup](#2-setup-django-project)
- [Production Settings](#3-configure-django-settings)
- [Gunicorn Configuration](#4-test-gunicorn)
- [Systemd Services](#5-create-gunicorn-service)
- [Nginx Setup](#6-configure-nginx)
- [Permissions & Security](#7-set-permissions)
- [SSL Certificate](#9-ssl-certificate-optional-but-recommended)
- [Maintenance Commands](#10-useful-commands)
- [Environment Variables](#11-environment-variables-recommended)
- [Database Setup](#12-database-setup-postgresql-example)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- 🖥️ Fresh Ubuntu/Debian VPS (20.04+ recommended)
- 🔑 Root or sudo access
- 🌐 Domain name (optional but recommended)
- 🐍 Basic knowledge of Python/Django
- 📝 Your Django project ready for deployment

## 🚀 Quick Start

If you're in a hurry, here's the essential commands:

```bash
# 1. Update system and install packages
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx git supervisor -y

# 2. Create user and setup project
sudo adduser django_user
su - django_user
mkdir ~/myproject && cd ~/myproject
python3 -m venv venv && source venv/bin/activate

# 3. Deploy your Django app
git clone YOUR_REPO_URL .
pip install -r requirements.txt
python manage.py migrate && python manage.py collectstatic

# 4. Setup services (see detailed steps below)
```

## 1. 🔧 Initial Server Setup

### Update system
```bash
sudo apt update && sudo apt upgrade -y
```

### Install required packages
```bash
sudo apt install python3 python3-pip python3-venv nginx git curl supervisor -y
```

### Create a dedicated user
```bash
sudo adduser django_user
sudo usermod -aG sudo django_user
```

## 2. 📦 Setup Django Project

### Switch to django user
```bash
su - django_user
```

### Create project directory
```bash
mkdir -p /home/django_user/myproject
cd /home/django_user/myproject
```

### Clone or upload your Django project
```bash
# If using Git
git clone https://github.com/yourusername/yourproject.git .

# Or create a new project
django-admin startproject myproject .
```

### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install django gunicorn
# Install your project requirements
pip install -r requirements.txt
```

## 3. ⚙️ Configure Django Settings

### Update settings.py for production
```python
# settings.py
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip', 'localhost']

# Database (example with PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Run migrations and collect static files
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 4. 🧪 Test Gunicorn

### Test Gunicorn manually
```bash
cd /home/django_user/myproject
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
```

Test in browser: `http://your-server-ip:8000`

## 5. 🔄 Create Gunicorn Service

### Create Gunicorn service file
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

### Add service configuration
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=django_user
Group=www-data
WorkingDirectory=/home/django_user/myproject
ExecStart=/home/django_user/myproject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Create Gunicorn socket
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Enable and start services
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

### Check status
```bash
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn
```

## 6. 🌐 Configure Nginx

### Create Nginx site configuration
```bash
sudo nano /etc/nginx/sites-available/myproject
```

### Add Nginx configuration
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com your-server-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/django_user/myproject;
    }
    
    location /media/ {
        root /home/django_user/myproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Enable the site
```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/
```

### Test Nginx configuration
```bash
sudo nginx -t
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Remove default Nginx site (optional)
```bash
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl reload nginx
```

## 7. 🔒 Set Permissions

### Fix file permissions
```bash
sudo usermod -a -G django_user www-data
sudo chmod 710 /home/django_user
sudo chmod 755 /home/django_user/myproject
sudo chmod -R 755 /home/django_user/myproject/staticfiles
sudo chmod -R 755 /home/django_user/myproject/media
```

## 8. 🔥 Firewall Configuration

### Configure UFW firewall
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## 9. 🔐 SSL Certificate (Optional but Recommended)

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain SSL certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Auto-renewal
```bash
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 10. 🛠️ Useful Commands

### Restart services
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### View logs
```bash
sudo journalctl -u gunicorn
sudo journalctl -u nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Test Gunicorn socket
```bash
sudo systemctl status gunicorn.socket
curl --unix-socket /run/gunicorn.sock localhost
```

### Update your Django app
```bash
cd /home/django_user/myproject
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## 11. 🔐 Environment Variables (Recommended)

### Create .env file
```bash
nano /home/django_user/myproject/.env
```

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Install python-decouple
```bash
pip install python-decouple
```

### Update settings.py
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

## 12. 🗃️ Database Setup (PostgreSQL Example)

### Install PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create database and user
```bash
sudo -u postgres psql
CREATE DATABASE myproject_db;
CREATE USER myproject_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE myproject_db TO myproject_user;
\q
```

### Install psycopg2
```bash
sudo apt install python3-dev libpq-dev -y
pip install psycopg2-binary
```

## 🚨 Troubleshooting

### Common issues and solutions

1. **Permission denied errors**
   ```bash
   sudo chown -R django_user:www-data /home/django_user/myproject
   sudo chmod -R 755 /home/django_user/myproject
   ```

2. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   sudo systemctl restart gunicorn nginx
   ```

3. **Gunicorn not starting**
   ```bash
   sudo journalctl -u gunicorn
   # Check the logs for specific errors
   ```

4. **502 Bad Gateway**
   ```bash
   sudo systemctl status gunicorn
   sudo journalctl -u gunicorn
   curl --unix-socket /run/gunicorn.sock localhost
   ```

Your Django app should now be running at `http://your-domain.com` or `http://your-server-ip`!

---

## 📚 Additional Resources

- [Django Deployment Documentation](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/en/stable/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

## 🤝 Contributing

Feel free to submit issues and pull requests to improve this guide.

## 📄 License

This guide is available under the MIT License.

---

**Made with ❤️ for the Django community**