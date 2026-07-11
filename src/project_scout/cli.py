from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from .extractors import ClaudeSemanticExtractor, RuleBasedExtractor
from .io import load_evidence, write_outputs
from .models import DIMENSIONS, Handoff
from .normalization import normalize_records
from .scoring import score_opportunities


def run(args: argparse.Namespace) -> int:
    evidence = normalize_records(load_evidence(Path(args.input)))
    extractor = ClaudeSemanticExtractor() if args.extractor == "claude" else RuleBasedExtractor()
    opportunities = score_opportunities(extractor.extract(evidence), evidence)
    handoffs = [Handoff(item, f"opp-{index:03d}-{_slug(item.theme)}") for index, item in enumerate(opportunities, 1)]
    write_outputs(handoffs, Path(args.output_dir), Path(args.manifest_output), Path(args.markdown_output), extractor.name, args.focus)
    print(f"Wrote {len(handoffs)} Planner-compatible handoffs to {args.output_dir}; manifest: {args.manifest_output}.")
    return 0


def validate(args: argparse.Namespace) -> int:
    errors = validate_handoff(json.loads(Path(args.input).read_text(encoding="utf-8")))
    if errors:
        print("Invalid handoff:\n- " + "\n- ".join(errors)); return 1
    print("Handoff is valid opportunity-handoff/v1."); return 0


def validate_handoff(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict): return ["handoff must be an object"]
    if data.get("schema_version") != "opportunity-handoff/v1": errors.append("schema_version must equal opportunity-handoff/v1")
    opportunity = data.get("opportunity")
    if not isinstance(opportunity, dict): errors.append("opportunity must be an object")
    else:
        for field in ("id", "title", "problem", "target_user", "proposed_solution"):
            if not isinstance(opportunity.get(field), str) or not opportunity[field].strip(): errors.append(f"opportunity.{field} must be a non-empty string")
    scores = data.get("scores")
    if not isinstance(scores, dict): errors.append("scores must be an object")
    else:
        for dimension in DIMENSIONS:
            score = scores.get(dimension)
            if not isinstance(score, dict): errors.append(f"scores.{dimension} must be an object"); continue
            value, confidence = score.get("score"), score.get("confidence")
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100): errors.append(f"scores.{dimension}.score must be null or 0..100")
            if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1: errors.append(f"scores.{dimension}.confidence must be 0..1")
            if not isinstance(score.get("rationale"), str) or not score["rationale"].strip(): errors.append(f"scores.{dimension}.rationale must be a non-empty string")
            if value is None and score.get("unknown") is not True: errors.append(f"scores.{dimension}.unknown must be true when score is null")
    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence: errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict): errors.append(f"evidence[{index}] must be an object"); continue
            for field in ("id", "claim", "source", "observed_at"):
                if not isinstance(item.get(field), str) or not item[field].strip(): errors.append(f"evidence[{index}].{field} must be a non-empty string")
    return errors


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "opportunity"


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="project-scout"); commands = root.add_subparsers(dest="command", required=True)
    p = commands.add_parser("run"); p.add_argument("--input", required=True); p.add_argument("--extractor", choices=("rules", "claude"), default="rules"); p.add_argument("--focus"); p.add_argument("--output-dir", default="project-scout-handoffs"); p.add_argument("--manifest-output", default="project-scout-bundle.json"); p.add_argument("--markdown-output", default="project-scout-report.md"); p.set_defaults(handler=run)
    p = commands.add_parser("validate"); p.add_argument("--input", required=True); p.set_defaults(handler=validate)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv); return args.handler(args)


if __name__ == "__main__": raise SystemExit(main())
