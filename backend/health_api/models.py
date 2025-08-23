from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Custom User model for health application"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class PillReminder(models.Model):
    """Model for pill reminders"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pill_reminders')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50, choices=[
        ('daily', 'Daily'),
        ('twice_daily', 'Twice Daily'),
        ('weekly', 'Weekly'),
        ('as_needed', 'As Needed'),
    ])
    times = models.JSONField()  # List of times like ["08:00", "20:00"]
    stock = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    caregiver_notify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"


class PillTaken(models.Model):
    """Model to track when pills were taken"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reminder = models.ForeignKey(PillReminder, on_delete=models.CASCADE, related_name='pills_taken')
    taken_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-taken_at']

    def __str__(self):
        return f"{self.reminder.name} taken at {self.taken_at}"


class HealthData(models.Model):
    """Model for storing health metrics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    data_type = models.CharField(max_length=50, choices=[
        ('blood_pressure', 'Blood Pressure'),
        ('heart_rate', 'Heart Rate'),
        ('weight', 'Weight'),
        ('blood_sugar', 'Blood Sugar'),
        ('temperature', 'Temperature'),
        ('oxygen_saturation', 'Oxygen Saturation'),
        ('steps', 'Steps'),
        ('sleep_hours', 'Sleep Hours'),
        ('mood', 'Mood'),
        ('pain_level', 'Pain Level'),
    ])
    value = models.FloatField()
    unit = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.user.email} - {self.data_type}: {self.value}"


class Doctor(models.Model):
    """Model for doctor information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Appointment(models.Model):
    """Model for medical appointments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    appointment_date = models.DateTimeField()
    duration = models.IntegerField(default=30)  # in minutes
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date']

    def __str__(self):
        return f"{self.title} - {self.appointment_date}"


class MentalHealthEntry(models.Model):
    """Model for mental health tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mental_health_entries')
    mood_score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10 scale
    anxiety_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10 scale
    stress_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10 scale
    sleep_quality = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10 scale
    notes = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.user.email} - Mood: {self.mood_score}"


class Notification(models.Model):
    """Model for in-app notifications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('pill_reminder', 'Pill Reminder'),
        ('appointment', 'Appointment'),
        ('health_alert', 'Health Alert'),
        ('general', 'General'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.email}"
