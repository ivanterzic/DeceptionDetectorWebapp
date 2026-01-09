#!/bin/bash
# Simple startup script without systemd

APP_DIR="/opt/deception-detector"
LOG_DIR="/var/log/deception-detector"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting Deception Detector...${NC}"

# Create log directory if needed
mkdir -p "$LOG_DIR"

# Start backend
cd "$APP_DIR/backend"
echo -e "${BLUE}Starting backend...${NC}"
source venv/bin/activate
nohup gunicorn \
    --workers 4 \
    --threads 2 \
    --timeout 300 \
    --bind 127.0.0.1:5000 \
    --access-logfile "$LOG_DIR/backend-access.log" \
    --error-logfile "$LOG_DIR/backend-error.log" \
    --log-level info \
    --daemon \
    --pid "$APP_DIR/backend.pid" \
    app:app
deactivate
echo -e "${GREEN}Backend started (PID: $(cat $APP_DIR/backend.pid))${NC}"

# Start frontend
cd "$APP_DIR/frontend"
echo -e "${BLUE}Starting frontend...${NC}"
nohup node server.js > "$LOG_DIR/frontend.log" 2>&1 &
echo $! > "$APP_DIR/frontend.pid"
echo -e "${GREEN}Frontend started (PID: $(cat $APP_DIR/frontend.pid))${NC}"

# Start nginx if not running
if ! systemctl is-active --quiet nginx 2>/dev/null; then
    echo -e "${BLUE}Starting nginx...${NC}"
    if command -v systemctl &> /dev/null; then
        sudo systemctl start nginx
    else
        sudo service nginx start
    fi
    echo -e "${GREEN}Nginx started${NC}"
fi

echo ""
echo -e "${GREEN}All services started!${NC}"
echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://127.0.0.1:8080"
echo "Nginx: http://localhost"
echo ""
echo "Logs:"
echo "  Backend:  tail -f $LOG_DIR/backend-error.log"
echo "  Frontend: tail -f $LOG_DIR/frontend.log"
echo ""
echo "To stop: bash deployment/stop.sh"
