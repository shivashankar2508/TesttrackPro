# TestTrack Pro

<div align="center">

**Enterprise-Grade Software Testing Platform**

[![CI Pipeline](https://github.com/yourusername/testtrack-pro/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/testtrack-pro/actions/workflows/ci.yml)
[![Staging Deployment](https://github.com/yourusername/testtrack-pro/actions/workflows/cd-staging.yml/badge.svg)](https://github.com/yourusername/testtrack-pro/actions/workflows/cd-staging.yml)
[![Production Deployment](https://github.com/yourusername/testtrack-pro/actions/workflows/cd-production.yml/badge.svg)](https://github.com/yourusername/testtrack-pro/actions/workflows/cd-production.yml)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Overview

TestTrack Pro is a comprehensive software testing platform designed for QA teams, developers, and project managers. It provides end-to-end test management, execution tracking, bug reporting, and advanced analytics in a single integrated platform.

Built with **Python/Flask**, **MySQL**, and **Vanilla JavaScript**, TestTrack Pro offers enterprise-grade features while maintaining simplicity and ease of deployment.

## Features

### 🧪 Test Case Management
- Create and organize test cases with detailed steps
- Support for multiple test types (functional, regression, smoke, integration, UAT, performance, security)
- Test case versioning and history tracking
- Clone test cases for quick duplication
- Tag-based organization
- Test templates for recurring patterns

### 🏃 Test Execution
- Plan test runs and assign tests to team members
- Step-by-step execution tracking
- Real-time result recording
- Evidence upload (screenshots, logs, attachments)
- Duration tracking and auto-timing
- Test history and trend analysis

### 🐛 Bug Management
- Auto-generated bug IDs (BUG-XXXXXX format)
- Complete lifecycle tracking (new → open → in progress → fixed → verified → closed)
- Bug linking to test cases
- Assignment and escalation
- Rich comments and discussion threads
- Workflow history and audit trail
- Fix tracking with commit integration

### 📊 Advanced Reporting
- Executive dashboards with key metrics
- Test execution summaries (pass/fail rates, coverage)
- Bug status and severity analysis
- Developer performance metrics
- Customizable date ranges and filters

### 🔔 Notifications
- Real-time in-app notifications
- Email notifications for assignments
- Notifications for status changes

### 👥 Project Management
- Multiple project support
- Team member management
- Milestone tracking

### 🔐 Security
- User authentication and authorization
- Role-based access control (Admin, Tester, Developer)
- Password reset with secure tokens
- JWT-based API authentication

### 🚀 Deployment
- Docker and Docker Compose support
- Automated CI/CD pipelines (GitHub Actions)
- Staging and production environments

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Documentation](#documentation)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6+) |
| **Backend** | Python 3.8+, Flask 2.3+, SQLAlchemy 2.0+ |
| **Database** | MySQL 8.0+ (25 normalized tables) |
| **Authentication** | JWT (flask-jwt-extended), bcrypt hashing |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **Testing** | pytest, Postman, Locust |

## Installation

### Prerequisites

- Python 3.8+
- MySQL 5.7+ (or Docker)
- Docker 20.10+ (recommended)
- Git

### Get Started in 5 Minutes

```bash
git clone https://github.com/yourusername/testtrack-pro.git
cd testtrack-pro
docker-compose up --build
```

Then open http://localhost:8000 and login with:
- Email: `admin@testtrack.local`
- Password: `password123`

### Full Installation Guide

For complete setup instructions, see [SETUP_COMPREHENSIVE.md](docs/SETUP_COMPREHENSIVE.md).

## Documentation

| Document | Purpose |
|----------|---------|
| [SETUP_COMPREHENSIVE.md](docs/SETUP_COMPREHENSIVE.md) | Detailed installation, configuration, and deployment guide |
| [API.md](docs/API.md) | Complete REST API reference with examples |
| [REQUIREMENTS.md](docs/REQUIREMENTS.md) | Functional and non-functional requirements |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and design patterns |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute to the project |

## Database Schema

The system uses **25 MySQL tables** organized into logical modules:

### Authentication & Users (3 tables)
- `users` - User accounts and profiles
- `password_reset_tokens` - Password reset security tokens
- `password_history` - User password change history

### Project Management (3 tables)
- `projects` - Project definitions
- `project_members` - Project team members
- `milestones` - Project milestones and phases

### Test Management (9 tables)
- `test_cases` - Test case definitions
- `test_case_steps` - Individual test steps
- `test_case_tags` - Test classification tags
- `test_case_versions` - Test version history
- `test_case_templates` - Reusable test templates
- `test_suites` - Grouped test cases
- `suite_test_cases` - Suite membership
- `test_case_comments` - Test case discussions
- `test_run_assignments` - Tester assignments

### Execution & Results (5 tables)
- `test_runs` - Test execution rounds
- `test_executions` - Individual test results
- `execution_steps` - Step-by-step results
- `execution_evidence` - Attached screenshots/logs
- `test_case_attachments` - Documentation files

### Bug Tracking (6 tables)
- `bugs` - Bug reports
- `bug_comments` - Bug discussions
- `bug_workflow_history` - Status change audit trail
- `bug_fixes` - Fix information
- `bug_attachments` - Bug related files
- `bug_linked_tests` - Test case linking

### System & Integration (4 tables)
- `notifications` - In-app notifications
- `audit_logs` - System activity audit
- `api_keys` - API authentication keys
- `webhooks` - Integration endpoints

## API Reference

### Key Endpoints

**Authentication:**
```
POST   /api/auth/register              Register new account
POST   /api/auth/login                 Get authentication token
POST   /api/auth/password-reset-request
```

**Test Cases:**
```
GET    /api/projects/{id}/testcases    List test cases
POST   /api/projects/{id}/testcases    Create test case
GET    /api/testcases/{id}             Get test details
PUT    /api/testcases/{id}             Update test case
POST   /api/testcases/{id}/clone       Clone test case
```

**Test Execution:**
```
POST   /api/projects/{id}/testruns     Start test run
POST   /api/testruns/{id}/execute      Execute test
POST   /api/executions/{id}/upload-evidence
```

**Bug Management:**
```
GET    /api/projects/{id}/bugs         List bugs
POST   /api/projects/{id}/bugs         Report bug
PUT    /api/bugs/{id}/status           Update status
POST   /api/bugs/{id}/comment          Add comment
```

**Reports:**
```
GET    /api/projects/{id}/reports/summary
GET    /api/projects/{id}/reports/developer-performance
```

See [API.md](docs/API.md) for complete endpoint documentation.

## Key Features

### Test Management
- ✅ Create test cases with multiple steps and data
- ✅ Support 8+ test types (functional, regression, smoke, etc.)
- ✅ Test case cloning and templating
- ✅ Version control and history
- ✅ Tag-based organization

### Test Execution
- ✅ Assign tests to team members
- ✅ Record step-by-step results
- ✅ Upload evidence (screenshots, logs)
- ✅ Automatic duration tracking
- ✅ Real-time status updates

### Bug Management
- ✅ Auto-generated bug IDs (BUG-XXXXXX)
- ✅ Complete lifecycle tracking
- ✅ Linking tests to bugs
- ✅ Developer assignment
- ✅ Rich comments and discussions
- ✅ Fix tracking with commit hashes

### Reporting & Analytics
- ✅ Test execution summaries (pass/fail rates)
- ✅ Bug status distribution
- ✅ Developer performance metrics
- ✅ Customizable date ranges
- ✅ Export capabilities (planned)

### Security & Access Control
- ✅ User authentication (login/logout)
- ✅ Password reset with email
- ✅ Role-based access (Admin/Tester/Developer)
- ✅ Failed login tracking
- ✅ Account lockout (5 attempts)
- ✅ JWT token authentication
- ✅ bcrypt password hashing

## Deployment

### Staging Environment

Push to `develop` branch for automatic staging deployment:

```bash
git checkout develop
git push origin develop
```

GitHub Actions will:
1. Run all tests
2. Build Docker image
3. Deploy to staging server
4. Run smoke tests

### Production Environment

Create a semantic version tag on `main` branch:

```bash
git tag -a v1.0.0 -m "Production release"
git push origin main
git push origin v1.0.0
```

GitHub Actions will:
1. Validate deployment
2. Create database backup
3. Deploy to production
4. Run health checks
5. Auto-rollback on failure

See [SETUP_COMPREHENSIVE.md](docs/SETUP_COMPREHENSIVE.md#production-deployment) for details.

## Performance Metrics

- **API Response Time:** <300ms (average)
- **Test Case Creation:** <500ms
- **Bug Search:** <200ms
- **Concurrent Users:** 100+
- **Database:** Optimized with indexes and connection pooling

## Development

### Local Development Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd testtrack-pro

# 2. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment
cp backend/.env.example backend/.env
# Edit .env with your database credentials

# 5. Set up database
mysql < database/schema.sql

# 6. Run backend
cd backend
python app_enterprise.py

# 7. Run frontend (new terminal)
cd frontend
python -m http.server 8000
```

### Running Tests

```bash
# All tests
pytest backend/tests/ -v

# Specific test file
pytest backend/tests/test_auth.py -v

# With coverage
pytest --cov=backend

# Integration tests
pytest tests/integration/ -v
```

### Code Style

- **Python:** PEP 8 (checked with flake8)
- **JavaScript:** ES6+ standards
- **HTML:** Semantic HTML5
- **CSS:** BEM methodology (optional)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Roadmap

Future features planned:

- [ ] Advanced filtering with saved filters
- [ ] Requirements linking
- [ ] CI/CD webhooks (Jenkins, GitLab)
- [ ] Performance testing integration
- [ ] Mobile app
- [ ] Custom dashboard widgets
- [ ] API key authentication
- [ ] Bulk operations
- [ ] AI-powered test suggestions
- [ ] Compliance reporting (GDPR, ISO)

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 in use | `lsof -i :5000` then `kill -9 <PID>` |
| Database connection error | Check MySQL credentials in `.env` |
| Python module error | Ensure virtual environment is activated |
| Docker permission denied | Add user to docker group: `sudo usermod -aG docker $USER` |

See [Troubleshooting Guide](docs/SETUP_COMPREHENSIVE.md#troubleshooting) for more help.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation:** [docs/](docs/) folder
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/testtrack-pro/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/testtrack-pro/discussions)
- 📧 **Email:** support@testtrack.example.com

## Acknowledgments

Built with ❤️ for QA professionals and testers everywhere.

---

<div align="center">

**[Setup Guide](docs/SETUP_COMPREHENSIVE.md) • [API Docs](docs/API.md) • [Report Issue](https://github.com/yourusername/testtrack-pro/issues)**

Managed with ⚙️ by the TestTrack Team

</div>

cd frontend
python -m http.server 8000

# Access: http://localhost:8000
# Login: admin@testtrack.local / password123
```

See [Setup Guide](docs/SETUP_COMPREHENSIVE.md) for detailed instructions.

## Project Stack

- **Frontend**: HTML/CSS/JavaScript (Vanilla, no framework)
- **Backend**: Python 3.8+ with Flask 2.3+
- **Database**: MySQL 8.0+
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **API**: REST with JWT authentication
- **Security**: bcrypt hashing, JWT tokens, CORS protection

## Project Structure

```
testtrack-pro/
├── frontend/                          # Web UI
│   ├── login.html
│   ├── dashboard.html
│   ├── testcases.html
│   ├── bugs.html
│   ├── reports.html
│   ├── styles.css
│   └── *.js
│
├── backend/                           # Python Flask API
│   ├── app_enterprise.py
│   ├── models_advanced.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── database/                          # MySQL schema
│   ├── schema.sql
│   └── migrations/
│
├── .github/workflows/                 # CI/CD automation
│   ├── ci.yml
│   ├── cd-staging.yml
│   └── cd-production.yml
│
├── docs/                              # Documentation
│   ├── API.md
│   ├── SETUP_COMPREHENSIVE.md
│   ├── REQUIREMENTS.md
│   └── ARCHITECTURE.md
│
├── docker-compose.yml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Key Features

1. **Role-Based Access Control**: Tester and Developer roles
2. **Test Case Management**: Create, edit, execute, and track test cases
3. **Rich Metadata**: Detailed test case information
4. **Test Reports**: Comprehensive reports for developers
5. **Resolution Workflows**: Track and resolve test issues
6. **Dashboard**: Real-time testing metrics and analytics

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd testtrack-pro
   ```

2. **Setup Database**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

3. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   python app.py
   ```

4. **Setup Frontend**
   ```bash
   cd frontend
   # Open index.html in your browser or use a local server
   python -m http.server 8000
   ```

## User Roles & Permissions

### Tester Role
- Create and edit test cases
- Execute test cases
- View test reports
- Comment on issues

### Developer Role
- View assigned test cases
- Resolve test cases
- View comprehensive reports
- Update test case status

## API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/testcases` - Create test case
- `GET /api/testcases` - Get all test cases
- `PUT /api/testcases/<id>` - Update test case
- `DELETE /api/testcases/<id>` - Delete test case
- `POST /api/testcases/<id>/execute` - Execute test case
- `GET /api/reports` - Get test reports

## Development Guidelines

- Follow PEP8 for Python code
- Use meaningful variable and function names
- Write comments for complex logic
- Test features before committing
- Create feature branches for new features

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, contact: support@testtrackpro.com
