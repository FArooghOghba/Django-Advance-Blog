from celery import shared_task
from time import sleep


@shared_task
def task_send_email():
    sleep(3)
    print('done sending email')