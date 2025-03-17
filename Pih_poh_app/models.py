 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.conf import settings # Import settings to get AUTH_USER_MODEL


class DanceLevel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class Style(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name




class UserInterest(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    interests = models.ManyToManyField('Interest')  # Ensure Interest is in quotes if it's defined later

    def __str__(self):
        return f"{self.user.first_name}'s Interests" if self.user.first_name else "User's Interests"



# Profile management apis related model 

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    dance_level = models.ForeignKey('DanceLevel', on_delete=models.SET_NULL, null=True, blank=True)
    interests = models.ManyToManyField('Interest', blank=True)
    styles = models.ManyToManyField('Style', blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups", 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  
        blank=True
    )

# payment and subcription related model 


# 1. Subscription Plans
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    # For free and standard, this is a positive number; for premium, use null to indicate "unlimited"
    video_analysis_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Null means unlimited")
    reference_comparison_available = models.BooleanField(default=False)
    process_tracking_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_name

# 2. User Subscriptions


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.end_date and self.end_date < now():
            self.is_active = False  # Automatically deactivate expired subscriptions
        super().save(*args, **kwargs)
	


# 3. Monthly Usage Tracking
class UsageTracking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Store the first day of the month to represent that month (e.g., 2025-03-01)
    month = models.DateField(help_text="Represented by the first day of the month")
    videos_analyzed = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'month')
        ordering = ['month']

    def __str__(self):
        return f"{self.user.email} usage for {self.month.strftime('%Y-%m')}"
		


# 4. Payment Details
class Payment(models.Model):
    PAYMENT_PLAN_CHOICES = [
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # For subscription payments
    subscription_id = models.CharField(max_length=255, blank=True, null=True)  # e.g., Stripe Subscription ID
    product_id = models.CharField(max_length=255, blank=True, null=True)       # e.g., Stripe Product ID
    plan_type = models.CharField(max_length=50, choices=PAYMENT_PLAN_CHOICES, blank=True, null=True)
    subscription_start_date = models.DateTimeField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # For one-time payment transactions (if applicable)
    payment_intent_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=10, default='usd')
    payment_method = models.CharField(max_length=255, blank=True, null=True)  # e.g., 'card'
    refund_status = models.CharField(max_length=50, default='not_refunded')

    # Common payment status
    status = models.CharField(max_length=50)  # e.g., 'succeeded', 'failed', 'pending'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        plan_display = self.plan_type if self.plan_type else "One-Time"
        return f"{self.user.email} - {plan_display}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['payment_intent_id']),
        ]


