# Agent Rollout Strategy

Agents are deployed to Maximo App Servers, HTTP Servers, and Database Nodes.

## Automated Deployment (Ansible/SCCM)

Manual installation is discouraged. Use the `esolutions-deploy` playbook.

### 1. Prepare Release Artifacts
*   **Windows**: `esol-agent-win-x64.msi`
*   **Linux**: `esol-agent-linux-x86_64.rpm`
*   **Configuration Template**: `agent_config.json`

### 2. Configuration Logic (`agent_config.json`)
The agent uses a modern JSON-based configuration.

```json
{
  "agent": {
    "hostname": "auto_detect",
    "environment": "production",
    "buffer_size_mb": 128
  },
  "connectivity": {
    "collector_list": ["10.20.1.5:8444", "10.20.1.6:8444"],
    "tls_enabled": true,
    "psk_file": "/etc/esolutions/secret.key"
  }
}
```

### 3. Execution (Windows Example)
Push via SCCM / PowerShell Remoting:

```powershell
Start-Process msiexec.exe -ArgumentList "/i esol-agent.msi /qn CONFIG=C:\Temp\agent_config.json" -Wait
```

### 4. Verification
Check the `agent.log` for the handshake success message:
`[INFO] Handshake with Collector 10.20.1.5:8444 successful. Session ID: A1B2...`
