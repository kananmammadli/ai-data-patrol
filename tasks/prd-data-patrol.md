# Product Requirements Document: Data-Patrol

## Introduction/Overview
Data-Patrol is a data quality monitoring system designed to help organizations maintain high data quality across their data ecosystem. It enables automated quality checks across multiple databases, provides visual dashboards for monitoring, and implements a role-based access control system for different stakeholders.

## Goals
1. Establish a centralized platform for monitoring data quality across multiple database systems
2. Reduce the time to detect and respond to data quality issues
3. Provide department-specific visibility into data quality metrics
4. Enable self-service data quality monitoring for different user roles
5. Automate notification processes for data quality issues

## User Stories

### For Data Engineers
- As a Data Engineer, I want to create custom SQL-based quality checks so that I can monitor specific data quality aspects
- As a Data Engineer, I want to set up scheduling for individual checks so that they run at appropriate intervals
- As a Data Engineer, I want to configure severity levels and expiry periods for checks so that issues are properly prioritized

### For Data Analysts
- As a Data Analyst, I want to view quality metrics for my department's data so that I can trust the data I'm analyzing
- As a Data Analyst, I want to receive notifications about severe quality issues so that I can adjust my analysis accordingly

### For Business Users
- As a Business User, I want to see a high-level dashboard of data quality in my department so that I can make informed decisions
- As a Business User, I want to drill down into specific quality metrics so that I can understand data reliability

### For Operations Teams
- As an Ops Team member, I want to monitor data quality across systems so that I can proactively address issues
- As an Ops Team member, I want to view historical quality metrics so that I can identify patterns and trends

## Functional Requirements

### 1. Database Connectivity
1.1. The system must support connections to PostgreSQL databases
1.2. The system must support connections to MySQL databases
1.3. The system must support connections to Amazon Redshift
1.4. The system must support connections to Snowflake

### 2. Check Configuration
2.1. The system must allow users to define custom SQL queries as quality checks with the following properties:
   a. Check name and description for clear identification
   b. Connection identifier to specify the target database
   c. SQL query that must include a 'severity' column in its output
   d. Number of output rows to save when severity changes
2.2. The system must support individual scheduling for each check
2.3. The system must allow configuring severity-specific settings:
   a. List of recipients for each severity level
   b. Expiry period for each severity level
2.4. The system must support adding troubleshooting instructions for the check
2.5. The system must support organizing checks by department and project
2.6. The system must allow adding optional tags to checks for better organization

### 3. Dashboard & Visualization
3.1. The system must provide a main dashboard with a general heatmap of all checks
3.2. The system must support filtering dashboards by department
3.3. The system must support on-demand monitoring of checks:
   a. Ability to rerun any specific check on demand
   b. Display check execution history with status and results
3.4. The system must display historical check results:
   a. Plot check runs for any selected time period
   b. Show severity trends over time
3.5. The system must support drill-down capabilities from high-level metrics

### 4. Access Control
4.1. The system must support three privilege levels: Admin, Engineer, and Analyst
4.2. The system must support role-based access control at department/project level
4.3. The system must restrict dashboard access based on user roles
4.4. The system must restrict check configuration capabilities based on user roles

### 5. Notifications
5.1. The system must support email notifications
5.2. The system must support Slack notifications
5.3. The system must trigger notifications only when:
   a. A check returns a different severity level than its previous run
   b. The current severity's expiry period has elapsed since the last notification
5.4. Each notification must include:
   a. Check name and description
   b. Troubleshooting instructions
   c. CSV file attachment with the check results (number of rows as configured)
   d. SQL file attachment with the query script
5.5. The system must maintain notification history with all attachments

## Non-Goals (Out of Scope)
1. Real-time streaming data quality checks
2. Machine learning-based anomaly detection
3. Support for non-SQL databases
4. Multi-step quality checks (initial version)
5. Data correction or cleansing capabilities
6. Integration with external data catalogs

## Technical Considerations
1. The application should be designed with a modular architecture to allow easy addition of new database types
2. Database connection credentials must be stored securely
3. The system should handle database connection timeouts gracefully
4. Check execution should be asynchronous to prevent system overload
5. Historical data should be stored with appropriate retention policies

## Design Considerations
1. Dashboard should follow a minimalist design focusing on clear visualization of issues
2. Color coding should be used consistently (e.g., red for critical issues, yellow for warnings)
3. Navigation should be intuitive with clear hierarchy (Global → Department → Project)
4. Mobile-responsive design for dashboard views

## Success Metrics
1. Number of detected exceptions (indicating active usage of the system)
2. Time to detection of data quality issues
3. User adoption rate across different roles
4. Number of active checks per department
5. System reliability (uptime and successful check execution rate)

## Open Questions
1. What is the expected volume of checks and frequency of execution?
2. Are there any specific compliance requirements for data access and monitoring?
3. What is the expected retention period for historical check results?
4. Should the system support custom notification channels beyond email and Slack?
5. What is the expected response time for dashboard queries?
