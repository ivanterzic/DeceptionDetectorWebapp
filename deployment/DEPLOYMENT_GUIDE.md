# Deception Detector - Deployment Guide (Process-Based)

This guide explains how to deploy and run the Deception Detector application using simple background processes (no systemd services required).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Deployment](#initial-deployment)
3. [Configuration](#configuration)
4. [Starting the Application](#starting-the-application)
5. [Stopping the Application](#stopping-the-application)
6. [Enabling HTTPS](#enabling-https)
7. [Monitoring and Logs](#monitoring-and-logs)
8. [Troubleshooting](#troubleshooting)
9. [Auto-Start on Reboot](#auto-start-on-reboot)

---

## Prerequisites

- **Ubuntu/Debian or CentOS/RHEL** server
- **Root access** (sudo privileges)
- **Domain name** (optional, for HTTPS)
- **Minimum 8GB RAM** (for AI models)
- **20GB disk space**

---

## Initial Deployment

### Step 1: Upload Files

Upload the entire `webapp` directory to your server:

```bash
# From your local machine
scp -r webapp/ user@your-server:~/DeceptionDetector/
```

### Step 2: Run Deployment Script

```bash
# On the server
cd ~/DeceptionDetector/webapp/deployment
sudo bash simple-deploy.sh
```

This script will:
- Install dependencies (Python, Node.js, Nginx)
- Set up application directory at `/opt/deception-detector`
- Install Python packages
- Build frontend
- Configure Nginx

**Note:** When prompted for a domain name, you can enter:
- Your actual domain (e.g., `example.com`) for production
- `localhost` for local testing
- Your server's IP address

---

## Configuration

### Backend Configuration

Edit the backend environment file:

```bash
sudo nano /opt/deception-detector/backend/.env
```

**Required settings:**

```bash
# API Credentials
API_USERNAME=your_username
API_PASSWORD=your_secure_password

# JWT Secret (already generated, but you can change it)
JWT_SECRET=your_generated_secret

# Security
DEBUG_MODE=False
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost

# Optional: Custom model directory
CUSTOM_MODEL_DIR=/opt/deception-detector/backend/custom_models
```

### Frontend Configuration

If needed, edit the API endpoint:

```bash
sudo nano /opt/deception-detector/frontend/src/config.js
```

---

## Starting the Application

### Start All Services

```bash
cd /opt/deception-detector
sudo bash deployment/start.sh
```

This will start:
- **Backend** (Flask/Gunicorn) on `http://127.0.0.1:5000`
- **Frontend** (Node.js/Express) on `http://127.0.0.1:8080`
- **Nginx** (Reverse proxy) on `http://your-domain` or `http://your-ip`

### Verify Services Are Running

```bash
# Check backend process
ps aux | grep gunicorn

# Check frontend process
ps aux | grep "node.*server.js"

# Check nginx
systemctl status nginx  # or: service nginx status
```

---

## Stopping the Application

```bash
cd /opt/deception-detector
sudo bash deployment/stop.sh
```

This will stop both backend and frontend processes.

---

## Enabling HTTPS

### Prerequisites for HTTPS

1. **Domain name** pointing to your server's IP
2. **Port 80 and 443** open in firewall
3. **Application running** (start.sh must be executed)

### Setup SSL Certificate

```bash
cd /opt/deception-detector
sudo bash deployment/setup-ssl.sh
```

When prompted:
- Enter your domain name (e.g., `example.com`)
- Enter your email address (for Let's Encrypt notifications)

The script will:
1. Install certbot if needed
2. Obtain SSL certificate from Let's Encrypt
3. Update Nginx configuration for HTTPS
4. Set up automatic certificate renewal

After successful setup, your app will be accessible at:
- `https://yourdomain.com` (HTTPS)
- `http://yourdomain.com` (redirects to HTTPS)

### Certificate Renewal

Certificates auto-renew via certbot's cron job. To manually renew:

```bash
sudo certbot renew
```

---

## Monitoring and Logs

### View Logs

**Backend logs:**
```bash
# Error log
tail -f /var/log/deception-detector/backend-error.log

# Access log
tail -f /var/log/deception-detector/backend-access.log
```

**Frontend logs:**
```bash
tail -f /var/log/deception-detector/frontend.log
```

**Nginx logs:**
```bash
# Access log
tail -f /var/log/nginx/deception-detector-access.log

# Error log
tail -f /var/log/nginx/deception-detector-error.log
```

### Check Process Status

```bash
# Check if backend is running
cat /opt/deception-detector/backend.pid
ps -p $(cat /opt/deception-detector/backend.pid)

# Check if frontend is running
cat /opt/deception-detector/frontend.pid
ps -p $(cat /opt/deception-detector/frontend.pid)
```

---

## Troubleshooting

### Backend Won't Start

**Check Python environment:**
```bash
cd /opt/deception-detector/backend
source venv/bin/activate
python -c "import flask; print('Flask OK')"
gunicorn --version
```

**Check .env file exists:**
```bash
ls -la /opt/deception-detector/backend/.env
```

**Test backend manually:**
```bash
cd /opt/deception-detector/backend
source venv/bin/activate
gunicorn --bind 127.0.0.1:5000 app:app
# Press Ctrl+C to stop
```

### Frontend Won't Start

**Check dist directory exists:**
```bash
ls -la /opt/deception-detector/frontend/dist/
```

**If dist is missing, rebuild:**
```bash
cd /opt/deception-detector/frontend
npm run build
```

**Test frontend manually:**
```bash
cd /opt/deception-detector/frontend
node server.js
# Press Ctrl+C to stop
```

### Nginx Errors

**Test nginx configuration:**
```bash
sudo nginx -t
```

**Check nginx is running:**
```bash
systemctl status nginx
# or
service nginx status
```

**Restart nginx:**
```bash
sudo systemctl restart nginx
# or
sudo service nginx restart
```

### Port Already in Use

**Check what's using port 5000 (backend):**
```bash
sudo lsof -i :5000
```

**Check what's using port 8080 (frontend):**
```bash
sudo lsof -i :8080
```

**Kill process on port:**
```bash
sudo kill -9 <PID>
```

### Cannot Access Application

**Check firewall:**
```bash
# Ubuntu/Debian
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# CentOS/RHEL
sudo firewall-cmd --list-all
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload
```

**Check all services are running:**
```bash
cd /opt/deception-detector
sudo bash deployment/start.sh
ps aux | grep -E "gunicorn|node.*server.js"
```

---

## Auto-Start on Reboot

### Option 1: Using Crontab

```bash
sudo crontab -e
```

Add this line:
```
@reboot sleep 30 && cd /opt/deception-detector && bash deployment/start.sh >> /var/log/deception-detector/startup.log 2>&1
```

### Option 2: Using rc.local

```bash
sudo nano /etc/rc.local
```

Add before `exit 0`:
```bash
# Start Deception Detector
sleep 30
cd /opt/deception-detector && bash deployment/start.sh >> /var/log/deception-detector/startup.log 2>&1
```

Make it executable:
```bash
sudo chmod +x /etc/rc.local
```

### Option 3: Manual Start After Reboot

After each reboot:
```bash
cd /opt/deception-detector
sudo bash deployment/start.sh
```

---

## Maintenance Commands

### Restart Application
```bash
cd /opt/deception-detector
sudo bash deployment/stop.sh
sudo bash deployment/start.sh
```

### Update Application
```bash
# Stop app
cd /opt/deception-detector
sudo bash deployment/stop.sh

# Upload new files to server
# Then copy to /opt/deception-detector

# Rebuild frontend if needed
cd /opt/deception-detector/frontend
npm run build

# Start app
cd /opt/deception-detector
sudo bash deployment/start.sh
```

### Check Application Health
```bash
# Backend health
curl http://127.0.0.1:5000/api/health

# Frontend
curl http://127.0.0.1:8080

# Through Nginx
curl http://localhost
```

---

## Security Best Practices

1. **Change default credentials** in `.env` file
2. **Set DEBUG_MODE=False** in production
3. **Use HTTPS** in production (setup-ssl.sh)
4. **Update ALLOWED_ORIGINS** to your actual domain
5. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade  # Ubuntu/Debian
   sudo yum update  # CentOS/RHEL
   ```
6. **Regular backups** of `/opt/deception-detector/backend/custom_models/`

---

## Support

For issues or questions:
- Check logs in `/var/log/deception-detector/`
- Review this guide's troubleshooting section
- Check nginx logs: `/var/log/nginx/`

---

## Summary of Key Commands

```bash
# Deploy (first time only)
sudo bash deployment/simple-deploy.sh

# Start
sudo bash deployment/start.sh

# Stop
sudo bash deployment/stop.sh

# Enable HTTPS
sudo bash deployment/setup-ssl.sh

# View logs
tail -f /var/log/deception-detector/*.log
```
