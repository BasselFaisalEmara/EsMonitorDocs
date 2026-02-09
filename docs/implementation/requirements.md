# Systems Requirements

Before Phase 2 (Core Build), the following prerequisites must be met by the Infrastructure Team.

## Firewall Rules (Network)

The eSolutions Platform uses a proprietary encrypted protocol.

| Source | Destination | Port | Description |
| :--- | :--- | :--- | :--- |
| **Collectors** | **Monitoring Core** | **8443** (TCP) | Data Aggregation Stream |
| **Agents** | **Collectors** | **8444** (TCP) | Agent Data Payload |
| **Admin PC** | **Monitoring Core** | **443** (HTTPS) | Web Console Access |

## Compute Resources

### Monitoring Core (Primary)
*   **OS**: RHEL 9 or Windows Server 2022.
*   **CPU**: 4 vCPU.
*   **RAM**: 16 GB.
*   **Storage**: 200 GB SSD (Tier 1).

### Collectors (x2)
*   **OS**: RHEL 9 or Windows Server 2022.
*   **CPU**: 2 vCPU.
*   **RAM**: 4 GB.

## Service Accounts
*   **Windows**: Domain Service Account `SVC_ESOL_MON` with "Log on as a Service" rights.
*   **Linux**: `sudo` access for initial installation (revoked after rollout).
*   **Database**: `db2monitor` user with `SYSMON` authority.
*   **WebSphere**: `maxadmin` (or equivalent read-only) for JMX queries.
