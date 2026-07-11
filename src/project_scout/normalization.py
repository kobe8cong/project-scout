from __future__ import annotations

import re
from collections.abc import Iterable

from .models import EvidenceRecord


def normalize_records(records: Iterable[EvidenceRecord]) -> list[EvidenceRecord]:
    """Normalize whitespace and remove duplicates without discarding provenance."""
    result: list[EvidenceRecord] = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        title = " ".join(record.title.split())
        content = " ".join(record.content.split())
        url = record.url.strip()
        fingerprint = (url, " ".join(f"{title} {content}".lower().split()))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        result.append(EvidenceRecord(
            source=record.source.lower().strip() or "unknown",
            title=title or "Untitled",
            content=content,
            url=url,
            created_at=record.created_at,
            engagement=max(0, int(record.engagement)),
            source_id=record.source_id,
            tags=tuple(sorted({tag.lower().strip() for tag in record.tags if tag.strip()})),
        ))
    return result


def topic_key(text: str) -> str:
    words = re.findall(r"[a-z0-9]{4,}", text.lower())
    stop = {"that", "this", "with", "from", "have", "there", "would", "should", "need", "want", "tool"}
    useful = [word for word in words if word not in stop]
    return " ".join(useful[:5]) or "general"
