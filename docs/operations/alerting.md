# Alerting Rules

Alerts are defined in the **Alert Engine** policies.

## Integration: Microsoft Teams
eSolutions provides a native connector for Teams Webhooks.

**Payload Format**:
```json
{
  "summary": "CRITICAL: Maximo UI Down",
  "source": "max-ui-01",
  "severity": 3,
  "metrics": {
    "net.http.check": 503
  }
}
```

## Routing Logic
1.  **Work Hours**: Alerts route to the L1 Support Dashboard.
2.  **Off Hours**: Critical alerts route to the On-Call PagerDuty/SMS integration.

## Escalation Chain
*   **T+0m**: Notification to channel.
*   **T+15m**: SMS to Primary SRE.
*   **T+60m**: Email to Manager if Unacknowledged.
