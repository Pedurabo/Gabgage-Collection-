# 🚀 Production Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Garbage Collection Management System to production.

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04 LTS or later / CentOS 8+ / RHEL 8+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 20GB free space
- **CPU**: 2+ cores recommended

### Software Requirements
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Nginx
- SSL Certificate (Let's Encrypt recommended)

## Deployment Options

### Option 1: Traditional Server Deployment

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash www-data
sudo usermod -aG sudo www-data
```

#### 2. Database Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE garbage_collection_prod;
CREATE USER gc_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE garbage_collection_prod TO gc_user;
\q
```

#### 3. Application Deployment
```bash
# Clone/copy application to server
sudo mkdir -p /opt/garbage-collection
sudo chown www-data:www-data /opt/garbage-collection

# Copy application files
sudo cp -r . /opt/garbage-collection/
sudo chown -R www-data:www-data /opt/garbage-collection

# Set up virtual environment
cd /opt/garbage-collection
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
```

#### 4. Environment Configuration
```bash
# Create production environment file
sudo -u www-data cp production.env .env
sudo -u www-data nano .env

# Update with your production values:
# - SECRET_KEY (generate with: python3 -c "import secrets; print(secrets.token_hex(32))")
# - DATABASE_URL
# - MAIL settings
# - Other environment-specific settings
```

#### 5. Service Setup
```bash
# Copy service file
sudo cp garbage-collection.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable garbage-collection.service
sudo systemctl start garbage-collection.service
```

#### 6. Nginx Configuration
```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/garbage-collection
sudo ln -s /etc/nginx/sites-available/garbage-collection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. SSL Certificate
```bash
# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Set up auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Docker Deployment

#### 1. Install Docker and Docker Compose
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Configure Environment
```bash
# Copy and edit environment file
cp production.env .env
nano .env
```

#### 3. Deploy with Docker Compose
```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps
```

## Security Configuration

### 1. Firewall Setup
```bash
# Configure UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. Database Security
```bash
# Configure PostgreSQL for production
sudo nano /etc/postgresql/13/main/postgresql.conf
# Set: listen_addresses = 'localhost'
# Set: max_connections = 100

sudo nano /etc/postgresql/13/main/pg_hba.conf
# Ensure only local connections are allowed
```

### 3. Application Security
- Use strong SECRET_KEY
- Enable HTTPS only
- Set secure session cookies
- Implement rate limiting
- Regular security updates

## Monitoring and Logging

### 1. Log Management
```bash
# Create log directory
sudo mkdir -p /var/log/garbage-collection
sudo chown www-data:www-data /var/log/garbage-collection

# Set up log rotation
sudo cp /etc/logrotate.d/garbage-collection /etc/logrotate.d/
```

### 2. Health Monitoring
```bash
# Test health endpoint
curl http://localhost:5000/health

# Set up monitoring (example with systemd)
sudo systemctl status garbage-collection.service
```

### 3. Backup Strategy
```bash
# Database backup script
#!/bin/bash
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump garbage_collection_prod > $BACKUP_DIR/backup_$DATE.sql

# Add to crontab for daily backups
# 0 2 * * * /path/to/backup_script.sh
```

## Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_requests_status ON service_requests(status);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to_id);
```

### 2. Application Optimization
- Use Gunicorn with multiple workers
- Enable Redis for caching
- Optimize database queries
- Use CDN for static files

### 3. Nginx Optimization
```nginx
# Enable gzip compression
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# Set up caching for static files
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check service status
sudo systemctl status garbage-collection.service

# View logs
sudo journalctl -u garbage-collection.service -f
```

#### 2. Database Connection Issues
```bash
# Test database connection
sudo -u www-data psql -h localhost -U gc_user -d garbage_collection_prod

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

#### 3. Nginx Issues
```bash
# Test nginx configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

## Maintenance

### Regular Tasks
1. **Daily**: Check application logs and health endpoint
2. **Weekly**: Review error logs and performance metrics
3. **Monthly**: Update system packages and application dependencies
4. **Quarterly**: Security audit and backup restoration test

### Update Procedure
```bash
# Stop service
sudo systemctl stop garbage-collection.service

# Backup current version
sudo cp -r /opt/garbage-collection /opt/garbage-collection.backup

# Update application
sudo -u www-data git pull origin main
sudo -u www-data venv/bin/pip install -r requirements.txt

# Run database migrations (if any)
sudo -u www-data venv/bin/python manage.py migrate

# Start service
sudo systemctl start garbage-collection.service

# Verify deployment
curl http://localhost:5000/health
```

## Support and Monitoring

### Monitoring Tools
- **Application**: Built-in health endpoint
- **System**: htop, iotop, netstat
- **Database**: pg_stat_statements
- **Web Server**: nginx status module

### Alerting
Set up monitoring for:
- Service availability
- Database connectivity
- Disk space usage
- Memory usage
- Error rates

## Emergency Procedures

### Service Recovery
```bash
# Restart service
sudo systemctl restart garbage-collection.service

# Check logs immediately
sudo journalctl -u garbage-collection.service --since "5 minutes ago"
```

### Database Recovery
```bash
# Restore from backup
pg_restore -d garbage_collection_prod backup_file.sql
```

### Rollback Procedure
```bash
# Stop current service
sudo systemctl stop garbage-collection.service

# Restore previous version
sudo rm -rf /opt/garbage-collection
sudo cp -r /opt/garbage-collection.backup /opt/garbage-collection

# Start service
sudo systemctl start garbage-collection.service
```

---

## Quick Deployment Checklist

- [ ] Server prepared with required software
- [ ] Database created and configured
- [ ] Application files deployed
- [ ] Environment variables configured
- [ ] Service installed and running
- [ ] Nginx configured and SSL certificate installed
- [ ] Firewall configured
- [ ] Health endpoint responding
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Documentation updated

For additional support, refer to the application logs and system documentation. 