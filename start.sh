#!/bin/bash

# PlanAI Travel Planner - Start Script
echo "🚀 Starting PlanAI Travel Planner..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
}

# Start Backend
echo "📡 Starting Backend Server..."
cd backend

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    source ../venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at ../venv"
fi

# Check if backend is already running
if check_port 8000; then
    echo "⚠️  Port 8000 is already in use. Backend might already be running."
else
    echo "🔄 Starting backend on port 8000..."
    nohup uvicorn app:app --reload --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo "✅ Backend started with PID: $BACKEND_PID"
    
    # Wait a moment for backend to start
    sleep 3
fi

# Go back to root and start frontend
cd ..

echo "🎨 Starting Frontend Server..."
cd frontend

# Check if frontend is already running
if check_port 3000; then
    echo "⚠️  Port 3000 is already in use. Frontend might already be running."
else
    echo "🔄 Starting frontend on port 3000..."
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "✅ Frontend started with PID: $FRONTEND_PID"
fi

cd ..

echo ""
echo "🎉 PlanAI Travel Planner is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop the servers:"
echo "   killall uvicorn  # Stop backend"
echo "   killall node     # Stop frontend"
echo ""

# Optional: Open browser
read -p "🌐 Open browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open http://localhost:3000
fi
