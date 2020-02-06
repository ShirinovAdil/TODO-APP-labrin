from celery import Celery
from celery import shared_task
from . models import Task
from datetime import datetime
from django.core.mail import send_mail
import pytz

app = Celery('tasks', broker='pyamqp://guest@localhost//')
#app.config_from_object(__name__)


@app.task
def test_task():
    print("SUCCESS")


@shared_task
def progress_bar():
    print("Executed every minute")


@app.task
def parse_todo():
    """Will parse all todo tasks and find the ones that are out of date"""
    all_tasks = Task.objects.all()
    today = datetime.now()

    for each in all_tasks:
        sub = each.end_date - datetime.now().replace(tzinfo=pytz.utc)
        if int((sub.total_seconds() + 14400)/60) <= 30:
            print("Task ends soon")
            send_mail(
                subject='TODO APP',
                message='One of your tasks end soon',
                from_email='adil.shirinov.99@gmail.com',
                recipient_list=['cowif39823@mailapp.top', ],
                fail_silently=False,
            )
            print("sent")
    print("END OF PARSING")




