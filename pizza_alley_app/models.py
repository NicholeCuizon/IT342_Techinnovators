from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Used for Login??
class Accounts(models.Model):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    user_type = models.IntegerField(default=2)
    password = models.CharField(max_length=255)  # Increased max_length for hashed passwords
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.firstname

    class Meta:
        db_table = 'Accounts'