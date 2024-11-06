# uvicorn_conf.py

bind = "0.0.0.0:8000"
workers = 4
threads = 4
connections = 1000

# (2 * core_number) + 1 = Max_Workers
# Per workers take 100mb RAM
# Per worker can handle 4 threads smoothly but depends
# per workers can handle 1000 connections smoothly but depends

# SSL Configuration
ssl_keyfile = "/etc/letsencrypt/live/your_domain.com/privkey.pem"
ssl_certfile = "/etc/letsencrypt/live/your_domain.com/fullchain.pem"

# Logging
log_level = "info"
access_log = True
error_log = "-"