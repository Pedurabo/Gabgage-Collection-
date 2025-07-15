from models import db, User, Department, Customer, ServiceRequest, Vehicle, Employee, Payment, Invoice, Contract, PricingPlan, Bill, Schedule, Route, WasteType, Inventory, Notification, ServiceMetrics, CustomerFeedback, MarketAnalysis, EquipmentMaintenance, RouteOptimization, CustomerPortal, Task
from app import app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_sample_data():
    with app.app_context():
        # Create departments
        departments = [
            Department(name='Operations', description='Main operations department', is_active=True),
            Department(name='Maintenance', description='Vehicle and equipment maintenance', is_active=True),
            Department(name='Customer Service', description='Customer support and billing', is_active=True),
            Department(name='Administration', description='Administrative and management', is_active=True)
        ]
        
        for dept in departments:
            db.session.add(dept)
        db.session.commit()
        
        # Create users first
        users_data = [
            {'username': 'admin', 'email': 'admin@ecoclean.com', 'first_name': 'Admin', 'last_name': 'User',
             'role': 'super_admin', 'is_active': True, 'is_verified': True},
            {'username': 'manager1', 'email': 'manager1@ecoclean.com', 'first_name': 'John', 'last_name': 'Manager',
             'role': 'manager', 'department_id': 1, 'is_active': True, 'is_verified': True},
            {'username': 'driver1', 'email': 'driver1@ecoclean.com', 'first_name': 'Mike', 'last_name': 'Driver',
             'role': 'driver', 'department_id': 1, 'is_active': True, 'is_verified': True},
            {'username': 'dept_admin1', 'email': 'dept_admin1@ecoclean.com', 'first_name': 'Sarah', 'last_name': 'Admin',
             'role': 'department_admin', 'department_id': 1, 'is_active': True, 'is_verified': True}
        ]
        
        users = []
        for user_data in users_data:
            user = User()
            for key, value in user_data.items():
                setattr(user, key, value)
            user.set_password('password123')
            users.append(user)
            db.session.add(user)
        db.session.commit()
        
        # Create employees
        employees = [
            Employee(user_id=2, employee_id='EMP001', position='driver', hire_date=datetime.now().date() - timedelta(days=365),
                    salary=45000, department_id=1, is_active=True),
            Employee(user_id=3, employee_id='EMP002', position='collector', hire_date=datetime.now().date() - timedelta(days=180),
                    salary=38000, department_id=1, is_active=True),
            Employee(user_id=4, employee_id='EMP003', position='supervisor', hire_date=datetime.now().date() - timedelta(days=730),
                    salary=55000, department_id=1, is_active=True)
        ]
        
        for emp in employees:
            db.session.add(emp)
        db.session.commit()
        
        # Create customers
        customers = [
            Customer(name='Downtown Office Complex', email='contact@downtownoffice.com', 
                    phone='555-0201', address='123 Main St, Downtown', customer_type='commercial',
                    service_frequency='daily', created_by=1),
            Customer(name='Green Valley Apartments', email='manager@greenvalley.com',
                    phone='555-0202', address='456 Oak Ave, Green Valley', customer_type='residential',
                    service_frequency='weekly', created_by=1),
            Customer(name='Industrial Park Factory', email='operations@industrialpark.com',
                    phone='555-0203', address='789 Industrial Blvd, Factory District', customer_type='industrial',
                    service_frequency='daily', created_by=1),
            Customer(name='Shopping Mall Center', email='admin@shoppingmall.com',
                    phone='555-0204', address='321 Retail Rd, Shopping District', customer_type='commercial',
                    service_frequency='daily', created_by=1),
            Customer(name='Residential Community', email='hoa@residentialcommunity.com',
                    phone='555-0205', address='654 Community Dr, Suburban Area', customer_type='residential',
                    service_frequency='weekly', created_by=1)
        ]
        
        for cust in customers:
            db.session.add(cust)
        db.session.commit()
        
        # Create vehicles
        vehicles = [
            Vehicle(vehicle_number='TRK-001', vehicle_type='garbage_truck', capacity='5 tons',
                   fuel_type='diesel', status='available', department_id=1, assigned_driver_id=2),
            Vehicle(vehicle_number='TRK-002', vehicle_type='recycling_truck', capacity='8 tons',
                   fuel_type='diesel', status='available', department_id=1, assigned_driver_id=3),
            Vehicle(vehicle_number='VAN-001', vehicle_type='pickup_truck', capacity='1 ton',
                   fuel_type='gas', status='available', department_id=1),
            Vehicle(vehicle_number='TRK-003', vehicle_type='garbage_truck', capacity='6 tons',
                   fuel_type='diesel', status='maintenance', department_id=1)
        ]
        
        for veh in vehicles:
            db.session.add(veh)
        db.session.commit()
        
        # Create waste types
        waste_types = [
            WasteType(name='General Waste', description='Regular household and office waste',
                     disposal_method='Landfill', hazardous=False),
            WasteType(name='Recyclable Paper', description='Paper, cardboard, newspapers',
                     disposal_method='Recycling Center', hazardous=False),
            WasteType(name='Plastic Waste', description='Plastic bottles, containers, packaging',
                     disposal_method='Recycling Center', hazardous=False),
            WasteType(name='Hazardous Waste', description='Chemicals, batteries, electronics',
                     disposal_method='Specialized Facility', hazardous=True),
            WasteType(name='Organic Waste', description='Food waste, garden waste, compostable materials',
                     disposal_method='Composting Facility', hazardous=False)
        ]
        
        for waste in waste_types:
            db.session.add(waste)
        db.session.commit()
        
        # Create pricing plans
        pricing_plans = [
            PricingPlan(name='Basic Residential', description='Weekly collection for residential customers',
                       price=150.0, frequency='weekly', service_type='residential', is_active=True, created_by=1),
            PricingPlan(name='Premium Residential', description='Daily collection with recycling',
                       price=300.0, frequency='daily', service_type='residential', is_active=True, created_by=1),
            PricingPlan(name='Commercial Standard', description='Daily collection for commercial properties',
                       price=500.0, frequency='daily', service_type='commercial', is_active=True, created_by=1),
            PricingPlan(name='Industrial Premium', description='Specialized industrial waste management',
                       price=1000.0, frequency='daily', service_type='commercial', is_active=True, created_by=1),
            PricingPlan(name='Eco-Friendly Package', description='Full recycling and composting service',
                       price=400.0, frequency='weekly', service_type='residential', is_active=True, created_by=1)
        ]
        
        for plan in pricing_plans:
            db.session.add(plan)
        db.session.commit()
        
        # Create contracts
        contracts = [
            Contract(customer_id=1, contract_number='CON-2024-001', contract_type='commercial',
                    start_date=datetime.now().date(), end_date=datetime.now().date() + timedelta(days=365),
                    monthly_fee=1500.0, status='active', created_by=1),
            Contract(customer_id=2, contract_number='CON-2024-002', contract_type='residential',
                    start_date=datetime.now().date() - timedelta(days=30), end_date=datetime.now().date() + timedelta(days=335),
                    monthly_fee=150.0, status='active', created_by=1),
            Contract(customer_id=3, contract_number='CON-2024-003', contract_type='industrial',
                    start_date=datetime.now().date() - timedelta(days=60), end_date=datetime.now().date() + timedelta(days=305),
                    monthly_fee=3000.0, status='active', created_by=1),
            Contract(customer_id=4, contract_number='CON-2024-004', contract_type='commercial',
                    start_date=datetime.now().date() - timedelta(days=15), end_date=datetime.now().date() + timedelta(days=350),
                    monthly_fee=1500.0, status='active', created_by=1),
            Contract(customer_id=5, contract_number='CON-2024-005', contract_type='residential',
                    start_date=datetime.now().date() - timedelta(days=45), end_date=datetime.now().date() + timedelta(days=320),
                    monthly_fee=300.0, status='active', created_by=1)
        ]
        
        for contract in contracts:
            db.session.add(contract)
        db.session.commit()
        
        # Create invoices
        invoices = [
            Invoice(customer_id=1, invoice_number='INV-2024-001', amount=500.0, tax_amount=50.0,
                   total_amount=550.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1),
            Invoice(customer_id=2, invoice_number='INV-2024-002', amount=150.0, tax_amount=15.0,
                   total_amount=165.0, status='paid', due_date=datetime.now().date(), paid_date=datetime.now().date() - timedelta(days=5), created_by=1),
            Invoice(customer_id=3, invoice_number='INV-2024-003', amount=1000.0, tax_amount=100.0,
                   total_amount=1100.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1),
            Invoice(customer_id=4, invoice_number='INV-2024-004', amount=500.0, tax_amount=50.0,
                   total_amount=550.0, status='overdue', due_date=datetime.now().date() + timedelta(days=15), created_by=1),
            Invoice(customer_id=5, invoice_number='INV-2024-005', amount=300.0, tax_amount=30.0,
                   total_amount=330.0, status='pending', due_date=datetime.now().date() + timedelta(days=30), created_by=1)
        ]
        
        for invoice in invoices:
            db.session.add(invoice)
        db.session.commit()
        
        # Create service requests
        service_requests = [
            ServiceRequest(customer_id=1, service_type='commercial', scheduled_date=datetime.now().date() + timedelta(days=1),
                         status='confirmed', description='Daily collection service', amount=500.0, created_by=1, assigned_to=2, department_id=1),
            ServiceRequest(customer_id=2, service_type='residential', scheduled_date=datetime.now().date() + timedelta(days=7),
                         status='pending', description='Weekly collection service', amount=150.0, created_by=1, assigned_to=3, department_id=1),
            ServiceRequest(customer_id=3, service_type='industrial', scheduled_date=datetime.now().date() + timedelta(days=1),
                         status='confirmed', description='Industrial waste collection', amount=1000.0, created_by=1, assigned_to=2, department_id=1),
            ServiceRequest(customer_id=4, service_type='commercial', scheduled_date=datetime.now().date() + timedelta(days=1),
                         status='in_progress', description='Daily collection service', amount=500.0, created_by=1, assigned_to=3, department_id=1),
            ServiceRequest(customer_id=5, service_type='residential', scheduled_date=datetime.now().date() + timedelta(days=7),
                         status='pending', description='Weekly collection service', amount=300.0, created_by=1, assigned_to=2, department_id=1)
        ]
        
        for req in service_requests:
            db.session.add(req)
        db.session.commit()
        
        # Create payments
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
        
        # Create bills
        bills = [
            Bill(customer_id=1, bill_number='BILL-2024-001', amount=500.0, due_date=datetime.now().date() + timedelta(days=30),
                 status='pending', created_by=1),
            Bill(customer_id=2, bill_number='BILL-2024-002', amount=150.0, due_date=datetime.now().date(),
                 status='paid', created_by=1),
            Bill(customer_id=3, bill_number='BILL-2024-003', amount=1000.0, due_date=datetime.now().date() + timedelta(days=30),
                 status='pending', created_by=1)
        ]
        
        for bill in bills:
            db.session.add(bill)
        db.session.commit()
        
        # Create routes
        routes = [
            Route(name='Downtown Route', description='Main downtown collection route',
                  start_location='Warehouse', end_location='Downtown', estimated_duration=240,
                  distance=25.0, is_active=True, created_by=1, department_id=1),
            Route(name='Suburban Route', description='Residential area collection route',
                  start_location='Warehouse', end_location='Suburban Area', estimated_duration=180,
                  distance=20.0, is_active=True, created_by=1, department_id=1),
            Route(name='Industrial Route', description='Industrial area collection route',
                  start_location='Warehouse', end_location='Industrial Park', estimated_duration=300,
                  distance=35.0, is_active=True, created_by=1, department_id=1)
        ]
        
        for route in routes:
            db.session.add(route)
        db.session.commit()
        
        # Create schedules
        schedules = [
            Schedule(request_id=1, driver_id=2, vehicle_id=1, scheduled_date=datetime.now().date() + timedelta(days=1),
                    scheduled_time=datetime.strptime('08:00', '%H:%M').time(), status='scheduled', created_by=1),
            Schedule(request_id=2, driver_id=3, vehicle_id=2, scheduled_date=datetime.now().date() + timedelta(days=7),
                    scheduled_time=datetime.strptime('09:00', '%H:%M').time(), status='scheduled', created_by=1),
            Schedule(request_id=3, driver_id=2, vehicle_id=1, scheduled_date=datetime.now().date() + timedelta(days=1),
                    scheduled_time=datetime.strptime('10:00', '%H:%M').time(), status='scheduled', created_by=1)
        ]
        
        for schedule in schedules:
            db.session.add(schedule)
        db.session.commit()
        
        # Create inventory
        inventory_items = [
            Inventory(item_name='Safety Gloves', description='Heavy-duty safety gloves', quantity=100,
                     unit_price=15.0, supplier='Safety Supply Co', reorder_level=20, department_id=1, created_by=1),
            Inventory(item_name='Trash Bags', description='Large trash bags', quantity=500,
                     unit_price=25.0, supplier='Bag Supply Inc', reorder_level=100, department_id=1, created_by=1),
            Inventory(item_name='Fuel Filters', description='Diesel fuel filters', quantity=50,
                     unit_price=45.0, supplier='Auto Parts Co', reorder_level=10, department_id=2, created_by=1),
            Inventory(item_name='Tire Chains', description='Winter tire chains', quantity=20,
                     unit_price=120.0, supplier='Tire Supply', reorder_level=5, department_id=2, created_by=1)
        ]
        
        for item in inventory_items:
            db.session.add(item)
        db.session.commit()
        
        # Create notifications
        notifications = [
            Notification(user_id=1, title='New Service Request', message='New service request received for Downtown Office Complex',
                       notification_type='info', is_read=False),
            Notification(user_id=2, title='Vehicle Maintenance Due', message='Vehicle TRK-003 requires maintenance',
                       notification_type='warning', is_read=False),
            Notification(user_id=3, title='Route Assignment', message='You have been assigned to Downtown Route',
                       notification_type='info', is_read=False)
        ]
        
        for notification in notifications:
            db.session.add(notification)
        db.session.commit()
        
        # Create service metrics
        service_metrics = [
            ServiceMetrics(department_id=1, metric_date=datetime.now().date() - timedelta(days=1),
                         total_requests=25, completed_requests=23, average_response_time=2.5,
                         customer_satisfaction=4.2),
            ServiceMetrics(department_id=1, metric_date=datetime.now().date() - timedelta(days=7),
                         total_requests=150, completed_requests=145, average_response_time=2.8,
                         customer_satisfaction=4.1),
            ServiceMetrics(department_id=1, metric_date=datetime.now().date() - timedelta(days=30),
                         total_requests=600, completed_requests=580, average_response_time=2.3,
                         customer_satisfaction=4.3)
        ]
        
        for metric in service_metrics:
            db.session.add(metric)
        db.session.commit()
        
        # Create customer feedback
        customer_feedback = [
            CustomerFeedback(customer_id=1, service_request_id=1, rating=4,
                           feedback_type='service', comment='Excellent service, always on time'),
            CustomerFeedback(customer_id=2, service_request_id=2, rating=5,
                           feedback_type='quality', comment='Very satisfied with recycling service'),
            CustomerFeedback(customer_id=3, service_request_id=3, rating=4,
                           feedback_type='driver', comment='Professional and courteous driver')
        ]
        
        for feedback in customer_feedback:
            db.session.add(feedback)
        db.session.commit()
        
        # Create market analysis
        market_analysis = [
            MarketAnalysis(analysis_date=datetime.now().date(), market_segment='residential',
                         customer_growth=12.5, revenue_growth=15.2, competitor_analysis='Strong competition in residential segment',
                         market_trends='Increasing demand for recycling services', created_by=1),
            MarketAnalysis(analysis_date=datetime.now().date(), market_segment='commercial',
                         customer_growth=8.3, revenue_growth=10.7, competitor_analysis='Moderate competition in commercial segment',
                         market_trends='Growing demand for sustainable waste management', created_by=1),
            MarketAnalysis(analysis_date=datetime.now().date(), market_segment='industrial',
                         customer_growth=5.1, revenue_growth=18.9, competitor_analysis='Limited competition in industrial segment',
                         market_trends='High-value contracts in industrial waste management', created_by=1)
        ]
        
        for analysis in market_analysis:
            db.session.add(analysis)
        db.session.commit()
        
        # Create equipment maintenance
        equipment_maintenance = [
            EquipmentMaintenance(vehicle_id=4, maintenance_type='preventive', description='Regular oil change and filter replacement',
                               cost=250.0, scheduled_date=datetime.now().date() + timedelta(days=7),
                               status='scheduled', technician='Mike Johnson', created_by=1),
            EquipmentMaintenance(vehicle_id=1, maintenance_type='corrective', description='Brake system repair',
                               cost=800.0, scheduled_date=datetime.now().date() + timedelta(days=1),
                               status='in_progress', technician='John Smith', created_by=1),
            EquipmentMaintenance(vehicle_id=2, maintenance_type='preventive', description='Tire rotation and inspection',
                               cost=150.0, scheduled_date=datetime.now().date() + timedelta(days=14),
                               status='scheduled', technician='Mike Johnson', created_by=1)
        ]
        
        for maintenance in equipment_maintenance:
            db.session.add(maintenance)
        db.session.commit()
        
        # Create route optimizations
        route_optimizations = [
            RouteOptimization(route_id=1, optimization_date=datetime.now(), original_distance=25.0,
                            optimized_distance=22.5, time_saved=30, fuel_saved=5.2, algorithm_used='TSP', created_by=1),
            RouteOptimization(route_id=2, optimization_date=datetime.now(), original_distance=20.0,
                            optimized_distance=18.8, time_saved=25, fuel_saved=3.8, algorithm_used='Clustering', created_by=1),
            RouteOptimization(route_id=3, optimization_date=datetime.now(), original_distance=35.0,
                            optimized_distance=32.1, time_saved=45, fuel_saved=7.5, algorithm_used='TSP', created_by=1)
        ]
        
        for optimization in route_optimizations:
            db.session.add(optimization)
        db.session.commit()
        
        # Create sample tasks
        tasks = [
            Task(
                title='Vehicle Maintenance - Truck #001',
                description='Perform routine maintenance on garbage truck #001 including oil change, tire rotation, and brake inspection.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=2),
                assigned_to_id=3,  # driver1
                created_by_id=2,   # manager1
                department_id=1,
                vehicle_id=1
            ),
            Task(
                title='Customer Complaint Resolution',
                description='Follow up on customer complaint regarding missed pickup at 123 Main St. Contact customer and reschedule.',
                priority='urgent',
                status='in_progress',
                due_date=datetime.now().date() + timedelta(days=1),
                assigned_to_id=2,  # manager1
                created_by_id=1,   # admin
                department_id=1,
                service_request_id=1
            ),
            Task(
                title='Route Optimization Analysis',
                description='Analyze current routes and optimize for fuel efficiency and time savings. Generate report with recommendations.',
                priority='normal',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=7),
                assigned_to_id=2,  # manager1
                created_by_id=1,   # admin
                department_id=1
            ),
            Task(
                title='Inventory Restock',
                description='Check inventory levels and order necessary supplies including safety equipment, cleaning materials, and spare parts.',
                priority='normal',
                status='completed',
                due_date=datetime.now().date() - timedelta(days=1),
                assigned_to_id=4,  # dept_admin1
                created_by_id=4,   # dept_admin1
                department_id=1,
                completed_at=datetime.now() - timedelta(hours=6)
            ),
            Task(
                title='Driver Training Session',
                description='Conduct safety training session for new drivers. Cover defensive driving, waste handling procedures, and emergency protocols.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=5),
                assigned_to_id=2,  # manager1
                created_by_id=1,   # admin
                department_id=1
            ),
            Task(
                title='Equipment Repair - Compactor',
                description='Repair hydraulic system on waste compactor. Parts have been ordered and should arrive tomorrow.',
                priority='urgent',
                status='in_progress',
                due_date=datetime.now().date() + timedelta(days=1),
                assigned_to_id=3,  # driver1
                created_by_id=2,   # manager1
                department_id=2
            ),
            Task(
                title='Monthly Report Preparation',
                description='Compile monthly operational report including service metrics, customer satisfaction scores, and financial summary.',
                priority='normal',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=3),
                assigned_to_id=4,  # dept_admin1
                created_by_id=1,   # admin
                department_id=1
            ),
            Task(
                title='Customer Site Visit',
                description='Visit new commercial customer to assess waste management needs and provide customized service proposal.',
                priority='high',
                status='pending',
                due_date=datetime.now().date() + timedelta(days=4),
                assigned_to_id=2,  # manager1
                created_by_id=1,   # admin
                department_id=1
            )
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        print("Sample tasks created successfully!")
        
        print("Sample data created successfully!") 