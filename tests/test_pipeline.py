import json
from pathlib import Path

from project_scout.cli import main, validate_handoff
from project_scout.io import load_evidence
from project_scout.normalization import normalize_records
from project_scout.scoring import score_opportunities

FIXTURE = Path(__file__).parent / "fixtures" / "evidence.json"


def test_normalization_removes_duplicate_and_preserves_provenance():
    records = normalize_records(load_evidence(FIXTURE))
    assert len(records) == 3
    assert {record.source for record in records} == {"reddit", "hackernews", "github"}


def test_scoring_is_deterministic():
    records = normalize_records(load_evidence(FIXTURE))
    candidates = [{"problem": "Automated release documentation", "theme": "automation", "evidence_urls": [r.url for r in records], "rationale": "fixture"}]
    assert score_opportunities(candidates, records) == score_opportunities(candidates, records)


def test_full_validation_rejects_nested_contract_errors():
    assert any("opportunity.title" in error for error in validate_handoff({"schema_version": "opportunity-handoff/v1", "opportunity": {}, "scores": {}, "evidence": []}))


def test_offline_e2e_writes_planner_consumable_artifacts(tmp_path):
    output_dir, manifest, report = tmp_path / "handoffs", tmp_path / "bundle.json", tmp_path / "report.md"
    assert main(["run", "--input", str(FIXTURE), "--output-dir", str(output_dir), "--manifest-output", str(manifest), "--markdown-output", str(report)]) == 0
    bundle = json.loads(manifest.read_text())
    assert len(bundle["artifacts"]) >= 1
    for artifact in bundle["artifacts"]:
        path = Path(artifact["path"])
        assert main(["validate", "--input", str(path)]) == 0
        data = json.loads(path.read_text())
        assert data["schema_version"] == "opportunity-handoff/v1"
        assert data["opportunity"]["title"] in report.read_text()
