# Platform Core Build

This section details the deployment of the central **Monitoring Core**.

## Architecture Setup
The Core should be deployed in a High Availability (HA) cluster configuration using a Virtual IP (VIP).

### Database Layer
eSolutions requires an enterprise-grade relational database.
*   **Recommendation**: PostgreSQL 15 (Clustered).
*   **Schema Deployment**:
    Run the `esol-db-init` utility:
    ```bash
    /opt/esolutions/bin/esol-db-init --db-host=db-cluster-vip --user=es_admin
    ```

### Core Engine Service
1.  **Install Binary**:
    *   Linux: `rpm -i esolutions-engine-enterprise.rpm`
    *   Windows: Run `Setup.exe` > Choose "Core Node".
2.  **Configuration**:
    Update the `engine.yaml` file (JSON/YAML format, not legacy INI).
    ```yaml
    core:
      mode: active
      listen_port: 8443
      workers: 50
    database:
      host: "db.internal"
      pool_size: 100
    ```

### Frontend (Dashboard Service)
Deployed on an isolated web node (Nginx/Apache).
*   **HTTPS**: Terminate SSL at the Load Balancer or the Web Node.
*   **Context Path**: `/esolutions/console`.
