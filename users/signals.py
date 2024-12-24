
import json
import random
from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from datetime import timedelta


def create_perodic_task(task:str,crontab:CrontabSchedule,arg):
    task_name = f"{task}_{arg}"
    try:
        PeriodicTask.objects.get(name=task_name).delete()
    except PeriodicTask.DoesNotExist:
        pass
    task = PeriodicTask.objects.create(
        crontab=crontab,
        task= f'utils.tasks.{task}',
        name=task_name,
        args=json.dumps(arg)
    )
    
    print(task)
    

@receiver(post_save, sender=User) 
def user_created(sender, instance, created, **kwargs):
    if created:
        date_joined = instance.date_joined + timedelta(days=1)
        times_to_send_first_message = [7,8,9]
        time_to_send_first_message = random.choice(times_to_send_first_message)
        
        ### FIRST MESSAGE 
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=7,
            hour=time_to_send_first_message,
            day_of_month=date_joined.day,
            month_of_year=date_joined.month,
            day_of_week = date_joined.isocalendar()[1]
        )
        
        
        
        create_perodic_task(task="send_user_first_subscription_message", crontab=crontab, arg=instance.pk)
        print("Week")
        print(date_joined.isocalendar()[1])
        print("Day of the month")
        print(date_joined.day)
        print("Month")
        print(date_joined.month)
        
        
        ## SECOND MESSAGE
        # crontab,created = CrontabSchedule.objects.get_or_create(
        #     minute=7,
        #     hour=time_to_send_first_message + 8,
        #     day_of_month=date_joined.day,
        #     month_of_year=date_joined.month,
        #     day_of_week = date_joined.isocalendar()[1]
        # )
        
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=46,
            hour=9,
            day_of_month=24,
            month_of_year=12,
            day_of_week = 52
        )
        
        create_perodic_task(task="send_user_second_subscription_message", crontab=crontab, arg=instance.pk)
        
        ### 24HR Message
        crontab,created = CrontabSchedule.objects.get_or_create(
            minute=7,
            hour=time_to_send_first_message + 24,
            day_of_month=date_joined.day,
            month_of_year=date_joined.month,
            day_of_week = date_joined.isocalendar()[1]
        )
        
        create_perodic_task(task="send_user_24_hr_subscription_message", crontab=crontab, arg=instance.pk)
        
        print("scheduled all tasks")
        
        



        