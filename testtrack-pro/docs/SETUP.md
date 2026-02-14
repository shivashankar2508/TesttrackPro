# TestTrack Pro - Installation & Setup Guide

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Frontend Requirements
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Basic knowledge of HTML/CSS/JavaScript

## Step-by-Step Installation

### 1. Database Setup

1. **Create MySQL Database**
   ```bash
   # Open MySQL command line
   mysql -u root -p
   
   # Run the schema script
   source database/schema.sql
   ```

   Or if you have a password:
   ```bash
   mysql -u root -p<password> < database/schema.sql
   ```

2. **Verify Database Creation**
   ```bash
   mysql -u root -p
   SHOW DATABASES;
   USE testtrack_pro;
   SHOW TABLES;
   ```

### 2. Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**
   ```bash
   # Create venv
   python -m venv venv
   
   # Activate venv (Windows)
   venv\Scripts\activate
   
   # Activate venv (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env file with your MySQL credentials
   # MYSQL_HOST=localhost
   # MYSQL_USER=root
   # MYSQL_PASSWORD=your_password
   # MYSQL_DB=testtrack_pro
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```

   Expected output:
   ```
   ✓ Database connected successfully
   Starting TestTrack Pro API server...
   Running on http://0.0.0.0:5000
   ```

### 3. Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Start a local server**
   
   **Option 1: Using Python**
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   ```

   **Option 2: Using Node.js (if installed)**
   ```bash
   npx http-server
   ```

   **Option 3: Direct file access**
   - Open `login.html` in your browser

3. **Access the application**
   - Open your browser
   - Navigate to `http://localhost:8000` or `http://localhost:3000`
   - You should see the TestTrack Pro login page

## Default Login Credentials

### Admin Account
- Email: `admin@testtrack.com`
- Password: `admin123`
- Role: Admin

### Sample Tester Account
- Email: `tester1@testtrack.com`
- Password: `tester123`
- Role: Tester

### Sample Developer Account
- Email: `developer1@testtrack.com`
- Password: `dev123`
- Role: Developer

## Project Structure

```
testtrack-pro/
├── frontend/                 # Web UI
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Main dashboard
│   ├── testcases.html       # Test case management
│   ├── reports.html         # Test reports
│   ├── styles.css           # Global styles
│   ├── api.js               # API client
│   ├── auth.js              # Authentication
│   ├── dashboard.js         # Dashboard logic
│   ├── testcases.js         # Test case logic
│   └── reports.js           # Reports logic
│
├── backend/                  # Python API Server
│   ├── app.py               # Flask application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models.py            # Data models
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
│
├── database/                 # Database scripts
│   ├── schema.sql           # Initial schema
│   └── migrations.sql       # Migrations
│
└── docs/                     # Documentation
```

## Testing the Application

### 1. Login
- Go to `http://localhost:8000/login.html`
- Use any of the demo credentials above
- You should be redirected to the dashboard

### 2. Create Test Case
- Navigate to "Test Cases" page
- Click "Create Test Case"
- Fill in the form with:
  - Title: "Sample Test"
  - Description: "This is a sample test"
  - Module: "Authentication"
  - Steps: "1. Step one\n2. Step two"
  - Expected Result: "Test passes"
  - Priority: "High"
- Click "Save Test Case"

### 3. View Reports
- Navigate to "Reports" page
- View the summary and module-wise reports
- Click "Export Report" to download CSV

## Troubleshooting

### MySQL Connection Error
```
Error: Failed to connect to database
```
**Solution:**
- Check MySQL service is running
- Verify credentials in `.env` file
- Ensure database `testtrack_pro` exists
- Check MySQL port (default: 3306)

### Python Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

### CORS Error in Browser
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:**
- Backend should have CORS enabled (already configured)
- Check backend is running on port 5000
- Clear browser cache and restart

### Port Already in Use
```
Address already in use
```
**Solution:**
- Change the port in `app.py` (line: `app.run(port=5000)`)
- Or kill the process using the port

## API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/testcases` - Get test cases
- `POST /api/testcases` - Create test case
- `PUT /api/testcases/<id>` - Update test case
- `DELETE /api/testcases/<id>` - Delete test case
- `POST /api/testcases/<id>/execute` - Execute test case
- `GET /api/reports/summary` - Get summary report
- `GET /api/reports/by-module` - Get module report

## Next Steps

1. **Customize the application**: Modify colors, logos, and branding
2. **Add more features**: User management, advanced filters, etc.
3. **Deploy**: Use Docker for containerization and cloud deployment
4. **CI/CD**: Setup GitHub Actions or similar for automated testing

## Support

For issues or questions:
- Check the documentation
- Review error logs
- Check MySQL error logs
- Enable debug mode in `app.py` (already enabled in development)

## License

MIT License - See LICENSE file
