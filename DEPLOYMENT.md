# 🚀 Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Garbage Collection Management System to production with Docker, AI/ML features, mobile APIs, and advanced business intelligence.

## 📋 Prerequisites

- Ubuntu 20.04+ or CentOS 8+
- Python 3.9+
- Docker and Docker Compose
- PostgreSQL 13+
- Redis 6+
- Nginx
- SSL certificates (Let's Encrypt recommended)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (SSL)   │    │  Flask App      │    │  PostgreSQL     │
│   Port 80/443   │───▶│  Port 5000      │───▶│  Port 5432      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Redis Cache    │
                       │  Port 6379      │
                       └─────────────────┘
```

## 🐳 Docker Deployment

### 1. Quick Start with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd garbage-collection-system

# Create environment file
cp .env.example .env
# Edit .env with your production values

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### 2. Production Docker Configuration

```bash
# Build production image
docker build -t garbage-collection:latest .

# Run with production settings
docker run -d \
  --name garbage-collection \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/uploads:/app/uploads \
  garbage-collection:latest
```

## 🔧 Manual Deployment

### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash garbage
sudo usermod -aG sudo garbage
```

### 2. Application Setup

```bash
# Switch to application user
sudo su - garbage

# Clone repository
git clone <repository-url>
cd garbage-collection-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Edit with production values
```

### 3. Database Setup

```bash
# Create database
sudo -u postgres createdb garbage_collection

# Create user
sudo -u postgres psql -c "CREATE USER garbage_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE garbage_collection TO garbage_user;"

# Run migrations
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Add sample data
python sample_data.py
```

### 4. Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/garbage-collection

# Add the following configuration:
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /home/garbage/garbage-collection-system/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/garbage-collection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate

```bash
# Install SSL certificate with Let's Encrypt
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### 6. Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/garbage-collection.service

# Add the following configuration:
[Unit]
Description=Garbage Collection Management System
After=network.target

[Service]
Type=simple
User=garbage
WorkingDirectory=/home/garbage/garbage-collection-system
Environment=PATH=/home/garbage/garbage-collection-system/venv/bin
ExecStart=/home/garbage/garbage-collection-system/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable garbage-collection
sudo systemctl start garbage-collection
```

## 🤖 AI/ML Features Setup

### 1. Route Optimization

The AI route optimization is automatically available through the `/api/optimize-routes` endpoint.

```bash
# Test route optimization
curl -X POST http://your-domain.com/api/optimize-routes \
  -H "Content-Type: application/json" \
  -d '{
    "service_requests": [...],
    "vehicles": [...],
    "constraints": {...}
  }'
```

### 2. Business Intelligence

Access business intelligence dashboard at `/analytics`:

```bash
# Generate analytics report
curl http://your-domain.com/api/analytics/comprehensive
```

### 3. Predictive Analytics

```bash
# Demand forecasting
curl http://your-domain.com/api/analytics/forecast-demand

# Revenue prediction
curl http://your-domain.com/api/analytics/forecast-revenue
```

## 📱 Mobile API Setup

### 1. Driver Mobile API

```bash
# Driver login
curl -X POST http://your-domain.com/api/mobile/driver/login \
  -H "Content-Type: application/json" \
  -d '{"username": "driver1", "password": "password123"}'

# Get driver dashboard
curl "http://your-domain.com/api/mobile/driver/dashboard?driver_id=1"
```

### 2. Customer Mobile API

```bash
# Customer login
curl -X POST http://your-domain.com/api/mobile/customer/login \
  -H "Content-Type: application/json" \
  -d '{"email": "customer@example.com", "password": "password123"}'

# Request service
curl -X POST http://your-domain.com/api/mobile/customer/request-service \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "service_type": "pickup",
    "description": "Regular pickup",
    "scheduled_date": "2024-01-15T10:00:00"
  }'
```

## 🔒 Security Configuration

### 1. Firewall Setup

```bash
# Configure UFW firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### 2. Security Headers

The application includes security headers automatically. Verify with:

```bash
curl -I http://your-domain.com
```

### 3. Rate Limiting

Nginx rate limiting is configured in the nginx.conf file:

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
```

## 📊 Monitoring and Logging

### 1. Application Logs

```bash
# View application logs
sudo journalctl -u garbage-collection -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Health Checks

```bash
# Application health
curl http://your-domain.com/health

# Database health
curl http://your-domain.com/api/health/database

# Redis health
curl http://your-domain.com/api/health/redis
```

### 3. Performance Monitoring

```bash
# Monitor system resources
htop
iotop
nethogs

# Monitor application performance
curl http://your-domain.com/api/metrics
```

## 🔄 Backup and Recovery

### 1. Database Backup

```bash
# Create backup script
sudo nano /usr/local/bin/backup-database.sh

#!/bin/bash
BACKUP_DIR="/home/garbage/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/garbage_collection_$DATE.sql"

pg_dump -h localhost -U garbage_user garbage_collection > $BACKUP_FILE
gzip $BACKUP_FILE

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Make executable
sudo chmod +x /usr/local/bin/backup-database.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-database.sh
```

### 2. Application Backup

```bash
# Backup application files
sudo tar -czf /home/garbage/backups/app_$(date +%Y%m%d_%H%M%S).tar.gz \
  /home/garbage/garbage-collection-system \
  --exclude=venv \
  --exclude=__pycache__ \
  --exclude=*.pyc
```

## 🚀 Scaling and Performance

### 1. Horizontal Scaling

```bash
# Run multiple application instances
docker-compose up -d --scale web=3

# Use load balancer
sudo apt install haproxy
```

### 2. Database Optimization

```bash
# PostgreSQL optimization
sudo nano /etc/postgresql/13/main/postgresql.conf

# Add these settings:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### 3. Redis Optimization

```bash
# Redis optimization
sudo nano /etc/redis/redis.conf

# Add these settings:
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## 🧪 Testing

### 1. Unit Tests

```bash
# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### 2. Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test performance
ab -n 1000 -c 10 http://your-domain.com/

# Test API endpoints
ab -n 1000 -c 10 -p test_data.json -T application/json http://your-domain.com/api/customers
```

### 3. Security Testing

```bash
# Test for common vulnerabilities
sudo apt install nikto
nikto -h your-domain.com

# Test SSL configuration
sudo apt install sslyze
sslyze --regular your-domain.com
```

## 🔧 Troubleshooting

### Common Issues

1. **Application won't start**
   ```bash
   sudo systemctl status garbage-collection
   sudo journalctl -u garbage-collection -f
   ```

2. **Database connection issues**
   ```bash
   sudo systemctl status postgresql
   sudo -u postgres psql -c "\l"
   ```

3. **Nginx configuration errors**
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   ```

4. **SSL certificate issues**
   ```bash
   sudo certbot certificates
   sudo certbot renew --dry-run
   ```

### Performance Issues

1. **High CPU usage**
   ```bash
   top
   htop
   ```

2. **High memory usage**
   ```bash
   free -h
   sudo systemctl status garbage-collection
   ```

3. **Slow database queries**
   ```bash
   sudo -u postgres psql -d garbage_collection -c "SELECT * FROM pg_stat_activity;"
   ```

## 📞 Support

For support and issues:

1. Check logs: `sudo journalctl -u garbage-collection -f`
2. Monitor system resources: `htop`
3. Test endpoints: `curl http://your-domain.com/health`
4. Check database: `sudo -u postgres psql -d garbage_collection`

## 🎯 Next Steps

1. **Customization**: Modify templates and styles for your brand
2. **Integration**: Connect with external systems (accounting, CRM)
3. **Mobile Apps**: Develop native mobile applications
4. **Advanced Analytics**: Implement more sophisticated AI/ML models
5. **Multi-tenancy**: Add support for multiple companies
6. **API Development**: Create public APIs for third-party integrations 