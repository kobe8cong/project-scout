---
name: project-scout
description: Analyze supplied evidence with the local Project Scout CLI. Use offline fixtures by default; only use Claude extraction when explicitly requested and credentials are available.
---

Run the local pipeline from the repository root:

```bash
project-scout run --input tests/fixtures/evidence.json
project-scout validate --input project-scout-handoffs/opp-001-automation.json
```

`run` writes one Planner-compatible `opportunity-handoff/v1` JSON per opportunity plus `project-scout-bundle.json` and a Markdown report.

For semantic extraction, opt in explicitly:

```bash
project-scout run --input evidence.json --extractor claude
```

The CLI creates JSON and Markdown from the same `Handoff` model. Do not claim live-source data was collected when using an offline input.
