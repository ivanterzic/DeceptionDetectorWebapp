#!/bin/bash
# Simple stop script

APP_DIR="/opt/deception-detector"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Stopping Deception Detector...${NC}"

# Stop backend
if [ -f "$APP_DIR/backend.pid" ]; then
    PID=$(cat "$APP_DIR/backend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping backend (PID: $PID)...${NC}"
        kill "$PID"
        rm "$APP_DIR/backend.pid"
        echo -e "${GREEN}Backend stopped${NC}"
    else
        echo -e "${RED}Backend not running${NC}"
        rm "$APP_DIR/backend.pid"
    fi
else
    echo -e "${RED}Backend PID file not found${NC}"
fi

# Stop frontend
if [ -f "$APP_DIR/frontend.pid" ]; then
    PID=$(cat "$APP_DIR/frontend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping frontend (PID: $PID)...${NC}"
        kill "$PID"
        rm "$APP_DIR/frontend.pid"
        echo -e "${GREEN}Frontend stopped${NC}"
    else
        echo -e "${RED}Frontend not running${NC}"
        rm "$APP_DIR/frontend.pid"
    fi
else
    echo -e "${RED}Frontend PID file not found${NC}"
fi

# Cleanup any remaining gunicorn processes
pkill -f "gunicorn.*deception-detector" 2>/dev/null && echo -e "${GREEN}Cleaned up remaining gunicorn processes${NC}"

# Cleanup any remaining node processes for this app
pkill -f "node.*deception-detector/frontend/server.js" 2>/dev/null && echo -e "${GREEN}Cleaned up remaining node processes${NC}"

echo -e "${GREEN}All services stopped${NC}"
