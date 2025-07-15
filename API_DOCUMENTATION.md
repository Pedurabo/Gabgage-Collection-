# EcoClean API Documentation

## Overview
The EcoClean API provides comprehensive endpoints for managing garbage collection and disposal operations. This RESTful API supports all core business functions including customer management, service requests, fleet management, and employee tracking.

## Base URL
```
http://localhost:5000/api
```

## Authentication
All API endpoints require authentication using session-based authentication. Users must be logged in to access protected endpoints.

## Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login |
| GET | `/auth/logout` | User logout |
| GET | `/auth/profile` | User profile |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | Get all customers |
| POST | `/customers` | Create new customer |
| GET | `/customers/{id}` | Get customer details |
| PUT | `/customers/{id}` | Update customer |
| DELETE | `/customers/{id}` | Delete customer |

### Service Requests
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/requests` | Get all service requests |
| POST | `/requests` | Create new service request |
| GET | `/requests/{id}` | Get request details |
| PUT | `/requests/{id}` | Update request status |
| DELETE | `/requests/{id}` | Delete request |

### Vehicles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vehicles` | Get all vehicles |
| POST | `/vehicles` | Add new vehicle |
| GET | `/vehicles/{id}` | Get vehicle details |
| PUT | `/vehicles/{id}` | Update vehicle |
| DELETE | `/vehicles/{id}` | Delete vehicle |

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| POST | `/employees` | Add new employee |
| GET | `/employees/{id}` | Get employee details |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |

### Departments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/departments` | Get all departments |
| POST | `/departments` | Create new department |
| GET | `/departments/{id}` | Get department details |
| PUT | `/departments/{id}` | Update department |
| DELETE | `/departments/{id}` | Delete department |

### Maintenance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/maintenance` | Get all maintenance records |
| POST | `/maintenance` | Add maintenance record |
| GET | `/maintenance/{id}` | Get maintenance details |
| PUT | `/maintenance/{id}` | Update maintenance record |
| DELETE | `/maintenance/{id}` | Delete maintenance record |

## Request/Response Examples

### Create Customer
```http
POST /api/customers
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St, City, State",
  "customer_type": "residential",
  "service_frequency": "weekly"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St, City, State",
  "customer_type": "residential",
  "service_frequency": "weekly",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Create Service Request
```http
POST /api/requests
Content-Type: application/json

{
  "customer_id": 1,
  "service_type": "pickup",
  "description": "Regular garbage pickup",
  "scheduled_date": "2024-01-20",
  "priority": "normal",
  "estimated_duration": 2.5
}
```

**Response:**
```json
{
  "id": 1,
  "customer_id": 1,
  "service_type": "pickup",
  "description": "Regular garbage pickup",
  "scheduled_date": "2024-01-20T00:00:00Z",
  "priority": "normal",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": "Error message",
  "code": 400,
  "details": "Additional error details"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting
API requests are limited to 100 requests per minute per user.

## Data Models

### Customer
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "address": "string",
  "customer_type": "residential|commercial|industrial",
  "service_frequency": "daily|weekly|bi-weekly|monthly",
  "created_at": "datetime"
}
```

### ServiceRequest
```json
{
  "id": "integer",
  "customer_id": "integer",
  "service_type": "pickup|disposal|recycling|bulk|hazardous",
  "description": "string",
  "scheduled_date": "datetime",
  "priority": "low|normal|high|urgent",
  "status": "pending|confirmed|in_progress|completed|cancelled",
  "created_at": "datetime"
}
```

### Vehicle
```json
{
  "id": "integer",
  "vehicle_number": "string",
  "vehicle_type": "truck|compactor|van|pickup",
  "capacity": "string",
  "status": "available|in_use|maintenance|out_of_service",
  "driver_name": "string",
  "created_at": "datetime"
}
```

### Employee
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "role": "driver|collector|supervisor|manager|admin",
  "department_id": "integer",
  "status": "active|inactive|on_leave|terminated",
  "created_at": "datetime"
}
```

## Webhooks
The API supports webhooks for real-time notifications:

### Webhook Events
- `customer.created`
- `request.created`
- `request.status_changed`
- `vehicle.maintenance_due`
- `employee.assigned`

### Webhook Payload
```json
{
  "event": "request.status_changed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "request_id": 1,
    "old_status": "pending",
    "new_status": "confirmed"
  }
}
```

## SDKs and Libraries
- Python SDK (coming soon)
- JavaScript SDK (coming soon)
- Mobile SDK (coming soon)

## Support
For API support and questions:
- Email: api@ecoclean.com
- Documentation: https://docs.ecoclean.com
- Status: https://status.ecoclean.com 