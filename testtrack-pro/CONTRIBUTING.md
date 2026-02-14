# Contributing to TestTrack Pro

Thank you for your interest in contributing to TestTrack Pro! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Questions](#questions)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discrimination
- Offensive comments
- Deliberate intimidation
- Unwelcome attention or advances

## How to Contribute

### Types of Contributions

1. **Code Contributions**
   - Bug fixes
   - Feature implementations
   - Performance improvements
   - Code refactoring

2. **Documentation**
   - README improvements
   - API documentation
   - Setup guides
   - Troubleshooting guides

3. **Testing**
   - Test case development
   - Bug reporting
   - Testing different environments
   - Performance testing

4. **Community Support**
   - Answering questions
   - Helping other users
   - Reporting issues
   - Feature discussions

## Development Setup

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Git
- Docker (recommended)

### Local Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/testtrack-pro.git
cd testtrack-pro

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -r backend/requirements.txt
pip install pytest pytest-cov black flake8 mypy

# 4. Set up environment file
cp backend/.env.example backend/.env
# Edit .env with your local database credentials

# 5. Initialize database
mysql < database/schema.sql

# 6. Verify setup
python backend/app_enterprise.py
```

### Using Docker

```bash
# Build and start services
docker-compose up --build

# Run tests in container
docker-compose exec backend pytest -v

# Access database in container
docker-compose exec mysql mysql -u testtrack -p
```

## Coding Standards

### Python Code Style

We follow **PEP 8** with the following tools:

```bash
# Format code automatically
black backend/ --line-length 100

# Check style
flake8 backend/
  - Max line length: 100
  - Ignore W503 (line break before binary operator)

# Type checking
mypy backend/ --ignore-missing-imports
  - Optional but recommended
```

### Python Best Practices

```python
# 1. Use type hints
def create_test_case(project_id: int, title: str, description: str) -> dict:
    pass

# 2. Use meaningful variable names
# ✅ Good
user_count = 10
is_active = True

# ❌ Avoid
uc = 10
ia = True

# 3. Write docstrings
def add_comment(bug_id: int, comment_text: str) -> None:
    """Add comment to a bug.
    
    Args:
        bug_id: The bug ID
        comment_text: Comment text content
        
    Returns:
        None
    """
    pass

# 4. Use list comprehensions, not loops
# ✅ Good
active_users = [u for u in users if u.is_active]

# ❌ Avoid
active_users = []
for u in users:
    if u.is_active:
        active_users.append(u)
```

### JavaScript Code Style

```javascript
// 1. Use const/let, not var
const apiUrl = 'http://localhost:5000/api';
let currentUser = null;

// 2. Use async/await, not callbacks
// ✅ Good
async function loadTestCases() {
    const response = await fetch('/api/testcases');
    return response.json();
}

// ❌ Avoid
function loadTestCases(callback) {
    fetch('/api/testcases', (response) => {
        callback(response);
    });
}

// 3. Use meaningful names
// ✅ Good
const getUserPermissions = () => { ... }

// ❌ Avoid
const gup = () => { ... }

// 4. Use arrow functions for callbacks
// ✅ Good
data.map((item) => item.name)

// ❌ Avoid
data.map(function(item) { return item.name; })
```

### HTML/CSS

- Use semantic HTML5 elements
- Use CSS classes (BEM convention optional)
- Keep inline styles minimal
- Ensure accessibility (alt text, ARIA labels)

### SQL

```sql
-- Use uppercase for keywords
SELECT id, name FROM projects WHERE status = 'active';

-- Use meaningful aliases
SELECT u.id, u.email, COUNT(t.id) as test_count
FROM users u
LEFT JOIN test_cases t ON u.id = t.created_by
GROUP BY u.id;

-- Use transactions for complex operations
BEGIN TRANSACTION;
INSERT INTO bugs VALUES (...);
INSERT INTO bug_workflow_history VALUES (...);
COMMIT;
```

## Git Workflow

### Branch Naming

Use descriptive branch names with prefixes:

```bash
# Feature
git checkout -b feature/test-case-cloning

# Bug fix
git checkout -b fix/password-reset-email

# Documentation
git checkout -b docs/api-documentation

# Refactoring
git checkout -b refactor/auth-module
```

### Commit Messages

Follow conventional commits format:

```bash
# Format: <type>(<scope>): <subject>

# Examples:
feat(testcases): add test case cloning
fix(auth): resolve password reset token expiry
docs(setup): add deployment guide
refactor(database): optimize query performance
test(bugs): add bug creation tests
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **refactor:** Code refactoring (no feature change)
- **test:** Test additions or modifications
- **chore:** Build, dependencies, tooling
- **perf:** Performance improvements
- **style:** Formatting (doesn't affect functionality)

### Commit Template

```bash
# Keep commits focused - one feature/fix per commit

# Good commit
git commit -m "feat(bugs): add bug assignment notification

- Send email when bug is assigned
- Create in-app notification
- Update bug status history"

# Avoid large commits with mixed changes
git commit -m "Various improvements and fixes"
```

## Pull Request Process

### Before Submitting

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following coding standards
   - Add tests for new features
   - Update documentation

3. **Test Locally**
   ```bash
   # Run code style checks
   black backend/
   flake8 backend/
   mypy backend/
   
   # Run tests
   pytest backend/tests/ -v
   
   # Test manual functionality
   ```

4. **Update Documentation**
   - Add/update docstrings
   - Update README if needed
   - Update API documentation if endpoints changed

### Submitting PR

1. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Write descriptive PR title
   - Fill out PR template
   - Link related issues

3. **PR Template**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Specific change 1
- Specific change 2
- Specific change 3

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Documentation
- [ ] Updated README
- [ ] Updated API docs
- [ ] Updated setup guide

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Dependencies updated in requirements.txt

## Related Issues
Closes #123
```

### PR Review

- Address reviewer comments promptly
- Keep discussions professional and constructive
- Push follow-up commits to the same branch
- Don't force-push after review started

### Merging

- Ensure all CI checks pass
- Require at least one approval
- Use "Squash and merge" for clean history
- Delete branch after merging

## Reporting Bugs

### Before Reporting

1. Check [existing issues](https://github.com/yourusername/testtrack-pro/issues)
2. Check [documentation](docs/)
3. Try to reproduce the issue

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happened

## Environment
- OS: Windows 10 / macOS / Linux
- Python: 3.9
- MySQL: 8.0
- Browser: Chrome 120

## Extra Information
- Screenshots or logs
- Error messages
- Database state information
```

### Good Bug Reports

- ✅ Include steps to reproduce
- ✅ Provide environment details
- ✅ Share error messages
- ✅ Include screenshots if visual
- ✅ Check if issue exists

### Poor Bug Reports

- ❌ "Something isn't working"
- ❌ No environment details
- ❌ Can't reproduce
- ❌ Vague descriptions

## Suggesting Features

### Feature Request Template

```markdown
## Description
What problem does this solve?

## Proposed Solution
How should this work?

## Use Case
When/why would users need this?

## Alternative Solutions
Other approaches considered?

## Additional Context
- Screenshots/mockups
- Related issues
```

### Good Feature Suggestions

- ✅ Explain the problem clearly
- ✅ Describe proposed solution
- ✅ Show use cases
- ✅ Consider impact on existing features

## Questions

### Where to Ask

- **General Questions:** [GitHub Discussions](https://github.com/yourusername/testtrack-pro/discussions)
- **Bug Reports:** [GitHub Issues](https://github.com/yourusername/testtrack-pro/issues)
- **Feature Requests:** [GitHub Issues](https://github.com/yourusername/testtrack-pro/issues) with `enhancement` label
- **Email:** support@testtrack.example.com

## Additional Resources

- [Development Setup](docs/SETUP_COMPREHENSIVE.md)
- [API Documentation](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Commit Best Practices](https://chris.beams.io/posts/git-commit/)

## Recognition

Contributors will be:
- Added to [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Mentioned in release notes
- Recognized in README

## Questions?

Feel free to reach out:
- Open [GitHub Discussions](https://github.com/yourusername/testtrack-pro/discussions)
- Send email to support@testtrack.example.com
- Join our community chat (if available)

---

Thank you for contributing to TestTrack Pro! 🎉
