from amd_main.celery import app
import time
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification


@app.task
def celery_test_task():
    time.sleep(5) #simulation of any task taht's going to take 10 seconds
    mail_subject = 'Test Subject'
    message = 'This is Test email'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message,to_email)
   
    return 'Email send Successfully'
@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
        
    except Exception as e:
        raise e
    # notify the user by email
    mail_subject = 'Import data Completed'
    message = 'Your data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message,to_email)
    return 'Data imported successfully.'

