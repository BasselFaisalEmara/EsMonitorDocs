# eSolutions Monitoring Platform — Deployment Guide

## Build

On your development machine, run:
```powershell
cd EsMonitor
.\build_all.bat
```

This produces two deployment folders:
```
dist\deploy\
├── agent\                     ← Copy to each Maximo server
│   ├── EsMonitorAgent.exe
│   ├── config.json
│   └── lib\JmxBridge.jar
│
└── core\                      ← Copy to the Core server
    ├── EsMonitorCore.exe
    └── config.yaml
```

> **No Python required on target servers.** Both EXEs are fully standalone.

---

## Deploy Core Server

### 1. Transfer
```powershell
xcopy /E /I dist\deploy\core \\CORE-SERVER\C$\eSolutions\Core
```

### 2. Configure
Edit `config.yaml` on the Core server:
```yaml
database:
  type: sqlite
  name: es_monitor.db

api:
  host: 0.0.0.0
  port: 8443
  workers: 4
```

### 3. Firewall
```powershell
netsh advfirewall firewall add rule name="eSolutions Core" dir=in action=allow protocol=tcp localport=8443
```

### 4. Run
```powershell
EsMonitorCore.exe
```

### 5. Verify
- API: `http://CORE-IP:8443/` → `{"status": "running"}`
- Dashboard: `http://CORE-IP:8443/dashboard`
- Docs: `http://CORE-IP:8443/docs`

---

## Deploy Agent (per Maximo Server)

### 1. Transfer
```powershell
xcopy /E /I dist\deploy\agent \\MAXIMO-SERVER\C$\eSolutions\Agent
```

### 2. Configure
Edit `config.json` on the Maximo server:
```json
{
    "core_url": "http://CORE-SERVER-IP:8443",
    "tenant_id": "client-name",
    "hostname": "auto",
    "interval": 60,
    "collectors": {
        "cpu": true,
        "memory": true,
        "disk": true,
        "network": false
    },
    "maximo": {
        "enabled": true,
        "host": "localhost",
        "port": 9060,
        "username": "wasadmin",
        "password": "wasadmin"
    }
}
```

| Field | Description |
| :--- | :--- |
| `core_url` | IP/hostname of your Core server |
| `tenant_id` | Client identifier for multi-tenancy |
| `maximo.enabled` | Set `true` on Maximo/WAS servers |
| `maximo.port` | WebSphere JMX/RMI port (usually 9060) |

### 3. Run
```powershell
EsMonitorAgent.exe
```

### 4. Verify
```
============================================================
eSolutions Monitoring Agent
============================================================
Hostname:     MAXIMO-APP-01
Core URL:     http://10.20.1.5:8443
Collectors:   5 enabled
============================================================
✓ Sent 7 metrics to Core
```

---

## Run as Windows Service (Recommended)

Since these are console applications, use **NSSM (Non-Sucking Service Manager)** to run them as robust Windows Services. This handles auto-restart and log capturing correctly.

1. Download `nssm.exe` (Latest release).
2. Run Command Prompt as **Administrator**.

### Agent Service
```powershell
nssm install EsMonitorAgent "C:\eSolutions\Agent\EsMonitorAgent.exe"
nssm set EsMonitorAgent AppDirectory "C:\eSolutions\Agent"
nssm set EsMonitorAgent AppStdout "C:\eSolutions\Agent\logs\service_out.log"
nssm set EsMonitorAgent AppStderr "C:\eSolutions\Agent\logs\service_err.log"
nssm start EsMonitorAgent
```

### Core Service
```powershell
nssm install EsMonitorCore "C:\eSolutions\Core\EsMonitorCore.exe"
nssm set EsMonitorCore AppDirectory "C:\eSolutions\Core"
nssm set EsMonitorCore AppStdout "C:\eSolutions\Core\logs\service_out.log"
nssm set EsMonitorCore AppStderr "C:\eSolutions\Core\logs\service_err.log"
nssm start EsMonitorCore
```

---

## Checking Logs

When running as a service, output is written to log files in the `logs\` directory.

| Component | Log File Path |
| :--- | :--- |
| **Agent** | `C:\eSolutions\Agent\logs\agent.log` |
| **Core** | `C:\eSolutions\Core\logs\core.log` |

**Troubleshooting Commands:**
```powershell
# Tail the agent log
Get-Content C:\eSolutions\Agent\logs\agent.log -Wait -Tail 20

# Tail the core log
Get-Content C:\eSolutions\Core\logs\core.log -Wait -Tail 20
```

---

## Prerequisites per Server

| Server | Requirement |
| :--- | :--- |
| Core | Windows Server 2016+ or RHEL 7+, Inbound TCP 8443 |
| Agent | Windows Server 2016+ or RHEL 7+, Outbound TCP 8443 |
| Agent (JMX) | Java JDK 8+ on the Maximo server |

---

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| `Failed to connect to Core` | Check firewall, verify Core IP in config.json |
| `JMX query timed out` | Verify WAS admin port (9060), check JMX is enabled |
| `Java not found` | Install JDK 8+ and add to PATH |
| Dashboard shows 0 hosts | Agent not sending — check config.json core_url |
| Port 8443 in use | Change port in config.yaml |
