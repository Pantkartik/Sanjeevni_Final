"""
Views for user authentication and profile management.
"""

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from .models import UserProfile
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, UserProfileUpdateSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view that uses our custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            user = serializer.save()
            profile = user.profile
            
            # Set default role based on request or use default
            role = request.data.get('role', 'patient')
            if role in dict(UserProfile.USER_ROLES):
                profile.role = role
                profile.save()
        
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    View for updating specific user profile fields.
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile


class ChangePasswordView(APIView):
    """
    View for changing user password.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """
    View for requesting password reset.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create reset URL (frontend should handle this)
                reset_url = f"http://localhost:3000/reset-password/{uid}/{token}"
                
                # Send email
                subject = 'Password Reset Request'
                message = f'''
                Hello {user.username},
                
                You requested a password reset. Please click the link below to reset your password:
                
                {reset_url}
                
                If you didn't request this, please ignore this email.
                
                Best regards,
                Health Dashboard Team
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Password reset email sent successfully'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                # Don't reveal if email exists or not
                return Response({
                    'message': 'If the email exists, a password reset link has been sent'
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    View for confirming password reset.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'error': 'Invalid reset link'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    """
    Get current user information.
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.profile.role,
        'date_joined': user.date_joined,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_firebase_token(request):
    """
    Update user's Firebase token for push notifications.
    """
    token = request.data.get('firebase_token')
    if not token:
        return Response({
            'error': 'Firebase token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.profile.firebase_token = token
    user.profile.save()
    
    return Response({
        'message': 'Firebase token updated successfully'
    }, status=status.HTTP_200_OK)
