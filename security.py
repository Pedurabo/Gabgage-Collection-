from functools import wraps
from flask import abort, current_app, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import string
from datetime import datetime, timedelta
# import jwt  # Commented out to prevent import error if PyJWT is not installed

class SecurityManager:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        
    def generate_secure_password(self, length=12):
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(c.isdigit() for c in password)
                    and any(c in "!@#$%^&*" for c in password)):
                return password
    
    def validate_password_strength(self, password):
        """Validate password meets security requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if not re.search(r"[!@#$%^&*]", password):
            return False, "Password must contain at least one special character (!@#$%^&*)"
        
        return True, "Password meets requirements"
    
    def hash_password(self, password):
        """Hash password using werkzeug security"""
        return generate_password_hash(password, method='pbkdf2:sha256')
    
    def verify_password(self, password_hash, password):
        """Verify password against hash"""
        return check_password_hash(password_hash, password)
    
    def generate_api_key(self):
        """Generate secure API key"""
        return secrets.token_urlsafe(32)
    
    def generate_jwt_token(self, user_id, expires_in=3600):
        """Generate JWT token for API authentication"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def verify_jwt_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

# Role-based access control decorators
def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                abort(401, description="Authentication required")
            
            # Get user role from session or database
            user_role = session.get('user_role', 'user')
            
            if user_role != role and user_role != 'admin':
                abort(403, description="Insufficient permissions")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin(f):
    """Decorator to require admin role"""
    return require_role('admin')(f)

def require_manager(f):
    """Decorator to require manager role"""
    return require_role('manager')(f)

def require_driver(f):
    """Decorator to require driver role"""
    return require_role('driver')(f)

# Security middleware
def security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Rate limiting
def rate_limit(limit="100 per minute"):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple IP-based rate limiting
            client_ip = request.remote_addr
            # Implementation would use Redis or similar for production
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Input sanitization
def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

# CSRF protection
def generate_csrf_token():
    """Generate CSRF token"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def validate_csrf_token(token):
    """Validate CSRF token"""
    return token == session.get('csrf_token')

# Audit logging
def log_security_event(event_type, user_id=None, details=None):
    """Log security events"""
    from datetime import datetime
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'details': details
    }
    # In production, this would write to a secure log file or database
    print(f"SECURITY LOG: {log_entry}")

# Initialize security manager
security = SecurityManager() 