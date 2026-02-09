# Custom Probes (Scripts)

The Agent can execute local scripts via the **Probe Extension API**.

## Configuration
Register custom scripts in the `agent_config.json` file under the `probes` section.

```json
"probes": {
  "check_file_age": {
    "cmd": "powershell -File C:\\scripts\\age.ps1",
    "timeout": 10
  },
  "check_ssl": {
    "cmd": "/bin/bash /etc/scripts/ssl.sh",
    "timeout": 5
  }
}
```

## Windows Extension (PowerShell)
**Path**: `C:\eSolutions\Scripts\Check-FileAge.ps1`

```powershell
param([string]$Path)
$age = (New-TimeSpan -Start (Get-Item $Path).LastWriteTime).TotalMinutes
Write-Output $age
```

## Linux Extension (Bash)
**Path**: `/etc/esolutions/scripts/check_ssl.sh`

```bash
#!/bin/bash
TARGET=$1
# Logic to check SSL expiry...
echo $DAYS_REMAINING
```
