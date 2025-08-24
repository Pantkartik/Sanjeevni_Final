"""
Models for pill reminders and notifications.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, date


class Reminder(models.Model):
    """
    Model for pill reminders.
    """
    REPEAT_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
        ('none', 'No Repeat'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 1 tablet, 2 capsules")
    time = models.TimeField(help_text="Time to take the medicine")
    date = models.DateField(default=date.today, help_text="Start date for the reminder")
    repeat_pattern = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='daily')
    custom_days = models.JSONField(default=list, blank=True, help_text="Custom days for weekly/monthly repeat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Additional fields
    instructions = models.TextField(blank=True, help_text="Special instructions")
    before_after_meal = models.CharField(max_length=20, choices=[
        ('before', 'Before Meal'),
        ('after', 'After Meal'),
        ('with', 'With Meal'),
        ('anytime', 'Anytime'),
    ], default='anytime')
    
    # Notification settings
    notification_enabled = models.BooleanField(default=True)
    reminder_before = models.IntegerField(default=15, help_text="Minutes before scheduled time")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_taken = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['time', 'date']
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'
    
    def __str__(self):
        return f"{self.medicine_name} - {self.user.username} at {self.time}"
    
    @property
    def is_due_today(self):
        """Check if reminder is due today."""
        today = date.today()
        
        if self.repeat_pattern == 'daily':
            return True
        elif self.repeat_pattern == 'weekly':
            return today.weekday() in self.custom_days
        elif self.repeat_pattern == 'monthly':
            return today.day in self.custom_days
        elif self.repeat_pattern == 'custom':
            # Custom logic for custom repeat patterns
            return True
        else:  # none
            return today == self.date
    
    @property
    def next_reminder_time(self):
        """Calculate the next reminder time."""
        if not self.is_due_today:
            return None
        
        reminder_time = timezone.make_aware(
            timezone.datetime.combine(date.today(), self.time)
        )
        return reminder_time - timezone.timedelta(minutes=self.reminder_before)


class ReminderLog(models.Model):
    """
    Log of when reminders were taken or missed.
    """
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='logs')
    scheduled_time = models.DateTimeField()
    taken_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('taken', 'Taken'),
        ('missed', 'Missed'),
        ('snoozed', 'Snoozed'),
        ('cancelled', 'Cancelled'),
    ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = 'Reminder Log'
        verbose_name_plural = 'Reminder Logs'
    
    def __str__(self):
        return f"{self.reminder.medicine_name} - {self.status} at {self.scheduled_time}"


class Notification(models.Model):
    """
    Model for storing notification history.
    """
    NOTIFICATION_TYPES = [
        ('reminder', 'Pill Reminder'),
        ('appointment', 'Appointment'),
        ('general', 'General'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True, help_text="Additional data for the notification")
    
    # Firebase specific fields
    firebase_token = models.CharField(max_length=500, blank=True)
    firebase_message_id = models.CharField(max_length=100, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class NotificationTemplate(models.Model):
    """
    Templates for different types of notifications.
    """
    name = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20, choices=Notification.NOTIFICATION_TYPES)
    title_template = models.CharField(max_length=200)
    message_template = models.TextField()
    variables = models.JSONField(default=list, help_text="List of variables used in the template")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    
    def __str__(self):
        return f"{self.name} - {self.notification_type}"
    
    def render_template(self, context):
        """Render the template with given context."""
        title = self.title_template
        message = self.message_template
        
        for key, value in context.items():
            title = title.replace(f"{{{key}}}", str(value))
            message = message.replace(f"{{{key}}}", str(value))
        
        return title, message
