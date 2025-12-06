#!/bin/bash

# Start both Flask backend and Next.js frontend
# Run this from the project root directory

PROJECT_ROOT="/Users/yusakaraaslan/Desktop/dersler 2025 güz/db/proje/database-project"

echo "========================================="
echo "🚀 Starting Olist Analytics Platform"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to kill processes on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $FLASK_PID $NEXTJS_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start Flask backend
echo -e "${BLUE}[1/2] Starting Flask backend on port 5001...${NC}"
cd "$PROJECT_ROOT"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
source venv/bin/activate
nohup flask --app app/app.py run --port 5001 > flask.log 2>&1 &
FLASK_PID=$!
sleep 2
echo -e "${GREEN}✓ Flask backend running (PID: $FLASK_PID)${NC}"
echo ""

# Start Next.js frontend
echo -e "${BLUE}[2/2] Starting Next.js frontend on port 3000...${NC}"
cd "$PROJECT_ROOT/olist-dashboard"
nohup npm run dev > nextjs.log 2>&1 &
NEXTJS_PID=$!
sleep 3
echo -e "${GREEN}✓ Next.js frontend running (PID: $NEXTJS_PID)${NC}"
echo ""

echo "========================================="
echo "✨ All servers are running!"
echo "========================================="
echo ""
echo "📊 Access the dashboard at:"
echo "   👉 http://localhost:3000"
echo ""
echo "🔧 API backend available at:"
echo "   👉 http://localhost:5001"
echo ""
echo "📝 Logs:"
echo "   Flask:  $PROJECT_ROOT/flask.log"
echo "   Next.js: $PROJECT_ROOT/olist-dashboard/nextjs.log"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "========================================="

# Keep script running
wait
