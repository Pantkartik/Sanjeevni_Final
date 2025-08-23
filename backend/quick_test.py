import requests
import json

def test_basic_endpoints():
    print("🧪 Testing Django API Endpoints...")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    # Test 2: Register a new user
    print("\n📝 Testing User Registration...")
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register/", json=register_data)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            token = data.get('token')
            print(f"✅ Registration successful!")
            print(f"Token: {token[:20]}..." if token else "No token received")
            
            # Test 3: Login
            print("\n🔐 Testing User Login...")
            login_data = {
                "email": "test@example.com",
                "password": "password123"
            }
            
            response = requests.post(f"{base_url}/auth/login/", json=login_data)
            print(f"Login Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Login successful!")
                
                # Test 4: Create a pill reminder
                print("\n💊 Testing Pill Reminder Creation...")
                headers = {"Authorization": f"Token {token}"}
                pill_data = {
                    "name": "Test Pill",
                    "dosage": "10mg",
                    "frequency": "daily",
                    "times": ["08:00"],
                    "stock": 30
                }
                
                response = requests.post(f"{base_url}/pill-reminders/", 
                                       json=pill_data, headers=headers)
                print(f"Pill Reminder Status: {response.status_code}")
                
                if response.status_code == 201:
                    print("✅ Pill reminder created successfully!")
                    
                    # Test 5: Get dashboard
                    print("\n📊 Testing Dashboard...")
                    response = requests.get(f"{base_url}/dashboard/", headers=headers)
                    print(f"Dashboard Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        print("✅ Dashboard data retrieved!")
                        print(f"Total reminders: {data.get('total_pill_reminders', 0)}")
                        print(f"Active reminders: {data.get('active_pill_reminders', 0)}")
                        print(f"Average adherence: {data.get('average_adherence', 0)}%")
                    else:
                        print(f"❌ Dashboard failed: {response.text}")
                else:
                    print(f"❌ Pill reminder creation failed: {response.text}")
            else:
                print(f"❌ Login failed: {response.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    test_basic_endpoints()
