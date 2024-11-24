
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
    'add-every-monday-morning': {
        'task': 'utils.tasks.update_db_monthly_distributions',
        'schedule': crontab(day_of_month='2', hour=1, minute=1),
    },
    # "send-role-notifications-8-hours":{
    #     'task': 'utils.tasks.sendUserRoleNotifications8Hours',
    #     'schedule': crontab(hour="*/12", minute=10),
    # },

    #  "send-role-notifications-10-hours":{
    #     'task': 'utils.tasks.sendUserRoleNotifications10Hours',
    #     'schedule': crontab(hour="*/18", minute=15),
    # },
    # "send-user-subscription-notification":{
    #     'task': 'utils.tasks.sendUserSubscriptionrRequestNotification',
    #     'schedule': crontab(hour="*/16",minute=20),
    # },
    #  "send-uses-1-4-bot-messages":{
    #     'task': 'utils.tasks.sendMessageTo14',
    #     'schedule': crontab(hour=9, minute=40),
    # },

    #  "send-user-5-9-first-bot-messages":{
    #     'task': 'utils.tasks.sendMessageTo59',
    #     'schedule': crontab(hour=10, minute=40),
    # },
    # "send-user-5-9-second-bot-messages":{
    #     'task': 'utils.tasks.sendMessageTo59',
    #     'schedule': crontab(hour=14, minute=10),
    # },
    
    
}