# Health Dashboard Django Backend

A comprehensive Django REST Framework backend for a health dashboard application with JWT authentication, pill reminders, mental health tracking, doctor appointments, community features, and AI analysis.

## 🚀 Features

### Authentication & User Management
- **JWT Authentication** for API endpoints
- **Session Authentication** for Django admin (both work together)
- User registration, login, password reset
- Extended user profiles with health information
- Role-based access control (patient, doctor, admin)

### Pill Reminders & Notifications
- Complete CRUD operations for medication reminders
- Flexible scheduling (daily, weekly, monthly, custom)
- Firebase Cloud Messaging integration for push notifications
- Reminder logs and adherence tracking
- Notification templates and history

### Dashboard & Analytics
- Comprehensive dashboard with customizable widgets
- Health metrics tracking (weight, blood pressure, mood, stress, sleep, exercise)
- Goal setting and progress tracking
- Data aggregation and trend analysis
- User activity analytics

### Mental Health Module
- Mood and stress tracking
- Mental health articles and exercises
- Progress monitoring and insights
- Personalized recommendations

### Doctors & Appointments
- Doctor profiles and specializations
- Appointment booking and management
- Availability scheduling
- Search and filtering capabilities

### Community Features
- Forum system with posts, comments, and likes
- User engagement tracking
- Moderation tools for admins
- Activity feeds and notifications

### AI Analysis & Chatbot
- AI-powered health insights
- OpenAI integration for mental health support
- Personalized recommendations
- Chatbot for health-related questions

## 🏗️ Project Structure

```
backend/
├── backend/                 # Main Django project
│   ├── settings.py         # Django settings with all configurations
│   ├── urls.py            # Main URL routing
│   └── celery.py          # Celery configuration for background tasks
├── users/                  # User authentication and profiles
│   ├── models.py          # UserProfile model
│   ├── serializers.py     # JWT and profile serializers
│   ├── views.py           # Authentication views
│   ├── urls.py            # Auth endpoints
│   └── admin.py           # Admin interface
├── reminders/              # Pill reminders and notifications
│   ├── models.py          # Reminder, ReminderLog, Notification models
│   ├── serializers.py     # CRUD serializers
│   ├── views.py           # Reminder management views
│   ├── urls.py            # Reminder endpoints
│   ├── admin.py           # Admin interface
│   └── services/          # Firebase notification service
├── dashboard/              # Dashboard and analytics
│   ├── models.py          # Widgets, health metrics, goals
│   ├── serializers.py     # Data aggregation serializers
│   ├── views.py           # Dashboard views
│   ├── urls.py            # Dashboard endpoints
│   └── admin.py           # Admin interface
├── mental_health/          # Mental health tracking
├── doctors/                # Doctor and appointment management
├── community/              # Community and forum features
├── ai/                     # AI analysis and chatbot
├── health_api/             # Existing health API (kept for compatibility)
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── manage.py              # Django management script
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite for development)
- Redis (for Celery, optional)
- Firebase project (for notifications)

### 1. Clone and Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `env.example` to `.env` and configure:
```bash
cp env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
# For SQLite (default)
python manage.py makemigrations
python manage.py migrate

# For PostgreSQL
# Update DATABASES in settings.py
# Install psycopg2-binary
# Run migrations
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables
```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=health_dashboard_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1

# Firebase
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id

# OpenAI
OPENAI_API_KEY=your-openai-key

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0
```

### Firebase Setup
1. Create a Firebase project
2. Download service account credentials
3. Update environment variables
4. Configure Firebase Admin SDK

### OpenAI Setup
1. Get API key from OpenAI
2. Add to environment variables
3. Configure in settings.py

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/auth/register/          # User registration
POST /api/auth/login/             # JWT login
POST /api/auth/refresh/           # Refresh JWT token
GET  /api/auth/profile/           # Get user profile
PUT  /api/auth/profile/update/    # Update profile
POST /api/auth/change-password/   # Change password
POST /api/auth/reset-password/    # Request password reset
```

### Reminder Endpoints
```
GET    /api/reminders/reminders/          # List reminders
POST   /api/reminders/reminders/          # Create reminder
GET    /api/reminders/reminders/{id}/     # Get reminder
PUT    /api/reminders/reminders/{id}/     # Update reminder
DELETE /api/reminders/reminders/{id}/     # Delete reminder
POST   /api/reminders/reminders/{id}/mark_taken/  # Mark as taken
POST   /api/reminders/reminders/{id}/snooze/      # Snooze reminder
GET    /api/reminders/reminders/due_today/        # Get due today
GET    /api/reminders/reminders/summary/          # Get summary
```

### Dashboard Endpoints
```
GET /api/dashboard/summary/                    # Comprehensive dashboard
GET /api/dashboard/widgets/                    # User widgets
GET /api/dashboard/health-metrics/             # Health metrics
GET /api/dashboard/health-metrics/trends/      # Health trends
GET /api/dashboard/goals/                      # User goals
POST /api/dashboard/goals/{id}/update_progress/ # Update goal progress
```

### Swagger Documentation
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **API Schema**: `/swagger<format>/`

## 🔐 Authentication

### JWT Tokens
- **Access Token**: Short-lived (5 hours by default)
- **Refresh Token**: Long-lived (1 day by default)
- **Header Format**: `Authorization: Bearer <token>`

### Session Authentication
- Django admin interface
- Template-based views
- CSRF protection enabled

### Permission Classes
- `IsAuthenticated`: Default for most endpoints
- `AllowAny`: Public endpoints (login, register)
- Custom permissions for role-based access

## 📱 Firebase Integration

### Notification Service
```python
from reminders.services.firebase_service import FirebaseNotificationService

service = FirebaseNotificationService()
result = service.send_notification(
    token="user_firebase_token",
    title="Medication Reminder",
    body="Time to take your medicine",
    data={"reminder_id": 123}
)
```

### Features
- Push notifications to mobile devices
- Topic-based messaging
- Multicast messaging
- Delivery status tracking

## 🤖 AI Integration

### OpenAI Integration
```python
# Configure in settings.py
OPENAI_API_KEY = "your-api-key"

# Use in views
import openai
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
```

### AI Analysis Endpoints
- `/api/ai/analysis/` - Health data analysis
- `/api/ai/chatbot/` - Mental health chatbot

## 🗄️ Database Models

### Key Models
- **UserProfile**: Extended user information
- **Reminder**: Medication reminders
- **ReminderLog**: Reminder history
- **Notification**: Push notifications
- **UserHealthMetrics**: Health tracking data
- **DashboardWidget**: User dashboard configuration
- **UserGoal**: Health and wellness goals

### Relationships
- One-to-one: User ↔ UserProfile
- One-to-many: User ↔ Reminders, Notifications, Goals
- Many-to-many: Users ↔ Community posts

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/HTTPS
- [ ] Configure static/media files
- [ ] Set up logging
- [ ] Configure Celery workers
- [ ] Set up monitoring

### Docker Support
```dockerfile
# Example Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
python manage.py test users
python manage.py test reminders
python manage.py test dashboard
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 Monitoring & Logging

### Logging Configuration
- File logging to `logs/django.log`
- Console logging for development
- Structured logging with context

### Health Checks
- Database connectivity
- External service status
- API endpoint health

## 🔧 Development

### Code Style
- Follow PEP 8
- Use type hints where possible
- Comprehensive docstrings
- Meaningful variable names

### Git Workflow
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# Create pull request
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## 🔮 Future Enhancements

- [ ] Real-time WebSocket support
- [ ] Advanced analytics dashboard
- [ ] Machine learning health predictions
- [ ] Integration with health devices
- [ ] Multi-language support
- [ ] Mobile app API endpoints
- [ ] Advanced reporting system
- [ ] Telemedicine features

---

**Built with ❤️ using Django REST Framework**
