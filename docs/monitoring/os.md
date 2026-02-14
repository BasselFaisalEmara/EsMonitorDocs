# Infrastructure (OS) Monitoring

Unified metrics for Windows and Linux endpoints, collected by the eSolutions Agent via `psutil`.

---

## Compute Metrics

| Resource | Metric Key | Status | Alert Thresholds |
| :--- | :--- | :---: | :--- |
| **CPU** | `os.cpu.usage` | ✅ Implemented | Warning > 70%, Critical > 90%, Very Critical > 95% |
| **RAM (%)** | `os.memory.percent` | ✅ Implemented | Warning > 80%, Critical > 90%, Very Critical > 95% |
| **RAM (MB)** | `os.memory.used_mb` | ✅ Implemented | Collected, no default alert rule |
| **RAM Total** | `os.memory.total_mb` | ✅ Implemented | Collected, no default alert rule |
| **Disk Usage** | `os.disk.usage_percent` | ✅ Implemented | Warning > 85%, Critical > 90%, Very Critical > 95% |
| **Disk Used** | `os.disk.used_gb` | ✅ Implemented | Collected, no default alert rule |
| **Disk Total** | `os.disk.total_gb` | ✅ Implemented | Collected, no default alert rule |
| **Network Sent** | `os.network.bytes_sent` | ✅ Implemented | Collected, no default alert rule |
| **Network Recv** | `os.network.bytes_recv` | ✅ Implemented | Collected, no default alert rule |
| **Swap** | `os.swap.usage_pct` | 🔴 Not Implemented | Planned |

> **Note**: Disk metrics include per-partition tags (e.g., `mountpoint=C:\`). Each partition generates separate alerts.

---

## Planned Features

| Feature | Metric Key | Status | Description |
| :--- | :--- | :---: | :--- |
| Service Monitoring | `os.service.status[name]` | 🔴 Not Implemented | Check if critical services (e.g., IBM HTTP Server) are running |
| Log Inspection | `os.log.grep[path, pattern]` | 🔴 Not Implemented | Real-time tailing of log files for error patterns |
| Swap Usage | `os.swap.usage_pct` | 🔴 Not Implemented | Monitor swap/pagefile usage |

---

## Dashboard Visualization

The Operations Dashboard shows circular gauges for the following metrics when you click on a host:

| Gauge | Metric Key | Color Thresholds |
| :--- | :--- | :--- |
| CPU Usage | `os.cpu.usage` | Green < 70%, Yellow 70-90%, Red > 90% |
| Memory | `os.memory.percent` | Green < 70%, Yellow 70-90%, Red > 90% |
| Disk (per partition) | `os.disk.usage_percent` | Green < 70%, Yellow 70-90%, Red > 90% |
| Network Out | `os.network.bytes_sent` | Scaled to human-readable units |
