# Production Deployment Checklist

**Last Updated:** November 10, 2025

---

##  What's Already Done

All security features are implemented:
-  Input validation & sanitization
-  Rate limiting (10/20/60 per minute)
-  Security headers (X-Frame-Options, CSP, etc.)
-  JWT authentication for public API
-  Error handling (no stack traces exposed)
-  .env file configuration

---

##  Must Do Before Deployment

### 1. Setup HTTPS

```bash
# Install certificate (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 2. Update CORS in backend/config.py

**Change:**
```python
ALLOWED_ORIGINS = ['http://localhost:8080', 'http://localhost:3000']
```

**To:**
```python
ALLOWED_ORIGINS = ['https://yourdomain.com']
```

### 3. Disable Debug Mode in backend/.env

```bash
FLASK_ENV=production
DEBUG_MODE=False
```

### 4. Generate Production Secrets

```bash
python generate_secrets.py
# Copy values to backend/.env
```

### 5. Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (redirect)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 5000/tcp   # Block direct backend access
sudo ufw enable
```

### 6. Setup NGINX Reverse Proxy

Create /etc/nginx/sites-available/deception-detector:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:8080;  # Frontend
        proxy_set_header Host $host;
    }

    location /api {
        proxy_pass http://localhost:5000;  # Backend
        proxy_set_header Host $host;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
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
