"""
TestTrack Pro - Comprehensive Flask API
Enterprise-grade testing platform with all features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models_advanced import (
    User, Project, TestCase, TestRun, TestExecution, Bug, 
    TestSuite, Notification, Report
)
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object('config.DevelopmentConfig')

# Sessions dictionary
sessions = {}

# ==================== MIDDLEWARE & UTILITIES ====================

def get_session_user():
    """Get user from session"""
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    return sessions.get(session_id)

def require_auth(func):
    """Authentication decorator"""
    def wrapper(*args, **kwargs):
        if not get_session_user():
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    required = ['username', 'email', 'password', 'full_name']
    
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    
    user_id = User.create(
        data['username'], 
        data['email'], 
        data['password'], 
        data['full_name'],
        data.get('role', 'tester')
    )
    
    if not user_id:
        return jsonify({'error': 'Registration failed'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Registered successfully. Verify email to activate.',
        'user_id': user_id
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.authenticate(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session_id = os.urandom(16).hex()
    sessions[session_id] = user['id']
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'session_id': session_id,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
    }), 200

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """User logout"""
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    if session_id in sessions:
        del sessions[session_id]
    return jsonify({'success': True, 'message': 'Logged out'}), 200

@app.route('/api/auth/password-reset-request', methods=['POST'])
def password_reset_request():
    """Request password reset"""
    data = request.get_json()
    user = User.get_by_email(data.get('email'))
    
    if not user:
        return jsonify({'success': True, 'message': 'If email exists, reset link sent'}), 200
    
    token = User.create_reset_token(user['id'])
    
    return jsonify({
        'success': True,
        'message': 'Reset link sent to email',
        'reset_token': token  # In production, this would be sent via email
    }), 200

# ==================== TEST CASE ROUTES ====================

@app.route('/api/projects', methods=['GET'])
@require_auth
def list_projects():
    """List all projects"""
    projects = Project.get_all()
    return jsonify({
        'success': True,
        'data': projects or []
    }), 200

@app.route('/api/projects', methods=['POST'])
@require_auth
def create_project():
    """Create new project"""
    user_id = get_session_user()
    data = request.get_json()
    
    required = ['name', 'key', 'description']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    project_id = Project.create(
        data['name'],
        data['description'],
        data['key'],
        user_id
    )
    
    if not project_id:
        return jsonify({'error': 'Project creation failed'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Project created successfully',
        'project_id': project_id
    }), 201

@app.route('/api/projects/<int:project_id>/testcases', methods=['GET'])
@require_auth
def get_testcases(project_id):
    """Get test cases for project"""
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('module'):
        filters['module'] = request.args.get('module')
    if request.args.get('priority'):
        filters['priority'] = request.args.get('priority')
    
    testcases = TestCase.get_all(project_id, filters)
    return jsonify({
        'success': True,
        'count': len(testcases) if testcases else 0,
        'data': testcases or []
    }), 200

@app.route('/api/projects/<int:project_id>/testcases', methods=['POST'])
@require_auth
def create_testcase(project_id):
    """Create test case"""
    user_id = get_session_user()
    data = request.get_json()
    
    required = ['title', 'description', 'module', 'type', 'priority', 'severity']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = TestCase.create(
        project_id,
        data['title'],
        data['description'],
        data['module'],
        data['type'],
        data['priority'],
        data['severity'],
        data.get('preconditions'),
        data.get('test_data'),
        data.get('environment'),
        data.get('postconditions'),
        data.get('cleanup_steps'),
        data.get('estimated_duration'),
        user_id
    )
    
    if not result:
        return jsonify({'error': 'Test case creation failed'}), 500
    
    # Add steps if provided
    if 'steps' in data and isinstance(data['steps'], list):
        for i, step in enumerate(data['steps'], 1):
            TestCase.add_step(
                result['id'],
                i,
                step.get('action'),
                step.get('test_data'),
                step.get('expected_result'),
                step.get('notes')
            )
    
    return jsonify({
        'success': True,
        'message': 'Test case created successfully',
        'test_case_id': result['test_case_id'],
        'id': result['id']
    }), 201

@app.route('/api/testcases/<int:test_case_id>', methods=['GET'])
@require_auth
def get_testcase(test_case_id):
    """Get test case details"""
    testcase = TestCase.get_by_id(test_case_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404
    
    return jsonify({
        'success': True,
        'data': testcase
    }), 200

@app.route('/api/testcases/<int:test_case_id>', methods=['PUT'])
@require_auth
def update_testcase(test_case_id):
    """Update test case"""
    data = request.get_json()
    
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    result = TestCase.update(test_case_id, **data)
    
    return jsonify({
        'success': True,
        'message': 'Test case updated successfully'
    }), 200

@app.route('/api/testcases/<int:test_case_id>', methods=['DELETE'])
@require_auth
def delete_testcase(test_case_id):
    """Soft delete test case"""
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    TestCase.soft_delete(test_case_id)
    
    return jsonify({
        'success': True,
        'message': 'Test case deleted successfully'
    }), 200

@app.route('/api/testcases/<int:test_case_id>/clone', methods=['POST'])
@require_auth
def clone_testcase(test_case_id):
    """Clone test case"""
    data = request.get_json()
    
    result = TestCase.clone(test_case_id, data.get('clone_attachments', False))
    if not result:
        return jsonify({'error': 'Clone failed'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Test case cloned successfully',
        'new_test_case_id': result['test_case_id']
    }), 201

# ==================== TEST EXECUTION ROUTES ====================

@app.route('/api/projects/<int:project_id>/testruns', methods=['POST'])
@require_auth
def create_testrun(project_id):
    """Create test run"""
    user_id = get_session_user()
    data = request.get_json()
    
    required = ['name']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = TestRun.create(
        project_id,
        data['name'],
        data.get('description'),
        data.get('milestone_id'),
        data.get('planned_start_date'),
        data.get('planned_end_date'),
        user_id
    )
    
    if not result:
        return jsonify({'error': 'Test run creation failed'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Test run created successfully',
        'test_run_id': result['test_run_id'],
        'id': result['id']
    }), 201

@app.route('/api/testruns/<int:test_run_id>/execute', methods=['POST'])
@require_auth
def execute_test(test_run_id):
    """Execute test"""
    user_id = get_session_user()
    data = request.get_json()
    
    execution_id = TestExecution.create(
        test_run_id,
        data.get('test_case_id'),
        user_id
    )
    
    if not execution_id:
        return jsonify({'error': 'Execution failed'}), 500
    
    # Add step results if provided
    if 'step_results' in data:
        for step in data['step_results']:
            TestExecution.add_step_result(
                execution_id,
                step['step_number'],
                step.get('actual_result'),
                step.get('status'),
                step.get('notes')
            )
    
    return jsonify({
        'success': True,
        'message': 'Test executed successfully',
        'execution_id': execution_id
    }), 201

@app.route('/api/executions/<int:execution_id>/upload-evidence', methods=['POST'])
@require_auth
def upload_evidence(execution_id):
    """Upload evidence for execution"""
    user_id = get_session_user()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # In production, upload to cloud storage (Cloudinary, S3, etc)
    file_url = f"/uploads/{execution_id}/{file.filename}"
    
    TestExecution.upload_evidence(
        execution_id,
        request.form.get('step_id'),
        file.filename,
        file.content_type,
        len(file.read()),
        file_url,
        request.form.get('evidence_type', 'screenshot'),
        user_id
    )
    
    return jsonify({
        'success': True,
        'message': 'Evidence uploaded successfully',
        'file_url': file_url
    }), 201

# ==================== BUG MANAGEMENT ROUTES ====================

@app.route('/api/projects/<int:project_id>/bugs', methods=['GET'])
@require_auth
def get_bugs(project_id):
    """Get bugs for project"""
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('priority'):
        filters['priority'] = request.args.get('priority')
    if request.args.get('severity'):
        filters['severity'] = request.args.get('severity')
    if request.args.get('assigned_to'):
        filters['assigned_to'] = request.args.get('assigned_to')
    
    bugs = Bug.get_all(project_id, filters)
    return jsonify({
        'success': True,
        'count': len(bugs) if bugs else 0,
        'data': bugs or []
    }), 200

@app.route('/api/projects/<int:project_id>/bugs', methods=['POST'])
@require_auth
def create_bug(project_id):
    """Create bug report"""
    user_id = get_session_user()
    data = request.get_json()
    
    required = ['title', 'description', 'severity', 'priority']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = Bug.create(
        project_id,
        data['title'],
        data['description'],
        data.get('steps_to_reproduce'),
        data.get('expected_behavior'),
        data.get('actual_behavior'),
        data['severity'],
        data['priority'],
        data.get('environment'),
        data.get('affected_version'),
        user_id
    )
    
    if not result:
        return jsonify({'error': 'Bug creation failed'}), 500
    
    # Create notification for assignee
    if data.get('assigned_to'):
        Bug.assign(result['id'], data['assigned_to'])
        Notification.create(
            data['assigned_to'],
            f"Bug {result['bug_id']} assigned to you",
            f"New bug: {data['title']}",
            'bug_assigned',
            'bug',
            result['id']
        )
    
    return jsonify({
        'success': True,
        'message': 'Bug created successfully',
        'bug_id': result['bug_id'],
        'id': result['id']
    }), 201

@app.route('/api/bugs/<int:bug_id>', methods=['GET'])
@require_auth
def get_bug(bug_id):
    """Get bug details"""
    bug = Bug.get_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    
    return jsonify({
        'success': True,
        'data': bug
    }), 200

@app.route('/api/bugs/<int:bug_id>/status', methods=['PUT'])
@require_auth
def update_bug_status(bug_id):
    """Update bug status"""
    user_id = get_session_user()
    data = request.get_json()
    
    if not data.get('status'):
        return jsonify({'error': 'Status required'}), 400
    
    bug = Bug.get_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    
    Bug.update_status(bug_id, data['status'], user_id, data.get('notes'))
    
    # Notify reporters of status change
    Notification.create(
        bug['reported_by'],
        f"Bug {bug['bug_id']} status changed",
        f"Status changed from {bug['status']} to {data['status']}",
        'bug_status_changed',
        'bug',
        bug_id
    )
    
    return jsonify({
        'success': True,
        'message': 'Bug status updated successfully'
    }), 200

@app.route('/api/bugs/<int:bug_id>/assign', methods=['PUT'])
@require_auth
def assign_bug(bug_id):
    """Assign bug to developer"""
    data = request.get_json()
    
    if not data.get('assigned_to'):
        return jsonify({'error': 'Developer ID required'}), 400
    
    bug = Bug.get_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    
    Bug.assign(bug_id, data['assigned_to'])
    
    # Notify developer
    Notification.create(
        data['assigned_to'],
        f"Bug {bug['bug_id']} assigned to you",
        bug['title'],
        'bug_assigned',
        'bug',
        bug_id
    )
    
    return jsonify({
        'success': True,
        'message': 'Bug assigned successfully'
    }), 200

@app.route('/api/bugs/<int:bug_id>/comment', methods=['POST'])
@require_auth
def add_bug_comment(bug_id):
    """Add comment to bug"""
    user_id = get_session_user()
    data = request.get_json()
    
    if not data.get('comment'):
        return jsonify({'error': 'Comment required'}), 400
    
    bug = Bug.get_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    
    Bug.add_comment(bug_id, user_id, data['comment'], data.get('is_internal', False))
    
    return jsonify({
        'success': True,
        'message': 'Comment added successfully'
    }), 201

@app.route('/api/bugs/<int:bug_id>/fix', methods=['POST'])
@require_auth
def mark_bug_fixed(bug_id):
    """Mark bug as fixed"""
    user_id = get_session_user()
    data = request.get_json()
    
    bug = Bug.get_by_id(bug_id)
    if not bug:
        return jsonify({'error': 'Bug not found'}), 404
    
    # Add fix details
    Bug.add_fix_details(
        bug_id,
        user_id,
        data.get('fix_notes'),
        data.get('commit_hash'),
        data.get('branch_name')
    )
    
    # Update status
    Bug.update_status(bug_id, 'fixed', user_id)
    
    # Notify original reporter for re-test
    Notification.create(
        bug['reported_by'],
        f"Re-test requested for {bug['bug_id']}",
        'Please verify the fix on staging environment',
        'retest_requested',
        'bug',
        bug_id
    )
    
    return jsonify({
        'success': True,
        'message': 'Bug marked as fixed'
    }), 200

# ==================== TEST SUITES ROUTES ====================

@app.route('/api/projects/<int:project_id>/suites', methods=['POST'])
@require_auth
def create_suite(project_id):
    """Create test suite"""
    user_id = get_session_user()
    data = request.get_json()
    
    required = ['name']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    suite_id = TestSuite.create(
        project_id,
        data['name'],
        data.get('description'),
        data.get('module'),
        user_id
    )
    
    if not suite_id:
        return jsonify({'error': 'Suite creation failed'}), 500
    
    # Add test cases if provided
    if 'test_case_ids' in data:
        for i, tc_id in enumerate(data['test_case_ids']):
            TestSuite.add_test_case(suite_id, tc_id, i)
    
    return jsonify({
        'success': True,
        'message': 'Test suite created successfully',
        'suite_id': suite_id
    }), 201

# ==================== REPORTING ROUTES ====================

@app.route('/api/projects/<int:project_id>/reports/summary', methods=['GET'])
@require_auth
def get_summary_report(project_id):
    """Get test summary report"""
    test_summary = Report.get_test_execution_summary(project_id)
    bug_summary = Report.get_bug_summary(project_id)
    
    return jsonify({
        'success': True,
        'data': {
            'tests': test_summary,
            'bugs': bug_summary
        }
    }), 200

@app.route('/api/projects/<int:project_id>/reports/developer-performance', methods=['GET'])
@require_auth
def get_developer_performance(project_id):
    """Get developer performance report"""
    report = Report.get_bugs_by_developer(project_id)
    
    return jsonify({
        'success': True,
        'data': report or []
    }), 200

# ==================== NOTIFICATIONS ====================

@app.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    """Get user notifications"""
    user_id = get_session_user()
    notifications = Notification.get_unread(user_id)
    
    return jsonify({
        'success': True,
        'data': notifications or []
    }), 200

@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
@require_auth
def mark_notification_read(notification_id):
    """Mark notification as read"""
    Notification.mark_as_read(notification_id)
    
    return jsonify({
        'success': True,
        'message': 'Notification marked as read'
    }), 200

# ==================== HEALTH & STATUS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_healthy = db.connect() if not db.connection else True
    
    return jsonify({
        'status': 'healthy' if db_healthy else 'unhealthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if db_healthy else 'disconnected'
    }), 200 if db_healthy else 503

# ==================== ERROR HANDLING ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== APPLICATION STARTUP ====================

if __name__ == '__main__':
    # Connect to database
    if db.connect():
        print("✓ Database connected successfully")
        print("Starting TestTrack Pro API server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("✗ Failed to connect to database")
        print("Please ensure MySQL is running and credentials are correct")
