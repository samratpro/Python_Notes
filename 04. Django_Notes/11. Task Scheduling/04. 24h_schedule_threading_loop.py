# threading is CPU base operation, like Image Processing, Data manipulation etc

import schedule
import os
from datetime import datetime
import threading


# This is a job, checking the a folder to see if there are any text files,
# The task will run after the specified time and after ( import schedule )
# This will work for 24 hours for an unlimited While loop ( while True )
# Threading will multitask here / Share task here ( threading.Thread() )

def job(arg='argument'):
    file_list = os.listdir('.')
    for file_name in file_list:
        if file_name.endswith('.txt'):
            text_file_path = os.path.join('.', file_name)
            with open(text_file_path, 'r') as file:
                file_contents = file.read()
            print(f"Contents of {file_name}:")
            print(file_contents)
            os.remove(file_name)
    else:
        print("No text files found in the folder.")
        print(arg)

def start_task(func, arg):
    thread = threading.Thread(target=func, args=(arg))
    thread.start()


schedule.every(1).seconds.to(5).do(job, 'argument')   # Passing argument

# Doing task with Threading, start_task is function, job is argument and 'argument' is job's argument
schedule.every(1).minutes.to(5).do(start_task, job, 'argument')

schedule.every(2).hours.to(5).do(start_task, job)

schedule.every().minute.at(':20').do(job)
schedule.every().hour.at(':20').do(job)
schedule.every(5).hours.at(':20').do(job)

schedule.every().day.at('12:20:30').do(job) # 24 HOURS TIME
schedule.every().monday.at('01:20').do(job)
schedule.every(10).seconds.until('10:20').do(job)
schedule.every(10).seconds.until(datetime(2024,11,21,10,21,5)).do(job)


# schedule.run_all(delay_seconds=1) # This delay is for between multiple schedule

while True:
    schedule.run_pending()
