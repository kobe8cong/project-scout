from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import EvidenceRecord, Handoff, Opportunity


def load_evidence(path: Path) -> list[EvidenceRecord]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    entries = [item for value in raw.values() if isinstance(value, list) for item in value] if isinstance(raw, dict) else raw
    records = []
    for item in entries:
        if not isinstance(item, dict): continue
        engagement = item.get("engagement")
        if engagement is None:
            engagement = int(item.get("upvotes", item.get("points", item.get("reactions", 0)))) + int(item.get("comments", 0))
        records.append(EvidenceRecord(source=str(item.get("source", "unknown")), title=str(item.get("title", "Untitled")), content=str(item.get("content", "")), url=str(item.get("url", "")), created_at=str(item.get("created_at", "")), engagement=int(engagement), source_id=str(item.get("id", "")), tags=tuple(str(x) for x in item.get("labels", item.get("tags", [])))))
    return records


def write_outputs(handoffs: list[Handoff], output_dir: Path, manifest_path: Path, markdown_path: Path, extractor: str, focus: str | None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for handoff in handoffs:
        path = output_dir / f"{handoff.identifier}.json"
        path.write_text(json.dumps(handoff.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        artifacts.append({"opportunity_id": handoff.identifier, "path": str(path)})
    manifest = {"bundle_version": "project-scout-bundle/v1", "extractor": extractor, "focus": focus, "artifacts": artifacts}
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    opportunities = [handoff.opportunity for handoff in handoffs]
    lines = ["# Project Scout Report", "", f"Extractor: `{extractor}`", "", f"Opportunities: {len(opportunities)}", ""]
    for number, item in enumerate(opportunities, 1):
        lines.extend([f"## {number}. {item.problem}", "", f"- Theme: {item.theme}", f"- Market gap score: {item.market_gap_score}/100", f"- Demand score: {item.demand_score}/100", f"- Competition proxy: {item.competition_score}/100", f"- Rationale: {item.rationale}", ""])
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
