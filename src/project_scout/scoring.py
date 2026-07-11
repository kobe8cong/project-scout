from __future__ import annotations

from collections import defaultdict

from .models import EvidenceRecord, Opportunity


def score_opportunities(candidates: list[dict[str, object]], evidence: list[EvidenceRecord]) -> list[Opportunity]:
    by_url = {record.url: record for record in evidence if record.url}
    opportunities: list[Opportunity] = []
    for candidate in candidates:
        selected = tuple(by_url[url] for url in candidate.get("evidence_urls", []) if url in by_url)
        if not selected:
            theme = str(candidate["theme"])
            selected = tuple(record for record in evidence if theme in record.canonical_text())[:3]
        sources = len({record.source for record in selected})
        volume = len(selected)
        engagement = sum(record.engagement for record in selected)
        demand = min(100, volume * 20 + sources * 10 + min(30, engagement // 10))
        # Offline fixtures have no live competitor lookup; use an explicit, stable proxy.
        competition = min(90, max(10, 70 - sources * 10 - volume * 5))
        gap = round(demand * (100 - competition) / 100)
        opportunities.append(Opportunity(
            problem=str(candidate["problem"]),
            theme=str(candidate["theme"]),
            evidence=selected,
            demand_score=demand,
            competition_score=competition,
            market_gap_score=gap,
            rationale=str(candidate["rationale"]),
        ))
    return sorted(opportunities, key=lambda item: (-item.market_gap_score, item.problem.lower()))
