#!/usr/bin/env python3
"""
Database Connection Test Script for KIDOO Django Project

This script tests the database connection to ensure everything is configured correctly.
Run this script to verify your SQL Server connection before running migrations.

Usage:
    python test_db_connection.py
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ImproperlyConfigured
from decouple import config

def test_database_connection():
    """Test the database connection"""
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    try:
        # Get database configuration
        USE_SQLSERVER = config('USE_SQLSERVER', default=False, cast=bool)
        DB_HOST = config('DB_HOST', default='localhost')
        DB_PORT = config('DB_PORT', default='1433')
        DB_NAME = config('DB_NAME', default='KIDOO')
        DB_USER = config('DB_USER', default='')
        
        print(f"Database Type: {'SQL Server' if USE_SQLSERVER else 'SQLite'}")
        
        if USE_SQLSERVER:
            print(f"Host: {DB_HOST}:{DB_PORT}")
            print(f"Database: {DB_NAME}")
            print(f"User: {DB_USER}")
            print(f"Password: {'*' * len(config('DB_PASSWORD', default=''))}")
        
        # Test the connection
        print("\n🔗 Testing connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Database connection successful!")
            
            # Get database info
            if USE_SQLSERVER:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT @@VERSION")
                    version = cursor.fetchone()[0]
                    print(f"📊 SQL Server Version: {version}")
                    
                    cursor.execute("SELECT DB_NAME()")
                    db_name = cursor.fetchone()[0]
                    print(f"📊 Connected to database: {db_name}")
            else:
                print("📊 Using SQLite database")
                
            return True
            
    except ImproperlyConfigured as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Created a .env file with proper database settings")
        print("   2. Installed required packages: pip install -r requirements.txt")
        print("   3. Set USE_SQLSERVER=True in your .env file for SQL Server")
        return False
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        
        if USE_SQLSERVER:
            print("\n💡 Common SQL Server connection issues:")
            print("   1. Make sure SQL Server is running")
            print("   2. Check if the database 'KIDOO' exists")
            print("   3. Verify username and password are correct")
            print("   4. Ensure SQL Server allows SQL Server authentication")
            print("   5. Check if the port 1433 is accessible")
            print("   6. Install ODBC Driver 17 for SQL Server")
        else:
            print("\n💡 Make sure SQLite database file is accessible")
            
        return False

def test_django_setup():
    """Test if Django is properly configured"""
    print("🐍 Testing Django Setup...")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django Setup Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 KIDOO Database Connection Test")
    print("=" * 50)
    
    # Test Django setup first
    if not test_django_setup():
        print("\n❌ Django setup failed. Please check your configuration.")
        sys.exit(1)
    
    print()
    
    # Test database connection
    if test_database_connection():
        print("\n🎉 All tests passed! Your database is ready.")
        print("\n📋 Next steps:")
        print("   1. Run migrations: python manage.py migrate")
        print("   2. Create superuser: python manage.py createsuperuser")
        print("   3. Start the server: python manage.py runserver")
        sys.exit(0)
    else:
        print("\n❌ Database connection failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
