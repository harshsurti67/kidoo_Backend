#!/usr/bin/env python
"""
Setup script to create admin user and start server for testing
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command


def setup_admin_user():
    print("🔧 Setting up admin user for testing...")
    
    # Check if admin user already exists
    if User.objects.filter(username='admin').exists():
        print("✅ Admin user already exists")
        admin_user = User.objects.get(username='admin')
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Is superuser: {admin_user.is_superuser}")
    else:
        print("👤 Creating admin user...")
        try:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@kiddoo.com',
                password='admin123'
            )
            print("✅ Admin user created successfully!")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Password: admin123")
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return False
    
    print("\n🌐 Admin Panel Access Information:")
    print("=" * 40)
    print("URL: http://127.0.0.1:8000/admin/")
    print("Username: admin")
    print("Password: admin123")
    print("=" * 40)
    
    print("\n📋 Testing Steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Open browser and go to: http://127.0.0.1:8000/admin/")
    print("3. Login with the credentials above")
    print("4. Navigate to 'Home Sliders' section")
    print("5. Click 'Add Home Slider'")
    print("6. Fill in the form:")
    print("   - Title: Test Video Slide")
    print("   - Subtitle: Testing video upload")
    print("   - Media Type: Video")
    print("   - Video: Upload a video file (max 15 seconds, max 50MB)")
    print("   - Video Poster: Optional poster image")
    print("   - Button Text: Learn More")
    print("   - Button URL: /programs")
    print("   - Order: 1")
    print("   - Is Active: ✓")
    print("7. Click 'Save'")
    
    print("\n🎬 Video Requirements:")
    print("- Duration: Maximum 15 seconds")
    print("- File Size: Maximum 50MB")
    print("- Format: MP4, MOV, or AVI")
    print("- Upload: Direct file upload (not URL)")
    
    return True


if __name__ == "__main__":
    setup_admin_user()
