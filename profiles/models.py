from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    #profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"