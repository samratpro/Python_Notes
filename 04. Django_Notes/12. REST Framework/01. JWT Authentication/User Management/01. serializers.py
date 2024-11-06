from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AppUser  # Assuming you have a custom user model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AppUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # To activate via email later
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials or account inactive.")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'profile_image']
