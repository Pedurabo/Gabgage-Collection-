#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('production.env')

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, init_database

# Initialize database if needed
if __name__ == "__main__":
    init_database()
    app.run(host='0.0.0.0', port=5000)
else:
    # For WSGI servers
    init_database() 