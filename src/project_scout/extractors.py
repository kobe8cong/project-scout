from __future__ import annotations

from collections import defaultdict
from typing import Protocol

from .models import EvidenceRecord
from .normalization import topic_key


class Extractor(Protocol):
    name: str

    def extract(self, evidence: list[EvidenceRecord]) -> list[dict[str, object]]: ...


class RuleBasedExtractor:
    """Deterministic extractor used by default and in offline workflows."""

    name = "rules"
    INDICATORS = ("wish", "need", "looking for", "missing", "frustrat", "annoy", "waste", "why isn't there", "would pay")
    THEMES = {
        "automation": ("automate", "automation", "workflow", "script"),
        "developer-productivity": ("developer", "code", "git", "api", "documentation"),
        "collaboration": ("team", "collaborate", "share"),
        "productivity": ("productive", "efficient", "time", "manual"),
    }

    def extract(self, evidence: list[EvidenceRecord]) -> list[dict[str, object]]:
        groups: dict[str, list[EvidenceRecord]] = defaultdict(list)
        for record in evidence:
            text = record.canonical_text()
            if any(indicator in text for indicator in self.INDICATORS):
                groups[self._theme(text)].append(record)
        return [
            {
                "problem": self._problem(theme, records),
                "theme": theme,
                "evidence_urls": [record.url for record in records if record.url],
                "rationale": f"{len(records)} normalized evidence records indicate recurring {theme} demand.",
            }
            for theme, records in sorted(groups.items())
        ]

    def _theme(self, text: str) -> str:
        for theme, keywords in self.THEMES.items():
            if any(keyword in text for keyword in keywords):
                return theme
        return topic_key(text)

    @staticmethod
    def _problem(theme: str, records: list[EvidenceRecord]) -> str:
        return records[0].title if records else f"Unmet {theme} need"


class ClaudeSemanticExtractor:
    """Semantic extraction through the official Anthropic Python SDK.

    This path is explicit so offline runs never instantiate a network client.
    """

    name = "claude"

    def __init__(self, client: object | None = None) -> None:
        self._client = client

    def extract(self, evidence: list[EvidenceRecord]) -> list[dict[str, object]]:
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        payload = [{"url": item.url, "source": item.source, "title": item.title, "content": item.content} for item in evidence]
        schema = {
            "type": "object",
            "properties": {"opportunities": {"type": "array", "items": {"type": "object", "properties": {"problem": {"type": "string"}, "theme": {"type": "string"}, "evidence_urls": {"type": "array", "items": {"type": "string"}}, "rationale": {"type": "string"}}, "required": ["problem", "theme", "evidence_urls", "rationale"], "additionalProperties": False}}},
            "required": ["opportunities"],
            "additionalProperties": False,
        }
        response = self._client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            output_config={"effort": "high", "format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content": "Extract distinct, evidence-grounded project opportunities. Do not invent sources. Input:\n" + __import__("json").dumps(payload, ensure_ascii=False)}],
        )
        import json
        text = next(block.text for block in response.content if block.type == "text")
        return json.loads(text)["opportunities"]
