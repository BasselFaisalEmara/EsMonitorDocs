# Maximo Monitoring Scope

The eSolutions platform uses deep-dive **Application Probes** to monitor Maximo logic.

## 1. User Experience (Synthetic)

Simulates user behavior 24/7.

* **Probe**: `ux.scenario.login_flow`
* **Parameters**: `{url: "https://maximo.url", user: "monitor"}`
* **SLA**: < 3000ms response time.

## 2. Cron Task Validator

Directly inspects the `CRONTASKINSTANCE` table via the Database Connector.

* **Metric Key**: `maximo.cron.stale_count`
* **Logic**: Count instanced where `Active=1` AND `LastRun` > `Schedule + Threshold`.

## 3. Escalation Engine

Monitors the heartbeat of the Escalation processing.

* **Metric Key**: `maximo.escalation.backlog`
* **Warning**: > 50 records pending.

## 4. UI Reachability

* **Metric Key**: `net.http.check`
* **Features**: SSL Certificate Validation, Content Matching ("Sign In").

## 5. JMX Metric Collection

The agent uses a lightweight Java Bridge (`JmxBridge.jar`) to query WebSphere/Liberty MBeans.

### Key Metrics

| Metric Key                    | MBean ObjectName                    | Attribute                |
| :---------------------------- | :---------------------------------- | :----------------------- |
| `maximo.jvm.heap.used`      | `java.lang:type=Memory`           | `HeapMemoryUsage.used` |
| `maximo.jvm.threads.active` | `java.lang:type=Threading`        | `ThreadCount`          |
| `maximo.web.sessions`       | `WebSphere:type=SessionManager,*` | `LiveCount`            |
| `maximo.cron.active`        | `maximo.cron:type=CronTask,*`     | `Active`               |

### Configuration

Enable the collector in `agent/config.json` and provide credentials:

```json
"maximo": {
    "enabled": true,
    "host": "localhost",
    "port": 9060,
    "username": "wasadmin",
    "password": "password"
}
```
