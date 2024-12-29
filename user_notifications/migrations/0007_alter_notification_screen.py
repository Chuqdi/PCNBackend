# Generated by Django 5.1.3 on 2024-12-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_notifications", "0006_alter_notification_users_subscription_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="screen",
            field=models.TextField(
                blank=True,
                choices=[
                    ("Home", "Home"),
                    ("Ticket", "Ticket"),
                    ("Plans", "Plans"),
                    ("welcome", "welcome"),
                    ("register", "register"),
                    ("dashboard", "dashboard"),
                    ("login", "login"),
                    ("forgotPassword", "forgotPassword"),
                    ("EditProfile", "EditProfile"),
                    ("ChangePassword", "ChangePassword"),
                    ("PCNCreated", "PCNCreated"),
                    ("Referrals", "Referrals"),
                    ("PlanDetailsBreakdownSection", "PlanDetailsBreakdownSection"),
                    ("PaymentSuccessful", "PaymentSuccessful"),
                    ("PreDashboard", "PreDashboard"),
                    ("Notifications", "Notifications"),
                    ("Profile", "Profile"),
                    ("PayAPCN", "PayAPCN"),
                    ("Subscriptions", "Subscriptions"),
                    ("AddVehicle", "AddVehicle"),
                    ("ListVehicles", "ListVehicles"),
                ],
                null=True,
            ),
        ),
    ]