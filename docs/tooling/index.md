# Gap Analysis Tools

This section documents the custom tooling used to maintain alignment between documentation and implementation.

## Implementation Gap Tracker

The `gap_tracker.py` tool scans the documentation and compares it against the codebase status defined in `implementation_gap.yaml`.

### Key Files

- [Implementation Gap Definition (YAML)](implementation_gap.yaml)
- [Gap Tracker Tool (Python Script)](mcp-server/tools/gap_tracker.py)
- [System Prompt](mcp-server/system_prompt.md)
- [Workflow Guide](mcp-server/WORKFLOW.md)

### Usage

Run the tracker from the project root:

```powershell
python EsMonitorDocs/docs/tooling/mcp-server/tools/gap_tracker.py --stats
python EsMonitorDocs/docs/tooling/mcp-server/tools/gap_tracker.py --next
```

### Purpose

Ensures that every feature documented in MkDocs has a corresponding tracking status in `implementation_gap.yaml`.
