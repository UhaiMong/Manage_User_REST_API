from rest_framework import serializers
from .import models
from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password

# User Registration Serializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    password = serializers.CharField(
        validators=[MinLengthValidator(6), validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        if password != password2:
            raise serializers.ValidationError({'error': "Passwords don't match!"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username already exists!'})

        # Create user account
        account = User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.is_active=False
        account.save()

        # Create user profile
        profile = Profile.objects.create(user=account)
        print(f'Profile created for user: {profile.user.username}')

        return account

    
# User login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'profileImage']
class AuthenticUserSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    user = UserSerializer()
    class Meta:
        model = models.UserModel
        fields = ['user','department','mobileNumber','profileImage']
