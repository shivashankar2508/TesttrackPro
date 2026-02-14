#!/bin/bash

# TestTrack Pro Setup Script for Mac/Linux

echo ""
echo "========================================"
echo "TestTrack Pro - Mac/Linux Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "ERROR: MySQL is not installed"
    echo "Please install MySQL 5.7+ from https://www.mysql.com/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo "✓ MySQL found: $(mysql --version)"
echo ""

# Setup Backend
echo "Setting up Backend..."
cd backend || exit

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "Note: Edit backend/.env with your MySQL credentials"
fi

echo ""
echo "✓ Backend setup complete"
echo ""

# Instructions
echo "========================================"
echo "Setup Instructions:"
echo "========================================"
echo ""
echo "1. Edit MySQL connection settings:"
echo "   - Open backend/.env"
echo "   - Update MYSQL_USER and MYSQL_PASSWORD"
echo ""
echo "2. Create database:"
echo "   mysql -u root -p < database/schema.sql"
echo ""
echo "3. Run backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "4. Run frontend (in new terminal):"
echo "   cd frontend"
echo "   python -m http.server 8000"
echo ""
echo "5. Open in browser:"
echo "   http://localhost:8000/login.html"
echo ""
echo "Demo Credentials:"
echo "   Tester: tester1@testtrack.com / tester123"
echo "   Developer: developer1@testtrack.com / dev123"
echo ""
