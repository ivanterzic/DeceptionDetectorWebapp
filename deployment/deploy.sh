#!/bin/bash

# Deception Detector - Production Deployment Script
# This script automates the deployment of the Deception Detector application
# on a Linux server with terminal access (Ubuntu/Debian/CentOS)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="deception-detector"
APP_DIR="/opt/${APP_NAME}"
APP_USER="www-data"
APP_GROUP="www-data"
LOG_DIR="/var/log/${APP_NAME}"
DOMAIN=""
EMAIL=""

# Function to print colored messages
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
        print_info "Detected OS: $OS $OS_VERSION"
    else
        print_error "Cannot detect OS"
        exit 1
    fi
}

# Function to install system dependencies
install_dependencies() {
    print_info "Installing system dependencies..."
    
    if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
        apt-get update
        apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            nodejs \
            npm \
            nginx \
            git \
            curl \
            wget \
            ufw \
            certbot \
            python3-certbot-nginx
    elif [[ "$OS" == "centos" || "$OS" == "rhel" ]]; then
        yum update -y
        yum install -y \
            python3 \
            python3-pip \
            nodejs \
            npm \
            nginx \
            git \
            curl \
            wget \
            firewalld \
            certbot \
            python3-certbot-nginx
    else
        print_error "Unsupported OS: $OS"
        exit 1
    fi
    
    print_success "System dependencies installed"
}

# Function to create application user if needed
create_app_user() {
    if id "$APP_USER" &>/dev/null; then
        print_info "User $APP_USER already exists"
    else
        print_info "Creating application user: $APP_USER"
        useradd -r -s /bin/bash -d "$APP_DIR" "$APP_USER" || true
    fi
}

# Function to setup application directory
setup_app_directory() {
    print_info "Setting up application directory: $APP_DIR"
    
    # Create directory if it doesn't exist
    mkdir -p "$APP_DIR"
    mkdir -p "$LOG_DIR"
    
    # Copy application files
    print_info "Copying application files..."
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    WEBAPP_DIR="$(dirname "$SCRIPT_DIR")"
    
    # Copy backend
    cp -r "$WEBAPP_DIR/backend" "$APP_DIR/"
    cp -r "$WEBAPP_DIR/models.txt" "$APP_DIR/" 2>/dev/null || true
    cp -r "$WEBAPP_DIR/download_models.py" "$APP_DIR/" 2>/dev/null || true
    cp -r "$WEBAPP_DIR/setup_base_models.py" "$APP_DIR/" 2>/dev/null || true
    cp -r "$WEBAPP_DIR/generate_secrets.py" "$APP_DIR/" 2>/dev/null || true
    
    # Copy frontend
    cp -r "$WEBAPP_DIR/frontend" "$APP_DIR/"
    
    # Copy deployment files
    cp -r "$WEBAPP_DIR/deployment" "$APP_DIR/"
    
    print_success "Application files copied"
}

# Function to setup Python environment and install dependencies
setup_backend() {
    print_info "Setting up Python backend..."
    
    cd "$APP_DIR/backend"
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r requirements.txt
    pip install gunicorn  # Production WSGI server
    
    # Generate secrets if not exists
    if [ ! -f .env ]; then
        print_info "Generating production secrets..."
        cd "$APP_DIR"
        python3 generate_secrets.py
        
        print_warning "Please edit $APP_DIR/backend/.env and configure:"
        print_warning "  - API_USERNAME"
        print_warning "  - API_PASSWORD"
        print_warning "  - JWT_SECRET (already generated)"
        print_warning "  - ALLOWED_ORIGINS (add your domain)"
    fi
    
    deactivate
    print_success "Backend setup complete"
}

# Function to setup Node.js frontend
setup_frontend() {
    print_info "Setting up Node.js frontend..."
    
    cd "$APP_DIR/frontend"
    
    # Clean up old dependencies to prevent conflicts
    print_info "Cleaning up old dependencies..."
    rm -rf node_modules package-lock.json
    
    # Install dependencies
    npm install
    
    # Build production bundle
    print_info "Building production frontend..."
    npm run build
    
    # Create a simple Node.js server for serving the built files
    cat > server.js << 'EOF'
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8080;

// Serve static files from dist directory
app.use(express.static(path.join(__dirname, 'dist')));

// Handle client-side routing - serve index.html for all routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, '127.0.0.1', () => {
    console.log(\`Frontend server listening on http://127.0.0.1:\${port}\`);
});
EOF
    
    # Install express if not already in package.json
    if ! grep -q '"express"' package.json; then
        npm install express
    fi
    
    print_success "Frontend setup complete"
}

# Function to download models
download_models() {
    print_info "Downloading AI models (this may take 10-30 minutes)..."
    
    cd "$APP_DIR"
    source backend/venv/bin/activate
    python3 download_models.py || print_warning "Model download failed, you can run it manually later"
    deactivate
    
    print_success "Models downloaded"
}

# Function to setup systemd services
setup_systemd_services() {
    print_info "Setting up systemd services..."
    
    # Copy service files
    cp "$APP_DIR/deployment/deception-detector-backend.service" /etc/systemd/system/
    cp "$APP_DIR/deployment/deception-detector-frontend.service" /etc/systemd/system/
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable services
    systemctl enable deception-detector-backend
    systemctl enable deception-detector-frontend
    
    print_success "Systemd services configured"
}

# Function to setup Nginx
setup_nginx() {
    print_info "Setting up Nginx reverse proxy..."
    
    if [ -z "$DOMAIN" ]; then
        read -p "Enter your domain name (e.g., deception-detector.com): " DOMAIN
    fi
    
    # Copy nginx config
    cp "$APP_DIR/deployment/nginx.conf" "/etc/nginx/sites-available/$APP_NAME"
    
    # Replace domain placeholder
    sed -i "s/yourdomain.com/$DOMAIN/g" "/etc/nginx/sites-available/$APP_NAME"
    
    # Enable site
    ln -sf "/etc/nginx/sites-available/$APP_NAME" "/etc/nginx/sites-enabled/$APP_NAME"
    
    # Remove default site if exists
    rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx config
    nginx -t
    
    print_success "Nginx configured"
}

# Function to setup SSL with Let's Encrypt
setup_ssl() {
    print_info "Setting up SSL certificate..."
    
    if [ -z "$EMAIL" ]; then
        read -p "Enter your email for SSL certificate: " EMAIL
    fi
    
    if [ -z "$DOMAIN" ]; then
        read -p "Enter your domain name: " DOMAIN
    fi
    
    # Stop nginx temporarily
    systemctl stop nginx
    
    # Get certificate
    certbot certonly --standalone -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
    
    # Start nginx
    systemctl start nginx
    
    # Setup auto-renewal
    systemctl enable certbot.timer
    systemctl start certbot.timer
    
    print_success "SSL certificate installed"
}

# Function to setup firewall
setup_firewall() {
    print_info "Configuring firewall..."
    
    if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
        ufw --force enable
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow 22/tcp comment 'SSH'
        ufw allow 80/tcp comment 'HTTP'
        ufw allow 443/tcp comment 'HTTPS'
        ufw deny 5000/tcp comment 'Block direct backend access'
        ufw deny 8080/tcp comment 'Block direct frontend access'
    elif [[ "$OS" == "centos" || "$OS" == "rhel" ]]; then
        systemctl enable firewalld
        systemctl start firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --remove-service=cockpit 2>/dev/null || true
        firewall-cmd --reload
    fi
    
    print_success "Firewall configured"
}

# Function to set correct permissions
set_permissions() {
    print_info "Setting file permissions..."
    
    chown -R "$APP_USER:$APP_GROUP" "$APP_DIR"
    chown -R "$APP_USER:$APP_GROUP" "$LOG_DIR"
    
    # Make scripts executable
    chmod +x "$APP_DIR/backend/venv/bin/"* 2>/dev/null || true
    chmod 600 "$APP_DIR/backend/.env" 2>/dev/null || true
    
    print_success "Permissions set"
}

# Function to start services
start_services() {
    print_info "Starting services..."
    
    systemctl restart deception-detector-backend
    systemctl restart deception-detector-frontend
    systemctl restart nginx
    
    # Check status
    sleep 3
    if systemctl is-active --quiet deception-detector-backend; then
        print_success "Backend service is running"
    else
        print_error "Backend service failed to start. Check logs with: journalctl -u deception-detector-backend -n 50"
    fi
    
    if systemctl is-active --quiet deception-detector-frontend; then
        print_success "Frontend service is running"
    else
        print_error "Frontend service failed to start. Check logs with: journalctl -u deception-detector-frontend -n 50"
    fi
    
    if systemctl is-active --quiet nginx; then
        print_success "Nginx is running"
    else
        print_error "Nginx failed to start. Check logs with: journalctl -u nginx -n 50"
    fi
}

# Function to display summary
display_summary() {
    echo ""
    echo "========================================="
    echo "  Deployment Complete!"
    echo "========================================="
    echo ""
    echo "Application directory: $APP_DIR"
    echo "Log directory: $LOG_DIR"
    echo ""
    echo "Services:"
    echo "  - Backend:  systemctl status deception-detector-backend"
    echo "  - Frontend: systemctl status deception-detector-frontend"
    echo "  - Nginx:    systemctl status nginx"
    echo ""
    echo "Logs:"
    echo "  - Backend:  journalctl -u deception-detector-backend -f"
    echo "  - Frontend: journalctl -u deception-detector-frontend -f"
    echo "  - Nginx:    tail -f /var/log/nginx/access.log"
    echo ""
    echo "Configuration files:"
    echo "  - Backend env:  $APP_DIR/backend/.env"
    echo "  - Nginx config: /etc/nginx/sites-available/$APP_NAME"
    echo ""
    if [ -n "$DOMAIN" ]; then
        echo "Access your application at:"
        echo "  https://$DOMAIN"
    fi
    echo ""
    print_warning "Don't forget to:"
    print_warning "  1. Edit $APP_DIR/backend/.env with your credentials"
    print_warning "  2. Update ALLOWED_ORIGINS in backend/config.py"
    print_warning "  3. Set DEBUG_MODE=False in backend/.env"
    print_warning "  4. Restart services after making changes"
    echo ""
}

# Main deployment flow
main() {
    echo "========================================="
    echo "  Deception Detector - Deployment Script"
    echo "========================================="
    echo ""
    
    check_root
    detect_os
    
    # Ask for configuration
    read -p "Enter your domain name (or press Enter to skip SSL setup): " DOMAIN
    if [ -n "$DOMAIN" ]; then
        read -p "Enter your email for SSL certificate: " EMAIL
    fi
    
    # Run deployment steps
    install_dependencies
    create_app_user
    setup_app_directory
    setup_backend
    setup_frontend
    
    # Ask about model download
    read -p "Download AI models now? (y/n, takes 10-30 minutes): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        download_models
    else
        print_warning "Skipping model download. Run manually: cd $APP_DIR && python3 download_models.py"
    fi
    
    setup_systemd_services
    setup_nginx
    
    if [ -n "$DOMAIN" ] && [ -n "$EMAIL" ]; then
        setup_ssl
    else
        print_warning "Skipping SSL setup. Run manually: sudo certbot --nginx -d yourdomain.com"
    fi
    
    setup_firewall
    set_permissions
    start_services
    display_summary
}

# Run main function
main "$@"
