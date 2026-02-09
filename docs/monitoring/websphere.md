# Middleware (WebSphere) Scope

Monitoring via the **JMX Bridge Module**.

## JVM Health
*   **Heap Usage**: `ibm.was.jvm.heap.percent_used`
    *   *Strategy*: Alert at 85% utilization to allow time for GC analysis.
*   **Garbage Collection**: `ibm.was.jvm.gc.time_spent`

## Thread Pools
Ensures the WebContainer is not saturated.
*   **Metric**: `ibm.was.threads.webcontainer.active`
*   **Metric**: `ibm.was.threads.webcontainer.max`

## JDBC Connection Pools
Monitors the `MaximoDS` connection pool health.
*   **Metric**: `ibm.was.jdbc.free_connections`
*   **Metric**: `ibm.was.jdbc.wait_time_ms`

## SSL Certificate Probes
Scans the WebSphere KeyStore (KDB) for expiring internal certs.
*   **Probe**: `security.cert.expiry_days`
