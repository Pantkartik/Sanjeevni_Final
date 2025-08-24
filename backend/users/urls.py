"""
URL patterns for users app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # JWT Authentication
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('info/', views.user_info, name='user_info'),
    
    # Password Management
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='reset_password_request'),
    path('reset-password/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    
    # Firebase Integration
    path('firebase-token/', views.update_firebase_token, name='update_firebase_token'),
]
