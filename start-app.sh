#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Start backend in background
echo -e "${GREEN}Starting backend server...${NC}"
cd "$(dirname "$0")/backend" || exit
source ../venv/bin/activate
(uvicorn app:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1) &
BACKEND_PID=$!
echo -e "${GREEN}Backend running with PID: ${BACKEND_PID}${NC}"

# Wait a moment for backend to initialize
sleep 2

# Start frontend
echo -e "${BLUE}Starting frontend development server...${NC}"
cd "../frontend" || exit
npm run dev

# When frontend is stopped with Ctrl+C, kill backend too
echo -e "${GREEN}Stopping backend (PID: ${BACKEND_PID})...${NC}"
kill $BACKEND_PID