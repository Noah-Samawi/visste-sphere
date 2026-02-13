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
# Vercel Python runtime expects 'app' variable to be a WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    
    # Initialize Django application
    # This is the WSGI application that Vercel will call
    app = get_wsgi_application()
    
except Exception as e:
    # Log the error for debugging in Vercel logs
    import traceback
    error_msg = f"Error initializing Django application: {e}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)
    
    # Create a simple error handler for Vercel that shows the error
    def error_app(environ, start_response):
        """Fallback error handler that displays the error."""
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [error_msg.encode('utf-8')]
    
    # Assign error handler as app so Vercel can at least show the error
    app = error_app
    
    # Don't raise here - let Vercel handle the error through the error_app
