# Project Methodology

eSolutions follows a rigid 4-phase implementation methodology to ensure zero-downtime deployment.

## Phase 1: Discovery & Design (Week 1)
*   **Asset Inventory**: Cataloging all Maximo JVMs, HTTP Servers, and DB Nodes.
*   **Network Mapping**: Verifying connectivity between Zones (App, DB, Mgmt).
*   **Metric Definition**: Workshops with App Owners to define "Critical" vs "Warning" thresholds.
*   **Output**: *Solution Design Document (SDD)*.

## Phase 2: Core Build (Week 2)
*   Deploy **eSolutions Monitoring Core** in the Management Zone.
*   Configure High Availability (Active/Standby) if required.
*   Deploy **Collectors** in the DMZ and Secure Zones.
*   Establish secure SSL tunnels between Connectors and Core.

## Phase 3: Agent Rollout (Week 3)
*   **Pilot Group**: Deploy Agents to Non-Prod environment first.
*   **Validation**: Verify metric ingestion integrity.
*   **Mass Rollout**: Use Ansible/SCCM to push Agents to Production.
*   **Plugin Activation**: Enable `MaximoProbe` and `DB2Probe` modules.

## Phase 4: Tuning & Handover (Week 4)
*   **Threshold Tuning**: Adjust sensitivity to eliminate false positives.
*   **Dashboard Creation**: Build role-based views (Mgmt, Ops, DB Team).
*   **Training**: Conduct "Train the Trainer" session for the NOC team.
*   **Sign-off**: Go-Live.
