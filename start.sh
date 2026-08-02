#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "   Starting Nyaya AI (Mini Project)...           "
echo "=================================================="

# 1. Start/verify Backend via PM2
echo "1. Checking Backend Service (PM2)..."
if pm2 list | grep -q "nyaya-backend"; then
    echo "   Backend service 'nyaya-backend' is already registered. Restarting..."
    pm2 restart nyaya-backend
else
    echo "   Backend service 'nyaya-backend' not registered. Registering with PM2..."
    cd "$SCRIPT_DIR/backend"
    pm2 start bash --name "nyaya-backend" -- -c "venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8001"
    cd "$SCRIPT_DIR"
fi

# Save PM2 process list to persist across reboots
pm2 save

echo "   Waiting for backend to boot up..."
sleep 3

# Verify backend health
if curl -s http://localhost:8001/ > /dev/null; then
    echo "   [✓] Backend API is online on port 8001!"
else
    echo "   [!] Warning: Backend is not responding yet. Check logs with: pm2 logs nyaya-backend"
fi

# 2. Open browser and run Frontend Dev Server
echo "2. Launching Frontend Dev Server..."
cd "$SCRIPT_DIR/frontend"

# Open user's default browser after Vite starts up
(sleep 2 && xdg-open "http://localhost:5174/" 2>/dev/null || open "http://localhost:5174/" 2>/dev/null) &

# Start Vite server
npm run dev
