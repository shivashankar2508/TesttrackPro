# TestTrack Pro API Documentation

## Overview

TestTrack Pro API is a comprehensive RESTful API for managing test cases, executions, bugs, and generating reports. The API uses JWT-based authentication.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints (except registration and health check) require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <session_id>
```

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass@123",
  "full_name": "John Doe",
  "role": "tester"  // optional: tester, developer, admin
}

Response: 201
{
  "success": true,
  "message": "Registered successfully. Verify email to activate.",
  "user_id": 1
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass@123"
}

Response: 200
{
  "success": true,
  "message": "Login successful",
  "session_id": "abc123def456...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "tester"
  }
}
```

#### Logout
```
POST /auth/logout
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "message": "Logged out"
}
```

#### Request Password Reset
```
POST /auth/password-reset-request
Content-Type: application/json

{
  "email": "john@example.com"
}

Response: 200
{
  "success": true,
  "message": "Reset link sent to email",
  "reset_token": "abc123..."
}
```

### Projects

#### List Projects
```
GET /projects
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "TestTrack Pro",
      "description": "Main testing platform",
      "key": "TTP",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Project
```
POST /projects
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "name": "Mobile App v2.0",
  "description": "Mobile testing project",
  "key": "MOBILE"
}

Response: 201
{
  "success": true,
  "message": "Project created successfully",
  "project_id": 2
}
```

### Test Cases

#### Get Test Cases
```
GET /projects/{project_id}/testcases?status=draft&module=Authentication&priority=high
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "test_case_id": "TC-000001",
      "title": "Login with valid credentials",
      "description": "Verify user can login",
      "module": "Authentication",
      "type": "functional",
      "priority": "high",
      "severity": "critical",
      "status": "approved",
      "estimated_duration": 5,
      "version": 2,
      "created_at": "2024-01-15T10:30:00Z",
      "steps": [
        {
          "step_number": 1,
          "action": "Navigate to login page",
          "expected_result": "Login page loads"
        }
      ],
      "tags": ["login", "smoke-test", "P1"]
    }
  ]
}
```

#### Create Test Case
```
POST /projects/{project_id}/testcases
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "title": "Login with valid credentials",
  "description": "Verify user can login with valid credentials",
  "module": "Authentication",
  "type": "functional",
  "priority": "high",
  "severity": "critical",
  "preconditions": "1. User account exists\n2. User is not logged in",
  "test_data": "Email: test@example.com\nPassword: Test@123",
  "environment": "Chrome 120+, Windows 11",
  "postconditions": "User is logged in",
  "cleanup_steps": "1. Logout user",
  "estimated_duration": 5,
  "steps": [
    {
      "action": "Open login page",
      "test_data": "URL: https://app.example.com/login",
      "expected_result": "Login page loads",
      "notes": "Page load time: 2.3s"
    },
    {
      "action": "Enter credentials",
      "test_data": "Email: test@example.com, Password: Test@123",
      "expected_result": "Credentials accepted"
    },
    {
      "action": "Click login",
      "expected_result": "User redirected to dashboard"
    }
  ]
}

Response: 201
{
  "success": true,
  "message": "Test case created successfully",
  "test_case_id": "TC-000001",
  "id": 1
}
```

#### Get Test Case
```
GET /testcases/{test_case_id}
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": { ... }
}
```

#### Update Test Case
```
PUT /testcases/{test_case_id}
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "priority": "critical",
  "status": "approved",
  "module": "Authentication"
}

Response: 200
{
  "success": true,
  "message": "Test case updated successfully"
}
```

#### Delete Test Case
```
DELETE /testcases/{test_case_id}
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "message": "Test case deleted successfully"
}
```

#### Clone Test Case
```
POST /testcases/{test_case_id}/clone
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "clone_attachments": false
}

Response: 201
{
  "success": true,
  "message": "Test case cloned successfully",
  "new_test_case_id": "TC-000002"
}
```

### Test Execution

#### Create Test Run
```
POST /projects/{project_id}/testruns
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "name": "Sprint 5 Regression",
  "description": "Full regression test cycle",
  "milestone_id": 1,
  "planned_start_date": "2024-01-20",
  "planned_end_date": "2024-01-25"
}

Response: 201
{
  "success": true,
  "message": "Test run created successfully",
  "test_run_id": "TR-000001",
  "id": 1
}
```

#### Execute Test
```
POST /testruns/{test_run_id}/execute
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "test_case_id": 1,
  "step_results": [
    {
      "step_number": 1,
      "actual_result": "Page loaded successfully",
      "status": "passed"
    },
    {
      "step_number": 2,
      "actual_result": "Error: Invalid format",
      "status": "failed",
      "notes": "Email validation issue"
    }
  ]
}

Response: 201
{
  "success": true,
  "message": "Test executed successfully",
  "execution_id": 1
}
```

#### Upload Evidence
```
POST /executions/{execution_id}/upload-evidence
Authorization: Bearer <session_id>
Content-Type: multipart/form-data

- file: <binary file>
- step_id: 2
- evidence_type: screenshot

Response: 201
{
  "success": true,
  "message": "Evidence uploaded successfully",
  "file_url": "/uploads/1/screenshot.png"
}
```

### Bugs

#### Get Bugs
```
GET /projects/{project_id}/bugs?status=new&priority=p1_urgent&assigned_to=2
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "bug_id": "BUG-000001",
      "title": "Login fails with valid credentials",
      "description": "System shows invalid credentials",
      "severity": "blocker",
      "priority": "p1_urgent",
      "status": "open",
      "assigned_to": 2,
      "reported_by": 1,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Bug
```
POST /projects/{project_id}/bugs
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "title": "Login fails with valid credentials",
  "description": "User cannot login despite valid credentials",
  "steps_to_reproduce": "1. Go to login page\n2. Enter valid email\n3. Enter valid password\n4. Click sign in",
  "expected_behavior": "User should be logged in",
  "actual_behavior": "Error: Invalid credentials",
  "severity": "blocker",
  "priority": "p1_urgent",
  "environment": "Chrome 120, Windows 11",
  "affected_version": "v2.4.1",
  "assigned_to": 2
}

Response: 201
{
  "success": true,
  "message": "Bug created successfully",
  "bug_id": "BUG-000001",
  "id": 1
}
```

#### Get Bug
```
GET /bugs/{bug_id}
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": { ... }
}
```

#### Update Bug Status
```
PUT /bugs/{bug_id}/status
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "status": "in_progress",
  "notes": "Started working on the fix"
}

Response: 200
{
  "success": true,
  "message": "Bug status updated successfully"
}
```

#### Assign Bug
```
PUT /bugs/{bug_id}/assign
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "assigned_to": 2
}

Response: 200
{
  "success": true,
  "message": "Bug assigned successfully"
}
```

#### Add Comment to Bug
```
POST /bugs/{bug_id}/comment
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "comment": "Found the issue in AuthService.validateCredentials()",
  "is_internal": false
}

Response: 201
{
  "success": true,
  "message": "Comment added successfully"
}
```

#### Mark Bug as Fixed
```
POST /bugs/{bug_id}/fix
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "fix_notes": "Fixed null pointer in auth validation",
  "commit_hash": "abc123def456",
  "branch_name": "fix/login-validation"
}

Response: 200
{
  "success": true,
  "message": "Bug marked as fixed"
}
```

### Test Suites

#### Create Test Suite
```
POST /projects/{project_id}/suites
Authorization: Bearer <session_id>
Content-Type: application/json

{
  "name": "Authentication Suite",
  "description": "All login-related tests",
  "module": "Authentication",
  "test_case_ids": [1, 2, 3]
}

Response: 201
{
  "success": true,
  "message": "Test suite created successfully",
  "suite_id": 1
}
```

### Reports

#### Get Summary Report
```
GET /projects/{project_id}/reports/summary
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": {
    "tests": {
      "total_executed": 145,
      "passed": 128,
      "failed": 12,
      "blocked": 3,
      "skipped": 2
    },
    "bugs": {
      "total_bugs": 15,
      "new_bugs": 2,
      "open_bugs": 5,
      "in_progress": 3,
      "fixed": 4,
      "verified": 1
    }
  }
}
```

#### Get Developer Performance Report
```
GET /projects/{project_id}/reports/developer-performance
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": [
    {
      "username": "mike_developer",
      "assigned_count": 15,
      "resolved": 12,
      "verified": 10
    }
  ]
}
```

### Notifications

#### Get Notifications
```
GET /notifications
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Bug BUG-000001 assigned to you",
      "message": "Login fails with valid credentials",
      "notification_type": "bug_assigned",
      "is_read": false,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Mark Notification as Read
```
PUT /notifications/{notification_id}/read
Authorization: Bearer <session_id>

Response: 200
{
  "success": true,
  "message": "Notification marked as read"
}
```

### Health Check

#### Health Check
```
GET /health

Response: 200
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123Z",
  "database": "connected"
}
```

## Error Responses

All error responses follow this format:

```
{
  "error": "Error message describing what went wrong"
}
```

Common HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

API implements rate limiting: 100 requests per minute per user.

Rate limit information is included in response headers:
- `X-RateLimit-Limit: 100`
- `X-RateLimit-Remaining: 95`
- `X-RateLimit-Reset: 1705316400`

## Pagination

List endpoints support pagination:

```
GET /projects/{project_id}/testcases?page=1&limit=20
```

Response includes:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

## Filtering & Sorting

Test cases can be filtered by:
- `status` - draft, ready_for_review, approved, deprecated, archived
- `module` - Any module name
- `priority` - low, medium, high, critical
- `type` - functional, regression, smoke, integration, uat, performance, security, usability

Bugs can be filtered by:
- `status` - new, open, in_progress, fixed, verified, closed, reopened, wont_fix, duplicate
- `priority` - p4_low, p3_medium, p2_high, p1_urgent
- `severity` - trivial, minor, major, critical, blocker
- `assigned_to` - User ID

## Webhook Events

TestTrack Pro can send webhooks for the following events:

- `bug.created` - New bug created
- `bug.assigned` - Bug assigned to developer
- `bug.status_changed` - Bug status updated
- `test.completed` - Test execution completed
- `comment.added` - Comment added to bug/test

Configure webhooks in project settings.
