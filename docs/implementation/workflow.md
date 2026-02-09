# Implementation Workflow

This section provides a detailed breakdown of the implementation activities.

## Pre-Implementation (1 Week Before Kickoff)

### Stakeholder Identification
*   **Sponsor**: IT Director / CIO.
*   **Technical Lead**: Maximo System Administrator.
*   **Network Team**: Firewall change approvals.
*   **Security Team**: Certificate provisioning and security review.

### Environment Preparation Checklist
- [ ] VM provisioning completed (Core, Collectors).
- [ ] Firewall rules submitted for approval.
- [ ] Service accounts created in Active Directory.
- [ ] Database server access granted.

## Phase 1: Discovery & Design (Week 1)

### Day 1-2: Asset Inventory
*   **Tool**: Automated discovery using `nmap`, `Ansible Facts`, or existing CMDB.
*   **Output**: Excel spreadsheet listing:
    *   Hostname
    *   IP Address
    *   OS Type/Version
    *   Installed Applications (Maximo, WAS, DB2)
    *   Current Monitoring Status

### Day 3-4: Network & Security Review
*   **Activity**: Review firewall logs to identify current traffic patterns.
*   **Workshop**: 2-hour session with Network and Security teams.
*   **Deliverable**: Network diagram with proposed monitoring zones.

### Day 5: Metric Definition Workshop
*   **Attendees**: Maximo App Owner, DBA, NOC Manager.
*   **Goal**: Define SLA thresholds (e.g., "Maximo login must complete in < 3 seconds").
*   **Output**: Threshold Matrix (Google Sheets or Confluence).

## Phase 2: Core Build (Week 2)

### Day 1: Database Setup
```bash
# PostgreSQL Installation
dnf install postgresql15-server postgresql15-contrib
postgresql-setup --initdb
systemctl enable --now postgresql

# TimescaleDB Extension
dnf install timescaledb
timescaledb-tune --yes
```

### Day 2-3: Core Engine Deployment
*   Install eSolutions Core package.
*   Configure `engine.yaml`:
    ```yaml
    database:
      host: db.internal
      name: es_monitor
      pool: 100
    listeners:
      - protocol: tcp
        port: 8443
        tls: true
    ```
*   Start service: `systemctl start esolutions-core`.

### Day 4-5: Collector Deployment
*   Deploy Collectors in DMZ and App Zone.
*   Configure upstream connection to Core.
*   Verify heartbeat in Core logs.

## Phase 3: Agent Rollout (Week 3)

### Day 1: Pilot Deployment (Non-Prod)
*   Target: 5 servers (1 App, 1 DB, 3 Windows).
*   **Method**: Manual installation for troubleshooting.
*   **Validation**: Check `agent.log` for successful handshake.

### Day 2-3: Automation Scripts
*   **Ansible Playbook** (Linux):
    ```yaml
    - name: Deploy eSolutions Agent
      hosts: maximo_linux
      tasks:
        - name: Install RPM
          yum:
            name: /tmp/esolutions-agent.rpm
        - name: Configure Agent
          template:
            src: agent_config.j2
            dest: /etc/esolutions/agent.conf
    ```
*   **SCCM Package** (Windows): Create MSI deployment with config JSON.

### Day 4-5: Production Rollout
*   Phased deployment: 20% → 50% → 100%.
*   Monitor Core CPU/Memory during rollout.

## Phase 4: Tuning & Handover (Week 4)

### Day 1-2: Threshold Tuning
*   Review false positive alerts from Week 3.
*   Adjust trigger sensitivity (e.g., "CPU > 90% for 10 min" → "15 min").

### Day 3: Dashboard Creation
*   Build 3 dashboards (Executive, Ops, Engineer).
*   Publish to stakeholder group for feedback.

### Day 4: Training Session
*   **Duration**: 2 hours.
*   **Topics**: 
    *   Dashboard navigation.
    *   Alert acknowledgment.
    *   Basic troubleshooting (restart agent).

### Day 5: Go-Live & Sign-Off
*   Conduct final health check.
*   Obtain sign-off from Sponsor.
*   Transition to BAU (Business As Usual) support.
