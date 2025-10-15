#!/usr/bin/env python
"""
Test script to check if video URLs are being generated correctly
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')
django.setup()

from api.models import HomeSlider
from api.serializers import HomeSliderSerializer
from django.test import RequestFactory


def test_video_api():
    print("🎬 Testing Video API and URL Generation")
    print("=" * 50)
    
    # Check if there are any HomeSlider objects
    sliders = HomeSlider.objects.all()
    print(f"\n1. Found {sliders.count()} HomeSlider objects")
    
    if sliders.count() == 0:
        print("   ⚠️  No sliders found. Creating a test slider...")
        
        # Create a test slider with video
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        test_video = SimpleUploadedFile(
            "test_video.mp4",
            b"fake video content for testing",
            content_type="video/mp4"
        )
        
        slider = HomeSlider.objects.create(
            title="Test Video Slide",
            subtitle="Testing video display",
            media_type="video",
            video=test_video,
            button_text="Learn More",
            button_url="/programs",
            order=1,
            is_active=True
        )
        print(f"   ✅ Created test slider: {slider.title}")
    else:
        slider = sliders.first()
        print(f"   📋 Using existing slider: {slider.title}")
    
    # Test the model properties
    print(f"\n2. Testing model properties:")
    print(f"   Media Type: {slider.media_type}")
    print(f"   Video File: {slider.video}")
    print(f"   Video URL: {slider.video.url if slider.video else 'None'}")
    print(f"   Media URL: {slider.media_url}")
    print(f"   Poster URL: {slider.poster_url}")
    
    # Test the serializer
    print(f"\n3. Testing serializer:")
    factory = RequestFactory()
    request = factory.get('/api/home-sliders/')
    request.META['HTTP_HOST'] = '127.0.0.1:8000'
    
    serializer = HomeSliderSerializer(slider, context={'request': request})
    serialized_data = serializer.data
    
    print(f"   Serialized data keys: {list(serialized_data.keys())}")
    print(f"   Media Type: {serialized_data.get('media_type')}")
    print(f"   Media URL: {serialized_data.get('media_url')}")
    print(f"   Poster URL: {serialized_data.get('poster_url')}")
    print(f"   Video field: {serialized_data.get('video')}")
    
    # Check if media_url is properly generated
    if serialized_data.get('media_url'):
        print(f"   ✅ Media URL generated: {serialized_data['media_url']}")
    else:
        print(f"   ❌ Media URL not generated")
    
    # Test API endpoint
    print(f"\n4. Testing API endpoint:")
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    try:
        response = client.get('/api/home-sliders/')
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API endpoint accessible")
            print(f"   Response data: {data}")
            
            if 'results' in data and len(data['results']) > 0:
                first_slider = data['results'][0]
                print(f"   First slider media_type: {first_slider.get('media_type')}")
                print(f"   First slider media_url: {first_slider.get('media_url')}")
            else:
                print(f"   ⚠️  No results in API response")
        else:
            print(f"   ❌ API endpoint error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API endpoint error: {e}")
    
    print(f"\n5. Frontend Integration Check:")
    print(f"   The frontend should check:")
    print(f"   - slide.media_type === 'video'")
    print(f"   - slide.media_url exists")
    print(f"   - Use slide.media_url as video source")
    print(f"   - Use slide.poster_url as poster attribute")
    
    return serialized_data


if __name__ == "__main__":
    test_video_api()
