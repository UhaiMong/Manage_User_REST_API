from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .import serializers
from .import models
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    
# User Registration API View
class UserRegistrationApiView(APIView):
    serializer_class = serializers.UserRegistrationSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            return Response("Your Registration is successful")
        Response(serializer.errors)

# User Login API View
class UserLoginApiView(APIView):
    def post(self,request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username,password=password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':'Invalid Credential'})
        return Response(serializer.errors)
    
# User logout API View
class UserLogoutApiView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
