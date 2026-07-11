"""Legacy compatibility wrapper for the Project Scout CLI."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_scout.cli import main


if __name__ == "__main__":
    raise SystemExit(main([
        "run",
        "--input", str(ROOT / "scraped_data.json"),
        "--output-dir", str(ROOT / "project-scout-handoffs"),
        "--manifest-output", str(ROOT / "project-scout-bundle.json"),
        "--markdown-output", str(ROOT / "project-scout-report.md"),
    ]))
