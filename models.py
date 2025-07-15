from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model for Authentication with Department-based Roles
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='user')  # super_admin, department_admin, manager, driver, user
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    # Relationships - explicitly specify foreign_keys to avoid ambiguity
    department = db.relationship('Department', foreign_keys=[department_id], backref=db.backref('department_users', lazy=True))
    created_requests = db.relationship('ServiceRequest', backref='created_by_user', foreign_keys='ServiceRequest.created_by')
    assigned_requests = db.relationship('ServiceRequest', backref='assigned_to_user', foreign_keys='ServiceRequest.assigned_to')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        if self.role == 'super_admin':
            return True
        elif self.role == 'department_admin':
            return permission in ['manage_department', 'view_department', 'edit_department_users']
        elif self.role == 'manager':
            return permission in ['manage_requests', 'view_reports', 'assign_tasks']
        elif self.role == 'driver':
            return permission in ['view_assigned_tasks', 'update_task_status']
        return False
    
    def can_access_department(self, department_id):
        """Check if user can access specific department"""
        if self.role == 'super_admin':
            return True
        return self.department_id == department_id
    
    def is_locked(self):
        """Check if account is locked due to failed attempts"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

# Department Model with Admin Assignment
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - explicitly specify foreign_keys to avoid ambiguity
    admin = db.relationship('User', foreign_keys=[admin_id], backref=db.backref('admin_departments', lazy=True))
    
    def get_admin(self):
        """Get department admin user"""
        return User.query.get(self.admin_id)
    
    def set_admin(self, user_id):
        """Set department admin"""
        user = User.query.get(user_id)
        if user and user.role in ['department_admin', 'super_admin']:
            self.admin_id = user_id
            return True
        return False

# Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text, nullable=False)
    customer_type = db.Column(db.String(20), default='residential')  # residential, commercial, industrial
    service_frequency = db.Column(db.String(20), default='weekly')  # weekly, biweekly, monthly, on-demand
    payment_method = db.Column(db.String(20), default='credit_card')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    requests = db.relationship('ServiceRequest', backref='customer')
    payments = db.relationship('Payment', backref='customer')
    invoices = db.relationship('Invoice', backref='customer')

# Service Request Model
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # residential, commercial, recycling, hazardous, bulk
    scheduled_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, in_progress, completed, cancelled
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    
    # Relationships
    department = db.relationship('Department', backref='requests')
    schedules = db.relationship('Schedule', backref='service_request')

# Vehicle Model
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)  # garbage_truck, recycling_truck, pickup_truck
    capacity = db.Column(db.String(20))
    fuel_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default='available')  # available, in_use, maintenance, out_of_service
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    last_location_update = db.Column(db.DateTime)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    assigned_driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', backref='vehicles')
    assigned_driver = db.relationship('User', foreign_keys=[assigned_driver_id])
    maintenance_records = db.relationship('EquipmentMaintenance', backref='vehicle')

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    position = db.Column(db.String(50), nullable=False)  # driver, collector, supervisor, manager
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Numeric(10, 2))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='employee_profile')
    department = db.relationship('Department', foreign_keys=[department_id], backref='employees')

# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # credit_card, bank_transfer, cash, check
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    transaction_id = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    invoice = db.relationship('Invoice', backref='payments')

# Invoice Model
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue, cancelled
    due_date = db.Column(db.Date, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    paid_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    items = db.relationship('InvoiceItem', backref='invoice')

# Invoice Item Model
class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

# Contract Model
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)  # residential, commercial, industrial
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    monthly_fee = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, expired, cancelled, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Pricing Plan Model
class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)  # weekly, biweekly, monthly
    service_type = db.Column(db.String(50), nullable=False)  # residential, commercial, recycling
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Bill Model
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    items = db.relationship('BillItem', backref='bill')

# Bill Item Model
class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

# Schedule Model
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    notes = db.Column(db.Text)
    completion_notes = db.Column(db.Text)
    completion_photo = db.Column(db.String(255))
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    driver = db.relationship('User', foreign_keys=[driver_id])
    vehicle = db.relationship('Vehicle', backref='schedules')

# Route Model
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_location = db.Column(db.String(200))
    end_location = db.Column(db.String(200))
    estimated_duration = db.Column(db.Integer)  # in minutes
    distance = db.Column(db.Float)  # in kilometers
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])
    department = db.relationship('Department', backref='routes')

# Waste Type Model
class WasteType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    disposal_method = db.Column(db.String(100))
    hazardous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Inventory Model
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Numeric(10, 2))
    supplier = db.Column(db.String(100))
    reorder_level = db.Column(db.Integer, default=10)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    department = db.relationship('Department', backref='inventory')
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # info, warning, error, success
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')

# Service Metrics Model
class ServiceMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    metric_date = db.Column(db.Date, nullable=False)
    total_requests = db.Column(db.Integer, default=0)
    completed_requests = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Float)  # in hours
    customer_satisfaction = db.Column(db.Float)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', backref='metrics')

# Customer Feedback Model
class CustomerFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    comment = db.Column(db.Text)
    feedback_type = db.Column(db.String(50))  # service, driver, vehicle, general
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service_request = db.relationship('ServiceRequest', backref='feedback')

# Market Analysis Model
class MarketAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_date = db.Column(db.Date, nullable=False)
    market_segment = db.Column(db.String(50))  # residential, commercial, industrial
    customer_growth = db.Column(db.Float)  # percentage
    revenue_growth = db.Column(db.Float)  # percentage
    competitor_analysis = db.Column(db.Text)
    market_trends = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Equipment Maintenance Model
class EquipmentMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    maintenance_type = db.Column(db.String(50))  # preventive, corrective, emergency
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Numeric(10, 2))
    scheduled_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed
    technician = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Route Optimization Model
class RouteOptimization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    optimization_date = db.Column(db.DateTime, default=datetime.utcnow)
    original_distance = db.Column(db.Float)
    optimized_distance = db.Column(db.Float)
    time_saved = db.Column(db.Integer)  # in minutes
    fuel_saved = db.Column(db.Float)  # in liters
    algorithm_used = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    route = db.relationship('Route', backref='optimizations')
    created_by_user = db.relationship('User', foreign_keys=[created_by])

# Customer Portal Model
class CustomerPortal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer', backref='portal_account')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    due_date = db.Column(db.Date)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign keys
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    # Relationships
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tasks')
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_tasks')
    department = db.relationship('Department', backref='tasks')
    service_request = db.relationship('ServiceRequest', backref='tasks')
    vehicle = db.relationship('Vehicle', backref='tasks')
    # Real-life logic methods
    def is_overdue(self):
        return self.due_date and self.status != 'completed' and self.due_date < datetime.utcnow().date()
    def mark_complete(self):
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
    def escalate(self):
        self.priority = 'urgent'
    def assign(self, user_id):
        self.assigned_to_id = user_id
    def __repr__(self):
        return f'<Task {self.title} - {self.status}>' 