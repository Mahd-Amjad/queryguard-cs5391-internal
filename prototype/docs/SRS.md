# QueryGuard - Software Requirements Specification (v1.1)

**Status:** v1.1, submission before midterm. Group review notes fold in as they arrive; the submission is not gated on them. Written from the working system and its decision log (`DECISIONS.md` D-001..D-019); every requirement below is implemented and test-covered unless explicitly marked stretch/open.
**Structure:** IEEE-830 shaped (the course-confirmed spec form); IEEE-830 was withdrawn and superseded by ISO/IEC/IEEE 29148 — section naming here follows the familiar 830 layout with 29148 terminology.
**Revision history:** v0.1 draft 2026-09-10; v1.0 candidate 2026-09-12; v1.1 2026-09-15 - requirement priority ranking (section 3.6) and this history block added per the adopted IEEE 830 / 29148 yardstick (SUBMISSION_CHECKLIST item 5). Review notes fold in as they arrive; the submission is not gated on them.

---

## 1. Introduction

### 1.1 Purpose
This SRS specifies QueryGuard, a safety gate for LLM-generated SQL, as the review artifact for Group Project 1 and the requirement source for Group Project 2 (implementation and demo).

### 1.2 Scope
In scope: plain-English question intake; candidate SQL generation (mock default, live LLM optional); a deterministic validation gate (9 rules, actions BLOCK / MASK / SUGGEST) operating on a parsed SQL AST; compound-statement verification per arm; sensitive-column side-channel blocking; a gate-only executor over a read-only connection; an append-only audit log; an evaluation harness (labeled corpus + metamorphic relations); a plain-language web UI.
Out of scope (kept out so Project 2 stays feasible): live-LLM prompt-engineering quality work, user account management, multi-database support beyond SQLite, deployment beyond a single demo machine, model-side defenses.

### 1.3 Definitions
- **Gate:** the validation component that returns a verdict (PASS / BLOCK) and optional actions (MASK, SUGGEST) for a candidate query.
- **Rule:** one numbered safety check applied to every candidate (FR-G01..G10). Each rule carries a plain-language name shown in the UI (`queryguard/explain.py`).
- **Verdict:** the gate's decision: PASS = ran as asked; MASK = answered with private columns removed; BLOCK = stopped, nothing ran. ERROR = a query that passed the gate failed at execution; audited, nothing ran, nothing changed (see FR-03).
- **Attack class:** one of six published categories: direct DML, write bypass, multi-query, read exfiltration, schema reconnaissance, semantic mismatch.
- **Audit log:** the append-only record of every question and verdict; it only grows.
- **Mock mode:** deterministic generator mapping prompts to canned candidates; default for development, tests, and demos (zero external dependency).
- **Metamorphic relation (MR):** a semantically equivalent rewrite that must not change the verdict (Section 8.3).

### 1.4 References
Pressman, *Software Engineering: A Practitioner's Approach* (course text); Yeow et al., ICETSIS 2024 (Quiz 1 paper); `TECH_PLAN.md` (design §§1-12); `COMPETITION_SCAN.md` (LangShield/P2SQL ICSE 2025, StruQ USENIX 2025, SecAlign CCS 2025, SQLShield, NeMo Guardrails, Guardrails AI, RBAC-T2SQL benchmark arXiv 2607.22115); ISO/IEC/IEEE 29148 (SRS standard, IEEE-830 successor).

### 1.5 Overview
Section 2 describes the product and its users. Section 3 gives numbered functional and non-functional requirements. Sections 4-5 give the data model and interfaces. Section 6 traces every requirement to a test. Section 7 maps milestones to course dates. Section 8 reports measured evaluation results. Section 9 lists the course practices this project applies. Section 10 lists open items.

## 2. Overall description

### 2.1 Product perspective
QueryGuard is a standalone web application with five components in one request path: Intake -> Generator -> Validation Gate -> Executor -> Audit Log. The gate is architectural, not advisory: the executor accepts connections only from the gate, and the database connection is read-only at the file level (`mode=ro`) plus `PRAGMA query_only`, so no write can succeed even if a rule were bypassed. Rules run on a normalized AST (sqlglot, SQLite dialect), never on raw substrings.

### 2.2 Product functions
Answer plain-English questions against a demo clinic database; show the generated SQL and its verdict; block or transform unsafe queries before execution; explain every decision in plain language; record everything; and measure itself (block rates, false-positive rate, latency, metamorphic stability) with a repeatable harness.

### 2.3 User classes
- **End user (demo persona):** asks questions in a browser; sees answers and plain-language verdict explanations; never needs to know gate internals.
- **Developer/reviewer (course staff, group):** reads the audit log, metrics page, corpus reports, decisions, and this SRS.
- **Evaluator (harness/CI):** runs the labeled corpus and metamorphic relations; publishes metrics artifacts.

### 2.3.1 User stories
| As a... | I want to... | so that... | Requirements |
|---|---|---|---|
| demo viewer | type a question and see an answer | I can see the product work end to end | FR-01, FR-02, FR-04, FR-U1 |
| demo viewer | see every blocked query explained in plain English | I trust that nothing dangerous ran | FR-U1, NFR-4 |
| privacy-conscious viewer | know private columns (SSN, billing status) can never appear in answers | I can believe the privacy claim | FR-G05, C-1 |
| compliance reviewer | browse a log of every decision | I can verify what ran and why, after the fact | FR-A1, FR-A2 |
| evaluator | run one command that tests the gate against known attacks | safety claims are measured, not asserted | FR-E1..FR-E4 |

### 2.4 Operating environment
Single-machine demo; Python + Flask API + a built React SPA frontend (TypeScript, Vite, shadcn/ui + Tailwind - built at dev time, served statically by Flask, offline-safe at runtime); SQLite demo database; pytest (API/engine) + vitest (frontend) + GitHub Actions CI. No cloud services required in mock mode.

### 2.5 Design and implementation constraints
- **C-1 Read-only execution:** the executor's connection is read-only at the file level and by pragma; writes cannot succeed.
- **C-2 AST rules:** rules operate on a parsed, normalized AST (sqlglot), never raw substrings.
- **C-3 Mock-first:** candidate generation is swappable; mock is the default (no API dependency).
- **C-4 Content separation:** no shared code, naming, or claims with the group's research artifact.
- **C-5 Audit before response:** every decision is persisted before the response returns.
- **C-6 Compound safety:** set operations (UNION / INTERSECT / EXCEPT) are verified arm by arm; sensitive columns in GROUP BY / ORDER BY / HAVING block (D-011, D-012).
  A query that passes the gate but fails at execution returns an error response, is audited with verdict ERROR, and changes nothing (fail closed).

### 2.6 Assumptions and dependencies
Two-person group (Mahd + Arwa) with named lanes; midterm date TBA (requirement document is the by-midterm deliverable, restated by Chen on Sep 3 and Sep 8); demo-scale data volumes; AI-usage policy for deliverables not yet stated on any captured course surface (open item).

## 3. Specific requirements

### 3.1 Query flow
- **FR-01 (Intake):** every question enters through one endpoint (`POST /api/ask`) so each request follows one recorded path.
- **FR-02 (Generator):** a candidate SQL query is produced per question by the mock generator by default; a live-LLM generator may be swapped in behind the same interface.
- **FR-03 (Gate-only executor):** only gate-PASSED or gate-MASKED queries execute, and only over the read-only connection; BLOCKED queries never reach the database.
- **FR-04 (Answer assembly):** every request returns `{answer, sql, verdict, elapsed_ms}`, where elapsed_ms is the full request time (generator + gate + execution), honestly labeled in the UI against the 50 ms target.

### 3.2 Validation gate (one FR per rule; each is one test case)
- **FR-G01 (No destructive statements):** BLOCK any INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE.
- **FR-G02 (One query at a time):** BLOCK stacked statements.
- **FR-G03 (No hidden write commands):** BLOCK write commands hidden by comments (comments stripped pre-parse; comment-joined candidates BLOCK, per the concat-form check).
- **FR-G04 (Only allowed tables):** BLOCK references to tables outside the declared queryable set.
- **FR-G05 (Private columns stay private):** BLOCK or MASK any statement exposing a SENSITIVE column, where exposing covers projections of any SELECT (including every arm of a compound statement) and references in GROUP BY, ORDER BY, or HAVING; MASK when non-sensitive columns remain, BLOCK when an all-sensitive projection or a side channel is present; WHERE-filtering on a sensitive column is allowed (D-002, D-011, D-012).
- **FR-G06 (No system-table snooping):** BLOCK catalog queries (`sqlite_master`, `information_schema`, pragma tables, equivalents).
- **FR-G07 (No execution tricks):** BLOCK PRAGMA, ATTACH, and side-effecting functions (e.g., `load_extension`).
- **FR-G09 (Huge answers get a hint):** unbounded non-aggregated SELECTs PASS with a SUGGEST action offering a LIMIT (D-003: suggestion, not block, protects the false-positive target).
- **FR-G10 (Answer must match the question) [stretch]:** BLOCK when declared intent and SQL shape disagree; droppable by recorded decision (D-005).
- **PARSE safety default:** unparseable candidates BLOCK (D-004).

### 3.3 Audit and evaluation
- **FR-A1 (Audit record):** one append-only record per request: id, ts, session, question, intent, sql, verdict, rule_id, action, latency_ms, mode.
- **FR-A2 (Audit view):** paginated audit browsing via `GET /api/audit` and the `/ui/audit` page.
- **FR-E1 (Corpus run):** the labeled corpus (64 entries: 30 benign + 34 attack, each labeled with expected verdict and rule) runs in one command; results retrievable per run.
- **FR-E2 (Metrics report):** per-class block rate, false-positive rate on the benign corpus, and latency percentiles as a JSON artifact + human-readable table.
- **FR-E3 (Regression):** rule changes rerun the corpus in CI; any expected-verdict miss fails the build (D-006 verdict-level compare; D-008 MASK satisfies expected BLOCK).
- **FR-E4 (Metamorphic stability):** equivalent rewrites (case, whitespace, semicolon, added LIMIT) shall not change any verdict; the harness reports violations and fails on any (Section 8.3).

### 3.4 User interface
- **FR-U1 (Ask view):** the user submits a question and sees the answer, the generated SQL, the verdict, and the rule's plain-language name and explanation.
- **FR-U2 (Metrics view):** pass/blocked/masked counts, per-rule attack-stop chart, and latency percentiles, each labeled so a first-time viewer knows what is good or bad.
- **FR-U3 (Explain view):** a "How it works" page states the three-step flow and all nine rules in plain language, so no internal id is required to understand a verdict (plain names owned by `queryguard/explain.py`).

### 3.5 Non-functional requirements
| ID | Requirement | Target |
|---|---|---|
| NFR-1 | Request latency (full path) | p95 < 50 ms, measured |
| NFR-2 | False positives on the benign corpus | 0 at v1 (target was < 10% at v0), reported openly |
| NFR-3 | Demo availability | all demos/tests run in mock mode, zero external API |
| NFR-4 | Explainability | every BLOCK/MASK/SUGGEST carries a plain-language reason |
| NFR-5 | Least privilege | read-only connection, no string-concatenated SQL, engine-level `mode=ro` |
| NFR-6 | Result bounds | answers capped at 50 rows in the UI layer |

### 3.6 Requirement priorities (29148 "ranked")

| Priority | Requirements | Basis |
|---|---|---|
| Essential | FR-01..FR-04, FR-G01..G07, PARSE, FR-A1, FR-A2, FR-E1..E3, FR-U1..U3, NFR-2..NFR-5 | the safety gate, its audit, its measurement, and the demo surface; without these the product does not exist |
| Conditional | FR-G09, FR-E4, NFR-1, NFR-6 | real contributions with recorded decisions (D-003) or measured headroom (p95 0.57 ms vs the 50 ms target); the product holds without them |
| Optional | FR-G10 | stretch by recorded decision (D-005); droppable without losing the demo |

## 4. Data model
Demo database (protected asset): `patients(id, name, dob, ssn*, diagnosis*)`, `appointments(id, patient_id, doctor_id, date, room)`, `doctors(id, name, specialty)`, `billing(id, patient_id, amount, paid*)`, `medications(id, name, manufacturer)`, `prescriptions(id, patient_id, medication_id, date, dose)`, `staff(id, name, role)`; `*` = SENSITIVE, masked by default (FR-G05). Audit log (canonical truth): one append-only table per FR-A1.

## 5. External interfaces
| Endpoint | Method | Purpose |
|---|---|---|
| `/api/ask` | POST | question -> {answer, sql, verdict, elapsed_ms} |
| `/api/audit` | GET | paginated audit JSON |
| `/api/metrics` | GET | pass rate, blocks by rule, latency percentiles |
| `/api/eval/run` + `/api/eval/results/<id>` | POST/GET | corpus run + report |
| `/` , `/ui/how`, `/ui/metrics`, `/ui/audit` | GET | plain-language pages (FR-U1..U3, FR-A2) |

## 6. Traceability (requirement -> evidence)
| Requirement | Evidence |
|---|---|
| FR-01..FR-04 | TC-01..TC-05 (`tests/test_app.py`): single-path intake, generator contract, blocked-never-executed, response shape |
| FR-G01..G09, PARSE | TC-G01..TC-G09 + PARSE (`tests/test_rules.py`): one pass case + one bypass attempt per rule |
| FR-G05 compound + side channels | 7 dedicated tests (`test_rules.py`, D-011/D-012) + corpus A-EXF-06..09 |
| FR-A1, FR-A2 | TC-06 append-only check; TC-07 pagination; `/ui/audit` render test |
| FR-E1..E3 | TC-08 corpus run artifact; TC-09 CI fail-on-miss; `run_eval.py` 64/64 (Section 8) |
| FR-E4 | `tests/test_meta.py` + `scripts/run_metamorphic.py` (384 relations, Section 8.3) |
| FR-U1..U3 | UI render tests (ask explains, metrics labels, audit page, how page) |
| NFR-1..NFR-6 | Metrics report p50/p95; FPR 0 on 30 benign; `fetchmany(50)` cap |
40 unit/integration/UI tests + 1 execution-error fail-closed test = 41 passing.

## 7. Milestones
| Milestone | Acceptance | State |
|---|---|---|
| M1 Proposal | presented Sep 9 (+Sep 10), Canvas receipt | done |
| M2 SRS + review + submit | this document; group review in DECISIONS; submit before midterm | v1.0 candidate; review pending |
| M3 Skeleton | end-to-end path on 3 demo asks | done (ahead of schedule) |
| M4 Rules complete | all rules with unit tests | done (G-10 stretch pending) |
| M5 Evaluation v1 | report in CI artifact + numbers in this SRS | done (Section 8) |
| M6 Demo | scripted demo rehearsed twice, CI green | before final |

## 8. Measured evaluation results (2026-09-12, `prototype/out/report.md`)
### 8.1 Corpus (64 entries, mock mode)
- verdict matches: **64/64**; benign false-positive rate: **0.0**.
- block-or-mask rate by attack class: direct_dml **100%**, write_bypass **100%**, multi_query **100%**, read_exfiltration **100%**, schema_recon **100%**, semantic_mismatch **100%**.
- exact-verdict match on read_exfiltration: 55.6% — the remainder returned MASK (private columns removed), the designed outcome; the safety-relevant leak rate is 0. Reported separately so the number stays honest (D-008).
- latency p50/p95: **0.224 / 0.569 ms** (target < 50 ms).
### 8.2 Tests
41 passing: per-rule pass+bypass, compound-arm and side-channel regressions, HTTP integration, UI render checks, fail-closed runtime regression (FR-03).
### 8.3 Metamorphic relations
384 checks (64 candidates x 6 relations): **all hold**. Equivalent rewrites never change a verdict.

## 9. Course practices applied
- **User stories** (XP, lecture Sep 3): Section 2.3.1, traced to requirements and tests.
- **Test-first / refactoring** (XP, lecture Sep 3): the UNION defect was reproduced as a failing behavior, fixed, and pinned by regression tests; rule interpretations were refactored with the corpus as the safety net.
- **Continuous integration** (lecture Sep 3 + slide 7): push-gate workflow fails the build on any test or corpus miss.
- **Security practices** (lecture Aug 27): masking vs tokenization, least privilege, read-only enforcement — all demonstrated by the gate.
- **AI-era framing** (lecture 1): the gate is the control layer for an AI tool writing SQL against a real schema.

## 10. Open items
1. Group review notes: folded in as received - not a submission gate.
2. AI-usage policy for deliverables: no course-stated policy exists; the operator rule applies (AI tools used in development, per course allowances where stated). Settled 09-15 - not a gate.
3. Midterm date: not yet posted; pins M2 submission.
4. Live-LLM mode: needs the group's API choice (Project 2 opener).
5. FR-G10 intent matching: stretch, droppable by recorded decision.
