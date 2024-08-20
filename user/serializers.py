from rest_framework import serializers
from .import models
from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.UserModel
        fields = '__all__'

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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance

class ProfileUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        profile.profileImage = profile_data.get('profileImage', profile.profileImage)
        profile.save()

        return instance
