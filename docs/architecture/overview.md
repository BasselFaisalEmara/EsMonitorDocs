# eSolutions Monitoring Platform Overview

The **eSolutions Monitoring Platform** is a unified, enterprise-grade observability solution designed for eSolutions clients. It provides comprehensive visibility into the health and performance of IBM Maximo environments, ensuring stability for mission-critical operations.

## High Level Design

The platform uses a distributed architecture to scale across hybrid environments (On-Premise, Cloud, and Multi-Site).

*   **eSolutions Monitoring Core**: The central brain handling data processing, alerting logic (Alert Engine), and data storage.
*   **eSolutions Collectors**: Lightweight, distributed proxies that gather data from remote zones and forward it to the Core.
*   **eSolutions Agents**: Installed on endpoints (Windows/Linux) to collect OS and Application metrics.

**Description of Architecture**:
Data flows from the **Agents** to the local **Collector**. The Collector compresses and encrypts the data before transmitting it securely to the **Monitoring Core**. The Core processes the data via the **Metrics Engine** and triggers notifications via the **Alert Engine**. Users interact with the system through the **Dashboard Service**.

## Network Flow

| Source Zone | Destination Zone | Source Component | Dest Component | Port | Protocol | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **App Zone** | **Mgmt Zone** | Collector | Monitoring Core | 8443 | TCP (TLS) | Data Transmission |
| **App Zone** | **App Zone** | Agent | Collector | 8444 | TCP | Active Checks |
| **DB Zone** | **DB Zone** | Agent | Collector | 8444 | TCP | Active Checks |
| **Admin LAN** | **Mgmt Zone** | User PC | Dashboard Svc | 443 | HTTPS | Web UI |

## Security Zones

*   **Management Zone**: Hosts the Monitoring Core and Database.
*   **Application Zone**: Hosts Maximo and Collectors.
*   **Database Zone**: Hosts DB2 and Collectors.
