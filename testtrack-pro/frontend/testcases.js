// Test Cases Handler

let allTestCases = [];

document.addEventListener('DOMContentLoaded', async () => {
    checkAuth();
    loadUserInfo();

    // Load test cases
    await loadTestCases();

    // Setup event listeners
    setupEventListeners();
});

async function loadTestCases(filters = {}) {
    try {
        const response = await api.getTestCases(filters);
        if (response.success) {
            allTestCases = response.data || [];
            displayTestCases(allTestCases);
        }
    } catch (error) {
        console.error('Failed to load test cases:', error);
    }
}

function displayTestCases(testcases) {
    const tbody = document.getElementById('testcasesTable');

    if (!testcases || testcases.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No test cases found</td></tr>';
        return;
    }

    tbody.innerHTML = testcases.map(tc => `
        <tr>
            <td>${tc.title}</td>
            <td>${tc.module}</td>
            <td><span class="badge badge-${tc.priority}">${tc.priority}</span></td>
            <td><span class="badge badge-${getStatusClass(tc.status)}">${tc.status}</span></td>
            <td>${new Date(tc.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-small" onclick="editTestCase(${tc.id})">Edit</button>
                <button class="btn btn-small" onclick="deleteTestCase(${tc.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function setupEventListeners() {
    // Create test case button
    const createBtn = document.getElementById('createCaseBtn');
    if (createBtn) {
        createBtn.addEventListener('click', openCreateModal);
    }

    // Apply filters
    const applyFiltersBtn = document.getElementById('applyFilters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }

    // Test case form
    const form = document.getElementById('testcaseForm');
    if (form) {
        form.addEventListener('submit', saveTestCase);
    }

    // Modal close button
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('testcaseModal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

function openCreateModal() {
    document.getElementById('testcaseId').value = '';
    document.getElementById('testcaseForm').reset();
    document.querySelector('#testcaseModal h2').textContent = 'Create Test Case';
    document.getElementById('testcaseModal').classList.add('show');
}

function closeModal() {
    document.getElementById('testcaseModal').classList.remove('show');
}

async function editTestCase(id) {
    try {
        const response = await api.getTestCase(id);
        if (response.success) {
            const tc = response.data;
            document.getElementById('testcaseId').value = tc.id;
            document.getElementById('title').value = tc.title;
            document.getElementById('description').value = tc.description;
            document.getElementById('module').value = tc.module;
            document.getElementById('steps').value = tc.steps;
            document.getElementById('expectedResult').value = tc.expected_result;
            document.getElementById('priority').value = tc.priority;

            document.querySelector('#testcaseModal h2').textContent = 'Edit Test Case';
            document.getElementById('testcaseModal').classList.add('show');
        }
    } catch (error) {
        alert('Failed to load test case');
    }
}

async function deleteTestCase(id) {
    if (!confirm('Are you sure you want to delete this test case?')) {
        return;
    }

    try {
        const response = await api.deleteTestCase(id);
        if (response.success) {
            alert('Test case deleted successfully');
            await loadTestCases();
        }
    } catch (error) {
        alert('Failed to delete test case');
    }
}

async function saveTestCase(e) {
    e.preventDefault();

    const id = document.getElementById('testcaseId').value;
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        module: document.getElementById('module').value,
        steps: document.getElementById('steps').value,
        expected_result: document.getElementById('expectedResult').value,
        priority: document.getElementById('priority').value,
        created_by: JSON.parse(localStorage.getItem('user')).id
    };

    try {
        let response;
        if (id) {
            response = await api.updateTestCase(id, data);
        } else {
            response = await api.createTestCase(data);
        }

        if (response.success) {
            alert(response.message);
            closeModal();
            await loadTestCases();
        }
    } catch (error) {
        alert('Failed to save test case: ' + error.message);
    }
}

function applyFilters() {
    const filters = {
        status: document.getElementById('statusFilter').value,
        priority: document.getElementById('priorityFilter').value
    };

    // Remove empty filters
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });

    loadTestCases(filters);
}

function getStatusClass(status) {
    const classes = {
        'created': 'secondary',
        'pending': 'info',
        'passed': 'success',
        'failed': 'danger',
        'blocked': 'warning'
    };
    return classes[status] || 'secondary';
}

// Add CSS for modal if not in main CSS
const style = document.createElement('style');
style.textContent = `
.badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    color: white;
}

.badge-low { background-color: #28a745; }
.badge-medium { background-color: #ffc107; color: #333; }
.badge-high { background-color: #dc3545; }
.badge-critical { background-color: #721c24; }

.badge-secondary { background-color: #6c757d; }
.badge-info { background-color: #17a2b8; }
.badge-success { background-color: #28a745; }
.badge-danger { background-color: #dc3545; }
.badge-warning { background-color: #ffc107; color: #333; }
`;
document.head.appendChild(style);
