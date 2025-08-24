"""
Serializers for user authentication and profile management.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes additional user information.
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['role'] = getattr(self.user.profile, 'role', 'patient')
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'date_of_birth', 'gender', 'phone_number', 'address',
            'emergency_contact', 'emergency_contact_name', 'blood_type',
            'allergies', 'medical_conditions', 'current_medications',
            'profile_picture', 'firebase_token', 'created_at', 'updated_at', 'age'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'role']
    
    def update(self, instance, validated_data):
        # Update User model fields
        user_data = {}
        for field in ['first_name', 'last_name']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        if user_data:
            User.objects.filter(id=instance.user.id).update(**user_data)
        
        # Update UserProfile fields
        return super().update(instance, validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile (limited fields).
    """
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone_number', 'address', 'emergency_contact', 'emergency_contact_name',
            'blood_type', 'allergies', 'medical_conditions', 'current_medications',
            'profile_picture', 'firebase_token'
        ]
    
    def update(self, instance, validated_data):
        # Update User model fields
        user_data = {}
        for field in ['first_name', 'last_name']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        if user_data:
            User.objects.filter(id=instance.user.id).update(**user_data)
        
        # Update UserProfile fields
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("New password fields didn't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting password reset.
    """
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset.
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
