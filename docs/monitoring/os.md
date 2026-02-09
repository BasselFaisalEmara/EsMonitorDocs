# Infrastructure (OS) Monitoring

Unified metrics for Windows and Linux endpoints.

## Compute Metrics

| Resource | eSolutions Metric Key | Alert Threshold |
| :--- | :--- | :--- |
| **CPU** | `os.cpu.total_usage_pct` | > 90% (15 min avg) |
| **RAM** | `os.mem.available_mb` | < 2048 MB |
| **Swap** | `os.swap.usage_pct` | > 50% |
| **Disk** | `os.disk.volume.free_pct` | < 10% |

## Service Assurance
Ensures critical daemons are running.
*   **Key**: `os.service.status[name]`
    *   Example: `os.service.status["IBMHTTPServer"]`
    *   Returns: `RUNNING` or `STOPPED`.

## Log Inspection
Real-time tailing of log files for keywords.
*   **Key**: `os.log.grep[path, pattern]`
*   **Example**: `os.log.grep["/opt/IBM/HTTPServer/logs/error_log", "Segmentation Fault"]`
