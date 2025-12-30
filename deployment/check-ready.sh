#!/bin/bash

# Pre-deployment checklist script
# Run this locally before deploying to ensure everything is ready

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================="
echo "  Pre-Deployment Checklist"
echo "========================================="
echo ""

ERRORS=0
WARNINGS=0

# Check if deployment files exist
echo "Checking deployment files..."
for file in deploy.sh nginx.conf .env.production.template deception-detector-backend.service deception-detector-frontend.service; do
    if [ -f "deployment/$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file missing"
        ((ERRORS++))
    fi
done
echo ""

# Check backend requirements
echo "Checking backend requirements..."
if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt exists"
else
    echo -e "${RED}✗${NC} requirements.txt missing"
    ((ERRORS++))
fi

if [ -f "backend/app.py" ]; then
    echo -e "${GREEN}✓${NC} app.py exists"
else
    echo -e "${RED}✗${NC} app.py missing"
    ((ERRORS++))
fi
echo ""

# Check frontend files
echo "Checking frontend files..."
if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓${NC} package.json exists"
else
    echo -e "${RED}✗${NC} package.json missing"
    ((ERRORS++))
fi

if [ -d "frontend/src" ]; then
    echo -e "${GREEN}✓${NC} src/ directory exists"
else
    echo -e "${RED}✗${NC} src/ directory missing"
    ((ERRORS++))
fi
echo ""

# Check for .env file (should not exist in repo)
echo "Checking for sensitive files..."
if [ -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠${NC} backend/.env exists (should not be in version control)"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓${NC} No .env in version control"
fi
echo ""

# Check documentation
echo "Checking documentation..."
if [ -f "deployment/DEPLOYMENT_GUIDE.md" ]; then
    echo -e "${GREEN}✓${NC} Deployment guide exists"
else
    echo -e "${YELLOW}⚠${NC} Deployment guide missing"
    ((WARNINGS++))
fi

if [ -f "README.md" ]; then
    echo -e "${GREEN}✓${NC} README exists"
else
    echo -e "${YELLOW}⚠${NC} README missing"
    ((WARNINGS++))
fi
echo ""

# Server requirements checklist
echo "Server Requirements Checklist:"
echo "  [ ] Ubuntu 20.04+ / Debian 11+ / CentOS 8+"
echo "  [ ] 4GB+ RAM (8GB+ recommended)"
echo "  [ ] 20GB+ storage"
echo "  [ ] Root/sudo access"
echo "  [ ] SSH access configured"
echo ""

echo "Pre-Deployment Checklist:"
echo "  [ ] Domain DNS configured (A record pointing to server)"
echo "  [ ] Firewall allows SSH (port 22)"
echo "  [ ] You have generated JWT secrets"
echo "  [ ] You have chosen API credentials"
echo "  [ ] SSL email address prepared"
echo ""

# Summary
echo "========================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "You're ready to deploy."
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s)${NC}"
    echo "Review warnings, but you can proceed with deployment."
else
    echo -e "${RED}✗ $ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo "Fix errors before deploying."
fi
echo "========================================="
echo ""

echo "Next steps:"
echo "1. Upload to server: scp -r webapp/ user@server:/tmp/"
echo "2. SSH to server: ssh user@server"
echo "3. Run deployment: cd /tmp/webapp/deployment && sudo ./deploy.sh"
echo ""

exit $ERRORS
