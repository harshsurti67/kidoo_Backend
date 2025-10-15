#!/usr/bin/env python3
"""
Data Migration Script: SQLite to SQL Server
This script migrates data from SQLite to SQL Server for the KIDOO project
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

from django.db import connections
from django.core import serializers
from django.contrib.auth.models import User
from api.models import *

def get_sqlite_data():
    """Get data from SQLite database"""
    print("📥 Reading data from SQLite database...")
    
    # Connect to SQLite database
    sqlite_conn = connections['sqlite']
    
    # List of models to migrate
    models_to_migrate = [
        User,
        Blog,
        Branch,
        Event,
        FAQ,
        Gallery,
        Program,
        Setting,
        TeamMember,
        Testimonial,
        Inquiry,
        AboutFeature,
        AboutPage,
        HomeSlider,
        HomeStats,
        Admission,
    ]
    
    data = {}
    
    for model in models_to_migrate:
        try:
            model_name = model.__name__
            print(f"  📋 Reading {model_name}...")
            
            # Get all objects from the model
            objects = model.objects.using('sqlite').all()
            data[model_name] = list(objects)
            
            print(f"  ✅ Found {len(data[model_name])} {model_name} records")
            
        except Exception as e:
            print(f"  ❌ Error reading {model_name}: {e}")
    
    return data

def migrate_to_sqlserver(data):
    """Migrate data to SQL Server"""
    print("\n📤 Migrating data to SQL Server...")
    
    for model_name, objects in data.items():
        if not objects:
            continue
            
        print(f"\n📋 Migrating {model_name}...")
        
        try:
            # Get the model class
            model_class = globals()[model_name]
            
            # Clear existing data in SQL Server
            model_class.objects.using('default').all().delete()
            print(f"  🗑️ Cleared existing {model_name} data")
            
            # Migrate each object
            migrated_count = 0
            for obj in objects:
                try:
                    # Save to SQL Server database
                    obj.save(using='default')
                    migrated_count += 1
                except Exception as e:
                    print(f"  ⚠️ Error migrating {model_name} object: {e}")
            
            print(f"  ✅ Migrated {migrated_count} {model_name} records")
            
        except Exception as e:
            print(f"  ❌ Error migrating {model_name}: {e}")

def main():
    """Main migration function"""
    print("🔄 KIDOO Data Migration: SQLite → SQL Server")
    print("=" * 50)
    
    try:
        # Read data from SQLite
        data = get_sqlite_data()
        
        # Check if we have any data
        total_records = sum(len(objects) for objects in data.values())
        if total_records == 0:
            print("\n❌ No data found in SQLite database.")
            return
        
        print(f"\n📊 Total records found: {total_records}")
        
        # Ask for confirmation
        response = input("\n🤔 Do you want to migrate this data to SQL Server? (y/N): ")
        if response.lower() != 'y':
            print("❌ Migration cancelled.")
            return
        
        # Migrate data
        migrate_to_sqlserver(data)
        
        print("\n🎉 Data migration completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Check your admin panel: http://localhost:8000/admin")
        print("   2. Verify all data is present")
        print("   3. Your SQL Server database now contains all your data!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    main()
