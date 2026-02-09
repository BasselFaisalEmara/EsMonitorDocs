# eSolutions Monitoring Platform - Quick Start Guide

## ✅ Phase 1 Complete!

You now have a complete MVP implementation with:
- ✓ Core API (FastAPI)
- ✓ Database models (PostgreSQL)
- ✓ Agent with collectors (CPU, Memory, Disk)
- ✓ Configuration files
- ✓ Startup scripts

## 🚀 Quick Start (Windows)

### Step 1: Run Setup
```cmd
setup.bat
```

### Step 2: Configure PostgreSQL

1. Install PostgreSQL 15+ if not already installed
2. Create the database:
```sql
CREATE DATABASE es_monitor;
CREATE USER es_admin WITH PASSWORD 'YourStrongPassword';
GRANT ALL PRIVILEGES ON DATABASE es_monitor TO es_admin;
```

3. Edit `core\config.yaml` and update the database password:
```yaml
database:
  password: YourStrongPassword
```

### Step 3: Start Core API
```cmd
start_core.bat
```

You should see:
```
Starting eSolutions Monitoring Core...
✓ Database tables created successfully
✓ Core API ready
```

API will be available at: http://localhost:8443

### Step 4: Start Agent (New Terminal)
```cmd
start_agent.bat
```

You should see:
```
eSolutions Monitoring Agent
Hostname:     YOUR-COMPUTER
Core URL:     http://localhost:8443
Interval:     60s
Collectors:   3 enabled
✓ Sent 5 metrics to Core
```

## 🚀 Quick Start (Linux/Mac)

```bash
# Make scripts executable
chmod +x setup.sh start_core.sh start_agent.sh

# Run setup
./setup.sh

# Configure PostgreSQL (same as Windows Step 2)

# Start Core
./start_core.sh

# Start Agent (new terminal)
./start_agent.sh
```

## 🔍 Verify Everything is Working

### 1. Check API Health
```bash
curl http://localhost:8443/
```

Expected response:
```json
{
  "status": "running",
  "service": "eSolutions Monitoring Core",
  "version": "0.1.0"
}
```

### 2. View API Documentation
Open browser: http://localhost:8443/docs

### 3. Query Metrics
```bash
curl http://localhost:8443/api/v1/metrics/summary
```

### 4. Check Database
```sql
-- Connect to database
psql -U es_admin -d es_monitor

-- View recent metrics
SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;
```

## 📁 Project Structure

```
EsMonitor/
├── core/
│   ├── api/
│   │   └── main.py          ← FastAPI application
│   ├── database/
│   │   ├── models.py        ← Database schema
│   │   └── connection.py    ← DB connection
│   └── config.yaml          ← Core configuration
├── agent/
│   ├── collectors/
│   │   ├── base.py          ← Base collector class
│   │   └── system.py        ← CPU, Memory, Disk collectors
│   ├── agent.py             ← Main agent loop
│   └── config.json          ← Agent configuration
├── requirements.txt
├── setup.bat / setup.sh
├── start_core.bat / start_core.sh
└── start_agent.bat / start_agent.sh
```

## ⚙️ Configuration

### Core API (`core/config.yaml`)
```yaml
database:
  host: localhost      # Database host
  port: 5432          # PostgreSQL port
  name: es_monitor    # Database name
  user: es_admin      # Database user
  password: ***       # Database password

api:
  host: 0.0.0.0       # API listen address
  port: 8443          # API port
  workers: 4          # Number of workers
```

### Agent (`agent/config.json`)
```json
{
  "core_url": "http://localhost:8443",  // Core API URL
  "hostname": "auto",                    // "auto" or specific hostname
  "interval": 60,                        // Collection interval (seconds)
  "collectors": {
    "cpu": true,                         // Enable CPU collector
    "memory": true,                      // Enable memory collector
    "disk": true,                        // Enable disk collector
    "network": false                     // Enable network collector
  }
}
```

## 🎯 Next Steps

### Week 1 Goals (Current Phase ✓)
- [x] Core API accepting metrics
- [x] Database storing metrics
- [x] Agent collecting and sending metrics

### Week 2 Goals (Next Phase)
- [ ] Add alert evaluation
- [ ] Implement email/Teams notifications
- [ ] Build simple web dashboard
- [ ] Add more metric collectors (Maximo-specific)

### Week 3 Goals
- [ ] Package agent as executable (PyInstaller)
- [ ] Create deployment automation (Ansible)
- [ ] Add Collectors (intermediate layer)
- [ ] Implement Celery for background tasks

## 📖 Documentation
All project documentation is now located in `EsMonitorDocs/`.

To view it locally:
```powershell
cd EsMonitorDocs
mkdocs serve
```
Then open [http://localhost:8000](http://localhost:8000)
