# 🚀 Quick Deployment Reference

**Target**: Traditional Linux server (VPS, dedicated server, cloud VM with terminal access)

---

## ⚡ Ultra-Quick Start (5 minutes)

```bash
# On local machine
cd webapp
scp -r . user@your-server:/tmp/webapp/

# On server
ssh user@your-server
cd /tmp/webapp/deployment
chmod +x deploy.sh
sudo ./deploy.sh
# Follow prompts for domain name and email
```

**That's it!** The script handles everything automatically.

---

## 📦 What You Need

- **Server**: Ubuntu 20.04+, 4GB+ RAM, 20GB+ storage
- **Access**: Root/sudo via SSH
- **Domain**: DNS pointing to server IP (optional but recommended)
- **Time**: 15-45 minutes (depending on model download)

---

## 📂 Files Created

After deployment:

```
/opt/deception-detector/          # Application
/var/log/deception-detector/      # Logs
/etc/systemd/system/              # Services
/etc/nginx/sites-available/       # Nginx config
/etc/letsencrypt/                 # SSL certificates
```

---

## 🔧 Essential Commands

### Service Control
```bash
# Start/stop/restart
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend
sudo systemctl reload nginx

# Check status
sudo systemctl status deception-detector-backend --no-pager

# View logs
sudo journalctl -u deception-detector-backend -f
```

### Configuration
```bash
# Edit backend config
sudo nano /opt/deception-detector/backend/.env

# Edit Nginx config
sudo nano /etc/nginx/sites-available/deception-detector

# Test Nginx config
sudo nginx -t

# After changes - restart services
sudo systemctl restart deception-detector-backend
sudo systemctl reload nginx
```

### Monitoring
```bash
# Health check
sudo /opt/deception-detector/deployment/health-check.sh

# View all logs
sudo journalctl -u deception-detector-backend -f
sudo tail -f /var/log/nginx/deception-detector-access.log
sudo tail -f /var/log/nginx/deception-detector-error.log
```

### Maintenance
```bash
# Update application
sudo /opt/deception-detector/deployment/update.sh

# Backup
sudo /opt/backup-deception.sh

# Check disk space
df -h /opt/deception-detector

# Check memory
free -h
```

---

## ⚙️ Must Configure (After Deployment)

### 1. Backend Environment (.env)

```bash
sudo nano /opt/deception-detector/backend/.env
```

**Required settings:**
- `FLASK_ENV=production`
- `DEBUG_MODE=False`
- `ALLOWED_ORIGINS=https://yourdomain.com`
- `JWT_SECRET=<64-char-secret>`
- `API_USERNAME=<your-username>`
- `API_PASSWORD=<your-password>`

### 2. Generate JWT Secret

```bash
cd /opt/deception-detector
python3 generate_secrets.py
# Copy JWT_SECRET to backend/.env
```

### 3. Restart After Config Changes

```bash
sudo systemctl restart deception-detector-backend
```

---

## 🔒 Security Checklist

- [ ] HTTPS enabled (Let's Encrypt certificate)
- [ ] Firewall configured (UFW: allow 22,80,443; deny 5000,8080)
- [ ] Debug mode disabled
- [ ] CORS restricted to your domain
- [ ] Strong JWT secret (64+ chars)
- [ ] API credentials set
- [ ] .env file permissions = 600
- [ ] Services owned by www-data user

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
sudo journalctl -u deception-detector-backend -n 50 --no-pager
# Check for missing .env or permission errors
```

### 502 Bad Gateway
```bash
# Check if services are running
sudo systemctl status deception-detector-backend
sudo systemctl status deception-detector-frontend

# Test directly
curl http://127.0.0.1:5000/api/models
curl http://127.0.0.1:8080/
```

### High Memory
```bash
free -h
# Restart services if needed
sudo systemctl restart deception-detector-backend
```

### SSL Certificate Issues
```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

---

## 📊 Architecture

```
Internet
    ↓
Nginx (:443 HTTPS)
    ├─→ Frontend (:8080) → Express → Vue.js (built)
    └─→ Backend (:5000) → Gunicorn → Flask API
```

**Ports:**
- 443: HTTPS (public)
- 80: HTTP → redirects to 443 (public)
- 5000: Backend (internal only)
- 8080: Frontend (internal only)

---

## 📖 Documentation

- **Complete Guide**: [deployment/DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Security**: [docs/PRODUCTION_SECURITY.md](../docs/PRODUCTION_SECURITY.md)
- **API Usage**: [docs/API_USAGE.md](../docs/API_USAGE.md)
- **Deployment Files**: [deployment/README.md](README.md)

---

## 🆘 Quick Fixes

### Restart Everything
```bash
sudo systemctl restart deception-detector-backend
sudo systemctl restart deception-detector-frontend
sudo systemctl reload nginx
```

### Check All Services
```bash
sudo systemctl status deception-detector-backend --no-pager
sudo systemctl status deception-detector-frontend --no-pager
sudo systemctl status nginx --no-pager
```

### View Recent Errors
```bash
sudo journalctl -u deception-detector-backend -n 50 --no-pager
```

### Free Up Memory
```bash
sudo systemctl restart deception-detector-backend
# Wait for service to fully restart
sleep 5
```

### Renew SSL Certificate
```bash
sudo certbot renew
sudo systemctl reload nginx
```

---

## 🎯 Performance Tuning

### For High Traffic
```bash
# Increase workers in service file
sudo nano /etc/systemd/system/deception-detector-backend.service
# Change: --workers 4 → --workers 8

sudo systemctl daemon-reload
sudo systemctl restart deception-detector-backend
```

### For GPU Servers
```bash
# Verify GPU detected
nvidia-smi

# Check if backend is using GPU
sudo journalctl -u deception-detector-backend | grep -i gpu
```

---

## 🔄 Regular Maintenance

**Weekly:**
- Check logs for errors
- Monitor disk space
- Verify backups are running

**Monthly:**
- Update system packages: `sudo apt update && sudo apt upgrade`
- Review security logs
- Test backup restoration

**As Needed:**
- Update application code
- Renew SSL (auto-renewed by certbot)
- Scale resources if traffic increases

---

## 💾 Backup & Restore

### Backup
```bash
sudo /opt/backup-deception.sh
# Saves to: /backup/deception-detector-YYYYMMDD_HHMMSS.tar.gz
```

### Restore
```bash
sudo tar -xzf /backup/deception-detector-YYYYMMDD.tar.gz -C /tmp/
sudo cp /tmp/backup-dir/* /opt/deception-detector/backend/ -r
sudo chown -R www-data:www-data /opt/deception-detector
sudo systemctl restart deception-detector-backend
```

---

## 📞 Getting Help

1. **Check logs first**: `sudo journalctl -u deception-detector-backend -n 100 --no-pager`
2. **Run health check**: `sudo /opt/deception-detector/deployment/health-check.sh`
3. **Review documentation**: See links above
4. **Test endpoints**: `curl http://127.0.0.1:5000/api/models`

---

**Ready to deploy?** Run `./deploy.sh` and you'll be live in 15-45 minutes! 🚀
