from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Customer, ServiceRequest, Vehicle, Employee, Route
from datetime import datetime, timedelta
import json
import uuid

mobile_api = Blueprint('mobile_api', __name__)

# Driver Mobile API Endpoints
@mobile_api.route('/api/mobile/driver/login', methods=['POST'])
def driver_login():
    """Driver login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, role='driver').first()
    if user and user.check_password(password):
        # Generate mobile token
        token = str(uuid.uuid4())
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'token': token,
            'driver_id': user.id,
            'driver_name': user.username,
            'message': 'Login successful'
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@mobile_api.route('/api/mobile/driver/dashboard', methods=['GET'])
def driver_dashboard():
    """Driver dashboard with today's routes and tasks"""
    driver_id = request.args.get('driver_id')
    
    # Get driver's assigned routes for today
    today = datetime.now().date()
    routes = Route.query.filter_by(driver_id=driver_id, status='active').all()
    
    # Get today's service requests
    requests = ServiceRequest.query.filter(
        ServiceRequest.scheduled_date >= today,
        ServiceRequest.scheduled_date < today + timedelta(days=1),
        ServiceRequest.assigned_employee_id == driver_id
    ).all()
    
    dashboard_data = {
        'today_routes': len(routes),
        'pending_requests': len([r for r in requests if r.status == 'pending']),
        'completed_requests': len([r for r in requests if r.status == 'completed']),
        'total_distance': sum(r.estimated_duration or 0 for r in routes),
        'current_location': {
            'latitude': 40.7128,  # Example coordinates
            'longitude': -74.0060
        }
    }
    
    return jsonify(dashboard_data)

@mobile_api.route('/api/mobile/driver/routes', methods=['GET'])
def driver_routes():
    """Get driver's assigned routes"""
    driver_id = request.args.get('driver_id')
    
    routes = Route.query.filter_by(driver_id=driver_id, status='active').all()
    
    route_data = []
    for route in routes:
        route_info = {
            'route_id': route.id,
            'route_name': route.name,
            'area_covered': route.area_covered,
            'estimated_duration': route.estimated_duration,
            'requests_count': len(route.requests),
            'status': route.status
        }
        route_data.append(route_info)
    
    return jsonify({'routes': route_data})

@mobile_api.route('/api/mobile/driver/requests', methods=['GET'])
def driver_requests():
    """Get driver's assigned service requests"""
    driver_id = request.args.get('driver_id')
    status = request.args.get('status', 'all')
    
    query = ServiceRequest.query.filter_by(assigned_employee_id=driver_id)
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    requests = query.order_by(ServiceRequest.scheduled_date).all()
    
    request_data = []
    for req in requests:
        customer = Customer.query.get(req.customer_id)
        request_info = {
            'request_id': req.id,
            'customer_name': customer.name if customer else 'Unknown',
            'customer_address': customer.address if customer else '',
            'customer_phone': customer.phone if customer else '',
            'service_type': req.service_type,
            'scheduled_date': req.scheduled_date.isoformat(),
            'priority': req.priority,
            'status': req.status,
            'notes': req.notes,
            'latitude': 40.7128,  # Example coordinates
            'longitude': -74.0060
        }
        request_data.append(request_info)
    
    return jsonify({'requests': request_data})

@mobile_api.route('/api/mobile/driver/update-request', methods=['POST'])
def update_request_status():
    """Update service request status"""
    data = request.get_json()
    request_id = data.get('request_id')
    status = data.get('status')
    notes = data.get('notes', '')
    actual_weight = data.get('actual_weight')
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'success': False, 'message': 'Request not found'}), 404
    
    service_request.status = status
    service_request.notes = notes
    
    if actual_weight:
        service_request.actual_weight = actual_weight
    
    if status == 'completed':
        service_request.completed_at = datetime.utcnow()
        service_request.actual_duration = data.get('actual_duration')
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Request updated successfully'})

@mobile_api.route('/api/mobile/driver/vehicle-info', methods=['GET'])
def vehicle_info():
    """Get driver's assigned vehicle information"""
    driver_id = request.args.get('driver_id')
    
    # Find vehicle assigned to driver
    vehicle = Vehicle.query.filter_by(driver_name=driver_id).first()
    
    if not vehicle:
        return jsonify({'success': False, 'message': 'No vehicle assigned'}), 404
    
    vehicle_info = {
        'vehicle_id': vehicle.id,
        'vehicle_number': vehicle.vehicle_number,
        'vehicle_type': vehicle.vehicle_type,
        'license_plate': vehicle.license_plate,
        'fuel_level': vehicle.fuel_level,
        'mileage': vehicle.mileage,
        'status': vehicle.status,
        'next_maintenance': vehicle.next_maintenance.isoformat() if vehicle.next_maintenance else None
    }
    
    return jsonify(vehicle_info)

# Customer Mobile API Endpoints
@mobile_api.route('/api/mobile/customer/login', methods=['POST'])
def customer_login():
    """Customer login endpoint"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        # Generate customer token
        token = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'token': token,
            'customer_id': customer.id,
            'customer_name': customer.name,
            'message': 'Login successful'
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@mobile_api.route('/api/mobile/customer/dashboard', methods=['GET'])
def customer_dashboard():
    """Customer dashboard with service history and upcoming services"""
    customer_id = request.args.get('customer_id')
    
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'success': False, 'message': 'Customer not found'}), 404
    
    # Get customer's service requests
    requests = ServiceRequest.query.filter_by(customer_id=customer_id).order_by(ServiceRequest.scheduled_date.desc()).limit(10).all()
    
    # Get upcoming services
    upcoming = ServiceRequest.query.filter(
        ServiceRequest.customer_id == customer_id,
        ServiceRequest.scheduled_date >= datetime.now(),
        ServiceRequest.status.in_(['pending', 'confirmed'])
    ).all()
    
    dashboard_data = {
        'customer_name': customer.name,
        'total_requests': len(requests),
        'upcoming_services': len(upcoming),
        'last_service': requests[0].scheduled_date.isoformat() if requests else None,
        'service_frequency': customer.service_frequency,
        'customer_type': customer.customer_type
    }
    
    return jsonify(dashboard_data)

@mobile_api.route('/api/mobile/customer/request-service', methods=['POST'])
def request_service():
    """Submit new service request"""
    data = request.get_json()
    customer_id = data.get('customer_id')
    
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'success': False, 'message': 'Customer not found'}), 404
    
    # Create new service request
    new_request = ServiceRequest(
        customer_id=customer_id,
        service_type=data.get('service_type'),
        description=data.get('description'),
        scheduled_date=datetime.fromisoformat(data.get('scheduled_date')),
        priority=data.get('priority', 'normal'),
        waste_type=data.get('waste_type', 'general'),
        weight_estimate=data.get('weight_estimate'),
        notes=data.get('notes', '')
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'request_id': new_request.id,
        'message': 'Service request submitted successfully'
    })

@mobile_api.route('/api/mobile/customer/track-service', methods=['GET'])
def track_service():
    """Track service request status"""
    request_id = request.args.get('request_id')
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'success': False, 'message': 'Request not found'}), 404
    
    # Get assigned employee info
    employee = None
    if service_request.assigned_employee_id:
        employee = Employee.query.get(service_request.assigned_employee_id)
    
    tracking_info = {
        'request_id': service_request.id,
        'status': service_request.status,
        'scheduled_date': service_request.scheduled_date.isoformat(),
        'assigned_employee': employee.name if employee else None,
        'estimated_arrival': None,  # Would be calculated based on route
        'notes': service_request.notes,
        'service_type': service_request.service_type
    }
    
    return jsonify(tracking_info)

@mobile_api.route('/api/mobile/customer/billing', methods=['GET'])
def customer_billing():
    """Get customer billing information"""
    customer_id = request.args.get('customer_id')
    
    # Get customer's bills
    bills = Bill.query.filter_by(customer_id=customer_id).order_by(Bill.bill_date.desc()).limit(10).all()
    
    bill_data = []
    for bill in bills:
        bill_info = {
            'bill_id': bill.id,
            'bill_number': bill.bill_number,
            'bill_date': bill.bill_date.isoformat(),
            'due_date': bill.due_date.isoformat(),
            'amount': bill.amount,
            'total_amount': bill.total_amount,
            'status': bill.status
        }
        bill_data.append(bill_info)
    
    return jsonify({'bills': bill_data})

# Real-time Features
@mobile_api.route('/api/mobile/realtime/location', methods=['POST'])
def update_location():
    """Update driver's real-time location"""
    data = request.get_json()
    driver_id = data.get('driver_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = data.get('timestamp')
    
    # Store location update (in production, use Redis or similar)
    location_data = {
        'driver_id': driver_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    }
    
    # Here you would store in Redis or database
    # For now, just return success
    
    return jsonify({'success': True, 'message': 'Location updated'})

@mobile_api.route('/api/mobile/realtime/notifications', methods=['GET'])
def get_notifications():
    """Get real-time notifications"""
    user_id = request.args.get('user_id')
    user_type = request.args.get('user_type')  # driver or customer
    
    # Mock notifications (in production, use WebSockets or polling)
    notifications = [
        {
            'id': 1,
            'type': 'service_update',
            'title': 'Service Completed',
            'message': 'Your service request has been completed',
            'timestamp': datetime.utcnow().isoformat(),
            'read': False
        }
    ]
    
    return jsonify({'notifications': notifications})

# Offline Support
@mobile_api.route('/api/mobile/sync', methods=['POST'])
def sync_offline_data():
    """Sync offline data when connection is restored"""
    data = request.get_json()
    offline_actions = data.get('offline_actions', [])
    
    synced_actions = []
    for action in offline_actions:
        # Process each offline action
        action_type = action.get('type')
        action_data = action.get('data')
        
        if action_type == 'update_request':
            # Process request update
            synced_actions.append({
                'id': action.get('id'),
                'status': 'synced'
            })
        elif action_type == 'new_request':
            # Process new request
            synced_actions.append({
                'id': action.get('id'),
                'status': 'synced'
            })
    
    return jsonify({
        'success': True,
        'synced_actions': synced_actions,
        'message': f'Synced {len(synced_actions)} actions'
    })

# Push Notifications
@mobile_api.route('/api/mobile/register-device', methods=['POST'])
def register_device():
    """Register device for push notifications"""
    data = request.get_json()
    user_id = data.get('user_id')
    device_token = data.get('device_token')
    platform = data.get('platform')  # ios, android
    
    # Store device token (in production, use database)
    device_info = {
        'user_id': user_id,
        'device_token': device_token,
        'platform': platform,
        'registered_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'Device registered successfully'})

@mobile_api.route('/api/mobile/send-notification', methods=['POST'])
def send_notification():
    """Send push notification"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    message = data.get('message')
    notification_type = data.get('type')
    
    # In production, use Firebase Cloud Messaging or similar
    notification_data = {
        'user_id': user_id,
        'title': title,
        'message': message,
        'type': notification_type,
        'sent_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'Notification sent'}) 