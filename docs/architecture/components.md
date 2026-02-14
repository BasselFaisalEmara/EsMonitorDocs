# Platform Components

## eSolutions Monitoring Core (Server)
The central hub handling data processing, alerting, and visualization.

| Aspect | Current Implementation |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **Database** | SQLite (file-based, zero-config) |
| **Dashboard** | HTML5 + Alpine.js + Tailwind CSS (served by Core) |
| **Alert Engine** | Synchronous rule evaluation on metric ingestion |
| **Notifications** | Email (SMTP) for very_critical severity |
| **Packaging** | PyInstaller standalone `.exe` |
| **OS Verified** | Windows 10/11, Windows Server 2016-2022 |

## eSolutions Agent
The endpoint data gatherer, installed on each monitored server.

| Aspect | Current Implementation |
| :--- | :--- |
| **Language** | Python 3.11+ (packaged as standalone `.exe`) |
| **System Metrics** | CPU, Memory, Disk, Network (via `psutil`) |
| **JMX Metrics** | Maximo/WebSphere MBeans (via `JmxBridge.jar`) |
| **Transport** | HTTP POST to Core API |
| **Packaging** | PyInstaller standalone `.exe` |
| **OS Verified** | Windows 10/11, Windows Server 2016-2022 |

### Collected Metrics

| Metric Key | Source | Description |
| :--- | :--- | :--- |
| `os.cpu.usage` | psutil | CPU utilization percentage |
| `os.memory.percent` | psutil | RAM usage percentage |
| `os.memory.used_mb` | psutil | RAM used in MB |
| `os.memory.total_mb` | psutil | Total RAM in MB |
| `os.disk.usage_percent` | psutil | Disk usage per partition |
| `os.disk.used_gb` | psutil | Disk used in GB per partition |
| `os.disk.total_gb` | psutil | Total disk in GB per partition |
| `os.network.bytes_sent` | psutil | Network bytes sent |
| `os.network.bytes_recv` | psutil | Network bytes received |
| `maximo.jvm.heap.used` | JMX | JVM heap memory used |
| `maximo.jvm.heap.max` | JMX | JVM heap memory max |
| `maximo.jvm.threads.active` | JMX | Active JVM thread count |
| `maximo.jvm.classes.loaded` | JMX | Loaded class count |
| `maximo.jvm.cpu.process` | JMX | JVM process CPU load |

## eSolutions Collector
Acts as a data concentrator and buffer between agents and core.

| Aspect | Status |
| :--- | :--- |
| **Implementation** | 🔴 **Not Yet Built** |
| **Purpose** | Offload polling, buffer data during outages, bridge network zones |
| **Planned Deployment** | One per security zone (App Zone, DB Zone) |

> **Current Architecture**: Agents connect **directly** to the Core API. The Collector component is planned for Tier 2 (multi-site) deployments and does not exist in the current codebase.

## Dashboard Service
The web-based visualization layer.

| Aspect | Current Implementation |
| :--- | :--- |
| **Technology** | HTML5 + Alpine.js + Tailwind CSS (CDN) |
| **Served By** | FastAPI `StaticFiles` (no separate web server) |
| **Access** | `http://CORE-IP:8444/dashboard` |
| **Features** | Host overview, metric gauges, alert table, tenant filtering, dark mode |
| **Refresh** | Auto-refresh every 5 seconds via REST API polling |
| **Authentication** | 🔴 None (publicly accessible) |
