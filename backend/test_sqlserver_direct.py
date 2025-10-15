#!/usr/bin/env python3
"""
Direct SQL Server connection test using pyodbc
"""

import pyodbc

def test_sqlserver_connection():
    """Test SQL Server connection directly with pyodbc"""
    print("🔍 Testing SQL Server Connection Directly...")
    print("=" * 50)
    
    # Test different server name formats
    server_formats = [
        ".\\SQLEXPRESS",
        "localhost\\SQLEXPRESS", 
        "localhost",
        "(local)\\SQLEXPRESS",
        ".\\SQLEXPRESS,1433"
    ]
    
    for server in server_formats:
        print(f"\n🔗 Trying server: {server}")
        
        try:
            # Test connection with Windows Authentication first
            conn_str = f"DRIVER={{SQL Server}};SERVER={server};Trusted_Connection=yes;"
            print(f"Connection string: {conn_str}")
            
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Get server info
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"📊 SQL Server Version: {version}")
            
            # List databases
            cursor.execute("SELECT name FROM sys.databases")
            databases = cursor.fetchall()
            print("📊 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            conn.close()
            return server  # Return the working server name
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    return None

def test_kidoo_database():
    """Test connection to KIDOO database specifically"""
    print("\n🎯 Testing KIDOO Database Connection...")
    print("=" * 50)
    
    server = ".\\SQLEXPRESS"  # Use the working server format
    db_name = "KIDOO"
    
    try:
        # Try with Windows Authentication first
        conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={db_name};Trusted_Connection=yes;"
        print(f"Connection string: {conn_str}")
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Successfully connected to {db_name} database!")
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to {db_name}: {e}")
        
        # Try to create the database
        try:
            print(f"\n🔨 Attempting to create {db_name} database...")
            master_conn_str = f"DRIVER={{SQL Server}};SERVER={server};Trusted_Connection=yes;"
            master_conn = pyodbc.connect(master_conn_str)
            master_cursor = master_conn.cursor()
            
            master_cursor.execute(f"CREATE DATABASE [{db_name}]")
            master_conn.commit()
            master_conn.close()
            
            print(f"✅ Successfully created {db_name} database!")
            return True
            
        except Exception as create_error:
            print(f"❌ Failed to create database: {create_error}")
    
    return False

if __name__ == "__main__":
    print("🧪 Direct SQL Server Connection Test")
    print("=" * 50)
    
    # Test basic connection
    working_server = test_sqlserver_connection()
    
    if working_server:
        print(f"\n✅ Found working server: {working_server}")
        
        # Test KIDOO database
        if test_kidoo_database():
            print("\n🎉 All tests passed! Database is ready.")
        else:
            print("\n⚠️ Database connection issues detected.")
    else:
        print("\n❌ Could not connect to SQL Server.")
        print("\n💡 Troubleshooting suggestions:")
        print("   1. Make sure SQL Server Express is running")
        print("   2. Check if SQL Server Browser service is running")
        print("   3. Verify the server name format")
        print("   4. Try enabling SQL Server authentication")
