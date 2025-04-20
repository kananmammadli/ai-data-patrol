# DataPatrol - Product Requirements Document

## Overview
DataPatrol is a web application designed to monitor and maintain data quality across multiple databases and organizations. It provides automated checks, notifications, and a comprehensive dashboard for data quality management.

## System Architecture

### Authentication & Authorization
- **Authentication Methods**:
  - Google OAuth
  - Okta
- **User Roles**:
  - Admin
  - Configurator
  - Viewer

### Core Components
1. **User Management**
   - User registration and role assignment
   - Role-based access control
   - User profile management

2. **Database Connections**
   - Secure storage of database credentials
   - Support for multiple database types
   - Connection testing and validation

3. **Data Quality Checks**
   - SQL-based check definitions
   - Configurable schedules
   - Severity levels
   - Result previews
   - Troubleshooting guides

4. **Notification System**
   - Email notifications
   - Configurable notification rules
   - Severity-based routing

## Data Models

### User
```typescript
interface User {
  id: UUID;
  email: string;
  role: UserRole; // enum: admin, configurator, viewer
}
```

### DBConnection
```typescript
interface DBConnection {
  id: UUID;
  name: string;
  host: string;
  port: number;
  database: string;
  username: string;
  encryptedPassword: string;
}
```

### DataCheck
```typescript
interface DataCheck {
  id: UUID;
  name: string;
  organization: string;
  project: string;
  description: string;
  troubleshootingGuide: string;
  dbConnectionId: UUID;
  sqlScript: string;
  schedule: string; // cron-style
  expiryPeriodHours: number;
  maxAttachmentRows: number;
  severityRecipients: SeverityRecipient[];
}
```

### SeverityRecipient
```typescript
interface SeverityRecipient {
  id: UUID;
  dataCheckId: UUID;
  minSeverity: number;
  maxSeverity: number;
  emails: string[];
}
```

### CheckRun
```typescript
interface CheckRun {
  id: UUID;
  dataCheckId: UUID;
  runAt: Date;
  severity: number;
  resultPreview: string; // CSV format
  notified: boolean;
  notificationTimestamp: Date | null;
}
```

## Core Logic

### Check Execution
1. **Scheduling**
   - Periodic execution based on cron schedule
   - Manual trigger capability
   - Concurrent execution support

2. **Severity Calculation**
   - If no rows returned → severity = 0
   - If rows returned → use max value from Severity column
   - Custom severity calculation support

3. **Result Processing**
   - CSV generation for result preview
   - Row limit enforcement (maxAttachmentRows)
   - Error handling and logging

### Notification Logic
1. **Trigger Conditions**
   - Severity change from last successful run
   - Time since last notification exceeds expiryPeriodHours
   - Manual trigger option

2. **Email Notification**
   - Subject: `[Severity: X] Alert: {Check Name}`
   - Body:
     - Description
     - Troubleshooting guide
     - Execution timestamp
   - Attachment: CSV of results (limited to maxAttachmentRows)

## User Interface

### Home Dashboard
- Charts and visualizations
  - Checks run over time
  - Active severities distribution
- Filters
  - Organization
  - Project
- Summary table
  - Current status
  - Last run timestamp
  - Last severity level

### User Management
- User list with roles
- Role assignment interface
- Authentication integration

### Check Management
- Hierarchical organization (Organization > Project > Checks)
- Filter and search capabilities
- Drag-and-drop rearrangement
- Export functionality

### Check Detail Page
- Edit interface for:
  - Description
  - SQL script
  - Schedule
  - Expiry period
  - Recipients
  - Max attachment rows
- Manual run capability
- Run history
- Result preview and download

## Permissions Matrix

| Feature                | Admin | Configurator | Viewer |
|-----------------------|-------|--------------|--------|
| View Dashboard        | ✅    | ✅           | ✅     |
| Manage Users         | ✅    | ❌           | ❌     |
| Manage DB Connections| ✅    | ❌           | ❌     |
| Configure Data Checks| ✅    | ✅           | ❌     |
| Run Checks Manually  | ✅    | ✅           | ❌     |
| View Run Results     | ✅    | ✅           | ✅     |

## Non-Functional Requirements

### Security
- OAuth2 authentication
- Encrypted credential storage
- Role-based access control
- Audit logging

### Scalability
- Support for multiple organizations
- Support for multiple projects
- Support for hundreds of checks
- Concurrent check execution

### Reliability
- Retry logic for failed checks
- Comprehensive error logging
- Error tracking and monitoring
- Database connection resilience

### Performance
- Fast dashboard loading
- Efficient check execution
- Optimized database queries
- Caching where appropriate

### Audit Trail
- User action logging
- Configuration change tracking
- Check execution history
- Notification history

## Development Guidelines

### Backend
- FastAPI for API development
- SQLAlchemy for database operations
- APScheduler for task scheduling
- Python-Jose for JWT handling

### Frontend
- React with TypeScript
- Material-UI for components
- React Query for data fetching
- React Router for navigation

### Database
- PostgreSQL for data storage
- UUID for primary keys
- Proper indexing for performance
- Regular backups

## Deployment Requirements
- Docker support
- Environment variable configuration
- Database migration support
- Health check endpoints
- Monitoring and logging setup 