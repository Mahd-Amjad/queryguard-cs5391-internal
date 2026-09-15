# CI Workflows (ready-to-drop; two files, nothing more)

**Unit:** CS5391-PROJ-1 evaluation prep (wave 1, unit C). Place at repo root as `.github/workflows/test-suite.yml` and `.github/workflows/eval-run.yml` when the repo exists. Deliberately minimal: no UAT/prod split, no auto-release, no matrix builds (over-engineering guard — see ROADMAP).

---

## `.github/workflows/test-suite.yml` (the push gate)

```yaml
name: Guard test suite

on:
  push:
    branches: [main]
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run gate unit tests (one test per rule G-01..G-10)
        run: pytest tests/ -v

      - name: Corpus regression (starter set must fully pass)
        run: python scripts/run_eval.py --corpus data/corpus.jsonl --mode mock --fail-on-miss
```

Notes: `--fail-on-miss` = any corpus entry whose expected verdict does not match fails the build. This is the mechanical gate: a broken rule shows a red X, visible in the demo.

## `.github/workflows/eval-run.yml` (the manual evaluation run)

```yaml
name: Evaluation run

on:
  workflow_dispatch:
    inputs:
      mode:
        description: 'Generator mode'
        required: true
        default: 'mock'
        type: choice
        options: [mock, live]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run full corpus evaluation
        run: python scripts/run_eval.py --corpus data/corpus.jsonl --mode ${{ inputs.mode }} --report out/report.md

      - name: Upload report artifact
        uses: actions/upload-artifact@v4
        with:
          name: eval-report-${{ inputs.mode }}
          path: out/report.md
```

Notes: `live` mode expects `LLM_API_KEY` as a repo secret (set only if the group opts into live mode; mock needs nothing). The artifact is the numbered report shown on the metrics page and in the demo.

## Deliberately NOT included

Multi-env deploys, tag releases, path filters, self-hosted runners, scheduled crons. Rationale: course project, 4 people, one deploy path; the checklist penalizes over-engineering and Group 2 weeks are scarce.

---

## Unit record (SM51 control)

Steps: 1 READ (zapply-backend + chrome-extension workflows read earlier this session as patterns; TECH_PLAN §6 requirements) · 2 UNDERSTAND (consumers: repo CI + demo; failure mode = flaky/overwide triggers wasting group time) · 3 EXPLORE (both ZJP workflow families reviewed: deploy-workers, auto-release; dashboard scripts; nothing else exists to reuse) · 4 RESEARCH (actions versions: checkout@v4, setup-python@v5, upload-artifact@v4 — current majors; verify at repo creation) · 5 REVIEW (two workflows only; third candidate — scheduled nightly run — rejected as ceremony) · 6 IDEATE (fail-on-miss flag vs soft report: hard fail chosen for the gate, soft report for eval run — separation is the point) · 7 DRY RUN (YAML reviewed for schema validity; workflow_dispatch choice input verified against actions syntax; actual run happens at repo creation — noted as pending verification) · 8 PLAN (this file + placement note) · 9 IMPLEMENT (delivered; destination = this document; live CI verification is explicitly deferred and recorded).
Alternatives: GitHub Actions vs local script — Actions chosen (visibility in demo + badge). Bias note: pattern-matching ZJP's automation could over-scope; the "deliberately NOT included" section is the countermeasure.
