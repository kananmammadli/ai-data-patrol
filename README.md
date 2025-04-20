# DataPatrol

DataPatrol is a web application for monitoring data quality across multiple databases and organizations. It provides automated checks, notifications, and a comprehensive dashboard for data quality management.

## Features

- Multi-organization and multi-project support
- Automated data quality checks with SQL-based rules
- Configurable severity levels and notification rules
- Role-based access control (Admin, Configurator, Viewer)
- Google OAuth / Okta authentication
- Comprehensive dashboard and reporting
- Email notifications for data quality issues

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- Python-Jose (JWT)
- Cryptography
- Passlib (Password Hashing)

### Frontend
- React
- TypeScript
- Material-UI
- React Query
- React Router

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Virtual environment (recommended)

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv ~/venvs/datapatrol
source ~/venvs/datapatrol/bin/activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Copy environment file and configure:
```bash
cp .env.example .env
# Edit .env with your configuration:
# - Set a secure ADMIN_PASSWORD
# - Configure database credentials
# - Set up OAuth credentials if using Google/Okta
# - Configure email settings
```

4. Initialize database:
```bash
# Make sure PostgreSQL is running
python init_db.py
```

5. Run the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Default Admin User

A default admin user is created during database initialization:

- Email: admin@datapatrol.io
- Password: Set in ADMIN_PASSWORD environment variable (defaults to "admin123" if not set)
- Role: ADMIN
- Authentication: Password-based

**Important**: Change the default admin password in production!

## Authentication

DataPatrol supports multiple authentication methods:

1. **Password Authentication**
   - Email/password login
   - Password hashing with bcrypt
   - JWT token-based sessions

2. **OAuth Authentication**
   - Google OAuth
   - Okta
   - JWT token-based sessions

## Development

- Backend API documentation available at `http://localhost:8000/docs`
- Frontend development server runs at `http://localhost:3000`

## Security Considerations

1. **Environment Variables**
   - Never commit .env file to version control
   - Use strong passwords and secrets
   - Rotate secrets regularly

2. **Database**
   - Use strong passwords for database users
   - Encrypt sensitive data
   - Regular backups

3. **Authentication**
   - Use HTTPS in production
   - Implement rate limiting
   - Monitor for suspicious activity

## License

MIT 