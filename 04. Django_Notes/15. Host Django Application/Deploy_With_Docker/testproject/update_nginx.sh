#!/bin/sh

# Your domain name (this will be provided by the CI/CD environment)
DOMAIN=$1
IP_ADDRESS=$2

# Path to your nginx configuration file
NGINX_CONFIG="nginx/nginx.conf"

# Replace "localhost" with your domain name in nginx.conf
sed -i "s/server_name localhost;/server_name $DOMAIN;/g" $NGINX_CONFIG
# Replace "localhost" from .env
sed -i "s/DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1;/DJANGO_ALLOWED_HOSTS=$DOMAIN,$IP_ADDRESS;/g" ".env"
