#!/bin/bash

# Health check script for monitoring
# Can be used by monitoring systems like Nagios, Prometheus, etc.

set -e

BACKEND_URL="http://127.0.0.1:5000"
FRONTEND_URL="http://127.0.0.1:8080"
EXIT_CODE=0

# Check backend
echo "Checking backend..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/models" || echo "000")
if [ "$BACKEND_STATUS" -eq 200 ]; then
    echo "✓ Backend is healthy (HTTP $BACKEND_STATUS)"
else
    echo "✗ Backend is unhealthy (HTTP $BACKEND_STATUS)"
    EXIT_CODE=1
fi

# Check frontend
echo "Checking frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/" || echo "000")
if [ "$FRONTEND_STATUS" -eq 200 ]; then
    echo "✓ Frontend is healthy (HTTP $FRONTEND_STATUS)"
else
    echo "✗ Frontend is unhealthy (HTTP $FRONTEND_STATUS)"
    EXIT_CODE=1
fi

# Check systemd services
echo "Checking services..."
if systemctl is-active --quiet deception-detector-backend; then
    echo "✓ Backend service is running"
else
    echo "✗ Backend service is not running"
    EXIT_CODE=1
fi

if systemctl is-active --quiet deception-detector-frontend; then
    echo "✓ Frontend service is running"
else
    echo "✗ Frontend service is not running"
    EXIT_CODE=1
fi

if systemctl is-active --quiet nginx; then
    echo "✓ Nginx is running"
else
    echo "✗ Nginx is not running"
    EXIT_CODE=1
fi

# Check disk space
echo "Checking disk space..."
DISK_USAGE=$(df -h /opt/deception-detector | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo "✓ Disk usage is ${DISK_USAGE}%"
else
    echo "⚠ Disk usage is high: ${DISK_USAGE}%"
    EXIT_CODE=2
fi

# Check memory
echo "Checking memory..."
MEM_AVAILABLE=$(free -m | awk 'NR==2{print $7}')
if [ "$MEM_AVAILABLE" -gt 500 ]; then
    echo "✓ Memory available: ${MEM_AVAILABLE}MB"
else
    echo "⚠ Low memory: ${MEM_AVAILABLE}MB available"
    EXIT_CODE=2
fi

# Summary
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ All health checks passed"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "⚠ Health checks passed with warnings"
else
    echo "✗ Health checks failed"
fi

exit $EXIT_CODE
