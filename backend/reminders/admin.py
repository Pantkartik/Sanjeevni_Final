"""
Admin interface for reminders app.
"""

from django.contrib import admin
from .models import Reminder, ReminderLog, Notification, NotificationTemplate


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Admin interface for Reminder model.
    """
    list_display = [
        'medicine_name', 'user', 'dosage', 'time', 'date', 'repeat_pattern',
        'status', 'notification_enabled', 'created_at'
    ]
    list_filter = [
        'status', 'repeat_pattern', 'notification_enabled', 'before_after_meal',
        'created_at', 'user__profile__role'
    ]
    search_fields = [
        'medicine_name', 'user__username', 'user__first_name', 'user__last_name',
        'instructions'
    ]
    readonly_fields = ['created_at', 'updated_at', 'last_taken']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'medicine_name', 'dosage', 'time', 'date')
        }),
        ('Schedule', {
            'fields': ('repeat_pattern', 'custom_days', 'status')
        }),
        ('Instructions', {
            'fields': ('instructions', 'before_after_meal')
        }),
        ('Notifications', {
            'fields': ('notification_enabled', 'reminder_before')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_taken'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    """
    Admin interface for ReminderLog model.
    """
    list_display = [
        'reminder', 'user', 'scheduled_time', 'taken_time', 'status',
        'created_at'
    ]
    list_filter = [
        'status', 'scheduled_time', 'created_at', 'reminder__user__profile__role'
    ]
    search_fields = [
        'reminder__medicine_name', 'reminder__user__username',
        'reminder__user__first_name', 'reminder__user__last_name', 'notes'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('reminder', 'scheduled_time', 'taken_time', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at')
        }),
    )
    
    def user(self, obj):
        """Display the user for the reminder."""
        return obj.reminder.user.username
    user.short_description = 'User'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('reminder__user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = [
        'title', 'user', 'notification_type', 'status', 'sent_at',
        'delivered_at', 'created_at'
    ]
    list_filter = [
        'notification_type', 'status', 'sent_at', 'delivered_at',
        'created_at', 'user__profile__role'
    ]
    search_fields = [
        'title', 'message', 'user__username', 'user__first_name',
        'user__last_name'
    ]
    readonly_fields = [
        'firebase_message_id', 'sent_at', 'delivered_at', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'title', 'message', 'data')
        }),
        ('Firebase Information', {
            'fields': ('firebase_token', 'firebase_message_id')
        }),
        ('Status Tracking', {
            'fields': ('status', 'sent_at', 'delivered_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationTemplate model.
    """
    list_display = [
        'name', 'notification_type', 'is_active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'notification_type', 'is_active', 'created_at', 'updated_at'
    ]
    search_fields = ['name', 'title_template', 'message_template']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'notification_type', 'is_active')
        }),
        ('Content', {
            'fields': ('title_template', 'message_template', 'variables')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-extract variables from templates."""
        if not change:  # Only for new templates
            import re
            # Extract variables from templates (anything in {{}})
            title_vars = re.findall(r'\{\{(\w+)\}\}', obj.title_template)
            message_vars = re.findall(r'\{\{(\w+)\}\}', obj.message_template)
            # Combine and remove duplicates
            all_vars = list(set(title_vars + message_vars))
            obj.variables = all_vars
        
        super().save_model(request, obj, form, change)
