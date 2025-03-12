 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

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



from django.conf import settings
# Import settings to get AUTH_USER_MODEL
class UserInterest(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    interests = models.ManyToManyField('Interest')  # Ensure Interest is in quotes if it's defined later

    def __str__(self):
        return f"{self.user.first_name}'s Interests" if self.user.first_name else "User's Interests"



# Profile management apis related model 
from django.contrib.auth.models import AbstractUser
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




