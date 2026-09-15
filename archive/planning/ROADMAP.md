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
