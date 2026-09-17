# QueryGuard - Canonical Index (the one file to read first)

**Rule:** this file is the map, not the territory. One line per thing: what it is, when to use
it. If a line and reality disagree, fix the line the same day (owner: whichever session finds it).

**Last updated:** 2026-09-15 (SM62). Maintainer: every session that changes the project.

## The 30-second orientation

- **What this is:** QueryGuard - a safety gate for LLM-generated SQL. CS5391 Group Project 1
  (Mahd Amjad + Arwa Arafeh). Backend: Flask + SQLite + sqlglot (9 rules, BLOCK/MASK/SUGGEST,
  audit log, 64-entry corpus, metamorphic relations). Frontend: React 19 + TypeScript + Vite +
  shadcn/ui + Tailwind v4 + recharts SPA served by Flask.
- **Run the demo:** `web/` built -> `web/dist` served by Flask at :5055. Dev: `cd web && pnpm
  dev` (proxies /api to Flask). Backend only: `qg.sh serve`.
- **Tests:** backend `pytest -q` (40, in `tests/`), frontend `cd web && pnpm test` (16, vitest
  jsdom). Both must pass before any commit.
- **The product's depth = the evaluation** (corpus + metrics), not the UI. UI = delivery vehicle.

## Canonical files (project root = repo root)

| File | Role |
|---|---|
| `README.md` | current state + run instructions (repo-facing) |
| `TECH_PLAN.md` | design SSOT: architecture, rules, section 16 = frontend rebuild design |
| `srs/SRS.md` (+ .html/.docx generated) | the requirement document (GP1 deliverable; md = source, run `scripts/md_to_html.py` after edits; docx via officecli) |
| `DECISIONS.md` | decision log D-001.. - append-only, never rewrite old entries |
| `QA_CHECKLIST.md` | the gate every unit passes (stranger test, truth pass, correctness pass) |
| `COMPETITION_SCAN.md` | related work + position (3 passes) |
| `submission/SUBMISSION_CHECKLIST.md` | GP1 submission tracker (11 items) |
| `docs/ui-ux-reference-study.md` | design-language study (zapply/softwarejobs) - references, not templates |
| `prototype/docs/story.md` | repo-facing narrative (renderer mirror of srs/ lives beside it) |
| `archive/` | consumed planning, jinja-ui-2026-09-15, planning originals |

## Canonical tools (how we do things)

| Tool | Use for | Command |
|---|---|---|
| officecli | docx/xlsx/pptx create + edit (canonical office pipeline; markdown element = md -> docx) | `officecli help docx` |
| `scripts/md_to_html.py` (in prototype/) | SRS md -> branded html + repo mirror | run from prototype after any SRS edit |
| presenton | deck GENERATION if needed (decks usually hand-built via python-pptx scripts) | see docs/DECK docs |
| `.meta/scripts/research.py` (workspace) | gh/web research pass (tool-mandatory RESEARCH step) | `research.py gh "<query>"` |
| `.meta/scripts/audit_scan.py` (workspace) | duplicate/corrupt/register audit | part of grad-doctor |
| `scripts/repo-sync.sh` (project/) | THE one push tool: `internal` = full tree -> queryguard-cs5391-internal; `shared` = whitelist subset -> queryguard-cs5391; `both` = both. Whitelist inline in the script | run from project/ |
| playwright chromium | SPA browser tests (starter config; install once if missing) | `pnpm test:browser:install` |
| `Slack_chat.txt` (Graduate root) | the Arwa Slack chain outbox - append messages, never draft in chat | one chain file per external party |

## Communication

- **To the operator:** the output contract in Business CORE_RULES section 2 (answer first, max-5 lists, no recap) + session tables max 5 rows.
- **To external parties (Arwa, professors):** the Legal-drafts shape - their question as the header, the answer up front, numbered facts, plain words, one next step. Messages are appended to the chain file for that party (Slack_chat.txt for Arwa), never drafted in chat.
- **Governance references:** Zapply Discord protocol (Business ssot/DISCORD_SERVER_PROTOCOL.md) = server access and incident governance only, not message writing.

## Canonical skills (load when the task matches)

| Skill | When |
|---|---|
| review-rigor (estate) | BEFORE any conclusion/claim (7-check discipline) |
| graduate-deep-audit | workspace-wide audits |
| session-end | session close: chronicle, SESSION.md, backups, board |
| xlsx | spreadsheets as input/output |
| web-research | external research routing |

## Non-negotiables (the short list; full versions live in the files above)

1. Two-phase work: Phase 1 = plan/analysis/design -> operator approval -> Phase 2 = build.
2. Verify at the destination (read the artifact, not the command exit code).
3. Backend tests + frontend tests + build green before every commit; commit after every
   verified unit (the drvfs tree can vanish uncommitted work - small commits).
4. No em dashes; no AI tells; group documents speak as the two-person team (never "operator").
5. The frontend never touches SQLite or the filesystem - Flask API only, same origin.
6. API keys live in Flask only - never in the frontend bundle.

## Build/serve mechanics (WSL drvfs warning)

This workspace lives on /mnt/c (drvfs). Known hazard: recently-written files can serve STALE
content to newly-spawned processes (builds, daemons) while the long-lived shell sees fresh
bytes. Consequences observed 2026-09-15: an empty generated docx, a stale served bundle.
Protocol: after writing files, build/serve from the NATIVE filesystem (`~/qgserve` holds the
runtime; `~/qgweb` the build tree) or re-verify the artifact content itself, never the exit
code. Commit small and often - the tree has vanished once (recovered from the backup mirror).
