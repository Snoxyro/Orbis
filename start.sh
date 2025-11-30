#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting...${NC}\n"

# Start database
echo -e "${GREEN}[1/3] Starting PostgreSQL...${NC}"
docker-compose up -d
echo ""

# Start backend
echo -e "${GREEN}[2/3] Starting API...${NC}"
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!
cd ..
echo "API running (PID: $API_PID)"
echo ""

# Start frontend
echo -e "${GREEN}[3/3] Starting Web...${NC}"
cd web
npm run dev &
WEB_PID=$!
cd ..
echo "Web running (PID: $WEB_PID)"
echo ""

echo -e "${BLUE}✓ All services running!${NC}"
echo ""
echo "  Web:      http://localhost:5173"
echo "  API:      http://localhost:8000"
echo "  Database: localhost:5432"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $API_PID $WEB_PID; docker-compose down; exit" INT
wait
