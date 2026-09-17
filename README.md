# QueryGuard: project entry point

Safety gate for LLM-generated SQL. CS5391 Group Project 1 (M. Mahd Amjad & Arwa Arafeh).
You ask a question in plain English, an AI drafts the SQL, and a deterministic gate checks
it before anything runs: destructive or snooping queries are blocked, private columns are
masked, and every decision is logged.

## Where to look

| Want | Go |
|---|---|
| Full map of files and folders (read first) | `INDEX.md` |
| Run the app, run the tests, where frontend work goes | `prototype/README.md` |
| Design, architecture, rule catalog | `TECH_PLAN.md` |
| Every decision with rationale and rejected alternatives | `DECISIONS.md` |
| The requirement document (the GP1 deliverable) | `srs/SRS.md` |
| Submission tracker (11 items) | `submission/SUBMISSION_CHECKLIST.md` |

## State (2026-09-16)

- Gate: 8 enforced rules + a parse-fail safe default on a parsed AST (stretch G-10 pending); compound SELECTs verified per arm; sensitive-column
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

## Modules (who owns what)

| Module | Owner | Contents |
|---|---|---|
| Gate & SQL engine | Mahd | rules, parser, database layer, security decisions (`prototype/queryguard/`) |
| Frontend | Arwa (Mahd keeps a working baseline) | pages, wording, look (`web/` React SPA per D-023; plain-language copy owned by `queryguard/explain.py`) |
| Evaluation | Mahd leads, Arwa adds user-side questions | corpus, harness, metamorphic relations (`data/`, `scripts/`) |
| Requirements & deliverables | Mahd drafts, Arwa reviews | `srs/SRS.md`, submission, presentation |
| Demo | shared | scripted walkthrough, rehearsals |

Resilience rule: every lane has a working baseline on both sides, so nobody blocks anybody.
