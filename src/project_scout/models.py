from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

DIMENSIONS = ("demand", "competition", "feasibility", "differentiation", "ecosystem_value")


@dataclass(frozen=True)
class EvidenceRecord:
    source: str
    title: str
    content: str
    url: str = ""
    created_at: str = ""
    engagement: int = 0
    source_id: str = ""
    tags: tuple[str, ...] = ()

    def canonical_text(self) -> str:
        return " ".join(f"{self.title} {self.content}".lower().split())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self); data["tags"] = list(self.tags); return data


@dataclass(frozen=True)
class Opportunity:
    problem: str
    theme: str
    evidence: tuple[EvidenceRecord, ...]
    demand_score: int
    competition_score: int
    market_gap_score: int
    rationale: str


@dataclass(frozen=True)
class Handoff:
    opportunity: Opportunity
    identifier: str

    def to_dict(self) -> dict[str, Any]:
        item = self.opportunity
        evidence = [{
            "id": record.source_id or f"{self.identifier}-e{index}",
            "claim": f"{record.title}: {record.content}" if record.content else record.title,
            "source": record.source, "url": record.url,
            "observed_at": record.created_at or "unknown (offline fixture)",
            "strength": "strong" if record.engagement >= 30 else "moderate" if record.engagement >= 10 else "weak",
            "limitations": "Offline supplied evidence; source was not independently refreshed.",
        } for index, record in enumerate(item.evidence, 1)]
        return {
            "schema_version": "opportunity-handoff/v1",
            "opportunity": {"id": self.identifier, "title": item.problem, "problem": item.problem,
                "target_user": f"People affected by the {item.theme} problem",
                "proposed_solution": f"Build and validate a focused {item.theme} tool addressing this evidence-backed need.",
                "constraints": ["Validate live competition before implementation"]},
            "scores": {
                "demand": _score(item.demand_score, .8, item.rationale),
                "competition": _score(item.competition_score, .45, "Deterministic offline competition proxy; validate with live research."),
                "feasibility": _score(None, 0, "Implementation feasibility was not measured by Scout.", True),
                "differentiation": _score(item.market_gap_score, .5, "Derived from demand and the offline competition proxy."),
                "ecosystem_value": _score(None, 0, "Ecosystem value requires Product Planner analysis.", True)},
            "evidence": evidence,
            "assumptions": ["Supplied evidence is representative of current demand."],
            "unknowns": ["Implementation feasibility", "Ecosystem value", "Live competitor quality"],
            "metadata": {"producer": "project-scout", "market_gap_score": item.market_gap_score},
        }


def _score(value: int | None, confidence: float, rationale: str, unknown: bool = False) -> dict[str, Any]:
    result = {"score": value, "confidence": confidence, "rationale": rationale}
    if unknown: result["unknown"] = True
    return result
