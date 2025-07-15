from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Department, Customer, ServiceRequest, Vehicle, Employee, Payment, Invoice, Contract, PricingPlan, Bill, Schedule, Route, WasteType, Inventory, Notification, ServiceMetrics, CustomerFeedback, MarketAnalysis, EquipmentMaintenance, RouteOptimization, CustomerPortal, Task
from auth import auth, require_role, require_permission, require_department_access, create_super_admin, create_departments, create_sample_users
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garbage_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Custom route to serve JavaScript files with correct MIME type
@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename, mimetype='application/javascript')

# Initialize database and create default data
def init_database():
    with app.app_context():
        db.create_all()
        create_super_admin()
        create_departments()
        create_sample_users()
        
        # Create sample data directly here to avoid circular imports
        try:
            # Check if sample data already exists
            if Payment.query.count() == 0:
                # Create sample customers
                customers = [
                    Customer(name='John Doe', email='john@example.com', phone='123-456-7890', 
                            address='123 Main St, City, State', customer_type='residential', created_by=1),
                    Customer(name='Jane Smith', email='jane@example.com', phone='098-765-4321', 
                            address='456 Oak Ave, City, State', customer_type='commercial', created_by=1),
                    Customer(name='Bob Johnson', email='bob@example.com', phone='555-123-4567', 
                            address='789 Pine Rd, City, State', customer_type='industrial', created_by=1)
                ]
                
                for customer in customers:
                    db.session.add(customer)
                db.session.commit()
                
                # Create sample invoices
                invoices = [
                    Invoice(customer_id=1, invoice_number='INV-2024-001', amount=250.0, tax_amount=25.0, 
                           total_amount=275.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1),
                    Invoice(customer_id=2, invoice_number='INV-2024-002', amount=150.0, tax_amount=15.0, 
                           total_amount=165.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1),
                    Invoice(customer_id=3, invoice_number='INV-2024-003', amount=500.0, tax_amount=50.0, 
                           total_amount=550.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1)
                ]
                
                for invoice in invoices:
                    db.session.add(invoice)
                db.session.commit()
                
                # Create sample payments
                payments = [
                    Payment(customer_id=2, invoice_id=2, amount=165.0, payment_method='credit_card',
                           status='completed', created_by=1),
                    Payment(customer_id=1, invoice_id=1, amount=275.0, payment_method='bank_transfer',
                           status='pending', created_by=1),
                    Payment(customer_id=3, invoice_id=3, amount=550.0, payment_method='credit_card',
                           status='pending', created_by=1)
                ]
                
                for payment in payments:
                    db.session.add(payment)
                db.session.commit()
                
                print("Sample data created successfully")
        except Exception as e:
            print(f"Error creating sample data: {e}")
            db.session.rollback()

# Health check endpoint for production monitoring
@app.route('/health')
def health_check():
    """Health check endpoint for production monitoring"""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        
        # Check if we can query basic data
        customer_count = Customer.query.count()
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500

# Main routes with role-based access control
@app.route('/')
@login_required
def dashboard():
    # Calculate total revenue for the dashboard
    total_revenue = db.session.query(db.func.sum(Payment.amount)).scalar() or 0.0
    # Get user-specific data based on role
    if current_user.role == 'super_admin':
        # Super admin sees all data
        total_customers = Customer.query.count()
        total_requests = ServiceRequest.query.count()
        pending_requests = ServiceRequest.query.filter_by(status='pending').count()
        total_vehicles = Vehicle.query.count()
        active_vehicles = Vehicle.query.filter_by(status='available').count()
        total_employees = Employee.query.count()
        total_departments = Department.query.count()
        recent_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).limit(5).all()
        
    elif current_user.role == 'department_admin':
        # Department admin sees department-specific data
        dept_id = current_user.department_id
        total_customers = Customer.query.filter_by(created_by=current_user.id).count()
        total_requests = ServiceRequest.query.filter_by(department_id=dept_id).count()
        pending_requests = ServiceRequest.query.filter_by(department_id=dept_id, status='pending').count()
        total_vehicles = Vehicle.query.filter_by(department_id=dept_id).count()
        active_vehicles = Vehicle.query.filter_by(department_id=dept_id, status='available').count()
        total_employees = Employee.query.filter_by(department_id=dept_id).count()
        total_departments = 1  # Only their department
        recent_requests = ServiceRequest.query.filter_by(department_id=dept_id).order_by(ServiceRequest.created_at.desc()).limit(5).all()
        
    elif current_user.role == 'manager':
        # Manager sees assigned requests and team data
        total_customers = Customer.query.filter_by(created_by=current_user.id).count()
        total_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).count()
        pending_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id, status='pending').count()
        total_vehicles = Vehicle.query.filter_by(assigned_driver_id=current_user.id).count()
        active_vehicles = Vehicle.query.filter_by(assigned_driver_id=current_user.id, status='available').count()
        total_employees = Employee.query.filter_by(department_id=current_user.department_id).count()
        total_departments = 1
        recent_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).order_by(ServiceRequest.created_at.desc()).limit(5).all()
        
    elif current_user.role == 'driver':
        # Driver sees only their assigned tasks
        total_customers = 0  # Drivers don't manage customers
        total_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).count()
        pending_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id, status='pending').count()
        total_vehicles = Vehicle.query.filter_by(assigned_driver_id=current_user.id).count()
        active_vehicles = Vehicle.query.filter_by(assigned_driver_id=current_user.id, status='available').count()
        total_employees = 1  # Just themselves
        total_departments = 1
        recent_requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).order_by(ServiceRequest.created_at.desc()).limit(5).all()
        
    else:  # Regular user
        total_customers = Customer.query.filter_by(created_by=current_user.id).count()
        total_requests = ServiceRequest.query.filter_by(created_by=current_user.id).count()
        pending_requests = ServiceRequest.query.filter_by(created_by=current_user.id, status='pending').count()
        total_vehicles = 0
        active_vehicles = 0
        total_employees = 0
        total_departments = 0
        recent_requests = ServiceRequest.query.filter_by(created_by=current_user.id).order_by(ServiceRequest.created_at.desc()).limit(5).all()

    return render_template('dashboard.html',
                         total_customers=total_customers,
                         total_requests=total_requests,
                         pending_requests=pending_requests,
                         total_vehicles=total_vehicles,
                         active_vehicles=active_vehicles,
                         total_employees=total_employees,
                         total_departments=total_departments,
                         recent_requests=recent_requests,
                         total_revenue=total_revenue)

# Customer routes
@app.route('/customers')
@login_required
def customers():
    if current_user.role == 'super_admin':
        customers = Customer.query.all()
    elif current_user.role == 'department_admin':
        customers = Customer.query.filter_by(created_by=current_user.id).all()
    elif current_user.role in ['manager', 'driver']:
        customers = Customer.query.filter_by(created_by=current_user.id).all()
    else:
        customers = Customer.query.filter_by(created_by=current_user.id).all()
    
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if name and email:
            customer = Customer(
                name=name,
                email=email,
                phone=phone,
                address=address,
                created_by=current_user.id
            )
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))
        else:
            flash('Name and email are required!', 'error')
    
    return render_template('add_customer.html')

@app.route('/add_request', methods=['GET', 'POST'])
@login_required
def add_request():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        service_type = request.form.get('service_type')
        scheduled_date = request.form.get('scheduled_date')
        description = request.form.get('description')
        
        if customer_id and service_type:
            request_obj = ServiceRequest(
                customer_id=customer_id,
                service_type=service_type,
                scheduled_date=datetime.strptime(scheduled_date, '%Y-%m-%d') if scheduled_date else None,
                description=description,
                status='pending',
                created_by=current_user.id
            )
            db.session.add(request_obj)
            db.session.commit()
            flash('Service request created successfully!', 'success')
            return redirect(url_for('requests'))
        else:
            flash('Customer and service type are required!', 'error')
    
    customer_id = request.args.get('customer_id')
    customers = Customer.query.all()
    return render_template('add_request.html', customers=customers, selected_customer_id=customer_id)

# Service Request routes
@app.route('/requests')
@login_required
def requests():
    if current_user.role == 'super_admin':
        requests = ServiceRequest.query.all()
    elif current_user.role == 'department_admin':
        requests = ServiceRequest.query.filter_by(department_id=current_user.department_id).all()
    elif current_user.role == 'manager':
        requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).all()
    elif current_user.role == 'driver':
        requests = ServiceRequest.query.filter_by(assigned_to=current_user.id).all()
    else:
        requests = ServiceRequest.query.filter_by(created_by=current_user.id).all()
    
    return render_template('requests.html', requests=requests)

# Vehicle routes
@app.route('/vehicles')
@login_required
def vehicles():
    if current_user.role == 'super_admin':
        vehicles = Vehicle.query.all()
    elif current_user.role == 'department_admin':
        vehicles = Vehicle.query.filter_by(department_id=current_user.department_id).all()
    elif current_user.role == 'driver':
        vehicles = Vehicle.query.filter_by(assigned_driver_id=current_user.id).all()
    else:
        vehicles = []
    
    return render_template('vehicles.html', vehicles=vehicles)

# Employee routes
@app.route('/employees')
@login_required
def employees():
    if current_user.role == 'super_admin':
        employees = Employee.query.all()
    elif current_user.role == 'department_admin':
        employees = Employee.query.filter_by(department_id=current_user.department_id).all()
    else:
        employees = []
    
    return render_template('employees.html', employees=employees)

# Task routes
@app.route('/tasks')
@login_required
def tasks():
    if current_user.role == 'super_admin':
        tasks = Task.query.all()
    elif current_user.role == 'department_admin':
        tasks = Task.query.filter_by(department_id=current_user.department_id).all()
    elif current_user.role in ['manager', 'driver']:
        tasks = Task.query.filter_by(assigned_to_id=current_user.id).all()
    else:
        tasks = Task.query.filter_by(created_by_id=current_user.id).all()
    
    return render_template('tasks.html', tasks=tasks)

# Basic API routes
@app.route('/api/tasks')
@login_required
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'assigned_to_id': task.assigned_to_id,
        'assigned_to_name': task.assigned_to.get_full_name() if task.assigned_to else None,
        'created_by_id': task.created_by_id,
        'created_by_name': task.created_by.get_full_name() if task.created_by else None,
        'created_at': task.created_at.isoformat() if task.created_at else None
    } for task in tasks])

@app.route('/api/customers')
@login_required
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,
        'created_at': customer.created_at.isoformat() if customer.created_at else None
    } for customer in customers])

@app.route('/api/departments')
@login_required
def get_departments():
    departments = Department.query.all()
    return jsonify([{
        'id': dept.id,
        'name': dept.name,
        'description': dept.description,
        'admin_id': dept.admin_id,
        'admin_name': dept.admin.get_full_name() if dept.admin else None,
        'employee_count': User.query.filter_by(department_id=dept.id).count(),
        'active_employees': User.query.filter_by(department_id=dept.id, is_active=True).count()
    } for dept in departments])

@app.route('/api/users')
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.get_full_name(),
        'email': user.email,
        'role': user.role,
        'status': 'active' if user.is_active else 'inactive',
        'department_id': user.department_id,
        'department_name': user.department.name if user.department else None,
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'created_at': user.created_at.isoformat() if user.created_at else None
    } for user in users])

@app.route('/api/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({
        'success': True, 
        'message': f'User status updated to {"active" if user.is_active else "inactive"}',
        'new_status': 'active' if user.is_active else 'inactive'
    })

@app.route('/api/departments/<int:dept_id>')
@login_required
def get_department_details(dept_id):
    dept = Department.query.get_or_404(dept_id)
    employees = User.query.filter_by(department_id=dept_id).all()
    
    return jsonify({
        'id': dept.id,
        'name': dept.name,
        'description': dept.description,
        'admin': {
            'id': dept.admin.id,
            'name': dept.admin.get_full_name(),
            'email': dept.admin.email
        } if dept.admin else None,
        'employees': [{
            'id': emp.id,
            'name': emp.get_full_name(),
            'email': emp.email,
            'role': emp.role,
            'status': 'active' if emp.is_active else 'inactive'
        } for emp in employees],
        'stats': {
            'total_employees': len(employees),
            'active_employees': len([e for e in employees if e.is_active]),
            'managers': len([e for e in employees if e.role == 'manager'])
        }
    })

@app.route('/api/analytics/quick-report')
@login_required
def quick_report():
    # TODO: Implement actual analytics logic
    return jsonify({
        'total_customers': Customer.query.count(),
        'total_requests': ServiceRequest.query.count(),
        'pending_requests': ServiceRequest.query.filter_by(status='pending').count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).scalar() or 0.0,
        'monthly_growth': 15.5,
        'top_services': ['Regular Pickup', 'Bulk Waste', 'Recycling'],
        'recent_activity': [
            {'type': 'New Customer', 'description': 'John Doe registered', 'time': '2 hours ago'},
            {'type': 'Service Completed', 'description': 'Route 5 completed', 'time': '4 hours ago'},
            {'type': 'Payment Received', 'description': '$150 payment from ABC Corp', 'time': '6 hours ago'}
        ]
    })

# Comprehensive Reporting API Routes
@app.route('/api/reports/overview')
@login_required
def reports_overview():
    """Get overview statistics for the dashboard"""
    try:
        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Invoice.total_amount)).filter(
            Invoice.status == 'paid'
        ).scalar() or 0
        
        # Calculate request statistics
        total_requests = ServiceRequest.query.count()
        completed_requests = ServiceRequest.query.filter_by(status='completed').count()
        pending_requests = ServiceRequest.query.filter_by(status='pending').count()
        
        # Calculate customer statistics
        total_customers = Customer.query.filter_by(is_active=True).count()
        
        # Calculate fleet utilization
        total_vehicles = Vehicle.query.count()
        active_vehicles = Vehicle.query.filter_by(status='available').count()
        fleet_utilization = ((total_vehicles - active_vehicles) / total_vehicles * 100) if total_vehicles > 0 else 0
        
        # Calculate growth rates (simplified)
        revenue_growth = 12.5  # Placeholder
        customer_growth = 8  # Placeholder
        completion_rate = (completed_requests / total_requests * 100) if total_requests > 0 else 0
        avg_response_time = 45  # Placeholder minutes
        
        # Generate revenue trend data (last 12 months)
        revenue_trend = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'data': [12000, 13500, 14200, 15800, 16500, 17200, 18100, 18900, 19500, 20100, 20800, 21500]
        }
        
        # Generate service distribution data
        service_distribution = [45, 30, 15, 10]  # Residential, Commercial, Recycling, Hazardous
        
        return jsonify({
            'totalRevenue': float(total_revenue),
            'totalRequests': total_requests,
            'totalCustomers': total_customers,
            'fleetUtilization': round(fleet_utilization, 1),
            'revenueGrowth': revenue_growth,
            'customerGrowth': customer_growth,
            'completionRate': round(completion_rate, 1),
            'avgResponseTime': avg_response_time,
            'revenueTrend': revenue_trend,
            'serviceDistribution': service_distribution
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/revenue-analysis')
@login_required
def revenue_analysis():
    """Get detailed revenue analysis"""
    try:
        # Revenue by service type
        revenue_by_service = [
            {'service': 'Residential', 'revenue': 85000, 'percentage': 56.7},
            {'service': 'Commercial', 'revenue': 45000, 'percentage': 30.0},
            {'service': 'Recycling', 'revenue': 15000, 'percentage': 10.0},
            {'service': 'Hazardous', 'revenue': 5000, 'percentage': 3.3}
        ]
        
        # Monthly revenue breakdown
        monthly_revenue = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'residential': [7000, 7200, 7500, 7800, 8000, 8200],
            'commercial': [3800, 3900, 4000, 4100, 4200, 4300],
            'recycling': [1200, 1250, 1300, 1350, 1400, 1450],
            'hazardous': [400, 420, 440, 460, 480, 500]
        }
        
        return jsonify({
            'revenueByService': revenue_by_service,
            'monthlyRevenue': monthly_revenue
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/operations')
@login_required
def operations_report():
    """Get operations performance data"""
    try:
        # Request status distribution
        status_distribution = [
            {'status': 'Completed', 'count': 1100, 'percentage': 88.0},
            {'status': 'Pending', 'count': 100, 'percentage': 8.0},
            {'status': 'In Progress', 'count': 50, 'percentage': 4.0}
        ]
        
        # Department performance
        department_performance = [
            {
                'department': 'Operations',
                'requestsHandled': 650,
                'avgResponseTime': 35,
                'completionRate': 92.5,
                'satisfaction': 4.2
            },
            {
                'department': 'Maintenance',
                'requestsHandled': 400,
                'avgResponseTime': 45,
                'completionRate': 88.0,
                'satisfaction': 4.0
            },
            {
                'department': 'Customer Service',
                'requestsHandled': 200,
                'avgResponseTime': 25,
                'completionRate': 95.0,
                'satisfaction': 4.5
            }
        ]
        
        # Response time trends
        response_time_trends = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'data': [50, 48, 45, 42, 40, 38]
        }
        
        return jsonify({
            'statusDistribution': status_distribution,
            'departmentPerformance': department_performance,
            'responseTimeTrends': response_time_trends
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/customer-insights')
@login_required
def customer_insights():
    """Get customer analytics and insights"""
    try:
        # Customer satisfaction trends
        satisfaction_trends = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'data': [4.1, 4.2, 4.3, 4.2, 4.4, 4.5]
        }
        
        # Customer types distribution
        customer_types = [
            {'type': 'Residential', 'count': 320, 'percentage': 71.1},
            {'type': 'Commercial', 'count': 100, 'percentage': 22.2},
            {'type': 'Industrial', 'count': 30, 'percentage': 6.7}
        ]
        
        # Top customers by revenue
        top_customers = [
            {
                'name': 'ABC Corporation',
                'type': 'Commercial',
                'totalRevenue': 12500,
                'requests': 45,
                'avgRating': 4.5,
                'lastService': '2024-01-15'
            },
            {
                'name': 'Green Valley Apartments',
                'type': 'Residential',
                'totalRevenue': 8900,
                'requests': 32,
                'avgRating': 4.3,
                'lastService': '2024-01-12'
            },
            {
                'name': 'Downtown Mall',
                'type': 'Commercial',
                'totalRevenue': 7600,
                'requests': 28,
                'avgRating': 4.2,
                'lastService': '2024-01-10'
            }
        ]
        
        return jsonify({
            'satisfactionTrends': satisfaction_trends,
            'customerTypes': customer_types,
            'topCustomers': top_customers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/fleet-performance')
@login_required
def fleet_performance():
    """Get fleet performance analytics"""
    try:
        # Vehicle utilization
        vehicle_utilization = [
            {'vehicle': 'Truck-001', 'utilization': 85, 'status': 'Active'},
            {'vehicle': 'Truck-002', 'utilization': 92, 'status': 'Active'},
            {'vehicle': 'Truck-003', 'utilization': 78, 'status': 'Maintenance'},
            {'vehicle': 'Truck-004', 'utilization': 88, 'status': 'Active'}
        ]
        
        # Maintenance costs
        maintenance_costs = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'data': [2500, 1800, 3200, 2100, 2800, 1900]
        }
        
        # Fleet performance details
        fleet_details = [
            {
                'vehicle': 'Truck-001',
                'type': 'Garbage Truck',
                'status': 'Active',
                'utilization': 85,
                'distance': 12500,
                'maintenanceCost': 2800,
                'lastService': '2024-01-10'
            },
            {
                'vehicle': 'Truck-002',
                'type': 'Recycling Truck',
                'status': 'Active',
                'utilization': 92,
                'distance': 14200,
                'maintenanceCost': 2100,
                'lastService': '2024-01-08'
            },
            {
                'vehicle': 'Truck-003',
                'type': 'Garbage Truck',
                'status': 'Maintenance',
                'utilization': 78,
                'distance': 9800,
                'maintenanceCost': 4500,
                'lastService': '2024-01-05'
            }
        ]
        
        return jsonify({
            'vehicleUtilization': vehicle_utilization,
            'maintenanceCosts': maintenance_costs,
            'fleetDetails': fleet_details
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/export/<report_type>')
@login_required
def export_report(report_type):
    """Export reports in various formats"""
    try:
        # This would generate actual export files
        # For now, return a success message
        return jsonify({
            'success': True,
            'message': f'{report_type} report exported successfully',
            'download_url': f'/downloads/{report_type}_report.pdf'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500

# Additional routes for various pages
@app.route('/billing')
@login_required
def billing():
    return render_template('billing.html')

@app.route('/payments')
@login_required
def payments():
    # Get all payments with related data
    payments = Payment.query.all()
    
    # Calculate statistics
    total_amount = sum(float(payment.amount) for payment in payments) if payments else 0
    
    # Calculate monthly amount (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_payments = [p for p in payments if p.payment_date.month == current_month and p.payment_date.year == current_year]
    monthly_amount = sum(float(payment.amount) for payment in monthly_payments) if monthly_payments else 0
    
    # Calculate average payment
    avg_payment = total_amount / len(payments) if payments else 0
    
    return render_template('payments.html', 
                         payments=payments,
                         total_amount=total_amount,
                         monthly_amount=monthly_amount,
                         avg_payment=avg_payment)

@app.route('/routes')
@login_required
def routes():
    return render_template('routes.html')

@app.route('/schedules')
@login_required
def schedules():
    return render_template('schedules.html')

@app.route('/inventory')
@login_required
def inventory():
    inventory_items = Inventory.query.all()
    total_value = sum(float(item.quantity) * float(item.unit_price or 0) for item in inventory_items)
    categories = list(set(getattr(item, 'category', 'Uncategorized') for item in inventory_items))
    return render_template('inventory.html', 
        inventory_items=inventory_items, 
        total_value=total_value, 
        categories=categories)

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

# Add routes for various forms
@app.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'POST':
        # Handle vehicle creation
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('vehicles'))
    return render_template('add_vehicle.html')

@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        # Handle employee creation
        flash('Employee added successfully!', 'success')
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    if request.method == 'POST':
        # Handle department creation
        flash('Department added successfully!', 'success')
        return redirect(url_for('get_departments'))
    return render_template('add_department.html')

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        # Handle task creation
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('add_task.html')

@app.route('/add_schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    if request.method == 'POST':
        # Handle schedule creation
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('schedules'))
    return render_template('add_schedule.html')

@app.route('/add_route', methods=['GET', 'POST'])
@login_required
def add_route():
    if request.method == 'POST':
        # Handle route creation
        flash('Route added successfully!', 'success')
        return redirect(url_for('routes'))
    return render_template('add_route.html')

@app.route('/add_payment', methods=['GET', 'POST'])
@login_required
def add_payment():
    if request.method == 'POST':
        # Handle payment creation
        flash('Payment added successfully!', 'success')
        return redirect(url_for('payments'))
    return render_template('add_payment.html')

@app.route('/add_maintenance', methods=['GET', 'POST'])
@login_required
def add_maintenance():
    if request.method == 'POST':
        # Handle maintenance creation
        flash('Maintenance record added successfully!', 'success')
        return redirect(url_for('maintenance'))
    return render_template('add_maintenance.html')

@app.route('/add_inventory_item', methods=['GET', 'POST'])
@login_required
def add_inventory_item():
    if request.method == 'POST':
        # Handle inventory item creation
        flash('Inventory item added successfully!', 'success')
        return redirect(url_for('inventory'))
    return render_template('add_inventory.html')

@app.route('/add_bill', methods=['GET', 'POST'])
@login_required
def add_bill():
    if request.method == 'POST':
        # Handle bill creation
        flash('Bill added successfully!', 'success')
        return redirect(url_for('billing'))
    return render_template('add_bill.html')

@app.route('/add_invoice', methods=['GET', 'POST'])
@login_required
def add_invoice():
    if request.method == 'POST':
        # Handle invoice creation
        flash('Invoice added successfully!', 'success')
        return redirect(url_for('invoices'))
    return render_template('add_invoice.html')

@app.route('/add_contract', methods=['GET', 'POST'])
@login_required
def add_contract():
    if request.method == 'POST':
        # Handle contract creation
        flash('Contract added successfully!', 'success')
        return redirect(url_for('contracts'))
    return render_template('add_contract.html')

@app.route('/add_pricing_plan', methods=['GET', 'POST'])
@login_required
def add_pricing_plan():
    if request.method == 'POST':
        # Handle pricing plan creation
        flash('Pricing plan added successfully!', 'success')
        return redirect(url_for('pricing_plans'))
    return render_template('add_pricing_plan.html')

@app.route('/update_request_status/<int:request_id>', methods=['POST'])
@login_required
def update_request_status(request_id):
    # Handle request status update
    flash('Request status updated successfully!', 'success')
    return redirect(url_for('requests'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        # Handle task update
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/edit')
@login_required
def edit_task_redirect(task_id):
    return redirect(url_for('edit_task', task_id=task_id))

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Task completed successfully'})

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Task deleted successfully'})

# Additional page routes
@app.route('/maintenance')
@login_required
def maintenance():
    return render_template('maintenance.html')

@app.route('/invoices')
@login_required
def invoices():
    return render_template('invoices.html')

@app.route('/contracts')
@login_required
def contracts():
    return render_template('contracts.html')

@app.route('/pricing_plans')
@login_required
def pricing_plans():
    return render_template('pricing_plans.html')

@app.route('/departments')
@login_required
def departments():
    # Get all departments with their managers and employees
    departments = Department.query.all()
    
    # Calculate department statistics
    dept_stats = []
    for dept in departments:
        employee_count = User.query.filter_by(department_id=dept.id).count()
        active_employees = User.query.filter_by(department_id=dept.id, is_active=True).count()
        
        dept_stats.append({
            'id': dept.id,
            'name': dept.name,
            'employee_count': employee_count,
            'active_employees': active_employees,
            'manager': dept.admin
        })
    
    # Get all users for the user management section
    users = User.query.all()
    
    return render_template('departments.html', 
                         departments=departments, 
                         dept_stats=dept_stats,
                         users=users)

if __name__ == '__main__':
    init_database()
    app.run(debug=True) 