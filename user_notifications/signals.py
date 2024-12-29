
from django.db.models.signals import post_save
from users.models import DeviceToken, User
from .models import Notification
from django.dispatch import receiver
from firebase_admin import messaging



class NotificationHandler:
    def __init__(self,instance:Notification):
        self.instance = instance
        self.title = instance.title
        self.message = instance.message
        self.screen = instance.screen
        self.expired_data = instance.expire_date
        self.data = {}
        
        if self.screen and len(self.screen) > 1:
            self.data = {"screen":self.screen}
        
        if self.expired_data:
            self.data = {"expired_data":self.expired_data}
        
        if instance.user:
            self._send_notification(instance.user)
            
        elif instance.to_all_registered_users:
            users = User.objects.all()
            for user in users:
                self._send_notification(user)
                
        elif instance.users_subscription_category:
            self._configure_subscription()

    
    
    
    def _configure_subscription(self,):
        if self.instance.users_subscription_category == "Basic":
            users = User.objects.filter(subscription__name="BASIC")
        elif self.instance.users_subscription_category == "Premium":
            users = User.objects.filter(subscription__name="PREMIUM")
        elif self.instance.users_subscription_category == "None":
            users = User.objects.filter(subscription__isnull = True)
            
        for user in users:
            self._send_notification(user)
            
    def _send_notification(self, user):
        try:
            user_token = DeviceToken.objects.get(user = user)
            n_message = messaging.Message(
            notification=messaging.Notification(
                title=self.title,
                body=self.message,
            ),
            data=self.data,
            token=user_token.token.strip(),
        )
            messaging.send(n_message)
            print("sent")
        except Exception as e:
            print(e)
        



@receiver(post_save, sender=Notification) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        notification = NotificationHandler(instance=instance)
        # title = instance.title
        # message = instance.message
        # expired_data = instance.expire_date
        # screen = instance.screen
        
        # data = {}
        
        # if screen and len(screen) > 1:
        #     data = {"screen":screen}
        
        # if expired_data:
        #     data = {"expired_data":expired_data}
        
        
        
        # try:
        #     user_token = DeviceToken.objects.get(user = instance.user)
        #     n_message = messaging.Message(
        #     notification=messaging.Notification(
        #         title=title,
        #         body=message,
        #     ),
        #     data=data,
        #     token=user_token.token.strip(),
        # )
        #     messaging.send(n_message)
        #     print("sent")
        # except Exception as e:
        #     print(e)

