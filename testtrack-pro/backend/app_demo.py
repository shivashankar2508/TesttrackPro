"""
TestTrack Pro - Demo/Development Version
Uses SQLite for local development without requiring MySQL installation
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Mock data - in-memory storage
demo_db = {
    'users': {
        1: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@testtrack.local',
            'full_name': 'Admin User',
            'role': 'admin',
            'status': 'active'
        },
        2: {
            'id': 2,
            'username': 'tester',
            'email': 'tester@testtrack.local',
            'full_name': 'Test Tester',
            'role': 'tester',
            'status': 'active'
        },
        3: {
            'id': 3,
            'username': 'developer',
            'email': 'developer@testtrack.local',
            'full_name': 'Dev Developer',
            'role': 'developer',
            'status': 'active'
        }
    },
    'projects': {
        1: {
            'id': 1,
            'name': 'TestTrack Pro',
            'description': 'Main testing platform',
            'key': 'TTP',
            'status': 'active',
            'created_at': datetime.utcnow().isoformat()
        }
    },
    'testcases': {
        1: {
            'id': 1,
            'test_case_id': 'TC-000001',
            'title': 'Login with valid credentials',
            'description': 'Verify user can login with valid email and password',
            'module': 'Authentication',
            'type': 'functional',
            'priority': 'high',
            'severity': 'critical',
            'status': 'approved',
            'project_id': 1,
            'created_at': datetime.utcnow().isoformat(),
            'steps': [
                {'step_number': 1, 'action': 'Navigate to login page', 'expected_result': 'Login page loads'},
                {'step_number': 2, 'action': 'Enter valid email', 'expected_result': 'Email field accepts input'},
                {'step_number': 3, 'action': 'Click login', 'expected_result': 'User redirected to dashboard'}
            ]
        },
        2: {
            'id': 2,
            'test_case_id': 'TC-000002',
            'title': 'Create test case',
            'description': 'Verify test cases can be created',
            'module': 'Test Management',
            'type': 'functional',
            'priority': 'high',
            'severity': 'major',
            'status': 'approved',
            'project_id': 1,
            'created_at': datetime.utcnow().isoformat(),
            'steps': []
        }
    },
    'bugs': {
        1: {
            'id': 1,
            'bug_id': 'BUG-000001',
            'title': 'Login fails with valid credentials',
            'description': 'System shows invalid credentials error',
            'severity': 'blocker',
            'priority': 'p1_urgent',
            'status': 'open',
            'assigned_to': 3,
            'reported_by': 2,
            'project_id': 1,
            'created_at': datetime.utcnow().isoformat(),
            'comments': []
        },
        2: {
            'id': 2,
            'bug_id': 'BUG-000002',
            'title': 'Reset password email not received',
            'description': 'Email verification not sent to user email',
            'severity': 'critical',
            'priority': 'p2_high',
            'status': 'new',
            'assigned_to': None,
            'reported_by': 2,
            'project_id': 1,
            'created_at': datetime.utcnow().isoformat(),
            'comments': []
        }
    },
    'test_runs': {
        1: {
            'id': 1,
            'name': 'Sprint 1 Regression',
            'description': 'Full regression test',
            'project_id': 1,
            'status': 'in_progress',
            'created_at': datetime.utcnow().isoformat()
        }
    }
}

# Session storage
sessions = {}
next_session_id = 1000

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'TestTrack Pro Demo Server is running',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'sqlite (demo mode)',
        'version': '1.0.0-demo'
    }), 200

# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint - demo version"""
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    # Demo: accept any email/password for demo purposes
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    # Find user by email
    user = None
    for u in demo_db['users'].values():
        if u['email'] == email:
            user = u
            break
    
    if not user:
        # Demo: create user dynamically
        user_id = max([u['id'] for u in demo_db['users'].values()]) + 1
        user = {
            'id': user_id,
            'username': email.split('@')[0],
            'email': email,
            'full_name': email.split('@')[0].title(),
            'role': 'tester',
            'status': 'active'
        }
        demo_db['users'][user_id] = user
    
    # Create session
    global next_session_id
    session_id = f'demo_session_{next_session_id}'
    next_session_id += 1
    sessions[session_id] = {
        'user_id': user['id'],
        'email': user['email'],
        'created_at': datetime.utcnow()
    }
    
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

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register endpoint - demo version"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    full_name = data.get('full_name')
    
    if not all([email, password, username, full_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    for u in demo_db['users'].values():
        if u['email'] == email:
            return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user_id = max([u['id'] for u in demo_db['users'].values()]) + 1
    new_user = {
        'id': user_id,
        'username': username,
        'email': email,
        'full_name': full_name,
        'role': 'tester',
        'status': 'active'
    }
    demo_db['users'][user_id] = new_user
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        session_id = auth_header[7:]
        if session_id in sessions:
            del sessions[session_id]
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200

# ============================================================================
# PROJECTS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    return jsonify({
        'success': True,
        'data': list(demo_db['projects'].values())
    }), 200

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create new project"""
    data = request.get_json()
    project_id = max([p['id'] for p in demo_db['projects'].values()]) + 1
    
    new_project = {
        'id': project_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'key': data.get('key'),
        'status': 'active',
        'created_at': datetime.utcnow().isoformat()
    }
    demo_db['projects'][project_id] = new_project
    
    return jsonify({
        'success': True,
        'message': 'Project created',
        'project_id': project_id
    }), 201

# ============================================================================
# TEST CASES
# ============================================================================

@app.route('/api/projects/<int:project_id>/testcases', methods=['GET'])
def get_testcases(project_id):
    """Get test cases for a project"""
    testcases = [tc for tc in demo_db['testcases'].values() if tc['project_id'] == project_id]
    return jsonify({
        'success': True,
        'count': len(testcases),
        'data': testcases
    }), 200

@app.route('/api/projects/<int:project_id>/testcases', methods=['POST'])
def create_testcase(project_id):
    """Create test case"""
    data = request.get_json()
    tc_id = max([tc['id'] for tc in demo_db['testcases'].values()]) + 1
    tc_number = max([int(tc['test_case_id'].split('-')[1]) for tc in demo_db['testcases'].values()]) + 1
    
    new_tc = {
        'id': tc_id,
        'test_case_id': f'TC-{tc_number:06d}',
        'title': data.get('title'),
        'description': data.get('description'),
        'module': data.get('module'),
        'type': data.get('type', 'functional'),
        'priority': data.get('priority', 'medium'),
        'severity': data.get('severity', 'major'),
        'status': 'draft',
        'project_id': project_id,
        'created_at': datetime.utcnow().isoformat(),
        'steps': data.get('steps', [])
    }
    demo_db['testcases'][tc_id] = new_tc
    
    return jsonify({
        'success': True,
        'message': 'Test case created',
        'test_case_id': new_tc['test_case_id'],
        'id': tc_id
    }), 201

@app.route('/api/testcases/<int:tc_id>', methods=['GET'])
def get_testcase(tc_id):
    """Get test case details"""
    if tc_id not in demo_db['testcases']:
        return jsonify({'error': 'Test case not found'}), 404
    
    return jsonify({
        'success': True,
        'data': demo_db['testcases'][tc_id]
    }), 200

# ============================================================================
# BUGS
# ============================================================================

@app.route('/api/projects/<int:project_id>/bugs', methods=['GET'])
def get_bugs(project_id):
    """Get bugs for a project"""
    bugs = [b for b in demo_db['bugs'].values() if b['project_id'] == project_id]
    return jsonify({
        'success': True,
        'count': len(bugs),
        'data': bugs
    }), 200

@app.route('/api/projects/<int:project_id>/bugs', methods=['POST'])
def create_bug(project_id):
    """Create bug report"""
    data = request.get_json()
    bug_id = max([b['id'] for b in demo_db['bugs'].values()]) + 1
    bug_number = max([int(b['bug_id'].split('-')[1]) for b in demo_db['bugs'].values()]) + 1
    
    new_bug = {
        'id': bug_id,
        'bug_id': f'BUG-{bug_number:06d}',
        'title': data.get('title'),
        'description': data.get('description'),
        'severity': data.get('severity', 'major'),
        'priority': data.get('priority', 'p3_medium'),
        'status': 'new',
        'assigned_to': data.get('assigned_to'),
        'reported_by': 2,
        'project_id': project_id,
        'created_at': datetime.utcnow().isoformat(),
        'comments': []
    }
    demo_db['bugs'][bug_id] = new_bug
    
    return jsonify({
        'success': True,
        'message': 'Bug created',
        'bug_id': new_bug['bug_id'],
        'id': bug_id
    }), 201

@app.route('/api/bugs/<int:bug_id>/status', methods=['PUT'])
def update_bug_status(bug_id):
    """Update bug status"""
    if bug_id not in demo_db['bugs']:
        return jsonify({'error': 'Bug not found'}), 404
    
    data = request.get_json()
    demo_db['bugs'][bug_id]['status'] = data.get('status', 'open')
    
    return jsonify({
        'success': True,
        'message': 'Bug status updated'
    }), 200

@app.route('/api/bugs/<int:bug_id>/comment', methods=['POST'])
def add_bug_comment(bug_id):
    """Add comment to bug"""
    if bug_id not in demo_db['bugs']:
        return jsonify({'error': 'Bug not found'}), 404
    
    data = request.get_json()
    comment = {
        'id': len(demo_db['bugs'][bug_id]['comments']) + 1,
        'user_id': 2,
        'text': data.get('comment'),
        'created_at': datetime.utcnow().isoformat()
    }
    demo_db['bugs'][bug_id]['comments'].append(comment)
    
    return jsonify({
        'success': True,
        'message': 'Comment added'
    }), 201

# ============================================================================
# REPORTS
# ============================================================================

@app.route('/api/projects/<int:project_id>/reports/summary', methods=['GET'])
def get_summary_report(project_id):
    """Get test execution summary"""
    project_testcases = [tc for tc in demo_db['testcases'].values() if tc['project_id'] == project_id]
    project_bugs = [b for b in demo_db['bugs'].values() if b['project_id'] == project_id]
    
    return jsonify({
        'success': True,
        'data': {
            'project_id': project_id,
            'total_testcases': len(project_testcases),
            'testcases_by_status': {
                'draft': len([tc for tc in project_testcases if tc['status'] == 'draft']),
                'approved': len([tc for tc in project_testcases if tc['status'] == 'approved']),
                'deprecated': len([tc for tc in project_testcases if tc['status'] == 'deprecated'])
            },
            'bugs': {
                'total_bugs': len(project_bugs),
                'new': len([b for b in project_bugs if b['status'] == 'new']),
                'open': len([b for b in project_bugs if b['status'] == 'open']),
                'in_progress': len([b for b in project_bugs if b['status'] == 'in_progress']),
                'fixed': len([b for b in project_bugs if b['status'] == 'fixed']),
                'verified': len([b for b in project_bugs if b['status'] == 'verified']),
                'closed': len([b for b in project_bugs if b['status'] == 'closed'])
            }
        }
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║           TestTrack Pro - Demo Server (SQLite Mode)           ║
    ║                                                                ║
    ║  🚀 Starting TestTrack Pro Demo Server...                     ║
    ║                                                                ║
    ║  📍 Backend URL: http://localhost:5000                        ║
    ║  📍 Health Check: http://localhost:5000/health                ║
    ║                                                                ║
    ║  🔐 Default Credentials:                                      ║
    ║     Email: admin@testtrack.local                              ║
    ║     Password: any password (demo mode)                        ║
    ║                                                                ║
    ║  📊 Sample Data Included:                                     ║
    ║     ✓ 3 Users (Admin, Tester, Developer)                      ║
    ║     ✓ 1 Project (TestTrack Pro)                               ║
    ║     ✓ 2 Test Cases (TC-000001, TC-000002)                     ║
    ║     ✓ 2 Bugs (BUG-000001, BUG-000002)                         ║
    ║                                                                ║
    ║  ⚠️  NOTE: This is demo mode using in-memory SQLite.          ║
    ║     Data will not persist between server restarts.            ║
    ║                                                                ║
    ║  📖 API Documentation: docs/API.md                            ║
    ║  🔗 Frontend: http://localhost:8000                           ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
