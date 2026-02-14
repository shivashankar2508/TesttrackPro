// Dashboard Handler

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    checkAuth();
    loadUserInfo();

    // Load dashboard data
    await loadDashboardData();
});

async function loadDashboardData() {
    try {
        // Load summary report
        const summary = await api.getReportSummary();
        if (summary.success) {
            const data = summary.data;
            document.getElementById('totalTests').textContent = data.total_tests || 0;
            document.getElementById('passedTests').textContent = data.passed || 0;
            document.getElementById('failedTests').textContent = data.failed || 0;
            document.getElementById('pendingTests').textContent = data.pending || 0;
        }

        // Load recent test cases
        const testcases = await api.getTestCases();
        if (testcases.success) {
            displayRecentTestCases(testcases.data.slice(0, 5));
        }
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

function displayRecentTestCases(testcases) {
    const tbody = document.getElementById('recentTestcases');

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
                <a href="#" class="btn btn-small">View</a>
            </td>
        </tr>
    `).join('');
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

// Add CSS for badges if not in main CSS
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
