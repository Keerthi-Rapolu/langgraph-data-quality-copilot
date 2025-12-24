from __future__ import annotations
from typing import Any, Dict
from pathlib import Path
import json
from datetime import datetime

def write_markdown_report(profile: Dict[str, Any], rules: Dict[str, Any], validation: Dict[str, Any], out_path: str) -> str:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(f"# Data Quality Report")
    lines.append(f"- Generated: {now}")
    lines.append("")
    lines.append("## Dataset Profile")
    lines.append(f"- Row count: **{profile.get('row_count')}**")
    lines.append("")
    lines.append("### Columns")
    for col, stats in profile.get("columns", {}).items():
        lines.append(f"- **{col}** ({stats.get('type')}): nulls={stats.get('nulls')}, distinct={stats.get('distinct')}")
    lines.append("")
    lines.append("## Proposed Rules (LLM)")
    lines.append("```json")
    lines.append(json.dumps(rules, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Validation Results")
    lines.append(f"- Failed rules: **{validation.get('failed_rules')}**")
    lines.append("")
    for r in validation.get("results", []):
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        lines.append(f"- {status} **{r['name']}** ({r['type']}) on `{r['column']}` — failed_rows={r['failed_rows']}")
        lines.append(f"  - {r['detail']}")

    p.write_text("\n".join(lines), encoding="utf-8")
    return str(p)
