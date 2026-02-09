# Metric Definitions

eSolutions uses a hierarchical Namespace format for metrics.

## Namespace Standard

`domain.component.subcomponent.metric[attributes]`

| Segment             | Example                      | Description                   |
| :------------------ | :--------------------------- | :---------------------------- |
| **Domain**    | `os`, `ibm`, `net`     | High level category.          |
| **Component** | `maximo`, `was`, `db2` | The software being monitored. |
| **Sub**       | `jvm`, `cron`, `logs`  | Specific internal component.  |

## Threshold Strategy

We avoid "Alert Fatigue" by implementing a 3-tier severity model in the **Alert Engine**.

1. **Info**: Logged for analysis, no notification. (e.g., "Backup Succeeded").
2. **Warning**: Potential issue, requires next-day review. (e.g., "Disk 85% full").
3. **Critical**: Immediate action required. (e.g., "Maximo Login Failed").

## Hysteresis implementation

To prevent flapping, all numerical alerts are configured with a recovery delta in the platform JSON configuration.

```json
{
  "trigger": "high_cpu",
  "threshold": 90,
  "recovery": 80,
  "duration": "5m"
}
```
