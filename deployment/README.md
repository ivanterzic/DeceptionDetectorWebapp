# Deployment Files

This directory contains all files needed for production deployment on a traditional Linux server.

## Files Overview

### Core Deployment Files

- **deploy.sh** - Automated deployment script (recommended)
- **DEPLOYMENT_GUIDE.md** - Complete step-by-step deployment guide
- **nginx.conf** - Nginx reverse proxy configuration
- **.env.production.template** - Production environment variables template

### Service Files

- **deception-detector-backend.service** - Systemd service for Flask backend
- **deception-detector-frontend.service** - Systemd service for Node.js frontend

### Utility Scripts

- **update.sh** - Quick update script for code changes
- **health-check.sh** - Health monitoring script
- **check-ready.sh** - Pre-deployment validation script

## Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# On your local machine
cd /path/to/webapp

# Run pre-deployment check
bash deployment/check-ready.sh

# Upload to server
scp -r . user@your-server:/tmp/webapp/

# On your server
ssh user@your-server
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

### Option 2: Manual Deployment

Follow the complete guide in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## What Gets Deployed

The deployment installs:

- Python 3.8+ with virtual environment
- Node.js 14+ with npm
- Flask backend running with Gunicorn (WSGI server)
- Vue.js frontend (pre-built, served by Express)
- Nginx reverse proxy
- SSL certificate (via Let's Encrypt)
- Systemd services for auto-start
- Firewall configuration
- Log rotation

## Architecture

```
Internet → Nginx (:443 HTTPS) → Frontend (:8080) or Backend (:5000)
                                      ↓                    ↓
                                 Express serves       Flask API with
                                 built Vue.js         Gunicorn WSGI
```

## Directory Structure After Deployment

```
/opt/deception-detector/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── models/            # Pre-trained models
│   ├── custom_models/     # User-trained models
│   ├── base_models/       # Cached base models
│   ├── .env               # Environment config (secure)
│   └── app.py             # Flask application
├── frontend/
│   ├── dist/              # Built Vue.js app
│   ├── node_modules/      # Node dependencies
│   └── server.js          # Express server
└── deployment/            # Deployment files

/var/log/deception-detector/
├── backend-access.log
└── backend-error.log

/etc/systemd/system/
├── deception-detector-backend.service
└── deception-detector-frontend.service

/etc/nginx/sites-available/
└── deception-detector
```

## Configuration Files

### Backend (.env)

Located at `/opt/deception-detector/backend/.env`

**Critical settings:**
- `FLASK_ENV=production`
- `DEBUG_MODE=False`
- `ALLOWED_ORIGINS` - Set to your domain
- `JWT_SECRET` - Strong random secret
- `API_USERNAME` / `API_PASSWORD` - API credentials

### Nginx

Located at `/etc/nginx/sites-available/deception-detector`

**Update:**
- Replace `yourdomain.com` with your actual domain
- SSL certificate paths (auto-configured by certbot)

## Service Management

```bash
# Backend
sudo systemctl start|stop|restart|status deception-detector-backend

# Frontend
sudo systemctl start|stop|restart|status deception-detector-frontend

# Nginx
sudo systemctl start|stop|restart|reload|status nginx

# View logs
sudo journalctl -u deception-detector-backend -f
sudo journalctl -u deception-detector-frontend -f
```

## Updating the Application

```bash
# Quick update
cd /opt/deception-detector/deployment
sudo ./update.sh

# Or manually
sudo systemctl stop deception-detector-backend deception-detector-frontend
# Update code
cd /opt/deception-detector
# ... update files ...
sudo systemctl start deception-detector-backend deception-detector-frontend
```

## Monitoring

### Health Checks

```bash
# Run health check
sudo /opt/deception-detector/deployment/health-check.sh

# Add to cron for regular monitoring (every 5 minutes)
*/5 * * * * /opt/deception-detector/deployment/health-check.sh >> /var/log/deception-detector/health.log 2>&1
```

### Logs

```bash
# Backend logs
sudo journalctl -u deception-detector-backend -f

# Frontend logs  
sudo journalctl -u deception-detector-frontend -f

# Nginx access log
sudo tail -f /var/log/nginx/deception-detector-access.log

# Nginx error log
sudo tail -f /var/log/nginx/deception-detector-error.log

# Application logs
sudo tail -f /var/log/deception-detector/backend-access.log
sudo tail -f /var/log/deception-detector/backend-error.log
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
sudo journalctl -u deception-detector-backend -n 50 --no-pager
sudo journalctl -u deception-detector-frontend -n 50 --no-pager

# Check if ports are in use
sudo netstat -tlnp | grep :5000
sudo netstat -tlnp | grep :8080

# Check file permissions
ls -la /opt/deception-detector/backend/.env
```

### 502 Bad Gateway

Backend or frontend not responding:

```bash
# Restart services
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend

# Check they're listening
curl http://127.0.0.1:5000/api/models
curl http://127.0.0.1:8080/
```

### SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew manually
sudo certbot renew

# Test auto-renewal
sudo certbot renew --dry-run
```

## Security Checklist

- [ ] Debug mode disabled
- [ ] Strong JWT secret configured
- [ ] API credentials set
- [ ] CORS restricted to your domain
- [ ] Firewall configured (ports 80, 443 open; 5000, 8080 blocked)
- [ ] SSL certificate installed
- [ ] .env file permissions set to 600
- [ ] Regular backups configured
- [ ] SSH key authentication enabled
- [ ] Root SSH login disabled

## Backup

```bash
# Manual backup
sudo tar -czf /backup/deception-detector-$(date +%Y%m%d).tar.gz \
  /opt/deception-detector/backend/.env \
  /opt/deception-detector/backend/models \
  /opt/deception-detector/backend/custom_models

# Automated backup (add to crontab)
0 2 * * * /opt/backup-deception.sh
```

## Support

- **Documentation**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Logs**: Always check logs first for error details
- **Health**: Run `health-check.sh` to verify system status

---

**Ready to deploy?** Start with `check-ready.sh` to validate your setup!
