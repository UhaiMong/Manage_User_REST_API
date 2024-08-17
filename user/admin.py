from django.contrib import admin
from .models import UserModel,Profile
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','mobileNumber','department']
    
    def first_name(self,obj):
        return obj.user.first_name
    def last_name(self,obj):
        return obj.user.last_name
    
admin.site.register(UserModel,UserModelAdmin)
admin.site.register(Profile)
