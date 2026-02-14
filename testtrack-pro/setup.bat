@echo off
REM TestTrack Pro Setup Script for Windows

echo.
echo ========================================
echo TestTrack Pro - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if MySQL is installed
mysql --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: MySQL is not installed or not in PATH
    echo Please install MySQL 5.7+ from https://www.mysql.com/
    pause
    exit /b 1
)

echo ✓ Python found
echo ✓ MySQL found
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo Note: Edit backend\.env with your MySQL credentials
)

echo.
echo ✓ Backend setup complete
echo.

REM Instructions
echo ========================================
echo Setup Instructions:
echo ========================================
echo.
echo 1. Edit MySQL connection settings:
echo    - Open backend\.env
echo    - Update MYSQL_USER and MYSQL_PASSWORD
echo.
echo 2. Create database:
echo    mysql -u root -p < database\schema.sql
echo.
echo 3. Run backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 4. Run frontend (in new terminal):
echo    cd frontend
echo    python -m http.server 8000
echo    OR use http-server if Node.js is installed
echo.
echo 5. Open in browser:
echo    http://localhost:8000/login.html
echo.
echo Demo Credentials:
echo    Tester: tester1@testtrack.com / tester123
echo    Developer: developer1@testtrack.com / dev123
echo.

pause
