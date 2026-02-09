# Runbook: Incident Response

## Workflow
1.  **Detect**: Alert Engine triggers a notification.
2.  **Triage**: Operator acknowledges alert in Dashboard Service.
3.  **Remediate**: Follow specific playbook below.
4.  **Resolve**: System auto-closes alert when metric returns to normal.

## Restart Procedures

=== "Maximo / WebSphere (Linux)"
    ```bash
    # Stop
    /opt/IBM/HTTPServer/bin/apachectl stop
    /opt/IBM/WebSphere/AppServer/profiles/ctgAppSrv01/bin/stopServer.sh MXServer
    
    # Start
    /opt/IBM/WebSphere/AppServer/profiles/ctgAppSrv01/bin/startServer.sh MXServer
    /opt/IBM/HTTPServer/bin/apachectl start
    ```

=== "Maximo / WebSphere (Windows)"
    1.  Open `services.msc`.
    2.  Stop **IBM HTTP Server**.
    3.  Stop **IBMWAS85Service - Node01 - MXServer**.
    4.  Wait 60 seconds.
    5.  Start **IBMWAS85Service**.
    6.  Start **IBM HTTP Server**.

## Common Scenarios

*   **Scenario**: "High JVM Heap"
    *   **Action**: Login to WAS Console > Troubleshooting > Java Dumps > Generate Heap Dump. Restart JVM if stuck.
*   **Scenario**: "Agent Unreachable"
    *   **Action**: Check Firewall (Port 8444). Restart Agent Service.
