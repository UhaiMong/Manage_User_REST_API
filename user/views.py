from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .import serializers
from .import models
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import logging
from .serializers import ProfileUpdateSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

# Profile update api view
class ProfileUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

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
logger = logging.getLogger(__name__)

class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"User {request.user.id} is authenticated and attempting to log out.")
            request.user.auth_token.delete()
            logout(request)
            return Response({"success": "Logged out successfully"}, status=200)
        else:
            logger.warning("Logout attempt failed: User is not authenticated.")
            logger.debug(f"Headers received: {request.headers}")
            logger.debug(f"Token in request: {request.META.get('HTTP_AUTHORIZATION')}")
            return Response({"error": "User is not logged in"}, status=400)

