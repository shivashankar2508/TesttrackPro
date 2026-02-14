"""
TestTrack Pro - SQLite Version
Uses SQLite database for local development with persistent storage
No external database installation required
"""

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import uuid
from functools import wraps

# Load environment variables
load_dotenv()

# Database setup
DATABASE_PATH = 'testtrack.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default='tester')  # admin, tester, developer
    status = Column(String(50), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    key = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default='active')
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TestCase(Base):
    __tablename__ = 'test_cases'
    
    id = Column(Integer, primary_key=True)
    test_case_id = Column(String(50), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    module = Column(String(100))
    type = Column(String(50))  # functional, regression, smoke, etc
    priority = Column(String(50))  # low, medium, high, critical
    severity = Column(String(50))
    status = Column(String(50), default='draft')
    estimated_duration = Column(Integer)
    version = Column(Integer, default=1)
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Bug(Base):
    __tablename__ = 'bugs'
    
    id = Column(Integer, primary_key=True)
    bug_id = Column(String(50), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(50))  # trivial, minor, major, critical, blocker
    priority = Column(String(50))  # p4_low, p3_medium, p2_high, p1_urgent
    status = Column(String(50), default='new')
    assigned_to = Column(Integer, ForeignKey('users.id'))
    reported_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TestRun(Base):
    __tablename__ = 'test_runs'
    
    id = Column(Integer, primary_key=True)
    test_run_id = Column(String(50), unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='planned')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Create tables
Base.metadata.create_all(engine)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# In-memory session store for demo purposes
sessions = {}

def generate_session(user):
    token = uuid.uuid4().hex
    sessions[token] = {
        'user_id': user.id,
        'role': user.role,
        'username': user.username,
        'created_at': datetime.utcnow()
    }
    return token

def get_session(token):
    return sessions.get(token)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        token = auth.split(' ', 1)[1]
        sess = get_session(token)
        if not sess:
            return jsonify({'error': 'Invalid or expired session'}), 401
        g.current_user = sess
        return f(*args, **kwargs)
    return decorated

def require_role(allowed_roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, 'current_user', None)
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            if user.get('role') not in allowed_roles:
                return jsonify({'error': 'Forbidden - insufficient role'}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper

def init_sample_data():
    """Initialize database with sample data"""
    db = Session()
    
    # Check if data already exists
    if db.query(User).first():
        db.close()
        return
    
    # Create default users
    users = [
        User(
            username='admin',
            email='admin@testtrack.local',
            password_hash='hashed_password_here',
            full_name='Admin User',
            role='admin',
            status='active'
        ),
        User(
            username='tester',
            email='tester@testtrack.local',
            password_hash='hashed_password_here',
            full_name='Test Tester',
            role='tester',
            status='active'
        ),
        User(
            username='developer',
            email='developer@testtrack.local',
            password_hash='hashed_password_here',
            full_name='Dev Developer',
            role='developer',
            status='active'
        )
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    
    # Get user IDs
    admin = db.query(User).filter_by(username='admin').first()
    tester = db.query(User).filter_by(username='tester').first()
    
    # Create default project
    project = Project(
        name='TestTrack Pro',
        description='Main testing platform',
        key='TTP',
        status='active',
        created_by=admin.id
    )
    db.add(project)
    db.commit()
    
    # Create sample test cases
    testcases = [
        TestCase(
            test_case_id='TC-000001',
            project_id=project.id,
            title='Login with valid credentials',
            description='Verify user can login with valid email and password',
            module='Authentication',
            type='functional',
            priority='high',
            severity='critical',
            status='approved',
            created_by=tester.id
        ),
        TestCase(
            test_case_id='TC-000002',
            project_id=project.id,
            title='Create test case',
            description='Verify test cases can be created',
            module='Test Management',
            type='functional',
            priority='high',
            severity='major',
            status='approved',
            created_by=tester.id
        )
    ]
    
    for tc in testcases:
        db.add(tc)
    
    db.commit()
    
    # Create sample bugs
    bugs = [
        Bug(
            bug_id='BUG-000001',
            project_id=project.id,
            title='Login fails with valid credentials',
            description='System shows invalid credentials error',
            severity='blocker',
            priority='p1_urgent',
            status='open',
            assigned_to=None,
            reported_by=tester.id
        ),
        Bug(
            bug_id='BUG-000002',
            project_id=project.id,
            title='Reset password email not received',
            description='Email verification not sent to user email',
            severity='critical',
            priority='p2_high',
            status='new',
            assigned_to=None,
            reported_by=tester.id
        )
    ]
    
    for bug in bugs:
        db.add(bug)
    
    db.commit()
    db.close()

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path,
        'method': request.method,
        'message': f'No route found for {request.method} {request.path}',
        'available_endpoints': [
            '/api/auth/login',
            '/api/auth/register',
            '/api/projects',
            '/api/testcases',
            '/api/reports/summary',
            '/api/reports/by-module',
            '/health'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'path': request.path,
        'method': request.method,
        'message': f'Method {request.method} not allowed for {request.path}'
    }), 405

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        'name': 'TestTrack Pro API',
        'version': '1.0.0',
        'description': 'Enterprise-Grade Software Testing Platform',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth/*',
            'projects': '/api/projects',
            'testcases': '/api/testcases',
            'bugs': '/api/bugs',
            'reports': '/api/reports/*'
        },
        'frontend': 'http://localhost:8000',
        'docs': 'See API.md for documentation'
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        db = Session()
        db.execute('SELECT 1')
        db.close()
        return jsonify({
            'status': 'healthy',
            'message': 'TestTrack Pro is running',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'SQLite',
            'version': '1.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    db = Session()
    user = db.query(User).filter_by(email=email).first()
    db.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 401
    
    # For demo, accept any password — create a session token
    token = generate_session(user)
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'session_id': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role
        }
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register endpoint"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    full_name = data.get('full_name')
    
    if not all([email, password, username, full_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = Session()
    
    if db.query(User).filter_by(email=email).first():
        db.close()
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(
        username=username,
        email=email,
        password_hash='hashed_password',
        full_name=full_name,
        role='tester',
        status='active'
    )
    db.add(new_user)
    db.commit()
    user_id = new_user.id
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201

# ============================================================================
# PROJECTS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    db = Session()
    projects = db.query(Project).all()
    db.close()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'key': p.key,
            'status': p.status,
            'created_at': p.created_at.isoformat()
        } for p in projects]
    }), 200

@app.route('/api/projects', methods=['POST'])
@require_auth
@require_role(['developer', 'admin'])
def create_project():
    """Create new project"""
    data = request.get_json()
    
    db = Session()
    project = Project(
        name=data.get('name'),
        description=data.get('description'),
        key=data.get('key'),
        status='active',
        created_by=1
    )
    db.add(project)
    db.commit()
    project_id = project.id
    db.close()
    
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
    db = Session()
    testcases = db.query(TestCase).filter_by(project_id=project_id).all()
    db.close()
    
    return jsonify({
        'success': True,
        'count': len(testcases),
        'data': [{
            'id': tc.id,
            'test_case_id': tc.test_case_id,
            'title': tc.title,
            'description': tc.description,
            'module': tc.module,
            'type': tc.type,
            'priority': tc.priority,
            'severity': tc.severity,
            'status': tc.status,
            'created_at': tc.created_at.isoformat()
        } for tc in testcases]
    }), 200

@app.route('/api/projects/<int:project_id>/testcases', methods=['POST'])
def create_testcase(project_id):
    """Create test case"""
    data = request.get_json()
    
    db = Session()
    
    # Get next test case ID
    last_tc = db.query(TestCase).order_by(TestCase.id.desc()).first()
    next_id = (last_tc.id + 1) if last_tc else 1
    
    testcase = TestCase(
        test_case_id=f'TC-{next_id:06d}',
        project_id=project_id,
        title=data.get('title'),
        description=data.get('description'),
        module=data.get('module'),
        type=data.get('type', 'functional'),
        priority=data.get('priority', 'medium'),
        severity=data.get('severity', 'major'),
        status='draft',
        created_by=1
    )
    db.add(testcase)
    db.commit()
    tc_id = testcase.id
    test_case_id = testcase.test_case_id
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Test case created',
        'test_case_id': test_case_id,
        'id': tc_id
    }), 201

# ============================================================================
# GLOBAL TEST CASE ENDPOINTS
# ============================================================================

@app.route('/api/testcases', methods=['GET'])
def get_all_testcases():
    """Get all test cases across all projects"""
    db = Session()
    testcases = db.query(TestCase).all()
    db.close()
    
    return jsonify({
        'success': True,
        'count': len(testcases),
        'data': [{
            'id': tc.id,
            'test_case_id': tc.test_case_id,
            'title': tc.title,
            'description': tc.description,
            'module': tc.module,
            'type': tc.type,
            'priority': tc.priority,
            'severity': tc.severity,
            'status': tc.status,
            'created_at': tc.created_at.isoformat(),
            'created_by': tc.created_by,
            'assigned_to': tc.assigned_to
        } for tc in testcases]
    }), 200

@app.route('/api/testcases', methods=['POST'])
@require_auth
@require_role(['tester', 'developer', 'admin'])
def create_global_testcase():
    """Create a test case globally"""
    data = request.get_json()
    
    db = Session()
    created_by = g.current_user.get('user_id') if getattr(g, 'current_user', None) else 1

    # Generate next test_case_id (e.g., TC-000001)
    last_tc = db.query(TestCase).order_by(TestCase.id.desc()).first()
    next_id = (last_tc.id + 1) if last_tc else 1
    tc_id = f'TC-{next_id:06d}'

    testcase = TestCase(
        test_case_id=tc_id,
        project_id=data.get('project_id', 1),  # Default to project 1
        title=data.get('title'),
        description=data.get('description'),
        module=data.get('module'),
        type=data.get('type', 'functional'),
        priority=data.get('priority', 'medium'),
        severity=data.get('severity', 'medium'),
        status='draft',
        created_by=created_by
    )
    db.add(testcase)
    db.commit()
    tc_id = testcase.id
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Test case created',
        'test_case_id': tc_id,
        'id': tc_id
    }), 201

@app.route('/api/testcases/<int:tc_id>/execute', methods=['POST'])
@require_auth
@require_role(['tester', 'developer', 'admin'])
def execute_testcase(tc_id):
    """Execute a test case"""
    data = request.get_json()
    
    db = Session()
    tc = db.query(TestCase).filter_by(id=tc_id).first()
    
    if not tc:
        db.close()
        return jsonify({'error': 'Test case not found'}), 404
    
    execution = TestExecution(
        test_case_id=tc_id,
        executed_by=g.current_user.get('user_id') if getattr(g, 'current_user', None) else 1,
        result=data.get('result', 'PASS'),
        comments=data.get('comments', ''),
        executed_at=datetime.utcnow()
    )
    db.add(execution)
    tc.status = 'executed'
    db.commit()
    exec_id = execution.id
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Test case executed',
        'execution_id': exec_id
    }), 201
    """Get all executions for a test case"""
    db = Session()
    executions = db.query(TestExecution).filter_by(test_case_id=tc_id).all()
    db.close()
    
    return jsonify({
        'success': True,
        'count': len(executions),
        'data': [{
            'id': ex.id,
            'result': ex.result,
            'comments': ex.comments,
            'executed_at': ex.executed_at.isoformat() if ex.executed_at else None
        } for ex in executions]
    }), 200

@app.route('/api/testcases/<int:tc_id>', methods=['GET'])
def get_testcase(tc_id):
    """Get test case details"""
    db = Session()
    tc = db.query(TestCase).filter_by(id=tc_id).first()
    db.close()
    
    if not tc:
        return jsonify({'error': 'Test case not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': tc.id,
            'test_case_id': tc.test_case_id,
            'title': tc.title,
            'description': tc.description,
            'module': tc.module,
            'type': tc.type,
            'priority': tc.priority,
            'status': tc.status,
            'created_at': tc.created_at.isoformat(),
            'assigned_to': tc.assigned_to
        }
    }), 200

@app.route('/api/testcases/<int:tc_id>', methods=['PUT'])
def update_testcase(tc_id):
    """Update test case"""
    data = request.get_json()
    
    db = Session()
    tc = db.query(TestCase).filter_by(id=tc_id).first()
    
    if not tc:
        db.close()
        return jsonify({'error': 'Test case not found'}), 404
    
    if 'priority' in data:
        tc.priority = data['priority']
    if 'status' in data:
        tc.status = data['status']
    if 'title' in data:
        tc.title = data['title']
    
    db.commit()
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Test case updated'
    }), 200

@app.route('/api/testcases/<int:tc_id>', methods=['DELETE'])
def delete_testcase(tc_id):
    """Delete a test case"""
    db = Session()
    tc = db.query(TestCase).filter_by(id=tc_id).first()
    
    if not tc:
        db.close()
        return jsonify({'error': 'Test case not found'}), 404
    
    db.delete(tc)
    db.commit()
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Test case deleted'
    }), 200


@app.route('/api/testcases/<int:tc_id>/assign', methods=['PUT'])
@require_auth
@require_role(['developer', 'admin'])
def assign_testcase(tc_id):
    """Assign a test case to a user (tester)"""
    data = request.get_json() or {}
    assigned_to = data.get('assigned_to') or data.get('assigned_user_id')
    assigned_email = data.get('assigned_email')

    db = Session()
    tc = db.query(TestCase).filter_by(id=tc_id).first()
    if not tc:
        db.close()
        return jsonify({'error': 'Test case not found'}), 404

    # Resolve user by id or email
    user = None
    if assigned_to:
        user = db.query(User).filter_by(id=assigned_to).first()
    elif assigned_email:
        user = db.query(User).filter_by(email=assigned_email).first()

    if not user:
        db.close()
        return jsonify({'error': 'Assignee user not found'}), 404

    tc.assigned_to = user.id
    # update status when assigning (optional)
    tc.status = data.get('status', tc.status)
    db.commit()
    db.close()

    return jsonify({
        'success': True,
        'message': 'Test case assigned successfully',
        'test_case_id': tc.test_case_id,
        'assigned_to': user.id,
        'assigned_email': user.email
    }), 200

# ============================================================================
# BUGS
# ============================================================================

@app.route('/api/projects/<int:project_id>/bugs', methods=['GET'])
def get_bugs(project_id):
    """Get bugs for a project"""
    db = Session()
    bugs = db.query(Bug).filter_by(project_id=project_id).all()
    db.close()
    
    return jsonify({
        'success': True,
        'count': len(bugs),
        'data': [{
            'id': b.id,
            'bug_id': b.bug_id,
            'title': b.title,
            'description': b.description,
            'severity': b.severity,
            'priority': b.priority,
            'status': b.status,
            'assigned_to': b.assigned_to,
            'reported_by': b.reported_by,
            'created_at': b.created_at.isoformat()
        } for b in bugs]
    }), 200

@app.route('/api/projects/<int:project_id>/bugs', methods=['POST'])
@require_auth
@require_role(['tester', 'developer', 'admin'])
def create_bug(project_id):
    """Create bug report"""
    data = request.get_json()
    
    db = Session()
    
    # Get next bug ID
    last_bug = db.query(Bug).order_by(Bug.id.desc()).first()
    next_id = (last_bug.id + 1) if last_bug else 1
    
    bug = Bug(
        bug_id=f'BUG-{next_id:06d}',
        project_id=project_id,
        title=data.get('title'),
        description=data.get('description'),
        severity=data.get('severity', 'major'),
        priority=data.get('priority', 'p3_medium'),
        status='new',
        assigned_to=data.get('assigned_to'),
        reported_by=1
    )
    db.add(bug)
    db.commit()
    bug_id = bug.id
    bug_id_str = bug.bug_id
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Bug created',
        'bug_id': bug_id_str,
        'id': bug_id
    }), 201

@app.route('/api/bugs/<int:bug_id>/status', methods=['PUT'])
@require_auth
@require_role(['developer', 'admin'])
def update_bug_status(bug_id):
    """Update bug status"""
    data = request.get_json()
    
    db = Session()
    bug = db.query(Bug).filter_by(id=bug_id).first()
    
    if not bug:
        db.close()
        return jsonify({'error': 'Bug not found'}), 404
    
    bug.status = data.get('status', 'open')
    db.commit()
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Bug status updated'
    }), 200
@app.route('/api/bugs/<int:bug_id>/assign', methods=['PUT'])
@require_auth
@require_role(['developer', 'admin'])
def assign_bug(bug_id):
    """Assign bug to developer"""
    data = request.get_json()
    
    db = Session()
    bug = db.query(Bug).filter_by(id=bug_id).first()
    
    if not bug:
        db.close()
        return jsonify({'error': 'Bug not found'}), 404
    
    bug.assigned_to = data.get('assigned_to')
    db.commit()
    db.close()
    
    return jsonify({
        'success': True,
        'message': 'Bug assigned successfully'
    }), 200

# ============================================================================
# REPORTS
# ============================================================================

@app.route('/api/reports/summary', methods=['GET'])
def get_global_summary_report():
    """Get global test execution summary"""
    db = Session()
    testcases = db.query(TestCase).all()
    executions = db.query(TestExecution).all()
    bugs = db.query(Bug).all()
    db.close()
    
    total_testcases = len(testcases)
    passed = len([e for e in executions if e.result == 'PASS'])
    failed = len([e for e in executions if e.result == 'FAIL'])
    total_bugs = len(bugs)
    open_bugs = len([b for b in bugs if b.status in ['new', 'open']])
    
    pending = len([tc for tc in testcases if tc.status in ['pending', 'created', 'draft']])
    return jsonify({
        'success': True,
        'data': {
            'total_tests': total_testcases,
            'total_executions': len(executions),
            'passed': passed,
            'failed': failed,
            'pending': pending,
            'pass_rate': (passed / len(executions) * 100) if executions else 0,
            'total_bugs': total_bugs,
            'open_bugs': open_bugs,
            'closed_bugs': total_bugs - open_bugs
        }
    }), 200

@app.route('/api/reports/by-module', methods=['GET'])
def get_report_by_module():
    """Get report grouped by module"""
    db = Session()
    testcases = db.query(TestCase).all()
    db.close()
    
    modules = {}
    for tc in testcases:
        if tc.module not in modules:
            modules[tc.module] = {
                'module': tc.module,
                'total': 0,
                'status': {}
            }
        modules[tc.module]['total'] += 1
        if tc.status not in modules[tc.module]['status']:
            modules[tc.module]['status'][tc.status] = 0
        modules[tc.module]['status'][tc.status] += 1
    
    return jsonify({
        'success': True,
        'data': list(modules.values())
    }), 200

@app.route('/api/projects/<int:project_id>/reports/summary', methods=['GET'])
def get_summary_report(project_id):
    """Get test execution summary"""
    db = Session()
    testcases = db.query(TestCase).filter_by(project_id=project_id).all()
    bugs = db.query(Bug).filter_by(project_id=project_id).all()
    db.close()
    
    return jsonify({
        'success': True,
        'data': {
            'project_id': project_id,
            'tests': {
                'total': len(testcases),
                'by_status': {
                    'draft': len([tc for tc in testcases if tc.status == 'draft']),
                    'approved': len([tc for tc in testcases if tc.status == 'approved']),
                    'deprecated': len([tc for tc in testcases if tc.status == 'deprecated'])
                }
            },
            'bugs': {
                'total_bugs': len(bugs),
                'new': len([b for b in bugs if b.status == 'new']),
                'open': len([b for b in bugs if b.status == 'open']),
                'in_progress': len([b for b in bugs if b.status == 'in_progress']),
                'fixed': len([b for b in bugs if b.status == 'fixed']),
                'verified': len([b for b in bugs if b.status == 'verified']),
                'closed': len([b for b in bugs if b.status == 'closed'])
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
    # Initialize sample data
    init_sample_data()
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║           TestTrack Pro - SQLite Version                      ║
    ║                                                                ║
    ║  🚀 Starting TestTrack Pro with SQLite Database...            ║
    ║                                                                ║
    ║  📍 Backend URL: http://localhost:5000                        ║
    ║  📍 Database: testtrack.db (SQLite)                           ║
    ║  📍 Health Check: http://localhost:5000/health                ║
    ║                                                                ║
    ║  🔐 Default Login:                                            ║
    ║     Email: admin@testtrack.local                              ║
    ║     Password: any password (demo mode)                        ║
    ║                                                                ║
    ║  📊 Sample Data:                                              ║
    ║     ✓ 3 Users (Admin, Tester, Developer)                      ║
    ║     ✓ 1 Project (TestTrack Pro)                               ║
    ║     ✓ 2 Test Cases                                            ║
    ║     ✓ 2 Bugs                                                  ║
    ║                                                                ║
    ║  💾 Data persists between server restarts!                    ║
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
