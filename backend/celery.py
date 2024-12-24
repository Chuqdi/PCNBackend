
import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend', include=['utils.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'send_user_fridays_subscription_message': {
        'task': 'utils.tasks.send_user_fridays_subscription_message',
        'schedule': crontab(day_of_week=4, hour=9, minute=30),
    },
    
    
    'send_user_first_subscription_message': {
        'task': 'utils.tasks.send_user_first_subscription_message',
        'schedule': crontab(day_of_week="*", hour=9, minute=30, day_of_month="*", month_of_year="*"),
    },
    'send_user_second_subscription_message': {
        'task': 'utils.tasks.send_user_second_subscription_message',
        'schedule': crontab(day_of_week="*", hour=17, minute=33, day_of_month="*", month_of_year="*"),
    },

}