#!/usr/bin/env python3
"""
Data Backup Script for Kidoo Preschool
This script exports all data from the database to JSON files for backup purposes.
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand

def backup_data():
    """Create a backup of all data in the database."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = project_dir / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    print(f"🔄 Creating backup with timestamp: {timestamp}")
    
    # Backup all data
    backup_file = backup_dir / f'full_backup_{timestamp}.json'
    
    try:
        execute_from_command_line([
            'manage.py', 
            'dumpdata', 
            '--natural-foreign', 
            '--natural-primary',
            '--exclude', 'contenttypes',
            '--exclude', 'auth.permission',
            '--exclude', 'admin.logentry',
            '--exclude', 'sessions.session',
            '--output', str(backup_file)
        ])
        print(f"✅ Full backup created: {backup_file}")
        
        # Also create API-specific backup
        api_backup_file = backup_dir / f'api_backup_{timestamp}.json'
        execute_from_command_line([
            'manage.py', 
            'dumpdata', 
            'api',
            '--natural-foreign', 
            '--natural-primary',
            '--output', str(api_backup_file)
        ])
        print(f"✅ API data backup created: {api_backup_file}")
        
        # Create users backup
        users_backup_file = backup_dir / f'users_backup_{timestamp}.json'
        execute_from_command_line([
            'manage.py', 
            'dumpdata', 
            'auth.user',
            '--natural-foreign', 
            '--natural-primary',
            '--output', str(users_backup_file)
        ])
        print(f"✅ Users backup created: {users_backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def restore_data(backup_file):
    """Restore data from a backup file."""
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    try:
        execute_from_command_line([
            'manage.py', 
            'loaddata', 
            backup_file
        ])
        print(f"✅ Data restored from: {backup_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")
        return False

def list_backups():
    """List all available backup files."""
    backup_dir = project_dir / 'backups'
    if not backup_dir.exists():
        print("📁 No backups directory found")
        return
    
    backup_files = list(backup_dir.glob('*.json'))
    if not backup_files:
        print("📁 No backup files found")
        return
    
    print("📁 Available backups:")
    for backup_file in sorted(backup_files, reverse=True):
        size = backup_file.stat().st_size
        modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
        print(f"  📄 {backup_file.name} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'backup':
            backup_data()
        elif command == 'restore' and len(sys.argv) > 2:
            restore_data(sys.argv[2])
        elif command == 'list':
            list_backups()
        else:
            print("Usage:")
            print("  python backup_data.py backup          # Create backup")
            print("  python backup_data.py restore <file>  # Restore from backup")
            print("  python backup_data.py list            # List available backups")
    else:
        print("🔄 Creating automatic backup...")
        backup_data()
