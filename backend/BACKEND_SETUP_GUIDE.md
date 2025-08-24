# Sanjeevni Health Application - Backend Setup Guide

This guide will help you set up the Django backend for the Sanjeevni health application with full backend control over all frontend actions.

## 🎯 What This Backend Provides

The Django backend is designed to control and manage **every action** performed in the frontend:

- ✅ **User Authentication & Authorization** (Login, Logout, Sign up, Password changes)
- ✅ **Data Entry Control** (All form submissions, data validation, business logic)
- ✅ **Button Action Management** (Every click, form submission, data modification)
- ✅ **Real-time Notifications** (In-app notifications, email alerts)
- ✅ **Background Task Processing** (Pill reminders, health alerts, data cleanup)
- ✅ **Data Validation & Security** (Input sanitization, permission checks)
- ✅ **Audit Logging** (Track all user actions, data changes)
- ✅ **Health Monitoring** (Automatic health alerts, trend analysis)

## 🏗️ Architecture Overview

```
Frontend (React/Next.js) ←→ Django Backend ←→ PostgreSQL Database
                              ↓
                        Celery + Redis
                              ↓
                    Background Tasks & Scheduling
```

## 📋 Prerequisites

Before setting up the backend, ensure you have:

- Python 3.8+ installed
- PostgreSQL 12+ installed and running
- Redis server installed and running
- Git installed

## 🚀 Quick Setup (Automated)

### Option 1: Automated Setup Script

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Run the automated setup script:**
   ```bash
   python setup_database.py
   ```

   This script will:
   - Check PostgreSQL installation
   - Create database and user
   - Update environment configuration
   - Install dependencies
   - Run migrations
   - Create admin user

### Option 2: Manual Setup

If you prefer manual setup or the automated script fails:

## 🔧 Manual Setup Steps

### 1. Install PostgreSQL

**Windows:**
- Download from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)
- Install with default settings
- Remember the password you set for the `postgres` user

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Install Redis

**Windows:**
- Download from [Redis Downloads](https://redis.io/download)
- Or use WSL2 with Ubuntu

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 3. Create Database and User

1. **Connect to PostgreSQL as superuser:**
   ```bash
   sudo -u postgres psql
   ```

2. **Create database and user:**
   ```sql
   CREATE USER sanjeevni_user WITH PASSWORD 'sanjeevni_password';
   CREATE DATABASE sanjeevni_db OWNER sanjeevni_user;
   GRANT ALL PRIVILEGES ON DATABASE sanjeevni_db TO sanjeevni_user;
   \q
   ```

### 4. Set Up Environment Configuration

1. **Copy the environment template:**
   ```bash
   cp env.example .env
   ```

2. **Edit the .env file with your configuration:**
   ```bash
   # Database Configuration
   DATABASE_URL=postgresql://sanjeevni_user:sanjeevni_password@localhost:5432/sanjeevni_db
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=sanjeevni_db
   DB_USER=sanjeevni_user
   DB_PASSWORD=sanjeevni_password
   DB_HOST=localhost
   DB_PORT=5432

   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   JWT_ACCESS_TOKEN_LIFETIME=5
   JWT_REFRESH_TOKEN_LIFETIME=1

   # Redis Configuration
   REDIS_URL=redis://localhost:6379/0

   # Email Configuration (optional for development)
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Test the Setup

```bash
python manage.py runserver
```

Visit `http://localhost:8000/api/debug/` to test the API.

## 🚀 Starting the Application

### 1. Start Django Server

```bash
python manage.py runserver
```

### 2. Start Celery Worker (Background Tasks)

```bash
celery -A backend worker --loglevel=info
```

### 3. Start Celery Beat (Scheduled Tasks)

```bash
celery -A backend beat --loglevel=info
```

### 4. Start Redis (if not running as service)

```bash
redis-server
```

## 🔐 Authentication & Security

The backend uses **JWT (JSON Web Tokens)** for authentication:

- **Access Token**: Valid for 5 hours (configurable)
- **Refresh Token**: Valid for 1 day (configurable)
- **Automatic token rotation** for security
- **Rate limiting** to prevent abuse
- **CORS protection** for frontend integration

### API Authentication Flow

1. **Register/Login** → Receive JWT tokens
2. **Include token** in Authorization header: `Bearer <access_token>`
3. **Automatic refresh** when access token expires
4. **Secure logout** with token invalidation

## 📊 Database Models

The backend includes comprehensive models for:

- **User Management** (Custom user model with health fields)
- **Pill Reminders** (Medication tracking with adherence)
- **Health Data** (Vital signs, measurements, trends)
- **Mental Health** (Mood tracking, wellness monitoring)
- **Appointments** (Doctor consultations, scheduling)
- **Notifications** (In-app alerts, reminders)
- **Audit Logs** (Action tracking, data changes)

## 🔄 Background Tasks & Automation

### Celery Tasks

- **Pill Reminders**: Send notifications at scheduled times
- **Health Alerts**: Monitor vital signs for concerning values
- **Stock Management**: Alert when medication is running low
- **Daily Reports**: Generate health summaries
- **Data Cleanup**: Maintain database performance
- **Appointment Reminders**: Notify users of upcoming visits

### Task Scheduling

- Pill reminders: Every 5 minutes
- Stock checks: Every hour
- Health reports: Daily
- Data cleanup: Weekly

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### User Management
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/change_password/` - Change password

### Pill Management
- `GET /api/pill-reminders/` - List reminders
- `POST /api/pill-reminders/` - Create reminder
- `POST /api/pill-reminders/{id}/mark_taken/` - Mark pill taken
- `GET /api/pill-reminders/adherence_stats/` - Get adherence
- `GET /api/pill-reminders/overdue_pills/` - Get overdue pills

### Health Data
- `GET /api/health-data/` - List health data
- `POST /api/health-data/` - Add health data
- `GET /api/health-data/latest/` - Get latest data
- `GET /api/health-data/trends/` - Get trends

### Dashboard
- `GET /api/dashboard/` - Get comprehensive stats

## 🛡️ Security Features

- **JWT Authentication** with automatic refresh
- **Rate Limiting** (100 requests/day for anonymous, 1000/day for users)
- **Input Validation** and sanitization
- **SQL Injection Protection** via Django ORM
- **XSS Protection** with security headers
- **CSRF Protection** for web forms
- **Permission-based Access Control**

## 📝 Logging & Monitoring

The backend includes comprehensive logging:

- **User Actions**: Login, logout, data changes
- **System Events**: Task execution, errors, warnings
- **Health Metrics**: API performance, database queries
- **Security Events**: Failed logins, permission violations

Logs are stored in `logs/django.log` and also displayed in console.

## 🔧 Configuration Options

### Environment Variables

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: JWT signing key
- `EMAIL_*`: Email configuration
- `CORS_*`: Cross-origin settings

### Django Settings

- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for session storage and caching
- **Static Files**: WhiteNoise for production serving
- **Media Files**: Local storage with configurable backends
- **Security**: HTTPS redirects, HSTS, security headers

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify database credentials in .env
   - Ensure database and user exist

2. **Redis Connection Failed**
   - Check Redis server is running
   - Verify Redis URL in .env
   - Test connection: `redis-cli ping`

3. **Migration Errors**
   - Delete existing migrations: `rm -rf health_api/migrations/`
   - Recreate: `python manage.py makemigrations`
   - Apply: `python manage.py migrate`

4. **Celery Tasks Not Running**
   - Check Redis is running
   - Verify Celery worker is started
   - Check task queue: `celery -A backend inspect active`

### Debug Mode

Enable debug mode in `.env`:
```
DEBUG=True
```

This will show detailed error messages and SQL queries.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

## 🤝 Support

If you encounter issues:

1. Check the logs in `logs/django.log`
2. Verify all services are running
3. Check environment configuration
4. Review this setup guide
5. Check the troubleshooting section above

## 🎉 Next Steps

After successful setup:

1. **Test the API** with the debug endpoint
2. **Create test data** through the admin interface
3. **Integrate with frontend** using the API endpoints
4. **Configure production settings** for deployment
5. **Set up monitoring** and alerting

---

**Happy coding! 🚀**

The Sanjeevni backend is now ready to control and manage all your frontend actions with enterprise-grade security and reliability.
