#!/bin/bash

# Quick deployment update script
# Use this to update the application after making changes

set -e

APP_DIR="/opt/deception-detector"
BACKUP_DIR="/opt/deception-detector-backups/$(date +%Y%m%d_%H%M%S)"

echo "Creating backup..."
mkdir -p "$BACKUP_DIR"
cp -r "$APP_DIR/backend/.env" "$BACKUP_DIR/"
cp -r "$APP_DIR/backend/models" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$APP_DIR/backend/custom_models" "$BACKUP_DIR/" 2>/dev/null || true

echo "Stopping services..."
systemctl stop deception-detector-backend
systemctl stop deception-detector-frontend

echo "Updating code..."
# Copy new code from your source
# Adjust the source path as needed
# cp -r /path/to/your/source/backend/* "$APP_DIR/backend/"
# cp -r /path/to/your/source/frontend/* "$APP_DIR/frontend/"

echo "Updating backend dependencies..."
cd "$APP_DIR/backend"
source venv/bin/activate
pip install -r requirements.txt --upgrade
deactivate

echo "Updating frontend dependencies..."
cd "$APP_DIR/frontend"
npm install
npm run build

echo "Setting permissions..."
chown -R www-data:www-data "$APP_DIR"

echo "Starting services..."
systemctl start deception-detector-backend
systemctl start deception-detector-frontend
systemctl restart nginx

echo "Checking services..."
sleep 3
systemctl status deception-detector-backend --no-pager
systemctl status deception-detector-frontend --no-pager

echo "Update complete!"
echo "Backup saved to: $BACKUP_DIR"
