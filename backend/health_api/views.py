from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Count, Q
from .models import (
    User, PillReminder, PillTaken, HealthData, Doctor, 
    Appointment, MentalHealthEntry, Notification
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    PillReminderSerializer, PillTakenSerializer, HealthDataSerializer,
    DoctorSerializer, AppointmentSerializer, MentalHealthEntrySerializer,
    NotificationSerializer, DashboardStatsSerializer
)


class DebugView(APIView):
    """Debug view to test API connectivity"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'message': 'Django API is working!',
            'timestamp': timezone.now().isoformat(),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
            'method': request.method,
        })

    def post(self, request):
        return Response({
            'message': 'POST request received',
            'data': request.data,
            'timestamp': timezone.now().isoformat(),
        })


class UserRegistrationView(APIView):
    """View for user registration"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key,
                    'message': 'User registered successfully'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Registration failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    """View for user login"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Login failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutView(APIView):
    """View for user logout"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PillReminderViewSet(viewsets.ModelViewSet):
    """ViewSet for PillReminder model"""
    serializer_class = PillReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PillReminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_taken(self, request, pk=None):
        """Mark a pill as taken"""
        reminder = self.get_object()
        scheduled_time = request.data.get('scheduled_time')
        notes = request.data.get('notes', '')

        if not scheduled_time:
            return Response(
                {'error': 'scheduled_time is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            scheduled_time = datetime.strptime(scheduled_time, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Invalid time format. Use HH:MM'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        PillTaken.objects.create(
            reminder=reminder,
            scheduled_time=scheduled_time,
            notes=notes
        )

        return Response({'message': 'Pill marked as taken'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def adherence_stats(self, request):
        """Get adherence statistics"""
        reminders = self.get_queryset()
        total_reminders = reminders.count()
        active_reminders = reminders.filter(is_active=True).count()
        
        adherence_data = []
        for reminder in reminders:
            total_scheduled = reminder.pills_taken.count()
            total_taken = reminder.pills_taken.filter(taken_at__isnull=False).count()
            adherence_rate = (total_taken / total_scheduled * 100) if total_scheduled > 0 else 0
            adherence_data.append({
                'reminder_id': reminder.id,
                'name': reminder.name,
                'adherence_rate': round(adherence_rate, 2)
            })

        return Response({
            'total_reminders': total_reminders,
            'active_reminders': active_reminders,
            'adherence_data': adherence_data
        })


class PillTakenViewSet(viewsets.ModelViewSet):
    """ViewSet for PillTaken model"""
    serializer_class = PillTakenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PillTaken.objects.filter(reminder__user=self.request.user)

    def perform_create(self, serializer):
        reminder_id = self.request.data.get('reminder_id')
        reminder = PillReminder.objects.get(id=reminder_id, user=self.request.user)
        serializer.save(reminder=reminder)


class HealthDataViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthData model"""
    serializer_class = HealthDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest health data for each type"""
        data_types = request.query_params.getlist('types', [])
        queryset = self.get_queryset()
        
        if data_types:
            queryset = queryset.filter(data_type__in=data_types)

        latest_data = {}
        for data_type in queryset.values_list('data_type', flat=True).distinct():
            latest = queryset.filter(data_type=data_type).first()
            if latest:
                latest_data[data_type] = HealthDataSerializer(latest).data

        return Response(latest_data)

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get health data trends"""
        data_type = request.query_params.get('type')
        days = int(request.query_params.get('days', 7))
        
        if not data_type:
            return Response(
                {'error': 'type parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = timezone.now() - timedelta(days=days)
        queryset = self.get_queryset().filter(
            data_type=data_type,
            recorded_at__gte=start_date
        ).order_by('recorded_at')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DoctorViewSet(viewsets.ModelViewSet):
    """ViewSet for Doctor model"""
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Appointment model"""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        queryset = self.get_queryset().filter(
            appointment_date__gte=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MentalHealthEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for MentalHealthEntry model"""
    serializer_class = MentalHealthEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MentalHealthEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get mental health trends"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.get_queryset().filter(
            recorded_at__gte=start_date
        ).order_by('recorded_at')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification model"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        queryset = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})


class DashboardView(APIView):
    """View for dashboard statistics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Pill reminder stats
        total_pill_reminders = PillReminder.objects.filter(user=user).count()
        active_pill_reminders = PillReminder.objects.filter(user=user, is_active=True).count()
        
        # Calculate average adherence
        adherence_rates = []
        for reminder in PillReminder.objects.filter(user=user):
            total_scheduled = reminder.pills_taken.count()
            total_taken = reminder.pills_taken.filter(taken_at__isnull=False).count()
            if total_scheduled > 0:
                adherence_rates.append((total_taken / total_scheduled) * 100)
        
        average_adherence = sum(adherence_rates) / len(adherence_rates) if adherence_rates else 0
        
        # Upcoming appointments
        upcoming_appointments = Appointment.objects.filter(
            user=user,
            appointment_date__gte=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).count()
        
        # Recent health data
        recent_health_data = HealthData.objects.filter(
            user=user
        ).order_by('-recorded_at')[:5]
        
        # Unread notifications
        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False
        ).count()
        
        # Mental health trend
        mental_health_trend = MentalHealthEntry.objects.filter(
            user=user
        ).order_by('-recorded_at')[:7]
        
        data = {
            'total_pill_reminders': total_pill_reminders,
            'active_pill_reminders': active_pill_reminders,
            'average_adherence': round(average_adherence, 2),
            'upcoming_appointments': upcoming_appointments,
            'recent_health_data': HealthDataSerializer(recent_health_data, many=True).data,
            'unread_notifications': unread_notifications,
            'mental_health_trend': MentalHealthEntrySerializer(mental_health_trend, many=True).data,
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
