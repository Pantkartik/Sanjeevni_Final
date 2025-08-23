# Django API Testing Guide

## 🚀 Quick Start

The Django server is running at: `http://localhost:8000/`

## 📋 Testing Methods

### 1. **Browser Testing** (Simple)
- Open browser and visit: `http://localhost:8000/admin/`
- Login with: `kartikpant.kp69@gmail.com` / `kartik123`

### 2. **cURL Testing** (Command Line)
- Use PowerShell or Command Prompt
- Test all endpoints with cURL commands

### 3. **Postman/Insomnia** (GUI)
- Import the endpoints and test visually

## 🔐 Authentication Endpoints

### **1. Register New User**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "gender": "male"
  }'
```

**Expected Response:**
```json
{
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "gender": "male"
  },
  "token": "your-auth-token-here",
  "message": "User registered successfully"
}
```

### **2. Login User**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "username": "testuser"
  },
  "token": "your-auth-token-here",
  "message": "Login successful"
}
```

### **3. Logout User**
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token your-auth-token-here"
```

## 💊 Pill Reminders Endpoints

### **1. Create Pill Reminder**
```bash
curl -X POST http://localhost:8000/api/pill-reminders/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin",
    "dosage": "100mg",
    "frequency": "daily",
    "times": ["08:00", "20:00"],
    "stock": 30,
    "notes": "Take with food",
    "caregiver_notify": false
  }'
```

### **2. Get All Pill Reminders**
```bash
curl -X GET http://localhost:8000/api/pill-reminders/ \
  -H "Authorization: Token your-auth-token-here"
```

### **3. Mark Pill as Taken**
```bash
curl -X POST http://localhost:8000/api/pill-reminders/reminder-id-here/mark_taken/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_time": "08:00",
    "notes": "Taken with breakfast"
  }'
```

### **4. Get Adherence Statistics**
```bash
curl -X GET http://localhost:8000/api/pill-reminders/adherence_stats/ \
  -H "Authorization: Token your-auth-token-here"
```

## 📊 Health Data Endpoints

### **1. Add Health Data**
```bash
curl -X POST http://localhost:8000/api/health-data/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "blood_pressure",
    "value": 120.5,
    "unit": "mmHg",
    "notes": "Morning reading"
  }'
```

### **2. Get Latest Health Data**
```bash
curl -X GET "http://localhost:8000/api/health-data/latest/?types=blood_pressure,heart_rate" \
  -H "Authorization: Token your-auth-token-here"
```

### **3. Get Health Data Trends**
```bash
curl -X GET "http://localhost:8000/api/health-data/trends/?type=blood_pressure&days=7" \
  -H "Authorization: Token your-auth-token-here"
```

## 👨‍⚕️ Doctor Endpoints

### **1. Add Doctor**
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "Cardiology",
    "phone": "+1234567890",
    "email": "dr.smith@hospital.com",
    "address": "123 Medical Center Dr",
    "notes": "Primary cardiologist",
    "is_primary": true
  }'
```

### **2. Get All Doctors**
```bash
curl -X GET http://localhost:8000/api/doctors/ \
  -H "Authorization: Token your-auth-token-here"
```

## 📅 Appointment Endpoints

### **1. Create Appointment**
```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": "doctor-id-here",
    "title": "Annual Checkup",
    "description": "Routine health checkup",
    "appointment_date": "2024-02-15T10:00:00Z",
    "duration": 30,
    "notes": "Bring recent blood work"
  }'
```

### **2. Get Upcoming Appointments**
```bash
curl -X GET http://localhost:8000/api/appointments/upcoming/ \
  -H "Authorization: Token your-auth-token-here"
```

## 🧠 Mental Health Endpoints

### **1. Add Mental Health Entry**
```bash
curl -X POST http://localhost:8000/api/mental-health/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "mood_score": 8,
    "anxiety_level": 3,
    "stress_level": 4,
    "sleep_quality": 7,
    "notes": "Feeling good today"
  }'
```

### **2. Get Mental Health Trends**
```bash
curl -X GET "http://localhost:8000/api/mental-health/trends/?days=7" \
  -H "Authorization: Token your-auth-token-here"
```

## 🔔 Notification Endpoints

### **1. Get Unread Notifications**
```bash
curl -X GET http://localhost:8000/api/notifications/unread/ \
  -H "Authorization: Token your-auth-token-here"
```

### **2. Mark Notification as Read**
```bash
curl -X POST http://localhost:8000/api/notifications/notification-id-here/mark_read/ \
  -H "Authorization: Token your-auth-token-here"
```

## 📈 Dashboard Endpoint

### **Get Dashboard Statistics**
```bash
curl -X GET http://localhost:8000/api/dashboard/ \
  -H "Authorization: Token your-auth-token-here"
```

**Expected Response:**
```json
{
  "total_pill_reminders": 3,
  "active_pill_reminders": 2,
  "average_adherence": 85.5,
  "upcoming_appointments": 1,
  "recent_health_data": [...],
  "unread_notifications": 2,
  "mental_health_trend": [...]
}
```

## 🧪 Testing Script

Create a file called `test_api.py` in the backend directory:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    # Test registration
    print("Testing registration...")
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 201:
        token = response.json()['token']
        print(f"Token: {token}")
        
        # Test pill reminder creation
        headers = {"Authorization": f"Token {token}"}
        pill_data = {
            "name": "Test Pill",
            "dosage": "10mg",
            "frequency": "daily",
            "times": ["08:00"],
            "stock": 30
        }
        
        response = requests.post(f"{BASE_URL}/pill-reminders/", 
                               json=pill_data, headers=headers)
        print(f"Pill Reminder Creation: {response.status_code}")
        
        # Test dashboard
        response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
        print(f"Dashboard: {response.status_code}")
        if response.status_code == 200:
            print(f"Dashboard Data: {response.json()}")

if __name__ == "__main__":
    test_api()
```

## 🚨 Common Issues & Solutions

### **1. CORS Error**
- Make sure Django server is running
- Check CORS settings in `settings.py`

### **2. Authentication Error**
- Ensure token is included in Authorization header
- Check if token is valid and not expired

### **3. 404 Error**
- Verify the endpoint URL is correct
- Check if Django server is running on port 8000

### **4. 500 Error**
- Check Django server logs for detailed error
- Verify request data format is correct

## 📱 Testing with Postman

1. **Import Collection**: Create a new collection in Postman
2. **Set Base URL**: `http://localhost:8000/api`
3. **Add Authorization**: Set Authorization type to "Bearer Token"
4. **Test Endpoints**: Add requests for each endpoint

## 🎯 Quick Test Checklist

- [ ] Django server running on port 8000
- [ ] Admin interface accessible
- [ ] Registration endpoint working
- [ ] Login endpoint working
- [ ] Token authentication working
- [ ] Pill reminders CRUD operations
- [ ] Health data endpoints
- [ ] Dashboard statistics

## 🔗 Useful URLs

- **Admin Interface**: `http://localhost:8000/admin/`
- **API Root**: `http://localhost:8000/api/`
- **Authentication**: `http://localhost:8000/api/auth/`
- **Pill Reminders**: `http://localhost:8000/api/pill-reminders/`
- **Health Data**: `http://localhost:8000/api/health-data/`
- **Dashboard**: `http://localhost:8000/api/dashboard/`
