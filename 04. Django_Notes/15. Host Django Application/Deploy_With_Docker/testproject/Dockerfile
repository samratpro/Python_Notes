FROM python:3.9

# Install necessary packages
RUN apt-get update && apt-get install -y python3-pip python3-dev libpq-dev cron && apt-get clean

# Copy the cron job file into the container
COPY docker_prune.sh /docker_prune.sh

# Make the script executable
RUN chmod +x /docker_prune.sh

# Add cron job to crontab
# Run everyday 2 am
RUN echo "0 2 * * * /docker_prune.sh >> /var/log/docker_prune.log 2>&1" > /etc/cron.d/docker-prune

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/docker-prune

# Apply cron job
RUN crontab /etc/cron.d/docker-prune

# Create application directory
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
