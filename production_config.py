import os
from datetime import timedelta

class ProductionConfig:
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-production-key-change-this'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///garbage_collection_prod.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # API Configuration
    API_RATE_LIMIT = "100 per minute"
    API_VERSION = "v1"
    
    # Business Logic Configuration
    DEFAULT_CURRENCY = "USD"
    TAX_RATE = 0.08  # 8% tax rate
    LATE_PAYMENT_FEE = 0.05  # 5% late payment fee
    AUTO_INVOICE_DAYS = 30  # Auto-generate invoices after 30 days
    
    # Notification Settings
    ENABLE_EMAIL_NOTIFICATIONS = True
    ENABLE_SMS_NOTIFICATIONS = False
    NOTIFICATION_RETRY_ATTEMPTS = 3
    
    # Analytics Configuration
    ENABLE_ANALYTICS = True
    ANALYTICS_RETENTION_DAYS = 365
    
    # Backup Configuration
    BACKUP_ENABLED = True
    BACKUP_FREQUENCY_HOURS = 24
    BACKUP_RETENTION_DAYS = 30 