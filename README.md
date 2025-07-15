# Garbage Collection & Disposal Firm Management System

A comprehensive Flask web application for managing garbage collection and disposal operations. This system provides tools for customer management, service requests, fleet management, and employee tracking.

## Features

### 🏠 Customer Management
- Add and manage customer information
- Track customer service history
- View customer details and contact information
- Customer search and filtering

### 📋 Service Request Management
- Create and track service requests
- Multiple service types (pickup, disposal, recycling, etc.)
- Status tracking (pending, confirmed, completed, cancelled)
- Scheduled service management

### 🚛 Fleet Management
- Vehicle inventory tracking
- Vehicle status monitoring (available, in use, maintenance)
- Driver assignment
- Capacity and type management

### 👥 Employee Management
- Employee database with roles and departments
- Contact information and status tracking
- Performance monitoring capabilities
- Role-based access control

### 📊 Dashboard & Analytics
- Real-time statistics and metrics
- Service request overview
- Customer and vehicle counts
- Recent activity tracking

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: Bootstrap 5, Font Awesome
- **Styling**: Custom CSS with modern gradients
- **JavaScript**: Vanilla JS for form validation and interactions

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   # Navigate to your project directory
   cd "Gabage collection and disposal firm"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will be ready to use

## Project Structure

```
Gabage collection and disposal firm/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── dashboard.html    # Dashboard with statistics
│   ├── customers.html    # Customer management
│   ├── add_customer.html # Add customer form
│   ├── requests.html     # Service requests
│   ├── add_request.html  # Add service request form
│   ├── vehicles.html     # Fleet management
│   ├── add_vehicle.html  # Add vehicle form
│   ├── employees.html    # Employee management
│   └── add_employee.html # Add employee form
└── garbage_collection.db # SQLite database (created automatically)
```

## Database Models

### Customer
- Personal information (name, email, phone, address)
- Service history tracking
- Registration date

### ServiceRequest
- Customer association
- Service type and description
- Scheduled date and status
- Creation and completion timestamps

### Vehicle
- Vehicle identification and type
- Capacity and status
- Driver assignment
- Maintenance tracking

### Employee
- Personal and contact information
- Role and department assignment
- Employment status
- Performance tracking

## Usage Guide

### Getting Started
1. **Add Customers**: Start by adding customers through the customer management section
2. **Create Service Requests**: Generate service requests for customers
3. **Manage Fleet**: Add vehicles and assign drivers
4. **Track Employees**: Maintain employee database and roles
5. **Monitor Dashboard**: Use the dashboard to track overall operations

### Key Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live statistics and current time display
- **Form Validation**: Client-side and server-side validation
- **Modal Dialogs**: Detailed views without page navigation
- **Status Tracking**: Comprehensive status management for all entities

## API Endpoints

### Web Routes
- `/` - Home page
- `/dashboard` - Main dashboard with statistics
- `/customers` - Customer management
- `/customers/add` - Add new customer
- `/requests` - Service request management
- `/requests/add` - Create new service request
- `/vehicles` - Fleet management
- `/vehicles/add` - Add new vehicle
- `/employees` - Employee management
- `/employees/add` - Add new employee

### API Routes
- `/api/requests` - JSON endpoint for service requests

## Customization

### Adding New Features
1. **Database Models**: Add new models in `app.py`
2. **Routes**: Create new routes for functionality
3. **Templates**: Add corresponding HTML templates
4. **Styling**: Customize CSS in `base.html`

### Configuration
- **Database**: Change SQLite to other databases in `app.py`
- **Secret Key**: Update the secret key for production
- **Port**: Modify the port in `app.py` if needed

## Security Considerations

- **Input Validation**: All forms include validation
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **XSS Protection**: Template escaping in Jinja2
- **CSRF Protection**: Form-based protection

## Future Enhancements

- **User Authentication**: Login system for employees
- **Reporting**: Advanced analytics and reports
- **Notifications**: Email/SMS notifications
- **Mobile App**: Native mobile application
- **Payment Integration**: Billing and payment processing
- **Route Optimization**: GPS and route planning
- **Inventory Management**: Equipment and supplies tracking

## Support

For questions or issues:
1. Check the documentation in this README
2. Review the code comments in `app.py`
3. Test the application functionality
4. Modify templates as needed for your specific requirements

## License

This project is open source and available for educational and commercial use.

---

**EcoClean Garbage Collection & Disposal Firm Management System**
*Professional waste management solutions for modern businesses* 