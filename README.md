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
# Edit .env with your configuration
```

4. Initialize database:
```bash
# Make sure PostgreSQL is running
python -m app.database
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

## Development

- Backend API documentation available at `http://localhost:8000/docs`
- Frontend development server runs at `http://localhost:3000`

## License

MIT 