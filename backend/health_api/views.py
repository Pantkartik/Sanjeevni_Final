from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.http import HttpResponse
import logging

from .models import (
    User, PillReminder, HealthData, Doctor, Appointment, 
    MentalHealthEntry, Notification, PillTaken
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, PillReminderSerializer,
    HealthDataSerializer, DoctorSerializer, AppointmentSerializer,
    MentalHealthEntrySerializer, NotificationSerializer, DashboardStatsSerializer
)

logger = logging.getLogger(__name__)

class HomeView(APIView):
    """Simple home view for the root URL"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sanjeevni Health API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2563eb; text-align: center; }
                .endpoint { background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2563eb; }
                .method { background: #2563eb; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }
                .url { font-family: monospace; color: #1e40af; }
                .description { color: #64748b; margin-top: 5px; }
                .admin-link { text-align: center; margin-top: 30px; }
                .admin-link a { background: #dc2626; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏥 Sanjeevni Health API</h1>
                <p style="text-align: center; color: #64748b; margin-bottom: 30px;">
                    Welcome to the Sanjeevni Health Application Backend API
                </p>
                
                <h2>Available Endpoints:</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/</span>
                    <div class="description">API root - lists all available endpoints</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/auth/register/</span>
                    <div class="description">User registration</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/auth/login/</span>
                    <div class="description">User login</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/auth/logout/</span>
                    <div class="description">User logout</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/dashboard/</span>
                    <div class="description">User dashboard with health statistics</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/users/</span>
                    <div class="description">User management endpoints</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/pill-reminders/</span>
                    <div class="description">Pill reminder management</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/health-data/</span>
                    <div class="description">Health data management</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/doctors/</span>
                    <div class="description">Doctor management</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/appointments/</span>
                    <div class="description">Appointment management</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/mental-health/</span>
                    <div class="description">Mental health tracking</div>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/notifications/</span>
                    <div class="description">Notification management</div>
                </div>
                
                <div class="admin-link">
                    <a href="/admin/">🔐 Access Django Admin</a>
                </div>
                
                <p style="text-align: center; margin-top: 30px; color: #64748b; font-size: 14px;">
                    Frontend should be running at: <strong>http://localhost:3000</strong>
                </p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content, content_type='text/html')

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = UserRegistrationSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    token, created = Token.objects.get_or_create(user=user)
                    logger.info(f"New user registered: {user.email}")
                    
                    # Create welcome notification
                    Notification.objects.create(
                        user=user,
                        title="Welcome to Sanjeevni!",
                        message="Thank you for joining our health platform. Start by adding your health data and setting up pill reminders.",
                        notification_type='general'
                    )
                    
                    return Response({
                        'user': UserSerializer(user).data,
                        'token': token.key,
                        'message': 'User registered successfully'
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"User registration failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Registration failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"User logged in: {user.email}")
                
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key,
                    'message': 'Login successful'
                })
            return Response({
                'error': 'Invalid credentials',
                'message': 'Login failed'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"User login failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Login failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to logout
            request.user.auth_token.delete()
            logger.info(f"User logged out: {request.user.email}")
            return Response({
                'message': 'Logout successful'
            })
        except Exception as e:
            logger.error(f"User logout failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Logout failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                with transaction.atomic():
                    user = serializer.save()
                    logger.info(f"User profile updated: {user.email}")
                    
                    # Create notification for profile update
                    Notification.objects.create(
                        user=user,
                        title="Profile Updated",
                        message="Your profile has been successfully updated.",
                        notification_type='general'
                    )
                    
                    return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        try:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            if not request.user.check_password(old_password):
                return Response({
                    'error': 'Invalid old password'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                request.user.set_password(new_password)
                request.user.save()
                
                # Delete old token and create new one
                request.user.auth_token.delete()
                new_token = Token.objects.create(user=request.user)
                
                logger.info(f"User password changed: {request.user.email}")
                
                return Response({
                    'message': 'Password changed successfully',
                    'token': new_token.key
                })
        except Exception as e:
            logger.error(f"Password change failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Password change failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PillReminderViewSet(viewsets.ModelViewSet):
    queryset = PillReminder.objects.all()
    serializer_class = PillReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PillReminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            reminder = serializer.save(user=self.request.user)
            logger.info(f"Pill reminder created: {reminder.id} for user {reminder.user.email}")
            
            # Create notification for new reminder
            Notification.objects.create(
                user=reminder.user,
                title="New Pill Reminder",
                message=f"Pill reminder '{reminder.medication_name}' has been set for {reminder.times}",
                notification_type='pill_reminder'
            )

    def perform_update(self, serializer):
        with transaction.atomic():
            reminder = serializer.save()
            logger.info(f"Pill reminder updated: {reminder.id} for user {reminder.user.email}")
            
            # Create notification for reminder update
            Notification.objects.create(
                user=reminder.user,
                title="Pill Reminder Updated",
                message=f"Pill reminder '{reminder.medication_name}' has been updated",
                notification_type='pill_reminder'
            )

    def perform_destroy(self, instance):
        with transaction.atomic():
            user_email = instance.user.email
            medication_name = instance.medication_name
            instance.delete()
            logger.info(f"Pill reminder deleted: {medication_name} for user {user_email}")
            
            # Create notification for reminder deletion
            Notification.objects.create(
                user=instance.user,
                title="Pill Reminder Deleted",
                message=f"Pill reminder '{medication_name}' has been removed",
                notification_type='pill_reminder'
            )

    @action(detail=True, methods=['post'])
    def mark_taken(self, request, pk=None):
        try:
            reminder = self.get_object()
            scheduled_time = request.data.get('scheduled_time')
            
            # Check if already taken for this scheduled time today
            if PillTaken.objects.filter(
                reminder=reminder,
                scheduled_time=scheduled_time,
                taken_at__date=timezone.now().date()
            ).exists():
                return Response({
                    'error': 'Pill already marked as taken for this time today'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                PillTaken.objects.create(
                    reminder=reminder,
                    scheduled_time=scheduled_time,
                    taken_at=timezone.now()
                )
                
                logger.info(f"Pill marked as taken: {reminder.medication_name} for user {reminder.user.email}")
                
                # Create notification
                Notification.objects.create(
                    user=reminder.user,
                    title="Pill Taken",
                    message=f"Great! You've taken {reminder.medication_name}",
                    notification_type='pill_reminder'
                )
                
                return Response({
                    'message': 'Pill marked as taken successfully'
                })
        except Exception as e:
            logger.error(f"Mark pill taken failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Failed to mark pill as taken'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False)
    def adherence_stats(self, request):
        reminders = self.get_queryset()
        total_reminders = reminders.count()
        active_reminders = reminders.filter(is_active=True).count()
        
        # Calculate adherence
        total_pills = sum(reminder.frequency for reminder in reminders)
        taken_pills = PillTaken.objects.filter(reminder__user=request.user).count()
        adherence = (taken_pills / total_pills * 100) if total_pills > 0 else 0
        
        return Response({
            'total_reminders': total_reminders,
            'active_reminders': active_reminders,
            'adherence': round(adherence, 2),
            'total_pills': total_pills,
            'taken_pills': taken_pills
        })

    @action(detail=False)
    def overdue_pills(self, request):
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        overdue_pills = []
        reminders = self.get_queryset().filter(is_active=True)
        
        for reminder in reminders:
            for time in reminder.times:
                scheduled_time = datetime.strptime(time, '%H:%M').time()
                scheduled_datetime = datetime.combine(timezone.now().date(), scheduled_time)
                
                if scheduled_datetime < timezone.now() - timedelta(hours=1):
                    # Check if not taken
                    if not PillTaken.objects.filter(
                        reminder=reminder,
                        scheduled_time=time,
                        taken_at__date=timezone.now().date()
                    ).exists():
                        overdue_pills.append({
                            'reminder_id': reminder.id,
                            'medication_name': reminder.medication_name,
                            'scheduled_time': time,
                            'overdue_hours': int((timezone.now() - scheduled_datetime).total_seconds() / 3600)
                        })
        
        return Response(overdue_pills)

class HealthDataViewSet(viewsets.ModelViewSet):
    queryset = HealthData.objects.all()
    serializer_class = HealthDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            health_data = serializer.save(user=self.request.user)
            logger.info(f"Health data recorded: {health_data.data_type} for user {health_data.user.email}")
            
            # Check for health alerts
            self._check_health_alerts(health_data)
            
            # Create notification
            Notification.objects.create(
                user=health_data.user,
                title="Health Data Recorded",
                message=f"Your {health_data.data_type} has been recorded: {health_data.value} {health_data.unit}",
                notification_type='health_data'
            )

    def _check_health_alerts(self, health_data):
        """Check if health data values are concerning and create alerts"""
        alerts = []
        
        if health_data.data_type == 'blood_pressure':
            systolic, diastolic = map(int, health_data.value.split('/'))
            if systolic > 140 or diastolic > 90:
                alerts.append(f"High blood pressure: {health_data.value}")
        
        elif health_data.data_type == 'heart_rate':
            heart_rate = int(health_data.value)
            if heart_rate > 100 or heart_rate < 60:
                alerts.append(f"Abnormal heart rate: {heart_rate} bpm")
        
        elif health_data.data_type == 'blood_sugar':
            blood_sugar = float(health_data.value)
            if blood_sugar > 140:
                alerts.append(f"High blood sugar: {blood_sugar} mg/dL")
        
        # Create alert notifications
        for alert in alerts:
            Notification.objects.create(
                user=health_data.user,
                title="Health Alert",
                message=alert,
                notification_type='health_alert'
            )

    @action(detail=False)
    def latest(self, request):
        latest_data = self.get_queryset().order_by('-recorded_at')[:10]
        serializer = self.get_serializer(latest_data, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def trends(self, request):
        from django.db.models import Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Get data from last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        trends = self.get_queryset().filter(
            recorded_at__gte=thirty_days_ago
        ).values('data_type').annotate(
            avg_value=Avg('value')
        )
        
        return Response(trends)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            doctor = serializer.save(user=self.request.user)
            logger.info(f"Doctor added: {doctor.name} for user {doctor.user.email}")
            
            # Create notification
            Notification.objects.create(
                user=doctor.user,
                title="Doctor Added",
                message=f"Dr. {doctor.name} has been added to your doctors list",
                notification_type='general'
            )

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            appointment = serializer.save(user=self.request.user)
            logger.info(f"Appointment scheduled: {appointment.title} for user {appointment.user.email}")
            
            # Create notification
            Notification.objects.create(
                user=appointment.user,
                title="Appointment Scheduled",
                message=f"Appointment '{appointment.title}' scheduled for {appointment.appointment_date}",
                notification_type='appointment'
            )

class MentalHealthEntryViewSet(viewsets.ModelViewSet):
    queryset = MentalHealthEntry.objects.all()
    serializer_class = MentalHealthEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MentalHealthEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            entry = serializer.save(user=self.request.user)
            logger.info(f"Mental health entry recorded for user {entry.user.email}")
            
            # Check for mental health alerts
            self._check_mental_health_alerts(entry)
            
            # Create notification
            Notification.objects.create(
                user=entry.user,
                title="Mental Health Entry",
                message="Your mental health entry has been recorded. Keep up the good work!",
                notification_type='mental_health'
            )

    def _check_mental_health_alerts(self, entry):
        """Check if mental health scores are concerning and create alerts"""
        alerts = []
        
        if entry.mood_score <= 3:
            alerts.append("Low mood detected. Consider reaching out for support.")
        
        if entry.anxiety_level >= 8:
            alerts.append("High anxiety level detected. Consider relaxation techniques.")
        
        if entry.stress_level >= 8:
            alerts.append("High stress level detected. Consider stress management strategies.")
        
        # Create alert notifications
        for alert in alerts:
            Notification.objects.create(
                user=entry.user,
                title="Mental Health Alert",
                message=alert,
                notification_type='health_alert'
            )

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            # Get basic stats
            total_pill_reminders = PillReminder.objects.filter(user=user).count()
            active_pill_reminders = PillReminder.objects.filter(user=user, is_active=True).count()
            
            # Calculate adherence
            total_pills = sum(reminder.frequency for reminder in PillReminder.objects.filter(user=user))
            taken_pills = PillTaken.objects.filter(reminder__user=user).count()
            average_adherence = (taken_pills / total_pills * 100) if total_pills > 0 else 0
            
            # Today's stats
            from django.utils import timezone
            from datetime import datetime, timedelta
            
            today = timezone.now().date()
            today_pills_taken = PillTaken.objects.filter(
                reminder__user=user,
                taken_at__date=today
            ).count()
            
            total_today_pills = 0
            for reminder in PillReminder.objects.filter(user=user, is_active=True):
                total_today_pills += reminder.frequency
            
            today_adherence = (today_pills_taken / total_today_pills * 100) if total_today_pills > 0 else 0
            
            # Other stats
            upcoming_appointments = Appointment.objects.filter(
                user=user,
                appointment_date__gte=timezone.now(),
                status__in=['scheduled', 'confirmed']
            ).count()
            
            recent_health_data = HealthData.objects.filter(user=user).order_by('-recorded_at')[:5]
            health_data_serializer = HealthDataSerializer(recent_health_data, many=True)
            
            unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
            
            # Mental health trend (last 7 days)
            week_ago = timezone.now() - timedelta(days=7)
            mental_health_trend = MentalHealthEntry.objects.filter(
                user=user,
                created_at__gte=week_ago
            ).order_by('created_at')
            mental_health_serializer = MentalHealthEntrySerializer(mental_health_trend, many=True)
            
            stats = {
                'total_pill_reminders': total_pill_reminders,
                'active_pill_reminders': active_pill_reminders,
                'average_adherence': round(average_adherence, 2),
                'today_adherence': round(today_adherence, 2),
                'upcoming_appointments': upcoming_appointments,
                'recent_health_data': health_data_serializer.data,
                'unread_notifications': unread_notifications,
                'mental_health_trend': mental_health_serializer.data,
                'today_pills_taken': today_pills_taken,
                'total_today_pills': total_today_pills
            }
            
            serializer = DashboardStatsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Dashboard data retrieval failed: {str(e)}")
            return Response({
                'error': str(e),
                'message': 'Failed to retrieve dashboard data'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
