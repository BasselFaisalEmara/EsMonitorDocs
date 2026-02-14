# Database (DB2) Monitoring

> **Status**: DB2 monitoring is **planned** but not yet implemented. No DB2 collector, driver, or connection code exists in the current codebase.

---

## Current State

| Component | Status |
| :--- | :--- |
| DB2 Collector (agent module) | 🔴 Not Implemented |
| `ibm_db` Python driver | 🔴 Not in requirements.txt |
| DB2 connection configuration | 🔴 Not Implemented |
| DB2 metric ingestion | 🔴 Not Implemented |

---

## Planned Metrics

The following metrics are planned for the DB2 monitoring module:

### Performance Indicators

| Metric Key | Description | Alert Condition | Status |
| :--- | :--- | :--- | :---: |
| `ibm.db2.connections.active` | Active application connections | > 80% of `MAXAPPLS` | 🔴 Planned |
| `ibm.db2.locks.deadlocks` | Deadlock count | Any increase > 0 | 🔴 Planned |

### Capacity Planning

| Metric Key | Description | Use Case | Status |
| :--- | :--- | :--- | :---: |
| `ibm.db2.tablespace.usage_pct[MAXDATA]` | Tablespace usage percentage | Storage forecasting | 🔴 Planned |
| `ibm.db2.logs.primary_usage` | Transaction log usage | Log space management | 🔴 Planned |

### Maintenance Checks

| Metric Key | Description | Alert Condition | Status |
| :--- | :--- | :--- | :---: |
| `ibm.db2.maintenance.last_backup_age_hours` | Hours since last backup | Critical if > 24 hours | 🔴 Planned |

---

## Implementation Approach (When Built)

The DB2 collector will:

1. Connect to DB2 using the `ibm_db` Python driver
2. Execute read-only monitoring queries against DB2 snapshot functions
3. Report metrics to the Core API via the standard ingestion endpoint

### Required Dependencies
```txt
ibm_db==3.2.3               # IBM DB2 Python driver
```

### Required Configuration
```json
{
    "db2": {
        "enabled": true,
        "host": "db2-server",
        "port": 50000,
        "database": "MAXDB",
        "username": "db2monitor",
        "password": "password"
    }
}
```

### Prerequisites
- DB2 client libraries on the agent server
- `db2monitor` user with `SYSMON` authority (read-only)
- Network connectivity from agent to DB2 instance (TCP 50000)
