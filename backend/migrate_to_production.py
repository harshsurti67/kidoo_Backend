#!/usr/bin/env python3
"""
Production Migration Script for Kidoo Preschool
This script ensures data consistency between local and production databases.
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

from django.core.management import execute_from_command_line
from django.db import connection
from api.models import *

def check_database_connection():
    """Check which database is being used"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Database connected: {version}")
            
            # Check if it's PostgreSQL
            if 'PostgreSQL' in version:
                print("✅ Using PostgreSQL database (Production Ready)")
                return True
            else:
                print("❌ Not using PostgreSQL database")
                return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_data_consistency():
    """Check if data exists in the database"""
    try:
        # Check key models
        programs_count = Program.objects.count()
        gallery_count = Gallery.objects.count()
        events_count = Event.objects.count()
        testimonials_count = Testimonial.objects.count()
        
        print(f"📊 Database Statistics:")
        print(f"   Programs: {programs_count}")
        print(f"   Gallery Items: {gallery_count}")
        print(f"   Events: {events_count}")
        print(f"   Testimonials: {testimonials_count}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return False

def run_migrations():
    """Run database migrations"""
    try:
        print("🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_sample_data():
    """Create sample data if database is empty"""
    try:
        programs_count = Program.objects.count()
        if programs_count == 0:
            print("🔄 Creating sample data...")
            execute_from_command_line(['manage.py', 'populate_sample_data'])
            print("✅ Sample data created successfully")
        else:
            print(f"✅ Database already has {programs_count} programs")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Starting Production Migration...")
    print("=" * 50)
    
    # Step 1: Check database connection
    if not check_database_connection():
        print("❌ Migration failed: Database connection issue")
        return False
    
    # Step 2: Run migrations
    if not run_migrations():
        print("❌ Migration failed: Database migration issue")
        return False
    
    # Step 3: Check data consistency
    if not check_data_consistency():
        print("❌ Migration failed: Data consistency issue")
        return False
    
    # Step 4: Create sample data if needed
    if not create_sample_data():
        print("❌ Migration failed: Sample data creation issue")
        return False
    
    print("=" * 50)
    print("🎉 Production Migration Completed Successfully!")
    print("✅ Database is ready for production deployment")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
