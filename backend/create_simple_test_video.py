#!/usr/bin/env python
"""
Create a simple test video file for testing video upload functionality
"""
import os


def create_simple_test_video():
    print("🎬 Creating simple test video file...")
    
    # Create a simple MP4 file with minimal content
    # This creates a very small, valid MP4 file for testing
    mp4_header = b'\x00\x00\x00\x20ftypmp42\x00\x00\x00\x00mp41mp42isom'
    mp4_data = b'\x00\x00\x00\x08mdat' + b'\x00' * 1000  # Minimal video data
    
    with open('test_video.mp4', 'wb') as f:
        f.write(mp4_header + mp4_data)
    
    file_size = os.path.getsize('test_video.mp4')
    file_size_kb = file_size / 1024
    
    print(f"✅ Simple test video created!")
    print(f"   File: test_video.mp4")
    print(f"   File size: {file_size_kb:.2f} KB")
    print(f"   Note: This is a minimal MP4 file for testing upload functionality")
    
    print("\n📁 You can now use this video file to test the admin upload functionality!")
    print("   Location: backend/test_video.mp4")
    print("\n⚠️  Note: This is a minimal test file. For real testing, use actual video files:")
    print("   - Duration: Maximum 15 seconds")
    print("   - File Size: Maximum 50MB")
    print("   - Format: MP4, MOV, or AVI")


if __name__ == "__main__":
    create_simple_test_video()
