# Competition Scan — existing solutions and our position (Research pass #1)

**Created:** 2026-09-01 (CS5391-PROJ-1, roadmap research pass 1 of 3). Feeds the proposal's Motivation + Related Work. Position statement refined from the operator discussions: we are an operationalized, audited, measurable engineering realization — not a novel-research claim.

---

## The landscape (one paragraph each)

**LangShield (ICSE 2025 — Pedro et al.).** The closest prior art, and our academic ancestor. Defines four defense mechanisms for LLM-database systems: database permission hardening (RBAC), SQL query rewriting (parse-and-restrict, <2 ms), in-prompt data preloading, and an auxiliary LLM guard. Tested on a custom dataset, not enterprise-scale schemas, and packaged as evaluation findings — not as a working, inspectable application. Our guard's rule classes map directly onto their taxonomy; our contribution is turning it into a running system with an audit trail and measured false-positive rate.

**StruQ (USENIX Security 2025) and SecAlign (ACM CCS 2025).** Model-side defenses: structured query formats and preference optimization respectively. Strong results, but both require retraining or fine-tuning the model — an existing deployment cannot adopt them without swapping models, and their guarantees do not transfer across model families. They defend the model; we defend the deployment.

**NVIDIA NeMo Guardrails.** General-purpose LLM guardrail framework (Colang configs + NVIDIA safety/detection models), including injection detection with SQL-injection heuristics. Broad and production-credible, but detection is model-based classification: opaque decisions, no SQL-semantic understanding of the specific database schema, no per-decision audit explanation, and the benchmarking literature (Adversarial Prompt Evaluation, NeurIPS 2024 workshop) documents that generic guardrails miss out-of-distribution attacks and add false positives.

**Guardrails AI.** Composable output-validation framework with a validator hub. Operates on request/response pairs against generic validators (structure, content rules); nothing SQL-semantic — no schema allowlist, no destructive-statement policy, no query-level audit log. A reasonable integration surface, not a competing gate.

**Llama Guard (Meta).** Prompt/response safety classifier; reported archived and no longer maintained as of 2026. Included for completeness.

**SQLShield (Cambridge, NLP 2025).** SQL-specialized prompt-injection defense analysis. Relevant academically; our project cites it as evidence that SQL-specialization matters, and differs in being a working gate with measured FPR rather than a defense study.
**Shipped tools (disconfirming scan 2026-09-01).** The generic gate exists as products and libraries: Thales `sql-data-guard` (LLM SQL safety layer), HeimdaLLM (LLM SQL validation), `user-query-guard` (local validation engine + MCP server), protectai `llm-guard` and `llm-injection-guard` (injection scanners). Consequence: building a gate is table stakes, not a differentiator. What these tools generally do NOT ship: a labeled evaluation corpus with published block-rate and false-positive numbers, per-decision plain-English explanations, schema-level sensitivity governance with automatic masking, or any multi-model comparison view. Those gaps define where our project's identity has to live.


## Position statement (the honest version)

We do not claim to outperform NeMo, Guardrails AI, or LangShield at their own game. The claim is narrower and defensible: **a transparent, deterministic, SQL-specific validation gate at the application layer** — schema allowlist, destructive-statement policy, injection-pattern detection — that any LLM can sit behind without retraining, that explains every decision in an audit log, and whose false-positive cost is measured on a published corpus. Deterministic rules make it testable (every rule = a numbered SRS requirement = a test case), which is why it is also a strong course project.

## Sources

- LangShield mechanisms: `research/text2sql_security/LITERATURE_REVIEW.md` §1.1 (from the ICSE 2025 P2SQL paper, citation-audited)
- StruQ/SecAlign: LITERATURE_REVIEW §3.1-3.2 (venues, authors, repos verified in the March reviewer sessions)
- NeMo injection detection: docs.nvidia.com (microservices guardrails tutorials, 25.6.0) — read 2026-09-01
- Guardrails AI: guardrails-ai GitHub + 2026 comparison articles — read 2026-09-01
- NeMo/generic-guardrail FPR critique: Adversarial Prompt Evaluation (arXiv 2502.15427), already in LITERATURE_REVIEW
- Llama Guard archived status: 2026 comparison article (single source — label: secondary, verify if it becomes load-bearing)

---

## Unit record (SM51 control — first application)

- **Steps:** 1 READ (lit review structure + defense sections read at destination; project decision tables consulted) · 2 UNDERSTAND (defense taxonomy vs our design; consumers = proposal Motivation/Related Work) · 3 EXPLORE (lit review archives + prior Discovery scans checked before searching; LangShield found — missed by memory-based planning) · 4 RESEARCH (NeMo/Guardrails-AI current state from vendor docs + comparisons; single-source item labeled) · 5 REVIEW (scan scope bounded to 7 entries; Llama Guard kept for completeness, flagged) · 6 IDEATE (position = narrow honest claim vs superiority claim — chosen; alternatives recorded) · 7-8 DRY RUN/PLAN (deliverable = this file; no code, no side effects) · 9 IMPLEMENT (file written; destination = this document).
- **Findings:** 7 entries; 1 surprise (LangShield — memory-based planning had missed it; read-first caught it).
- **Alternatives:** superiority-claim framing rejected as unverifiable at course scale.
- **Destination proof:** this file, read back post-write.

## Research pass #2 (2026-09-10, DDGS prior-art scan for the build phase)

New finds beyond the Sep 1 pass:

- **WajeehAlamoudi/QueryGuard (GitHub).** Same name, overlapping pillars: deterministic validation, read-only enforcement, schema-based column filtering. Independent convergence on our feature set — validating, but also a naming collision. Course use keeps the name; revisit before any public release (see DECISIONS.md D-010). Differentiators to state in the SRS: our MASK/SUGGEST actions, append-only audit log, labeled corpus with published verdicts.
- **guardrails-ai/valid_sql (GitHub).** Validates generated SQL by EXECUTING it against a live database. Opposite safety posture to ours (we judge on the parsed AST pre-execution). Good contrast paragraph: execution-based validation can run the attack once to find out.
- **tldrsec/prompt-injection-defenses (GitHub).** Practical-defense catalogue; usable as a citation bundle for the threat-model section.
- **Attack papers on text-to-SQL specifically:** TrojanSQL (EMNLP 2023, backdoor attacks on text-to-SQL parsers), ToxicSQL (arXiv 2503.05445, backdoor framework), DaMiT-SQL (2025, detection/mitigation review). Together with our six classes, these give the SRS related-work section published-attack grounding.
- **defog-ai/sql-eval (GitHub).** How industry evaluates LLM-generated SQL — reference for our harness/report design.
- **NVIDIA NeMo Guardrails** rechecked: still actively maintained (Aug 2026), still model-based classification — our Sep 1 positioning unchanged.


Net effect on the plan: no architecture change. The build already implements the differentiators this scan says matter (labeled corpus, published verdicts, explainable per-decision audit, masking). The collision + contrast findings feed SRS §1.4 references and the related-work paragraph.
## Research pass #3 (2026-09-12, GitHub-API + DDGS + live dry runs; operator-directed adversarial review)

Method note: first pass added GitHub REST as a discovery channel (now in the web-research skill); all repo claims below verified via api.github.com metadata (stars/pushed/license) this session.

**Related-work additions (postdate the March lit review):**
- Benchmarking Text-to-SQL under Role-Based Access Control (arXiv 2607.22115, Jul 2026) - closest new academic neighbor; SRS 1.4 + related-work item.
- "Text-to-SQL Benchmarks are Broken" (CIDR 2026) - corpus-design citation for the eval section.
- Semantic-layer challenge, now with OSS faces: dbt semantic-layer benchmark (Apr 2026, near-100% on covered queries), cube-js/cube (20.8k stars), tencentmusic/supersonic (5k, Chat BI). One related-work sentence: narrowing the surface (semantic layer) is the competing answer to guarding free-form SQL; we defend deployments without semantic layers.
- Practitioner consensus quartet (rietta.com, kkit.dev, adaptive.live, uniclaw.ai; Feb-Jun 2026): read-only enforcement at the engine, AST-level LIMIT injection, query timeout. Independent validation of our gap list.
- Shipped tools new since pass 2: arcjet-js (injection detection + tool-call authorization + data redaction). Tiny 2026 t2sql-guard clones (access-aware-text-to-sql, queryforge, text-to-sql-guardrails) keep converging on our feature set and ship rate limiting + caching - the two intake features our prototype lacks (TECH_PLAN mentions rate limit; code has neither; demo-scale assumption to state in SRS).
- Eval methodology: "metamorphic testing" is the formal name for the guard-tests-itself idea (semantically equivalent rewrites must not change verdicts); NVIDIA/garak (9.2k) probe taxonomy as prior art for the fuzz harness. Microsoft BIPIA (indirect-PI benchmark) optional cite.

**Tool verdicts (dry-run evidence, this session):**
- mvp.css 1.17.3 (MIT, 10KB): A/B tested by live injection on the running app, then ADOPTED - vendored at `queryguard/static/mvp.css`, loaded before style.css in base.html (custom stylesheet keeps precedence). Verified by post-restart screenshot.
- markitdown: FAILS legacy .doc (the course syllabus is a genuine Word Composite Document; markitdown handles .docx). LibreOffice also fails to load this file (twice, /tmp copy + clean profile; root cause UNKNOWN). `strings` extracts the text; course facts already live in 00_COURSE_INDEX.md - no derived file persisted.
- Figma-Context-MCP (15.8k, MIT) / FigmaToCode (5.2k): design-time-only aid; REJECTED for now (3 server-rendered pages; adds a tool chain for nothing the demo needs). Revisit only for a design-first UI pass.
- sqlfluff / sqruff / polyglot: REJECTED (sqlglot already parses and validates every candidate; a linter adds nothing the rule tests do not).
- terrastruct/d2: UNVERIFIED (API returned null this session) - do not cite until checked.
- diagram-design (38.7k, MIT) / archify (59.2k, MIT): agent skills for editorial HTML+SVG diagrams; candidate assets for the SRS presentation deck unit (alternative to Mermaid), not build dependencies.

**Gate findings from the same session (owner: DECISIONS.md + gate fix unit, next):** UNION exfiltration bypass (both arms PASS; root cause gate.py G-05 branch is Select-only; per-arm masking dry-run-verified feasible, empty-arm must BLOCK, nested unions need recursion), GROUP BY/ORDER BY/WHERE side channels (PASS by design; documented accepted risk or rule change decision pending), latency metric mismatch (FR-04 says gate-added; code times generator+gate+execution), engine-level second wall for reads via sqlite3 set_authorizer verified working at column level (writes already double-walled via mode=ro).

## Research pass #4 (2026-09-12, SM61 Part IV; operator-directed multi-pass: course-context + AI-era references)

Context: the operator redirected research toward the COURSE-project standard (stakeholders: Chen's
grading arc, Arwa, classmates, Project 2) and away from conference-paper framing. Multi-pass:
GitHub x3 queries, DDGS web x3, 2 primary sources read in full.

**SRS conformance yardstick (adopted):**
- IEEE 830 + ISO/IEC/IEEE 29148 quality characteristics (unambiguous, complete, consistent,
  ranked, verifiable, traceable, modifiable) - the standard's own checklist used to measure our SRS.
- jam01/SRS-Template (448 stars, CC0, IEEE 830 + 29148 aligned, verifiable-requirement patterns +
  traceability-ready ID schema): adopted as the structural yardstick. Conformance verdict: our SRS
  is strongest on verifiability/traceability/measured-results; 2 gaps queued for v1.1 (priority
  ranking, revision history) - see `submission/SUBMISSION_CHECKLIST.md` item 5.

**AI-era discourse (dated 2025-12 / 2026-01, read in full):**
- Graham Lee, "Is spec-driven development the end of Agile software development?" (sicpers.info,
  2025-12-12): a spec written before code is the same activity as test-first at a different
  abstraction level; agile's machine-readable spec was the test suite. Spec-driven development is
  not agile's refutation - it is the same discipline with a document as the artifact.
- Addy Osmani, "My LLM coding workflow going into 2026" (2026-01-04): "waterfall in 15 minutes" -
  brainstorm a spec.md with the AI, plan, then code in small tested chunks; ~90% of Claude Code's
  code is written by Claude Code itself; specs are the control artifact for code-generating agents.
- USE FOR: S8 close (speaker note, no slide change mid-review): "industry declared the SRS dead in
  agile; AI-era spec-driven development brought it back as the control artifact for code-generating
  agents - our SRS + gate is that artifact, measured (FPR 0, 384 metamorphic relations stable)."
  This is Chen's AI-era framing (lecture 1) with current industry receipts.

**Skills ecosystem (AI-agent skills, for adoption evaluation):**
- K-Dense-AI/scientific-agent-skills (44.7k, MIT, 166 skills, open Agent Skills standard):
  relevant to the research lane - literature-review, evidence-traceable scientific writing,
  peer-review-response workflow, citation management, database-lookup. Adoption = research-lane
  session decision (Sep 29+); install pattern: `gh skill install K-Dense-AI/scientific-agent-skills <skill>`.
- Ecosystem lists: ComposioHQ/awesome-claude-skills (75.0k), VoltAgent/awesome-agent-skills (34.2k,
  1000+ skills), hesreallyhim/awesome-claude-code (54.0k) - catalogued for future skill sourcing;
  no individual adoption this pass.

**Course-context calibration:** student SRS repos on GitHub are low-signal (1-star templates);
the authoritative course anchors remain Chen's own arc (requirement doc restated Aug 27/Sep 3/Sep 8,
XP practices, labeled-block slides) as captured in `../PROFESSOR_STYLE.md`. Course-project standard,
not conference standard - recorded so the next session does not re-mismatch the lens.
