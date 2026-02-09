# Getting Started - MVP Implementation

This guide walks through building the **Minimum Viable Product (MVP)** of the eSolutions Monitoring Platform in 1-2 weeks.

## Goals

By the end of this guide, you will have:
- ✅ A working Core API that ingests metrics
- ✅ A PostgreSQL database storing metric data
- ✅ A Python agent collecting system metrics
- ✅ Basic alert evaluation
- ✅ A simple web interface to view metrics

## Prerequisites

### Software Requirements
*   Python 3.11+
*   PostgreSQL 15+
*   Git
*   Node.js 18+ (for web dashboard)

### Database
The platform uses **SQLite** for zero-configuration storage. No database installation is required.
The data will be stored in `EsMonitor/es_monitor.db`.

## Project Structure

```
EsMonitor/
├── core/                   # Core Engine
│   ├── api/               # FastAPI application
│   ├── database/          # Database models and connection
│   ├── engine/            # Metric processing
│   └── config.yaml        # Configuration
├── agent/                 # Agent codebase
│   ├── collectors/        # Metric collectors
│   ├── agent.py          # Main agent loop
│   └── config.json       # Agent configuration
├── web/                   # Web Dashboard (Phase 2)
│   ├── backend/          # FastAPI backend
│   └── frontend/         # React app
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
└── README.md
```

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

# Initialize git
git init
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

### Step 2: Install Dependencies

Create `requirements.txt`:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pyyaml==6.0.1
python-dateutil==2.8.2
psutil==5.9.8
requests==2.31.0
```

Install:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database

The configuration in `core/config.yaml` is pre-configured for SQLite:
```yaml
database:
  type: sqlite
  name: es_monitor.db
```

### Step 4: Core API Implementation

Create `core/api/main.py`:
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from core.database.connection import get_db, init_db
from core.database.models import Metric as MetricModel

app = FastAPI(title="eSolutions Monitoring Core", version="0.1.0")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

class Metric(BaseModel):
    hostname: str
    key: str
    value: float
    timestamp: float
    tags: dict = {}

class MetricBatch(BaseModel):
    metrics: List[Metric]

@app.get("/")
def root():
    return {"status": "running", "service": "eSolutions Core"}

@app.post("/api/v1/metrics/ingest")
def ingest_metrics(batch: MetricBatch, db: Session = Depends(get_db)):
    """Receive metrics from agents or collectors"""
    try:
        for metric in batch.metrics:
            db_metric = MetricModel(
                hostname=metric.hostname,
                metric_key=metric.key,
                value=metric.value,
                timestamp=datetime.fromtimestamp(metric.timestamp),
                tags=str(metric.tags)
            )
            db.add(db_metric)
        
        db.commit()
        return {"status": "success", "ingested": len(batch.metrics)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/metrics/latest/{hostname}")
def get_latest_metrics(hostname: str, db: Session = Depends(get_db)):
    """Get latest metrics for a hostname"""
    metrics = db.query(MetricModel).filter(
        MetricModel.hostname == hostname
    ).order_by(MetricModel.timestamp.desc()).limit(20).all()
    
    return {
        "hostname": hostname,
        "metrics": [
            {
                "key": m.metric_key,
                "value": m.value,
                "timestamp": m.timestamp.isoformat()
            } for m in metrics
        ]
    }
```

### Step 5: Run the Core API

```bash
# From EsMonitor directory
uvicorn core.api.main:app --host 0.0.0.0 --port 8443 --reload
```

Test it:
```bash
curl http://localhost:8443/
```

Expected response:
```json
{"status": "running", "service": "eSolutions Core"}
```

## Phase 2: Agent (Days 4-6)

### Step 1: Create Agent Structure

Create `agent/config.json`:
```json
{
  "core_url": "http://localhost:8443",
  "hostname": "auto",
  "interval": 60,
  "collectors": {
    "cpu": true,
    "memory": true,
    "disk": true,
    "network": true
  }
}
```

### Step 2: Build Collectors

Create `agent/collectors/base.py`:
```python
from abc import ABC, abstractmethod
from typing import List, Dict
import socket

class BaseCollector(ABC):
    def __init__(self):
        self.hostname = socket.gethostname()
    
    @abstractmethod
    def collect(self) -> List[Dict]:
        pass
```

Create `agent/collectors/system.py`:
```python
import psutil
import time
from agent.collectors.base import BaseCollector

class CPUCollector(BaseCollector):
    def collect(self):
        return [{
            "hostname": self.hostname,
            "key": "os.cpu.usage",
            "value": psutil.cpu_percent(interval=1),
            "timestamp": time.time(),
            "tags": {}
        }]

class MemoryCollector(BaseCollector):
    def collect(self):
        mem = psutil.virtual_memory()
        return [{
            "hostname": self.hostname,
            "key": "os.memory.usage_percent",
            "value": mem.percent,
            "timestamp": time.time(),
            "tags": {}
        }]

class DiskCollector(BaseCollector):
    def collect(self):
        metrics = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                metrics.append({
                    "hostname": self.hostname,
                    "key": "os.disk.usage_percent",
                    "value": usage.percent,
                    "timestamp": time.time(),
                    "tags": {"mountpoint": partition.mountpoint}
                })
            except:
                pass
        return metrics
```

### Step 3: Main Agent Loop

Create `agent/agent.py`:
```python
import time
import json
import requests
from agent.collectors.system import CPUCollector, MemoryCollector, DiskCollector

class Agent:
    def __init__(self, config_path="agent/config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.collectors = []
        if self.config['collectors']['cpu']:
            self.collectors.append(CPUCollector())
        if self.config['collectors']['memory']:
            self.collectors.append(MemoryCollector())
        if self.config['collectors']['disk']:
            self.collectors.append(DiskCollector())
    
    def collect_all_metrics(self):
        metrics = []
        for collector in self.collectors:
            metrics.extend(collector.collect())
        return metrics
    
    def send_to_core(self, metrics):
        url = f"{self.config['core_url']}/api/v1/metrics/ingest"
        payload = {"metrics": metrics}
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            print(f"✓ Sent {len(metrics)} metrics to Core")
            return True
        except Exception as e:
            print(f"✗ Failed to send metrics: {e}")
            return False
    
    def run(self):
        print(f"Starting eSolutions Agent...")
        print(f"Core URL: {self.config['core_url']}")
        print(f"Interval: {self.config['interval']}s")
        
        while True:
            metrics = self.collect_all_metrics()
            self.send_to_core(metrics)
            time.sleep(self.config['interval'])

if __name__ == "__main__":
    agent = Agent()
    agent.run()
```

### Step 4: Run the Agent

```bash
# From EsMonitor directory
python -m agent.agent
```

Expected output:
```
Starting eSolutions Agent...
Core URL: http://localhost:8443
Interval: 60s
✓ Sent 5 metrics to Core
```

## Verification

### Check Database
```sql
SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;
```

### Query API
```bash
curl http://localhost:8443/api/v1/metrics/latest/YOUR_HOSTNAME
```

## Next Steps

Once you have metrics flowing:
1. Add alert evaluation (Week 2)
2. Build simple web dashboard (Week 2)
3. Package agent as executable (Week 3)
4. Deploy to test servers (Week 3)

See **Implementation Workflow** for detailed week-by-week plan.
