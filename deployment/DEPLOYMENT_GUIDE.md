# 🚀 Production Deployment Guide

Complete guide for deploying Deception Detector on a traditional Linux server (VPS, dedicated server, or cloud VM with terminal access).

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Deployment](#quick-deployment)
3. [Manual Deployment](#manual-deployment)
4. [Configuration](#configuration)
5. [Service Management](#service-management)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)
8. [Security Best Practices](#security-best-practices)

---

## Prerequisites

### Server Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| OS | Ubuntu 20.04 / Debian 11 / CentOS 8 | Ubuntu 22.04 LTS |
| CPU | 2 cores | 4+ cores |
| RAM | 4GB | 8GB+ (16GB with GPU) |
| Storage | 20GB | 50GB+ |
| GPU | - | NVIDIA GPU with 4GB+ VRAM |

### What You Need

- Root/sudo access to your server
- Domain name pointing to your server IP (optional but recommended)
- SSH access to the server
- Basic Linux command-line knowledge

### Pre-Deployment Checklist

- [ ] Server is running and accessible via SSH
- [ ] Domain DNS records are configured (A record pointing to server IP)
- [ ] Firewall rules allow SSH access (port 22)
- [ ] You have the application code on your local machine

---

## Quick Deployment

### Option 1: Automated Deployment (Recommended)

The automated script handles everything for you:

```bash
# 1. Upload the webapp folder to your server
scp -r webapp/ user@your-server:/tmp/

# 2. SSH into your server
ssh user@your-server

# 3. Run the deployment script
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

The script will:
- ✅ Install all system dependencies
- ✅ Setup Python and Node.js environments
- ✅ Configure systemd services
- ✅ Setup Nginx reverse proxy
- ✅ Configure SSL certificates (if domain provided)
- ✅ Setup firewall rules
- ✅ Download AI models (optional)
- ✅ Start all services

**Estimated time:** 15-45 minutes (depending on model download)

---

## Manual Deployment

If you prefer step-by-step control or need to customize the deployment:

### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3 python3-pip python3-venv \
    nodejs npm \
    nginx \
    git curl wget \
    ufw \
    certbot python3-certbot-nginx

# For GPU support (optional)
# Follow NVIDIA CUDA installation guide for your OS
```

### Step 2: Create Application Directory

```bash
# Create directory
sudo mkdir -p /opt/deception-detector
sudo mkdir -p /var/log/deception-detector

# Transfer your files
cd /opt/deception-detector
# Upload via scp, rsync, or git clone
```

### Step 3: Setup Backend

```bash
cd /opt/deception-detector/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create .env file
cp ../deployment/.env.production.template .env
nano .env  # Edit configuration

# Generate JWT secret
cd ..
python3 generate_secrets.py
# Copy the JWT_SECRET to backend/.env
```

### Step 4: Setup Frontend

```bash
cd /opt/deception-detector/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Create server file
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
    console.log(\`Frontend server listening on http://127.0.0.1:\${port}\`);
});
EOF

npm install express
```

### Step 5: Download AI Models (Optional)

```bash
cd /opt/deception-detector
source backend/venv/bin/activate
python3 download_models.py
deactivate
```

This takes 10-30 minutes depending on your internet speed.

### Step 6: Setup Systemd Services

```bash
# Copy service files
sudo cp deployment/deception-detector-backend.service /etc/systemd/system/
sudo cp deployment/deception-detector-frontend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable deception-detector-backend
sudo systemctl enable deception-detector-frontend

# Start services
sudo systemctl start deception-detector-backend
sudo systemctl start deception-detector-frontend

# Check status
sudo systemctl status deception-detector-backend
sudo systemctl status deception-detector-frontend
```

### Step 7: Setup Nginx

```bash
# Copy nginx config
sudo cp deployment/nginx.conf /etc/nginx/sites-available/deception-detector

# Edit domain name
sudo nano /etc/nginx/sites-available/deception-detector
# Replace 'yourdomain.com' with your actual domain

# Enable site
sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 8: Setup SSL Certificate

```bash
# Get certificate from Let's Encrypt
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot will automatically:
# - Obtain SSL certificate
# - Configure Nginx to use it
# - Setup auto-renewal

# Test renewal
sudo certbot renew --dry-run
```

### Step 9: Configure Firewall

```bash
# Enable firewall
sudo ufw --force enable

# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to backend/frontend
sudo ufw deny 5000/tcp
sudo ufw deny 8080/tcp

# Check status
sudo ufw status
```

### Step 10: Set Permissions

```bash
# Set ownership
sudo chown -R www-data:www-data /opt/deception-detector
sudo chown -R www-data:www-data /var/log/deception-detector

# Secure .env file
sudo chmod 600 /opt/deception-detector/backend/.env
```

---

## Configuration

### Backend Configuration (backend/.env)

```bash
# Edit the environment file
sudo nano /opt/deception-detector/backend/.env
```

**Critical settings to configure:**

```env
# Set to production
FLASK_ENV=production
DEBUG_MODE=False

# Your domain (for CORS)
ALLOWED_ORIGINS=https://yourdomain.com

# Generate strong secret with: python3 generate_secrets.py
JWT_SECRET=your_64_char_secret_here

# Set API credentials
API_USERNAME=your_api_username
API_PASSWORD=your_secure_password
```

### Frontend Configuration (frontend/src/config.js)

```bash
sudo nano /opt/deception-detector/frontend/src/config.js
```

Update API URL if needed:

```javascript
export default {
  apiUrl: '/api'  // Uses same domain via Nginx proxy
}
```

Then rebuild:

```bash
cd /opt/deception-detector/frontend
npm run build
sudo systemctl restart deception-detector-frontend
```

---

## Service Management

### Common Commands

```bash
# Backend service
sudo systemctl start deception-detector-backend
sudo systemctl stop deception-detector-backend
sudo systemctl restart deception-detector-backend
sudo systemctl status deception-detector-backend

# Frontend service
sudo systemctl start deception-detector-frontend
sudo systemctl stop deception-detector-frontend
sudo systemctl restart deception-detector-frontend
sudo systemctl status deception-detector-frontend

# Nginx
sudo systemctl restart nginx
sudo systemctl reload nginx  # Reload config without downtime

# View logs
sudo journalctl -u deception-detector-backend -f
sudo journalctl -u deception-detector-frontend -f
sudo tail -f /var/log/nginx/deception-detector-access.log
sudo tail -f /var/log/nginx/deception-detector-error.log
```

### After Making Changes

```bash
# After editing .env or config files
sudo systemctl restart deception-detector-backend

# After changing frontend code
cd /opt/deception-detector/frontend
npm run build
sudo systemctl restart deception-detector-frontend

# After changing Nginx config
sudo nginx -t  # Test config first
sudo systemctl reload nginx
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
sudo journalctl -u deception-detector-backend -n 100 --no-pager

# Common issues:
# 1. Missing .env file
ls -la /opt/deception-detector/backend/.env

# 2. Python dependencies
cd /opt/deception-detector/backend
source venv/bin/activate
pip install -r requirements.txt

# 3. Permission issues
sudo chown -R www-data:www-data /opt/deception-detector/backend
```

### Frontend Won't Start

```bash
# Check logs
sudo journalctl -u deception-detector-frontend -n 100 --no-pager

# Common issues:
# 1. Node modules not installed
cd /opt/deception-detector/frontend
npm install

# 2. Build not created
npm run build

# 3. Port already in use
sudo lsof -i :8080
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Verify backend is running
curl http://127.0.0.1:5000/api/health

# Verify frontend is running
curl http://127.0.0.1:8080
```

### SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check auto-renewal
sudo systemctl status certbot.timer
```

### 502 Bad Gateway

This means Nginx can't reach the backend/frontend:

```bash
# Check if services are running
sudo systemctl status deception-detector-backend
sudo systemctl status deception-detector-frontend

# Check if they're listening
sudo netstat -tlnp | grep :5000
sudo netstat -tlnp | grep :8080
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart services to free memory
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend

# Adjust resource limits in service files if needed
sudo nano /etc/systemd/system/deception-detector-backend.service
# Edit MemoryLimit and CPUQuota
sudo systemctl daemon-reload
sudo systemctl restart deception-detector-backend
```

---

## Maintenance

### Regular Updates

```bash
# Use the update script
cd /opt/deception-detector/deployment
sudo chmod +x update.sh
sudo ./update.sh
```

Or manually:

```bash
# 1. Backup current state
sudo cp -r /opt/deception-detector /backup/deception-detector-$(date +%Y%m%d)

# 2. Pull new code (if using git)
cd /opt/deception-detector
sudo git pull

# 3. Update dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
deactivate

cd ../frontend
npm install
npm run build

# 4. Restart services
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend
```

### Backup Strategy

```bash
# Create backup script
cat > /opt/backup-deception.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/deception-detector-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /opt/deception-detector/backend/.env "$BACKUP_DIR/"
cp -r /opt/deception-detector/backend/models "$BACKUP_DIR/"
cp -r /opt/deception-detector/backend/custom_models "$BACKUP_DIR/"
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
find /backup -name "deception-detector-*.tar.gz" -mtime +30 -delete
EOF

chmod +x /opt/backup-deception.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /opt/backup-deception.sh" | sudo crontab -
```

### Monitor Logs

```bash
# Setup log rotation
sudo nano /etc/logrotate.d/deception-detector
```

Add:

```
/var/log/deception-detector/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload deception-detector-backend
    endscript
}
```

### Cleanup Old Models

The cleanup service runs automatically, but you can trigger it manually:

```bash
cd /opt/deception-detector/backend
source venv/bin/activate
python3 -c "from cleanup_service import cleanup_old_models; cleanup_old_models()"
```

---

## Security Best Practices

### ✅ Checklist

- [ ] Debug mode disabled (`DEBUG_MODE=False`)
- [ ] Strong JWT secret generated (64+ characters)
- [ ] API credentials set and secured
- [ ] CORS configured for your domain only
- [ ] Firewall enabled and configured
- [ ] SSL certificate installed and auto-renewing
- [ ] Direct backend/frontend access blocked
- [ ] File permissions set correctly (`.env` is 600)
- [ ] Regular backups configured
- [ ] Log rotation configured
- [ ] Server software kept up to date
- [ ] SSH key authentication enabled (password auth disabled)

### Additional Security Measures

```bash
# 1. Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no (use SSH keys)
sudo systemctl restart sshd

# 2. Install fail2ban (brute force protection)
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 3. Setup automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 4. Regular security audits
sudo apt install lynis
sudo lynis audit system
```

---

## Performance Tuning

### For GPU Servers

```bash
# Verify GPU is detected
nvidia-smi

# Backend will automatically use GPU if available
# Check logs to confirm:
sudo journalctl -u deception-detector-backend | grep GPU
```

### For High Traffic

```bash
# Increase Gunicorn workers
sudo nano /etc/systemd/system/deception-detector-backend.service
# Change --workers 4 to --workers 8 (or 2x CPU cores)

# Increase Nginx worker connections
sudo nano /etc/nginx/nginx.conf
# worker_processes auto;
# worker_connections 4096;

sudo systemctl daemon-reload
sudo systemctl restart deception-detector-backend
sudo systemctl reload nginx
```

---

## Getting Help

- **Logs:** Check service logs first (`journalctl -u service-name`)
- **Documentation:** See `/opt/deception-detector/docs/`
- **Issues:** Review error messages carefully
- **Testing:** Use `curl` to test endpoints directly

---

## Quick Reference

```bash
# Application directory
cd /opt/deception-detector

# View backend logs
sudo journalctl -u deception-detector-backend -f

# View frontend logs
sudo journalctl -u deception-detector-frontend -f

# Restart everything
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend
sudo systemctl reload nginx

# Check all services
sudo systemctl status deception-detector-backend --no-pager
sudo systemctl status deception-detector-frontend --no-pager
sudo systemctl status nginx --no-pager

# Update application
sudo /opt/deception-detector/deployment/update.sh

# Backup application
sudo /opt/backup-deception.sh
```

---

**Deployment complete!** Your application should now be accessible at `https://yourdomain.com` 🎉
