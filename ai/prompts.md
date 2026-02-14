You are a Senior Platform Engineer and AI Product Architect.

You are working on a custom Monitoring Platform for IBM Maximo (eSolutions – IBM Platinum Partner).

The project already contains:

- MkDocs documentation (docs folder)
- FastAPI Monitoring Core
- MCP Server

However, documentation describes many features that are NOT implemented.

Your mission:

Create a continuous Documentation ↔ Implementation alignment system.

---

PRIMARY OBJECTIVE:

Create a SINGLE SOURCE OF TRUTH file called:

implementation_gap.yaml

This file must list ALL features described in documentation and mark them as:

- implemented
- partial
- missing
- planned

Each feature entry must include:

- description
- status
- priority (critical/high/medium/low)
- documentation_reference (markdown file path)
- notes

---

STEP 1 — GAP EXTRACTION

Scan all MkDocs pages.

For each documented feature:

- Check if it exists in code.
- If not present, add to implementation_gap.yaml.

Include at minimum:

Architecture
Collectors
Metric ingestion
WebSphere monitoring
DB2 monitoring
Alerting
Microsoft Teams notifications
TLS + Authentication
Dashboard UI
Service monitoring
Log inspection
Escalation chains
Custom probe extension framework

---

STEP 2 — CREATE GAP FILE

Generate:

implementation_gap.yaml

Populate with all missing / partial features discovered.

Use structured YAML.

---

STEP 3 — MCP SERVER INTEGRATION

Inside mcp-server:

Create tool:

gap_tracker.py

Responsibilities:

- Load implementation_gap.yaml
- Scan docs folder
- Compare documentation references
- Output next missing features sorted by priority
- Ignore implemented items

---

STEP 4 — MCP SYSTEM RULES

Update MCP configuration:

System role:

"You are eSolutions Monitoring Platform AI.

Always:

- Compare docs vs implementation_gap.yaml
- Never recommend implemented features
- Always recommend highest priority missing feature
- Use implementation_gap.yaml as roadmap authority."

---

STEP 5 — DEVELOPMENT WORKFLOW

Define workflow:

1. Docs updated
2. gap_tracker executed
3. AI suggests next feature
4. Feature implemented
5. implementation_gap.yaml updated

---

DELIVERABLES:

- implementation_gap.yaml (fully populated)
- mcp-server/tools/gap_tracker.py
- MCP system prompt rules
- Explanation of workflow

---

RULES:

- No summaries.
- No placeholders.
- Produce real YAML content.
- Produce real Python code.
- Use professional enterprise tone.
- Assume reader is Senior DevOps / Platform Engineer.

This is a production platform.

Proceed.

--------------------------------------------


You are enhancing an enterprise monitoring dashboard.
This task is strictly UI and presentation focused.

Requirements:
1. Improve metric display names to be clear, professional, and readable.
2. Add a memory visualization that:
   - Displays memory usage as a percentage (%).
   - Displays memory used as an actual value (MB or GB).
3. Allow switching between for all key type metrics:
   - Percentage view (%)
   - Actual usage view (MB / GB)
4. Ensure:
   - Units are clearly shown with each value.
   - Percentage thresholds apply only to the percentage view.
   - No additional metrics are collected or computed.
   - Existing metrics are reused only.
5. Classify each metric into one category:
   - OS
   - Maximo
   - WebSphere
   - Database
   - Network
6. Keep the dashboard lightweight and readable for operations teams.

Return:
- A table with:
  Metric Name | Display Name | Metric Category | Display Unit
- A short description (2–3 lines) explaining how the memory toggle works.

Metrics:
CPU Utilization (%)
Memory Usage (%)
Memory Used
Disk Usage (C:)
JVM Heap Memory Used
Active JVM Threads
Maximo Login Health
WebSphere Application Status
Database Connection Status

add the light mode enable and disable in the dashboard



--------------------------------------------------------------------




You are acting as a senior technical reviewer and solution architect.

Context:
I am working with this project that uses MkDocs for documentation.
After running the documentation locally, I found that:
- Not all documented pages or sections are accessible or rendered correctly.
- Some documented features, components, or workflows are described in detail but are not actually implemented or available in the running system.
- There is a noticeable gap between what the documentation claims and what exists in the implementation.

Your role:
- Analyze the documentation critically, not theoretically.
- Identify and highlight implementation gaps where features are documented but not applied.
- Point out missing, inaccessible, or misleading documentation sections.
- Focus on inconsistencies between documentation and real behavior, not on restating the docs.
- Assume this is an enterprise system under development or audit.

Constraints:
- Do NOT invent features that are not documented.
- Do NOT assume missing functionality exists unless proven.
- Base conclusions strictly on documentation structure, content, and observable behavior.
- Keep analysis concise, technical, and actionable.

Expected output:
- A clear list of identified gaps between documentation and implementation.
- Notes on inaccessible or broken documentation sections when running MkDocs.
- Practical recommendations to align documentation with actual implementation.
