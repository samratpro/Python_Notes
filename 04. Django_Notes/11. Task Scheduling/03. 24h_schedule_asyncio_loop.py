# asyncio is IO operation, API requests, Data base query etc

import os
import schedule
from datetime import datetime
import asyncio


# This is a job, checking the a folder to see if there are any text files,
# The task will run after the specified time and after ( import schedule )
# This will work for 24 hours for an unlimited While loop ( while True )
# Asyncio will multitask here / Share task here ( schedule_job() )


async def job(arg='argument'):
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


def schedule_job():
    loop = asyncio.get_event_loop()       # It ensures that these tasks are executed efficiently and concurrently
    task = asyncio.create_task(job())     # event loop to actually run that task
    loop.run_until_complete(task)         # This line effectively tells the event loop to execute the task and await its completion


schedule.every(1).seconds.to(5).do(schedule_job)
schedule.every(1).minutes.to(5).do(schedule_job)
schedule.every(2).hours.to(5).do(schedule_job)
schedule.every().minute.at(':20').do(schedule_job)
schedule.every().hour.at(':20').do(schedule_job)
schedule.every(5).hours.at(':20').do(schedule_job)
schedule.every().day.at('12:20:30').do(schedule_job)
schedule.every().monday.at('01:20').do(schedule_job)
schedule.every(10).seconds.until('10:20').do(schedule_job)
schedule.every(10).seconds.until(datetime(2024, 11, 21, 10, 21, 5)).do(schedule_job)


while True:
    schedule.run_pending()
