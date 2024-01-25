from time import sleep
from celery import shared_task


@shared_task
def notify_customer(msg):
  print('Sending 10k emails...')
  print(msg)
  sleep(10)
  print('Emails sent successfully...')
