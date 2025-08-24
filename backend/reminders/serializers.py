"""
Serializers for reminders app.
"""

from rest_framework import serializers
from .models import Reminder, ReminderLog, Notification, NotificationTemplate


class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for Reminder model.
    """
    user = serializers.ReadOnlyField(source='user.username')
    is_due_today = serializers.ReadOnlyField()
    next_reminder_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'user', 'medicine_name', 'dosage', 'time', 'date',
            'repeat_pattern', 'custom_days', 'status', 'instructions',
            'before_after_meal', 'notification_enabled', 'reminder_before',
            'created_at', 'updated_at', 'last_taken', 'is_due_today',
            'next_reminder_time'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'last_taken']


class ReminderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new reminders.
    """
    class Meta:
        model = Reminder
        fields = [
            'medicine_name', 'dosage', 'time', 'date', 'repeat_pattern',
            'custom_days', 'instructions', 'before_after_meal',
            'notification_enabled', 'reminder_before'
        ]
    
    def validate_custom_days(self, value):
        """Validate custom days based on repeat pattern."""
        repeat_pattern = self.initial_data.get('repeat_pattern')
        
        if repeat_pattern == 'weekly' and value:
            if not all(0 <= day <= 6 for day in value):
                raise serializers.ValidationError("Weekly days must be 0-6 (Monday=0, Sunday=6)")
        elif repeat_pattern == 'monthly' and value:
            if not all(1 <= day <= 31 for day in value):
                raise serializers.ValidationError("Monthly days must be 1-31")
        
        return value


class ReminderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating reminders.
    """
    class Meta:
        model = Reminder
        fields = [
            'medicine_name', 'dosage', 'time', 'date', 'repeat_pattern',
            'custom_days', 'status', 'instructions', 'before_after_meal',
            'notification_enabled', 'reminder_before'
        ]


class ReminderLogSerializer(serializers.ModelSerializer):
    """
    Serializer for ReminderLog model.
    """
    reminder_medicine = serializers.ReadOnlyField(source='reminder.medicine_name')
    reminder_dosage = serializers.ReadOnlyField(source='reminder.dosage')
    
    class Meta:
        model = ReminderLog
        fields = [
            'id', 'reminder', 'reminder_medicine', 'reminder_dosage',
            'scheduled_time', 'taken_time', 'status', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'reminder_medicine', 'reminder_dosage', 'created_at']


class ReminderLogCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reminder logs.
    """
    class Meta:
        model = ReminderLog
        fields = ['reminder', 'scheduled_time', 'taken_time', 'status', 'notes']
    
    def validate(self, attrs):
        """Validate that taken_time is after scheduled_time if provided."""
        if attrs.get('taken_time') and attrs.get('scheduled_time'):
            if attrs['taken_time'] < attrs['scheduled_time']:
                raise serializers.ValidationError(
                    "Taken time cannot be before scheduled time"
                )
        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'notification_type', 'title', 'message', 'data',
            'firebase_token', 'firebase_message_id', 'status', 'sent_at',
            'delivered_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'firebase_message_id', 'sent_at', 'delivered_at', 'created_at', 'updated_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notifications.
    """
    class Meta:
        model = Notification
        fields = ['notification_type', 'title', 'message', 'data', 'firebase_token']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationTemplate model.
    """
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'notification_type', 'title_template',
            'message_template', 'variables', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReminderSummarySerializer(serializers.Serializer):
    """
    Serializer for reminder summary data.
    """
    total_reminders = serializers.IntegerField()
    active_reminders = serializers.IntegerField()
    due_today = serializers.IntegerField()
    taken_today = serializers.IntegerField()
    missed_today = serializers.IntegerField()
    upcoming_reminders = serializers.ListField(child=ReminderSerializer())


class MarkReminderTakenSerializer(serializers.Serializer):
    """
    Serializer for marking a reminder as taken.
    """
    reminder_id = serializers.IntegerField()
    taken_time = serializers.DateTimeField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_reminder_id(self, value):
        """Validate that the reminder exists and belongs to the user."""
        from .models import Reminder
        try:
            reminder = Reminder.objects.get(id=value)
            if reminder.user != self.context['request'].user:
                raise serializers.ValidationError("You can only mark your own reminders as taken")
        except Reminder.DoesNotExist:
            raise serializers.ValidationError("Reminder not found")
        
        return value
