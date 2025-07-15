#!/usr/bin/env python3
"""
Production Deployment Script for Garbage Collection Management System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'uploads',
        'ssl',
        'backups',
        'static',
        'instance'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_environment():
    """Setup production environment variables"""
    env_content = """# Production Environment Variables
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-change-this
DATABASE_URL=postgresql://postgres:password@localhost:5432/garbage_collection

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# AI/ML Configuration
MODEL_PATH=/app/models
PREDICTION_ENABLED=true

# Mobile API Configuration
MOBILE_API_ENABLED=true
PUSH_NOTIFICATIONS_ENABLED=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("🔧 Created .env file with production configuration")

def install_dependencies():
    """Install production dependencies"""
    run_command("pip install -r requirements.txt", "Installing Python dependencies")
    
    # Install system dependencies (for Ubuntu/Debian)
    system_deps = [
        "postgresql postgresql-contrib",
        "redis-server",
        "nginx",
        "certbot python3-certbot-nginx"
    ]
    
    for dep in system_deps:
        run_command(f"sudo apt-get install -y {dep}", f"Installing {dep}")

def setup_database():
    """Setup PostgreSQL database"""
    print("🗄️ Setting up PostgreSQL database...")
    
    # Create database and user
    db_commands = [
        "sudo -u postgres createdb garbage_collection",
        "sudo -u postgres psql -c \"CREATE USER garbage_user WITH PASSWORD 'password';\"",
        "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE garbage_collection TO garbage_user;\""
    ]
    
    for command in db_commands:
        run_command(command, "Database setup")

def setup_nginx():
    """Setup Nginx configuration"""
    print("🌐 Setting up Nginx...")
    
    # Copy nginx configuration
    nginx_conf = """server {
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
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}"""
    
    with open('/etc/nginx/sites-available/garbage-collection', 'w') as f:
        f.write(nginx_conf)
    
    # Enable site
    run_command("sudo ln -sf /etc/nginx/sites-available/garbage-collection /etc/nginx/sites-enabled/", "Enabling Nginx site")
    run_command("sudo nginx -t", "Testing Nginx configuration")
    run_command("sudo systemctl restart nginx", "Restarting Nginx")

def setup_ssl():
    """Setup SSL certificates"""
    print("🔒 Setting up SSL certificates...")
    
    # Generate self-signed certificate for development
    ssl_commands = [
        "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/privkey.pem -out ssl/fullchain.pem -subj '/CN=localhost'",
        "chmod 600 ssl/privkey.pem",
        "chmod 644 ssl/fullchain.pem"
    ]
    
    for command in ssl_commands:
        run_command(command, "SSL certificate generation")

def setup_systemd():
    """Setup systemd service"""
    print("⚙️ Setting up systemd service...")
    
    service_content = """[Unit]
Description=Garbage Collection Management System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('/etc/systemd/system/garbage-collection.service', 'w') as f:
        f.write(service_content)
    
    run_command("sudo systemctl daemon-reload", "Reloading systemd")
    run_command("sudo systemctl enable garbage-collection", "Enabling service")
    run_command("sudo systemctl start garbage-collection", "Starting service")

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    
    # Initialize database
    run_command("python -c \"from app import app, db; app.app_context().push(); db.create_all()\"", "Creating database tables")
    
    # Add sample data
    run_command("python sample_data.py", "Adding sample data")

def setup_monitoring():
    """Setup monitoring and logging"""
    print("📊 Setting up monitoring...")
    
    # Create log rotation
    logrotate_conf = """/path/to/your/app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}"""
    
    with open('/etc/logrotate.d/garbage-collection', 'w') as f:
        f.write(logrotate_conf)

def security_setup():
    """Setup security measures"""
    print("🔐 Setting up security measures...")
    
    # Firewall rules
    firewall_commands = [
        "sudo ufw allow 22/tcp",
        "sudo ufw allow 80/tcp",
        "sudo ufw allow 443/tcp",
        "sudo ufw --force enable"
    ]
    
    for command in firewall_commands:
        run_command(command, "Firewall configuration")

def health_check():
    """Perform health check"""
    print("🏥 Performing health check...")
    
    checks = [
        ("curl -f http://localhost:5000/health", "Application health"),
        ("sudo systemctl is-active garbage-collection", "Service status"),
        ("sudo systemctl is-active nginx", "Nginx status"),
        ("sudo systemctl is-active postgresql", "PostgreSQL status"),
        ("sudo systemctl is-active redis", "Redis status")
    ]
    
    for command, description in checks:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: FAILED")
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")

def main():
    """Main deployment function"""
    print("🚀 Starting production deployment...")
    
    # Check if running as root
    if os.geteuid() == 0:
        print("⚠️ Warning: Running as root. Consider using a non-root user for security.")
    
    # Deployment steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up database", setup_database),
        ("Setting up Nginx", setup_nginx),
        ("Setting up SSL", setup_ssl),
        ("Setting up systemd service", setup_systemd),
        ("Running migrations", run_migrations),
        ("Setting up monitoring", setup_monitoring),
        ("Setting up security", security_setup),
        ("Health check", health_check)
    ]
    
    for step_name, step_function in steps:
        print(f"\n{'='*50}")
        print(f"📋 {step_name}")
        print(f"{'='*50}")
        step_function()
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update domain name in nginx configuration")
    print("2. Configure SSL certificates with Let's Encrypt")
    print("3. Set up monitoring and alerting")
    print("4. Configure backups")
    print("5. Test all functionality")
    print("6. Update firewall rules for your specific needs")

if __name__ == "__main__":
    main() 