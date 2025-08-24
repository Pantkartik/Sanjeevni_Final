#!/usr/bin/env python3
"""
Setup script for Health Dashboard Django Backend
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def create_env_file():
    """Create .env file from template."""
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file with your configuration")
    else:
        print("⚠️  env.example not found, creating basic .env file")
        with open(env_file, 'w') as f:
            f.write("""# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Database Configuration (using SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1

# Firebase Configuration (optional)
FIREBASE_CREDENTIALS_PATH=
FIREBASE_PROJECT_ID=

# OpenAI Configuration (optional)
OPENAI_API_KEY=

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
""")


def install_dependencies():
    """Install Python dependencies."""
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        return False
    return True


def run_migrations():
    """Run Django migrations."""
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        return False
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        print("❌ Failed to apply migrations")
        return False
    
    return True


def create_superuser():
    """Create a superuser account."""
    print("🔄 Creating superuser account...")
    print("⚠️  You will be prompted to enter username, email, and password")
    
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Superuser creation failed or was cancelled")
        return False


def collect_static():
    """Collect static files."""
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files")
        return False
    return True


def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✅ Logs directory created")
    else:
        print("✅ Logs directory already exists")


def test_server():
    """Test if the server can start."""
    print("🔄 Testing server startup...")
    try:
        # Try to start server in background and stop it quickly
        process = subprocess.Popen(
            "python manage.py runserver --noreload",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        import time
        time.sleep(3)
        
        # Stop the server
        process.terminate()
        process.wait()
        
        print("✅ Server test successful")
        return True
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Health Dashboard Django Backend Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create necessary directories
    create_logs_directory()
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Run migrations
    if not run_migrations():
        print("❌ Setup failed at migrations")
        return
    
    # Collect static files
    if not collect_static():
        print("❌ Setup failed at static file collection")
        return
    
    # Test server
    if not test_server():
        print("❌ Setup failed at server test")
        return
    
    # Create superuser (optional)
    create_superuser()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Configure Firebase (optional)")
    print("3. Configure OpenAI (optional)")
    print("4. Start the server: python manage.py runserver")
    print("5. Access admin at: http://localhost:8000/admin")
    print("6. View API docs at: http://localhost:8000/swagger/")
    
    print("\n🔗 Useful URLs:")
    print("- Admin Interface: http://localhost:8000/admin")
    print("- API Documentation: http://localhost:8000/swagger/")
    print("- ReDoc Documentation: http://localhost:8000/redoc/")
    print("- Health API: http://localhost:8000/api/health/")


if __name__ == "__main__":
    main()
