from django.shortcuts import render
from rest_framework import viewsets
from .import serializers
from .import models


# Create your views here.

class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = models.AboutUs.objects.all()
    serializer_class = serializers.AboutUsSerializer