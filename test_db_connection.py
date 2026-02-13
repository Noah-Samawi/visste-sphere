#!/usr/bin/env python3
"""
Test script to verify database connection with Neon DATABASE_URL.
Usage: DATABASE_URL="your-neon-url" python3 test_db_connection.py
"""
import os
import sys
import dj_database_url

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visstesphere.settings')

def test_database_connection():
    """Test database connection and run migrations."""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not set!")
        print("\nUsage:")
        print('  export DATABASE_URL="postgresql://user:pass@host:port/db"')
        print('  python3 test_db_connection.py')
        sys.exit(1)
    
    print(f"✓ DATABASE_URL found: {database_url[:50]}...")
    
    try:
        # Parse database URL
        db_config = dj_database_url.parse(database_url)
        print(f"✓ Database URL parsed successfully")
        print(f"  Engine: {db_config.get('ENGINE', 'N/A')}")
        print(f"  Host: {db_config.get('HOST', 'N/A')}")
        print(f"  Database: {db_config.get('NAME', 'N/A')}")
        
        # Test connection
        import django
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✓ Database connection successful!")
            print(f"  PostgreSQL version: {version[0]}")
        
        # Check migrations
        from django.core.management import call_command
        print("\n📋 Checking migration status...")
        call_command('showmigrations', verbosity=0)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_database_connection()
    sys.exit(0 if success else 1)
