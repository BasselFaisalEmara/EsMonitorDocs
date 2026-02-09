"""
eSolutions Monitoring Platform — Gap Tracker Tool
MCP Server Integration for Documentation ↔ Implementation Alignment.

Responsibilities:
  - Load implementation_gap.yaml
  - Scan docs folder for referenced files
  - Output next missing features sorted by priority
  - Ignore implemented items

Usage:
  python gap_tracker.py                    # Show all missing/partial features
  python gap_tracker.py --priority critical # Filter by priority
  python gap_tracker.py --next             # Show single highest-priority item
  python gap_tracker.py --stats            # Show summary statistics
"""

import yaml
import os
import sys
import argparse
from pathlib import Path

# Resolve paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
GAP_FILE = PROJECT_ROOT / "EsMonitorDocs" / "docs" / "tooling" / "implementation_gap.yaml"
DOCS_DIR = PROJECT_ROOT / "EsMonitorDocs" / "docs"

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def load_gap_file() -> list:
    """Load and parse implementation_gap.yaml"""
    if not GAP_FILE.exists():
        print(f"ERROR: Gap file not found at {GAP_FILE}")
        sys.exit(1)

    with open(GAP_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("features", [])


def validate_doc_references(features: list) -> list:
    """Check that documentation_reference paths actually exist in docs/"""
    warnings = []
    for feat in features:
        doc_ref = feat.get("documentation_reference")
        if doc_ref:
            doc_path = DOCS_DIR / doc_ref
            if not doc_path.exists():
                warnings.append(
                    f"  WARNING: {feat['id']} references '{doc_ref}' but file not found at {doc_path}"
                )
    return warnings


def filter_actionable(features: list) -> list:
    """Return only missing or partial features, sorted by priority"""
    actionable = [
        f for f in features if f.get("status") in ("missing", "partial", "planned")
    ]
    actionable.sort(key=lambda x: PRIORITY_ORDER.get(x.get("priority", "low"), 99))
    return actionable


def get_next_feature(features: list) -> dict:
    """Return the single highest-priority unimplemented feature"""
    actionable = filter_actionable(features)
    return actionable[0] if actionable else None


def get_stats(features: list) -> dict:
    """Return summary statistics"""
    stats = {"total": len(features), "implemented": 0, "partial": 0, "missing": 0, "planned": 0}
    by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for f in features:
        status = f.get("status", "missing")
        stats[status] = stats.get(status, 0) + 1
        if status in ("missing", "partial"):
            prio = f.get("priority", "low")
            by_priority[prio] = by_priority.get(prio, 0) + 1

    stats["actionable_by_priority"] = by_priority
    return stats


def format_feature(feat: dict) -> str:
    """Format a single feature for display"""
    lines = [
        f"  ID:       {feat['id']}",
        f"  Name:     {feat['name']}",
        f"  Status:   {feat['status'].upper()}",
        f"  Priority: {feat['priority'].upper()}",
        f"  Doc:      {feat.get('documentation_reference', 'N/A')}",
        f"  Code:     {feat.get('code_reference', 'N/A')}",
        f"  Notes:    {feat.get('notes', '')}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="eSolutions Gap Tracker")
    parser.add_argument("--priority", choices=["critical", "high", "medium", "low"],
                        help="Filter by priority level")
    parser.add_argument("--next", action="store_true",
                        help="Show only the next highest-priority feature")
    parser.add_argument("--stats", action="store_true",
                        help="Show summary statistics")
    parser.add_argument("--validate", action="store_true",
                        help="Validate documentation references exist")
    parser.add_argument("--status", choices=["missing", "partial", "implemented", "planned"],
                        help="Filter by status")
    args = parser.parse_args()

    features = load_gap_file()

    # Validate doc references
    if args.validate:
        warnings = validate_doc_references(features)
        if warnings:
            print("Documentation Reference Validation:")
            for w in warnings:
                print(w)
        else:
            print("All documentation references are valid.")
        return

    # Stats mode
    if args.stats:
        stats = get_stats(features)
        print("=" * 50)
        print("eSolutions Implementation Gap — Statistics")
        print("=" * 50)
        print(f"  Total Features:    {stats['total']}")
        print(f"  Implemented:       {stats['implemented']}")
        print(f"  Partial:           {stats['partial']}")
        print(f"  Missing:           {stats['missing']}")
        print(f"  Planned:           {stats['planned']}")
        print()
        print("  Actionable by Priority:")
        for prio, count in stats["actionable_by_priority"].items():
            print(f"    {prio.upper():10s} {count}")
        return

    # Next feature mode
    if args.next:
        feat = get_next_feature(features)
        if feat:
            print("=" * 50)
            print("NEXT RECOMMENDED FEATURE TO IMPLEMENT")
            print("=" * 50)
            print(format_feature(feat))
        else:
            print("All features are implemented.")
        return

    # List mode (default)
    actionable = filter_actionable(features)

    if args.priority:
        actionable = [f for f in actionable if f.get("priority") == args.priority]

    if args.status:
        actionable = [f for f in features if f.get("status") == args.status]

    print("=" * 50)
    print(f"eSolutions Implementation Gap — {len(actionable)} items")
    print("=" * 50)

    current_priority = None
    for feat in actionable:
        prio = feat.get("priority", "low")
        if prio != current_priority:
            current_priority = prio
            print(f"\n--- {prio.upper()} PRIORITY ---")
        print()
        print(format_feature(feat))
        print()


if __name__ == "__main__":
    main()
