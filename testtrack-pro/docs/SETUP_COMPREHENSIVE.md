# TestTrack Pro - Comprehensive Setup & Deployment Guide

## Quick Start (5 minutes)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/testtrack-pro.git
cd testtrack-pro

# Start all services
docker-compose up --build

# Access application
# Frontend: http://localhost:8000
# Backend API: http://localhost:5000
# Login: admin@testtrack.local / password123
```

### Option 2: Local Development

```bash
# Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
python app_enterprise.py

# Frontend (Terminal 2)
cd frontend
python -m http.server 8000

# Access: http://localhost:8000
```

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Setup](#docker-setup)
4. [Database Configuration](#database-configuration)
5. [Running the Application](#running-the-application)
6. [Staging Deployment](#staging-deployment)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Environment Variables](#environment-variables-reference)

## Prerequisites

### Minimum Requirements

- **Python:** 3.8 or higher
- **Node.js:** 16+ (optional, for frontend tools)
- **MySQL:** 5.7+ (or Docker)
- **Git:** For version control

### System Requirements

- **RAM:** Minimum 2GB (4GB recommended)
- **Disk Space:** 2GB for Docker images, 500MB for code
- **OS:** Windows, macOS, or Linux

### Optional Tools

- **Docker Desktop:** 20.10+
- **Docker Compose:** 1.29+
- **Postman:** For API testing

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/testtrack-pro.git
cd testtrack-pro
```

### Step 2: Set Up Python Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit backend/.env with your settings:
```

**Critical variables to set:**

```env
# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=testtrack
MYSQL_PASSWORD=your_secure_password
MYSQL_DB=testtrack_pro

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_development_secret_key_here

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here
PASSWORD_RESET_EXPIRY=3600

# Logging
LOG_LEVEL=DEBUG
```

### Step 5: Set Up Database

#### Using MySQL directly:

```bash
# Create database and user
mysql -u root -p << 'EOF'
CREATE DATABASE testtrack_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'testtrack'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON testtrack_pro.* TO 'testtrack'@'localhost';
FLUSH PRIVILEGES;
EOF

# Import schema
mysql -u testtrack -p testtrack_pro < database/schema.sql
```

#### Using Docker (easier):

```bash
# Start MySQL container
docker run -d \
  --name testtrack-mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=testtrack_pro \
  -e MYSQL_USER=testtrack \
  -e MYSQL_PASSWORD=testtrack123 \
  -p 3306:3306 \
  mysql:8.0

# Import schema
docker exec -i testtrack-mysql mysql -u testtrack -p testtrack_pro < database/schema.sql
```

### Step 6: Verify Database

```bash
# Test connection
mysql -h localhost -u testtrack -p testtrack_pro -e "SELECT COUNT(*) as 'Tables in testtrack_pro' FROM information_schema.tables WHERE table_schema='testtrack_pro';"
```

Expected output: `Tables in testtrack_pro: 25`

### Step 7: Start Backend

```bash
cd backend
python app_enterprise.py
```

Expected output:
```
* Serving Flask app 'app_enterprise'
* Debug mode: on
* Running on http://0.0.0.0:5000
```

### Step 8: Start Frontend

In a new terminal:

```bash
cd frontend
python -m http.server 8000
```

Open browser and navigate to `http://localhost:8000`

### Default Credentials

| User | Email | Password | Role |
|------|-------|----------|------|
| Admin | admin@testtrack.local | password123 | admin |
| Tester | tester@testtrack.local | password123 | tester |
| Developer | developer@testtrack.local | password123 | developer |

## Docker Setup

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+

### Quick Start

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Compose Services

The `docker-compose.yml` includes:

1. **MySQL**
   - Port: 3306
   - Volume: mysql_data (persistent storage)
   - Health check: Every 10 seconds

2. **Backend (Flask)**
   - Port: 5000
   - Volume: ./backend (for development hot-reload)
   - Depends on: MySQL health check

3. **Frontend (Web Server)**
   - Port: 8000
   - Volume: ./frontend

### Running Individual Services

```bash
# Start only database
docker-compose up mysql

# Start database and backend
docker-compose up mysql backend

# Start everything
docker-compose up
```

### Accessing Docker Services

```bash
# Connect to MySQL in container
docker-compose exec mysql mysql -u testtrack -p

# View backend logs
docker-compose logs backend -f

# Execute command in backend
docker-compose exec backend python database/migrate.py

# Access application shell
docker-compose exec backend python -i

# Check resource usage
docker stats
```

## Database Configuration

### Schema Overview

The database includes 25 tables:

**Authentication & Users**
- users
- password_reset_tokens
- password_history

**Project Management**
- projects
- project_members
- milestones

**Test Management**
- test_cases
- test_case_steps
- test_case_tags
- test_case_versions
- test_case_templates
- test_suites
- suite_test_cases

**Execution & Results**
- test_runs
- test_run_assignments
- test_executions
- execution_steps
- execution_evidence

**Bug Tracking**
- bugs
- bug_linked_tests
- bug_comments
- bug_workflow_history
- bug_fixes
- bug_attachments

**System**
- notifications
- audit_logs
- api_keys
- webhooks
- webhook_logs

### Database Backup

```bash
# Backup using Docker
docker-compose exec mysql mysqldump -u testtrack -p testtrack_pro | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Restore from backup
gunzip -c backup_20240115_103000.sql.gz | docker-compose exec -T mysql mysql -u testtrack -p testtrack_pro
```

### Database Optimization

```bash
# Optimize all tables
docker-compose exec mysql mysql -u testtrack -p testtrack_pro -e "OPTIMIZE TABLE test_cases, bugs, test_executions;"

# Check table status
docker-compose exec mysql mysql -u testtrack -p testtrack_pro -e "ANALYZE TABLE test_cases;"

# Reset auto-increment
docker-compose exec mysql mysql -u testtrack -p testtrack_pro -e "ALTER TABLE test_cases AUTO_INCREMENT = 1;"
```

## Running the Application

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:8000 | Main web application |
| Backend API | http://localhost:5000 | REST API endpoints |
| Health Check | http://localhost:5000/health | Service health status |
| API Docs | [API.md](./docs/API.md) | Complete API documentation |

### Frontend Features

- **Dashboard:** Overview of test cases, executions, and bugs
- **Test Cases:** Create, edit, clone, and manage test cases
- **Test Execution:** Execute tests, record results, upload evidence
- **Bug Management:** Report, track, and resolve bugs
- **Reports:** Summary reports and performance analytics
- **Notifications:** Real-time notifications for assigned items

### API Endpoints

**Authentication:**
- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/logout`

**Test Cases:**
- GET `/api/projects/{id}/testcases`
- POST `/api/projects/{id}/testcases`
- PUT `/api/testcases/{id}`

**Test Execution:**
- POST `/api/projects/{id}/testruns`
- POST `/api/testruns/{id}/execute`

**Bug Management:**
- GET `/api/projects/{id}/bugs`
- POST `/api/projects/{id}/bugs`
- PUT `/api/bugs/{id}/status`

**Reporting:**
- GET `/api/projects/{id}/reports/summary`
- GET `/api/projects/{id}/reports/developer-performance`

See [API.md](./docs/API.md) for complete endpoint documentation.

## Staging Deployment

### Prerequisites

- GitHub repository with push access
- Staging server with Docker & Docker Compose
- Private Docker registry credentials
- SSH access to staging server

### GitHub Secrets Configuration

Go to Settings → Secrets and set:

```
DOCKER_REGISTRY=docker.io
DOCKER_USERNAME=<username>
DOCKER_PASSWORD=<password>
STAGING_HOST=staging.example.com
STAGING_USER=deploy
STAGING_SSH_KEY=<private_key>
```

### Deploy to Staging

```bash
# Push to develop branch
git checkout develop
git push origin develop

# GitHub Actions will automatically:
# 1. Run all tests
# 2. Build Docker image
# 3. Deploy to staging
# 4. Run smoke tests
```

Monitor progress: GitHub → Actions → "CD - Deploy to Staging"

## Production Deployment

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed and merged to main
- [ ] Database backups configured
- [ ] SSL certificates installed
- [ ] Environment variables configured
- [ ] Monitoring and logging set up

### Release Process

```bash
# Ensure main branch is up to date
git checkout main
git pull origin main

# Create semantic version tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag
git push origin v1.0.0

# GitHub Actions will automatically deploy to production
```

### Manual Deployment

If automated deployment fails:

```bash
# SSH to production server
ssh your_user@production.example.com

cd /opt/testtrack-pro

# Create backup
docker exec testtrack-pro-mysql mysqldump -u testtrack -p testtrack_pro | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Pull latest code
git pull origin main
git checkout v1.0.0

# Update and restart
cp .env.production .env
docker-compose up -d --build

# Verify
curl http://localhost:5000/health
```

### Rollback

```bash
# SSH to production
ssh your_user@production.example.com
cd /opt/testtrack-pro

# Restore previous version
git checkout v0.9.0
docker-compose down
docker-compose up -d

# Restore database
gunzip -c backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker exec -i testtrack-pro-mysql mysql -u testtrack -p testtrack_pro
```

## Troubleshooting

### Port Already in Use

```bash
# macOS/Linux
lsof -i :5000
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Connection Failed

```bash
# Check MySQL is running
docker-compose ps

# Test connection
mysql -h localhost -u testtrack -p testtrack_pro -e "SELECT 1;"

# Check .env credentials
grep MYSQL backend/.env
```

### Python Module Not Found

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Docker Permission Denied

```bash
# Linux only
sudo usermod -aG docker $USER
newgrp docker
docker ps
```

### API Returns 401 Unauthorized

- Verify JWT token is included in Authorization header
- Check JWT_SECRET_KEY is set in .env
- Ensure token hasn't expired (default: 24 hours)

### Database Migration Fails

```bash
# Check migration status
docker exec testtrack-pro-backend python database/migrate.py

# View detailed logs
docker logs testtrack-pro-backend | grep -i error
```

### Application Crashes on Startup

```bash
# Check logs
docker-compose logs backend

# Verify environment variables
docker-compose config | grep -A 20 backend

# Check database connectivity
docker exec testtrack-pro-mysql mysql -u root -p << 'EOF'
SHOW DATABASES;
USE testtrack_pro;
SHOW TABLES;
EOF
```

## Environment Variables Reference

```env
# === Database ===
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=testtrack
MYSQL_PASSWORD=secure_password
MYSQL_DB=testtrack_pro
MYSQL_CHARSET=utf8mb4

# === Flask ===
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key
LOG_LEVEL=INFO

# === Security ===
JWT_SECRET_KEY=your_jwt_secret
JWT_EXPIRATION_HOURS=24
PASSWORD_RESET_EXPIRY=3600
SESSION_TIMEOUT=900
MAX_LOGIN_ATTEMPTS=5

# === Email ===
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=app_password
MAIL_FROM_ADDR=noreply@testtrack.com

# === File Upload ===
MAX_CONTENT_LENGTH=104857600
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,doc,docx

# === API ===
API_RATE_LIMIT=100
API_RATE_LIMIT_WINDOW=60
CORS_ORIGINS=*

# === Cloudinary (Optional) ===
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# === Production ===
ENABLE_HTTPS=True
ALLOW_CORS=False
DEBUG=False
```

## Support & Resources

- **Documentation:** See [docs/](./docs/) folder
- **API Reference:** See [API.md](./docs/API.md)
- **Requirements:** See [REQUIREMENTS.md](./docs/REQUIREMENTS.md)
- **Contributing:** See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
