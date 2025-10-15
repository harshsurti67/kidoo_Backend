from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import HomeSlider
import os
import tempfile


class Command(BaseCommand):
    help = 'Test video validation for HomeSlider model'

    def handle(self, *args, **options):
        self.stdout.write('Testing video validation...')
        
        # Test 1: Valid video file (if we had one)
        self.stdout.write('Test 1: Video validation structure')
        
        # Test 2: File size validation
        self.stdout.write('Test 2: File size validation')
        large_file = SimpleUploadedFile(
            "large_video.mp4",
            b"x" * (51 * 1024 * 1024),  # 51MB file
            content_type="video/mp4"
        )
        
        try:
            slider = HomeSlider(
                title="Test Large Video",
                subtitle="Testing file size validation",
                media_type="video",
                video=large_file
            )
            slider.full_clean()
            self.stdout.write(self.style.ERROR('❌ File size validation failed - large file was accepted'))
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f'✅ File size validation working: {str(e)}'))
        
        # Test 3: File extension validation
        self.stdout.write('Test 3: File extension validation')
        invalid_file = SimpleUploadedFile(
            "invalid_video.txt",
            b"not a video",
            content_type="text/plain"
        )
        
        try:
            slider = HomeSlider(
                title="Test Invalid Format",
                subtitle="Testing file format validation",
                media_type="video",
                video=invalid_file
            )
            slider.full_clean()
            self.stdout.write(self.style.ERROR('❌ File format validation failed - invalid format was accepted'))
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f'✅ File format validation working: {str(e)}'))
        
        self.stdout.write('Video validation tests completed!')
