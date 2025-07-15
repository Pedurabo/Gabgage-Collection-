from app import app, db
from models import User, Department

with app.app_context():
    try:
        # Test database connection
        print("Testing database connection...")
        users = User.query.all()
        print(f"Found {len(users)} users in database")
        
        departments = Department.query.all()
        print(f"Found {len(departments)} departments in database")
        
        # Test if we can create a user
        print("Database is working properly!")
        
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc() 