# eSolutions Development Workflow
# Documentation ↔ Implementation Continuous Alignment

## Workflow Steps

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. Docs     │────>│ 2. Gap       │────>│ 3. AI       │────>│ 4. Feature   │────>│ 5. Update    │
│  Updated     │     │ Tracker Run  │     │ Recommends  │     │ Implemented  │     │ gap.yaml     │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘     └──────┬───────┘
                                                                                         │
                                                                                         └──> Loop
```

### Step 1: Documentation Updated
A new feature is described in `EsMonitorDocs/docs/`.

### Step 2: Gap Tracker Executed
Run the tracker to detect the new gap:
```powershell
python EsMonitorDocs/mcp-server/tools/gap_tracker.py --stats
python EsMonitorDocs/mcp-server/tools/gap_tracker.py --next
```

### Step 3: AI Suggests Next Feature
The MCP system prompt ensures the AI always recommends the highest-priority missing feature.

### Step 4: Feature Implemented
Engineer (with AI assistance) writes the code.

### Step 5: Gap File Updated
Update `implementation_gap.yaml`:
```yaml
- id: ALERT-002
  status: implemented    # Changed from 'missing'
```

## CLI Reference

| Command | Description |
| :--- | :--- |
| `python gap_tracker.py` | List all missing/partial features |
| `python gap_tracker.py --next` | Show highest-priority next feature |
| `python gap_tracker.py --stats` | Show implementation statistics |
| `python gap_tracker.py --priority critical` | Filter by priority |
| `python gap_tracker.py --validate` | Check doc references exist |
| `python gap_tracker.py --status partial` | Filter by status |
