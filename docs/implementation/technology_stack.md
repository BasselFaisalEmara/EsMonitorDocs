# Technology Stack

The eSolutions Monitoring Platform is built with Python and designed to scale from a single-server MVP to a distributed enterprise deployment.

> This page documents both the **current implementation** and the **target architecture**. Items marked ✅ are in use today; items marked 🔴 are planned for future phases.

---

## Current Stack (MVP — Tier 1)

These technologies are **actively used** in the running system.

### Core Engine
| Component | Technology | Version | Notes |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.11+ | All components |
| **Web Framework** | FastAPI | 0.109+ | REST API + static file serving |
| **ASGI Server** | Uvicorn | 0.27+ | Development and production |
| **ORM** | SQLAlchemy | 2.0+ | Database models and queries |
| **Validation** | Pydantic | 2.5+ | API request/response validation |
| **Config** | PyYAML | 6.0+ | YAML configuration parsing |

### Database
| Component | Technology | Notes |
| :--- | :--- | :--- |
| **Storage** | SQLite | Zero-config, file-based (`es_monitor.db`) |
| **Schema** | SQLAlchemy ORM | Auto-created on startup |

### Web Dashboard
| Component | Technology | Notes |
| :--- | :--- | :--- |
| **Frontend** | HTML5 + Alpine.js (CDN) | Single-page application |
| **Styling** | Tailwind CSS (CDN) | Utility-first CSS framework |
| **Gauges** | Hand-coded SVG | Circular gauge components |
| **Data Refresh** | REST API polling | Every 5 seconds |
| **Served By** | FastAPI `StaticFiles` | No separate web server needed |

### Agent
| Component | Technology | Notes |
| :--- | :--- | :--- |
| **Metrics** | psutil | Cross-platform CPU, RAM, Disk, Network |
| **HTTP Client** | requests | Agent → Core communication |
| **JMX Bridge** | Java subprocess | `JmxBridge.jar` for Maximo/WebSphere MBeans |
| **Packaging** | PyInstaller | Standalone `.exe` (no Python required on target) |

### Notifications
| Channel | Technology | Status |
| :--- | :--- | :--- |
| **Email (SMTP)** | `smtplib` (stdlib) | ✅ Implemented (very_critical only) |
| **Dashboard** | REST API | ✅ Implemented (all severities) |
| **Log File** | Python `logging` | ✅ Implemented |

### Alert Engine
| Component | Technology | Notes |
| :--- | :--- | :--- |
| **Rule Evaluation** | Python (synchronous) | Evaluated inline during metric ingestion |
| **Rules Storage** | SQLite `alert_rules` table | Seeded on first startup |
| **History** | SQLite `alert_history` table | FIRING / RESOLVED lifecycle |

---

## Target Architecture (Future Phases)

The following technologies are **planned** but **not yet implemented**.

### Phase B (Next Sprint)

| Component | Planned Technology | Purpose | Status |
| :--- | :--- | :--- | :---: |
| MS Teams Notifications | Incoming Webhooks | Alert channel for operations | 🔴 Planned |
| API Authentication | API Key / Bearer Token | Secure agent-to-core communication | 🔴 Planned |
| HTTPS | Reverse Proxy (NGINX) or native TLS | Transport encryption | 🔴 Planned |

### Phase C (Enterprise Scaling)

| Component | Planned Technology | Purpose | Status |
| :--- | :--- | :--- | :---: |
| Production Database | PostgreSQL 15+ | Scalable storage for high ingestion | 🔴 Planned |
| Time-Series Extension | TimescaleDB | Efficient time-series queries | 🔴 Planned |
| Message Queue | RabbitMQ / Redis Streams | Decouple ingestion from processing | 🔴 Planned |
| Background Workers | Celery | Async alert evaluation and aggregation | 🔴 Planned |
| Dashboard Frontend | React + TypeScript | Rich interactive dashboards | 🔴 Planned |
| Charting | Apache ECharts | Time-series graphs | 🔴 Planned |
| Real-time Updates | WebSockets | Live dashboard without polling | 🔴 Planned |
| Authentication | OAuth2 / SAML 2.0 | Enterprise AD integration | 🔴 Planned |
| Secrets | HashiCorp Vault | Encrypted credential storage | 🔴 Planned |
| Docker | Container deployment | Cloud-native packaging | 🔴 Planned |

---

## Dependency List

### `requirements.txt` (Current)
```txt
fastapi
uvicorn[standard]
sqlalchemy
pydantic
pyyaml
psutil
requests
```

### Agent Additional Dependencies
```txt
# Included in PyInstaller bundle — no separate install needed
psutil          # System metrics
requests        # HTTP client
```

> **Note**: The agent is packaged as a standalone `.exe` via PyInstaller. Target servers do **not** need Python installed.
