#!/bin/bash

# Deception Detector - Simple Deployment (No Systemd Services)
# This script deploys the app without systemd services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

APP_NAME="deception-detector"
APP_DIR="/opt/${APP_NAME}"
LOG_DIR="/var/log/${APP_NAME}"
DOMAIN=""

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        print_info "Detected OS: $OS"
    else
        print_error "Cannot detect OS"
        exit 1
    fi
}

install_dependencies() {
    print_info "Installing system dependencies..."
    
    if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
        apt-get update
        apt-get install -y python3 python3-pip python3-venv nodejs npm nginx git curl wget
    elif [[ "$OS" == "centos" || "$OS" == "rhel" ]]; then
        yum update -y
        yum install -y python3 python3-pip nodejs npm nginx git curl wget
    fi
    
    print_success "Dependencies installed"
}

setup_app_directory() {
    print_info "Setting up application directory..."
    
    mkdir -p "$APP_DIR"
    mkdir -p "$LOG_DIR"
    
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    WEBAPP_DIR="$(dirname "$SCRIPT_DIR")"
    
    cp -r "$WEBAPP_DIR/backend" "$APP_DIR/"
    cp -r "$WEBAPP_DIR/frontend" "$APP_DIR/"
    cp -r "$WEBAPP_DIR/deployment" "$APP_DIR/"
    cp "$WEBAPP_DIR"/*.py "$APP_DIR/" 2>/dev/null || true
    cp "$WEBAPP_DIR/models.txt" "$APP_DIR/" 2>/dev/null || true
    
    print_success "Files copied"
}

setup_backend() {
    print_info "Setting up Python backend..."
    
    cd "$APP_DIR/backend"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install gunicorn
    
    if [ ! -f .env ]; then
        cd "$APP_DIR"
        python3 generate_secrets.py
        print_warning "Edit $APP_DIR/backend/.env with your credentials"
    fi
    
    deactivate
    print_success "Backend setup complete"
}

setup_frontend() {
    print_info "Setting up frontend..."
    
    cd "$APP_DIR/frontend"
    rm -rf node_modules package-lock.json
    npm cache clean --force
    npm install
    npm run build
    
    # Create server.js
    cat > server.js << 'EOF'
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static(path.join(__dirname, 'dist')));

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, '127.0.0.1', () => {
    console.log(`Frontend server listening on http://127.0.0.1:${port}`);
});
EOF
    
    npm install express
    print_success "Frontend setup complete"
}

setup_nginx() {
    print_info "Setting up Nginx..."
    
    if [ -z "$DOMAIN" ]; then
        read -p "Enter domain name (or 'localhost' for testing): " DOMAIN
    fi
    
    cat > "/etc/nginx/sites-available/$APP_NAME" << EOF
server {
    listen 80;
    server_name $DOMAIN;
    client_max_body_size 50M;
    
    # Let's Encrypt validation
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    access_log /var/log/nginx/deception-detector-access.log;
    error_log /var/log/nginx/deception-detector-error.log;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_cache_bypass \$http_upgrade;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF
    
    ln -sf "/etc/nginx/sites-available/$APP_NAME" "/etc/nginx/sites-enabled/$APP_NAME"
    rm -f /etc/nginx/sites-enabled/default
    
    if nginx -t; then
        if command -v systemctl &> /dev/null; then
            systemctl restart nginx
        else
            service nginx restart
        fi
        print_success "Nginx configured (HTTP only)"
    else
        print_error "Nginx configuration test failed"
        return 1
    fi
}

make_scripts_executable() {
    chmod +x "$APP_DIR/deployment/start.sh"
    chmod +x "$APP_DIR/deployment/stop.sh"
    chmod +x "$APP_DIR/deployment/setup-ssl.sh"
}

main() {
    echo "========================================="
    echo "  Simple Deployment (Process-Based)"
    echo "========================================="
    
    check_root
    detect_os
    install_dependencies
    setup_app_directory
    setup_backend
    setup_frontend
    setup_nginx
    make_scripts_executable
    
    echo ""
    echo "========================================="
    echo "  Deployment Complete!"
    echo "========================================="
    echo ""
    print_success "Application installed to: $APP_DIR"
    echo ""
    echo "NEXT STEPS:"
    echo ""
    echo "1. Configure your application:"
    echo "   nano $APP_DIR/backend/.env"
    echo ""
    echo "2. Start the application:"
    echo "   cd $APP_DIR && bash deployment/start.sh"
    echo ""
    echo "3. (Optional) Enable HTTPS:"
    echo "   bash $APP_DIR/deployment/setup-ssl.sh"
    echo ""
    echo "OTHER COMMANDS:"
    echo "  Stop:  bash $APP_DIR/deployment/stop.sh"
    echo "  Logs:  tail -f /var/log/deception-detector/*.log"
    echo ""
    echo "Access at: http://$DOMAIN"
    echo ""
    print_info "See $APP_DIR/deployment/DEPLOYMENT_GUIDE.md for detailed instructions"
    echo ""
}

main "$@"
