# TECH_PLAN superseded content (extracted verbatim 2026-09-15, SM62 truth pass)

Provenance: sections removed from TECH_PLAN.md on 2026-09-15 under D-019 (consumed
content leaves the SSOT - the same principle as D-017). Line numbers refer to the
pre-edit TECH_PLAN.md (317 lines). The SRS cites "TECH_PLAN design sections 1-12";
numbering is preserved in TECH_PLAN, only bodies collapsed.

---

## [was lines 82-91] Section 7 body - milestone table (duplicate of SRS section 7)

## 7. Milestones and acceptance

| Milestone | Acceptance |
|---|---|
| M1 Proposal (by ~Sep 19) | Submitted; rubric items covered; deck in Chen structure rules |
| M2 SRS (before midterm) | FRs G-01..G-10 + UI/audit FRs, numbered, each mapped to a test; review comments addressed in `DECISIONS.md` |
| M3 Skeleton (post-midterm wk 1) | Intake→generator(mock)→gate→executor→audit path works end-to-end on 3 questions |
| M4 Rules complete | G-01..G-10 implemented, each with unit tests |
| M5 Evaluation v1 | Corpus report generated in CI; FPR/block-rate published in-app |
| M6 Demo | Scripted: normal Qs answered, attack visibly blocked with rule id, metrics page live; rehearsal ×2 |

---

## [was line 95] Section 8 - demonstration script v1 (pre mock-only fix)

1. Ask "how many appointments in March?" -> answer + clean SQL shown. 2. Ask "delete all billing records" -> BLOCKED (G-01), logged. 3. Ask a PII question -> MASKED (G-05). 4. Live-LLM finale: adversarial phrasing -> still blocked. 5. Metrics page: block-rate + FPR + latency, from the audit log. 6. GitHub: CI green, corpus report artifact.

---

## [was lines 97-99] Section 9 - group-dependent decisions (all resolved/superseded)

## 9. Group-dependent decisions (the only open items)

1. Stack: Python/Flask vs Node vs .NET (free choice presumed; confirm vs Canvas project page). 2. Lane owners (5 lanes above). 3. Corpus authorship split (each member writes N benign + N attack prompts for their lane). 4. Group risk appetite (if minimum-effort wins, fallback D remains in the matrix).

---

## [was lines 112-176] Section 11 body - Sep-1 era roadmap (consumed by execution)

# 11. Roadmap, effort split, quality loops (absorbed verbatim from ROADMAP.md, 2026-09-04 consolidation)

# CS5391 Project - Roadmap (QueryGuard working name)

**Created:** 2026-09-01 (post group-brief share) · **Updated:** 2026-09-03 (full-semester execution pass; proposal presented today, topic locked per operator direction 2026-09-02, pending group social confirmation)
**Goal:** a genuinely great project - top of the class against the other group - by putting depth only where the rubric looks, and keeping breadth competent but thin.

---

## Breadth vs depth (where effort goes)

**Breadth (competent, not deep):** web UI, API layer, deployment, docs site, presentation polish. These exist so the project is complete; none is a selling point.

**Depth (the three differentiators):**
1. **The guard + its evaluation.** Rule set (destructive statements, injection patterns, schema allowlist), measured block-rate and false-positive rate on a fixed corpus, repeatable via one-click evaluation run. Numbers are the story.
2. **The audit trail.** Every query: allowed/blocked + reason + timestamp, browsable. This is the "explainable" claim made concrete.
3. **SE process artifacts.** Numbered testable SRS requirements, decision records, CI gate, change-management section. This is what the rubric actually grades in Group Project 1.

## Calendar (full semester; midterm TBA - assumed ~Oct 12-16; dead week/finals TBA)

| Window | Phase | Output |
|---|---|---|
| Sep 3 (today) | Decide - close out | Proposal deck (candidate A) presented; group topic confirmation recorded in `DECISIONS.md`; Canvas project page + midterm date captured; literature-review quiz dates captured (parallel track - do not let them sneak up) |
| Sep 4 → Sep 5 | Decide | Slack replies folded into the matrix; stack locked (free choice presumed vs Canvas page); lane assignments drafted |
| Sep 8 → Sep 19 | **Proposal build** | Lit/competition table (from the operator's existing citation-audited review + the one defined competition-scan pass), proposal from brief §3, deck per the corrected from-scratch pptx workflow (REPO_LEARNING_PLAN Phase D; OfficeCLI-verified, Gate 3 screenshot audit) |
| Sep 22 → Sep 26 | **Proposal submit + present** | Group review pass (comments in `DECISIONS.md`), revisions executed, submit with buffer; Canvas receipt + rubric walk recorded |
| Sep 29 → Oct 10 | **SRS** | 18-20 numbered FRs (G-01..G-10 incl. the AST-parsing requirement, plus intake/UI, audit, eval-harness FRs - each = a Group 2 test case), NFRs (p95 < 50 ms, FPR target), data model + audit schema, traceability matrix (FR → test), group review pass, submit **before midterm** |
| ~Oct 19 → Nov 13 | **Build** | Dependency order per PHASE_PLANS B.0-B.8: repo + CI green from commit #1, demo schema, gate engine (sqlglot - verify SQLite dialect quirks early, not late), mock generator, executor + audit, UI, eval harness; weekly evaluation runs on the corpus; stretch rules G-08/G-09 droppable if the calendar bites - the core demo survives with 8 rules |
| Nov 16 → Dec 4 | **Demo + retro** | Scripted 6-step demo (bad query visibly blocked + live metrics on screen), rehearsal ×2 incl. failure modes (live LLM hangs → cut to mock), retrospective + peer evals, repo cleanup for grading (README, decision log, no dead code) |
| Dead week / finals (TBA) | Buffer | No new work - submission wrangling only. Proposal and SRS already carry buffer by design |

## Process allocation (total project effort)

| Activity | Share | Notes |
|---|---|---|
| Implementation | ~40% | Mock-first; CI from day 1; lanes per contract |
| Evaluation/measurement | ~20% | Corpus, block-rate, FPR, latency - the depth area |
| Research (bounded) | ~15% | See research policy below |
| Writing (proposal/SRS/slides) | ~15% | From skeletons; style pass every artifact |
| Review/iterate/rehearse | ~10% | The loops below |

## Research policy (bounded, not open-ended)

- **Reuse first:** the operator's research project already has a citation-audited literature review covering StruQ, SecAlign, SQLShield, prompt-injection benchmarks - the competition table starts there, not from scratch.
- **Three defined online passes only:** (1) competition scan for the proposal (NeMo/Guardrails-AI/vendor gateways - what exists, one paragraph each), (2) evaluation-design check (how do security papers measure guard FPR - we already know: hallucinator-style validation, corpus discipline), (3) related-work refresh right before the final presentation.
- **Local exploration:** ZJP patterns already extracted into the matrix; further exploration is pull-based (only when a build question actually needs it).

## Quality loops (every deliverable, every time)

1. Rubric check - walk the known/expected grading criteria item by item.
2. Grader-lens review - read it as the TA who has 30 submissions to grade.
3. Style pass - `AI_DETECTION_AVOIDANCE_RULES` + professor-style deltas (Section 2 to be filled from Chen's decks before the first draft).
4. One group iteration - the group reviews before anything is submitted; their comments are recorded in `DECISIONS.md`.

## Risks and standing mitigations

| Risk | Mitigation |
|---|---|
| Scope creep (this idea can eat a semester) | Out-of-scope list in the proposal; mock-LLM-first; breadth stays thin by design |
| LLM API dependency/cost | Mock mode is the development default; live LLM is demo finale only |
| Uneven contribution | Lane contracts with named owners; decision log records who did what |
| Calendar collision (CS5338 A2-A4 + CS5391 deliverables) | Rollers in root TODO carry all dated items; proposal submitted with buffer, never at the deadline |
| "Operator's project" perception | Teammate lanes (UI, evaluation harness, docs) are first-class, assigned early |

---

## [was lines 205-297] Section 12 body - phase parts + perspectives (executed)

# 12. Phase parts and perspective analysis (absorbed verbatim from PHASE_PLANS.md, 2026-09-04 consolidation)

# Phase Plans and Perspective Analysis (CS5391 project)

**Created:** 2026-09-01 (CS5391-PROJ-1 planning unit; operator-directed brainstorm, own-parts format). Companion to `ROADMAP.md` (calendar) and `TECH_PLAN.md` (design). This file answers: what are the PARTS of each phase, and what does each stakeholder perspective demand of them.

---

## 1. Perspective lens (applied to every phase below)

| Perspective | Wants | Fears | Design consequence |
|---|---|---|---|
| End user (non-technical analyst) | Fast answers | Jargon, false blocks | Block reasons in plain English + a suggested refined question; FPR kept visible and low |
| Attacker / red team | A bypass | Being logged | Normalization layer before rules (case, comments, unicode); fuzz variants of every corpus attack |
| Grader / TA | Findable, checkable deliverables | Vague claims | Numbered FRs mapped 1:1 to tests; rubric walk attached to each submission |
| Teammate (Arwa, non-security background) | A lane she can own end-to-end | Being the weak link | UI/UX and corpus lanes are first-class, not scraps; pair on the first rule |
| Professor (Chen) | AI-era SE process, visibly | Ad-hoc work | CI story, decision records, process artifacts; his labeled-block slide style |
| Judge (vs the other group) | A memorable demo | Sameness | Live attack playground + published numbers, not narrated slides |
| Product / compliance buyer | Governance evidence | Unexplained behavior | Sensitivity labels, masking report, safety receipts |

New ideas surfaced by the lenses: (a) the evaluation harness can auto-generate attack variants (casing/comment/unicode fuzz) of each corpus prompt, so **the guard tests itself**; (b) a rule **changelog page** (governance: when a rule was added/tightened and why) — cheap and very "real product"; (c) flag EMPTY result sets as suspicious (a semantic-mismatch signal beyond G-10). All three are candidate stretch features, not commitments.

## 2. Phase P — Proposal (Sep 5-19)

**Entry gate:** group topic + stack confirmed; Canvas project page + midterm date captured.
**Parts:**

| Part | Output | Owner |
|---|---|---|
| P.1 Finalize matrix + lanes | Signed-off matrix (2-person core design kept) | group |
| P.2 Rubric mapping | Draft sections mapped to the Canvas rubric line by line | operator + assistant |
| P.3 Content assembly | From PROPOSAL_DRAFT + TECH_PLAN + COMPETITION_SCAN (no new research needed) | assistant |
| P.4 Slides | Per pptx spec + Chen structure rules (labeled blocks, decision guides, no em-dashes); OfficeCLI render-verified | assistant |
| P.5 Review pass | Group reads; comments recorded in `DECISIONS.md`; revisions executed | group |
| P.6 Submit + receipt | Canvas submission; capture proof | operator clicks |

**Exit gate:** submitted with buffer before midterm; receipt + rubric walk recorded.

## 3. Phase S — SRS (Sep 22 - Oct 10)

**Entry gate:** proposal accepted; midterm date known.
**Parts:**

| Part | Output |
|---|---|
| S.1 Functional requirements | 18-20 numbered FRs: G-01..G-10 (incl. the AST-parsing requirement), intake/UI FRs, audit FRs, eval-harness FRs; each with trigger/input/processing/output |
| S.2 Non-functional requirements | Gate latency p95 < 50 ms, FPR target, availability of mock mode, usability of block explanations |
| S.3 Data model + audit schema | Demo schema + append-only audit table (from TECH_PLAN §3) |
| S.4 External interfaces | The five API endpoints, request/response shapes |
| S.5 Traceability matrix | FR -> test case table (the "review" deliverable evidence) |
| S.6 Group review + revision | Comments + resolutions in `DECISIONS.md` |
| S.7 SRS presentation + submit | Deck per spec; submit before midterm |

**Exit gate:** SRS submitted; every FR has a mapped test.

## 4. Phase B — Build (post-midterm -> mid-Nov)

**Order (dependency-driven, not preference):**

| Part | Depends on | Output |
|---|---|---|
| B.0 Repo + CI live | topic locked | Both workflows green on an empty skeleton; badge in README |
| B.1 Demo schema + seed data | B.0 | The 7-table database with sensitive columns populated |
| B.2 Gate engine (sqlglot AST) | B.0, B.1 | Normalizer + G-01..G-10 with unit tests; the hard requirement from TECH_PLAN |
| B.3 Mock generator | B.1 | Prompt-to-candidate lookup incl. attack candidates |
| B.4 Executor + audit | B.2 | Read-only execution of PASSed SQL; audit rows written |
| B.5 UI (split-pane + safety receipts) | B.3, B.4 | Ask flow, verdict cards, audit page, metrics strip |
| B.6 Eval harness + report | B.2-B.4 | `/api/eval/run` + CI artifact + metrics page |
| B.7 Live-LLM option | B.3 (optional) | API swap behind the same interface |
| B.8 Hardening + fuzz variants | B.6 | Auto-generated attack variants; fix whatever bypasses |

## 5. Phase D — Demo and close (Nov)

| Part | Output |
|---|---|
| D.1 Demo script final | The 6-step script from TECH_PLAN §8, timed under 10 minutes |
| D.2 Metrics on screen | Live metrics page + the CI corpus report artifact |
| D.3 Rehearsals | Two full run-throughs; failure modes rehearsed (what if live LLM hangs: cut to mock) |
| D.4 Retro + peer evals | PEER_EVAL_METHODOLOGY; honest contribution record |
| D.5 Repo cleanup for grading | README, decision log, no dead code |

## 6. Scrutiny (adversarial pass on our own plan)

- **Found and fixed:** G-01 substring matching would false-block `deleted_at` and miss obfuscation; gate must parse SQL (sqlglot). Silent REWRITE removed (semantics change without consent); action set is now BLOCK / MASK / SUGGEST.
- **2-person capacity risk:** Group 2 build is heavy for operator + Arwa. Mitigation: B.2-B.4 (the core path) is assistant-heavy; Arwa owns B.5 UI + corpus growth + docs; stretch rules (G-08, G-09) drop to "stretch" if the calendar bites — the core demo survives with 8 rules.
- **SQLite parse caveats:** sqlglot must handle SQLite pragmas and dialect quirks; verify early in B.2, not late.

## Unit record (SM51 control)

Steps: 1 READ (TECH_PLAN at destination; ROADMAP; matrix; prior brainstorm threads) · 2 UNDERSTAND (per-phase consumers and gates; failure modes: phase parts without gates become vibes) · 3 EXPLORE (all project surfaces; perspectives enumerated to 7; archive/prior lessons: SM50 tooling-unit failure informs B-phase verification-first rule) · 4 RESEARCH (no new external research needed; sqlglot choice flagged for B.2 verification) · 5 REVIEW (parts bounded; stretch rules explicitly droppable; no new features committed without group) · 6 IDEATE (3 lens-born ideas recorded as candidates, not commitments; fuzz-self-test judged the strongest) · 7 DRY RUN (found and fixed 2 design defects in TECH_PLAN: substring matching, silent REWRITE — the perspectives pass paid for itself) · 8 PLAN (this file) · 9 IMPLEMENT (delivered; TECH_PLAN edits verified at destination by read-back).
Bias note: builder bias guarded by explicit droppable stretch rules; confirmation bias guarded by the adversarial pass attacking our own design first.

---

## [was lines 313-317] Tail position paragraph (stale counts)

**Position (2026-09-12):** proposal presented (Sep 9 + Sep 10). SRS draft v0.1 exists with
user stories (§2.3.1) and the fixed FR-G05 wording. Prototype = working app: 39 tests,
64-entry corpus green, Tabler UI with plain-language layer. Remaining before midterm:
SRS v1.0 in the group's voice + group review + submit. Post-midterm: live-LLM mode, G-10,
corpus hardening, demo (phase B/D remainder).
