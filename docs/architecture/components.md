# Platform Components

## eSolutions Monitoring Core (Server)
The heart of the platform.
*   **Role**: Central orchestration, Alert Engine execution, and long-term storage.
*   **OS Support**: 
    *   **Linux**: RHEL 8/9, Ubuntu 22.04 LTS.
    *   **Windows**: Windows Server 2019 / 2022.
*   **Database**: PostgreSQL (recommended) or MySQL.

## eSolutions Collector
Acts as a data concentrator and buffer.
*   **Role**: Offloads polling from the Core and buffers data for up to 24h during network outages.
*   **Deployment**: One per security zone (e.g., App Zone, DB Zone).
*   **OS Support**: Linux (Preferred) or Windows.

## eSolutions Agent
The endpoint data gatherer.
*   **Role**: Collects CPU, RAM, Disk, and invokes custom probes (PowerShell/Bash).
*   **Features**:
    *   **Dynamic OS Support**: Single binary architecture for Windows and Linux.
    *   **Plugin System**: Extensible via Python/Go plugins for DB2 and WebSphere.
    *   **Encryption**: Native TLS support.

## Dashboard Service
The visualization layer.
*   **Role**: Renders topology maps, graphs, and SLA reports.
*   **Access**: Web-based (HTTPS).
