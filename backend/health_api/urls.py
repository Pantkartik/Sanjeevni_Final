from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView, UserRegistrationView, UserLoginView, UserLogoutView, UserViewSet,
    PillReminderViewSet, HealthDataViewSet,
    DoctorViewSet, AppointmentViewSet, MentalHealthEntryViewSet,
    NotificationViewSet, DashboardView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'pill-reminders', PillReminderViewSet, basename='pill-reminder')
router.register(r'health-data', HealthDataViewSet, basename='health-data')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'mental-health', MentalHealthEntryViewSet, basename='mental-health')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Home page
    path('', HomeView.as_view(), name='home'),
    
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    
    # Dashboard endpoint
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # API router
    path('', include(router.urls)),
]
