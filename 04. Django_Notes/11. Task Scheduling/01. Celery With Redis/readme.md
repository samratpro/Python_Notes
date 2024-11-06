## 00. Celery Basic Rules
- Celery function under share_task dosen't support argument that can't store in json format exmple, a Model, user can't arument
- try: except
```py
try:
 ..
except:
 pass
```
Dosen't support celery, need to use try, except as ops, final, continute etc
Example:
```py
try: # Handle error entire process

    # Main processing code within the loop
    # for loop here
    ...
    try:
        # Directory creation code
    except Exception as e:
        logger.error(f"Directory creation failed: {e}")
        # Skip to the next iteration if there's an error in directory creation
        continue
    
    try:
        # Posting to Wordpress and related code
    except Exception as e:
        logger.error(f"Error during posting for keyword {keyword}: {e}")
        keyword_model.logs = f"Exception during posting: {str(e)}"
        keyword_model.status = 'Failed'
        keyword_model.save()
    
    finally:
        # Cleanup code (removing directory)
        try:
            shutil.rmtree(new_directory_path)
        except Exception as e:
            logger.error(f"Failed to remove directory {new_directory_path}: {e}")

    # for loop end..
    
except Exception as e:
    # Critical error handling outside the loop
    logger.error(f"Critical error in BulkKeywordsJob: {e}")
    curent_user.logs = f"Critical error: {str(e)}"
    curent_user.save()

```


## 01. Install Celery
```bash
pip install celery
pip install django-celery-results
pip install redis
```
```
# Documentation :  https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django
```
## 02. Install Redis (if not installed)
- Windows, Download : https://www.memurai.com/
- Macos, Download   : https://redis.io/docs/install/install-redis/install-redis-on-mac-os/
## For Ubuntu
```bash
sudo apt update
sudo apt install redis-server
sudo apt-get install redis-server
redis-server # command to check redis server is running
```
## 03. run the Celery worker
- After setup or update -> navigate to your Django project directory, and run the Celery worker
- Must open a new separate terminal and use these command
- All tasks with celery will show in this tab
- worker1, worker2 is related with project/settings.py
```bash
celery -A project_name worker -l info                                 # replace project name (-l info or --loglevel=info )
celery -A project_name worker -l info --concurrency=10 -Q worker1     # Running 10 task in worker1 
celery -A project_name worker -l info --concurrency=10 -Q worker2     # Running 10 task in worker2
```

## 04. Debug
```
celery -A project_name worker -l debug --concurrency=10 -Q worker_name
```
# 05. celery in VPS
## 5.1 Install supervisor
```bash
sudo apt install supervisor
```

## 5.2 Navigate to Supervisor Configuration Directory:
```
cd /etc/supervisor/conf.d/
```
## 5.3 Create a New Configuration File:
```
sudo nano celery.conf
```
## 5.4 Enter Supervisor Configuration:
```
[program:celery-worker1]
command=/www/wwwroot/project_path/venv_path_venv/bin/celery -A project_name worker -l info --concurrency=10 -Q worker1
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

[program:celery-worker2]
command=/www/wwwroot/project_path/venv_path_venv/bin/celery -A project_name worker -l info --concurrency=10 -Q worker2
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
### 5.5 for schedule
```
[program:celery-worker3]
command=/www/wwwroot/PROJECT_PATH/venv_path/bin/celery -A beat -l info
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
## 5.6 Save and Exit:
```
Press Ctrl + O >>> then press Enter to save the file.
Press Ctrl + X to exit nano.
Update Supervisor Configuration:
```
## 5.7 Linux command
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart celery-worker1
sudo supervisorctl restart celery-worker2
```
## 5.8 Check celery is working
```
sudo service supervisor status
sudo supervisorctl status
```
```
Active: active (running) ...(time)
```
## 5.9 Stop Celery
```
sudo supervisorctl
stop celery-worker
```
## 5.10 To start again
```
start celery-worker
```

