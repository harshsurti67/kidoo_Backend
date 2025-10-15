#!/usr/bin/env python3
"""
Script to populate the Kidoo Preschool database with sample data
Run this script from the project root directory
"""

import os
import sys
import subprocess

def main():
    print("🎨 Populating Kidoo Preschool Database with Sample Data")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("backend"):
        print("❌ Please run this script from the project root directory")
        print("   The script expects a 'backend' directory to exist")
        return False
    
    # Navigate to backend directory
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    # Check if virtual environment exists
    venv_path = os.path.join(backend_dir, "venv")
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found!")
        print("   Please run 'python setup.py' first to set up the environment")
        return False
    
    # Determine the correct Python executable
    if os.name == 'nt':  # Windows
        python_cmd = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Unix/Linux/Mac
        python_cmd = os.path.join(venv_path, "bin", "python")
    
    if not os.path.exists(python_cmd):
        print("❌ Python executable not found in virtual environment")
        return False
    
    # Run the Django management command
    print("🚀 Running Django management command...")
    try:
        result = subprocess.run([
            python_cmd, 
            "manage.py", 
            "populate_sample_data"
        ], cwd=backend_dir, check=True, capture_output=True, text=True)
        
        print("✅ Sample data populated successfully!")
        print("\n📊 Data created:")
        print("   • 5 Programs")
        print("   • 8 Gallery items")
        print("   • 5 Testimonials")
        print("   • 5 Events")
        print("   • 4 Branches")
        print("   • 3 Blog posts")
        print("   • 6 Team members")
        print("   • 10 FAQs")
        print("   • 8 Settings")
        
        print("\n🎉 You can now:")
        print("   1. Start the backend server: cd backend && python manage.py runserver")
        print("   2. Start the frontend server: cd frontend && npm start")
        print("   3. Visit http://localhost:3000 to see the website with sample data")
        print("   4. Visit http://localhost:8000/admin to manage the data")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running management command: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
