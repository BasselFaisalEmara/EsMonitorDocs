# DR & Backup Strategy

## Backup Policy
**Frequency**: Daily Full Backup + Hourly Transaction Logs.

### Scripted Backup
eSolutions provides a built-in backup utility.
```bash
esol-admin backup --target s3://my-backup-bucket/daily --retention 30d
```

## Disaster Recovery
In case of primary site failure:
1.  **Activate Standby Core**: The Passive Core node in the DR site promotes itself to Active.
2.  **DNS Update**: `monitor.internal` DNS TTL is 60s, allowing rapid switchover.
3.  **Collector Failover**: Collectors are configured with primary and secondary Core IPs. They will automatically reroute traffic.
