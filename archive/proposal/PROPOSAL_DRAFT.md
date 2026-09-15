# Group Project Proposal (DRAFT v0.1, provisional)

**Status:** PROVISIONAL pending (a) group confirmation of topic/stack, (b) Canvas project page format/rubric capture. Content complete; format maps to whatever Canvas requires.
**Team:** [names pending] | **Course:** CS5391 Fall 2026 (Chen) | **Date:** 2026-09-01

---

## 1. Problem statement

Applications that let users query databases in plain English are now common: LangChain, LlamaIndex, and Vanna all translate natural language to SQL using large language models. The translation step is powerful, and it is also the attack surface. An attacker who can influence the prompt can make the LLM produce SQL that reads data it should never return or destroys the database entirely. This is not hypothetical: three CVEs affecting major LLM-database frameworks were disclosed between 2024 and 2026, including remote code execution in Vanna AI (CVE-2024-5565, CVSS 8.1) and extraction of personal information through AnythingLLM's SQL agent plugin (CVE-2026-32628). Teams adopting these tools today are wiring an unvetted code generator straight into their database.

## 2. Motivation

Existing defenses leave a practical gap. Model-side fixes (StruQ, USENIX Security 2025; SecAlign, ACM CCS 2025) require retraining or fine-tuning, so an existing deployment cannot adopt them without swapping models. General guardrail frameworks such as NVIDIA NeMo Guardrails and Guardrails AI detect injection using classification models that are opaque, are not aware of the specific database schema, and have documented false-positive problems on out-of-distribution attacks (Adversarial Prompt Evaluation, NeurIPS 2024 workshop). Academic work specific to this domain exists (LangShield, ICSE 2025) but was evaluated on a custom dataset and published as findings rather than as a working tool.

The gap sits at the application layer: a transparent, deterministic, SQL-specific check between the LLM and the database. Our project builds that layer.

## 3. Objectives

1. Build a working web application where users ask questions in plain English and receive answers computed from a relational database through an LLM-generated query.
2. Implement a deterministic validation gate that every generated query must pass before execution, covering destructive statements, multi-statement escapes, comment obfuscation, schema allowlist violations, and sensitive-column access.
3. Measure the gate: block rate per attack class and false-positive rate on a labeled corpus, produced by a repeatable one-command evaluation run.
4. Record every query decision (allowed or blocked, with the rule that fired) in an audit log viewable in the application.
5. Keep the full pipeline under continuous integration so a broken rule fails the build visibly.

## 4. Proposed solution

The system is a pipeline of five components with a hard trust boundary between the generator and the executor:

| Stage | Responsibility |
|---|---|
| Intake | Session handling, rate limiting, question log |
| Generator | LLM (or deterministic mock) produces candidate SQL plus a declared intent |
| Validation gate | Rule engine (10 rules) returns PASS or BLOCK(rule); every verdict is logged |
| Executor | Runs only gate-passed queries, read-only, against the demo database |
| Audit and metrics | Single append-only log; UI views and evaluation reports are derived from it |

The validation gate is architectural, not advisory: the executor accepts queries only from the gate, so no code path can bypass it. The rule catalog (G-01 to G-10) covers the six attack classes published in the ICSE 2025 P2SQL taxonomy; three rules also support MASK (hide sensitive columns) and REWRITE (add a missing LIMIT) actions. A mock generator mode with canned candidates, including malicious ones, makes development and demonstrations deterministic; a live LLM is an optional finish. Full design: rule catalog, data model, API surface, and evaluation methodology are already specified in the project working documents and will be attached to the SRS.

## 5. Scope

In scope: single-database demo application (SQLite), the ten-rule validation gate, audit log and metrics views, evaluation corpus (30 benign + 30 attack prompts) with automated reporting, CI test suite and evaluation workflow, project documentation (proposal, SRS, reviews, presentations).

Out of scope (explicitly): multi-database or cloud deployments, user account management beyond a demo session, defending against attacks on the LLM provider itself, performance tuning beyond gate latency measurement, and any mobile interface. These exclusions keep the build feasible in the second half of the semester and will be revisited only by team decision.

## 6. Team and roles (provisional until group confirms)

Five lanes, one owner each (4 people: the audit/metrics lane merges with evaluation): intake and UI, generator and LLM integration, validation gate and rule engine, evaluation corpus and harness, documentation and presentation. Every lane has a written contract in the design document; the operator's database and security coursework concentrates in the gate lane, while UI, evaluation, and documentation lanes give other members full ownership of graded deliverables.

## 7. Tools and stack (provisional: free choice per course; confirm against the Canvas project page)

| Tool | Role | Why |
|---|---|---|
| Python + Flask (or Node/Express if the group prefers) | Web application | Simple, well known, fast to test |
| SQLite | Demo database | Zero setup, real SQL semantics, file-shareable in the repo |
| pytest + GitHub Actions | Tests and CI | One workflow runs every rule test on each push; a second runs the full evaluation on demand |
| Mock generator | Deterministic development and demos | No API key needed; live LLM optional for the final demo |

## 8. Milestones

| Milestone | Target date | Acceptance |
|---|---|---|
| Proposal + presentation | before midterm (date TBA on Canvas) | This document final; slides reviewed by all members |
| SRS, review, presentation | before midterm | 15+ numbered requirements, each mapped to a test case; review comments addressed |
| Working skeleton | week after midterm | End-to-end path demonstrated on three questions |
| Rule set complete | +2 weeks | All ten rules implemented with unit tests |
| Evaluation v1 | +3 weeks | Corpus report generated in CI; block rate and false-positive rate published in the app |
| Final demo | before final | Scripted demo rehearsed twice; live metrics shown from the audit log |

## 9. Evaluation plan

A labeled corpus of 30 benign and 30 attack prompts, two per published attack class to start and grown by the team, is run by a single command that produces a per-rule report. Success criteria: 100 percent block rate on the write-oriented classes, a measured (not asserted) false-positive rate reported openly with a target under 10 percent at v1, and added gate latency under 50 ms per query at p95. The same corpus runs in CI on every change, so a rule that stops working breaks the build.

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| LLM API cost or downtime | Mock generator mode is the default; live mode is demo-only |
| Uneven contribution | Lane contracts with named owners; decision log records contributions |
| Scope creep | Section 5 exclusions are commitments, not suggestions |
| Late discovery of format/rubric differences | Proposal is structured to map onto standard rubric sections; Canvas spec will be checked against this draft before submission |

---

**Attachments referenced:** design document (architecture, rule catalog, data model, API, evaluation methodology), competition scan (seven existing solutions), corpus starter and mock candidate set.

---

## Unit record (SM51 control)

Steps: 1 READ (brief §3 skeleton, TECH_PLAN all sections, COMPETITION_SCAN, style rules, course index; no new files needed, all read earlier this session and re-checked) · 2 UNDERSTAND (consumers: Chen + TA; failure modes: missing rubric section, AI-style prose, late work) · 3 EXPLORE (all project surfaces inventoried; Canvas format confirmed still uncaptured, so PROVISIONAL labels applied rather than guessed) · 4 RESEARCH (competition scan is the cited research; CVEs and defense papers carry verified citations from the audited literature review) · 5 REVIEW (draft scope = Group 1 deliverable only; SRS and build not opened) · 6 IDEATE (full provisional draft vs outline: full chosen because content exists and the Sep 8-19 window is real; single-candidate framing vs multi-candidate: single, since the group decision is pending and A is the recommendation, noted as provisional) · 7 DRY RUN (style check: no em-dashes, no brochure voice, tables and labeled blocks per Chen patterns; every number traced to the project's verified records; rubric walk against the known grading table) · 8 PLAN (section order follows the brief skeleton; this file) · 9 IMPLEMENT (delivered at `project/proposal/` location; destination = this document; Canvas-format mapping remains an explicit open item, not silently assumed).
Findings: the draft is roughly 80 percent content-complete against the known rubric; the only genuine gaps are team names, the Canvas format, and the midterm date, all operator/group inputs.
Alternatives: outline-only (rejected, wastes the window); waiting for Canvas spec before any drafting (rejected: date risk with no compensating benefit).
Bias note: author reviewing own draft; mitigated by running the rubric walk and style rules as explicit checks, and by leaving the verdict to the group review pass.
