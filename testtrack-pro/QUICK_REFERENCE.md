curl http://localhost:5000/health# TestTrack Pro - Quick Reference Guide

## 🚀 Quick Start (Choose One)

### Docker Method (30 seconds)
```bash
git clone <repo> && cd testtrack-pro && docker-compose up --build
```
Access: http://localhost:8000

### Local Method (2 minutes)
```bash
# Terminal 1: Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cp .env.example .env && python app_enterprise.py

# Terminal 2: Frontend
cd frontend && python -m http.server 8000
```
Access: http://localhost:8000

**Default Login:**
- Email: `admin@testtrack.local`
- Password: `password123`

---

## 📚 Key Documentation

| Need | File |
|------|------|
| Setup Instructions | [docs/SETUP_COMPREHENSIVE.md](docs/SETUP_COMPREHENSIVE.md) |
| API Reference | [docs/API.md](docs/API.md) |
| How to Contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Version History | [CHANGELOG.md](CHANGELOG.md) |
| Project Overview | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |

---

## 🏗️ Project Structure at a Glance

```
frontend/  → Web UI (HTML/CSS/JavaScript)
backend/   → Python Flask API (900+ lines, 30 endpoints)
database/  → MySQL schema (25 tables)
docs/      → Documentation
.github/   → CI/CD automation
```

---

## 🔑 Important Commands

### Docker
```bash
docker-compose up           # Start all services
docker-compose down         # Stop services
docker-compose logs -f      # View logs
docker-compose exec backend pytest -v  # Run tests
```

### Python
```bash
python -m venv venv         # Create environment
source venv/bin/activate    # Activate (macOS/Linux)
venv\Scripts\activate       # Activate (Windows)
pip install -r requirements.txt  # Install packages
python app_enterprise.py    # Run backend
```

### Database
```bash
mysql -u testtrack -p testtrack_pro < database/schema.sql  # Initialize
docker-compose exec mysql mysql -u testtrack -p              # Connect
```

### Testing
```bash
pytest backend/tests/ -v    # Run tests
pytest --cov=backend        # With coverage
black backend/              # Format code
flake8 backend/             # Lint code
```

---

## 🔐 Default Credentials

| User | Email | Password | Role |
|------|-------|----------|------|
| Admin | admin@testtrack.local | password123 | Admin |
| Tester | tester@testtrack.local | password123 | Tester |
| Developer | developer@testtrack.local | password123 | Developer |

⚠️ **Change in production!**

---

## 📡 API Endpoints Summary

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| POST | `/api/auth/logout` | Logout |

### Test Cases
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/projects/{id}/testcases` | List tests |
| POST | `/api/projects/{id}/testcases` | Create test |
| GET | `/api/testcases/{id}` | Get details |
| PUT | `/api/testcases/{id}` | Update test |
| POST | `/api/testcases/{id}/clone` | Clone test |

### Bug Management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/projects/{id}/bugs` | List bugs |
| POST | `/api/projects/{id}/bugs` | Report bug |
| PUT | `/api/bugs/{id}/status` | Update status |
| POST | `/api/bugs/{id}/comment` | Add comment |

### Reports
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/projects/{id}/reports/summary` | Get summary |
| GET | `/api/projects/{id}/reports/developer-performance` | Dev metrics |

Full API reference: [docs/API.md](docs/API.md)

---

## 🐛 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| **Port 5000 in use** | `lsof -i :5000` then `kill -9 <PID>` |
| **MySQL connection error** | Check MYSQL_* variables in `.env` |
| **Module not found** | Activate venv: `source venv/bin/activate` |
| **Docker permission denied** | `sudo usermod -aG docker $USER` |
| **Database empty** | Run: `mysql < database/schema.sql` |

Full troubleshooting: [docs/SETUP_COMPREHENSIVE.md#troubleshooting](docs/SETUP_COMPREHENSIVE.md#troubleshooting)

---

## 📊 Database Tables (25 Total)

**Users** (3): users, password_reset_tokens, password_history
**Projects** (3): projects, project_members, milestones
**Tests** (9): test_cases, test_case_steps, test_case_tags, test_case_versions, test_case_templates, test_suites, suite_test_cases, test_case_comments, test_run_assignments
**Execution** (5): test_runs, test_executions, execution_steps, execution_evidence, test_case_attachments
**Bugs** (6): bugs, bug_comments, bug_workflow_history, bug_fixes, bug_attachments, bug_linked_tests
**System** (4): notifications, audit_logs, api_keys, webhooks, webhook_logs

---

## 🔄 Development Workflow

### 1. Make Changes
```bash
git checkout -b feature/my-feature
# Edit files...
black backend/       # Format
flake8 backend/      # Lint
pytest backend/      # Test
```

### 2. Commit
```bash
git add .
git commit -m "feat(module): description"  # Conventional commit
```

### 3. Push & PR
```bash
git push origin feature/my-feature
# Open Pull Request on GitHub
```

### 4. Deploy (Automatic)
- Staging: Push to `develop` branch
- Production: Create version tag (`v1.0.0`)

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:8000 | Web application |
| Backend | http://localhost:5000 | REST API |
| Health Check | http://localhost:5000/health | Service status |
| MySQL | localhost:3306 | Database |

---

## 📦 Technology Stack

**Frontend:** HTML5, CSS3, Vanilla JavaScript
**Backend:** Python 3.11+, Flask 2.3+
**Database:** MySQL 8.0+
**DevOps:** Docker, Docker Compose, GitHub Actions
**Authentication:** JWT, bcrypt

---

## 📝 Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `.env.example` | Environment template | ✅ Complete |
| `docker-compose.yml` | Docker orchestration | ✅ Complete |
| `requirements.txt` | Python packages | ✅ Complete |
| `.github/workflows/*.yml` | CI/CD pipelines | ✅ Complete |
| `database/schema.sql` | Database schema | ✅ Complete |

---

## 🚨 Important Notes

1. **Change default passwords** before production deployment
2. **Set JWT_SECRET_KEY** to a strong random value
3. **Configure email/SMTP** for notifications (optional)
4. **Set up database backups** before going live
5. **Enable HTTPS** in production
6. **Configure firewall** to restrict database access
7. **Set up monitoring** with application logs
8. **Enable automatic updates** for dependencies

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit changes: `git commit -m "feat(...): description"`
4. Push branch: `git push origin feature/amazing`
5. Open Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@testtrack.example.com

---

## 📄 File Locations

| File | Location |
|------|----------|
| Frontend HTML | `frontend/*.html` |
| Frontend CSS | `frontend/styles.css` |
| Frontend JS | `frontend/*.js` |
| Backend API | `backend/app_enterprise.py` |
| Models | `backend/models_advanced.py` |
| Database | `database/schema.sql` |
| Config | `backend/.env.example` |
| Docker | `docker-compose.yml`, `backend/Dockerfile` |

---

## 🎯 Common Tasks

### Add New Test Type
1. Update database schema (test_cases table)
2. Update models validation
3. Update API endpoint
4. Update frontend dropdown

### Create New API Endpoint
1. Define route in `app_enterprise.py`
2. Add business logic in `models_advanced.py`
3. Add authentication decorator
4. Add error handling
5. Document in `API.md`
6. Write tests in `backend/tests/`

### Deploy to Production
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
# GitHub Actions automatically deploys with backup & health checks
```

### Troubleshoot Deployment
```bash
docker-compose logs -f backend  # View backend logs
docker-compose exec mysql mysql -u root  # Check database
curl http://localhost:5000/health  # Check API health
```

---

## ✅ Pre-Deployment Checklist

- [ ] All tests passing
- [ ] `.env` configured for production
- [ ] Database backups enabled
- [ ] SSL certificates installed
- [ ] JWT_SECRET_KEY set to random value
- [ ] Default passwords changed
- [ ] Email/SMTP configured (optional)
- [ ] Firewall rules configured
- [ ] Monitoring setup
- [ ] Logging enabled

---

## 🔗 Quick Links

- [GitHub Repository](https://github.com/yourusername/testtrack-pro)
- [Issue Tracker](https://github.com/yourusername/testtrack-pro/issues)
- [Project Board](https://github.com/yourusername/testtrack-pro/projects)
- [Discussions](https://github.com/yourusername/testtrack-pro/discussions)
- [Security Policy](SECURITY.md) (if available)

---

**Version:** 1.0.0
**Last Updated:** January 15, 2024
**Status:** ✅ Production Ready
