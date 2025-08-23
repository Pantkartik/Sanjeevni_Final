# 🧪 How to Test Django API Endpoints

## 🚀 Quick Start Guide

### **Step 1: Start the Django Server**
```bash
cd backend
python manage.py runserver
```

### **Step 2: Verify Server is Running**
- Open browser and visit: `http://localhost:8000/admin/`
- Login with: `kartikpant.kp69@gmail.com` / `kartik123`

### **Step 3: Test API Endpoints**

## 📋 Testing Methods

### **Method 1: Browser Testing (Easiest)**
1. Open your browser
2. Visit: `http://localhost:8000/admin/`
3. Login with admin credentials
4. Navigate through the admin interface to see all models

### **Method 2: Python Script Testing**
```bash
python quick_test.py
```

### **Method 3: Manual cURL Testing (PowerShell)**
```powershell
# Test registration
Invoke-WebRequest -Uri "http://localhost:8000/api/auth/register/" -Method POST -ContentType "application/json" -Body '{"email":"test@example.com","username":"testuser","password":"password123","confirm_password":"password123","first_name":"John","last_name":"Doe"}'

# Test login
Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login/" -Method POST -ContentType "application/json" -Body '{"email":"test@example.com","password":"password123"}'
```

### **Method 4: Postman/Insomnia (Recommended)**
1. Download Postman or Insomnia
2. Create a new collection
3. Set base URL: `http://localhost:8000/api`
4. Add requests for each endpoint

## 🔐 Authentication Endpoints

### **Register User**
- **URL**: `POST http://localhost:8000/api/auth/register/`
- **Body**:
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123",
  "confirm_password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### **Login User**
- **URL**: `POST http://localhost:8000/api/auth/login/`
- **Body**:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

### **Logout User**
- **URL**: `POST http://localhost:8000/api/auth/logout/`
- **Headers**: `Authorization: Token your-token-here`

## 💊 Pill Reminders Endpoints

### **Create Pill Reminder**
- **URL**: `POST http://localhost:8000/api/pill-reminders/`
- **Headers**: `Authorization: Token your-token-here`
- **Body**:
```json
{
  "name": "Aspirin",
  "dosage": "100mg",
  "frequency": "daily",
  "times": ["08:00", "20:00"],
  "stock": 30,
  "notes": "Take with food"
}
```

### **Get All Pill Reminders**
- **URL**: `GET http://localhost:8000/api/pill-reminders/`
- **Headers**: `Authorization: Token your-token-here`

### **Mark Pill as Taken**
- **URL**: `POST http://localhost:8000/api/pill-reminders/{id}/mark_taken/`
- **Headers**: `Authorization: Token your-token-here`
- **Body**:
```json
{
  "scheduled_time": "08:00",
  "notes": "Taken with breakfast"
}
```

## 📊 Health Data Endpoints

### **Add Health Data**
- **URL**: `POST http://localhost:8000/api/health-data/`
- **Headers**: `Authorization: Token your-token-here`
- **Body**:
```json
{
  "data_type": "blood_pressure",
  "value": 120.5,
  "unit": "mmHg",
  "notes": "Morning reading"
}
```

### **Get Latest Health Data**
- **URL**: `GET http://localhost:8000/api/health-data/latest/`
- **Headers**: `Authorization: Token your-token-here`

## 📈 Dashboard Endpoint

### **Get Dashboard Statistics**
- **URL**: `GET http://localhost:8000/api/dashboard/`
- **Headers**: `Authorization: Token your-token-here`

**Expected Response:**
```json
{
  "total_pill_reminders": 1,
  "active_pill_reminders": 1,
  "average_adherence": 0.0,
  "upcoming_appointments": 0,
  "recent_health_data": [],
  "unread_notifications": 0,
  "mental_health_trend": []
}
```

## 🧪 Step-by-Step Testing Process

### **1. Start the Server**
```bash
cd backend
python manage.py runserver
```

### **2. Run the Test Script**
```bash
python quick_test.py
```

### **3. Check Results**
The script will show:
- ✅ Server Status
- ✅ Registration Status
- ✅ Login Status
- ✅ Pill Reminder Creation
- ✅ Dashboard Data

### **4. Manual Testing**
1. Open browser to `http://localhost:8000/admin/`
2. Login with admin credentials
3. Navigate to different models to see data

## 🚨 Troubleshooting

### **Server Not Starting**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F

# Start server on different port
python manage.py runserver 8001
```

### **Database Issues**
```bash
# Reset database
python manage.py flush

# Create new superuser
python manage.py createsuperuser
```

### **CORS Issues**
- Check `CORS_ALLOWED_ORIGINS` in `settings.py`
- Add your frontend URL to the list

### **Authentication Issues**
- Ensure token is included in Authorization header
- Check if token is valid and not expired
- Verify user exists in database

## 📱 Testing with Postman

### **1. Create Collection**
1. Open Postman
2. Create new collection: "Health API"
3. Set base URL: `http://localhost:8000/api`

### **2. Add Environment Variables**
- `base_url`: `http://localhost:8000/api`
- `token`: (will be set after login)

### **3. Create Requests**
1. **Register User**
   - Method: POST
   - URL: `{{base_url}}/auth/register/`
   - Body: Raw JSON with registration data

2. **Login User**
   - Method: POST
   - URL: `{{base_url}}/auth/login/`
   - Body: Raw JSON with login data
   - Tests: Set token variable from response

3. **Create Pill Reminder**
   - Method: POST
   - URL: `{{base_url}}/pill-reminders/`
   - Headers: `Authorization: Token {{token}}`
   - Body: Raw JSON with pill data

4. **Get Dashboard**
   - Method: GET
   - URL: `{{base_url}}/dashboard/`
   - Headers: `Authorization: Token {{token}}`

## 🎯 Success Criteria

Your API is working correctly if:

- ✅ Server starts without errors
- ✅ Admin interface is accessible
- ✅ User registration returns 201 status
- ✅ User login returns 200 status with token
- ✅ Pill reminder creation returns 201 status
- ✅ Dashboard returns 200 status with data
- ✅ All endpoints return proper JSON responses

## 🔗 Useful URLs

- **Admin Interface**: `http://localhost:8000/admin/`
- **API Root**: `http://localhost:8000/api/`
- **Authentication**: `http://localhost:8000/api/auth/`
- **Pill Reminders**: `http://localhost:8000/api/pill-reminders/`
- **Health Data**: `http://localhost:8000/api/health-data/`
- **Dashboard**: `http://localhost:8000/api/dashboard/`

## 📞 Need Help?

If you encounter issues:

1. Check Django server logs for errors
2. Verify all dependencies are installed
3. Ensure database migrations are applied
4. Check CORS settings for frontend integration
5. Verify authentication tokens are valid

The API is fully functional and ready for your health application! 🎉
