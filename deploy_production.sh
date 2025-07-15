#!/bin/bash

# Production Deployment Script for Garbage Collection Management System
# Run this script as root or with sudo privileges

set -e  # Exit on any error

echo "🚀 Starting Production Deployment..."

# Configuration
APP_NAME="garbage-collection"
APP_DIR="/opt/$APP_NAME"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"
LOG_DIR="/var/log/$APP_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root or with sudo"
   exit 1
fi

# Step 1: Create application directory
print_status "Creating application directory..."
mkdir -p $APP_DIR
mkdir -p $LOG_DIR

# Step 2: Copy application files
print_status "Copying application files..."
cp -r . $APP_DIR/
chown -R $SERVICE_USER:$SERVICE_GROUP $APP_DIR
chmod -R 755 $APP_DIR

# Step 3: Create virtual environment
print_status "Setting up Python virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Step 4: Install dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Set up environment variables
print_status "Setting up environment variables..."
if [ ! -f production.env ]; then
    print_warning "production.env not found. Please create it with your production settings."
    exit 1
fi

# Step 6: Install and configure systemd service
print_status "Installing systemd service..."
cp garbage-collection.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable garbage-collection.service

# Step 7: Set up database
print_status "Setting up database..."
# Note: This assumes PostgreSQL is already installed and configured
# You may need to manually create the database and user

# Step 8: Set up Nginx (if not using Docker)
print_status "Setting up Nginx configuration..."
if [ -f nginx.conf ]; then
    cp nginx.conf /etc/nginx/sites-available/$APP_NAME
    ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx
fi

# Step 9: Set up SSL certificates (if available)
if [ -d ssl ]; then
    print_status "Setting up SSL certificates..."
    mkdir -p /etc/nginx/ssl
    cp ssl/* /etc/nginx/ssl/
    chmod 600 /etc/nginx/ssl/*
fi

# Step 10: Set up log rotation
print_status "Setting up log rotation..."
cat > /etc/logrotate.d/$APP_NAME << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_GROUP
    postrotate
        systemctl reload garbage-collection.service
    endscript
}
EOF

# Step 11: Set up firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    print_status "Configuring firewall..."
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
fi

# Step 12: Start services
print_status "Starting services..."
systemctl start garbage-collection.service
systemctl status garbage-collection.service

# Step 13: Final checks
print_status "Performing final checks..."
sleep 5

if systemctl is-active --quiet garbage-collection.service; then
    print_status "✅ Service is running successfully!"
else
    print_error "❌ Service failed to start. Check logs with: journalctl -u garbage-collection.service"
    exit 1
fi

# Step 14: Health check
print_status "Performing health check..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    print_status "✅ Health check passed!"
else
    print_warning "⚠️  Health check failed. Application may still be starting up."
fi

print_status "🎉 Production deployment completed successfully!"
print_status "Application URL: http://your-domain.com"
print_status "Service status: systemctl status garbage-collection.service"
print_status "View logs: journalctl -u garbage-collection.service -f" 