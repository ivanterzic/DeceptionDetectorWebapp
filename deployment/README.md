# Deception Detector - Docker Deployment Guide


```bash
cd ~/deception-detector/webapp
sudo bash deployment/docker-deploy.sh
```
The script will:
- Install Docker and Docker Compose
- Create environment files
- Build Docker images
- Start all containers

### 3. Access Application

- **HTTP:** `http://your-server-ip` or `http://localhost`
- **Frontend:** Port 8080
- **Backend:** Port 5000

---

## Configuration

### Backend Configuration

Edit the environment file:

```bash
nano ~/deception-detector/webapp/backend/.env
```

Required settings:

```bash
API_USERNAME=your_username
API_PASSWORD=your_secure_password
JWT_SECRET=generated_secret
DEBUG_MODE=False
ALLOWED_ORIGINS=http://your-domain.com,http://localhost
```

After editing, restart containers:

```bash
cd ~/deception-detector/webapp
docker-compose restart backend
```

---

## Docker Commands

### View Status

```bash
cd ~/deception-detector/webapp
docker-compose ps
```

### View Logs

```bash
# All containers
docker-compose logs -f

# Specific container
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### Start/Stop/Restart

```bash
# Start all
docker-compose start

# Stop all
docker-compose stop

# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Remove Everything

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove containers, volumes, and images
docker-compose down -v --rmi all
```

---

## Enabling HTTPS

### Option 1: With Domain Name (Recommended)

**Prerequisites:**
1. Domain name pointing to your server
2. Ports 80 and 443 open in firewall
3. Containers running

**Setup:**
```bash
cd ~/deception-detector/webapp
sudo bash deployment/docker-setup-ssl.sh
```

Follow the prompts to:
- Enter your domain name
- Enter your email address

The script will:
- Obtain SSL certificate from Let's Encrypt
- Update nginx configuration
- Enable HTTPS

**Certificate Renewal:**

Certificates auto-renew via certbot's systemd timer. To manually renew:

```bash
sudo certbot renew
docker-compose restart nginx
```

---

### Option 2: With IP Address (Self-Signed Certificate)

**When to use:**
- Don't have a domain name
- Testing/development environments
- Internal networks

**⚠️ Important Notes:**
- Browsers will show security warnings
- Users must manually accept the certificate
- Not recommended for production
- Consider using a cheap domain ($1-2/year) with Let's Encrypt instead

**Setup:**

```bash
cd ~/deception-detector/webapp/deployment
sudo bash setup-ip-ssl.sh
```

Follow the prompts:
1. Enter your server's IP address
2. Confirm you understand about browser warnings

The script will:
- Generate a 2048-bit RSA private key
- Create a self-signed certificate (valid 365 days)
- Configure nginx for HTTPS
- Update docker-compose.yml automatically

**Manual Setup (if script fails):**

If the script doesn't auto-update docker-compose.yml:

```bash
cd ~/deception-detector/webapp
nano docker-compose.yml
```

Update the nginx volumes section:
```yaml
nginx:
  volumes:
    - ./deployment/nginx-docker-ssl.conf:/etc/nginx/conf.d/default.conf:ro
    - ./deployment/ssl:/etc/nginx/ssl:ro
```

Then restart:
```bash
docker-compose restart nginx
```

**Accessing with Self-Signed Certificate:**

1. Navigate to `https://YOUR_IP`
2. Browser shows "Your connection is not private" warning
3. Click "Advanced" or "Details"
4. Click "Proceed to [IP] (unsafe)" or "Accept the Risk"
5. Application will load normally

**Certificate Renewal:**

Self-signed certificates expire after 365 days. To renew:

```bash
cd ~/deception-detector/webapp/deployment
sudo bash setup-ip-ssl.sh
# Enter same IP address
docker-compose restart nginx
```

---

## Monitoring

### Check Container Health

```bash
docker-compose ps
```

Healthy containers show "Up" status.

### Resource Usage

```bash
# All containers
docker stats

# Specific container
docker stats deception-detector-backend
```

### Access Container Shell

```bash
# Backend
docker exec -it deception-detector-backend bash

# Frontend
docker exec -it deception-detector-frontend sh

# Nginx
docker exec -it deception-detector-nginx sh
```

### Test API

```bash
# Health check
curl http://localhost:5000/api/health

# Through nginx
curl http://localhost/api/health
```

---

## Troubleshooting

### Containers Won't Start

**Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Common issues:**
- Port already in use
- Missing .env file
- Build failures

### Port Conflicts

**Check what's using a port:**
```bash
sudo lsof -i :5000
sudo lsof -i :8080
sudo lsof -i :80
```

**Stop conflicting service:**
```bash
sudo systemctl stop service-name
```

### Backend Import Errors

**Access backend container:**
```bash
docker exec -it deception-detector-backend bash
cd /app
python -c "import app"
```

### Rebuild from Scratch

```bash
cd ~/deception-detector/webapp

# Stop and remove everything
docker-compose down -v

# Rebuild
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

### Disk Space Issues

**Check Docker disk usage:**
```bash
docker system df
```

**Clean up:**
```bash
# Remove unused containers, networks, images
docker system prune

# Remove everything including volumes
docker system prune -a --volumes
```

---

## Updating

### Update Application Code

```bash
cd ~/deception-detector/webapp

# Pull new code or upload new files
# Then rebuild

docker-compose down
docker-compose up -d --build
```

### Update Single Service

```bash
cd ~/deception-detector/webapp

# Update backend
docker-compose up -d --build backend

# Update frontend
docker-compose up -d --build frontend
```

### Update Docker Images

```bash
# Pull latest base images
docker-compose pull

# Rebuild
docker-compose up -d --build
```

---

## Auto-Start on Reboot

Docker containers with `restart: unless-stopped` will automatically start after reboot if Docker service starts.

**Ensure Docker starts on boot:**
```bash
sudo systemctl enable docker
```

---

## Backup and Restore

### Backup Models

```bash
cd ~/deception-detector/webapp
tar -czf models-backup.tar.gz backend/models backend/custom_models backend/base_models
```

### Restore Models

```bash
cd ~/deception-detector/webapp
tar -xzf models-backup.tar.gz
docker-compose restart backend
```

---

## Production Checklist

- [ ] Change API credentials in `.env`
- [ ] Set `DEBUG_MODE=False`
- [ ] Configure `ALLOWED_ORIGINS` properly
- [ ] Enable HTTPS
  - With domain: Run `docker-setup-ssl.sh`
  - With IP only: Run `setup-ip-ssl.sh` (shows browser warnings)
- [ ] Set up firewall (allow ports 80, 443)
- [ ] Configure automatic backups
- [ ] Monitor logs regularly
- [ ] Set up monitoring/alerting

---

## Useful Commands Summary

```bash
# Deploy
sudo bash deployment/docker-deploy.sh

# View logs
docker-compose logs -f

# Status
docker-compose ps

# Restart
docker-compose restart

# Stop
docker-compose stop

# Start
docker-compose start

# Rebuild
docker-compose up -d --build

# Enable HTTPS (domain)
sudo bash deployment/docker-setup-ssl.sh

# Enable HTTPS (IP address)
sudo bash deployment/setup-ip-ssl.sh

# Shell access
docker exec -it deception-detector-backend bash

# Clean up
docker system prune
```