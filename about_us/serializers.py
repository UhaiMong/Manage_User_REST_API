from rest_framework import serializers
from .import models
from user.models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'department', 'mobileNumber', 'profileImage']
class AboutUsSerializer(serializers.ModelSerializer):
    about = UserModelSerializer()

    class Meta:
        model = models.AboutUs
        fields = ['about', 'bio', 'contribution']