from models import db, Task, User, Department, ServiceRequest, Vehicle
from app import app
from datetime import datetime, timedelta

def add_sample_tasks():
    with app.app_context():
        # Get existing users and departments
        users = User.query.all()
        departments = Department.query.all()
        service_requests = ServiceRequest.query.all()
        vehicles = Vehicle.query.all()
        
        if not users or not departments:
            print("Error: No users or departments found. Please run the main sample data script first.")
            return
        
        # Create sample tasks
        tasks = [
            Task(
                title='Vehicle Maintenance - Truck #001',
                description='Perform routine maintenance on garbage truck #001 including oil change, tire rotation, and brake inspection.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=2),
                assigned_to_id=users[2].id if len(users) > 2 else users[0].id,  # driver1
                created_by_id=users[1].id if len(users) > 1 else users[0].id,   # manager1
                department_id=departments[0].id,
                vehicle_id=vehicles[0].id if vehicles else None
            ),
            Task(
                title='Customer Complaint Resolution',
                description='Follow up on customer complaint regarding missed pickup at 123 Main St. Contact customer and reschedule.',
                priority='urgent',
                status='in_progress',
                due_date=datetime.now().date() + timedelta(days=1),
                assigned_to_id=users[1].id if len(users) > 1 else users[0].id,  # manager1
                created_by_id=users[0].id,   # admin
                department_id=departments[0].id,
                service_request_id=service_requests[0].id if service_requests else None
            ),
            Task(
                title='Route Optimization Analysis',
                description='Analyze current routes and optimize for fuel efficiency and time savings. Generate report with recommendations.',
                priority='normal',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=7),
                assigned_to_id=users[1].id if len(users) > 1 else users[0].id,  # manager1
                created_by_id=users[0].id,   # admin
                department_id=departments[0].id
            ),
            Task(
                title='Inventory Restock',
                description='Check inventory levels and order necessary supplies including safety equipment, cleaning materials, and spare parts.',
                priority='normal',
                status='completed',
                due_date=datetime.now().date() - timedelta(days=1),
                assigned_to_id=users[3].id if len(users) > 3 else users[0].id,  # dept_admin1
                created_by_id=users[3].id if len(users) > 3 else users[0].id,   # dept_admin1
                department_id=departments[0].id,
                completed_at=datetime.now() - timedelta(hours=6)
            ),
            Task(
                title='Driver Training Session',
                description='Conduct safety training session for new drivers. Cover defensive driving, waste handling procedures, and emergency protocols.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=5),
                assigned_to_id=users[1].id if len(users) > 1 else users[0].id,  # manager1
                created_by_id=users[0].id,   # admin
                department_id=departments[0].id
            ),
            Task(
                title='Equipment Repair - Compactor',
                description='Repair hydraulic system on waste compactor. Parts have been ordered and should arrive tomorrow.',
                priority='urgent',
                status='in_progress',
                due_date=datetime.now().date() + timedelta(days=1),
                assigned_to_id=users[2].id if len(users) > 2 else users[0].id,  # driver1
                created_by_id=users[1].id if len(users) > 1 else users[0].id,   # manager1
                department_id=departments[1].id if len(departments) > 1 else departments[0].id
            ),
            Task(
                title='Monthly Report Preparation',
                description='Compile monthly operational report including service metrics, customer satisfaction scores, and financial summary.',
                priority='normal',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=3),
                assigned_to_id=users[3].id if len(users) > 3 else users[0].id,  # dept_admin1
                created_by_id=users[0].id,   # admin
                department_id=departments[0].id
            ),
            Task(
                title='Customer Site Visit',
                description='Visit new commercial customer to assess waste management needs and provide customized service proposal.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=4),
                assigned_to_id=users[1].id if len(users) > 1 else users[0].id,  # manager1
                created_by_id=users[0].id,   # admin
                department_id=departments[0].id
            )
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        print(f"Successfully created {len(tasks)} sample tasks!")

if __name__ == '__main__':
    add_sample_tasks() 