#!/bin/bash
# Setup SSL/HTTPS for Deception Detector

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root (use sudo)"
    exit 1
fi

read -p "Enter your domain name: " DOMAIN
read -p "Enter your email address: " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    print_error "Domain and email are required"
    exit 1
fi

print_info "Installing certbot if needed..."
if ! command -v certbot &> /dev/null; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" || "$ID" == "debian" ]]; then
            apt-get update
            apt-get install -y certbot python3-certbot-nginx
        elif [[ "$ID" == "centos" || "$ID" == "rhel" ]]; then
            yum install -y certbot python3-certbot-nginx
        fi
    fi
fi

print_info "Obtaining SSL certificate..."
certbot certonly --webroot -w /var/www/html \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive

if [ $? -ne 0 ]; then
    print_error "Failed to obtain SSL certificate"
    print_info "Make sure:"
    print_info "  1. Your domain DNS points to this server"
    print_info "  2. Port 80 is open in firewall"
    print_info "  3. Nginx is running"
    exit 1
fi

print_info "Updating nginx configuration for HTTPS..."

cat > /etc/nginx/sites-available/deception-detector << EOF
# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers off;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Logging
    access_log /var/log/nginx/deception-detector-access.log;
    error_log /var/log/nginx/deception-detector-error.log;
    
    # Max upload size
    client_max_body_size 50M;
    
    # Frontend
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF

print_info "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    print_info "Reloading nginx..."
    if command -v systemctl &> /dev/null; then
        systemctl reload nginx
    else
        service nginx reload
    fi
    
    print_success "SSL/HTTPS enabled successfully!"
    echo ""
    echo "Your application is now accessible at:"
    echo "  https://$DOMAIN"
    echo ""
    echo "Certificate will auto-renew via certbot timer."
else
    print_error "Nginx configuration test failed"
    exit 1
fi
