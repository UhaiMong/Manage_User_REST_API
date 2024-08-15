from rest_framework import serializers
from .import models

class AboutUsSerializer(serializers.ModelSerializer):
    about = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.AboutUs
        fields = '__all__'