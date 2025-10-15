#!/usr/bin/env python
"""
Test script to verify video upload functionality in admin interface
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import HomeSlider
from django.core.exceptions import ValidationError


def test_video_upload_functionality():
    print("🎬 Testing Video Upload Functionality in Admin")
    print("=" * 50)
    
    # Test 1: Check if HomeSlider model has video field
    print("\n1. Checking HomeSlider model fields...")
    slider_fields = [field.name for field in HomeSlider._meta.fields]
    required_fields = ['media_type', 'video', 'video_poster']
    
    for field in required_fields:
        if field in slider_fields:
            print(f"   ✅ {field} field exists")
        else:
            print(f"   ❌ {field} field missing")
    
    # Test 2: Test video validation
    print("\n2. Testing video validation...")
    
    # Test valid video file (small MP4)
    valid_video = SimpleUploadedFile(
        "test_video.mp4",
        b"fake video content" * 1000,  # Small file
        content_type="video/mp4"
    )
    
    try:
        slider = HomeSlider(
            title="Test Video Slide",
            subtitle="Testing video upload",
            media_type="video",
            video=valid_video
        )
        slider.full_clean()
        print("   ✅ Valid video file accepted")
    except ValidationError as e:
        print(f"   ⚠️  Valid video validation error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Test 3: Test file size validation
    print("\n3. Testing file size validation...")
    large_video = SimpleUploadedFile(
        "large_video.mp4",
        b"x" * (51 * 1024 * 1024),  # 51MB
        content_type="video/mp4"
    )
    
    try:
        slider = HomeSlider(
            title="Test Large Video",
            subtitle="Testing file size",
            media_type="video",
            video=large_video
        )
        slider.full_clean()
        print("   ❌ Large file was accepted (should be rejected)")
    except ValidationError as e:
        if "50MB" in str(e):
            print("   ✅ File size validation working correctly")
        else:
            print(f"   ⚠️  Different validation error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Test 4: Test file format validation
    print("\n4. Testing file format validation...")
    invalid_video = SimpleUploadedFile(
        "invalid.txt",
        b"not a video",
        content_type="text/plain"
    )
    
    try:
        slider = HomeSlider(
            title="Test Invalid Format",
            subtitle="Testing format validation",
            media_type="video",
            video=invalid_video
        )
        slider.full_clean()
        print("   ❌ Invalid format was accepted (should be rejected)")
    except ValidationError as e:
        if "extension" in str(e).lower():
            print("   ✅ File format validation working correctly")
        else:
            print(f"   ⚠️  Different validation error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Test 5: Check admin configuration
    print("\n5. Checking admin configuration...")
    from django.contrib import admin
    from api.admin import HomeSliderAdmin
    
    if HomeSlider in admin.site._registry:
        admin_config = admin.site._registry[HomeSlider]
        if isinstance(admin_config, HomeSliderAdmin):
            print("   ✅ HomeSlider is properly registered in admin")
            print(f"   ✅ Admin class: {admin_config.__class__.__name__}")
            
            # Check if video field is in fieldsets
            fieldsets = admin_config.fieldsets
            video_in_fieldsets = False
            for section_name, section_data in fieldsets:
                if 'video' in section_data.get('fields', []):
                    video_in_fieldsets = True
                    print(f"   ✅ Video field found in '{section_name}' section")
                    break
            
            if not video_in_fieldsets:
                print("   ❌ Video field not found in admin fieldsets")
        else:
            print("   ❌ HomeSlider admin configuration incorrect")
    else:
        print("   ❌ HomeSlider not registered in admin")
    
    # Test 6: Check media type choices
    print("\n6. Checking media type choices...")
    media_choices = HomeSlider._meta.get_field('media_type').choices
    if ('video', 'Video') in media_choices:
        print("   ✅ Video option available in media_type choices")
    else:
        print("   ❌ Video option missing from media_type choices")
    
    print("\n" + "=" * 50)
    print("🎬 Video Upload Test Complete!")
    print("\nTo test in admin interface:")
    print("1. Start server: python manage.py runserver")
    print("2. Go to: http://127.0.0.1:8000/admin/")
    print("3. Login with admin credentials")
    print("4. Navigate to 'Home Sliders' section")
    print("5. Click 'Add Home Slider'")
    print("6. Select 'Video' as media type")
    print("7. Upload a video file (max 15 seconds, max 50MB, MP4/MOV/AVI)")


if __name__ == "__main__":
    test_video_upload_functionality()
