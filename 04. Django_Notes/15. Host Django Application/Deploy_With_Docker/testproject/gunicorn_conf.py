# gunicorn_conf.py

bind = "0.0.0.0:8000"
workers = 4
worker_connections = 1000
threads = 4

# (2 * core_number) + 1 = Max_Workers
# Per workers take 100mb RAM
# Per worker can handle 4 threads smoothly but depends
# per workers can handle 1000 connections smoothly but depends

# SSL Configuration
certfile = "/etc/letsencrypt/live/your_domain.com/fullchain.pem"
keyfile = "/etc/letsencrypt/live/your_domain.com/privkey.pem"

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"