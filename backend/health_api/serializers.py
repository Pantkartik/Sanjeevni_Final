from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, PillReminder, PillTaken, HealthData, Doctor, 
    Appointment, MentalHealthEntry, Notification
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'gender', 'profile_picture',
            'emergency_contact', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'confirm_password',
            'first_name', 'last_name', 'phone_number', 'date_of_birth', 'gender'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')

        return attrs


class PillReminderSerializer(serializers.ModelSerializer):
    """Serializer for PillReminder model"""
    user = UserSerializer(read_only=True)
    adherence_rate = serializers.SerializerMethodField()

    class Meta:
        model = PillReminder
        fields = [
            'id', 'user', 'name', 'dosage', 'frequency', 'times',
            'stock', 'notes', 'caregiver_notify', 'is_active',
            'created_at', 'updated_at', 'adherence_rate'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_adherence_rate(self, obj):
        """Calculate adherence rate for the pill reminder"""
        total_scheduled = obj.pills_taken.count()
        total_taken = obj.pills_taken.filter(taken_at__isnull=False).count()
        if total_scheduled == 0:
            return 0
        return round((total_taken / total_scheduled) * 100, 2)


class PillTakenSerializer(serializers.ModelSerializer):
    """Serializer for PillTaken model"""
    reminder = PillReminderSerializer(read_only=True)

    class Meta:
        model = PillTaken
        fields = ['id', 'reminder', 'taken_at', 'scheduled_time', 'notes']
        read_only_fields = ['id', 'taken_at']


class HealthDataSerializer(serializers.ModelSerializer):
    """Serializer for HealthData model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = HealthData
        fields = [
            'id', 'user', 'data_type', 'value', 'unit', 'notes', 'recorded_at'
        ]
        read_only_fields = ['id', 'user', 'recorded_at']


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'name', 'specialization', 'phone', 'email',
            'address', 'notes', 'is_primary', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    user = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'doctor', 'title', 'description', 'appointment_date',
            'duration', 'status', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class MentalHealthEntrySerializer(serializers.ModelSerializer):
    """Serializer for MentalHealthEntry model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = MentalHealthEntry
        fields = [
            'id', 'user', 'mood_score', 'anxiety_level', 'stress_level',
            'sleep_quality', 'notes', 'recorded_at'
        ]
        read_only_fields = ['id', 'user', 'recorded_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'notification_type',
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_pill_reminders = serializers.IntegerField()
    active_pill_reminders = serializers.IntegerField()
    average_adherence = serializers.FloatField()
    today_adherence = serializers.FloatField()
    upcoming_appointments = serializers.IntegerField()
    recent_health_data = serializers.ListField()
    unread_notifications = serializers.IntegerField()
    mental_health_trend = serializers.ListField()
    today_pills_taken = serializers.IntegerField()
    total_today_pills = serializers.IntegerField()
