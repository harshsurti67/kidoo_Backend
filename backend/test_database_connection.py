#!/usr/bin/env python3
"""
Database Connection Test Script
Tests the PostgreSQL database connection with your specific credentials.
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
from api.models import Program, Gallery, Event, Testimonial

def test_database_connection():
    """Test database connection and display information"""
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Database Version: {version}")
            
            # Get database info
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✅ Database Name: {db_name}")
            
            cursor.execute("SELECT current_user;")
            db_user = cursor.fetchone()[0]
            print(f"✅ Database User: {db_user}")
            
            cursor.execute("SELECT inet_server_addr();")
            db_host = cursor.fetchone()[0]
            print(f"✅ Database Host: {db_host}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    print("=" * 50)
    print("📊 Database Statistics:")
    
    try:
        # Count records in each table
        programs = Program.objects.count()
        gallery = Gallery.objects.count()
        events = Event.objects.count()
        testimonials = Testimonial.objects.count()
        
        print(f"   📚 Programs: {programs}")
        print(f"   🖼️  Gallery Items: {gallery}")
        print(f"   📅 Events: {events}")
        print(f"   💬 Testimonials: {testimonials}")
        
        # Check for programs with images
        programs_with_images = Program.objects.exclude(image__isnull=True).count()
        programs_without_images = Program.objects.filter(image__isnull=True).count()
        
        print(f"   🖼️  Programs with images: {programs_with_images}")
        print(f"   ❌ Programs without images: {programs_without_images}")
        
        # Check for gallery items with images
        gallery_with_images = Gallery.objects.exclude(image__isnull=True).count()
        gallery_without_images = Gallery.objects.filter(image__isnull=True).count()
        
        print(f"   🖼️  Gallery with images: {gallery_with_images}")
        print(f"   ❌ Gallery without images: {gallery_without_images}")
        
    except Exception as e:
        print(f"❌ Error counting records: {e}")
        return False
    
    print("=" * 50)
    print("🎉 Database Connection Test Successful!")
    return True

def test_sample_queries():
    """Test some sample queries"""
    print("\n🔍 Testing Sample Queries...")
    print("=" * 50)
    
    try:
        # Test programs query
        programs = Program.objects.all()[:3]
        print(f"✅ Found {len(programs)} programs (showing first 3):")
        for program in programs:
            image_status = "✅ Has image" if program.image else "❌ No image"
            print(f"   - {program.name} ({program.age_group}) - {image_status}")
        
        # Test gallery query
        gallery_items = Gallery.objects.all()[:3]
        print(f"✅ Found {len(gallery_items)} gallery items (showing first 3):")
        for item in gallery_items:
            image_status = "✅ Has image" if item.image else "❌ No image"
            print(f"   - {item.title} ({item.category}) - {image_status}")
            
    except Exception as e:
        print(f"❌ Error testing queries: {e}")
        return False
    
    print("✅ Sample queries successful!")
    return True

if __name__ == '__main__':
    print("🚀 Kidoo Preschool Database Connection Test")
    print("=" * 60)
    
    # Test database connection
    if not test_database_connection():
        print("❌ Database connection test failed!")
        sys.exit(1)
    
    # Test sample queries
    if not test_sample_queries():
        print("❌ Sample queries test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Database is ready for production.")
    sys.exit(0)
