from database import db
import hashlib
import json

class User:
    """User model"""
    
    @staticmethod
    def create(username, email, password, role='tester'):
        """Create new user"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = """
            INSERT INTO users (username, email, password, role, status)
            VALUES (%s, %s, %s, %s, 'active')
        """
        result = db.execute_update(query, (username, email, hashed_password, role))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = db.execute_query(query, (user_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = db.execute_query(query, (email,))
        return result[0] if result else None
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user"""
        user = User.get_by_email(email)
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user['password'] == hashed_password:
                return user
        return None

class TestCase:
    """Test Case model"""
    
    @staticmethod
    def create(title, description, module, steps, expected_result, created_by, priority='medium'):
        """Create new test case"""
        query = """
            INSERT INTO test_cases 
            (title, description, module, steps, expected_result, created_by, priority, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'created', NOW())
        """
        result = db.execute_update(query, (title, description, module, steps, expected_result, created_by, priority))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def get_all(filters=None):
        """Get all test cases with optional filters"""
        query = "SELECT * FROM test_cases WHERE 1=1"
        params = []
        
        if filters:
            if 'status' in filters:
                query += " AND status = %s"
                params.append(filters['status'])
            if 'module' in filters:
                query += " AND module = %s"
                params.append(filters['module'])
            if 'priority' in filters:
                query += " AND priority = %s"
                params.append(filters['priority'])
        
        query += " ORDER BY created_at DESC"
        return db.execute_query(query, params) if params else db.execute_query(query)
    
    @staticmethod
    def get_by_id(test_case_id):
        """Get test case by ID"""
        query = "SELECT * FROM test_cases WHERE id = %s"
        result = db.execute_query(query, (test_case_id,))
        return result[0] if result else None
    
    @staticmethod
    def update(test_case_id, **kwargs):
        """Update test case"""
        allowed_fields = ['title', 'description', 'module', 'steps', 'expected_result', 'priority', 'status']
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return 0
        
        params.append(test_case_id)
        query = f"UPDATE test_cases SET {', '.join(updates)}, updated_at = NOW() WHERE id = %s"
        return db.execute_update(query, params)
    
    @staticmethod
    def delete(test_case_id):
        """Delete test case"""
        query = "DELETE FROM test_cases WHERE id = %s"
        return db.execute_update(query, (test_case_id,))

class TestExecution:
    """Test Execution model"""
    
    @staticmethod
    def create(test_case_id, executed_by, status, notes=None):
        """Create test execution record"""
        query = """
            INSERT INTO test_executions 
            (test_case_id, executed_by, status, notes, executed_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        result = db.execute_update(query, (test_case_id, executed_by, status, notes))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def get_by_test_case(test_case_id):
        """Get execution history for a test case"""
        query = """
            SELECT e.*, u.username as executed_by_name 
            FROM test_executions e
            JOIN users u ON e.executed_by = u.id
            WHERE e.test_case_id = %s
            ORDER BY e.executed_at DESC
        """
        return db.execute_query(query, (test_case_id,))

class TestReport:
    """Test Report model"""
    
    @staticmethod
    def get_summary():
        """Get test summary report"""
        query = """
            SELECT 
                COUNT(*) as total_tests,
                SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'created' THEN 1 ELSE 0 END) as not_executed
            FROM test_executions
        """
        result = db.execute_query(query)
        return result[0] if result else {}
    
    @staticmethod
    def get_by_module():
        """Get test report by module"""
        query = """
            SELECT 
                tc.module,
                COUNT(tc.id) as total,
                SUM(CASE WHEN te.status = 'passed' THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN te.status = 'failed' THEN 1 ELSE 0 END) as failed
            FROM test_cases tc
            LEFT JOIN test_executions te ON tc.id = te.test_case_id
            GROUP BY tc.module
        """
        return db.execute_query(query)
