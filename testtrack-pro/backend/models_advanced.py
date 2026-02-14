"""
Advanced Models for TestTrack Pro
Implements all data models for enterprise features
"""

from database import db
import hashlib
import json
from datetime import datetime, timedelta
import random
import string

# ==================== USER MODELS ====================

class User:
    """User model with enhanced auth"""
    
    @staticmethod
    def create(username, email, password, full_name, role='tester'):
        """Create new user"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = """
            INSERT INTO users (username, email, password, full_name, role, status, email_verified)
            VALUES (%s, %s, %s, %s, %s, 'active', FALSE)
        """
        result = db.execute_update(query, (username, email, hashed_password, full_name, role))
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
        """Authenticate user with login attempts tracking"""
        user = User.get_by_email(email)
        if not user:
            return None
        
        # Check if account is locked
        if user['status'] == 'locked' and user['locked_until']:
            if datetime.fromisoformat(str(user['locked_until'])) > datetime.now():
                return None
        
        # Verify password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user['password'] != hashed_password:
            # Increment failed login attempts
            User.increment_failed_login(user['id'])
            return None
        
        # Reset failed attempts and update last login
        query = "UPDATE users SET failed_login_attempts = 0, last_login_at = NOW(), locked_until = NULL WHERE id = %s"
        db.execute_update(query, (user['id'],))
        return user
    
    @staticmethod
    def increment_failed_login(user_id):
        """Track failed login attempts"""
        query = """
            UPDATE users 
            SET failed_login_attempts = failed_login_attempts + 1,
                locked_until = IF(failed_login_attempts >= 4, DATE_ADD(NOW(), INTERVAL 15 MINUTE), NULL),
                status = IF(failed_login_attempts >= 4, 'locked', status)
            WHERE id = %s
        """
        db.execute_update(query, (user_id,))
    
    @staticmethod
    def update_password(user_id, old_password, new_password):
        """Update password with history"""
        user = User.get_by_id(user_id)
        if not user:
            return False
        
        # Verify old password
        old_hash = hashlib.sha256(old_password.encode()).hexdigest()
        if user['password'] != old_hash:
            return False
        
        # Check password history
        query = "SELECT old_password FROM password_history WHERE user_id = %s ORDER BY changed_at DESC LIMIT 5"
        history = db.execute_query(query, (user_id,))
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        for record in history:
            if record['old_password'] == new_hash:
                return False  # Cannot reuse last 5 passwords
        
        # Save old password to history
        hist_query = "INSERT INTO password_history (user_id, old_password) VALUES (%s, %s)"
        db.execute_update(hist_query, (user_id, user['password']))
        
        # Update password
        update_query = "UPDATE users SET password = %s, password_changed_at = NOW() WHERE id = %s"
        return db.execute_update(update_query, (new_hash, user_id)) > 0
    
    @staticmethod
    def create_reset_token(user_id):
        """Create password reset token"""
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        expires = datetime.now() + timedelta(hours=1)
        query = "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)"
        db.execute_update(query, (user_id, token, expires))
        return token


# ==================== PROJECT MODELS ====================

class Project:
    """Project model"""
    
    @staticmethod
    def create(name, description, key, created_by):
        """Create new project"""
        query = """
            INSERT INTO projects (name, description, `key`, created_by, status)
            VALUES (%s, %s, %s, %s, 'active')
        """
        result = db.execute_update(query, (name, description, key, created_by))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def get_all(filters=None):
        """Get all projects"""
        query = "SELECT * FROM projects WHERE status = 'active'"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(project_id):
        """Get project by ID"""
        query = "SELECT * FROM projects WHERE id = %s"
        result = db.execute_query(query, (project_id,))
        return result[0] if result else None
    
    @staticmethod
    def add_member(project_id, user_id, role='member'):
        """Add member to project"""
        query = "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)"
        return db.execute_update(query, (project_id, user_id, role)) > 0


# ==================== TEST CASE MODELS ====================

class TestCase:
    """Test Case model with full featured management"""
    
    @staticmethod
    def create(project_id, title, description, module, type_enum, priority, severity, 
               preconditions, test_data, environment, postconditions, cleanup, 
               estimated_duration, created_by):
        """Create new test case"""
        # Generate test case ID
        last_id = db.execute_query("SELECT MAX(CAST(SUBSTRING(test_case_id, 4) AS UNSIGNED)) as max_id FROM test_cases")
        next_id = (last_id[0]['max_id'] if last_id and last_id[0]['max_id'] else 0) + 1
        test_case_id = f"TC-{next_id:06d}"
        
        query = """
            INSERT INTO test_cases 
            (test_case_id, project_id, title, description, module, type, priority, severity, 
             status, preconditions, test_data, environment_requirements, postconditions, 
             cleanup_steps, estimated_duration, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'draft', %s, %s, %s, %s, %s, %s, %s)
        """
        result = db.execute_update(query, 
            (test_case_id, project_id, title, description, module, type_enum, priority, severity,
             preconditions, test_data, environment, postconditions, cleanup, estimated_duration, created_by))
        
        if result:
            return {
                'id': db.get_last_insert_id(),
                'test_case_id': test_case_id
            }
        return None
    
    @staticmethod
    def add_step(test_case_id, step_number, action, test_data, expected_result, notes=None):
        """Add step to test case"""
        query = """
            INSERT INTO test_case_steps (test_case_id, step_number, action, test_data, expected_result, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_update(query, (test_case_id, step_number, action, test_data, expected_result, notes))
    
    @staticmethod
    def get_by_id(test_case_id):
        """Get test case with all details"""
        query = "SELECT * FROM test_cases WHERE id = %s"
        tc = db.execute_query(query, (test_case_id,))
        if not tc:
            return None
        
        tc = tc[0]
        # Get steps
        steps_query = "SELECT * FROM test_case_steps WHERE test_case_id = %s ORDER BY step_number"
        tc['steps'] = db.execute_query(steps_query, (test_case_id,))
        
        # Get tags
        tags_query = "SELECT tag_name FROM test_case_tags WHERE test_case_id = %s"
        tags = db.execute_query(tags_query, (test_case_id,))
        tc['tags'] = [t['tag_name'] for t in tags] if tags else []
        
        return tc
    
    @staticmethod
    def get_all(project_id, filters=None):
        """Get all test cases"""
        query = "SELECT * FROM test_cases WHERE project_id = %s AND is_deleted = FALSE"
        params = [project_id]
        
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
        return db.execute_query(query, params)
    
    @staticmethod
    def update(test_case_id, **kwargs):
        """Update test case with version tracking"""
        allowed_fields = ['title', 'description', 'module', 'type', 'priority', 'severity', 
                         'preconditions', 'test_data', 'environment_requirements', 'postconditions',
                         'cleanup_steps', 'estimated_duration', 'status', 'automation_status', 
                         'automation_script_link']
        
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            return 0
        
        params.append(test_case_id)
        query = f"UPDATE test_cases SET {', '.join(updates)}, version = version + 1, updated_at = NOW() WHERE id = %s"
        return db.execute_update(query, params)
    
    @staticmethod
    def clone(test_case_id, clone_attachments=False):
        """Clone test case"""
        original = TestCase.get_by_id(test_case_id)
        if not original:
            return None
        
        # Create new test case
        new_id = TestCase.create(
            original['project_id'],
            f"{original['title']} (Clone)",
            original['description'],
            original['module'],
            original['type'],
            original['priority'],
            original['severity'],
            original['preconditions'],
            original['test_data'],
            original['environment_requirements'],
            original['postconditions'],
            original['cleanup_steps'],
            original['estimated_duration'],
            original['created_by']
        )
        
        if new_id and original['steps']:
            for step in original['steps']:
                TestCase.add_step(new_id['id'], step['step_number'], step['action'],
                                step['test_data'], step['expected_result'], step['notes'])
        
        return new_id
    
    @staticmethod
    def soft_delete(test_case_id):
        """Soft delete test case"""
        query = "UPDATE test_cases SET is_deleted = TRUE, deleted_at = NOW() WHERE id = %s"
        return db.execute_update(query, (test_case_id,)) > 0


# ==================== TEST EXECUTION MODELS ====================

class TestRun:
    """Test Run model"""
    
    @staticmethod
    def create(project_id, name, description, milestone_id, planned_start, planned_end, created_by):
        """Create test run"""
        # Generate test run ID
        last = db.execute_query("SELECT MAX(CAST(SUBSTRING(test_run_id, 4) AS UNSIGNED)) as max_id FROM test_runs")
        next_id = (last[0]['max_id'] if last and last[0]['max_id'] else 0) + 1
        test_run_id = f"TR-{next_id:06d}"
        
        query = """
            INSERT INTO test_runs (test_run_id, project_id, name, description, milestone_id, 
                                 planned_start_date, planned_end_date, status, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'planned', %s)
        """
        result = db.execute_update(query, 
            (test_run_id, project_id, name, description, milestone_id, planned_start, planned_end, created_by))
        
        return {
            'id': db.get_last_insert_id(),
            'test_run_id': test_run_id
        } if result else None
    
    @staticmethod
    def assign_tester(test_run_id, user_id, assigned_by):
        """Assign tester to test run"""
        query = "INSERT INTO test_run_assignments (test_run_id, assigned_to, assigned_by) VALUES (%s, %s, %s)"
        return db.execute_update(query, (test_run_id, user_id, assigned_by)) > 0
    
    @staticmethod
    def get_by_id(test_run_id):
        """Get test run"""
        query = "SELECT * FROM test_runs WHERE id = %s"
        result = db.execute_query(query, (test_run_id,))
        return result[0] if result else None


class TestExecution:
    """Test Execution model"""
    
    @staticmethod
    def create(test_run_id, test_case_id, executed_by):
        """Create test execution"""
        query = """
            INSERT INTO test_executions (test_run_id, test_case_id, executed_by, overall_status, execution_start_time)
            VALUES (%s, %s, %s, 'not_executed', NOW())
        """
        result = db.execute_update(query, (test_run_id, test_case_id, executed_by))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def add_step_result(execution_id, step_number, actual_result, status, notes=None):
        """Add step execution result"""
        query = """
            INSERT INTO execution_steps (execution_id, step_number, actual_result, status, executed_at, notes)
            VALUES (%s, %s, %s, %s, NOW(), %s)
        """
        return db.execute_update(query, (execution_id, step_number, actual_result, status, notes))
    
    @staticmethod
    def upload_evidence(execution_id, step_id, file_name, file_type, file_size, file_url, evidence_type, uploaded_by):
        """Upload execution evidence"""
        query = """
            INSERT INTO execution_evidence 
            (execution_id, step_id, file_name, file_type, file_size, file_url, evidence_type, uploaded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return db.execute_update(query, 
            (execution_id, step_id, file_name, file_type, file_size, file_url, evidence_type, uploaded_by))
    
    @staticmethod
    def complete_execution(execution_id, status, duration_seconds):
        """Complete test execution"""
        query = """
            UPDATE test_executions 
            SET overall_status = %s, execution_end_time = NOW(), execution_duration_seconds = %s
            WHERE id = %s
        """
        return db.execute_update(query, (status, duration_seconds, execution_id)) > 0


# ==================== BUG MODELS ====================

class Bug:
    """Bug/Defect model"""
    
    @staticmethod
    def create(project_id, title, description, steps_to_reproduce, expected_behavior, 
               actual_behavior, severity, priority, environment, affected_version, reported_by):
        """Create bug report"""
        # Generate bug ID
        last = db.execute_query("SELECT MAX(CAST(SUBSTRING(bug_id, 5) AS UNSIGNED)) as max_id FROM bugs")
        next_id = (last[0]['max_id'] if last and last[0]['max_id'] else 0) + 1
        bug_id = f"BUG-{next_id:06d}"
        
        query = """
            INSERT INTO bugs (bug_id, project_id, title, description, steps_to_reproduce, 
                            expected_behavior, actual_behavior, severity, priority, environment, 
                            affected_version, status, reported_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'new', %s)
        """
        result = db.execute_update(query,
            (bug_id, project_id, title, description, steps_to_reproduce, expected_behavior,
             actual_behavior, severity, priority, environment, affected_version, reported_by))
        
        return {
            'id': db.get_last_insert_id(),
            'bug_id': bug_id
        } if result else None
    
    @staticmethod
    def get_by_id(bug_id):
        """Get bug details"""
        query = "SELECT * FROM bugs WHERE id = %s"
        bug = db.execute_query(query, (bug_id,))
        if not bug:
            return None
        
        bug = bug[0]
        # Get linked test cases
        tc_query = "SELECT test_case_id FROM bug_linked_tests WHERE bug_id = %s"
        linked = db.execute_query(tc_query, (bug_id,))
        bug['linked_test_cases'] = [t['test_case_id'] for t in linked] if linked else []
        
        # Get comments
        comm_query = "SELECT * FROM bug_comments WHERE bug_id = %s ORDER BY created_at DESC"
        bug['comments'] = db.execute_query(comm_query, (bug_id,))
        
        return bug
    
    @staticmethod
    def update_status(bug_id, new_status, changed_by, notes=None):
        """Update bug status with workflow history"""
        bug = Bug.get_by_id(bug_id)
        if not bug:
            return False
        
        # Record workflow transition
        hist_query = """
            INSERT INTO bug_workflow_history (bug_id, from_status, to_status, changed_by, change_notes)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_update(hist_query, (bug_id, bug['status'], new_status, changed_by, notes))
        
        # Update bug status
        update_query = "UPDATE bugs SET status = %s, updated_at = NOW() WHERE id = %s"
        return db.execute_update(update_query, (new_status, bug_id)) > 0
    
    @staticmethod
    def assign(bug_id, assigned_to):
        """Assign bug to developer"""
        query = "UPDATE bugs SET assigned_to = %s, updated_at = NOW() WHERE id = %s"
        return db.execute_update(query, (assigned_to, bug_id)) > 0
    
    @staticmethod
    def add_comment(bug_id, user_id, comment_text, is_internal=False):
        """Add comment to bug"""
        query = """
            INSERT INTO bug_comments (bug_id, user_id, comment_text, is_internal)
            VALUES (%s, %s, %s, %s)
        """
        return db.execute_update(query, (bug_id, user_id, comment_text, is_internal))
    
    @staticmethod
    def add_fix_details(bug_id, developer_id, fix_notes, commit_hash, branch_name):
        """Add fix details to bug"""
        query = """
            INSERT INTO bug_fixes (bug_id, developer_id, fix_notes, commit_hash, branch_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_update(query, (bug_id, developer_id, fix_notes, commit_hash, branch_name))
    
    @staticmethod
    def get_all(project_id, filters=None):
        """Get all bugs"""
        query = "SELECT * FROM bugs WHERE project_id = %s"
        params = [project_id]
        
        if filters:
            if 'status' in filters:
                query += " AND status = %s"
                params.append(filters['status'])
            if 'priority' in filters:
                query += " AND priority = %s"
                params.append(filters['priority'])
            if 'severity' in filters:
                query += " AND severity = %s"
                params.append(filters['severity'])
            if 'assigned_to' in filters:
                query += " AND assigned_to = %s"
                params.append(filters['assigned_to'])
        
        query += " ORDER BY created_at DESC"
        return db.execute_query(query, params)


# ==================== TEST SUITE MODELS ====================

class TestSuite:
    """Test Suite model"""
    
    @staticmethod
    def create(project_id, name, description, module, created_by):
        """Create test suite"""
        query = """
            INSERT INTO test_suites (project_id, name, description, module, created_by, status)
            VALUES (%s, %s, %s, %s, %s, 'active')
        """
        result = db.execute_update(query, (project_id, name, description, module, created_by))
        return db.get_last_insert_id() if result else None
    
    @staticmethod
    def add_test_case(suite_id, test_case_id, order_index):
        """Add test case to suite"""
        query = "INSERT INTO suite_test_cases (suite_id, test_case_id, order_index) VALUES (%s, %s, %s)"
        return db.execute_update(query, (suite_id, test_case_id, order_index)) > 0
    
    @staticmethod
    def get_test_cases(suite_id):
        """Get all test cases in suite"""
        query = """
            SELECT tc.* FROM test_cases tc
            JOIN suite_test_cases stc ON tc.id = stc.test_case_id
            WHERE stc.suite_id = %s
            ORDER BY stc.order_index
        """
        return db.execute_query(query, (suite_id,))


# ==================== NOTIFICATION MODELS ====================

class Notification:
    """Notification model"""
    
    @staticmethod
    def create(user_id, title, message, notification_type, entity_type=None, entity_id=None):
        """Create notification"""
        query = """
            INSERT INTO notifications (user_id, title, message, notification_type, related_entity_type, related_entity_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_update(query, (user_id, title, message, notification_type, entity_type, entity_id))
    
    @staticmethod
    def get_unread(user_id, limit=20):
        """Get unread notifications"""
        query = """
            SELECT * FROM notifications 
            WHERE user_id = %s AND is_read = FALSE
            ORDER BY created_at DESC
            LIMIT %s
        """
        return db.execute_query(query, (user_id, limit))
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        query = "UPDATE notifications SET is_read = TRUE, read_at = NOW() WHERE id = %s"
        return db.execute_update(query, (notification_id,)) > 0


# ==================== REPORTING MODELS ====================

class Report:
    """Reporting model"""
    
    @staticmethod
    def get_test_execution_summary(project_id, test_run_id=None):
        """Get test execution summary"""
        query = """
            SELECT 
                COUNT(*) as total_executed,
                SUM(CASE WHEN overall_status = 'passed' THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN overall_status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN overall_status = 'blocked' THEN 1 ELSE 0 END) as blocked,
                SUM(CASE WHEN overall_status = 'skipped' THEN 1 ELSE 0 END) as skipped
            FROM test_executions te
            WHERE te.test_case_id IN (
                SELECT id FROM test_cases WHERE project_id = %s
            )
        """
        params = [project_id]
        
        if test_run_id:
            query += " AND te.test_run_id = %s"
            params.append(test_run_id)
        
        result = db.execute_query(query, params)
        return result[0] if result else {}
    
    @staticmethod
    def get_bug_summary(project_id):
        """Get bug summary"""
        query = """
            SELECT 
                COUNT(*) as total_bugs,
                SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new_bugs,
                SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open_bugs,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'fixed' THEN 1 ELSE 0 END) as fixed,
                SUM(CASE WHEN status = 'verified' THEN 1 ELSE 0 END) as verified
            FROM bugs WHERE project_id = %s
        """
        result = db.execute_query(query, (project_id,))
        return result[0] if result else {}
    
    @staticmethod
    def get_bugs_by_developer(project_id):
        """Get bugs assigned by developer"""
        query = """
            SELECT 
                u.username,
                COUNT(*) as assigned_count,
                SUM(CASE WHEN b.status = 'fixed' THEN 1 ELSE 0 END) as resolved,
                SUM(CASE WHEN b.status = 'verified' THEN 1 ELSE 0 END) as verified
            FROM bugs b
            LEFT JOIN users u ON b.assigned_to = u.id
            WHERE b.project_id = %s
            GROUP BY b.assigned_to, u.username
        """
        return db.execute_query(query, (project_id,))
