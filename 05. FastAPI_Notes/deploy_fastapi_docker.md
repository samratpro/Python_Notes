# FastAPI Deploy with docker

### 01 : Mapping with IP
```
# Configure Name Server
- Login Domain Provider Website or Cloudflare
- Navigate to Manage DNS
```
Add Following Records:
| Type  | Host/Name   | Value                   |
|-------|-------------|-------------------------|
| A     | @/api       | Your Remote Server IP   |
| A     | www/www.api | Your Remote Server IP   |
| AAAA  | @/api       | Your Remote Server IPv6 |
| AAAA  | www/www.api | Your Remote Server IPv6 |

### 02 : Git repository clone in Server
- open putty enter ip
- login as root
- enter password
- create a dir and clone repo

### 03 : Install Docker
[My Docker Repo](https://github.com/samratpro/Git_Shell_Docker_Linux_CICD/blob/master/04.%20Docker_Commands.md)

### 04.1 : Connect Domain SSL with aapanel
Install aapnel
```bash
URL=https://www.aapanel.com/script/install_7.0_en.sh && if [ -f /usr/bin/curl ];then curl -ksSO "$URL" ;else wget --no-check-certificate -O install_7.0_en.sh "$URL";fi;bash install_7.0_en.sh aapanel
```
- Then Initial Setup

### 04.2 : Add a New Site in aaPanel
```
aaPanel dashboard:
  Go to Website > Add Site
  Domain: api.web.com
  Site path: any folder (not used)
  Web server: Nginx
  Enable SSL (Let’s Encrypt) → issue certificate now
```
### 05 : Modified Nginx Config
- Replace everything from this line:
```
include enable-php-83.conf;
```
Down to (but NOT including) access_log ...; With this:
```
location / {
    proxy_pass http://127.0.0.1:8002;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
- Here used 8002 port
## Dockerfile
```
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
## docker-compose.yml
```
# docker-compose.yml
version: "3.8"

services:
  fastapi:
    build: .
    container_name: fastapi_app
    ports:
      - "8002:8000"
    restart: always
```
### 06: Run 
```
docker-compose up -d --build
```
uses
```
docker-compose up                      # Build from scratch
docker-compose up --build              # build and rebuild with existing
docker-compose up -d --build           # build for server                      

docker-compose down                    # Down will remove container and images
docker-compose down -v                 # -v flag removes named volumes declared 
docker-compose stop                    # simply stop docker without remove anything
docker rm -f container_name            # Remove specific container 
docker system prune -a -f              # Remove All Containers

docker-compose logs -f                 # View Logs
docker-compose exec web sh             # Interactive Shell:

docker-compose logs -f celery_worker     # Verify Celery Worker
docker stats                             # CPU Memory Network Block status
docker stats your_container_name
docker logs your_container_name
docker-compose logs celery_worker_app1   # celery worker1 logs
docker-compose logs celery_worker_app2   # celery worker2 logs
```




