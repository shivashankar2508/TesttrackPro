// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Client
class APIClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const sessionId = localStorage.getItem('sessionId');

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (sessionId) {
            headers['Authorization'] = `Bearer ${sessionId}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    async register(username, email, password, role) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, role })
        });
    }

    // Test Cases
    async getTestCases(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/testcases?${params}`);
    }

    async createTestCase(data) {
        return this.request('/testcases', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getTestCase(id) {
        return this.request(`/testcases/${id}`);
    }

    async updateTestCase(id, data) {
        return this.request(`/testcases/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteTestCase(id) {
        return this.request(`/testcases/${id}`, {
            method: 'DELETE'
        });
    }

    async executeTestCase(id, data) {
        return this.request(`/testcases/${id}/execute`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getTestCaseExecutions(id) {
        return this.request(`/testcases/${id}/executions`);
    }

    // Reports
    async getReportSummary() {
        return this.request('/reports/summary');
    }

    async getReportByModule() {
        return this.request('/reports/by-module');
    }

    // Health Check
    async healthCheck() {
        return this.request('/health');
    }
}

// Create API client instance
const api = new APIClient(API_BASE_URL);
