#!/usr/bin/env python3
"""
Setup script for Kidoo Preschool website
This script helps set up the development environment
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_backend():
    """Set up the Django backend"""
    print("🚀 Setting up Django backend...")
    
    # Check if Python is available
    success, output = run_command("python --version")
    if not success:
        print("❌ Python is not installed or not in PATH")
        return False
    
    print(f"✅ Python version: {output.strip()}")
    
    # Navigate to backend directory
    backend_dir = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    venv_path = os.path.join(backend_dir, "venv")
    if not os.path.exists(venv_path):
        success, output = run_command("python -m venv venv", cwd=backend_dir)
        if not success:
            print(f"❌ Failed to create virtual environment: {output}")
            return False
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("📦 Installing Python dependencies...")
    success, output = run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir)
    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False
    print("✅ Dependencies installed")
    
    # Create .env file if it doesn't exist
    env_file = os.path.join(backend_dir, ".env")
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("SECRET_KEY=django-insecure-change-this-in-production\n")
            f.write("DEBUG=True\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
            f.write("\n# Database Configuration\n")
            f.write("# Set USE_SQLSERVER=True to use SQL Server, False to use SQLite\n")
            f.write("USE_SQLSERVER=False\n")
            f.write("\n# SQL Server Database Settings (only used when USE_SQLSERVER=True)\n")
            f.write("DB_HOST=localhost\n")
            f.write("DB_PORT=1433\n")
            f.write("DB_NAME=KIDOO\n")
            f.write("DB_USER=your_sqlserver_username\n")
            f.write("DB_PASSWORD=your_sqlserver_password\n")
        print("✅ .env file created")
    
    # Test database connection
    print("🔍 Testing database connection...")
    success, output = run_command(f"{pip_cmd} run python test_db_connection.py", cwd=backend_dir)
    if not success:
        print(f"⚠️ Database connection test failed: {output}")
        print("💡 You can still proceed, but make sure to configure your database settings in .env")
        print("💡 Run 'python test_db_connection.py' manually to troubleshoot")
    else:
        print("✅ Database connection test passed")
    
    # Run migrations
    print("🗄️ Running database migrations...")
    success, output = run_command(f"{pip_cmd} run manage.py makemigrations", cwd=backend_dir)
    if not success:
        print(f"❌ Failed to make migrations: {output}")
        return False
    
    success, output = run_command(f"{pip_cmd} run manage.py migrate", cwd=backend_dir)
    if not success:
        print(f"❌ Failed to run migrations: {output}")
        return False
    print("✅ Database migrations completed")
    
    print("✅ Backend setup completed!")
    return True

def setup_frontend():
    """Set up the React frontend"""
    print("🚀 Setting up React frontend...")
    
    # Check if Node.js is available
    success, output = run_command("node --version")
    if not success:
        print("❌ Node.js is not installed or not in PATH")
        return False
    
    print(f"✅ Node.js version: {output.strip()}")
    
    # Check if npm is available
    success, output = run_command("npm --version")
    if not success:
        print("❌ npm is not installed or not in PATH")
        return False
    
    print(f"✅ npm version: {output.strip()}")
    
    # Navigate to frontend directory
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    print("📦 Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False
    print("✅ Dependencies installed")
    
    # Create .env file if it doesn't exist
    env_file = os.path.join(frontend_dir, ".env")
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("REACT_APP_API_URL=http://localhost:8000/api\n")
        print("✅ .env file created")
    
    print("✅ Frontend setup completed!")
    return True

def main():
    """Main setup function"""
    print("🎨 Kidoo Preschool Website Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Please run this script from the project root directory")
        print("   The script expects 'backend' and 'frontend' directories to exist")
        return False
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return False
    
    print()
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        return False
    
    print()
    print("🎉 Setup completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python manage.py runserver")
    print()
    print("2. Start the frontend server (in a new terminal):")
    print("   cd frontend")
    print("   npm start")
    print()
    print("3. Visit http://localhost:3000 to see the website")
    print("4. Visit http://localhost:8000/admin to access the admin panel")
    print()
    print("📚 For more information, see the README.md file")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
