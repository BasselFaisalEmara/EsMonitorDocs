# Python Development Guide

This section provides technical details for developers working on the eSolutions Platform Python codebase.

## Project Structure

```
esolutions-platform/
├── core/                      # Core Engine
│   ├── api/                   # FastAPI REST endpoints
│   ├── engine/                # Metric processing engine
│   ├── alerts/                # Alert evaluation logic
│   └── workers/               # Celery background tasks
├── agents/                    # Agent codebase
│   ├── collectors/            # Metric collectors (psutil, WMI, etc.)
│   ├── probes/                # Custom probe framework
│   └── transport/             # Communication with collectors
├── web/                       # Dashboard
│   ├── backend/               # FastAPI backend
│   ├── frontend/              # React frontend
│   └── api/                   # API routes
└── tests/                     # Unit and integration tests
```

## Core Dependencies

### Production Requirements
```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
celery[redis]==5.3.6
redis==5.0.1
psycopg2-binary==2.9.9       # PostgreSQL driver
sqlalchemy==2.0.25           # ORM
pydantic==2.5.3              # Data validation
requests==2.31.0             # HTTP client
psutil==5.9.8                # System metrics
python-dateutil==2.8.2       # Date/time utilities
pyyaml==6.0.1                # YAML config parsing
jinja2==3.1.3                # Template engine
cryptography==42.0.0         # Encryption/TLS

# IBM Integration
ibm_db==3.2.3                # DB2 driver
jpype1==1.5.0                # Java integration (for JMX)
```

### Agent-Specific Dependencies
```txt
# agent-requirements.txt (Windows)
pywin32==306                 # Windows APIs
wmi==1.5.1                   # WMI interface

# agent-requirements.txt (Linux)
# (psutil covers most Linux needs)
```

## Core Engine Architecture

### 1. FastAPI Application (`core/api/main.py`)
```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from core.engine.metrics import MetricsEngine
from core.alerts.evaluator import AlertEvaluator

app = FastAPI(title="eSolutions Monitoring Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

@app.post("/api/v1/metrics/ingest")
async def ingest_metrics(payload: MetricPayload):
    """Receive metrics from Collectors"""
    engine = MetricsEngine()
    await engine.process(payload)
    return {"status": "accepted"}

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time dashboard updates"""
    await websocket.accept()
    # Stream metric updates...
```

### 2. Metric Processing Engine (`core/engine/metrics.py`)
```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session

class MetricsEngine:
    async def process(self, payload: MetricPayload):
        async with get_session() as session:
            # Store in TimescaleDB
            await self._store_metrics(session, payload.metrics)
            
            # Trigger alert evaluation
            await self._evaluate_alerts(payload.metrics)
    
    async def _evaluate_alerts(self, metrics: List[Metric]):
        evaluator = AlertEvaluator()
        for metric in metrics:
            if evaluator.should_alert(metric):
                await self._dispatch_alert(metric)
```

### 3. Celery Workers (`core/workers/tasks.py`)
```python
from celery import Celery
from core.engine.metrics import MetricsEngine

celery_app = Celery('esolutions', broker='redis://localhost:6379/0')

@celery_app.task
def aggregate_metrics_hourly():
    """Runs every hour to create rollup aggregates"""
    engine = MetricsEngine()
    engine.aggregate(period='1h')

@celery_app.task
def send_alert_notification(alert_id: int):
    """Send alert to Teams/Email"""
    from core.notifications.teams import send_teams_message
    alert = Alert.get_by_id(alert_id)
    send_teams_message(alert)
```

## Agent Framework

### Agent Main Loop (`agents/agent.py`)
```python
import time
import psutil
from agents.transport import CollectorClient
from agents.collectors.cpu import CPUCollector
from agents.collectors.memory import MemoryCollector

class Agent:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.client = CollectorClient(self.config['collector_url'])
        self.collectors = [
            CPUCollector(),
            MemoryCollector(),
            # ... more collectors
        ]
    
    def run(self):
        while True:
            metrics = []
            for collector in self.collectors:
                metrics.extend(collector.collect())
            
            self.client.send_batch(metrics)
            time.sleep(self.config['interval'])

if __name__ == "__main__":
    agent = Agent("/etc/esolutions/agent.json")
    agent.run()
```

### Example Collector (`agents/collectors/cpu.py`)
```python
import psutil
from agents.collectors.base import BaseCollector

class CPUCollector(BaseCollector):
    def collect(self) -> List[Metric]:
        cpu_percent = psutil.cpu_percent(interval=1)
        return [
            Metric(
                key="os.cpu.usage",
                value=cpu_percent,
                timestamp=time.time(),
                tags={"hostname": self.hostname}
            )
        ]
```

## Configuration Management

### Core Config (`/etc/esolutions/core.yaml`)
```yaml
database:
  host: postgres.internal
  port: 5432
  name: es_monitor
  user: es_admin
  password: ${DB_PASSWORD}  # Environment variable

api:
  host: 0.0.0.0
  port: 8443
  workers: 8
  tls:
    enabled: true
    cert: /etc/esolutions/certs/server.crt
    key: /etc/esolutions/certs/server.key

celery:
  broker: redis://redis.internal:6379/0
  result_backend: redis://redis.internal:6379/1
```

## Testing

### Unit Tests (`tests/test_metrics_engine.py`)
```python
import pytest
from core.engine.metrics import MetricsEngine

@pytest.mark.asyncio
async def test_metric_ingestion():
    engine = MetricsEngine()
    payload = MetricPayload(metrics=[
        Metric(key="test.metric", value=42.0)
    ])
    result = await engine.process(payload)
    assert result.status == "success"
```

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ --cov=core --cov-report=html
```

## Deployment

### Building Agent Executable
```bash
# Package agent as standalone executable (Windows/Linux)
pyinstaller --onefile \
    --name esolutions-agent \
    --hidden-import=psutil \
    --hidden-import=wmi \
    agents/agent.py
```

### Docker Deployment (Core)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ ./core/
CMD ["uvicorn", "core.api.main:app", "--host", "0.0.0.0", "--port", "8443"]
```
