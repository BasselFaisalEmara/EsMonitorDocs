# Alerting Rules

The eSolutions Alert Engine evaluates incoming metrics against configurable threshold rules and triggers notifications based on severity.

---

## Severity Model

All alert rules have a **severity** level that determines the notification behavior:

| Severity | Level | Notification | Use Case |
| :--- | :---: | :--- | :--- |
| `info` | 1 | Dashboard only | Informational counters |
| `warning` | 2 | Dashboard + log | Approaching threshold |
| `critical` | 3 | Dashboard + log | Threshold breached |
| `very_critical` | 4 | Dashboard + log + **Email** | Emergency action required |

> **Only `very_critical` alerts trigger email notifications.** All other severities are visible on the dashboard and in logs.

---

## Default Alert Rules

The following rules are seeded automatically on first startup:

| Metric | Condition | Threshold | Severity |
| :--- | :---: | :---: | :--- |
| `os.cpu.usage` | > | 70% | ⚠️ warning |
| `os.cpu.usage` | > | 90% | 🔴 critical |
| `os.cpu.usage` | > | 95% | 🚨 very_critical |
| `os.memory.percent` | > | 85% | ⚠️ warning |
| `os.memory.percent` | > | 90% | 🔴 critical |
| `os.memory.percent` | > | 95% | 🚨 very_critical |
| `os.disk.usage_percent` | > | 85% | ⚠️ warning |
| `os.disk.usage_percent` | > | 90% | 🔴 critical |
| `os.disk.usage_percent` | > | 95% | 🚨 very_critical |

---

## Email Notifications

Email alerts are sent via SMTP for **`very_critical`** severity breaches only.

### Configuration (`config.yaml`)

```yaml
notifications:
  email:
    enabled: true
    smtp_host: smtp.gmail.com
    smtp_port: 587
    use_tls: true
    username: "your-email@gmail.com"
    password: "your-app-password"
    sender: "esolutions-alerts@yourcompany.com"
    recipients:
      - "admin@yourcompany.com"
      - "oncall@yourcompany.com"
```

### Gmail App Password Setup
If using Gmail, you must use an **App Password** (not your regular password):
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App passwords** → Generate one for "Mail"
4. Use that 16-character password in `config.yaml`

### Email Format

**Trigger Email** includes:
- Severity badge (color-coded)
- Hostname
- Metric key and current value
- Threshold that was breached
- Timestamp

**Resolution Email** is sent when the metric returns below the threshold.

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/alerts` | List active (FIRING) alerts |
| `GET` | `/api/v1/alerts?tenant=X` | Filter alerts by tenant |

---

## Planned Features

| Feature | Status |
| :--- | :--- |
| Microsoft Teams Webhooks | 🔴 Not Implemented |
| Escalation Chain (T+15m SMS, T+60m Manager) | 🔴 Not Implemented |
| Work Hours / Off Hours Routing | 🔴 Not Implemented |
| Alert Acknowledgment | 🔴 Not Implemented |
