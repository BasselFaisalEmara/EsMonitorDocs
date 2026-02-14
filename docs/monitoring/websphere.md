# Middleware (WebSphere) Monitoring

Monitoring WebSphere Application Server via the **JMX Bridge Module**.

> The JMX Bridge (`JmxBridge.jar`) is implemented and collects basic JVM metrics. Advanced WebSphere-specific metrics (thread pools, JDBC pools, SSL certs) are planned but not yet implemented.

---

## JVM Health (via JMX Bridge)

| Metric Key | MBean | Attribute | Status |
| :--- | :--- | :--- | :---: |
| `maximo.jvm.heap.used` | `java.lang:type=Memory` | `HeapMemoryUsage.used` | ✅ Implemented |
| `maximo.jvm.heap.max` | `java.lang:type=Memory` | `HeapMemoryUsage.max` | ✅ Implemented |
| `maximo.jvm.threads.active` | `java.lang:type=Threading` | `ThreadCount` | ✅ Implemented |
| `maximo.jvm.classes.loaded` | `java.lang:type=ClassLoading` | `LoadedClassCount` | ✅ Implemented |
| `maximo.jvm.cpu.process` | `java.lang:type=OperatingSystem` | `ProcessCpuLoad` | ✅ Implemented |

### Configuration

Enable JMX collection in `agent/config.json`:
```json
{
    "maximo": {
        "enabled": true,
        "protocol": "iiop",
        "host": "localhost",
        "port": 9060,
        "username": "wasadmin",
        "password": "wasadmin"
    }
}
```

| Protocol | Use Case | Port |
| :--- | :--- | :--- |
| `iiop` | Traditional WebSphere 8.5/9.0 | 9060 (default) |
| `rmi` | Liberty Profile / Open Liberty | 9443 (default) |

---

## Planned WebSphere Metrics

The following metrics are documented targets but **not yet collected** by the JMX Bridge.

### Thread Pools

| Metric Key | Description | Status |
| :--- | :--- | :---: |
| `ibm.was.threads.webcontainer.active` | WebContainer active threads | 🔴 Not Implemented |
| `ibm.was.threads.webcontainer.max` | WebContainer max threads | 🔴 Not Implemented |

### JDBC Connection Pools

| Metric Key | Description | Status |
| :--- | :--- | :---: |
| `ibm.was.jdbc.free_connections` | MaximoDS free JDBC connections | 🔴 Not Implemented |
| `ibm.was.jdbc.wait_time_ms` | JDBC connection wait time | 🔴 Not Implemented |

### JVM Extended

| Metric Key | Description | Status |
| :--- | :--- | :---: |
| `ibm.was.jvm.heap.percent_used` | Heap usage as percentage | 🔴 Not Implemented |
| `ibm.was.jvm.gc.time_spent` | GC pause time | 🔴 Not Implemented |

### Security

| Metric Key | Description | Status |
| :--- | :--- | :---: |
| `security.cert.expiry_days` | SSL certificate days until expiry | 🔴 Not Implemented |

---

## Prerequisites

- Java JDK 8+ installed on the Maximo server
- `JmxBridge.jar` deployed in the agent's `lib/` directory (included in the agent package)
- WebSphere admin port accessible (default 9060 for IIOP)
- Valid WebSphere admin credentials
