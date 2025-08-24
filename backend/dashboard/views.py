"""
Views for dashboard app.
"""

from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Count, Avg, Max, Min
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, timedelta

from .models import DashboardWidget, UserHealthMetrics, DashboardAnalytics, UserGoal
from .serializers import (
    DashboardWidgetSerializer, DashboardWidgetUpdateSerializer,
    UserHealthMetricsSerializer, UserHealthMetricsCreateSerializer,
    DashboardAnalyticsSerializer, UserGoalSerializer, UserGoalCreateSerializer,
    UserGoalUpdateSerializer, DashboardSummarySerializer,
    HealthMetricsTrendSerializer, GoalProgressSerializer
)


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing dashboard widgets.
    """
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return widgets for the current user."""
        return DashboardWidget.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['update', 'partial_update']:
            return DashboardWidgetUpdateSerializer
        return DashboardWidgetSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a widget."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder dashboard widgets."""
        widget_orders = request.data.get('widget_orders', [])
        
        for order_data in widget_orders:
            widget_id = order_data.get('widget_id')
            position = order_data.get('position')
            
            try:
                widget = DashboardWidget.objects.get(
                    id=widget_id, user=request.user
                )
                widget.position = position
                widget.save()
            except DashboardWidget.DoesNotExist:
                continue
        
        return Response({'message': 'Widgets reordered successfully'})
    
    @action(detail=False, methods=['post'])
    def reset_defaults(self, request):
        """Reset dashboard to default widget configuration."""
        # Clear existing widgets
        DashboardWidget.objects.filter(user=request.user).delete()
        
        # Create default widgets
        default_widgets = [
            {'widget_type': 'reminders', 'position': 0},
            {'widget_type': 'mental_health', 'position': 1},
            {'widget_type': 'appointments', 'position': 2},
            {'widget_type': 'community', 'position': 3},
            {'widget_type': 'ai_analysis', 'position': 4},
            {'widget_type': 'health_stats', 'position': 5},
        ]
        
        for widget_data in default_widgets:
            DashboardWidget.objects.create(
                user=request.user,
                **widget_data
            )
        
        return Response({'message': 'Dashboard reset to defaults'})


class UserHealthMetricsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user health metrics.
    """
    serializer_class = UserHealthMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    
    def get_queryset(self):
        """Return health metrics for the current user."""
        return UserHealthMetrics.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return UserHealthMetricsCreateSerializer
        return UserHealthMetricsSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating health metrics."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get health metrics trends over time."""
        days = int(request.query_params.get('days', 30))
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        metrics = self.get_queryset().filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Prepare trend data
        dates = []
        weight_data = []
        blood_pressure_data = []
        mood_data = []
        stress_data = []
        sleep_data = []
        exercise_data = []
        adherence_data = []
        
        for metric in metrics:
            dates.append(metric.date)
            if metric.weight:
                weight_data.append(float(metric.weight))
            if metric.blood_pressure_systolic and metric.blood_pressure_diastolic:
                blood_pressure_data.append({
                    'systolic': metric.blood_pressure_systolic,
                    'diastolic': metric.blood_pressure_diastolic
                })
            if metric.mood_score:
                mood_data.append(metric.mood_score)
            if metric.stress_level:
                stress_data.append(metric.stress_level)
            if metric.sleep_hours:
                sleep_data.append(float(metric.sleep_hours))
            if metric.exercise_minutes:
                exercise_data.append(metric.exercise_minutes)
            if metric.medication_adherence_rate:
                adherence_data.append(metric.medication_adherence_rate)
        
        trend_data = {
            'dates': dates,
            'weight_data': weight_data,
            'blood_pressure_data': blood_pressure_data,
            'mood_data': mood_data,
            'stress_data': stress_data,
            'sleep_data': sleep_data,
            'exercise_data': exercise_data,
            'adherence_data': adherence_data,
        }
        
        serializer = HealthMetricsTrendSerializer(trend_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary of health metrics."""
        # Get latest metrics
        latest_metrics = self.get_queryset().order_by('-date').first()
        
        # Get averages for the last 30 days
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_metrics = self.get_queryset().filter(date__gte=thirty_days_ago)
        
        summary_data = {
            'latest_metrics': UserHealthMetricsSerializer(latest_metrics).data if latest_metrics else None,
            'averages_30_days': {
                'mood_score': recent_metrics.aggregate(Avg('mood_score'))['mood_score__avg'],
                'stress_level': recent_metrics.aggregate(Avg('stress_level'))['stress_level__avg'],
                'sleep_hours': recent_metrics.aggregate(Avg('sleep_hours'))['sleep_hours__avg'],
                'exercise_minutes': recent_metrics.aggregate(Avg('exercise_minutes'))['exercise_minutes__avg'],
                'medication_adherence': recent_metrics.aggregate(Avg('medications_taken'))['medications_taken__avg'],
            },
            'trends': {
                'weight_trend': self._calculate_trend('weight', recent_metrics),
                'mood_trend': self._calculate_trend('mood_score', recent_metrics),
                'stress_trend': self._calculate_trend('stress_level', recent_metrics),
            }
        }
        
        return Response(summary_data)
    
    def _calculate_trend(self, field, queryset):
        """Calculate trend for a specific field."""
        values = list(queryset.values_list(field, flat=True).exclude(**{f'{field}__isnull': True}))
        if len(values) < 2:
            return 'stable'
        
        # Simple trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg * 1.1:
            return 'improving'
        elif second_avg < first_avg * 0.9:
            return 'declining'
        else:
            return 'stable'


class DashboardAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing dashboard analytics (read-only).
    """
    serializer_class = DashboardAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'health_trend', 'risk_level']
    
    def get_queryset(self):
        """Return analytics for the current user."""
        return DashboardAnalytics.objects.filter(user=self.request.user)


class UserGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user goals.
    """
    serializer_class = UserGoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'status']
    
    def get_queryset(self):
        """Return goals for the current user."""
        return UserGoal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return UserGoalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserGoalUpdateSerializer
        return UserGoalSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a goal."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update goal progress."""
        goal = self.get_object()
        new_value = request.data.get('current_value')
        
        if new_value is not None:
            goal.current_value = new_value
            goal.save()
            
            return Response({
                'message': 'Progress updated successfully',
                'progress_percentage': goal.progress_percentage
            })
        
        return Response(
            {'error': 'current_value is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        """Get summary of goal progress."""
        goals = self.get_queryset().filter(status='active')
        
        progress_data = []
        for goal in goals:
            days_remaining = None
            if goal.target_date:
                days_remaining = (goal.target_date - date.today()).days
            
            progress_data.append({
                'goal_id': goal.id,
                'title': goal.title,
                'category': goal.category,
                'current_value': goal.current_value,
                'target_value': goal.target_value,
                'progress_percentage': goal.progress_percentage,
                'is_overdue': goal.is_overdue,
                'days_remaining': days_remaining
            })
        
        serializer = GoalProgressSerializer(progress_data, many=True)
        return Response(serializer.data)


class DashboardSummaryView(generics.RetrieveAPIView):
    """
    View for getting comprehensive dashboard summary.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """Get comprehensive dashboard summary."""
        user = request.user
        
        # Get user info
        user_info = {
            'username': user.username,
            'full_name': user.get_full_name(),
            'role': getattr(user.profile, 'role', 'patient'),
            'date_joined': user.date_joined,
        }
        
        # Get reminder summary (from reminders app)
        try:
            from reminders.models import Reminder, ReminderLog
            total_reminders = Reminder.objects.filter(user=user).count()
            active_reminders = Reminder.objects.filter(user=user, status='active').count()
            today_logs = ReminderLog.objects.filter(
                reminder__user=user,
                scheduled_time__date=date.today()
            )
            taken_today = today_logs.filter(status='taken').count()
            missed_today = today_logs.filter(status='missed').count()
            
            reminder_summary = {
                'total': total_reminders,
                'active': active_reminders,
                'taken_today': taken_today,
                'missed_today': missed_today,
            }
        except ImportError:
            reminder_summary = {'error': 'Reminders app not available'}
        
        # Get mental health summary (placeholder)
        mental_health_summary = {
            'entries_this_week': 0,
            'mood_trend': 'stable',
            'stress_level': 'medium',
        }
        
        # Get appointment summary (placeholder)
        appointment_summary = {
            'upcoming': 0,
            'completed_this_month': 0,
            'cancelled_this_month': 0,
        }
        
        # Get community activity summary (placeholder)
        community_summary = {
            'posts_this_week': 0,
            'comments_this_week': 0,
            'likes_received': 0,
        }
        
        # Get AI analysis summary (placeholder)
        ai_analysis_summary = {
            'last_analysis': None,
            'insights_count': 0,
            'recommendations_count': 0,
        }
        
        # Get health metrics summary
        try:
            latest_metrics = UserHealthMetrics.objects.filter(user=user).order_by('-date').first()
            health_metrics_summary = {
                'latest_weight': latest_metrics.weight if latest_metrics else None,
                'latest_mood': latest_metrics.mood_score if latest_metrics else None,
                'latest_stress': latest_metrics.stress_level if latest_metrics else None,
                'blood_pressure_status': latest_metrics.blood_pressure_status if latest_metrics else None,
            }
        except:
            health_metrics_summary = {'error': 'Health metrics not available'}
        
        # Get goals summary
        active_goals = UserGoal.objects.filter(user=user, status='active')
        goals_summary = {
            'total_active': active_goals.count(),
            'completed_this_month': UserGoal.objects.filter(
                user=user, status='completed',
                updated_at__month=timezone.now().month
            ).count(),
            'overdue': active_goals.filter(
                target_date__lt=date.today()
            ).count(),
        }
        
        # Get recent activity (placeholder)
        recent_activity = []
        
        # Get notifications (from reminders app)
        try:
            from reminders.models import Notification
            notifications = Notification.objects.filter(
                user=user, status='pending'
            ).order_by('-created_at')[:5]
            notifications_data = []
            for notif in notifications:
                notifications_data.append({
                    'id': notif.id,
                    'title': notif.title,
                    'type': notif.notification_type,
                    'created_at': notif.created_at,
                })
        except ImportError:
            notifications_data = []
        
        # Get widgets configuration
        widgets = DashboardWidget.objects.filter(user=user, is_enabled=True).order_by('position')
        widgets_data = DashboardWidgetSerializer(widgets, many=True).data
        
        summary_data = {
            'user_info': user_info,
            'reminder_summary': reminder_summary,
            'mental_health_summary': mental_health_summary,
            'appointment_summary': appointment_summary,
            'community_summary': community_summary,
            'ai_analysis_summary': ai_analysis_summary,
            'health_metrics_summary': health_metrics_summary,
            'goals_summary': goals_summary,
            'recent_activity': recent_activity,
            'notifications': notifications_data,
            'widgets': widgets_data,
        }
        
        serializer = DashboardSummarySerializer(summary_data)
        return Response(serializer.data)
