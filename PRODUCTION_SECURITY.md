# Production Deployment Security Checklist

**Document Version:** 1.1  
**Last Updated:** November 4, 2025  
**Application:** Deception Detector Web Application

---

## 📋 Overview

This document provides a comprehensive security checklist for deploying the Deception Detector application to production. Follow these steps to ensure a secure deployment.

## ⚠️ Important: Authentication Design Decision

**This system is designed WITHOUT user authentication, authorization, or RBAC (Role-Based Access Control).** This is an intentional architectural decision based on the application's use case and deployment environment.

### ✅ Security Measures Already Implemented in Development:

The following security features have been implemented and are ready for production:

- **Input Validation & Sanitization** ✅
  - Text input validation (max 1300 characters, null byte removal, XSS detection)
  - Model key validation (path traversal prevention)
  - Model code validation (6-character alphanumeric format)
  - CSV file validation (type, size max 100MB, filename sanitization)
  - Training parameter validation (epochs, batch size, learning rate, validation split)

- **Rate Limiting** ✅
  - Analysis endpoints: 20 requests/minute
  - Training endpoints: 5 requests/minute
  - Default endpoints: 60 requests/minute
  - Thread-safe in-memory rate limiter for development

- **CORS Configuration** ✅
  - Restricted to localhost (ports 8080, 3000) in development
  - Ready to be updated with production domains

- **Security Headers** ✅
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: 1; mode=block
  - Referrer-Policy: strict-origin-when-cross-origin
  - Content-Security-Policy: default-src 'self'

- **Error Message Sanitization** ✅
  - No stack traces exposed to clients
  - Generic error messages prevent information leakage
  - Detailed errors logged server-side only

### 🔄 Remaining Production Tasks:

The checklist below focuses on infrastructure and deployment security measures that still need to be implemented for production deployment.

---

## ✅ Pre-Deployment Checklist

### 1. HTTPS/TLS Configuration

**Priority:** 🔴 CRITICAL

**What to do:**
- [ ] Install SSL/TLS certificate (Let's Encrypt recommended)
- [ ] Configure NGINX or Apache as reverse proxy with HTTPS
- [ ] Redirect all HTTP traffic to HTTPS
- [ ] Enable HSTS (HTTP Strict Transport Security)
- [ ] Set minimum TLS version to 1.2 or higher

**How to implement:**

```nginx
# NGINX Configuration Example
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
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Let's Encrypt Certificate Installation:**
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

---

### 2. Authentication & Authorization

**Priority:** ⚪ NOT APPLICABLE

**Note:** This application is intentionally designed **WITHOUT** authentication, authorization, or RBAC. The system does not require user accounts, login functionality, or access control beyond network-level restrictions.

**Security is achieved through:**
- Input validation ✅ (already implemented)
- Rate limiting ✅ (already implemented)
- Network-level access control (firewall, VPN)
- CORS restrictions (localhost in dev, production domain in prod)

**This section can be ignored for this application.**

---

### 3. CORS Configuration - **UPDATE FOR PRODUCTION**

**Priority:** 🔴 CRITICAL

**Status:** ✅ Implemented for development, needs production update

**Current state (Development):**
```python
# backend/config.py
ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
```

**What to do:**
- [ ] Update `ALLOWED_ORIGINS` in `backend/config.py` with production domain(s)
- [ ] Remove localhost entries for production

**How to implement for production:**

```python
# backend/config.py - UPDATE THIS FOR PRODUCTION
ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com'
]
```

**Current CORS configuration** (already implemented in `backend/app.py`):
```python
from flask_cors import CORS
from config import ALLOWED_ORIGINS

CORS(app, resources={
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})
```

---

### 4. Rate Limiting - **UPGRADE FOR PRODUCTION**

**Priority:** 🟠 HIGH

**Status:** ✅ Implemented for development with in-memory storage

**Current state:**
- ✅ Rate limiting decorator implemented (`@rate_limit`)
- ✅ Applied to all API endpoints
- ✅ Analysis: 20/min, Training: 5/min, Default: 60/min
- ⚠️ Uses in-memory storage (not suitable for multi-instance production)

**What to do for production:**
- [ ] Upgrade to Redis-backed rate limiter for multi-instance support
- [ ] Consider CDN (Cloudflare) for additional DDoS protection
- [ ] Add NGINX rate limiting as additional layer

**How to upgrade to Redis for production:**

```python
# backend/requirements.txt - add:
# redis==5.0.1

# backend/security.py - UPDATE RateLimiter class
import redis
import time
from threading import Lock

class RateLimiter:
    def __init__(self, redis_url='redis://localhost:6379'):
        """Rate limiter using Redis for multi-instance support"""
        self.redis_client = redis.from_url(redis_url)
    
    def is_allowed(self, identifier, limit=10, window=60):
        """Check if request is allowed under rate limit"""
        key = f"rate_limit:{identifier}"
        current_time = time.time()
        
        pipe = self.redis_client.pipeline()
        pipe.zadd(key, {current_time: current_time})
        pipe.zremrangebyscore(key, 0, current_time - window)
        pipe.zcard(key)
        pipe.expire(key, window)
        results = pipe.execute()
        
        request_count = results[2]
        return request_count <= limit

# backend/config.py - add:
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
```

**NGINX Rate Limiting:**

```nginx
# In nginx.conf
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=train_limit:10m rate=1r/m;

    server {
        location /api/analyze {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://localhost:5000;
        }

        location /api/train {
            limit_req zone=train_limit burst=2;
            proxy_pass http://localhost:5000;
        }
    }
}
```

---

### 5. Input Validation & Sanitization

**Priority:** 🔴 CRITICAL

**Status:** ✅ FULLY IMPLEMENTED

All input validation has been implemented in `backend/security.py`:

- ✅ `validate_text_input()` - Text sanitization, max 1300 chars, null byte removal, XSS detection
- ✅ `validate_model_key()` - Path traversal prevention for model keys
- ✅ `validate_model_code()` - 6-character alphanumeric validation
- ✅ `validate_csv_file()` - File type, size (100MB max), filename sanitization
- ✅ `validate_training_params()` - Training parameter validation (epochs, batch size, learning rate, validation split)

**Applied to all endpoints in:**
- `backend/routes.py` - Main API routes
- `backend/training_routes.py` - Training and custom model routes

**No additional action required for production.**

---

### 6. Secrets Management

**Priority:** 🔴 CRITICAL

**What to do:**
- [ ] Create `.env` file for production secrets (never commit to Git)
- [ ] Use environment variables for sensitive configuration
- [ ] Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault) for larger deployments
- [ ] Generate secure random secrets for Flask

**Important secrets to set:**
- `FLASK_SECRET_KEY` - Flask session encryption
- `REDIS_URL` - Redis connection string (if using Redis rate limiter)
- `ALLOWED_ORIGINS` - Production domain(s)

**How to implement:**

**Create `.env` file (add to .gitignore):**

```bash
# .env (NEVER COMMIT THIS FILE)
FLASK_SECRET_KEY=your-very-long-random-secret-key-here
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Load environment variables:**

```python
# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("FLASK_SECRET_KEY must be set in environment")
    
    REDIS_URL = os.environ.get('REDIS_URL', 'memory://')
    
    # Parse ALLOWED_ORIGINS from environment
    origins_str = os.environ.get('ALLOWED_ORIGINS', '')
    ALLOWED_ORIGINS = [origin.strip() for origin in origins_str.split(',') if origin.strip()]
    
    # Validate required secrets
    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise ValueError("Missing required config: SECRET_KEY")
        if not cls.ALLOWED_ORIGINS:
            raise ValueError("Missing required config: ALLOWED_ORIGINS")

# backend/app.py
app.config.from_object(Config)
Config.validate()
```

**Generate secure random secrets:**

```bash
# Generate secure random keys
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### 7. Resource Limits & DoS Prevention

**Priority:** 🟠 HIGH

**What to do:**
- [ ] Set memory limits for model training
- [ ] Set CPU/GPU usage limits
- [ ] Limit concurrent training jobs
- [ ] Implement job queuing system
- [ ] Set timeouts for long-running operations

**How to implement:**

**Docker Resource Limits:**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# ... existing setup ...

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    restart: unless-stopped
```

**Job Queue Implementation (Celery):**

```python
# backend/requirements.txt - add:
# celery==5.3.4
# redis==5.0.1

# backend/celery_app.py
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

celery.conf.update(
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3300,  # 55 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=10,
)

@celery.task(bind=True, max_retries=0)
def train_model_task(self, model_code, dataset, config):
    """Background task for model training"""
    try:
        # ... training code ...
        return {'status': 'completed', 'model_code': model_code}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}

# backend/routes.py
@app.route('/api/train', methods=['POST'])
def start_training():
    # ... validation ...
    task = train_model_task.delay(model_code, dataset, config)
    return jsonify({
        'task_id': task.id,
        'model_code': model_code,
        'status': 'queued'
    })

@app.route('/api/train/<task_id>/status', methods=['GET'])
def get_training_status(task_id):
    task = train_model_task.AsyncResult(task_id)
    return jsonify({
        'status': task.state,
        'result': task.result if task.ready() else None
    })
```

---

### 8. File System Security

**Priority:** 🟠 HIGH

**What to do:**
- [ ] Set proper file permissions on model directory
- [ ] Prevent directory traversal attacks
- [ ] Isolate user uploads in separate directories
- [ ] Clean up temporary files
- [ ] Set disk usage quotas

**How to implement:**

```python
# backend/file_security.py
import os
from pathlib import Path

MODELS_DIR = Path('/var/app/models')
UPLOADS_DIR = Path('/var/app/uploads')
MAX_DISK_USAGE = 50 * 1024 * 1024 * 1024  # 50 GB

def secure_path(base_dir, filename):
    """Prevent path traversal attacks"""
    base_dir = Path(base_dir).resolve()
    target_path = (base_dir / filename).resolve()
    
    # Ensure the target path is within base_dir
    if not str(target_path).startswith(str(base_dir)):
        raise ValueError("Invalid file path")
    
    return target_path

def check_disk_usage():
    """Check if disk usage is within limits"""
    total_size = sum(f.stat().st_size for f in MODELS_DIR.rglob('*') if f.is_file())
    if total_size > MAX_DISK_USAGE:
        raise RuntimeError("Disk usage limit exceeded")
    return total_size

def cleanup_old_models():
    """Remove models older than 7 days"""
    import time
    cutoff = time.time() - (7 * 24 * 60 * 60)
    
    for model_dir in MODELS_DIR.iterdir():
        if model_dir.is_dir() and model_dir.stat().st_mtime < cutoff:
            shutil.rmtree(model_dir)
```

**Set proper permissions (Linux):**

```bash
# Create dedicated user
sudo useradd -r -s /bin/false deception-app

# Set ownership and permissions
sudo chown -R deception-app:deception-app /var/app/models
sudo chmod 750 /var/app/models
sudo chmod 640 /var/app/models/*

# Models should be readable only by app user
find /var/app/models -type f -exec chmod 640 {} \;
find /var/app/models -type d -exec chmod 750 {} \;
```

---

### 9. Logging & Monitoring

**Priority:** 🟠 HIGH

**What to do:**
- [ ] Implement centralized logging
- [ ] Log security events (failed auth, suspicious requests)
- [ ] Set up alerting for errors and anomalies
- [ ] Monitor resource usage
- [ ] Do NOT log sensitive data (passwords, tokens)

**How to implement:**

```python
# backend/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
        }
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

# Configure logging
def setup_logging(app):
    # File handler
    file_handler = RotatingFileHandler(
        '/var/log/deception-detector/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

# backend/middleware.py
@app.before_request
def log_request():
    app.logger.info(f"Request: {request.method} {request.path}", extra={
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string
    })

@app.after_request
def log_response(response):
    if response.status_code >= 400:
        app.logger.warning(f"Response: {response.status_code}", extra={
            'path': request.path,
            'method': request.method,
            'ip': request.remote_addr
        })
    return response

# Log security events
def log_security_event(event_type, details):
    app.logger.warning(f"Security Event: {event_type}", extra={
        'event': event_type,
        'details': details,
        'ip': request.remote_addr,
        'timestamp': datetime.utcnow().isoformat()
    })
```

**Prometheus Monitoring (Optional):**

```python
# backend/requirements.txt - add:
# prometheus-flask-exporter==0.22.4

# backend/app.py
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Custom metrics
model_training_counter = metrics.counter(
    'model_training_total', 'Total number of model training requests'
)

analysis_histogram = metrics.histogram(
    'analysis_duration_seconds', 'Time spent processing analysis'
)
```

---

### 10. Database Security (If Applicable)

**Priority:** ⚪ NOT CURRENTLY APPLICABLE

**Note:** The application currently does not use a persistent database. Model metadata and training status are stored in JSON files on the filesystem.

**If you decide to add a database in the future:**
- Use parameterized queries (prevent SQL injection)
- Encrypt sensitive data at rest
- Use SSL/TLS for database connections
- Implement database backups
- Use principle of least privilege for DB users

**This section can be ignored for current deployment.**

---

### 11. Backup & Disaster Recovery

**Priority:** 🟡 MEDIUM

**What to do:**
- [ ] Implement automated backups
- [ ] Test backup restoration regularly
- [ ] Store backups in a separate location
- [ ] Document recovery procedures

**How to implement:**

```bash
#!/bin/bash
# backup.sh - Run daily via cron

BACKUP_DIR="/var/backups/deception-detector"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup models
tar -czf "$BACKUP_DIR/models_$DATE.tar.gz" /var/app/models/

# Backup database (if applicable)
pg_dump deception_db > "$BACKUP_DIR/db_$DATE.sql"

# Backup configs
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" /etc/deception-detector/

# Clean up backups older than 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 sync $BACKUP_DIR s3://your-backup-bucket/
```

**Crontab entry:**

```bash
# Run daily at 2 AM
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

---

### 12. Dependency Security

**Priority:** 🟠 HIGH

**What to do:**
- [ ] Regularly update dependencies
- [ ] Scan for known vulnerabilities
- [ ] Pin dependency versions
- [ ] Use virtual environments

**How to implement:**

```bash
# Install security scanning tools
pip install safety pip-audit

# Scan for known vulnerabilities
safety check
pip-audit

# Update dependencies (test thoroughly first!)
pip list --outdated
pip install --upgrade package-name

# Pin versions in requirements.txt
pip freeze > requirements.txt
```

**GitHub Dependabot (if using GitHub):**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
  
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
```

---

## 🚀 Deployment Steps

### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3-pip nodejs npm nginx redis-server postgresql

# Create app user
sudo useradd -r -m -s /bin/bash deception-app

# Create directories
sudo mkdir -p /var/app/deception-detector
sudo mkdir -p /var/log/deception-detector
sudo mkdir -p /var/app/models
sudo chown -R deception-app:deception-app /var/app /var/log/deception-detector
```

### Step 2: Deploy Application

```bash
# Clone repository (as deception-app user)
sudo -u deception-app git clone https://github.com/yourusername/deception-detector.git /var/app/deception-detector

# Setup backend
cd /var/app/deception-detector/backend
sudo -u deception-app python3 -m venv venv
sudo -u deception-app venv/bin/pip install -r requirements.txt

# Setup frontend
cd /var/app/deception-detector/frontend
sudo -u deception-app npm install
sudo -u deception-app npm run build

# Download models
cd /var/app/deception-detector
sudo -u deception-app python3 download_models.py
```

### Step 3: Configure Services

**Create systemd service for backend:**

```ini
# /etc/systemd/system/deception-backend.service
[Unit]
Description=Deception Detector Backend
After=network.target

[Service]
Type=simple
User=deception-app
WorkingDirectory=/var/app/deception-detector/backend
Environment="PATH=/var/app/deception-detector/backend/venv/bin"
ExecStart=/var/app/deception-detector/backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable deception-backend
sudo systemctl start deception-backend
sudo systemctl status deception-backend
```

### Step 4: Configure NGINX

```bash
# Copy NGINX config from earlier
sudo nano /etc/nginx/sites-available/deception-detector

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/deception-detector /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart NGINX
sudo systemctl restart nginx
```

### Step 5: Setup SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com
```

### Step 6: Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

---

## 🔍 Post-Deployment Verification

### Checklist:

- [ ] HTTPS working correctly (test with https://www.ssllabs.com/ssltest/)
- [ ] All HTTP redirects to HTTPS
- [ ] API endpoints require authentication (if implemented)
- [ ] Rate limiting is active (test by making rapid requests)
- [ ] CORS policy is restrictive (test from unauthorized domain)
- [ ] Logs are being written correctly
- [ ] Backups are running (check backup directory)
- [ ] Services restart automatically on server reboot
- [ ] Error pages don't expose sensitive information
- [ ] Health checks are responding

### Test Commands:

```bash
# Test HTTPS
curl -I https://yourdomain.com

# Test rate limiting
for i in {1..100}; do curl https://yourdomain.com/api/models; done

# Test authentication (should return 401)
curl https://yourdomain.com/api/analyze -X POST

# Check logs
sudo tail -f /var/log/deception-detector/app.log

# Check service status
sudo systemctl status deception-backend

# Test backup
sudo /usr/local/bin/backup.sh
```

---

## 📊 Monitoring Checklist

Set up monitoring for:

- [ ] Server uptime and availability
- [ ] API response times
- [ ] Error rates (4xx, 5xx responses)
- [ ] Disk usage
- [ ] Memory usage
- [ ] CPU usage
- [ ] Number of active users/requests
- [ ] Model training queue length

**Tools to consider:**
- Prometheus + Grafana (metrics)
- ELK Stack (logs)
- Uptime Robot (uptime monitoring)
- Sentry (error tracking)

---

## 🆘 Incident Response

### If you detect a security breach:

1. **Isolate:** Disconnect affected systems
2. **Assess:** Determine scope of breach
3. **Contain:** Stop further damage
4. **Eradicate:** Remove threat
5. **Recover:** Restore from backups
6. **Review:** Analyze what went wrong
7. **Improve:** Update security measures

### Emergency Contacts:

- Server admin: [contact info]
- Security team: [contact info]
- Hosting provider support: [contact info]

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [NGINX Security Tips](https://www.nginx.com/blog/mitigating-ddos-attacks-with-nginx-and-nginx-plus/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

## 📝 Update Log

| Date | Changes | Author |
|------|---------|--------|
| 2025-11-04 | Initial version | [Your name] |

---

**Remember:** Security is an ongoing process, not a one-time setup. Review and update this checklist regularly!
