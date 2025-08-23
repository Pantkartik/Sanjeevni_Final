import requests
import json

def test_api_endpoint():
    """Test if the Django API endpoint is responding correctly"""
    
    # Test the API root endpoint
    try:
        response = requests.get('http://localhost:8000/api/')
        print(f"API Root Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ API root endpoint is working!")
            try:
                data = response.json()
                print(f"Response Data: {data}")
            except json.JSONDecodeError:
                print("⚠️ Response is not JSON (this might be expected)")
                print(f"Response Text: {response.text[:200]}...")
        else:
            print(f"❌ API root returned status {response.status_code}")
            print(f"Response Text: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

    # Test the auth register endpoint
    try:
        test_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\nAuth Register Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code in [201, 400]:  # 201 for success, 400 for validation error
            print("✅ Auth register endpoint is responding!")
            try:
                data = response.json()
                print(f"Response Data: {data}")
            except json.JSONDecodeError:
                print("⚠️ Response is not JSON")
                print(f"Response Text: {response.text[:200]}...")
        else:
            print(f"❌ Auth register returned unexpected status {response.status_code}")
            print(f"Response Text: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server for auth test")
    except Exception as e:
        print(f"❌ Error testing auth endpoint: {e}")

if __name__ == "__main__":
    print("🧪 Testing Django API Endpoints...")
    print("=" * 50)
    test_api_endpoint()
    print("=" * 50)
    print("Test completed!")
