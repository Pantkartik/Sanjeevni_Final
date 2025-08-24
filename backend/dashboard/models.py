"""
Models for dashboard app - data aggregation and user preferences.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DashboardWidget(models.Model):
    """
    Model for user's dashboard widget preferences.
    """
    WIDGET_TYPES = [
        ('reminders', 'Pill Reminders'),
        ('mental_health', 'Mental Health'),
        ('appointments', 'Appointments'),
        ('community', 'Community Activity'),
        ('ai_analysis', 'AI Analysis'),
        ('health_stats', 'Health Statistics'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    position = models.PositiveIntegerField(default=0, help_text="Widget position on dashboard")
    is_enabled = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True, help_text="Widget-specific settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position']
        unique_together = ['user', 'widget_type']
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_widget_type_display()}"


class UserHealthMetrics(models.Model):
    """
    Model for storing user's health metrics and statistics.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    date = models.DateField(default=timezone.now)
    
    # General health metrics
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    # Mental health metrics
    mood_score = models.PositiveIntegerField(null=True, blank=True, help_text="1-10 scale")
    stress_level = models.PositiveIntegerField(null=True, blank=True, help_text="1-10 scale")
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    exercise_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    # Medication adherence
    medications_taken = models.PositiveIntegerField(default=0)
    medications_total = models.PositiveIntegerField(default=0)
    
    # Notes and observations
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name = 'User Health Metrics'
        verbose_name_plural = 'User Health Metrics'
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    @property
    def medication_adherence_rate(self):
        """Calculate medication adherence rate as percentage."""
        if self.medications_total > 0:
            return (self.medications_taken / self.medications_total) * 100
        return 0
    
    @property
    def blood_pressure_status(self):
        """Get blood pressure status based on readings."""
        if not self.blood_pressure_systolic or not self.blood_pressure_diastolic:
            return 'unknown'
        
        if self.blood_pressure_systolic < 120 and self.blood_pressure_diastolic < 80:
            return 'normal'
        elif self.blood_pressure_systolic < 130 and self.blood_pressure_diastolic < 80:
            return 'elevated'
        elif self.blood_pressure_systolic >= 130 or self.blood_pressure_diastolic >= 80:
            return 'high'
        else:
            return 'unknown'


class DashboardAnalytics(models.Model):
    """
    Model for storing dashboard analytics and insights.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_analytics')
    date = models.DateField(default=timezone.now)
    
    # Activity metrics
    login_count = models.PositiveIntegerField(default=0)
    reminder_interactions = models.PositiveIntegerField(default=0)
    mental_health_entries = models.PositiveIntegerField(default=0)
    community_posts = models.PositiveIntegerField(default=0)
    
    # Health insights
    health_trend = models.CharField(max_length=20, choices=[
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
        ('unknown', 'Unknown'),
    ], default='unknown')
    
    # AI-generated insights
    ai_insights = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    
    # Risk assessments
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('unknown', 'Unknown'),
    ], default='unknown')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name = 'Dashboard Analytics'
        verbose_name_plural = 'Dashboard Analytics'
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.health_trend}"


class UserGoal(models.Model):
    """
    Model for user's health and wellness goals.
    """
    GOAL_CATEGORIES = [
        ('medication', 'Medication Adherence'),
        ('mental_health', 'Mental Health'),
        ('physical_health', 'Physical Health'),
        ('lifestyle', 'Lifestyle'),
        ('community', 'Community Engagement'),
    ]
    
    GOAL_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=GOAL_CATEGORIES)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True, help_text="e.g., days, percentage, minutes")
    
    start_date = models.DateField(default=timezone.now)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='active')
    
    # Progress tracking
    milestones = models.JSONField(default=list, blank=True)
    progress_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Goal'
        verbose_name_plural = 'User Goals'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage."""
        if self.target_value and self.target_value > 0:
            progress = (self.current_value / self.target_value) * 100
            return min(progress, 100)  # Cap at 100%
        return 0
    
    @property
    def is_overdue(self):
        """Check if goal is overdue."""
        if self.target_date and self.status == 'active':
            return timezone.now().date() > self.target_date
        return False
