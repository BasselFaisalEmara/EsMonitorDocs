# Dashboard Strategy

The eSolutions Platform provides a web dashboard at **`http://CORE-IP:8443/dashboard`**, served directly by the Core API. No additional web server is required.

---

## Currently Implemented

### Operations Dashboard (DASH-001)

The main dashboard provides real-time visibility into all monitored infrastructure.

**Stat Cards:**
| Card | Data Source | Description |
| :--- | :--- | :--- |
| Monitored Hosts | `/api/v1/metrics/summary` | Count of all agents reporting in |
| Active Alerts | `/api/v1/alerts?status=FIRING` | Count of unresolved threshold breaches |
| System Health | Derived | Green if 0 alerts, otherwise Red |

**Active Hosts Table:**
- Hostname (clickable for drill-down)
- Tenant badge
- Online/Offline status
- Last Seen timestamp
- Total metric count

**Features:**
- Multi-tenant filtering (dropdown selector)
- Auto-refresh every 5 seconds
- Dark mode UI with Tailwind CSS + Alpine.js

### Host Metrics Drill-Down (DASH-005)

Click any hostname in the Active Hosts table to reveal a detail panel.

**Circular Gauge Cards:**
| Gauge | Metric Key | Thresholds |
| :--- | :--- | :--- |
| CPU Usage | `os.cpu.usage` | Green < 70%, Yellow 70-90%, Red > 90% |
| Memory | `os.memory.percent` | Green < 70%, Yellow 70-90%, Red > 90% |
| Disk | `os.disk.usage_percent` | Green < 70%, Yellow 70-90%, Red > 90% |
| Network Out | `os.network.bytes_sent` | Scaled to MB |

**Full Metrics Table:**
- All metric keys with values and timestamps
- Color-coded values for high CPU/Memory
- Auto-refreshes while the panel is open

---

## Planned Dashboards

The following dashboards are documented and planned for future phases.

### Executive View — CIO / Management (DASH-002)
**Goal**: High-level SLA tracking for leadership.

| Widget | Description | Status |
| :--- | :--- | :--- |
| Overall Maximo Availability | 30-day rolling average uptime | 🔴 Not Implemented |
| License Usage | Active User License count vs Purchased | 🔴 Not Implemented |
| System Status | Green/Yellow/Red traffic light per environment | 🔴 Not Implemented |

### Operations Center — NOC (DASH-003)
**Goal**: Rapid triage of alerts and system status.

| Widget | Description | Status |
| :--- | :--- | :--- |
| Problem Feed | Live stream of Critical/Warning alerts | 🔴 Not Implemented |
| Database Lock Monitor | DB2 lock/deadlock live view | 🔴 Not Implemented |
| JVM Cluster Heatmap | WebSphere JVM health across cluster | 🔴 Not Implemented |

### Engineer View — SRE / Admin (DASH-004)
**Goal**: Deep Dive Root Cause Analysis.

| Widget | Description | Status |
| :--- | :--- | :--- |
| Heap Memory Graph | Time-series JVM heap usage | 🔴 Not Implemented |
| GC Activity Graph | Garbage Collection pauses over time | 🔴 Not Implemented |
| CPU Steal Time | Hypervisor contention detection | 🔴 Not Implemented |
| Log Stream | Tail of `SystemOut.log` and `db2diag.log` | 🔴 Not Implemented |

---

## Technical Details

- **Technology**: HTML5, Tailwind CSS (CDN), Alpine.js (CDN)
- **Served by**: FastAPI `StaticFiles` mount at `/static`
- **Entry point**: `GET /dashboard` → `core/web/static/index.html`
- **Data source**: All data fetched from Core REST API (`/api/v1/*`)
- **Refresh interval**: 5 seconds (configurable in JavaScript)
