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
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ProfileSerializer
from django.http import JsonResponse
import logging

# Email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.AuthenticUserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # queryset = models.Profile.objects.all()
    # serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        # Return the profile for the logged-in user only
        return models.Profile.objects.filter(user=self.request.user)

    def get_object(self):
        # Get the logged-in user's profile
        return self.get_queryset().first()

# Profile update api view
class ProfileUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        try:
            profile = models.Profile.objects.get(user=request.user)
        except models.Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            confirm_link = f"http://127.0.0.1:8000/user/active/{uid}/{token}"
            email_subject = "Account activation"
            email_body = render_to_string('account_active.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# activate function

def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Account activated successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Activation link is invalid.'}) 
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
                return Response({'token':token.key,'user_id':user.id,"message":"success"})
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

