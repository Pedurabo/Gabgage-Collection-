#!/usr/bin/env python3
"""
Production startup script for Garbage Collection Management System
"""
import os
import sys
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('production.env')

# Set production environment
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'app.py'

if __name__ == "__main__":
    from app import app, init_database
    
    # Initialize database
    init_database()
    
    # Start production server
    print("🚀 Starting Garbage Collection Management System in PRODUCTION mode...")
    print("📍 Application URL: http://127.0.0.1:5000")
    print("🔍 Health Check: http://127.0.0.1:5000/health")
    print("⚠️  This is a development server. For true production, use Gunicorn or uWSGI.")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    ) 