-- TestTrack Pro Database Schema - Enterprise Edition
-- MySQL 5.7+

-- Create Database
CREATE DATABASE IF NOT EXISTS testtrack_pro;
USE testtrack_pro;

-- ==================== USERS & AUTHENTICATION ====================

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    role ENUM('tester', 'developer', 'admin') NOT NULL DEFAULT 'tester',
    status ENUM('active', 'inactive', 'locked') NOT NULL DEFAULT 'active',
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP NULL,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login_at TIMESTAMP NULL,
    password_changed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Password Reset Tokens
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Password History
CREATE TABLE IF NOT EXISTS password_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    old_password VARCHAR(255) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== PROJECTS ====================

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    key VARCHAR(20) NOT NULL UNIQUE,
    created_by INT NOT NULL,
    status ENUM('active', 'inactive', 'archived') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_status (status),
    INDEX idx_key (key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Project Members
CREATE TABLE IF NOT EXISTS project_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('member', 'lead', 'admin') NOT NULL DEFAULT 'member',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_user (project_id, user_id),
    INDEX idx_project_id (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Milestones
CREATE TABLE IF NOT EXISTS milestones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    target_date DATE,
    status ENUM('planned', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TEST CASES ====================

-- Test Cases Table
CREATE TABLE IF NOT EXISTS test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_id VARCHAR(50) NOT NULL UNIQUE,
    project_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description LONGTEXT,
    module VARCHAR(100) NOT NULL,
    type ENUM('functional', 'regression', 'smoke', 'integration', 'uat', 'performance', 'security', 'usability') DEFAULT 'functional',
    priority ENUM('low', 'medium', 'high', 'critical') NOT NULL DEFAULT 'medium',
    severity ENUM('trivial', 'minor', 'major', 'critical', 'blocker') DEFAULT 'major',
    status ENUM('draft', 'ready_for_review', 'approved', 'deprecated', 'archived') NOT NULL DEFAULT 'draft',
    preconditions LONGTEXT,
    test_data LONGTEXT,
    environment_requirements LONGTEXT,
    postconditions LONGTEXT,
    cleanup_steps LONGTEXT,
    estimated_duration INT,
    automation_status ENUM('not_automated', 'in_progress', 'automated', 'cannot_automate') DEFAULT 'not_automated',
    automation_script_link VARCHAR(500),
    created_by INT NOT NULL,
    version INT DEFAULT 1,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_test_case_id (test_case_id),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status),
    INDEX idx_module (module),
    INDEX idx_priority (priority),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Case Steps
CREATE TABLE IF NOT EXISTS test_case_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_id INT NOT NULL,
    step_number INT NOT NULL,
    action LONGTEXT NOT NULL,
    test_data LONGTEXT,
    expected_result LONGTEXT NOT NULL,
    notes LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    INDEX idx_test_case_id (test_case_id),
    UNIQUE KEY unique_step (test_case_id, step_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Case Tags
CREATE TABLE IF NOT EXISTS test_case_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_id INT NOT NULL,
    tag_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    INDEX idx_test_case_id (test_case_id),
    INDEX idx_tag_name (tag_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Case Versions
CREATE TABLE IF NOT EXISTS test_case_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_id INT NOT NULL,
    version INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description LONGTEXT,
    change_summary VARCHAR(500),
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id),
    INDEX idx_test_case_id (test_case_id),
    UNIQUE KEY unique_version (test_case_id, version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Case Templates
CREATE TABLE IF NOT EXISTS test_case_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    category VARCHAR(100),
    template_content LONGTEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TEST SUITES ====================

-- Test Suites
CREATE TABLE IF NOT EXISTS test_suites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    module VARCHAR(100),
    parent_suite_id INT,
    created_by INT NOT NULL,
    status ENUM('active', 'archived') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_suite_id) REFERENCES test_suites(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Suite Test Cases (Junction Table)
CREATE TABLE IF NOT EXISTS suite_test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    suite_id INT NOT NULL,
    test_case_id INT NOT NULL,
    order_index INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (suite_id) REFERENCES test_suites(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    UNIQUE KEY unique_suite_test (suite_id, test_case_id),
    INDEX idx_suite_id (suite_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== TEST EXECUTION ====================

-- Test Runs
CREATE TABLE IF NOT EXISTS test_runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_run_id VARCHAR(50) NOT NULL UNIQUE,
    project_id INT NOT NULL,
    milestone_id INT,
    name VARCHAR(255) NOT NULL,
    description LONGTEXT,
    status ENUM('planned', 'in_progress', 'completed', 'paused', 'cancelled') NOT NULL DEFAULT 'planned',
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATETIME,
    actual_end_date DATETIME,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (milestone_id) REFERENCES milestones(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Run Assignments
CREATE TABLE IF NOT EXISTS test_run_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_run_id INT NOT NULL,
    assigned_to INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_run_id) REFERENCES test_runs(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    INDEX idx_test_run_id (test_run_id),
    INDEX idx_assigned_to (assigned_to)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Executions
CREATE TABLE IF NOT EXISTS test_executions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_run_id INT,
    test_case_id INT NOT NULL,
    execution_number INT DEFAULT 1,
    executed_by INT NOT NULL,
    overall_status ENUM('not_executed', 'passed', 'failed', 'blocked', 'skipped') NOT NULL DEFAULT 'not_executed',
    execution_start_time DATETIME,
    execution_end_time DATETIME,
    execution_duration_seconds INT,
    notes LONGTEXT,
    is_automated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (test_run_id) REFERENCES test_runs(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (executed_by) REFERENCES users(id),
    INDEX idx_test_case_id (test_case_id),
    INDEX idx_test_run_id (test_run_id),
    INDEX idx_overall_status (overall_status),
    INDEX idx_executed_by (executed_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Test Execution Steps
CREATE TABLE IF NOT EXISTS execution_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    execution_id INT NOT NULL,
    step_number INT NOT NULL,
    step_name VARCHAR(255),
    expected_result LONGTEXT,
    actual_result LONGTEXT,
    status ENUM('not_executed', 'passed', 'failed', 'blocked', 'skipped') NOT NULL DEFAULT 'not_executed',
    notes LONGTEXT,
    executed_at TIMESTAMP NULL,
    FOREIGN KEY (execution_id) REFERENCES test_executions(id) ON DELETE CASCADE,
    INDEX idx_execution_id (execution_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Execution Evidence (Attachments)
CREATE TABLE IF NOT EXISTS execution_evidence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    execution_id INT NOT NULL,
    step_id INT,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size INT,
    file_path VARCHAR(500),
    file_url VARCHAR(500),
    evidence_type ENUM('screenshot', 'video', 'log', 'document', 'trace') DEFAULT 'screenshot',
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES test_executions(id) ON DELETE CASCADE,
    FOREIGN KEY (step_id) REFERENCES execution_steps(id) ON DELETE SET NULL,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_execution_id (execution_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== BUG/DEFECT MANAGEMENT ====================

-- Bugs/Defects
CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id VARCHAR(50) NOT NULL UNIQUE,
    project_id INT NOT NULL,
    test_execution_id INT,
    title VARCHAR(255) NOT NULL,
    description LONGTEXT NOT NULL,
    steps_to_reproduce LONGTEXT,
    expected_behavior LONGTEXT,
    actual_behavior LONGTEXT,
    severity ENUM('trivial', 'minor', 'major', 'critical', 'blocker') NOT NULL DEFAULT 'major',
    priority ENUM('p4_low', 'p3_medium', 'p2_high', 'p1_urgent') NOT NULL DEFAULT 'p3_medium',
    status ENUM('new', 'open', 'in_progress', 'fixed', 'verified', 'closed', 'reopened', 'wont_fix', 'duplicate') NOT NULL DEFAULT 'new',
    environment VARCHAR(255),
    affected_version VARCHAR(50),
    assigned_to INT,
    reported_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (test_execution_id) REFERENCES test_executions(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (reported_by) REFERENCES users(id),
    INDEX idx_bug_id (bug_id),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_assigned_to (assigned_to)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bug Linked Test Cases
CREATE TABLE IF NOT EXISTS bug_linked_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT NOT NULL,
    test_case_id INT NOT NULL,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE CASCADE,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    INDEX idx_bug_id (bug_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bug Attachments
CREATE TABLE IF NOT EXISTS bug_attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_path VARCHAR(500),
    file_url VARCHAR(500),
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_bug_id (bug_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bug Workflow History
CREATE TABLE IF NOT EXISTS bug_workflow_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT NOT NULL,
    from_status VARCHAR(50),
    to_status VARCHAR(50) NOT NULL,
    changed_by INT NOT NULL,
    change_notes LONGTEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id),
    INDEX idx_bug_id (bug_id),
    INDEX idx_changed_at (changed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bug Comments
CREATE TABLE IF NOT EXISTS bug_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text LONGTEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_bug_id (bug_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bug Fix Details
CREATE TABLE IF NOT EXISTS bug_fixes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT NOT NULL,
    fix_notes LONGTEXT,
    developer_id INT NOT NULL,
    commit_hash VARCHAR(100),
    commit_url VARCHAR(500),
    branch_name VARCHAR(255),
    fixed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE CASCADE,
    FOREIGN KEY (developer_id) REFERENCES users(id),
    INDEX idx_bug_id (bug_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== NOTIFICATIONS ====================

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message LONGTEXT,
    notification_type ENUM('bug_assigned', 'bug_status_changed', 'test_assigned', 'comment_added', 'retest_requested', 'test_result', 'mention') DEFAULT 'test_result',
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(50),
    related_entity_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Notification Preferences
CREATE TABLE IF NOT EXISTS notification_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    email_enabled BOOLEAN DEFAULT TRUE,
    in_app_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_type (user_id, notification_type),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== COMMENTS & COLLABORATION ====================

-- Test Case Comments
CREATE TABLE IF NOT EXISTS test_case_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text LONGTEXT NOT NULL,
    parent_comment_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES test_case_comments(id) ON DELETE CASCADE,
    INDEX idx_test_case_id (test_case_id),
    INDEX idx_parent_comment_id (parent_comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== AUDIT & LOGGING ====================

-- Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_entity_type (entity_type),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== INTEGRATIONS ====================

-- Git Commits
CREATE TABLE IF NOT EXISTS git_commits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT,
    project_id INT NOT NULL,
    commit_hash VARCHAR(100) NOT NULL,
    commit_message LONGTEXT,
    author_name VARCHAR(100),
    author_email VARCHAR(100),
    branch_name VARCHAR(255),
    commit_url VARCHAR(500),
    committed_at TIMESTAMP NULL,
    linked_by INT,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_by) REFERENCES users(id),
    UNIQUE KEY unique_commit (project_id, commit_hash),
    INDEX idx_bug_id (bug_id),
    INDEX idx_project_id (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Webhooks
CREATE TABLE IF NOT EXISTS webhooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    webhook_url VARCHAR(500) NOT NULL,
    secret_key VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_event_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Webhook Logs
CREATE TABLE IF NOT EXISTS webhook_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    webhook_id INT NOT NULL,
    event_data JSON,
    http_status INT,
    response_body LONGTEXT,
    retry_count INT DEFAULT 0,
    last_retry_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (webhook_id) REFERENCES webhooks(id) ON DELETE CASCADE,
    INDEX idx_webhook_id (webhook_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- API Keys
CREATE TABLE IF NOT EXISTS api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    last_used_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_key_hash (key_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==================== INSERT DEFAULT DATA ====================

-- Create Default Admin User (password: admin123)
INSERT INTO users (username, email, password, full_name, role, status, email_verified) VALUES
('admin', 'admin@testtrack.com', '240be518fabd2724ddb6f04eeb1da5967448d7e1d33f33371597da0a2a5596f2', 'Admin User', 'admin', 'active', TRUE)
ON DUPLICATE KEY UPDATE id=id;

-- Create Sample Tester User (password: tester123)
INSERT INTO users (username, email, password, full_name, role, status, email_verified) VALUES
('tester1', 'tester1@testtrack.com', '2e7d32cfe8202c3847291e0f992d748418b64974427b9a83e60fcf451d7ecec1', 'Jane Tester', 'tester', 'active', TRUE)
ON DUPLICATE KEY UPDATE id=id;

-- Create Sample Developer User (password: dev123)
INSERT INTO users (username, email, password, full_name, role, status, email_verified) VALUES
('developer1', 'developer1@testtrack.com', '9b871830fbf75705cf57f1b2fb761183e57e0b0e9cbecf92b5f8e4b4e1f1f2f3', 'Mike Developer', 'developer', 'active', TRUE)
ON DUPLICATE KEY UPDATE id=id;

-- Create Default Project
INSERT INTO projects (name, description, `key`, created_by, status) VALUES
('TestTrack Pro', 'Main testing platform for QA and development', 'TTP', 1, 'active')
ON DUPLICATE KEY UPDATE id=id;
