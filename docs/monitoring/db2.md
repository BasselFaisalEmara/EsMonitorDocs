# Database (DB2) Monitoring

The **DB2 Application Module** connects directly to the DB2 instance.

## Performance Indicators

*   **Active Applications**: `ibm.db2.connections.active`
    *   Alert if > 80% of `MAXAPPLS`.
*   **Locking**: `ibm.db2.locks.deadlocks`
    *   Alert: Any increase > 0.

## Capacity Planning

*   **Tablespace Usage**: `ibm.db2.tablespace.usage_pct[MAXDATA]`
    *   Used for trend analysis and storage forecasting.
*   **Transaction Logs**: `ibm.db2.logs.primary_usage`

## Maintenance Checks
*   **Backup Age**: `ibm.db2.maintenance.last_backup_age_hours`
    *   Critical Alert if > 24 hours.
