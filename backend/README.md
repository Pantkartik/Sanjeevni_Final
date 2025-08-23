# Health Application Django Backend

A comprehensive Django REST API backend for the Sanjeevni health application.

## Features

- **User Authentication**: Custom user model with email-based authentication
- **Pill Reminders**: Complete medication management system
- **Health Data Tracking**: Store and retrieve various health metrics
- **Doctor Management**: Store doctor information and appointments
- **Mental Health Tracking**: Mood and wellness monitoring
- **Notifications**: In-app notification system
- **Dashboard Analytics**: Comprehensive health insights

## Models

### User
- Custom user model with health-specific fields
- Email-based authentication
- Profile information (phone, DOB, gender, emergency contact)

### PillReminder
- Medication name, dosage, frequency
- Multiple reminder times per day
- Stock tracking
- Caregiver notifications

### HealthData
- Various health metrics (blood pressure, heart rate, weight, etc.)
- Timestamped data points
- Unit tracking and notes

### Doctor & Appointment
- Doctor information and specializations
- Appointment scheduling and status tracking

### MentalHealthEntry
- Mood, anxiety, stress, and sleep quality tracking
- 1-10 scale measurements

### Notification
- In-app notification system
- Different notification types

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Users
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/update_profile/` - Update user profile

### Pill Reminders
- `GET /api/pill-reminders/` - List all reminders
- `POST /api/pill-reminders/` - Create new reminder
- `GET /api/pill-reminders/{id}/` - Get specific reminder
- `PUT /api/pill-reminders/{id}/` - Update reminder
- `DELETE /api/pill-reminders/{id}/` - Delete reminder
- `POST /api/pill-reminders/{id}/mark_taken/` - Mark pill as taken
- `GET /api/pill-reminders/adherence_stats/` - Get adherence statistics

### Health Data
- `GET /api/health-data/` - List health data
- `POST /api/health-data/` - Add health data
- `GET /api/health-data/latest/` - Get latest data by type
- `GET /api/health-data/trends/` - Get data trends

### Doctors
- `GET /api/doctors/` - List doctors
- `POST /api/doctors/` - Add doctor

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Create appointment
- `GET /api/appointments/upcoming/` - Get upcoming appointments

### Mental Health
- `GET /api/mental-health/` - List mental health entries
- `POST /api/mental-health/` - Add mental health entry
- `GET /api/mental-health/trends/` - Get mental health trends

### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/unread/` - Get unread notifications
- `POST /api/notifications/{id}/mark_read/` - Mark as read

### Dashboard
- `GET /api/dashboard/` - Get dashboard statistics

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API is available at:
- **Base URL**: `http://localhost:8000/api/`
- **Admin Interface**: `http://localhost:8000/admin/`

## Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Token <your-token-here>
```

## Example Usage

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Add a pill reminder
```bash
curl -X POST http://localhost:8000/api/pill-reminders/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin",
    "dosage": "100mg",
    "frequency": "daily",
    "times": ["08:00", "20:00"],
    "stock": 30,
    "notes": "Take with food"
  }'
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations health_api
```

### Applying Migrations
```bash
python manage.py migrate
```

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure CORS settings for your domain
5. Use environment variables for sensitive settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
