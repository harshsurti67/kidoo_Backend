#!/usr/bin/env python
"""
Create a test video file for testing video upload functionality
"""
import cv2
import numpy as np
import os


def create_test_video():
    print("🎬 Creating test video file...")
    
    # Video properties
    width, height = 1920, 1080
    fps = 30
    duration = 10  # 10 seconds (under 15 second limit)
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_video.mp4', fourcc, fps, (width, height))
    
    print(f"Creating {duration}-second video ({total_frames} frames)...")
    
    for frame_num in range(total_frames):
        # Create a colorful gradient background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create animated gradient
        for y in range(height):
            for x in range(width):
                # Animated color based on frame number
                r = int(255 * (x / width) * (1 + 0.5 * np.sin(frame_num * 0.1)))
                g = int(255 * (y / height) * (1 + 0.5 * np.cos(frame_num * 0.1)))
                b = int(255 * ((x + y) / (width + height)) * (1 + 0.5 * np.sin(frame_num * 0.05)))
                
                frame[y, x] = [min(255, b), min(255, g), min(255, r)]
        
        # Add text overlay
        text = f"Kiddoo Preschool - Frame {frame_num + 1}/{total_frames}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        color = (255, 255, 255)
        thickness = 3
        
        # Get text size for centering
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        x = (width - text_width) // 2
        y = (height + text_height) // 2
        
        # Add text with shadow
        cv2.putText(frame, text, (x + 2, y + 2), font, font_scale, (0, 0, 0), thickness + 2)
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        
        # Add progress bar
        progress = (frame_num + 1) / total_frames
        bar_width = int(width * 0.6)
        bar_height = 20
        bar_x = (width - bar_width) // 2
        bar_y = height - 100
        
        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
        # Progress bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
        
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:  # Print progress every second
            print(f"Progress: {frame_num + 1}/{total_frames} frames ({progress*100:.1f}%)")
    
    out.release()
    cv2.destroyAllWindows()
    
    # Check file size
    file_size = os.path.getsize('test_video.mp4')
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✅ Test video created successfully!")
    print(f"   File: test_video.mp4")
    print(f"   Duration: {duration} seconds")
    print(f"   Resolution: {width}x{height}")
    print(f"   File size: {file_size_mb:.2f} MB")
    print(f"   FPS: {fps}")
    
    if file_size_mb > 50:
        print("⚠️  Warning: File size exceeds 50MB limit")
    else:
        print("✅ File size is within 50MB limit")
    
    print("\n📁 You can now use this video file to test the admin upload functionality!")
    print("   Location: backend/test_video.mp4")


if __name__ == "__main__":
    try:
        create_test_video()
    except ImportError:
        print("❌ OpenCV not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
        print("✅ OpenCV installed. Please run the script again.")
    except Exception as e:
        print(f"❌ Error creating test video: {e}")
        print("Make sure OpenCV is installed: pip install opencv-python")
