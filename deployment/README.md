# Deployment Guide

Linux deployment with HTTPS for Ubuntu/Debian/CentOS.

## SSH Setup

First, ensure you can SSH into your server:

```bash
# Test SSH connection
ssh user@your-server

# If using a key file
ssh -i /path/to/key.pem user@your-server

# For AWS/cloud instances, the user is often:
# - ubuntu@ip-address (Ubuntu)
# - ec2-user@ip-address (Amazon Linux)
# - root@ip-address (most VPS)
```

## Quick Deploy

```bash
# From your local machine, upload the webapp
cd /path/to/DeceptionDetector/webapp
scp -r . user@your-server:/tmp/webapp/

# If using a key file
scp -i /path/to/key.pem -r . user@your-server:/tmp/webapp/

# SSH into server and deploy
ssh user@your-server
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

Enter your domain and email when prompted for automatic HTTPS setup via Let's Encrypt.

## Files

- **deploy.sh** - Complete deployment with HTTPS
- **nginx.conf** - Nginx reverse proxy configuration
- **deception-detector-backend.service** - Backend systemd service
- **deception-detector-frontend.service** - Frontend systemd service
- **health-check.sh** - Health monitoring
- **update.sh** - Quick updates

## What Gets Installed

- Python 3, Node.js, Nginx
- Backend with Gunicorn WSGI server
- Frontend with Express server
- SSL certificate (Let's Encrypt)
- Systemd services for auto-start
- Firewall configuration

## Architecture

```
Internet → Nginx (:443 HTTPS) → Backend (:5000) or Frontend (:8080)
```

## Post-Deployment

1. Edit `/opt/deception-detector/backend/.env` with your API credentials
2. Restart services: `sudo systemctl restart deception-detector-{backend,frontend}`
3. View logs: `journalctl -u deception-detector-backend -f`
4. Access your app at `https://yourdomain.com`

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
