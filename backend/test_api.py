import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    print(f"\n{'='*50}")
    print(f"📋 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*50}")

def test_api():
    print("🚀 Starting Django API Tests...")
    
    # Test 1: Register a new user
    print("\n1️⃣ Testing User Registration...")
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "gender": "male"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print_response(response, "User Registration")
    
    if response.status_code == 201:
        token = response.json()['token']
        user_id = response.json()['user']['id']
        print(f"✅ Registration successful! Token: {token[:20]}...")
        
        headers = {"Authorization": f"Token {token}"}
        
        # Test 2: Login
        print("\n2️⃣ Testing User Login...")
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print_response(response, "User Login")
        
        # Test 3: Create Pill Reminder
        print("\n3️⃣ Testing Pill Reminder Creation...")
        pill_data = {
            "name": "Aspirin",
            "dosage": "100mg",
            "frequency": "daily",
            "times": ["08:00", "20:00"],
            "stock": 30,
            "notes": "Take with food",
            "caregiver_notify": False
        }
        
        response = requests.post(f"{BASE_URL}/pill-reminders/", 
                               json=pill_data, headers=headers)
        print_response(response, "Pill Reminder Creation")
        
        if response.status_code == 201:
            reminder_id = response.json()['id']
            
            # Test 4: Get All Pill Reminders
            print("\n4️⃣ Testing Get All Pill Reminders...")
            response = requests.get(f"{BASE_URL}/pill-reminders/", headers=headers)
            print_response(response, "Get All Pill Reminders")
            
            # Test 5: Mark Pill as Taken
            print("\n5️⃣ Testing Mark Pill as Taken...")
            mark_taken_data = {
                "scheduled_time": "08:00",
                "notes": "Taken with breakfast"
            }
            
            response = requests.post(f"{BASE_URL}/pill-reminders/{reminder_id}/mark_taken/", 
                                   json=mark_taken_data, headers=headers)
            print_response(response, "Mark Pill as Taken")
            
            # Test 6: Get Adherence Statistics
            print("\n6️⃣ Testing Adherence Statistics...")
            response = requests.get(f"{BASE_URL}/pill-reminders/adherence_stats/", headers=headers)
            print_response(response, "Adherence Statistics")
        
        # Test 7: Add Health Data
        print("\n7️⃣ Testing Health Data Creation...")
        health_data = {
            "data_type": "blood_pressure",
            "value": 120.5,
            "unit": "mmHg",
            "notes": "Morning reading"
        }
        
        response = requests.post(f"{BASE_URL}/health-data/", 
                               json=health_data, headers=headers)
        print_response(response, "Health Data Creation")
        
        # Test 8: Get Latest Health Data
        print("\n8️⃣ Testing Get Latest Health Data...")
        response = requests.get(f"{BASE_URL}/health-data/latest/", headers=headers)
        print_response(response, "Latest Health Data")
        
        # Test 9: Add Doctor
        print("\n9️⃣ Testing Doctor Creation...")
        doctor_data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology",
            "phone": "+1234567890",
            "email": "dr.smith@hospital.com",
            "address": "123 Medical Center Dr",
            "notes": "Primary cardiologist",
            "is_primary": True
        }
        
        response = requests.post(f"{BASE_URL}/doctors/", 
                               json=doctor_data, headers=headers)
        print_response(response, "Doctor Creation")
        
        if response.status_code == 201:
            doctor_id = response.json()['id']
            
            # Test 10: Create Appointment
            print("\n🔟 Testing Appointment Creation...")
            appointment_data = {
                "doctor": doctor_id,
                "title": "Annual Checkup",
                "description": "Routine health checkup",
                "appointment_date": "2024-02-15T10:00:00Z",
                "duration": 30,
                "notes": "Bring recent blood work"
            }
            
            response = requests.post(f"{BASE_URL}/appointments/", 
                                   json=appointment_data, headers=headers)
            print_response(response, "Appointment Creation")
            
            # Test 11: Get Upcoming Appointments
            print("\n1️⃣1️⃣ Testing Get Upcoming Appointments...")
            response = requests.get(f"{BASE_URL}/appointments/upcoming/", headers=headers)
            print_response(response, "Upcoming Appointments")
        
        # Test 12: Add Mental Health Entry
        print("\n1️⃣2️⃣ Testing Mental Health Entry Creation...")
        mental_health_data = {
            "mood_score": 8,
            "anxiety_level": 3,
            "stress_level": 4,
            "sleep_quality": 7,
            "notes": "Feeling good today"
        }
        
        response = requests.post(f"{BASE_URL}/mental-health/", 
                               json=mental_health_data, headers=headers)
        print_response(response, "Mental Health Entry Creation")
        
        # Test 13: Get Mental Health Trends
        print("\n1️⃣3️⃣ Testing Mental Health Trends...")
        response = requests.get(f"{BASE_URL}/mental-health/trends/?days=7", headers=headers)
        print_response(response, "Mental Health Trends")
        
        # Test 14: Get Dashboard Statistics
        print("\n1️⃣4️⃣ Testing Dashboard Statistics...")
        response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
        print_response(response, "Dashboard Statistics")
        
        # Test 15: Logout
        print("\n1️⃣5️⃣ Testing User Logout...")
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print_response(response, "User Logout")
        
        print("\n🎉 All tests completed!")
        
    else:
        print("❌ Registration failed! Check the server logs.")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
