from django.db import models
from user.models import UserModel
# Create your models here.

class AboutUs(models.Model):
    about = models.OneToOneField(UserModel,on_delete=models.CASCADE)
    bio = models.TextField()
    CONTRIBUTED_CHOICE = [
        ('Frontend','Frontend'),
        ('Backend','Backend'),
        ('UI Design','UI Design'),
        ('Full Stack','Full Stack'),
    ]
    contribution = models.CharField(choices=CONTRIBUTED_CHOICE,max_length=10,default="UI Design")
    
    def __str__(self):
        return f"{self.about.user.first_name},{self.about.user.last_name}"
    class Meta:
         verbose_name_plural = 'About Us'