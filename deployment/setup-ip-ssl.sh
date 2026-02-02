#!/bin/bash
# Setup self-signed SSL certificate for IP address

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root"
    exit 1
fi

# Get IP address
read -p "Enter your server IP address: " IP_ADDRESS

if [ -z "$IP_ADDRESS" ]; then
    print_error "IP address is required"
    exit 1
fi

# Validate IP format (basic check)
if ! [[ $IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Invalid IP address format"
    exit 1
fi

print_warning "Self-signed certificates will show browser warnings."
print_warning "Users will need to manually accept the certificate."
print_info "For production, consider using a domain name with Let's Encrypt."
echo ""
read -p "Continue? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    exit 0
fi

# Create directories
print_info "Creating certificate directories..."
mkdir -p ssl
cd ssl

# Generate private key
print_info "Generating private key..."
openssl genrsa -out privkey.pem 2048

# Create OpenSSL config for IP SAN
print_info "Creating certificate configuration..."
cat > cert.conf << EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req
x509_extensions = v3_req

[dn]
C=US
ST=State
L=City
O=Organization
OU=Department
CN=$IP_ADDRESS

[v3_req]
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP_ADDRESS
IP.2 = 127.0.0.1
DNS.1 = localhost
EOF

# Generate certificate
print_info "Generating self-signed certificate..."
openssl req -new -x509 -days 365 \
    -key privkey.pem \
    -out fullchain.pem \
    -config cert.conf \
    -extensions v3_req

if [ $? -ne 0 ]; then
    print_error "Failed to generate certificate"
    exit 1
fi

# Set permissions
chmod 600 privkey.pem
chmod 644 fullchain.pem

cd ..

print_success "Certificate generated successfully!"
print_info "Certificate location: $(pwd)/ssl/"
print_info "Certificate valid for: 365 days"
print_info "Certificate includes: $IP_ADDRESS, 127.0.0.1, localhost"
echo ""

# Create nginx SSL configuration
print_info "Creating nginx SSL configuration..."
cat > nginx-docker-ssl.conf << 'EOF'
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name _;
    
    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name _;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 50M;
    
    # Frontend
    location / {
        proxy_pass http://frontend:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Backend API - Large file downloads (must be before /api/)
    location /api/custom/download/ {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Disable buffering for large file streaming
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Extended timeouts for large downloads
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        
        # Don't limit response size
        proxy_max_temp_file_size 0;
        
        # Pass through download headers
        proxy_pass_request_headers on;
    }
    
    # Backend API - Regular endpoints
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Extended timeouts for AI processing
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # Enable buffering for regular API responses
        proxy_buffering on;
        proxy_request_buffering off;
        
        # Standard buffer sizes
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}
EOF

print_success "nginx SSL configuration created!"
echo ""

# Update docker-compose.yml
print_info "Updating docker-compose.yml..."
cd ..

if [ -f "docker-compose.yml" ]; then
    # Backup original
    cp docker-compose.yml docker-compose.yml.backup
    print_success "Backup created: docker-compose.yml.backup"
    
    # Check if SSL volume already exists
    if grep -q "./deployment/ssl:" docker-compose.yml; then
        print_info "SSL volume already configured"
    else
        # Add SSL volume to nginx service
        print_info "Adding SSL certificate volume to nginx service..."
        sed -i '/- \.\/deployment\/nginx-docker\.conf/a\      - ./deployment/ssl:/etc/nginx/ssl:ro' docker-compose.yml
    fi
    
    # Switch to SSL config
    print_info "Switching to SSL nginx configuration..."
    sed -i 's|./deployment/nginx-docker\.conf|./deployment/nginx-docker-ssl.conf|g' docker-compose.yml
    
    print_success "docker-compose.yml updated successfully!"
    echo ""
    print_info "To apply changes, run:"
    echo "  docker-compose restart nginx"
else
    print_error "docker-compose.yml not found in parent directory"
    echo ""
    print_info "Manual setup required:"
    echo "  1. Edit docker-compose.yml nginx volumes section:"
    echo "     Change: - ./deployment/nginx-docker.conf:/etc/nginx/conf.d/default.conf"
    echo "     To:     - ./deployment/nginx-docker-ssl.conf:/etc/nginx/conf.d/default.conf"
    echo ""
    echo "  2. Add SSL certificate volume:"
    echo "     - ./deployment/ssl:/etc/nginx/ssl:ro"
    echo ""
    echo "  3. Restart services:"
    echo "     docker-compose restart nginx"
fi

echo ""
print_warning "Browser will show security warning - this is normal for self-signed certificates"
print_info "Users must click 'Advanced' -> 'Proceed to $IP_ADDRESS (unsafe)' to access"
echo ""
print_success "Setup complete!"
