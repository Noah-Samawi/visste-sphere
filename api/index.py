"""
Vercel serverless function entry point for Django application.
This file routes all requests to the Django WSGI application.
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module BEFORE importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visstesphere.settings')

# Import Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    # Get WSGI application - Vercel expects 'app' variable
    app = get_wsgi_application()
except Exception as e:
    # Log the error for debugging
    import traceback
    print(f"Error initializing Django application: {e}")
    print(traceback.format_exc())
    raise
