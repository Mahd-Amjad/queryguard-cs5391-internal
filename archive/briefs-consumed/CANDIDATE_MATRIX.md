# CS5391 Project — Candidate Matrix (deep-dive)

**Created:** 2026-09-01 (CS5391-PROJ-1 in-depth evaluation, per operator direction: no rushing)
**Purpose:** pick the topic on evidence, not vibes. Read with `PROJECT_BRIEF.md` (candidates defined there).
**Status:** DRAFT — two inputs pending: group members + skills, group appetite (after Slack share).

---

## Decision criteria (agreed frame)

1. Rubric fit — does it generate strong proposal/SRS/review/presentation material?
2. Divisibility — can 3-4 people own separate chunks without stepping on each other?
3. Effort — buildable in ~4-5 weeks part-time (Group 2 is also 20%: total semester cost matters).
4. Demo risk — can it be demoed live without luck?
5. Course alignment — uses what Chen actually teaches (grading eye).
6. Operator leverage — where the operator's strengths save the team real time.

## UNKNOWN (blocking final call)

- Group members, their skill areas (frontend? data? writing?), weekly hours.
- Whether anyone insists on .NET (Chen's examples) vs free stack.
- Group's risk appetite: "impressive but tighter" (A) vs "safe and boring" (D).

## Candidates

| Criterion | A. AI-SQL Guard | B. CI/CD scanner | C. Requirements tracer | D. Plain CRUD |
|---|---|---|---|---|
| Rubric fit | **High** — natural FRs (guard rules = numbered, testable reqs), clean SRS, real review hooks | Medium — security rules make OK reqs; SRS thinner | Medium-high — meta-fit, but fuzzy correctness = weak review story | Low-medium — reqs exist but generic; nothing to review deeply |
| Divisibility | **High** — UI / API+LLM / guard rules+DB / tests+docs = 4 clean lanes | Medium — core engine + action wrapper + tests; UI-less so 4th person is thin | Medium — parser / matrix gen / test stubs / UI: parser and gen overlap | High — classic 4-way split |
| Effort (Group 2) | Medium — mock-LLM mode caps the risk; guard rules are the real work (good: that's the graded part) | Low-medium | Medium — parsing + LLM quality is unpredictable | Low |
| Demo risk | Low-mitigable — mock mode makes the live demo deterministic; one live-LLM query as the finale | Low — but visually dull (terminal/report) | Medium — output quality varies per run | Low — nothing can fail, nothing impresses |
| Course alignment | **All 7 lecture topics touch it** | git + security only | SE-process meta + AI-era | None of the AI-era angle |
| Operator leverage | **Max** — DB schema design, SQL injection knowledge, evaluation discipline | Medium — real-world CI knowledge | Medium | Low (overqualified for CRUD) |
| Main risk | Teammates see it as "the operator's project" — mitigate by assigning non-SQL lanes (UI, tests, docs) to others | Underscoped SRS | Correctness story hard to defend in review | Low grade ceiling; weak vs the other group if they build anything interesting |

## Recommendation (provisional until group inputs land)

**A**, with two commitments that answer the real risks:
1. **Mock-LLM mode first** — deterministic demo, zero API dependency for development; live LLM is a finale, not a dependency.
2. **Lane assignment that gives teammates real ownership** — UI, evaluation harness, docs/presentation are full lanes, not scraps. If the group skews non-DB skills, A still works; if the group wants minimum effort, D is the honest fallback and we say so out loud.

## Reference architecture — patterns borrowed from ZJP (internal design aid)

ZJP (the operator's production job-aggregation pipeline) already solved the architectural problems this project will hit. Borrow the patterns, not the code:

| ZJP pattern | What it means there | What it becomes in AI-SQL Guard |
|---|---|---|
| Single canonical truth layer | One store owns the data; nobody recomputes locally | One DB + one append-only audit log own "what ran, what was blocked, why" — UI and metrics are views over it, never parallel records |
| Mechanical gate over advocacy | The SDLC gate can't be skipped, so standards actually hold | The validation gate is *architectural*: no code path can execute SQL without passing the checker. That is the product's core claim |
| Named pipeline stages with contracts (AGG/ENR/SUP/…) | Each module does one job against a written contract | Five lanes, one per member: intake → LLM generation → validation gate → execution → audit/metrics. Each lane gets a one-paragraph contract in the SRS |
| Metric definitions registry | Metrics defined once, computed at write time | Block-rate, FPR, latency defined once in the SRS; computed when the query is processed, not re-derived per view |
| Decision records | Every significant choice logged with rationale and date | A `DECISIONS.md` in the repo — doubles as the "review" deliverable evidence for Group Project 1 |
| Blast-radius check | Trace all consumers before changing shared things | Change-management section of the SRS: what breaks if a guard rule changes (this is textbook SE-process material for the rubric) |

Why this helps beyond design: in the proposal and presentation, these patterns read as deliberate software engineering process — which is exactly what the rubric grades. Teammates get named, bounded lanes instead of a vague "we'll all work on the app."

### GitHub automation (from the actual repos: `Zapply/zapply-backend`, chrome-extension, `genai-dashboard`)

| ZJP machinery | Borrow? | Guard version |
|---|---|---|
| CI gate on push | **Yes** | One small workflow: pytest runs the guard-rule suite on every push; a red X on a broken rule is the project's thesis made visible. Chen literally taught "AI can draft the YAML; review before use" — this is on-lecture-material |
| `workflow_dispatch` evaluation run | **Yes** | A button that runs the full evaluation corpus and saves results as an artifact — repeatable evaluation instead of someone's laptop; this is Group 2's harness seed |
| README status badge | **Yes** | One line; free credibility in the demo |
| Path-filtered triggers, UAT/prod split, tag auto-releases | **No** | Overkill for a 4-person course project; one deploy path. Gold-plating infra burns Group 2 weeks on plumbing nobody grades |

### From the vision doc (the deeper borrow)

- **End-to-end slice rule:** ZJP counts a lane done only when it reaches the user — half-lanes don't count. Guard adopts it as the definition of done: a feature is finished only when prompt → LLM → guard → database → visible answer works as one path. This kills the classic course-project failure of three half-built pieces.
- **North-star metric:** ZJP optimizes one number (source-to-user latency). Guard's equivalent: **time from question asked to safe answer shown** — the demo's headline number and the tie-breaker for every design argument.

Advisory note: an optional dev-team sanity check of this mapping (via the operator's relay) is worth one message when the proposal drafts — the dev team owns the machinery and will spot misreadings. Not blocking.

## Effort sketch (Group 1 only, per candidate)

- A: proposal ~1 wk · SRS ~1.5 wk (12-15 numbered FRs) · review + presentation ~0.5 wk → fits by midterm with buffer.
- D: roughly half that — which is exactly the problem if the other group does more.

## Decision procedure (next session)

1. Slack replies → fill UNKNOWN block above.
2. Pick candidate + stack (free choice presumed; verify on Canvas project page).
3. Spin `project/proposal/` from the brief's skeleton; lane assignment goes in the proposal's team section.
