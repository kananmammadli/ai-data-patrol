# Backend Implementation Status (snapshot)

This file contains a concise snapshot of the backend structure and implemented features. Update this file as progress continues.

## Folder structure (backend/)
- alembic/
  - versions/ — migration scripts (initial schema + org model)
  - env.py, script.py.mako, alembic.ini — Alembic config
- requirements.txt — Python dependencies for backend
- app/
  - main.py — FastAPI app entrypoint; registers routers, metrics, middleware
  - core/
    - database.py — SQLAlchemy engine, Base, session factory
    - connection_manager.py — connector registry, connection/pool management, health checks
    - secure_storage.py — Fernet-based credential encrypt/decrypt utilities
    - sql_validation.py — SQL syntax / safety validation utilities
    - scheduler.py — APScheduler integration and check runner orchestration
    - logging_config.py — structured logging setup
  - models/
    - data_quality.py — SQLAlchemy models:
      - DatabaseConnection
      - DataQualityCheck (name, SQL, schedule, org_node_id, num_rows_to_save, expiry, notification rule refs, tags, troubleshooting)
      - SeverityConfig (per-check severity -> recipients / threshold mapping)
      - DataQualityResult (run results, severity (integer), saved rows, status, timestamps)
      - OrganizationNode (hierarchical org/project model persisted in DB)
  - schemas/
    - data_quality.py — Pydantic schemas for checks, results, severity/notification config, organization nodes
  - api/
    - v1/
      - checks.py — endpoints to create/edit/list checks, rerun on-demand, update expiry, assign org_node_id
      - severity.py — endpoints to manage severity -> recipients / expiry mappings
      - organization.py — CRUD for organization tree (departments/projects), export/import JSON endpoints
      - health/metrics endpoints (health, metrics)
  - tests/
    - test_connectors.py — unit tests for connectors and connection manager (mocked)
    - test_organization.py — tests for org endpoints

## Implemented functionality (summary)
- FastAPI backend scaffolded and running (main app + routers)
- Database schema + Alembic migrations for checks, results, connections, organization
- Database connectivity layer:
  - Base connector interface + ConnectionManager
  - PostgreSQL (asyncpg), MySQL (aiomysql), Redshift (asyncpg-compatible), Snowflake (sync connector with threads) connectors
  - Connection pooling management, secure credential storage, health checks
- Check configuration models: supports SQL (must return severity integer), schedule, num_rows_to_save, tags, org_node_id, troubleshooting text
- Severity configuration and recipient/expiry rule storage and API (implemented via `SeverityConfig` model: per-check severity mappings to recipient lists and thresholds)
- SQL validation utility and API endpoint for dry-validate queries
- Scheduling: APScheduler-based runner to schedule and execute checks
- Logging (structured) and monitoring (/metrics for Prometheus)
- Unit tests for connectors and organization API
- CI pipeline (GitHub Actions) runs tests for backend + frontend

## Next recommended focus areas
- Implement check execution engine & detailed result storage (store saved rows when severity changes)
- Notification sending pipeline (email + Slack), CSV/SQL attachments
- Dashboard integration points for historical results and rerun API
- Additional tests and end-to-end scenarios
