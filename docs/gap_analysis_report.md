# Documentation vs Implementation — Gap Analysis Report

> **Audit Date**: 2026-02-14  
> **Auditor**: Technical Review (AI-Assisted)  
> **Scope**: All 27 documentation pages in `EsMonitorDocs/docs/` vs actual codebase in `EsMonitor/`

---

## Executive Summary

The eSolutions Monitoring Platform documentation describes a **Tier 3 enterprise-grade** monitoring system with features like TLS encryption, Active Directory authentication, RabbitMQ message queues, Celery workers, PostgreSQL clusters, Docker deployment, React dashboards, HashiCorp Vault integration, and Collector proxy nodes.

**The actual implementation is a Tier 1 MVP**: a FastAPI + SQLite application with a single-file HTML dashboard, a Python agent using `psutil`, and a basic JMX bridge. Many documented features do not exist in the codebase.

| Category | Documented Features | Actually Implemented | Gap Rate |
|:---|:---:|:---:|:---:|
| **Security & Encryption** | 7 | 0 | 🔴 100% |
| **Infrastructure (Collectors, HA, DR)** | 8 | 0 | 🔴 100% |
| **Monitoring Scope** | 18 metrics/probes | 5 | 🔴 72% |
| **Dashboard Views** | 4 dashboards | 1 | 🟡 75% |
| **Alerting & Notifications** | 6 channels | 1 | 🟡 83% |
| **Core Engine Components** | 7 components | 3 | 🟡 57% |
| **Deployment & Packaging** | 6 methods | 1 | 🔴 83% |

---

## Category 1: 🔴 CRITICAL — Security & Hardening (100% Gap)

**Documentation**: `security/hardening.md`  
**Claims**: TLS 1.3, Active Directory/LDAP authentication, certificate-based agent auth, encrypted vault (`esol-vault`), least-privilege service accounts.

### Findings

| Documented Feature | Implementation Status | Evidence |
|:---|:---|:---|
| TLS 1.3 encryption in transit | ❌ **Not implemented** | Core runs plain HTTP on port 8444. No TLS config in `run_core.py` or `main.py`. Agent `config.json` uses `http://` URLs. |
| Active Directory / LDAP auth | ❌ **Not implemented** | No authentication on any API endpoint. Dashboard is public. No auth middleware in `main.py`. |
| Certificate-based agent auth | ❌ **Not implemented** | Agent uses plain HTTP POST with no authentication. No certificate generation or validation code exists. |
| Encrypted Vault (`esol-vault`) | ❌ **Not implemented** | No vault CLI tool. Passwords stored in plaintext in `config.yaml` and `config.json`. |
| `esol_agent` / `Network Service` user | ❌ **Not implemented** | No service account setup. Agent runs as the executing user. |

> **Risk**: The entire system runs unauthenticated over HTTP. Any network actor can ingest fake metrics, read all alerts, or access the dashboard. This is **misleading for enterprise audit contexts**.

---

## Category 2: 🔴 CRITICAL — Infrastructure Components (100% Gap)

### Collectors (Documented in 5+ pages, Never Built)

**Documented in**: `architecture/overview.md`, `architecture/components.md`, `architecture/scaling.md`, `implementation/workflow.md`, `implementation/requirements.md`

| Documented Feature | Status |
|:---|:---|
| eSolutions Collectors (data concentrators) | ❌ **No code exists** — no `collector/` directory, no collector binary, no collector config |
| 24h data buffering during outages | ❌ **Not implemented** |
| Collector-to-Core TLS tunnels | ❌ **Not implemented** |
| Collector-per-security-zone deployment | ❌ **Not implemented** |

> The architecture diagram shows `Agent → Collector → Core`. **In reality, Agents connect directly to Core.** The Collector component is entirely aspirational.

### High Availability & Disaster Recovery

**Documented in**: `maintenance/backup_dr.md`, `architecture/scaling.md`

| Documented Feature | Status |
|:---|:---|
| Active/Standby Core failover | ❌ **Not implemented** |
| `esol-admin backup` CLI utility | ❌ **Not implemented** — no `esol-admin` binary exists |
| S3 backup integration | ❌ **Not implemented** |
| DNS-based DR switchover | ❌ **Not implemented** |
| Collector failover (primary/secondary Core IPs) | ❌ **Not implemented** (Collectors don't exist) |

---

## Category 3: 🟡 MAJOR — Monitoring Scope Gaps

### OS Monitoring (`monitoring/os.md`)

| Doc Metric Key | Implemented Key | Status |
|:---|:---|:---|
| `os.cpu.total_usage_pct` | `os.cpu.usage` | ⚠️ **Key name mismatch** |
| `os.mem.available_mb` | `os.memory.percent` / `os.memory.used_mb` | ⚠️ **Different metric** (doc says MB available, code sends % used) |
| `os.swap.usage_pct` | — | ❌ **Not implemented** |
| `os.disk.volume.free_pct` | `os.disk.usage_percent` | ⚠️ **Key name mismatch** and inverted logic (doc says "free %", code sends "used %") |
| `os.service.status[name]` | — | ❌ **Not implemented** — no service monitoring |
| `os.log.grep[path, pattern]` | — | ❌ **Not implemented** — no log tailing |

### Maximo Monitoring (`monitoring/maximo.md`)

| Doc Feature | Status |
|:---|:---|
| Synthetic UX probe (`ux.scenario.login_flow`) | ❌ **Not implemented** |
| Cron Task Validator (`maximo.cron.stale_count`) | ❌ **Not implemented** |
| Escalation Engine (`maximo.escalation.backlog`) | ❌ **Not implemented** |
| UI Reachability (`net.http.check`) with SSL validation | ❌ **Not implemented** |
| JMX metrics (heap, threads, sessions, cron) | ✅ **Partially implemented** — heap + threads work via `JmxBridge.jar`. Session count (`maximo.web.sessions`) and cron MBean (`maximo.cron.active`) not tested/verified. |

### WebSphere Monitoring (`monitoring/websphere.md`)

| Doc Metric | Status |
|:---|:---|
| `ibm.was.jvm.heap.percent_used` | ❌ **Not implemented** — JMX collector uses `maximo.jvm.heap.used` (different key, raw bytes not %) |
| `ibm.was.jvm.gc.time_spent` | ❌ **Not implemented** |
| `ibm.was.threads.webcontainer.active/max` | ❌ **Not implemented** |
| `ibm.was.jdbc.free_connections` | ❌ **Not implemented** |
| `ibm.was.jdbc.wait_time_ms` | ❌ **Not implemented** |
| `security.cert.expiry_days` (SSL cert probe) | ❌ **Not implemented** |

### DB2 Monitoring (`monitoring/db2.md`)

| Doc Metric | Status |
|:---|:---|
| `ibm.db2.connections.active` | ❌ **Not implemented** — no DB2 collector code exists |
| `ibm.db2.locks.deadlocks` | ❌ **Not implemented** |
| `ibm.db2.tablespace.usage_pct` | ❌ **Not implemented** |
| `ibm.db2.logs.primary_usage` | ❌ **Not implemented** |
| `ibm.db2.maintenance.last_backup_age_hours` | ❌ **Not implemented** |

> **The entire DB2 monitoring module is documented but has zero implementation.** There is no `db2.py` collector, no `ibm_db` dependency in `requirements.txt`, and no DB2-related code anywhere in the codebase.

---

## Category 4: 🟡 MAJOR — Technology Stack Misrepresentations

**File**: `implementation/technology_stack.md`

| Documented Technology | Actual Implementation |
|:---|:---|
| Celery + Redis (distributed task queue) | ❌ **Not used** — alert evaluation is synchronous in the API request cycle |
| RabbitMQ 3.12 (message queue) | ❌ **Not used** — no queue exists |
| PostgreSQL 15 (production DB) | ❌ **Not used** — SQLite only |
| TimescaleDB extension | ❌ **Not used** |
| React 18 + TypeScript + Material-UI (dashboard) | ❌ **Not used** — dashboard is a single `index.html` with Alpine.js + Tailwind CDN |
| Apache ECharts / Plotly.js (charting) | ❌ **Not used** — gauges are hand-coded SVG circles |
| WebSockets (`/ws/realtime`) | ❌ **Not used** — dashboard polls REST API every 5s |
| OAuth2 / SAML 2.0 auth | ❌ **Not used** — no authentication |
| Docker deployment | ❌ **Not used** — PyInstaller EXE packaging only |
| HashiCorp Vault | ❌ **Not used** |
| `cryptography` library (TLS) | ❌ **Not in requirements.txt** |
| `ibm_db` (DB2 driver) | ❌ **Not in requirements.txt** |
| `jpype1` (Java bridge) | ❌ **Not used** — subprocess calls to `java -jar` instead |
| `pywin32` / `wmi` (Windows probes) | ❌ **Not used** |
| JSON Schema config validation | ❌ **Not implemented** |

### Actual Dependencies (`requirements.txt`)
```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
pyyaml
psutil
requests
```

> The documented tech stack describes an enterprise platform with 15+ dependencies. The actual `requirements.txt` has **7 packages**. The gap is extreme.

---

## Category 5: 🟡 MAJOR — Dashboard Gaps

**File**: `platform_config/dashboards.md`

| Dashboard | Doc Status | Implementation |
|:---|:---|:---|
| DASH-001: Operations Dashboard | ✅ Documented as implemented | ✅ **Actually implemented** |
| DASH-002: Executive / CIO View | 🔴 Documented as planned | ❌ Not implemented |
| DASH-003: NOC Operations Center | 🔴 Documented as planned | ❌ Not implemented |
| DASH-004: Engineer / SRE View | 🔴 Documented as planned | ❌ Not implemented |
| DASH-005: Host Drill-Down | ✅ Documented as implemented | ✅ **Actually implemented** |

> DASH-001 and DASH-005 documentation is **accurate** and matches the implementation. This is the strongest alignment in the entire project.

---

## Category 6: 🟡 MAJOR — Alerting Gaps

**File**: `operations/alerting.md`

| Feature | Status |
|:---|:---|
| Severity model (info/warning/critical/very_critical) | ✅ **Implemented** |
| Default alert rules (CPU, Memory, Disk) | ✅ **Implemented** |
| Email notifications (SMTP) for very_critical | ✅ **Implemented** |
| Microsoft Teams Webhooks | ❌ **Not implemented** (correctly marked 🔴 in docs) |
| Escalation Chain (SMS at T+15m, Manager at T+60m) | ❌ **Not implemented** (correctly marked 🔴) |
| Work Hours routing | ❌ **Not implemented** (correctly marked 🔴) |
| Alert Acknowledgment | ❌ **Not implemented** (correctly marked 🔴) |

> **Positive**: The `operations/alerting.md` page is the **best-documented page** in the project. It clearly marks planned vs. implemented features. This pattern should be replicated across all other pages.

---

## Category 7: 🟡 Metric Key Inconsistencies

The documentation uses different metric key names than the actual code:

| Location | Doc Key | Code Key | Impact |
|:---|:---|:---|:---|
| `monitoring/os.md` | `os.cpu.total_usage_pct` | `os.cpu.usage` | Alert rules reference code key, not doc key |
| `monitoring/os.md` | `os.mem.available_mb` | `os.memory.percent` | Completely different metric (MB vs %) |
| `monitoring/os.md` | `os.disk.volume.free_pct` | `os.disk.usage_percent` | Inverted: "free" vs "used" |
| `getting_started.md` | `os.memory.usage_percent` | `os.memory.percent` | Code example differs from implementation |
| `monitoring/websphere.md` | `ibm.was.jvm.heap.percent_used` | `maximo.jvm.heap.used` | Different namespace and unit |
| `operations/alerting.md` | `os.memory.percent` | `os.memory.percent` | ✅ **Correct** |
| `operations/alerting.md` | `os.cpu.usage` | `os.cpu.usage` | ✅ **Correct** |

---

## Category 8: 🔴 MkDocs Rendering Issues

### Broken Navigation Items

| Nav Entry | File Referenced | Issue |
|:---|:---|:---|
| `Documentation Alignment > Implementation Gap` | `tooling/implementation_gap.yaml` | ⚠️ **YAML file** — MkDocs cannot render `.yaml` as a documentation page. Clicking this link will fail or show raw YAML. |
| `Documentation Alignment > Tooling Overview` | `tooling/index.md` | ⚠️ Links to `mcp-server/tools/gap_tracker.py` which is a **relative path from a different directory** — link will 404. |

### Orphaned Pages (exist but not in nav)

The `docs/installation/` directory contains 3 pages not listed in `mkdocs.yml`:
- `installation/core.md`
- `installation/agents.md`
- `installation/collectors.md`

These are **inaccessible through navigation** — users cannot find them unless they know the URL.

### Content Rendering Issues

| Page | Issue |
|:---|:---|
| `operations/runbook.md` | Uses MkDocs `===` tabbed content syntax (`=== "Maximo / WebSphere (Linux)"`) — requires `pymdownx.tabbed` extension which is **not configured** in `mkdocs.yml`. Tabs will render as plain text. |
| `architecture/scaling.md` | Uses Mermaid diagrams (`mermaid` code blocks) — requires `pymdownx.superfences` with Mermaid plugin which is **not configured** in `mkdocs.yml`. Diagrams will render as code blocks. |

---

## Category 9: 🟡 Documentation Internal Contradictions

| Page A | Says | Page B | Says | Conflict |
|:---|:---|:---|:---|:---|
| `getting_started.md` L9 | "PostgreSQL 15+" required | `getting_started.md` L23 | "SQLite for zero-config" | **Same page contradicts itself** |
| `getting_started.md` L20 | "Node.js 18+ for dashboard" | Actual dashboard | Single HTML file, no Node.js | Node.js is not needed |
| `getting_started.md` L39-41 | `web/backend/` + `web/frontend/` (React) | Actual structure | `core/web/static/index.html` | Project structure is wrong |
| `architecture/components.md` L9 | "PostgreSQL (recommended) or MySQL" | `core/config.yaml` | SQLite only | Database choice misrepresented |
| `architecture/components.md` L26 | "internal Go runtime" | All code | Python 3.11 | **Language is completely wrong** — docs say Go, code is Python |
| `architecture/compatibility.md` L20 | "AIX 7.1, 7.2 PowerPC binaries" | Agent code | Python + psutil (no AIX support) | AIX is not supported |
| `architecture/compatibility.md` L17 | "MSI Installer available" | Actual packaging | PyInstaller `.exe` | No MSI installer exists |
| `implementation/technology_stack.md` L33 | "React 18 + TypeScript + Material-UI" | Dashboard | Alpine.js + Tailwind CDN | Completely different stack |
| `implementation/requirements.md` L6 | "proprietary encrypted protocol" | Agent transport | Plain HTTP JSON POST | No proprietary protocol exists |
| `platform_config/metrics.md` L25-33 | "Hysteresis with recovery delta" | Alert engine code | Simple threshold comparison | No hysteresis implemented |

---

## Category 10: Custom Extensions (Probe API)

**File**: `custom_monitoring/scripts.md`

| Feature | Status |
|:---|:---|
| Probe Extension API | ❌ **Not implemented** — no `probes` section parsing in agent code |
| `agent_config.json` probes section | ❌ **Not implemented** — `config.json` has no `probes` key |
| PowerShell script execution | ❌ **Not implemented** |
| Bash script execution | ❌ **Not implemented** |

---

## Recommendations (Prioritized)

### 🔴 P0 — Fix Immediately (Misleading for Audits)

1. **`security/hardening.md`**: Rewrite entirely. Add a clear "Current Status" section stating that TLS, authentication, and vault are **not yet implemented**. A client or auditor reading this page would believe the system is secure — it is not.

2. **`architecture/components.md` L26**: Remove "internal Go runtime" — the platform is Python. This is factually incorrect.

3. **`implementation/technology_stack.md`**: Add a "Current State" vs "Target Architecture" split. The page currently presents aspirational tech (Celery, RabbitMQ, React, Redis) as if it exists.

4. **`getting_started.md` L9, L20, L39-41**: Remove PostgreSQL and Node.js prerequisites. Fix the project structure diagram to match reality.

### 🟡 P1 — Fix Before Next Release

5. **`monitoring/os.md`**: Update metric keys to match the actual code (`os.cpu.usage`, `os.memory.percent`, `os.disk.usage_percent`).

6. **`monitoring/db2.md`** and **`monitoring/websphere.md`**: Add clear "🔴 Not Implemented" status markers to every metric, following the pattern used in `operations/alerting.md`.

7. **`mkdocs.yml`**: 
   - Add `pymdownx.tabbed` and `pymdownx.superfences` extensions for tab and mermaid rendering.
   - Change `tooling/implementation_gap.yaml` nav entry to link to the `tooling/index.md` page instead.
   - Add the 3 orphaned `installation/*.md` pages to the nav.

8. **`maintenance/backup_dr.md`**: Mark all content as "Planned" — the `esol-admin` tool and S3 backup do not exist.

### 🟢 P2 — Improvement

9. **Adopt the `alerting.md` pattern everywhere**: Every page should have a "Implemented ✅ / Planned 🔴" status column. This page is the gold standard.

10. **`implementation/python_guide.md`**: Update code examples to match actual `core/api/main.py`, `core/engine/alerts.py`, and `agent/agent.py`. The documented code examples use classes and patterns (e.g., `MetricsEngine`, async/await, `CollectorClient`) that do not exist.

---

## Summary Scorecard

| Documentation Area | Accuracy Score | Notes |
|:---|:---:|:---|
| `operations/alerting.md` | **9/10** | ✅ Best page. Honest status markers. |
| `platform_config/dashboards.md` | **8/10** | ✅ Good. Clear "Planned" section. |
| `deployment_guide.md` | **7/10** | ✅ Mostly accurate for Tier 1 MVP. |
| `getting_started.md` | **5/10** | ⚠️ Contradictions (PostgreSQL vs SQLite). |
| `monitoring/maximo.md` | **4/10** | ⚠️ JMX partially works. Synthetic probes don't. |
| `architecture/overview.md` | **3/10** | 🔴 Collectors don't exist. Network flow is wrong. |
| `security/hardening.md` | **1/10** | 🔴 Nothing described is implemented. |
| `implementation/technology_stack.md` | **1/10** | 🔴 Almost entirely aspirational. |
| `implementation/python_guide.md` | **1/10** | 🔴 Code examples don't match any real file. |
| `architecture/compatibility.md` | **2/10** | 🔴 Claims AIX, RPM, DEB, MSI, Go runtime — none exist. |
| `maintenance/backup_dr.md` | **1/10** | 🔴 Entire page is fiction. |
| `monitoring/db2.md` | **0/10** | 🔴 Zero implementation. No code, no driver. |
| `monitoring/websphere.md` | **1/10** | 🔴 Metric keys don't match. Most not collected. |

**Overall Documentation Accuracy: ~30%**  
Only 3 of 27 pages can be considered reliable.
