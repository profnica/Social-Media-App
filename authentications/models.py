from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField()

    def __str__(self):
        return self.email

# creating user profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth= models.DateField(blank=True, null=True)
    photo=models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.date_of_birth:
            self.date_of_birth = timezone.now().date()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Profile of {self.user.username}'