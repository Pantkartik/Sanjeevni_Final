"""
Serializers for dashboard app.
"""

from rest_framework import serializers
from .models import DashboardWidget, UserHealthMetrics, DashboardAnalytics, UserGoal


class DashboardWidgetSerializer(serializers.ModelSerializer):
    """
    Serializer for DashboardWidget model.
    """
    widget_type_display = serializers.CharField(source='get_widget_type_display', read_only=True)
    
    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'widget_type', 'widget_type_display', 'position', 'is_enabled',
            'settings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardWidgetUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating dashboard widget settings.
    """
    class Meta:
        model = DashboardWidget
        fields = ['position', 'is_enabled', 'settings']


class UserHealthMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for UserHealthMetrics model.
    """
    medication_adherence_rate = serializers.ReadOnlyField()
    blood_pressure_status = serializers.ReadOnlyField()
    
    class Meta:
        model = UserHealthMetrics
        fields = [
            'id', 'date', 'weight', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature', 'mood_score', 'stress_level', 'sleep_hours',
            'exercise_minutes', 'medications_taken', 'medications_total',
            'medication_adherence_rate', 'blood_pressure_status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserHealthMetricsCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating health metrics.
    """
    class Meta:
        model = UserHealthMetrics
        fields = [
            'date', 'weight', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature', 'mood_score', 'stress_level', 'sleep_hours',
            'exercise_minutes', 'medications_taken', 'medications_total', 'notes'
        ]
    
    def validate(self, attrs):
        """Validate health metrics data."""
        # Validate blood pressure
        systolic = attrs.get('blood_pressure_systolic')
        diastolic = attrs.get('blood_pressure_diastolic')
        
        if systolic and diastolic:
            if systolic < diastolic:
                raise serializers.ValidationError(
                    "Systolic pressure should be higher than diastolic pressure"
                )
            if systolic > 300 or diastolic > 200:
                raise serializers.ValidationError(
                    "Blood pressure values seem unrealistic"
                )
        
        # Validate heart rate
        heart_rate = attrs.get('heart_rate')
        if heart_rate and (heart_rate < 30 or heart_rate > 200):
            raise serializers.ValidationError(
                "Heart rate should be between 30 and 200 BPM"
            )
        
        # Validate temperature
        temperature = attrs.get('temperature')
        if temperature and (temperature < 30 or temperature > 45):
            raise serializers.ValidationError(
                "Temperature should be between 30°C and 45°C"
            )
        
        # Validate mood and stress scores
        mood_score = attrs.get('mood_score')
        if mood_score and (mood_score < 1 or mood_score > 10):
            raise serializers.ValidationError(
                "Mood score should be between 1 and 10"
            )
        
        stress_level = attrs.get('stress_level')
        if stress_level and (stress_level < 1 or stress_level > 10):
            raise serializers.ValidationError(
                "Stress level should be between 1 and 10"
            )
        
        return attrs


class DashboardAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for DashboardAnalytics model.
    """
    health_trend_display = serializers.CharField(source='get_health_trend_display', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    
    class Meta:
        model = DashboardAnalytics
        fields = [
            'id', 'date', 'login_count', 'reminder_interactions', 'mental_health_entries',
            'community_posts', 'health_trend', 'health_trend_display', 'ai_insights',
            'recommendations', 'risk_level', 'risk_level_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for UserGoal model.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = UserGoal
        fields = [
            'id', 'title', 'description', 'category', 'category_display',
            'target_value', 'current_value', 'unit', 'start_date', 'target_date',
            'status', 'status_display', 'milestones', 'progress_notes',
            'progress_percentage', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserGoalCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user goals.
    """
    class Meta:
        model = UserGoal
        fields = [
            'title', 'description', 'category', 'target_value', 'unit',
            'start_date', 'target_date', 'milestones'
        ]
    
    def validate(self, attrs):
        """Validate goal data."""
        start_date = attrs.get('start_date')
        target_date = attrs.get('target_date')
        
        if target_date and start_date and target_date <= start_date:
            raise serializers.ValidationError(
                "Target date must be after start date"
            )
        
        return attrs


class UserGoalUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user goals.
    """
    class Meta:
        model = UserGoal
        fields = [
            'title', 'description', 'category', 'target_value', 'current_value',
            'unit', 'target_date', 'status', 'milestones', 'progress_notes'
        ]


class DashboardSummarySerializer(serializers.Serializer):
    """
    Serializer for dashboard summary data.
    """
    # User profile summary
    user_info = serializers.DictField()
    
    # Reminder summary
    reminder_summary = serializers.DictField()
    
    # Mental health summary
    mental_health_summary = serializers.DictField()
    
    # Appointment summary
    appointment_summary = serializers.DictField()
    
    # Community activity summary
    community_summary = serializers.DictField()
    
    # AI analysis summary
    ai_analysis_summary = serializers.DictField()
    
    # Health metrics summary
    health_metrics_summary = serializers.DictField()
    
    # Goals summary
    goals_summary = serializers.DictField()
    
    # Recent activity
    recent_activity = serializers.ListField()
    
    # Notifications
    notifications = serializers.ListField()
    
    # Widgets configuration
    widgets = DashboardWidgetSerializer(many=True)


class HealthMetricsTrendSerializer(serializers.Serializer):
    """
    Serializer for health metrics trends over time.
    """
    dates = serializers.ListField(child=serializers.DateField())
    weight_data = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    blood_pressure_data = serializers.ListField(child=serializers.DictField(), required=False)
    mood_data = serializers.ListField(child=serializers.IntegerField(), required=False)
    stress_data = serializers.ListField(child=serializers.IntegerField(), required=False)
    sleep_data = serializers.ListField(child=serializers.DecimalField(max_digits=3, decimal_places=1), required=False)
    exercise_data = serializers.ListField(child=serializers.IntegerField(), required=False)
    adherence_data = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)


class GoalProgressSerializer(serializers.Serializer):
    """
    Serializer for goal progress tracking.
    """
    goal_id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField()
    current_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    target_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    progress_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_overdue = serializers.BooleanField()
    days_remaining = serializers.IntegerField(required=False)
