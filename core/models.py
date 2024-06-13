from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='', null=True, blank=True, default='default_profile_picture.jpg')

    def __str__(self):
        return self.user.username

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Changed to handle custom services

    def __str__(self):
        return self.name

class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer_description = models.TextField()
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('pending', 'Pending'),('rejected', 'Rejected'),('completed', 'Completed')], default='pending')
    details = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
