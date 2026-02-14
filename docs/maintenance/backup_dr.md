# DR & Backup Strategy

> **Status**: The features described on this page are **planned** but not yet implemented. The platform currently operates as a Tier 1 MVP with no built-in backup or disaster recovery tooling.

---

## Current State

| Feature | Status |
| :--- | :--- |
| Built-in backup utility (`esol-admin`) | 🔴 Not Implemented |
| S3/Cloud backup integration | 🔴 Not Implemented |
| Active/Standby Core failover | 🔴 Not Implemented |
| DNS-based DR switchover | 🔴 Not Implemented |
| Automated restore | 🔴 Not Implemented |

---

## Manual Backup (Interim Procedure)

Since the platform uses SQLite, backup is straightforward — copy the database file.

### Database Backup
```powershell
# Windows — Copy the SQLite database file
copy "C:\eSolutions\Core\es_monitor.db" "C:\Backups\es_monitor_%date:~-4%-%date:~3,2%-%date:~0,2%.db"
```

```bash
# Linux — Copy with timestamp
cp /opt/esolutions/core/es_monitor.db /backups/es_monitor_$(date +%F).db
```

### Configuration Backup
```powershell
# Backup config files
copy "C:\eSolutions\Core\config.yaml" "C:\Backups\config.yaml"
copy "C:\eSolutions\Agent\config.json" "C:\Backups\config.json"
```

### Scheduled Backup (Windows Task Scheduler)
```powershell
# Create a daily backup task
schtasks /create /tn "eSolutions DB Backup" /tr "copy C:\eSolutions\Core\es_monitor.db C:\Backups\es_monitor_daily.db" /sc daily /st 02:00
```

---

## Recovery Procedure

1. Stop the Core service
2. Replace `es_monitor.db` with the backup copy
3. Restart the Core service
4. Verify via dashboard that metrics resume

---

## Planned Features (Future Phases)

| Phase | Feature | Description |
| :--- | :--- | :--- |
| **C.1** | Built-in backup CLI | `esol-admin backup` command with scheduling |
| **C.2** | S3/Azure Blob export | Cloud backup integration |
| **C.3** | Active/Standby failover | Dual-Core with automatic promotion |
| **C.4** | Data retention policies | Automatic purge of metrics older than N days |
