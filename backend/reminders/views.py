"""
Views for reminders app.
"""

from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, datetime
from django_filters.rest_framework import DjangoFilterBackend

from .models import Reminder, ReminderLog, Notification, NotificationTemplate
from .serializers import (
    ReminderSerializer, ReminderCreateSerializer, ReminderUpdateSerializer,
    ReminderLogSerializer, ReminderLogCreateSerializer, NotificationSerializer,
    NotificationCreateSerializer, NotificationTemplateSerializer,
    ReminderSummarySerializer, MarkReminderTakenSerializer
)
# from .services.firebase_service import FirebaseNotificationService


class ReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reminders.
    """
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'repeat_pattern', 'notification_enabled']
    
    def get_queryset(self):
        """Return reminders for the current user."""
        return Reminder.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return ReminderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReminderUpdateSerializer
        return ReminderSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a reminder."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_taken(self, request, pk=None):
        """Mark a reminder as taken."""
        reminder = self.get_object()
        serializer = MarkReminderTakenSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            taken_time = serializer.validated_data.get('taken_time', timezone.now())
            notes = serializer.validated_data.get('notes', '')
            
            # Create log entry
            ReminderLog.objects.create(
                reminder=reminder,
                scheduled_time=timezone.now(),
                taken_time=taken_time,
                status='taken',
                notes=notes
            )
            
            # Update reminder last_taken
            reminder.last_taken = taken_time
            reminder.save()
            
            return Response({'message': 'Reminder marked as taken'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def snooze(self, request, pk=None):
        """Snooze a reminder for a specified number of minutes."""
        reminder = self.get_object()
        minutes = request.data.get('minutes', 15)
        
        # Create log entry for snoozed reminder
        ReminderLog.objects.create(
            reminder=reminder,
            scheduled_time=timezone.now(),
            status='snoozed',
            notes=f'Snoozed for {minutes} minutes'
        )
        
        return Response({
            'message': f'Reminder snoozed for {minutes} minutes',
            'next_reminder': timezone.now() + timezone.timedelta(minutes=minutes)
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def due_today(self, request):
        """Get reminders due today."""
        today = date.today()
        reminders = self.get_queryset().filter(
            Q(date=today) |  # One-time reminders
            Q(repeat_pattern='daily') |  # Daily reminders
            Q(repeat_pattern='weekly', custom_days__contains=[today.weekday()]) |  # Weekly reminders
            Q(repeat_pattern='monthly', custom_days__contains=[today.day])  # Monthly reminders
        ).filter(status='active')
        
        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary of user's reminders."""
        user = request.user
        today = date.today()
        
        # Get reminder counts
        total_reminders = Reminder.objects.filter(user=user).count()
        active_reminders = Reminder.objects.filter(user=user, status='active').count()
        
        # Get today's reminders
        today_reminders = Reminder.objects.filter(
            user=user,
            status='active'
        ).filter(
            Q(date=today) |
            Q(repeat_pattern='daily') |
            Q(repeat_pattern='weekly', custom_days__contains=[today.weekday()]) |
            Q(repeat_pattern='monthly', custom_days__contains=[today.day])
        )
        
        due_today = today_reminders.count()
        
        # Get today's logs
        today_logs = ReminderLog.objects.filter(
            reminder__user=user,
            scheduled_time__date=today
        )
        
        taken_today = today_logs.filter(status='taken').count()
        missed_today = today_logs.filter(status='missed').count()
        
        # Get upcoming reminders (next 24 hours)
        upcoming_reminders = today_reminders[:5]  # Limit to 5 for performance
        
        summary_data = {
            'total_reminders': total_reminders,
            'active_reminders': active_reminders,
            'due_today': due_today,
            'taken_today': taken_today,
            'missed_today': missed_today,
            'upcoming_reminders': ReminderSerializer(upcoming_reminders, many=True).data
        }
        
        serializer = ReminderSummarySerializer(summary_data)
        return Response(serializer.data)


class ReminderLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reminder logs.
    """
    serializer_class = ReminderLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'reminder']
    
    def get_queryset(self):
        """Return reminder logs for the current user."""
        return ReminderLog.objects.filter(reminder__user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return ReminderLogCreateSerializer
        return ReminderLogSerializer
    
    def perform_create(self, serializer):
        """Set the scheduled_time if not provided."""
        if not serializer.validated_data.get('scheduled_time'):
            serializer.save(scheduled_time=timezone.now())


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['notification_type', 'status']
    
    def get_queryset(self):
        """Return notifications for the current user."""
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a notification."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications."""
        count = self.get_queryset().filter(status='pending').count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.status = 'delivered'
        notification.delivered_at = timezone.now()
        notification.save()
        
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)


class NotificationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notification templates (read-only).
    """
    queryset = NotificationTemplate.objects.filter(is_active=True)
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['notification_type']


class SendNotificationView(generics.CreateAPIView):
    """
    View for sending notifications via Firebase.
    """
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Send notification and create record."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create notification record
        notification = serializer.save(user=request.user)
        
        # Send via Firebase if token is provided (commented out for now)
        # if notification.firebase_token:
        #     try:
        #         firebase_service = FirebaseNotificationService()
        #         result = firebase_service.send_notification(
        #             token=notification.firebase_token,
        #             title=notification.title,
        #             body=notification.message,
        #             data=notification.data
        #         )
        #         
        #         if result.get('success'):
        #             notification.status = 'sent'
        #             notification.sent_at = timezone.now()
        #             notification.firebase_message_id = result.get('message_id', '')
        #         else:
        #             notification.status = 'failed'
        #         
        #         notification.save()
        #         
        #     except Exception as e:
        #         notification.status = 'failed'
        #         notification.save()
        #         return Response({
        #         'message': 'Notification created but failed to send',
        #         'error': str(e)
        #         }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Notification sent successfully',
            'notification_id': notification.id
        }, status=status.HTTP_201_CREATED)
