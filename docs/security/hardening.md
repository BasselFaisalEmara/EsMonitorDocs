# Security & Hardening

## Current Security Posture

> **Status**: The platform is currently in **MVP / Development** stage. The security features listed below represent the **target architecture**. Items marked ✅ are implemented; items marked 🔴 are planned for future phases.

---

## Transport Security

| Feature | Status | Details |
| :--- | :---: | :--- |
| Agent → Core communication | 🔴 **Plaintext HTTP** | Agents send metrics via `http://` to the Core API |
| TLS 1.3 encryption | 🔴 Not Implemented | Planned for Phase B — requires certificate provisioning |
| HTTPS on Dashboard | 🔴 Not Implemented | Core serves dashboard over HTTP |

**Current Risk**: All metric data and alert information is transmitted in cleartext. Suitable for isolated lab/dev networks only.

**Mitigation (Interim)**: Deploy behind a reverse proxy (NGINX/IIS) with TLS termination.

```nginx
# Example: NGINX reverse proxy with TLS
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/esolutions.crt;
    ssl_certificate_key /etc/ssl/esolutions.key;

    location / {
        proxy_pass http://127.0.0.1:8444;
    }
}
```

---

## Authentication & Authorization

| Feature | Status | Details |
| :--- | :---: | :--- |
| API Authentication | 🔴 Not Implemented | All API endpoints are publicly accessible |
| Dashboard Login | 🔴 Not Implemented | Dashboard is accessible without credentials |
| Agent Authentication | 🔴 Not Implemented | Any client can POST metrics to `/api/v1/metrics/ingest` |
| Active Directory / LDAP | 🔴 Not Implemented | Planned for enterprise deployments |
| Role-Based Access Control | 🔴 Not Implemented | No user roles exist |

**Current Risk**: Any network actor can inject fake metrics, read all alerts, or access the dashboard.

**Mitigation (Interim)**: Restrict access via firewall rules — allow only known agent IPs to reach port 8444.

---

## Secrets Management

| Feature | Status | Details |
| :--- | :---: | :--- |
| SMTP credentials | ⚠️ **Plaintext in config.yaml** | Email password stored as plain text |
| JMX credentials | ⚠️ **Plaintext in config.json** | WebSphere admin password stored as plain text |
| Encrypted Vault (`esol-vault`) | 🔴 Not Implemented | Planned — environment variables recommended as interim |

**Mitigation (Interim)**: Use environment variables for sensitive values:
```yaml
# config.yaml
notifications:
  email:
    password: ${SMTP_PASSWORD}  # Read from environment
```

---

## Runtime Security

| Feature | Status | Details |
| :--- | :---: | :--- |
| Dedicated service account | 🔴 Not Implemented | Agent/Core run as the executing user |
| Process isolation | ✅ **Implemented** | Agent and Core are separate processes |
| Log file rotation | 🔴 Not Implemented | Log files grow unbounded |
| Input validation | ✅ **Implemented** | Pydantic models validate all API inputs |

---

## Security Roadmap

| Phase | Feature | Priority |
| :--- | :--- | :---: |
| **B.1** | API Key authentication for agents | 🔴 High |
| **B.2** | HTTPS via reverse proxy documentation | 🟡 Medium |
| **B.3** | Environment variable secret injection | 🟡 Medium |
| **C.1** | Native TLS support in Core | 🔴 High |
| **C.2** | Dashboard login (local users) | 🟡 Medium |
| **C.3** | Active Directory / LDAP integration | 🟢 Low |
| **C.4** | Certificate-based agent authentication | 🟢 Low |
