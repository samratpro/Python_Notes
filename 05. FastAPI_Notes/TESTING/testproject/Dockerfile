FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# Copy application code
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt
COPY . /opt/app/

# Set execute permission for entrypoint script
RUN chmod +x /opt/app/entrypoint.sh

# Define entrypoint
# Start cron daemon and the entrypoint script
CMD ["sh", "-c", "cron && /opt/app/entrypoint.sh"]