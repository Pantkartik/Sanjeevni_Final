"""
URL patterns for reminders app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reminders'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'reminders', views.ReminderViewSet, basename='reminder')
router.register(r'logs', views.ReminderLogViewSet, basename='reminderlog')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'templates', views.NotificationTemplateViewSet, basename='notificationtemplate')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional custom endpoints
    path('send-notification/', views.SendNotificationView.as_view(), name='send_notification'),
]
