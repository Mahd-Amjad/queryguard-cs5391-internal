# QueryGuard: project entry point

Safety gate for LLM-generated SQL. CS5391 Group Project 1 (M. Mahd Amjad & Arwa Arafeh).
You ask a question in plain English, an AI drafts the SQL, and a deterministic gate checks
it before anything runs: destructive or snooping queries are blocked, private columns are
masked, and every decision is logged.

## Map (canonical files; superseded material lives in `archive/`)

| File / folder | What it is |
|---|---|
| `prototype/` | **The working app** (Flask + SQLite + sqlglot). Run instructions in `prototype/README.md` |
| `srs/SRS.md` (+ generated .html/.docx) | Software Requirements Specification v1.1 (the GP1 deliverable): user stories, numbered FRs/NFRs, traceability matrix |
| `TECH_PLAN.md` | Design + architecture + rule catalog + phases (§§13-15 are pointers to live files) |
| `DECISIONS.md` | Every design decision with rationale and rejected alternatives (D-001..) |
| `COMPETITION_SCAN.md` | Related work + prior-art scans (3 passes) |
| `QA_CHECKLIST.md` | The gate every unit passes before "done" |
| `proposal/` | Delivered Group Project 1 deck + deck record + theme script |
| `archive/` | Consumed briefs, superseded planning, deck iterations |
| `INDEX.md` | The one file to read first: orientation, canonical map, tools, non-negotiables |
| `CONTINUOUS_IMPROVEMENT.md` | Standing improvement contract (adopted 09-15) |
| `submission/SUBMISSION_CHECKLIST.md` | GP1 submission tracker (11 items) |
| `docs/` | UI/UX reference study + repo-facing docs |
| `group/` | Arwa review copies + answered messages |
| `communications/` | Routed Slack exports (the live chain file lives at the Graduate root) |
| `scripts/` | `repo-sync.sh`: the one push tool (internal + shared repos) |

## State (2026-09-15)

- Gate: 9 rules on a parsed AST; compound SELECTs verified per arm; sensitive-column
  side channels (GROUP BY / ORDER BY / HAVING) blocked; read-only executor; append-only audit.
- Evaluation: 64-entry labeled corpus, verdict-compare harness, metamorphic relations
  (384 checks, all stable), CI workflows committed.
- UI: React SPA (TypeScript + Vite + shadcn/ui + Tailwind + recharts), system-theme default
  with light/dark toggle, served same-origin by Flask from `web/dist`. Pages: Ask, How it
  works, Metrics, Audit log. Frontend tests: vitest + testing-library (16).
- Demo data: enriched clinic (826 rows: 120 patients, 380 appointments incl. a March cluster,
  160 billing, 140 prescriptions); deterministic seed in `data/schema.sql`; audit log reset for
  a clean demo story 09-15 (SM62 visual pass, D-021).
- Tests: 40 backend (pytest; re-verified 09-16 after the D-023 cutover) + 16 frontend (vitest).
- Repos: shared `github.com/Mahd-Amjad/queryguard-cs5391` (whitelisted subset) + internal `queryguard-cs5391-internal` (full tree), both private. One push tool: `scripts/repo-sync.sh` (internal|shared|both).
- Next: SRS presentation Tue Sep 16 (deck READY; informal update). Frontend rebuild SHIPPED 09-15 (section 16, D-023). Review notes fold in as received (not a gate). Remaining: fuzz/hardening unit (subquery-nested-union residual), live-LLM mode (needs operator API key), Project 2 depth.

## Workspace tooling added (2026-09-12)

- `.meta/scripts/lint_sendable.py`: sendable quality gate (incident-grounded rules, selftest PASS; run on anything before it leaves the workspace).
- `.meta/scripts/research.py`: codified GitHub/DDGS research patterns.
- `scripts/md_to_html.py`: branded markdown-to-HTML renderer (SRS mode mirrors into the repo).
- Group comms: `group/SRS_REVIEW.html` (Arwa's review copy), `group/MESSAGE_ARWA_RUN_REPO_ANSWER_2026-09-12.txt` (SENT, thumbs-up received).

## Modules (who owns what)

| Module | Owner | Contents |
|---|---|---|
| Gate & SQL engine | Mahd | rules, parser, database layer, security decisions (`prototype/queryguard/`) |
| Frontend | Arwa (Mahd keeps a working baseline) | pages, wording, look (`web/` React SPA per D-023; plain-language copy owned by `queryguard/explain.py`) |
| Evaluation | Mahd leads, Arwa adds user-side questions | corpus, harness, metamorphic relations (`data/`, `scripts/`) |
| Requirements & deliverables | Mahd drafts, Arwa reviews | `srs/SRS.md`, submission, presentation |
| Demo | shared | scripted walkthrough, rehearsals |

Resilience rule: every lane has a working baseline on both sides, so nobody blocks anybody.
