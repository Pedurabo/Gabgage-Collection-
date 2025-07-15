from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Department, Employee
from datetime import datetime, timedelta
import re
from functools import wraps

auth = Blueprint('auth', __name__)

# Role-based permission decorators
def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role != role and current_user.role != 'super_admin':
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(permission):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not current_user.has_permission(permission):
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_department_access(department_id):
    """Decorator to require department access"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not current_user.can_access_department(department_id):
                flash('Access denied. You cannot access this department.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Password validation
def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

# Email validation
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Account lockout management
def check_account_lockout(user):
    """Check if account is locked due to failed attempts"""
    if user.is_locked():
        remaining_time = user.locked_until - datetime.utcnow()
        minutes = int(remaining_time.total_seconds() / 60)
        return True, f"Account is locked. Try again in {minutes} minutes."
    return False, None

def lock_account(user):
    """Lock account for 15 minutes after 5 failed attempts"""
    user.failed_login_attempts += 1
    if user.failed_login_attempts >= 5:
        user.locked_until = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()

def reset_failed_attempts(user):
    """Reset failed login attempts on successful login"""
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.session.commit()

# Authentication routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        # Validation
        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')
        
        # Check if account is locked
        is_locked, lock_message = check_account_lockout(user)
        if is_locked:
            flash(lock_message, 'error')
            return render_template('auth/login.html')
        
        # Check if account is active
        if not user.is_active:
            flash('Account is deactivated. Contact administrator.', 'error')
            return render_template('auth/login.html')
        
        # Verify password
        if not user.check_password(password):
            lock_account(user)
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')
        
        # Successful login
        reset_failed_attempts(user)
        login_user(user, remember=remember)
        
        # Log login activity
        log_login_activity(user, request.remote_addr)
        
        # Redirect based on role
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        return redirect(url_for('dashboard'))
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validation
        errors = []
        
        if not all([username, email, password, confirm_password, first_name, last_name]):
            errors.append('Please fill in all fields.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Validate password strength
        is_valid, password_message = validate_password(password)
        if not is_valid:
            errors.append(password_message)
        
        # Validate email format
        if not validate_email(email):
            errors.append('Please enter a valid email address.')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='user',  # Default role
            is_verified=False
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please wait for admin approval.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        # Validate new password strength
        is_valid, password_message = validate_password(new_password)
        if not is_valid:
            flash(password_message, 'error')
            return render_template('auth/change_password.html')
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')

# Admin routes for user management
@auth.route('/admin/users')
@login_required
@require_role('super_admin')
def admin_users():
    users = User.query.all()
    departments = Department.query.all()
    return render_template('auth/admin_users.html', users=users, departments=departments)

@auth.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@require_role('super_admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    departments = Department.query.all()
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.department_id = request.form.get('department_id') or None
        user.is_active = request.form.get('is_active') == 'on'
        user.is_verified = request.form.get('is_verified') == 'on'
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('auth.admin_users'))
    
    return render_template('auth/edit_user.html', user=user, departments=departments)

@auth.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@require_role('super_admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('auth.admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('auth.admin_users'))

# Department admin routes
@auth.route('/department/users')
@login_required
@require_role('department_admin')
def department_users():
    if not current_user.department_id:
        flash('You are not assigned to any department.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.filter_by(department_id=current_user.department_id).all()
    return render_template('auth/department_users.html', users=users)

@auth.route('/department/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@require_role('department_admin')
def edit_department_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if user belongs to admin's department
    if user.department_id != current_user.department_id:
        flash('You can only edit users in your department.', 'error')
        return redirect(url_for('auth.department_users'))
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        user.is_active = request.form.get('is_active') == 'on'
        
        # Department admins can only change roles within their department
        new_role = request.form.get('role')
        if new_role in ['user', 'driver', 'manager']:
            user.role = new_role
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('auth.department_users'))
    
    return render_template('auth/edit_department_user.html', user=user)

# Utility functions
def log_login_activity(user, ip_address):
    """Log user login activity"""
    # This could be expanded to log to a separate table
    print(f"User {user.username} logged in from {ip_address} at {datetime.utcnow()}")

def create_super_admin():
    """Create super admin user if none exists"""
    if not User.query.filter_by(role='super_admin').first():
        admin = User(
            username='admin',
            email='admin@ecoclean.com',
            first_name='Super',
            last_name='Admin',
            role='super_admin',
            is_active=True,
            is_verified=True
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        db.session.commit()
        print("Super admin created: username=admin, password=Admin@123")

def create_departments():
    """Create default departments"""
    departments = [
        {'name': 'Operations', 'description': 'Main operations department'},
        {'name': 'Fleet Management', 'description': 'Vehicle and equipment management'},
        {'name': 'Customer Service', 'description': 'Customer support and relations'},
        {'name': 'Finance', 'description': 'Billing and financial operations'},
        {'name': 'Maintenance', 'description': 'Equipment and facility maintenance'}
    ]
    
    for dept_data in departments:
        if not Department.query.filter_by(name=dept_data['name']).first():
            dept = Department(**dept_data)
            db.session.add(dept)
    
    db.session.commit()
    print("Default departments created")

def create_sample_users():
    """Create sample users for testing"""
    # Department admins
    dept_admins = [
        {
            'username': 'ops_admin',
            'email': 'ops@ecoclean.com',
            'first_name': 'Operations',
            'last_name': 'Admin',
            'role': 'department_admin',
            'department_name': 'Operations'
        },
        {
            'username': 'fleet_admin',
            'email': 'fleet@ecoclean.com',
            'first_name': 'Fleet',
            'last_name': 'Admin',
            'role': 'department_admin',
            'department_name': 'Fleet Management'
        },
        {
            'username': 'cs_admin',
            'email': 'cs@ecoclean.com',
            'first_name': 'Customer Service',
            'last_name': 'Admin',
            'role': 'department_admin',
            'department_name': 'Customer Service'
        }
    ]
    
    for admin_data in dept_admins:
        if not User.query.filter_by(username=admin_data['username']).first():
            dept = Department.query.filter_by(name=admin_data['department_name']).first()
            if dept:
                admin = User(
                    username=admin_data['username'],
                    email=admin_data['email'],
                    first_name=admin_data['first_name'],
                    last_name=admin_data['last_name'],
                    role=admin_data['role'],
                    department_id=dept.id,
                    is_active=True,
                    is_verified=True
                )
                admin.set_password('Admin@123')
                db.session.add(admin)
    
    # Sample managers and drivers
    sample_users = [
        {
            'username': 'manager1',
            'email': 'manager1@ecoclean.com',
            'first_name': 'John',
            'last_name': 'Manager',
            'role': 'manager',
            'department_name': 'Operations'
        },
        {
            'username': 'driver1',
            'email': 'driver1@ecoclean.com',
            'first_name': 'Mike',
            'last_name': 'Driver',
            'role': 'driver',
            'department_name': 'Operations'
        },
        {
            'username': 'driver2',
            'email': 'driver2@ecoclean.com',
            'first_name': 'Sarah',
            'last_name': 'Driver',
            'role': 'driver',
            'department_name': 'Fleet Management'
        }
    ]
    
    for user_data in sample_users:
        if not User.query.filter_by(username=user_data['username']).first():
            dept = Department.query.filter_by(name=user_data['department_name']).first()
            if dept:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role'],
                    department_id=dept.id,
                    is_active=True,
                    is_verified=True
                )
                user.set_password('User@123')
                db.session.add(user)
    
    db.session.commit()
    print("Sample users created") 