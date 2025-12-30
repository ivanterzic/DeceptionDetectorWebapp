# Production Deployment & Security Checklist

**Last Updated:** December 30, 2025

> **Quick Start:** For complete deployment instructions, see [deployment/DEPLOYMENT_GUIDE.md](../deployment/DEPLOYMENT_GUIDE.md)

---

##  What's Already Done

All security features are implemented and ready for production:
-  Input validation & sanitization
-  Rate limiting (20/5/60 per minute by endpoint)
-  Security headers (X-Frame-Options, CSP, HSTS, etc.)
-  JWT authentication for public API with SHA256 password hashing
-  Error handling (no stack traces exposed in production)
-  Environment-based configuration (.env file)
-  CORS configuration
-  Path traversal protection
-  SQL injection protection (if database added)

---

##  Automated Deployment

**NEW:** We've created automated deployment scripts!

### Quick Deploy (Recommended)

```bash
# On your local machine - run pre-deployment check
cd webapp
bash deployment/check-ready.sh

# Upload to server
scp -r webapp/ user@your-server:/tmp/

# SSH to server and deploy
ssh user@your-server
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

The automated script handles:
- ✅ System dependencies installation
- ✅ Python/Node.js environment setup
- ✅ Systemd service configuration
- ✅ Nginx reverse proxy with SSL
- ✅ Firewall configuration
- ✅ File permissions
- ✅ Service startup

See [deployment/DEPLOYMENT_GUIDE.md](../deployment/DEPLOYMENT_GUIDE.md) for detailed instructions.

---

##  Pre-Deployment Checklist

### 1. Generate Production Secrets

```bash
python generate_secrets.py
# Copy JWT_SECRET to backend/.env
```

### 2. Configure Environment Variables

Edit `backend/.env`:

```bash
# Production mode
FLASK_ENV=production
DEBUG_MODE=False

# Your domain (for CORS)
ALLOWED_ORIGINS=https://yourdomain.com

# Generated JWT secret (from generate_secrets.py)
JWT_SECRET=your_64_char_secret_here

# Set API credentials for public API
API_USERNAME=your_api_username
API_PASSWORD=your_secure_password
```

### 3. Update Frontend API URL (if needed)

If deploying to a separate API server, update `frontend/src/config.js`:

```javascript
export default {
  apiUrl: 'https://api.yourdomain.com/api'  // Or '/api' for same domain
}
```

### 4. Prepare Server

- [ ] Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- [ ] 4GB+ RAM (8GB+ recommended)
- [ ] 20GB+ storage (50GB+ with models)
- [ ] Root/sudo access
- [ ] Domain DNS configured (A record pointing to server IP)
- [ ] SSH access configured with key authentication

---

##  Security Configuration

All these are handled by the deployment script, but verify manually:

### 1. HTTPS/SSL Certificate

```bash
# Automated by deploy.sh or manually:
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Verify auto-renewal
sudo certbot renew --dry-run
```

### 2. Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (redirects to HTTPS)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 5000/tcp   # Block direct backend access
sudo ufw deny 8080/tcp   # Block direct frontend access
sudo ufw enable

# Verify
sudo ufw status
```

### 3. Nginx Reverse Proxy

Configuration file provided at `deployment/nginx.conf`

Installed to: `/etc/nginx/sites-available/deception-detector`

Key features:
- HTTP to HTTPS redirect
- Modern TLS configuration (TLS 1.2+)
- Security headers (HSTS, CSP, X-Frame-Options)
- Request size limits (50MB for datasets)
- Extended timeouts for AI processing
- Static file caching

### 4. File Permissions

```bash
# Set secure ownership
sudo chown -R www-data:www-data /opt/deception-detector
sudo chown -R www-data:www-data /var/log/deception-detector

# Secure .env file
sudo chmod 600 /opt/deception-detector/backend/.env
```

---

##  Pre-Launch Checklist

- [ ] HTTPS working (test: curl -I https://yourdomain.com)
- [ ] CORS updated (no localhost in config)
- [ ] Debug mode OFF
- [ ] Production secrets set in .env
- [ ] Firewall configured
- [ ] NGINX reverse proxy running
- [ ] Test all API endpoints
- [ ] Rate limiting works (make 30 rapid requests)

---

##  Optional (Recommended)

- Setup logging: /var/log/deception-detector/app.log
- Configure backups (models + config)
- Monitor uptime (Uptime Robot)
- Update dependencies monthly: pip list --outdated

---

##  If Credentials Compromised

```bash
python generate_secrets.py
# Update backend/.env with new values
# Restart backend
```

---

**That's it!** Complete the 6 must-do tasks above and you're ready to deploy.
