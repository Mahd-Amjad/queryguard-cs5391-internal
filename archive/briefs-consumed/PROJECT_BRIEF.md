# CS5391 Group Project — Working Brief (Phase 1)

**Created:** 2026-09-01 (session unit: CS5391-PROJ-1 Phase 1b prep)
**Status:** group FORMED (operator + Arwa Arafeh); **topic A "QueryGuard" LOCKED per operator direction 2026-09-02** (pending group social confirmation); proposal presentation Thursday.
**Purpose:** everything needed to pick the topic in the next group meeting and start the proposal/SRS immediately after — grounded only in captured course facts; no fabricated requirements.

---

## 1. Evidence base (what this brief is built on)

| Fact | Source | Label |
|---|---|---|
| Project is **student-defined** (no assigned topic list) | Lecture 1 transcript capture (`notes/2026-08-20_Lecture01_NOTES.md`) | FACT |
| Groups of 3-4; ~2 groups expected; form after first class | Lecture 1 + syllabus (via transcript) | FACT |
| Group Project 1 = proposal + presentation (10%) and SRS + review + presentation (10%), due **by midterm** (date TBA) | Canvas grading capture -> `00_COURSE_INDEX.md` | FACT |
| Group Project 2 = implementation + demo (20%), second half | Canvas grading capture | FACT |
| No late work accepted, ever | Syllabus (transcript + index) | FACT |
| Chen's lecture arc: SE in AI era -> full-stack dev -> AI-generated apps (.NET) -> database integration -> performance/scalability -> security/auth -> git | `lectures/slides/` 1-7 | FACT |
| Raw Canvas project page (proposal/SRS format, rubric, any topic constraints) | **NOT CAPTURED** | UNKNOWN |
| Course examples use .NET; whether the project stack must match | not stated anywhere captured | UNKNOWN |
| Midterm ~mid-semester -> proposal/SRS runway is roughly 4-6 weeks | derived from "by midterm" | INFERENCE |

---

## 2. Topic candidates (bring to the group; pick one)

Selection criteria: maps onto Chen's lecture arc (grading eye), buildable + divisible by 3-4 people in ~6 weeks, demos well, reuses operator strengths (DB design CS5332, algorithms CS5329, LLM-SQL security research).

### A. "AI-SQL Guard" — review gate for LLM-generated SQL (RECOMMENDED)
Natural-language questions over a demo database; an LLM drafts the SQL; a **review layer** checks it (destructive-statement block, injection-pattern detection, schema allowlist) before execution; results render in a simple web UI.
- **Why it wins:** touches every module Chen teaches — full-stack UI, database integration, security, AI-era SE, git — so lectures double as project guidance. Operator's home turf (19-table Oracle design, normalization, SQL review patterns from the research project). Demo is visual and reliable (deterministic guard rules demo better than raw LLM output).
- **SRS writes itself:** functional reqs = query flow + guard rules + audit log; non-functional = safety (nothing executes unchecked), latency, usability.
- **Boundary note:** this is a *course tool demo*, NOT the research paper's artifact — no shared code, naming, or claims. Keeps the two lanes clean.
- **Risk:** LLM API key/cost for the group. Mitigation: mock-LLM mode (canned generations) for dev/demo, live LLM optional.
- Stack suggestion: Python/Flask or Node + SQLite/Postgres (operator + typical group familiarity). .NET only if the group prefers matching lecture examples.

### B. CI/CD workflow security scanner (GitHub Action)
A linting action that checks repo workflows for common CI/CD security mistakes (overbroad permissions, unpinned third-party actions, secret exposure) and reports findings.
- **Wins:** small, sharply scoped, real-world relevance; aligns with git + security lectures.
- **Loses:** little database/full-stack content (weak coverage of Chen's arc); less visual demo; thin SRS surface.
- Best if the group wants minimal risk over breadth.

### C. Requirements-to-test traceability tool
Parses a structured SRS (markdown) and generates a traceability matrix + stub test scaffolding, LLM-assisted.
- **Wins:** most "meta-SE" — directly exercises the SE process Chen grades on; nice fit with the requirements lecture.
- **Loses:** LLM-output quality is hard to guarantee; demo less impressive; evaluation story ("correct traces") is fuzzy.
- Interesting, but harder to scope than A.

### D. Plain CRUD web app (fallback)
Standard tracked-issue app (e.g., event finder — the CS5332 project was exactly this shape).
- **Wins:** lowest effort, well-understood, easy to divide.
- **Loses:** zero differentiation, wastes operator strengths, ignores the AI-era theme the course opened with. Chen sees ~2 groups; the comparison will be direct.
- Only if the group wants minimum viable.

**Recommendation: A**, with B as the low-appetite alternative. Decide stack with the group (see UNKNOWNs).

---

## 3. Proposal outline (liftable once topic is picked)

Standard SE-proposal shape; adjust to whatever the Canvas project page actually requires once captured.

1. **Problem statement** — the pain, one paragraph, concrete.
2. **Motivation** — why now (AI-generated code needs guardrails), who cares.
3. **Objectives** — 3-5 measurable bullets (each must be demoable/checkable).
4. **Proposed solution** — architecture sketch: components, data flow, key decisions.
5. **Scope** — in-scope list AND explicit out-of-scope list (the out-of-scope list is what keeps Project 2 feasible).
6. **Team & roles** — per member: area ownership + backup.
7. **Tools & stack** — with one-line justification each.
8. **Milestones** — mapped to the real course deadlines below.
9. **Evaluation plan** — how we'll show each objective met (test, metric, demo step).
10. **Risks & mitigations** — top 3 only (e.g., LLM availability -> mock mode).

## 4. SRS skeleton (IEEE-830-shaped, liftable)

1. **Introduction** — 1.1 Purpose, 1.2 Scope, 1.3 Definitions/acronyms, 1.4 References, 1.5 Overview
2. **Overall description** — 2.1 Product perspective, 2.2 Product functions, 2.3 User classes, 2.4 Operating environment, 2.5 Design & implementation constraints, 2.6 Assumptions & dependencies
3. **Specific requirements** — 3.1 External interface requirements (UI, API, DB), 3.2 Functional requirements (numbered FR-1..n, each with trigger/input/processing/output — **the guard rules live here**), 3.3 Performance requirements, 3.4 Design constraints, 3.5 Software system attributes (reliability, security, maintainability), 3.6 (optional) organizing info for Project 2
4. **Appendices** — data model / schema reference, glossary

Write FRs as testable one-liners ("The system SHALL reject any generated statement containing DROP/ALTER/TRUNCATE and log the rejection") — each FR becomes a Project 2 test case. That traceability is exactly what the "review" component of Group Project 1 is about.

## 5. Capture checklist (from Canvas / next class — the missing raw spec)

- [ ] Canvas project page: exact proposal format (doc? slides? length?), SRS format/template, rubric weights
- [ ] Any topic constraints or approval step (does Chen sign off on topics?)
- [ ] Exact midterm date (= real Group Project 1 deadline)
- [ ] Stack expectations (free choice vs .NET)
- [ ] Group member names + contacts; who presents
- [ ] Literature-review quiz announcements (parallel track — do not let them sneak up)

## 6. Backward timeline (from assumed midterm ~Oct 12-16; refine when date is known)

| Week of | Milestone |
|---|---|
| Sep 1-5 | Topic agreed in group; Canvas spec captured; roles drafted |
| Sep 8-12 | Proposal draft v1 circulated; data/schema sketch |
| Sep 15-19 | Proposal finalized + presentation built (deck per pptx spec, OfficeCLI-verified) |
| Sep 22-26 | **Submit/present proposal** (buffer before midterm) |
| Sep 29-Oct 10 | SRS draft -> group review pass -> SRS + review + presentation submitted **before midterm** |
| post-midterm | Project 2: lock architecture, build, demo |

## 7. One-line group pitch (for candidate A)

> "An AI assistant that writes SQL from plain-English questions, plus a safety layer that reviews every query before it touches the database — so we cover full-stack, database, security, and AI-era SE in one demoable project."

---

**Next unit:** topic confirmed by group -> create `project/proposal/` + `project/srs/` working files from sections 3-4, load `PROFESSOR_STYLE.md` (fill Section 2 anti-AI deltas from Chen's own decks before drafting), draft to the captured Canvas rubric.
