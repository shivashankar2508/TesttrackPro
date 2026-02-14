from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import User, TestCase, TestExecution, TestReport
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object('config.DevelopmentConfig')

# Sessions dictionary (in production, use proper session management)
sessions = {}

# ==================== Authentication Routes ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.authenticate(email, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create session
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
            'role': user['role']
        }
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'tester')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.get_by_email(email):
        return jsonify({'error': 'Email already registered'}), 400
    
    user_id = User.create(username, email, password, role)
    if not user_id:
        return jsonify({'error': 'Registration failed'}), 500
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout"""
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    if session_id in sessions:
        del sessions[session_id]
    return jsonify({'success': True, 'message': 'Logout successful'}), 200

# ==================== Test Case Routes ====================

@app.route('/api/testcases', methods=['GET'])
def get_testcases():
    """Get all test cases with filters"""
    filters = {}
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('module'):
        filters['module'] = request.args.get('module')
    if request.args.get('priority'):
        filters['priority'] = request.args.get('priority')
    
    testcases = TestCase.get_all(filters)
    return jsonify({
        'success': True,
        'count': len(testcases) if testcases else 0,
        'data': testcases or []
    }), 200

@app.route('/api/testcases', methods=['POST'])
def create_testcase():
    """Create new test case"""
    data = request.get_json()
    
    required_fields = ['title', 'description', 'module', 'steps', 'expected_result', 'created_by']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    test_case_id = TestCase.create(
        title=data['title'],
        description=data['description'],
        module=data['module'],
        steps=data['steps'],
        expected_result=data['expected_result'],
        created_by=data['created_by'],
        priority=data.get('priority', 'medium')
    )
    
    if not test_case_id:
        return jsonify({'error': 'Failed to create test case'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Test case created successfully',
        'test_case_id': test_case_id
    }), 201

@app.route('/api/testcases/<int:test_case_id>', methods=['GET'])
def get_testcase(test_case_id):
    """Get specific test case"""
    testcase = TestCase.get_by_id(test_case_id)
    if not testcase:
        return jsonify({'error': 'Test case not found'}), 404
    
    return jsonify({
        'success': True,
        'data': testcase
    }), 200

@app.route('/api/testcases/<int:test_case_id>', methods=['PUT'])
def update_testcase(test_case_id):
    """Update test case"""
    data = request.get_json()
    
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    result = TestCase.update(test_case_id, **data)
    if result == 0:
        return jsonify({'error': 'No updates made'}), 400
    
    return jsonify({
        'success': True,
        'message': 'Test case updated successfully'
    }), 200

@app.route('/api/testcases/<int:test_case_id>', methods=['DELETE'])
def delete_testcase(test_case_id):
    """Delete test case"""
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    result = TestCase.delete(test_case_id)
    if result == 0:
        return jsonify({'error': 'Failed to delete test case'}), 500
    
    return jsonify({
        'success': True,
        'message': 'Test case deleted successfully'
    }), 200

# ==================== Test Execution Routes ====================

@app.route('/api/testcases/<int:test_case_id>/execute', methods=['POST'])
def execute_testcase(test_case_id):
    """Execute test case"""
    data = request.get_json()
    
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    execution_id = TestExecution.create(
        test_case_id=test_case_id,
        executed_by=data.get('executed_by'),
        status=data.get('status', 'pending'),
        notes=data.get('notes')
    )
    
    if not execution_id:
        return jsonify({'error': 'Failed to execute test case'}), 500
    
    # Update test case status
    TestCase.update(test_case_id, status=data.get('status', 'pending'))
    
    return jsonify({
        'success': True,
        'message': 'Test case executed successfully',
        'execution_id': execution_id
    }), 201

@app.route('/api/testcases/<int:test_case_id>/executions', methods=['GET'])
def get_testcase_executions(test_case_id):
    """Get execution history for test case"""
    if not TestCase.get_by_id(test_case_id):
        return jsonify({'error': 'Test case not found'}), 404
    
    executions = TestExecution.get_by_test_case(test_case_id)
    return jsonify({
        'success': True,
        'count': len(executions) if executions else 0,
        'data': executions or []
    }), 200

# ==================== Reports Routes ====================

@app.route('/api/reports/summary', methods=['GET'])
def get_report_summary():
    """Get test summary report"""
    summary = TestReport.get_summary()
    return jsonify({
        'success': True,
        'data': summary
    }), 200

@app.route('/api/reports/by-module', methods=['GET'])
def get_report_by_module():
    """Get test report by module"""
    report = TestReport.get_by_module()
    return jsonify({
        'success': True,
        'data': report or []
    }), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'TestTrack Pro API is running'
    }), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Connect to database
    if db.connect():
        print("Starting TestTrack Pro API server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to connect to database")
