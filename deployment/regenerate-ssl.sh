#!/bin/bash
# Regenerate SSL certificate with correct extensions

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root"
    exit 1
fi

IP_ADDRESS="161.53.18.44"
SSL_DIR="./ssl"

print_info "Backing up existing certificates..."
if [ -f "$SSL_DIR/privkey.pem" ]; then
    cp "$SSL_DIR/privkey.pem" "$SSL_DIR/privkey.pem.backup"
    cp "$SSL_DIR/fullchain.pem" "$SSL_DIR/fullchain.pem.backup"
    print_success "Backup created"
fi

print_info "Generating new certificate with correct extensions..."

# Use existing private key or generate new one
if [ ! -f "$SSL_DIR/privkey.pem" ]; then
    print_info "Generating new private key..."
    openssl genrsa -out "$SSL_DIR/privkey.pem" 2048
fi

# Generate certificate with correct extensions
openssl req -new -x509 -days 365 \
    -key "$SSL_DIR/privkey.pem" \
    -out "$SSL_DIR/fullchain.pem" \
    -config "$SSL_DIR/cert.conf" \
    -extensions v3_req

if [ $? -ne 0 ]; then
    print_error "Failed to generate certificate"
    if [ -f "$SSL_DIR/fullchain.pem.backup" ]; then
        print_info "Restoring backup..."
        mv "$SSL_DIR/fullchain.pem.backup" "$SSL_DIR/fullchain.pem"
    fi
    exit 1
fi

# Set correct permissions
chmod 600 "$SSL_DIR/privkey.pem"
chmod 644 "$SSL_DIR/fullchain.pem"

print_success "Certificate regenerated successfully!"
print_info "Verifying certificate..."

# Verify certificate extensions
echo ""
openssl x509 -in "$SSL_DIR/fullchain.pem" -text -noout | grep -A 3 "X509v3 extensions"
openssl x509 -in "$SSL_DIR/fullchain.pem" -text -noout | grep -A 1 "Key Usage"
openssl x509 -in "$SSL_DIR/fullchain.pem" -text -noout | grep -A 1 "Extended Key Usage"
openssl x509 -in "$SSL_DIR/fullchain.pem" -text -noout | grep -A 3 "Subject Alternative Name"

echo ""
print_warning "You need to restart the Docker containers for changes to take effect:"
print_info "  cd /path/to/DeceptionDetectorWebapp"
print_info "  docker-compose restart nginx"
print_info "or"
print_info "  docker-compose down && docker-compose up -d"
