# Production Deployment Checklist

Print this checklist and check off each item as you complete your deployment.

---

## Pre-Deployment

### Local Preparation
- [ ] Run `bash deployment/check-ready.sh` to validate files
- [ ] Generate JWT secret: `python3 generate_secrets.py`
- [ ] Choose API username and password
- [ ] Commit all code changes to version control

### Server Preparation
- [ ] Server is running (Ubuntu 20.04+, Debian 11+, or CentOS 8+)
- [ ] 4GB+ RAM available (8GB+ recommended)
- [ ] 20GB+ storage available (50GB+ recommended)
- [ ] Root/sudo access confirmed
- [ ] SSH access working
- [ ] Domain purchased (if using custom domain)
- [ ] DNS A record configured pointing to server IP

---

## Deployment Process

### Upload & Execute
- [ ] Upload files: `scp -r webapp/ user@server:/tmp/`
- [ ] SSH to server: `ssh user@server`
- [ ] Navigate to deployment: `cd /tmp/webapp/deployment`
- [ ] Make script executable: `chmod +x deploy.sh`
- [ ] Run deployment: `sudo ./deploy.sh`
- [ ] Enter domain name when prompted
- [ ] Enter email for SSL certificate when prompted
- [ ] Wait for installation to complete (15-45 minutes)

### Automated by Script
- [x] System dependencies installed
- [x] Python virtual environment created
- [x] Node.js dependencies installed
- [x] Systemd services configured
- [x] Nginx reverse proxy setup
- [x] SSL certificate obtained
- [x] Firewall configured
- [x] Services started

---

## Post-Deployment Configuration

### Backend Configuration
- [ ] Edit backend/.env: `sudo nano /opt/deception-detector/backend/.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG_MODE=False`
- [ ] Set `ALLOWED_ORIGINS=https://yourdomain.com`
- [ ] Set `JWT_SECRET=<your-64-char-secret>`
- [ ] Set `API_USERNAME=<your-username>`
- [ ] Set `API_PASSWORD=<your-password>`
- [ ] Save and exit (Ctrl+X, Y, Enter)
- [ ] Restart backend: `sudo systemctl restart deception-detector-backend`

### Verify Services
- [ ] Backend running: `sudo systemctl status deception-detector-backend`
- [ ] Frontend running: `sudo systemctl status deception-detector-frontend`
- [ ] Nginx running: `sudo systemctl status nginx`

---

## Testing

### Basic Functionality
- [ ] Visit https://yourdomain.com (should load without errors)
- [ ] HTTPS working (no certificate warnings)
- [ ] HTTP redirects to HTTPS
- [ ] Analysis page loads
- [ ] Fine-tuning page loads
- [ ] Test text analysis with any model

### API Testing
- [ ] Login endpoint: `POST /api/auth/login`
- [ ] Get JWT token successfully
- [ ] Test checkDeception endpoint with token
- [ ] Verify SHAP/LIME explanations returned

### Security Testing
- [ ] Direct backend blocked: `curl http://yourdomain.com:5000` (should fail)
- [ ] Direct frontend blocked: `curl http://yourdomain.com:8080` (should fail)
- [ ] Firewall status: `sudo ufw status` (22, 80, 443 allowed only)
- [ ] Test rate limiting (25 rapid requests should get 429 error)
- [ ] Security headers: Visit https://securityheaders.com
- [ ] SSL test: Visit https://www.ssllabs.com/ssltest/

---

## Security Hardening

### Essential Security
- [ ] Debug mode disabled (DEBUG_MODE=False)
- [ ] CORS restricted to production domain only
- [ ] Strong JWT secret (64+ characters)
- [ ] API credentials set and complex
- [ ] .env file permissions: `sudo chmod 600 /opt/deception-detector/backend/.env`
- [ ] Services owned by www-data: `sudo chown -R www-data:www-data /opt/deception-detector`

### Additional Security (Recommended)
- [ ] SSH key authentication enabled
- [ ] Password authentication disabled: Edit `/etc/ssh/sshd_config`
- [ ] Root SSH login disabled: `PermitRootLogin no`
- [ ] fail2ban installed: `sudo apt install fail2ban`
- [ ] Automatic security updates: `sudo apt install unattended-upgrades`
- [ ] Change default SSH port (optional)

---

## Backup Setup

### Configure Backups
- [ ] Test backup script: `sudo /opt/backup-deception.sh`
- [ ] Verify backup created in `/backup/`
- [ ] Add to crontab: `sudo crontab -e`
- [ ] Add line: `0 2 * * * /opt/backup-deception.sh`
- [ ] Test backup restoration process

---

## Monitoring Setup

### Health Monitoring
- [ ] Test health check: `sudo /opt/deception-detector/deployment/health-check.sh`
- [ ] All checks pass
- [ ] Add to cron for regular checks (optional)
- [ ] Configure log rotation (handled by deployment)

### Log Management
- [ ] Know how to view logs: `sudo journalctl -u deception-detector-backend -f`
- [ ] Nginx logs location: `/var/log/nginx/deception-detector-*.log`
- [ ] Application logs: `/var/log/deception-detector/`

---

## Documentation

### Save Important Information
- [ ] Document server IP address: ________________
- [ ] Document domain name: ________________
- [ ] Document API username: ________________
- [ ] Document API password location (secure storage)
- [ ] Document JWT secret location (secure storage)
- [ ] Save backup of .env file (encrypted, off-server)

### Access Information
- [ ] SSH connection: `ssh user@________________`
- [ ] Application URL: `https://________________`
- [ ] Nginx config: `/etc/nginx/sites-available/deception-detector`
- [ ] Backend config: `/opt/deception-detector/backend/.env`
- [ ] Service logs: `sudo journalctl -u deception-detector-backend`

---

## Maintenance Schedule

### Daily (Automated)
- [x] Backups run (2 AM)
- [x] SSL certificate auto-renewal check
- [x] Log rotation

### Weekly (Manual)
- [ ] Check disk space: `df -h`
- [ ] Review error logs
- [ ] Monitor memory usage: `free -h`

### Monthly (Manual)
- [ ] System updates: `sudo apt update && sudo apt upgrade`
- [ ] Review security logs
- [ ] Test backup restoration
- [ ] Review application performance

---

## Emergency Contacts

### Support Resources
- **Deployment Guide**: /opt/deception-detector/deployment/DEPLOYMENT_GUIDE.md
- **Quick Reference**: /opt/deception-detector/deployment/QUICK_REFERENCE.md
- **Security Guide**: /opt/deception-detector/docs/PRODUCTION_SECURITY.md

### Quick Commands
- **Restart Everything**: `sudo systemctl restart deception-detector-backend deception-detector-frontend && sudo systemctl reload nginx`
- **View Logs**: `sudo journalctl -u deception-detector-backend -f`
- **Health Check**: `sudo /opt/deception-detector/deployment/health-check.sh`

---

## Final Verification

### Go-Live Checklist
- [ ] All above items completed
- [ ] Application accessible at production URL
- [ ] HTTPS working correctly
- [ ] All features tested and working
- [ ] API authentication working
- [ ] Security tests passed
- [ ] Backups configured and tested
- [ ] Team trained on maintenance procedures
- [ ] Emergency procedures documented

---

## Sign-Off

**Deployed by:** _______________________  **Date:** ___________

**Verified by:** _______________________  **Date:** ___________

**Notes:**
________________________________________________________________
________________________________________________________________
________________________________________________________________
________________________________________________________________

---

**Deployment Status:** 
- [ ] Development
- [ ] Staging
- [ ] **Production** ✅

**Next Review Date:** ___________

---

*Keep this checklist for reference and future deployments*
