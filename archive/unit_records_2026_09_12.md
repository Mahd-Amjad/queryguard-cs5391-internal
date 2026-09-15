# DECISIONS.md unit records (extracted verbatim 2026-09-15, SM62)

Provenance: five session-process "Unit record" blocks moved out of DECISIONS.md
(D-019: the decision log holds decisions; process records live in archives).
Label correction: the originals say "SM59"; the work they describe (gate fix,
UI units, Tabler rebuild, repo bring-up, restructure) was executed in session
SM60 (chronicle SESSION_SM60_2026_09_12.md units 5-9) - SM59 is the same-day
meta-audit session. Originals kept verbatim below, labels unmodified.

---

## [was DECISIONS.md lines 41-42] gate-fix unit

## Unit record (SM59 gate-fix unit, 2026-09-12)
Steps: 1 READ (gate/db/app/generator/test_rules/test_app/run_eval/corpus/candidates at destination; DECISIONS D-001..D-010) · 2 UNDERSTAND (consumers: app verdict contract, harness compare per D-006/D-008, test conventions) · 3 EXPLORE (full project surface incl. archives earlier this session; no prior compound handling existed) · 4 RESEARCH (live probes: bypass reproduced pre-fix, per-arm masking feasibility proven, nested-union left-deep shape, distinct flag carries UNION vs UNION ALL) · 5 REVIEW (scope held to gate+data+tests+decisions; SRS wording deferred to the v1.0 unit; builder bias guarded by minimal scope; confirmation bias countered by reproducing the bypass before the fix and re-running it after) · 6 IDEATE (per-arm masking vs BLOCK-all; side-channel BLOCK vs accepted-risk — D-011/D-012) · 7 DRY RUN (nested-union parse probe; earlier live MASK feasibility probe) · 8 PLAN (gate -> data -> tests -> verify) · 9 IMPLEMENT (gate.py: _nonprojection_sensitive helper, compound-arm handler, Select side-channel check; candidates.json +4; corpus.jsonl +4 = 64; test_rules.py +7; test_app corpus-count pin converted from hardcoded 60 to corpus-derived total). VERIFY: pytest 37/37; run_eval --fail-on-miss 64/64; live HTTP after app restart: UNION BLOCK / UNION ALL MASK / GROUP BY BLOCK / benign PASS. Honest note: one self-inflicted import drop during the test edit, caught by the suite on the next run and restored.

---

## [was DECISIONS.md lines 47-48] UI unit

## Unit record (SM59 UI unit, 2026-09-12)
Steps: 1 READ (style.css, ask/metrics/base templates, make_dark_theme.py palette, test_app pins — at destination) · 2 UNDERSTAND (consumers: operator demo, grader eye, Arwa's UI lane; failure mode = breaking pinned strings or demo flow) · 3 EXPLORE (found metrics page already double-served as audit log — split concerns instead of adding a duplicate table; found POST-only /ask, page lives at /) · 4 RESEARCH (palette = deck SSOT script; verdict-UX guidance from the earlier block-explanation search; no new external claims) · 5 REVIEW (builder-bias guard: no JS framework, no build step, templates-first, 3 pages only; scope = B.5 spec items) · 6 IDEATE (bespoke dark stylesheet vs mvp var overrides — chose bespoke, mvp unlinked; separate audit page vs keeping log on metrics — chose split) · 7 DRY RUN (suite after templates; POST-only /ask caught live, retried from /) · 8 PLAN (css -> templates -> routes -> verify) · 9 IMPLEMENT (style.css rewritten token-driven; ask.html split panes; metrics.html stat cards + bars; audit.html new; base.html nav + Audit link; app.py metrics_view computed stats + audit_view route; +1 audit render test). VERIFY: pytest 38/38; corpus 64/64; live screenshots of ask (MASK split), metrics (bars), audit (pagination) after restart. Honest note: one base.html mis-anchor during edit (brand span swapped for nav) caught by immediate read-back and repaired same turn.

---

## [was DECISIONS.md lines 53-54] plain-language UX unit

## Unit record (SM59 plain-language UX unit, 2026-09-12)
Steps: 1 READ (all four templates + app routes + explain targets at destination) · 2 UNDERSTAND (consumers: first-time demo viewers, grader, operator; failure mode = jargon without meaning) · 3 EXPLORE (existing "What the gate checks" card was buried on the ask page; promoted to its own page) · 4 RESEARCH (none new; earlier block-explanation UX guidance applied) · 5 REVIEW (scope: copy + one new page + one data module; no engine changes) · 6 IDEATE (context processor injection vs per-route passing — chose context processor so every template gets helpers) · 7 DRY RUN (suite after wiring) · 8 PLAN (explain.py -> app wiring -> templates -> verify) · 9 IMPLEMENT (explain.py; app.py import + context processor + /ui/how route; how.html; ask/metrics/audit plain copy; base nav + How it works; +1 how-page test). VERIFY: pytest 39/39; screenshots of ask (MASK), how, metrics, audit after restart.

---

## [was DECISIONS.md lines 59-60] Tabler rebuild + repo bring-up unit

## Unit record (SM59 Tabler rebuild + repo bring-up unit, 2026-09-12)
Steps: 1 READ (review-rigor skill loaded — the default conclusion skill this session had skipped; test pins; gh auth state) · 2 UNDERSTAND (failure mode = research theater: collecting references and then building from scratch anyway) · 3 EXPLORE (gh CLI authenticated as Mahd-Amjad; D-010 name-collision note; existing repo list checked for collisions) · 4 RESEARCH (Tabler chosen as reference: highest-star OSS dashboard kit, single-file CSS, dark theme built in, no JS needed for our pages) · 5 REVIEW (scope: templates + css + test pins + repo init; engine untouched) · 6 IDEATE (vendor full Tabler CSS vs hand-copy its look — chose vendor, the entire point of the correction) · 7 DRY RUN (suite after rebuild caught 2 stale test pins — fixed by asserting behavior: plain rule name, takeaway heading — plus one tautological assert removed on sight) · 8 PLAN (css -> templates -> tests -> verify -> repo) · 9 IMPLEMENT (tabler.min.css + custom.css vendored; base/ask/metrics/audit/how rebuilt on Tabler structure; style.css link removed; QA_CHECKLIST.md created at project root as the standing gate for every future unit; git init + commit 2dcadcf, 31 files). VERIFY: pytest 39/39, corpus 64/64, screenshots of 4 pages post-restart. BLOCKED (operator-held, 1 click): GitHub token lacks createRepository scope; local repo + workflows ready; after the operator creates private repo queryguard-cs5391 (or widens token scope), push is one command and CI runs the push gate for the first time.

---

## [was DECISIONS.md lines 68-69] restructure unit

## Unit record (SM59 restructure unit, 2026-09-12)
Steps: 1 READ (full inventory incl. assignments/group_project location, TECH_PLAN boundaries) · 2 UNDERSTAND (consumers of every path: course index, SRS, README, scan) · 3 EXPLORE (archive/ already held absorbed planning; proposal/ mixed delivered vs draft) · 4 RESEARCH (n/a local) · 5 REVIEW (scope: moves + dedup + pointers; no engine or content rewrites except the two path references) · 6 IDEATE (rename prototype/ to app/ rejected: reference churn across course surfaces outweighs cosmetic gain) · 7 DRY RUN (suite after moves: 39/39) · 8 PLAN (move -> dedup -> pointers -> entry README) · 9 IMPLEMENT (3 briefs + 2 proposal drafts archived; DECISIONS to root; SRS renamed; TECH_PLAN 524->317 lines; project/README.md new; prototype/README.md rewritten to current truth; course index path fixed). VERIFY: tree listed at destination, suite green, read-backs of every edited file.
