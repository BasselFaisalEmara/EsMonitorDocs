# Technology Stack

The eSolutions Monitoring Platform is built on a modern, scalable microservices architecture.

## Core Technologies

### 1. Platform Engine
*   **Language**: Python 3.11+
*   **Framework**: FastAPI (async web framework) + Celery (distributed task queue).
*   **Reason**: Rapid development, extensive library ecosystem, and strong integration capabilities with IBM technologies.
*   **Components**:
    *   **Data Ingestion Pipeline**: FastAPI endpoints + asyncio for concurrent processing (10K+ metrics/sec).
    *   **Real-time Alert Engine**: Celery workers with rule evaluation using Python expressions.
    *   **REST API Gateway**: FastAPI with Pydantic validation for external integrations.
    *   **Scheduler**: APScheduler for cron-like metric collection tasks.

### 2. Time-Series Database
*   **Primary**: SQLite (for MVP / Single-node deployments).
*   **Production**: PostgreSQL 15 (for clustered/HA deployments).
*   **Retention Policy**: 
    *   One file database per core instance (`es_monitor.db`).
    *   Automatic VACUUM management.

### 3. Messaging Queue
*   **Technology**: RabbitMQ 3.12
*   **Purpose**: Decouples Collectors from the Core for fault tolerance.
*   **Queues**:
    *   `metrics.ingest` - Raw metric stream.
    *   `alerts.dispatch` - Outbound notifications.

### 4. Web Dashboard
*   **Backend**: Python 3.11 (FastAPI framework).
*   **Frontend**: React 18 + TypeScript + Material-UI.
*   **Charting**: Apache ECharts / Plotly.js for interactive graphs.
*   **Real-time Updates**: WebSockets (via FastAPI WebSocket support).
*   **Authentication**: OAuth2 / SAML 2.0 integration with Active Directory.

### 5. Configuration Management
*   **Format**: YAML / JSON (stored in PostgreSQL `config` table).
*   **Validation**: JSON Schema for all configuration files.

## Agent Technologies

### Universal Agent (Cross-Platform)
*   **Language**: Python 3.11 (packaged with PyInstaller for standalone executables).
*   **Deployment**: 
    *   **Windows**: MSI Installer (via SCCM / GPO).
    *   **Linux**: RPM / DEB packages (via Ansible / yum/apt).
*   **Core Libraries**:
    *   `psutil` - Cross-platform system metrics (CPU, RAM, Disk, Network).
    *   `requests` - HTTP client for API monitoring.
    *   `pyodbc` / `ibm_db` - Database connectivity (SQL Server, DB2).
*   **Windows-Specific Probes**:
    *   WMI queries via `wmi` library.
    *   Event Log tailing via `win32evtlog`.
    *   PowerShell script execution via `subprocess`.
*   **Linux-Specific Probes**:
    *   `/proc` and `/sys` filesystem parsing.
    *   Systemd status via `subprocess` + `systemctl`.
    *   Bash script execution.

## Integrations

### IBM Maximo
*   **Method**: RESTful API + Direct DB Queries (Read-Only).
*   **Libraries**: `python-requests`, `ibm_db` (DB2 connector).

### WebSphere
*   **Method**: JMX over RMI.
*   **Libraries**: Java Gateway (OpenJDK 11 + JMX Client).

### Microsoft Teams
*   **Method**: Incoming Webhooks.
*   **Payload**: Adaptive Cards (JSON format).

## Security Technologies
*   **Encryption**: TLS 1.3 (ChaCha20-Poly1305 cipher suite).
*   **Secrets**: HashiCorp Vault integration (optional) or native encrypted storage.
*   **Certificates**: Internal PKI using Let's Encrypt or corporate CA.
