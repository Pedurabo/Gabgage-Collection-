#!/usr/bin/env python3
"""
Database initialization script for EcoClean Garbage Collection System
Creates super admin, departments, and sample users with role-based access control
"""

from app import app, db
from models import User, Department, Employee
from auth import create_super_admin, create_departments, create_sample_users
from datetime import datetime, date

def init_database():
    """Initialize database with all required data"""
    print("🚀 Initializing EcoClean Database...")
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create super admin
        create_super_admin()
        print("✅ Super admin created")
        
        # Create departments
        create_departments()
        print("✅ Departments created")
        
        # Create sample users
        create_sample_users()
        print("✅ Sample users created")
        
        # Create additional sample data
        create_sample_employees()
        print("✅ Sample employees created")
        
        print("\n🎉 Database initialization complete!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        print("Super Admin:")
        print("  Username: admin")
        print("  Password: Admin@123")
        print("\nDepartment Admins:")
        print("  Operations Admin:")
        print("    Username: ops_admin")
        print("    Password: Admin@123")
        print("  Fleet Admin:")
        print("    Username: fleet_admin")
        print("    Password: Admin@123")
        print("  Customer Service Admin:")
        print("    Username: cs_admin")
        print("    Password: Admin@123")
        print("\nSample Users:")
        print("  Manager:")
        print("    Username: manager1")
        print("    Password: User@123")
        print("  Drivers:")
        print("    Username: driver1")
        print("    Password: User@123")
        print("    Username: driver2")
        print("    Password: User@123")
        print("\n🔐 Security Features:")
        print("  • Password strength validation")
        print("  • Account lockout after 5 failed attempts")
        print("  • Role-based access control")
        print("  • Department-specific permissions")
        print("  • Session management")
        print("\n🌐 Access URLs:")
        print("  • Main Dashboard: http://localhost:5000/")
        print("  • Login: http://localhost:5000/auth/login")
        print("  • User Management: http://localhost:5000/auth/admin/users")
        print("  • Department Users: http://localhost:5000/auth/department/users")

def create_sample_employees():
    """Create sample employee records"""
    # Get departments
    operations_dept = Department.query.filter_by(name='Operations').first()
    fleet_dept = Department.query.filter_by(name='Fleet Management').first()
    cs_dept = Department.query.filter_by(name='Customer Service').first()
    
    # Sample employees data
    employees_data = [
        {
            'user_id': User.query.filter_by(username='manager1').first().id,
            'employee_id': 'EMP001',
            'position': 'Operations Manager',
            'hire_date': date(2023, 1, 15),
            'salary': 65000.00,
            'department_id': operations_dept.id if operations_dept else None
        },
        {
            'user_id': User.query.filter_by(username='driver1').first().id,
            'employee_id': 'EMP002',
            'position': 'Senior Driver',
            'hire_date': date(2023, 3, 10),
            'salary': 45000.00,
            'department_id': operations_dept.id if operations_dept else None
        },
        {
            'user_id': User.query.filter_by(username='driver2').first().id,
            'employee_id': 'EMP003',
            'position': 'Fleet Driver',
            'hire_date': date(2023, 6, 20),
            'salary': 42000.00,
            'department_id': fleet_dept.id if fleet_dept else None
        }
    ]
    
    for emp_data in employees_data:
        if not Employee.query.filter_by(employee_id=emp_data['employee_id']).first():
            employee = Employee(**emp_data)
            db.session.add(employee)
    
    db.session.commit()

def verify_database():
    """Verify that all data was created correctly"""
    print("\n🔍 Verifying database setup...")
    
    with app.app_context():
        # Check super admin
        admin = User.query.filter_by(role='super_admin').first()
        if admin:
            print(f"✅ Super admin: {admin.username} ({admin.email})")
        else:
            print("❌ Super admin not found")
        
        # Check departments
        departments = Department.query.all()
        print(f"✅ Departments: {len(departments)} created")
        for dept in departments:
            print(f"  • {dept.name}: {dept.description}")
        
        # Check users by role
        roles = ['super_admin', 'department_admin', 'manager', 'driver', 'user']
        for role in roles:
            users = User.query.filter_by(role=role).all()
            print(f"✅ {role.replace('_', ' ').title()}s: {len(users)}")
        
        # Check employees
        employees = Employee.query.all()
        print(f"✅ Employees: {len(employees)} created")
        
        print("\n✅ Database verification complete!")

def reset_database():
    """Reset database (WARNING: This will delete all data)"""
    print("⚠️  WARNING: This will delete all data!")
    response = input("Are you sure you want to reset the database? (yes/no): ")
    
    if response.lower() == 'yes':
        with app.app_context():
            db.drop_all()
            print("🗑️  Database dropped")
            init_database()
            verify_database()
    else:
        print("❌ Database reset cancelled")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            init_database()
            verify_database()
        elif command == 'verify':
            verify_database()
        elif command == 'reset':
            reset_database()
        else:
            print("Usage: python create_admin.py [init|verify|reset]")
            print("  init   - Initialize database with sample data")
            print("  verify - Verify database setup")
            print("  reset  - Reset database (WARNING: deletes all data)")
    else:
        # Default: initialize database
        init_database()
        verify_database() 