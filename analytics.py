from flask import Blueprint, render_template, request, jsonify
from models import db, Customer, ServiceRequest, Vehicle, Employee, Payment, Invoice, Contract, PricingPlan, Bill, Route
from datetime import datetime, timedelta
import json
import random

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics')
def analytics_dashboard():
    """Analytics dashboard"""
    # Get basic statistics
    total_customers = Customer.query.count()
    total_requests = ServiceRequest.query.count()
    total_vehicles = Vehicle.query.count()
    total_employees = Employee.query.count()
    
    # Get recent data for charts
    recent_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).limit(10).all()
    recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(10).all()
    
    # Calculate revenue
    total_revenue = sum(payment.amount for payment in Payment.query.all())
    
    # Get service type distribution
    service_types = db.session.query(ServiceRequest.service_type, db.func.count(ServiceRequest.id)).group_by(ServiceRequest.service_type).all()
    
    # Get customer types
    customer_types = db.session.query(Customer.customer_type, db.func.count(Customer.id)).group_by(Customer.customer_type).all()
    
    # Get vehicle status
    vehicle_status = db.session.query(Vehicle.status, db.func.count(Vehicle.id)).group_by(Vehicle.status).all()
    
    return render_template('analytics.html',
                         total_customers=total_customers,
                         total_requests=total_requests,
                         total_vehicles=total_vehicles,
                         total_employees=total_employees,
                         total_revenue=total_revenue,
                         recent_requests=recent_requests,
                         recent_payments=recent_payments,
                         service_types=service_types,
                         customer_types=customer_types,
                         vehicle_status=vehicle_status)

@analytics.route('/api/analytics/revenue')
def revenue_analytics():
    """Revenue analytics API"""
    # Get monthly revenue data
    payments = Payment.query.all()
    
    # Group by month
    monthly_revenue = {}
    for payment in payments:
        month = payment.payment_date.strftime('%Y-%m')
        if month not in monthly_revenue:
            monthly_revenue[month] = 0
        monthly_revenue[month] += payment.amount
    
    return jsonify({
        'monthly_revenue': monthly_revenue,
        'total_revenue': sum(monthly_revenue.values()),
        'average_revenue': sum(monthly_revenue.values()) / len(monthly_revenue) if monthly_revenue else 0
    })

@analytics.route('/api/analytics/customers')
def customer_analytics():
    """Customer analytics API"""
    customers = Customer.query.all()
    
    # Customer type distribution
    customer_types = {}
    for customer in customers:
        customer_type = customer.customer_type
        if customer_type not in customer_types:
            customer_types[customer_type] = 0
        customer_types[customer_type] += 1
    
    # Service frequency distribution
    service_frequencies = {}
    for customer in customers:
        frequency = customer.service_frequency
        if frequency not in service_frequencies:
            service_frequencies[frequency] = 0
        service_frequencies[frequency] += 1
    
    return jsonify({
        'total_customers': len(customers),
        'customer_types': customer_types,
        'service_frequencies': service_frequencies
    })

@analytics.route('/api/analytics/operations')
def operations_analytics():
    """Operations analytics API"""
    requests = ServiceRequest.query.all()
    vehicles = Vehicle.query.all()
    employees = Employee.query.all()
    
    # Service request status distribution
    request_status = {}
    for request in requests:
        status = request.status
        if status not in request_status:
            request_status[status] = 0
        request_status[status] += 1
    
    # Vehicle utilization
    vehicle_utilization = {}
    for vehicle in vehicles:
        status = vehicle.status
        if status not in vehicle_utilization:
            vehicle_utilization[status] = 0
        vehicle_utilization[status] += 1
    
    # Employee roles
    employee_roles = {}
    for employee in employees:
        role = employee.role
        if role not in employee_roles:
            employee_roles[role] = 0
        employee_roles[role] += 1
    
    return jsonify({
        'total_requests': len(requests),
        'request_status': request_status,
        'vehicle_utilization': vehicle_utilization,
        'employee_roles': employee_roles
    })

@analytics.route('/api/analytics/performance')
def performance_analytics():
    """Performance analytics API"""
    # Calculate completion rate
    total_requests = ServiceRequest.query.count()
    completed_requests = ServiceRequest.query.filter_by(status='completed').count()
    completion_rate = (completed_requests / total_requests * 100) if total_requests > 0 else 0
    
    # Calculate average response time (simplified)
    recent_completed = ServiceRequest.query.filter_by(status='completed').order_by(ServiceRequest.completed_at.desc()).limit(10).all()
    avg_response_time = 0
    if recent_completed:
        total_time = sum((req.completed_at - req.created_at).total_seconds() for req in recent_completed if req.completed_at)
        avg_response_time = total_time / len(recent_completed)
    
    # Customer satisfaction (simplified - based on repeat customers)
    customers_with_multiple_requests = db.session.query(ServiceRequest.customer_id).group_by(ServiceRequest.customer_id).having(db.func.count(ServiceRequest.id) > 1).count()
    total_customers = Customer.query.count()
    satisfaction_rate = (customers_with_multiple_requests / total_customers * 100) if total_customers > 0 else 0
    
    return jsonify({
        'completion_rate': completion_rate,
        'avg_response_time': avg_response_time,
        'satisfaction_rate': satisfaction_rate,
        'total_requests': total_requests,
        'completed_requests': completed_requests
    })

@analytics.route('/api/analytics/forecast')
def forecast_analytics():
    """Forecast analytics API"""
    # Simple demand forecasting based on historical data
    requests = ServiceRequest.query.all()
    
    # Group by month
    monthly_requests = {}
    for request in requests:
        month = request.scheduled_date.strftime('%Y-%m')
        if month not in monthly_requests:
            monthly_requests[month] = 0
        monthly_requests[month] += 1
    
    # Calculate trend (simplified)
    if len(monthly_requests) >= 2:
        months = sorted(monthly_requests.keys())
        first_month_count = monthly_requests[months[0]]
        last_month_count = monthly_requests[months[-1]]
        growth_rate = ((last_month_count - first_month_count) / first_month_count * 100) if first_month_count > 0 else 0
    else:
        growth_rate = 0
    
    # Predict next month
    if monthly_requests:
        avg_requests = sum(monthly_requests.values()) / len(monthly_requests)
        predicted_next_month = avg_requests * (1 + growth_rate / 100)
    else:
        predicted_next_month = 0
    
    return jsonify({
        'monthly_requests': monthly_requests,
        'growth_rate': growth_rate,
        'predicted_next_month': predicted_next_month,
        'confidence_level': 0.85
    })

@analytics.route('/api/analytics/comprehensive')
def comprehensive_analytics():
    """Comprehensive analytics combining all metrics"""
    # Get all data
    customers = Customer.query.all()
    requests = ServiceRequest.query.all()
    payments = Payment.query.all()
    vehicles = Vehicle.query.all()
    employees = Employee.query.all()
    
    # Financial metrics
    total_revenue = sum(payment.amount for payment in payments)
    avg_revenue_per_customer = total_revenue / len(customers) if customers else 0
    
    # Operational metrics
    completion_rate = len([r for r in requests if r.status == 'completed']) / len(requests) * 100 if requests else 0
    vehicle_utilization = len([v for v in vehicles if v.status == 'in_use']) / len(vehicles) * 100 if vehicles else 0
    
    # Customer metrics
    customer_retention = len([c for c in customers if len(c.requests) > 1]) / len(customers) * 100 if customers else 0
    
    # Service metrics
    service_type_distribution = {}
    for request in requests:
        service_type = request.service_type
        if service_type not in service_type_distribution:
            service_type_distribution[service_type] = 0
        service_type_distribution[service_type] += 1
    
    return jsonify({
        'financial': {
            'total_revenue': total_revenue,
            'avg_revenue_per_customer': avg_revenue_per_customer,
            'total_payments': len(payments)
        },
        'operational': {
            'completion_rate': completion_rate,
            'vehicle_utilization': vehicle_utilization,
            'total_requests': len(requests),
            'total_vehicles': len(vehicles),
            'total_employees': len(employees)
        },
        'customer': {
            'total_customers': len(customers),
            'customer_retention': customer_retention,
            'customer_types': {c.customer_type: len([c2 for c2 in customers if c2.customer_type == c.customer_type]) for c in customers}
        },
        'service': {
            'service_type_distribution': service_type_distribution,
            'request_status': {r.status: len([r2 for r2 in requests if r2.status == r.status]) for r in requests}
        }
    }) 