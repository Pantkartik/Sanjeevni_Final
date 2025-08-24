#!/usr/bin/env python3
"""
Database Setup Script for Sanjeevni Health Application

This script helps set up the PostgreSQL database for the Django backend.
Run this script after installing PostgreSQL and creating the database.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        return False

def create_database_and_user():
    """Create database and user for the application"""
    print("\n🔧 Setting up database and user...")
    
    # Database configuration
    db_name = "sanjeevni_db"
    db_user = "sanjeevni_user"
    db_password = "sanjeevni_password"
    
    try:
        # Create user
        create_user_cmd = [
            'psql', '-U', 'postgres', '-c',
            f"CREATE USER {db_user} WITH PASSWORD '{db_password}';"
        ]
        
        print(f"Creating user {db_user}...")
        result = subprocess.run(create_user_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ User {db_user} created successfully")
        else:
            if "already exists" in result.stderr:
                print(f"ℹ️  User {db_user} already exists")
            else:
                print(f"❌ Failed to create user: {result.stderr}")
                return False
        
        # Create database
        create_db_cmd = [
            'psql', '-U', 'postgres', '-c',
            f"CREATE DATABASE {db_name} OWNER {db_user};"
        ]
        
        print(f"Creating database {db_name}...")
        result = subprocess.run(create_db_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Database {db_name} created successfully")
        else:
            if "already exists" in result.stderr:
                print(f"ℹ️  Database {db_name} already exists")
            else:
                print(f"❌ Failed to create database: {result.stderr}")
                return False
        
        # Grant privileges
        grant_cmd = [
            'psql', '-U', 'postgres', '-c',
            f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
        ]
        
        print(f"Granting privileges to {db_user}...")
        result = subprocess.run(grant_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Privileges granted successfully")
        else:
            print(f"❌ Failed to grant privileges: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during database setup: {str(e)}")
        return False

def update_environment_file():
    """Update the environment file with database configuration"""
    print("\n📝 Updating environment configuration...")
    
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    # Read the example file
    with open(env_example, 'r') as f:
        content = f.read()
    
    # Update database settings
    db_settings = """# Database Configuration
DATABASE_URL=postgresql://sanjeevni_user:sanjeevni_password@localhost:5432/sanjeevni_db
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sanjeevni_db
DB_USER=sanjeevni_user
DB_PASSWORD=sanjeevni_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=django-insecure-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:3000,https://sanjeevni-b96da.web.app
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
"""
    
    # Replace the database section
    if 'DATABASE_URL=' in content:
        # Find and replace the database section
        lines = content.split('\n')
        new_lines = []
        skip_db_section = False
        
        for line in lines:
            if line.startswith('# Database Configuration'):
                skip_db_section = True
                new_lines.append(db_settings)
                continue
            elif skip_db_section and (line.startswith('#') or line.startswith('DATABASE_') or line.startswith('DB_')):
                continue
            elif skip_db_section and line.strip() == '':
                skip_db_section = False
                new_lines.append(line)
            elif not skip_db_section:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
    else:
        # Add database section at the end
        content += '\n' + db_settings
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ Environment file updated successfully")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {str(e)}")
        return False

def run_migrations():
    """Run Django migrations"""
    print("\n🔄 Running Django migrations...")
    
    try:
        # Make migrations
        result = subprocess.run([sys.executable, 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations created successfully")
        else:
            print(f"❌ Failed to create migrations: {result.stderr}")
            return False
        
        # Run migrations
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
            return True
        else:
            print(f"❌ Failed to apply migrations: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running migrations: {str(e)}")
        return False

def create_superuser():
    """Create a superuser account"""
    print("\n👤 Creating superuser account...")
    
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], 
                              input='admin\nadmin@example.com\nadmin123\nadmin123\n', 
                              text=True, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Superuser created successfully")
            print("   Username: admin")
            print("   Email: admin@example.com")
            print("   Password: admin123")
            return True
        else:
            print(f"❌ Failed to create superuser: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating superuser: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 Sanjeevni Health Application Database Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the backend directory")
        return
    
    # Check PostgreSQL installation
    if not check_postgresql_installed():
        print("\n📖 Please install PostgreSQL first:")
        print("   - Windows: Download from https://www.postgresql.org/download/windows/")
        print("   - macOS: brew install postgresql")
        print("   - Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        return
    
    # Create database and user
    if not create_database_and_user():
        print("\n❌ Database setup failed. Please check the errors above.")
        return
    
    # Update environment file
    if not update_environment_file():
        print("\n❌ Environment file update failed.")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed.")
        return
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Migration failed.")
        return
    
    # Create superuser
    if not create_superuser():
        print("\n❌ Superuser creation failed.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Start the Django server: python manage.py runserver")
    print("   2. Access the admin interface: http://localhost:8000/admin")
    print("   3. Start Celery worker: celery -A backend worker --loglevel=info")
    print("   4. Start Celery beat: celery -A backend beat --loglevel=info")
    print("\n🔑 Default admin credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Email: admin@example.com")

if __name__ == "__main__":
    main()
