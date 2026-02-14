# Gap Analysis Tools

This section documents the custom tooling used to maintain alignment between documentation and implementation.

## Implementation Gap Tracker

The `gap_tracker.py` tool scans the documentation and compares it against the codebase status defined in `implementation_gap.yaml`.

### Key Files

| File | Location | Description |
| :--- | :--- | :--- |
| Gap Analysis Report | `docs/gap_analysis_report.md` | Latest audit of documentation vs implementation |
| Implementation Gap YAML | `EsMonitorDocs/implementation_gap.yaml` | Machine-readable gap definitions |
| Gap Tracker Script | `EsMonitorDocs/mcp-server/tools/gap_tracker.py` | Python script that analyzes gaps |

### Usage

Run the tracker from the project root:

```powershell
python EsMonitorDocs/mcp-server/tools/gap_tracker.py --stats
python EsMonitorDocs/mcp-server/tools/gap_tracker.py --next
```

### Purpose

Ensures that every feature documented in MkDocs has a corresponding tracking status in `implementation_gap.yaml`. The tracker helps identify:

- Features documented but not implemented
- Features implemented but not documented
- Metric key mismatches between docs and code
- Missing status markers on documentation pages

### Related

- [Gap Analysis Report](../gap_analysis_report.md) — Full audit results
