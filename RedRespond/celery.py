from celery import Celery
import os
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedRespond.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('RedRespond')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'update-donations-every-hour': {
        'task': 'main.tasks.update_donations',  # Specify your task here
        'schedule': crontab(minute='*/2'),  # Every 2 minutes
    },
}

app.conf.timezone = 'UTC'  # Or your desired timezone