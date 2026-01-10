#!/bin/bash
# Docker Deployment Script for Deception Detector

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

check_docker() {
    print_info "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found. Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        rm get-docker.sh
        print_success "Docker installed"
    else
        print_success "Docker is already installed"
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_warning "Docker Compose not found. Installing..."
        apt-get update
        apt-get install -y docker-compose-plugin
        print_success "Docker Compose installed"
    else
        print_success "Docker Compose is already installed"
    fi

    # Start Docker service
    systemctl start docker
    systemctl enable docker
}

setup_env() {
    print_info "Setting up environment..."
    
    if [ ! -f backend/.env ]; then
        print_info "Creating .env file..."
        cd ../backend
        python3 ../generate_secrets.py
        cd ..
        print_warning "Please edit backend/.env with your credentials"
        print_warning "Press Enter when ready to continue..."
        read
    else
        print_success ".env file already exists"
    fi
}

cleanup_containers() {
    print_info "Cleaning up existing containers..."
    
    # Stop and remove existing containers
    docker-compose down -v 2>/dev/null || true
    
    # Remove any orphaned containers
    docker container prune -f
    
    print_success "Cleanup complete"
}

build_and_start() {
    print_info "Building Docker images (this may take several minutes)..."
    docker-compose build
    
    print_info "Starting containers..."
    docker-compose up -d
    
    print_success "Containers started!"
}

show_status() {
    echo ""
    echo "========================================="
    echo "  Docker Deployment Complete!"
    echo "========================================="
    echo ""
    print_info "Container Status:"
    docker-compose ps
    echo ""
    print_info "Access your application at:"
    echo "  http://localhost"
    echo "  http://your-server-ip"
    echo ""
    print_info "Useful Commands:"
    echo "  View logs:       docker-compose logs -f"
    echo "  Stop:            docker-compose stop"
    echo "  Start:           docker-compose start"
    echo "  Restart:         docker-compose restart"
    echo "  Status:          docker-compose ps"
    echo "  Rebuild:         docker-compose up -d --build"
    echo ""
    print_warning "To enable HTTPS, run: sudo bash deployment/docker-setup-ssl.sh"
    echo ""
}

main() {
    echo "========================================="
    echo "  Deception Detector - Docker Deployment"
    echo "========================================="
    echo ""
    
    check_root
    check_docker
    setup_env
    cleanup_containers
    build_and_start
    show_status
}

main "$@"
