from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, PillReminder, PillTaken, HealthData, Doctor, 
    Appointment, MentalHealthEntry, Notification
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for User model"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_staff', 'created_at', 'gender']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Health Information', {
            'fields': ('phone_number', 'date_of_birth', 'gender', 'profile_picture', 'emergency_contact')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Health Information', {
            'fields': ('phone_number', 'date_of_birth', 'gender', 'profile_picture', 'emergency_contact')
        }),
    )


@admin.register(PillReminder)
class PillReminderAdmin(admin.ModelAdmin):
    """Admin configuration for PillReminder model"""
    list_display = ['name', 'user', 'dosage', 'frequency', 'stock', 'is_active', 'created_at']
    list_filter = ['frequency', 'is_active', 'caregiver_notify', 'created_at']
    search_fields = ['name', 'user__email', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PillTaken)
class PillTakenAdmin(admin.ModelAdmin):
    """Admin configuration for PillTaken model"""
    list_display = ['reminder', 'scheduled_time', 'taken_at']
    list_filter = ['taken_at', 'scheduled_time']
    search_fields = ['reminder__name', 'reminder__user__email']
    ordering = ['-taken_at']
    readonly_fields = ['taken_at']


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    """Admin configuration for HealthData model"""
    list_display = ['user', 'data_type', 'value', 'unit', 'recorded_at']
    list_filter = ['data_type', 'recorded_at']
    search_fields = ['user__email', 'notes']
    ordering = ['-recorded_at']
    readonly_fields = ['recorded_at']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Admin configuration for Doctor model"""
    list_display = ['name', 'user', 'specialization', 'phone', 'is_primary', 'created_at']
    list_filter = ['specialization', 'is_primary', 'created_at']
    search_fields = ['name', 'user__email', 'specialization', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin configuration for Appointment model"""
    list_display = ['title', 'user', 'doctor', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['title', 'user__email', 'doctor__name', 'description']
    ordering = ['-appointment_date']
    readonly_fields = ['created_at']


@admin.register(MentalHealthEntry)
class MentalHealthEntryAdmin(admin.ModelAdmin):
    """Admin configuration for MentalHealthEntry model"""
    list_display = ['user', 'mood_score', 'anxiety_level', 'stress_level', 'sleep_quality', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['user__email', 'notes']
    ordering = ['-recorded_at']
    readonly_fields = ['recorded_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for Notification model"""
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'user__email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
