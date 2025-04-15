from django.db import models
from users.models import User

APP_SCREENS = [
        ("Home", 'Home'),
        ("Ticket", 'Ticket'),
        ("Plans", 'Plans'),
        ("welcome","welcome"),
        ("register","register"),
        ("dashboard","dashboard"),
        ("login","login"),
        ("forgotPassword","forgotPassword"),
        ("EditProfile","EditProfile"),
        ("ChangePassword","ChangePassword"),
        ("PCNCreated","PCNCreated"),
        ("Referrals","Referrals"),
        ("PlanDetailsBreakdownSection","PlanDetailsBreakdownSection"),
        ("PaymentSuccessful","PaymentSuccessful"),
        ("PreDashboard","PreDashboard"),
        ("Notifications","Notifications"),
        ("Profile","Profile"),
        ("PayAPCN","PayAPCN"),
        ("Subscriptions","Subscriptions"),
        ("AddVehicle","AddVehicle"),
        ("ListVehicles","ListVehicles"),
        
    ]

USERS_SUBSCRIPTION_CATEGORY = [
        ("Basic", 'Basic'),
        ("Premium", 'Premium'),
        ("None", 'None')
    ]



class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    screen = models.TextField(
        choices=APP_SCREENS,
        null=True,
        blank=True
    )
    expire_date = models.DateField(null=True, blank=True)
    users_subscription_category = models.TextField(null=True, blank=True, choices=USERS_SUBSCRIPTION_CATEGORY,)
    to_all_registered_users = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ["-id"]
