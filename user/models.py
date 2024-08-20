from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=20)
    mobileNumber = models.CharField(max_length=11)
    profileImage = models.ImageField(upload_to="user/images")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    class Meta:
        verbose_name_plural = 'Authentic User'
        
# User Profile

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to="user/images", blank=True,null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"