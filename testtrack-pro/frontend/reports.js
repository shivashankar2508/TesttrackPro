// Reports Handler

document.addEventListener('DOMContentLoaded', async () => {
    checkAuth();
    loadUserInfo();

    // Load reports
    await loadReports();
});

async function loadReports() {
    try {
        // Load summary report
        const summary = await api.getReportSummary();
        if (summary.success) {
            const data = summary.data;
            document.getElementById('summaryTotal').textContent = data.total_tests || 0;
            document.getElementById('summaryPassed').textContent = data.passed || 0;
            document.getElementById('summaryFailed').textContent = data.failed || 0;
            document.getElementById('summaryPending').textContent = data.pending || 0;
        }

        // Load module-wise report
        const moduleReport = await api.getReportByModule();
        if (moduleReport.success) {
            displayModuleReport(moduleReport.data || []);
        }
    } catch (error) {
        console.error('Failed to load reports:', error);
    }
}

function displayModuleReport(data) {
    const tbody = document.getElementById('moduleReport');

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No data available</td></tr>';
        return;
    }

    tbody.innerHTML = data.map(item => {
        const passRate = item.total > 0 ? ((item.passed / item.total) * 100).toFixed(1) : 0;
        return `
            <tr>
                <td>${item.module}</td>
                <td>${item.total || 0}</td>
                <td class="text-success">${item.passed || 0}</td>
                <td class="text-danger">${item.failed || 0}</td>
                <td>${passRate}%</td>
            </tr>
        `;
    }).join('');
}

// Export report functionality
document.addEventListener('DOMContentLoaded', () => {
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportReport);
    }
});

function exportReport() {
    // Get current report data
    const summaryData = {
        totalTests: document.getElementById('summaryTotal').textContent,
        passed: document.getElementById('summaryPassed').textContent,
        failed: document.getElementById('summaryFailed').textContent,
        pending: document.getElementById('summaryPending').textContent,
        timestamp: new Date().toLocaleString()
    };

    // Generate CSV
    const csv = generateCSV(summaryData);

    // Download CSV
    downloadFile(csv, 'testtrack-report.csv', 'text/csv');

    alert('Report exported successfully!');
}

function generateCSV(data) {
    return `TestTrack Pro - Test Report
Generated: ${data.timestamp}

Summary
Total Tests,${data.totalTests}
Passed,${data.passed}
Failed,${data.failed}
Pending,${data.pending}

Pass Rate,${((data.passed / data.totalTests) * 100).toFixed(1)}%
`;
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}
