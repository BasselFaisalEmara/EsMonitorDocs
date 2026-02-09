# Enterprise Scaling Strategy

The eSolutions Monitoring Platform is designed to scale from a single server (MVP) to a globally distributed enterprise deployment. This document outlines the architectural tiers and scaling strategies.

## Tier 1: MVP / Single Site
**Best for**: POCs, Small environments (< 50 Servers), Development.

In this model, all "Core" components run on a single server.
*   **eSolutions Core**: 1 Node (API + Alert Engine).
*   **Database**: SQLite (local file) or Single PostgreSQL instance.
*   **Dashboard**: Served directly by the Core.

```mermaid
graph LR
    Agents -->|Port 8443| Core
    Core -->|Read/Write| SQLite[(es_monitor.db)]
    User -->|Port 80/443| Core
```

## Tier 2: Distributed (Multi-Client / MSP)
**Best for**: Managed Service Providers (MSPs), Multi-Site Organizations.

This model separates the "Ingestion" from the "Processing" and introduces **Collectors** to bridge network zones.

*   **Collectors**: Placed in remote customer networks (behind firewalls). They buffer data and push to the Core.
*   **Core**: Centralized in the MSP Datacenter.
*   **Database**: PostgreSQL 15 (Dedicated Server).

```mermaid
graph LR
    subgraph "Client A (Site 1)"
        AgentA1 --> CollectorA[Collector A]
        AgentA2 --> CollectorA
    end
    
    subgraph "Client B (Site 2)"
        AgentB1 --> CollectorB[Collector B]
    end
    
    subgraph "MSP Datacenter"
        CollectorA -->|TLS| CORE[Core API]
        CollectorB -->|TLS| CORE
        CORE --> DB[(PostgreSQL)]
    end
```

## Tier 3: Enterprise (High Availability)
**Best for**: Large Enterprises (> 1000 Servers), Critical Infrastructure.

This model eliminates Single Points of Failure (SPOF) and handles high ingestion rates.

*   **Load Balancer**: NGINX / HAProxy distributing traffic.
*   **Core Cluster**: Multiple stateless Core instances behind the LB.
*   **Message Queue**: RabbitMQ buffers incoming metrics for asynchronous processing.
*   **Database**: PostgreSQL Cluster (Patroni/stolon) + TimescaleDB.

```mermaid
graph TD
    LB[Load Balancer] --> Core1
    LB --> Core2
    Core1 -->|Publish| RabbitMQ
    Core2 -->|Publish| RabbitMQ
    
    RabbitMQ --> Worker1[Alert Engine]
    RabbitMQ --> Worker2[Data Writer]
    
    Worker1 --> DB[(PostgreSQL Cluster)]
    Worker2 --> DB
```

## Capacity Planning

| Tier | Metric/Sec | Storage (1 Yr) | CPU | RAM |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (MVP)** | < 100 | ~50 GB | 2 vCPU | 4 GB |
| **Tier 2 (SME)** | 100 - 1,000 | ~500 GB | 4 vCPU | 8 GB |
| **Tier 3 (Ent)** | > 1,000 | > 2 TB | 8+ vCPU | 16+ GB |

## Handling Multi-Tenancy (Multi-Client)
For MSPs monitoring multiple distinct clients:

1.  **Network Isolation**: Use **Collectors** as gateways. No direct connection from Agent to Core required.
2.  **Data Segregation**: 
    *   Add `tenant_id` tag to every metric at the Collector level.
    *   Row-Level Security (RLS) in PostgreSQL ensures Client A cannot query Client B's data.
3.  **Authentication**: Issue unique API Tokens per Collector.
