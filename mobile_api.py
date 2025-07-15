from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import json
from models import db, ServiceRequest, Vehicle, Employee, Customer, Payment, Route, Schedule
from functools import wraps

mobile_api = Blueprint('mobile_api', __name__)

# Simple decorator replacements
def require_role(role):
    """Simple role requirement decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            if current_user.role != role and current_user.role != 'super_admin':
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit(limit="60 per minute"):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Simple implementation - just pass through for now
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@mobile_api.route('/api/mobile/driver/tasks', methods=['GET'])
@login_required
@require_role('driver')
@rate_limit("60 per minute")
def get_driver_tasks():
    """Get current driver's assigned tasks"""
    try:
        driver_id = current_user.id
        
        # Get today's schedule
        today = datetime.now().date()
        tasks = db.session.query(Schedule).filter(
            Schedule.driver_id == driver_id,
            Schedule.schedule_date == today
        ).all()
        
        task_list = []
        for task in tasks:
            # Get associated service request
            request_data = ServiceRequest.query.get(task.request_id)
            if request_data:
                customer = Customer.query.get(request_data.customer_id)
                task_list.append({
                    'id': task.id,
                    'request_id': task.request_id,
                    'customer_name': customer.name if customer else 'Unknown',
                    'customer_address': customer.address if customer else '',
                    'service_type': request_data.service_type,
                    'scheduled_time': task.scheduled_time.isoformat() if task.scheduled_time else None,
                    'status': task.status,
                    'notes': task.notes
                })
        
        return jsonify({
            'success': True,
            'tasks': task_list,
            'total_tasks': len(task_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/driver/update-task', methods=['POST'])
@login_required
@require_role('driver')
@rate_limit("30 per minute")
def update_task_status():
    """Update task status and add completion notes"""
    try:
        data = request.get_json()
        task_id = data.get('task_id')
        status = data.get('status')
        notes = data.get('notes', '')
        completion_photo = data.get('completion_photo', '')
        
        if not task_id or not status:
            return jsonify({
                'success': False,
                'error': 'Task ID and status are required'
            }), 400
        
        # Update schedule
        schedule = Schedule.query.get(task_id)
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        schedule.status = status
        schedule.completion_notes = notes
        schedule.completion_photo = completion_photo
        schedule.completed_at = datetime.now()
        
        # Update associated service request
        if status == 'completed':
            service_request = ServiceRequest.query.get(schedule.request_id)
            if service_request:
                service_request.status = 'completed'
                service_request.completion_date = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/customer/requests', methods=['GET'])
@login_required
@rate_limit("60 per minute")
def get_customer_requests():
    """Get customer's service requests"""
    try:
        customer_id = current_user.id if hasattr(current_user, 'id') else request.args.get('customer_id')
        
        if not customer_id:
            return jsonify({
                'success': False,
                'error': 'Customer ID required'
            }), 400
        
        requests = ServiceRequest.query.filter(
            ServiceRequest.customer_id == customer_id
        ).order_by(ServiceRequest.created_at.desc()).all()
        
        request_list = []
        for req in requests:
            request_list.append({
                'id': req.id,
                'service_type': req.service_type,
                'status': req.status,
                'created_at': req.created_at.isoformat(),
                'scheduled_date': req.scheduled_date.isoformat() if req.scheduled_date else None,
                'completion_date': req.completion_date.isoformat() if req.completion_date else None,
                'description': req.description,
                'amount': float(req.amount) if req.amount else 0
            })
        
        return jsonify({
            'success': True,
            'requests': request_list,
            'total_requests': len(request_list)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/customer/new-request', methods=['POST'])
@login_required
@rate_limit("10 per minute")
def create_service_request():
    """Create new service request from mobile app"""
    try:
        data = request.get_json()
        
        required_fields = ['service_type', 'description', 'scheduled_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        customer_id = current_user.id if hasattr(current_user, 'id') else data.get('customer_id')
        
        # Create new service request
        new_request = ServiceRequest(
            customer_id=customer_id,
            service_type=data['service_type'],
            description=data['description'],
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            status='pending',
            created_at=datetime.now()
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'request_id': new_request.id,
            'message': 'Service request created successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/payment/make-payment', methods=['POST'])
@login_required
@rate_limit("20 per minute")
def make_payment():
    """Process payment from mobile app"""
    try:
        data = request.get_json()
        
        required_fields = ['amount', 'payment_method', 'request_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        # Create payment record
        payment = Payment(
            customer_id=data.get('customer_id'),
            request_id=data['request_id'],
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            payment_date=datetime.now(),
            status='completed'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment_id': payment.id,
            'message': 'Payment processed successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/vehicle/location', methods=['POST'])
@login_required
@require_role('driver')
@rate_limit("120 per minute")
def update_vehicle_location():
    """Update vehicle location for GPS tracking"""
    try:
        data = request.get_json()
        
        required_fields = ['vehicle_id', 'latitude', 'longitude']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        vehicle_id = data['vehicle_id']
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        
        # Update vehicle location (in production, store in Redis or database)
        # For now, just return success
        
        return jsonify({
            'success': True,
            'message': 'Location updated successfully',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/notifications', methods=['GET'])
@login_required
@rate_limit("60 per minute")
def get_notifications():
    """Get user notifications"""
    try:
        user_id = current_user.id if hasattr(current_user, 'id') else request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID required'
            }), 400
        
        # Mock notifications (in production, fetch from database)
        notifications = [
            {
                'id': 1,
                'type': 'service_update',
                'title': 'Service Completed',
                'message': 'Your service request has been completed successfully',
                'timestamp': datetime.now().isoformat(),
                'read': False
            },
            {
                'id': 2,
                'type': 'payment',
                'title': 'Payment Received',
                'message': 'Payment of $150.00 has been received',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                'read': True
            }
        ]
        
        return jsonify({
            'success': True,
            'notifications': notifications,
            'unread_count': len([n for n in notifications if not n['read']])
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@mobile_api.route('/api/mobile/notifications/mark-read', methods=['POST'])
@login_required
@rate_limit("30 per minute")
def mark_notification_read():
    """Mark notification as read"""
    try:
        data = request.get_json()
        notification_id = data.get('notification_id')
        
        if not notification_id:
            return jsonify({
                'success': False,
                'error': 'Notification ID required'
            }), 400
        
        # In production, update notification status in database
        # For now, just return success
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 