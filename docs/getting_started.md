# Getting Started - MVP Implementation

This guide walks through building the **Minimum Viable Product (MVP)** of the eSolutions Monitoring Platform.

## What You'll Have

By the end of this guide, you will have:
- ✅ A working Core API that ingests metrics
- ✅ An SQLite database storing metric data (zero configuration)
- ✅ A Python agent collecting system metrics (CPU, RAM, Disk, Network)
- ✅ Alert evaluation with severity levels (warning, critical, very_critical)
- ✅ Email notifications for very_critical alerts
- ✅ A real-time web dashboard with gauges and alert tables

## Prerequisites

### Development Machine
*   Python 3.11+
*   Git
*   Java JDK 8+ (only if using Maximo JMX monitoring)

### Target Servers (for deployment)
*   **No Python required** — Agent and Core are packaged as standalone `.exe` files via PyInstaller
*   Windows Server 2016+ or RHEL 7+
*   Network: Agent must be able to reach Core on TCP port 8444

### Database
The platform uses **SQLite** for zero-configuration storage. No database installation is required.
The database file is automatically created at `core/database/es_monitor.db` on first startup.

---

## Project Structure

```
EsMonitor/
├── core/                   # Core Engine (Central Server)
│   ├── api/
│   │   └── main.py        # FastAPI application + REST endpoints
│   ├── database/
│   │   ├── connection.py  # SQLite connection management
│   │   └── models.py      # SQLAlchemy models (Metric, AlertRule, AlertHistory)
│   ├── engine/
│   │   ├── alerts.py      # Alert evaluation engine
│   │   └── notifier.py    # Email notification sender
│   ├── web/
│   │   └── static/
│   │       └── index.html # Dashboard (Alpine.js + Tailwind CSS)
│   └── config.yaml        # Core configuration (API port, SMTP settings)
│
├── agent/                  # Agent (runs on monitored servers)
│   ├── collectors/
│   │   ├── base.py        # Base collector class
│   │   ├── system.py      # CPU, Memory, Disk, Network collectors
│   │   └── maximo.py      # JMX collector for Maximo/WebSphere
│   ├── agent.py           # Main agent loop
│   └── config.json        # Agent configuration (core URL, collectors)
│
├── build_all.bat           # Build script (produces standalone EXEs)
├── start_core.bat          # Start the Core (development)
├── start_agent.bat         # Start the Agent (development)
└── requirements.txt        # Python dependencies
```

---

## Phase 1: Core API (Days 1-3)

### Step 1: Initialize Project

```bash
cd EsMonitor

# Create Python virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` contains:
```txt
fastapi
uvicorn[standard]
sqlalchemy
pydantic
pyyaml
psutil
requests
```

### Step 3: Configure Core

The configuration in `core/config.yaml` is pre-configured for local development:
```yaml
database:
  type: sqlite
  name: es_monitor.db

api:
  host: 0.0.0.0
  port: 8444
  workers: 4
```

### Step 4: Run the Core API

```bash
# From EsMonitor directory
uvicorn core.api.main:app --host 0.0.0.0 --port 8444 --reload
```

Or use the batch file:
```powershell
.\start_core.bat
```

Test it:
```bash
curl http://localhost:8444/
```

Expected response:
```json
{"status": "running", "service": "eSolutions Core"}
```

### Step 5: Open the Dashboard

Open your browser to: **`http://localhost:8444/dashboard`**

You should see the monitoring dashboard with stat cards and an empty host table.

---

## Phase 2: Agent (Days 4-6)

### Step 1: Configure the Agent

Edit `agent/config.json`:
```json
{
    "core_url": "http://localhost:8444",
    "tenant_id": "default",
    "hostname": "auto",
    "interval": 60,
    "collectors": {
        "cpu": true,
        "memory": true,
        "disk": true,
        "network": false
    },
    "maximo": {
        "enabled": false,
        "protocol": "iiop",
        "host": "localhost",
        "port": 9060,
        "username": "wasadmin",
        "password": "wasadmin"
    }
}
```

| Field | Description |
| :--- | :--- |
| `core_url` | URL of the Core API server |
| `tenant_id` | Client identifier for multi-tenancy |
| `hostname` | Set to `"auto"` to use the machine hostname |
| `interval` | Metric collection interval in seconds |
| `collectors` | Enable/disable individual metric collectors |
| `maximo.enabled` | Set `true` on Maximo/WAS servers with JMX access |

### Step 2: Run the Agent

```bash
# From EsMonitor directory
python -m agent.agent
```

Or use the batch file:
```powershell
.\start_agent.bat
```

Expected output:
```
============================================================
eSolutions Monitoring Agent
============================================================
Hostname:     YOUR-HOSTNAME
Core URL:     http://localhost:8444
Collectors:   3 enabled
============================================================
[OK] Sent 7 metrics to Core
```

---

## Verification

### Dashboard
Refresh `http://localhost:8444/dashboard` — you should see:
- **Monitored Hosts**: 1
- **Active Alerts**: Count based on current thresholds
- **System Health**: Green (Healthy), Yellow (Warning), or Red (Critical)
- Click your hostname to see CPU, Memory, and Disk gauges

### API Endpoints
```bash
# Check system status
curl http://localhost:8444/

# List monitored hosts
curl http://localhost:8444/api/v1/metrics/summary

# Get latest metrics for a host
curl http://localhost:8444/api/v1/metrics/latest/YOUR-HOSTNAME

# View active alerts
curl http://localhost:8444/api/v1/alerts
```

---

## Next Steps

Once you have metrics flowing:
1. Configure **email notifications** in `config.yaml` (see [Alerting Rules](operations/alerting.md))
2. Enable **Maximo JMX monitoring** on WAS servers (see [Maximo Metrics](monitoring/maximo.md))
3. **Package as executables** for deployment (see [Deployment Guide](deployment_guide.md))
4. Deploy to production servers (no Python required on targets)
