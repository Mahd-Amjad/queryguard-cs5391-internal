# Deck Rebuild Record (SM51 unit-record)

**Unit:** CS5391-PROJ-1 proposal deck rebuild inside the vendor's designed template (`budget_review_v2.pptx`, OfficeCLI vendor repo, direct download).
**Why:** operator rejected the months-old v2 reuse twice; template sourcing lesson applied (VISUAL_DELIVERABLE_METHODOLOGY Rule 1, updated this session).
**Method:** 9-step; Tier 3 template-first with a NEW acquired template; dump -> path-keyed text refill -> atomic batch (451/451) -> auditor-driven height fixes (15/15) -> gates.

## Mapping (budget template -> QueryGuard proposal)

| Slide | Was | Now |
|---|---|---|
| 1 | Budget cover | QueryGuard cover (kicker/title/subtitle/team) |
| 2 | Pull-quote on alignment | Thesis: check every generated query; CVE consequence |
| 3 | Overview + 4 numbered cards | PROBLEM: 3 CVEs / CVSS 9.8 / 50% ASR / 0 explanations |
| 4 | 3 big stats + insight | EXISTING DEFENSES: Retrain / Generic / Tools, with the gap as key insight |
| 5 | Expense breakdown + pie | SOLUTION: 4 components + planned-effort pie (40/20/20/20) |
| 6 | Variance chart | EVALUATION: corpus current-vs-target bar chart (6 published attack classes; starter 2/class, target 5/class) |
| 7 | 3 priorities | MILESTONES: proposal+SRS / build+CI / demo, each with receipt |
| 8 | Next steps + closing | Immediate action items (group confirm, Canvas capture, corpus growth) + closing line |

All chart data is PLANNED composition, clearly labeled; no research-project numbers were imported into the course deck (lane separation).

## Verification (destination)

- `batch`: 451/451 succeeded, 0 failed.
- `view issues`: 15 overflow findings from refill -> auditor's suggested heights applied (15/15) -> **0 issues** (re-checked after the refinement unit: still 0).
- `validate`: **passed, no errors** (cleaner than the v2-based build, which carried a replay-induced schema finding).
- Render snapshot: `PROPOSAL_DECK_snapshot.html` (regenerated for this deck; 0 placeholder tokens; 0 template leftovers: no "Budget", "FY 2024" strings remain).
- Charts: pie categories/data and bar title/categories/series verified present in render.
- CJK sweep (refinement unit): **0 Chinese characters across all package XML parts** after removing the cover's placeholder text box.

## Addendum 2026-09-01 (refinement unit)

- **Defect found and fixed:** the template carried a visible Chinese placeholder text box on the cover (`[ 流光背景图片 ]`, "flowing-light background image"). Removed; full-package CJK sweep now 0 chars.
- **New permanent gate:** every template-sourced deck gets a CJK/foreign-remnant sweep (slides, notes, layouts, masters, alt-text) before handoff — vendor example decks are authored with Chinese fixtures.
- **Template scout verdict:** vendor repo exhausted (90 .pptx files; only `budget_review_v2` is a usable designed deck; `Cat-Secret-Life` = Chinese humor fixture). Public galleries (Slidesgo/SlidesCarnival/Microsoft Create) remain the only source of a *different* designed template and need the operator's browser (2 minutes). Until then, the current dark-design deck is the best acquired candidate.
- Superseded build kept temporarily as `PROPOSAL_DECK_v2base_OLD.pptx` for comparison; delete after the operator's pick. **DISPOSITION 2026-09-04: operator picked candidate A (Sep 2) / DARK editorial (Sep 3) - v2base_OLD, both losing candidates (ALT, BLUEPRINT) + their snapshots, the predesignqa dump, and the WIP orphan moved to `../archive/proposal/` (retrievable, not deleted) per the CS5391-PROJ-1 cleanup gate.**

## Pending

1. Operator human design pass (`officecli watch` or the snapshot html): Tier 3 mandatory.
2. Team names/date on cover once group confirms.
3. Canvas format mapping when the project page posts.

## Addendum 2026-09-02: third candidate (blueprint design)

- **New acquisition:** `skills/morph-ppt/reference/styles/` in the OfficeCLI vendor repo holds **25 designed template decks** (dark/light/vivid/warm families) — the template sourcing gap is closed: 26 designed editable decks now known, direct downloads.
- **Built `PROPOSAL_DECK_BLUEPRINT.pptx`**: dark__blueprint_grid style (5-slide product-launch grammar: cover+tagline, problem, three pillars, 4 stats, close). 23 text slots refilled, 10 Chinese runs translated to QueryGuard content, charts n/a. Gates: issues 0, validation passed, visible-text CJK 0, snapshot regenerated.
- **New mechanical lesson (in SSOT pitfalls):** template packages may number slide parts non-sequentially AND carry Chinese in raw-XML slide parts invisible to the dump's set-commands — always (1) map sldIdLst -> rels -> parts to find REFERENCED slides, (2) sweep `<a:t>` runs per slide part with the officecli resident closed (live resident overwrites external disk edits).
- **Candidates now:** PROPOSAL_DECK.pptx (dark budget design, 8 slides) vs PROPOSAL_DECK_BLUEPRINT.pptx (blueprint launch design, 5 slides) vs PROPOSAL_DECK_ALT.pptx (SlidesCarnival startup, 17 slides). Operator picks after viewing the three snapshot html files.

## Addendum 2026-09-02 (SM53, night): operator picked candidate A for Sep 3 + design-QA pass executed

- **Decision (D1):** present candidate A tomorrow; the from-scratch rebuild (corrected method, shortlist on file in `REPO_LEARNING_PLAN.md`) becomes the Phase 2+ standard.
- **Gate-3 screenshot audit run on candidate A (the design-level check it never had):** per-slide screenshots + 12-item checklist caught what `view issues` missed - body sentences at 12-17pt across slides 3-8 (floor 18pt), two 34pt titles (floor 36), and a PRE-EXISTING collision: the closing epigram (y=18.3) sat on the footer text (18.06-18.76) on slide 8.
- **Fixes applied (dump backup first: `PROPOSAL_DECK_predesignqa_dump.json`):** 21 atomic size sets (intros/key lines -> 18pt; column sublabels -> 15-16pt within column-width limits; S5/S7 titles -> 36pt; authors 16pt), 8 height sets from auditor suggestions, closing epigram moved to slide-8 speaker notes (line removed - duplicated slide-2 thesis, no clean 18pt slot existed), row-3 icon nudge 16.65 -> 16.4cm.
- **Post-fix gates:** issues 0, validation passed, CJK sweep 0 (full package), resident closed + saved.
- **Residual (3-cycle stop, template-level):** slide-8 row-3 decorative hairline icons read as near-invisible at render scale (line #6A6458/6emu on dark card - template-wide trait); vision audit calls them "clipped" but geometry proves nothing crosses the 18.0 band. Left as-is per the fix-verify max-3-cycles rule. Column sublabels at 15-16pt are a documented partial-floor compromise (Zoom delivery, column width), not silent full compliance.
- **Honest floor statement:** titles 36pt+, intro/key sentences 18pt, column sublabels 15-16pt, kickers 10pt, footers 10pt (exempt). Pre-fix state was 12-17pt body throughout - this pass materially improved classroom/Zoom readability.
- **Speaker notes unit (Sep 3 morning):** deck previously had ONE notes element (slide-8 epigram); the pptx-v2 skill requires notes on every content slide (H7, "missing = not shippable"). Added cue-style presenter notes to slides 1-7 + rewrote slide-8's into the full version (timing cues totaling ~6.5 min, key sentences, numbers to emphasize, transitions, and the crib-sheet Q&A answers folded in at slides 4 and 6). Batch 8/8 atomic after one path fix (`/slide[8]/notes` is unindexed); verify: notes count 8, validate pass, issues 0, saved; readback spot-checked on slides 1 and 8.

## Addendum 2026-09-03 (SM53 morning): editorial re-skin built (operator go-ahead)

- **Unit:** apply the editorial-story style to the verified candidate-A layout as `PROPOSAL_DECK_EDITORIAL.pptx` (copy first - candidate A untouched as fallback). Answers the operator's "why haven't the slides improved": this is the visible-improvement path, structure and content preserved.
- **Method (v2d, after 3 failed iterations, each root-caused):** attribute-level XML color/font transform from the pristine copy. Iteration lessons: (1) element-span regex deleted alpha children -> XML corruption (fixed: attribute-level replacement only); (2) officecli's stale resident served phantom validation errors + can idle-flush old content over external edits (fixed: `OFFICECLI_NO_AUTO_RESIDENT=1` - now noted in SSOT pitfalls); (3) the template mixes namespaced tags (`<a:p xmlns:a=...>` vs `<a:p>`) - exact-string tag splits skipped whole shapes' text passes (fixed: prefix-tolerant split). Verify leftover-scan after every pass.
- **Transform:** all 8 slide backgrounds -> white; text palette -> slate 2C3E50 / muted 5D6D7E / red kickers C0392B; gold structural fills -> red E74C3C (accent-level) or near-invisible tints; dark cards -> light grays; greens dropped (slate); fonts Aptos Display -> Cambria, Aptos -> Calibri, theme fonts updated; charts: bar series -> slate, pie -> 4 dPt editorial colors (schema-order fix required after first insert); cover stripe that struck through the kicker removed; slide-6 caption repositioned flush under a shortened chart (latent candidate-A collision also present there - noted).
- **Gates:** validate pass, issues 0, CJK 0, notes carried (8), saved. Gate-3: "coherent white editorial deck: YES"; cover CLEAN; slide 6 CLEAN at full resolution.
- **State:** TWO ready decks - `PROPOSAL_DECK.pptx` (dark, unchanged) and `PROPOSAL_DECK_EDITORIAL.pptx` (light). Operator picks at the watch pass. Gallery: `style_gallery/EDITORIAL_full.png` + per-slide shots.

## Addendum 2026-09-03 (SM53, later): operator design review -> rubric + fix round

- **Operator review of the editorial deck found:** subtitle wrap/clipping on the cover, misaligned elements, thin visual interest, flat story, and admin trivia on the closing slide (all fair).
- **Root causes (geometry-verified, not guessed):** cover subtitle was a 15cm box for ~14.7cm of 22pt text (wrap risk) - and the naive widen ran the text UNDER the cover's opaque right panel (x=18+); "Retrain" at 72pt wraps to 2 lines in a 10cm column (was silently absorbing a 6.35cm box); slide-8 row titles (w=24) ran under the date chips (x=25.67); slide-6 caption/footer collision was inherited from candidate A; slide-8's "Capture Canvas project page" row was workspace-admin trivia unfit for a professor audience.
- **Fixes:** cover title/subtitle w=16.5 (clear of the panel, one line); Retrain 72->60pt (one line, hierarchy kept); S8 row titles w=21; slide-6 chart shortened 0.8cm + caption re-slotted flush; S8 content rebuilt professor-facing ("From proposal to working gate": confirm topic/lanes -> SRS + repo/CI live -> corpus starter in CI, with dates); titles now carry arguments (S5 "A transparent gate at the application layer", S6 "Measured, not asserted"); 2 timeline arrows added on S7.
- **RUBRIC created** at `.meta/DELIVERABLE_SPECS/presentation_pptx_spec.md` (8 dimensions x 0-5 anchors; <4 = iterate; geometry scan + fresh-eyes audit as the scoring instruments). Self-score of this deck: S1 story 4, S2 layout 4 (residual documented), S3 typography 4 (documented compromise), S4 color 4, S5 visual 3 (weakest - pipeline diagram on the solution slide is the identified lever, deferred), S6 credibility 4, S7 audience 4, S8 delivery 5. Nothing below 3; the 3 has a named next lever.
- **Iteration ledger this unit:** 4 correction rounds on the re-skin (span-regex corruption; resident phantom; namespaced tags; panel-overlap from naive widening) - each root-caused before the next attempt, per the fix-verify rule.

## Addendum 2026-09-03 (SM53, continued): pipeline diagram unit (rubric dimension 5 lever)

- **Unit:** replace the effort pie on the solution slide with the architecture itself - a 5-stage vertical pipeline (Intake / Generator / VALIDATION GATE in red / read-only Executor / Audit log) with down-arrows and the trust-boundary caption "Executor accepts only gate-passed queries". Rationale: the pie duplicated the effort split already carried by each lane's percentage; the pipeline IS the proposal's core claim. Pie removal is safe (labels + record keep the data).
- **Method:** officecli batch (10 shapes) + 3 caption iterations (wrap overflow -> one-line trims verified by `view issues`).
- **Gates:** validate pass, issues 0, saved. Render: `style_gallery/PIPELINE_slide5.png`.
- **Honest state:** mechanical verification complete; the fresh-eyes VISUAL audit is PENDING - the inspect_image device began failing ("Not Found" on verified-existing files, reported via report_issue) before the final visual pass. Do not treat the deck as visually signed off until a human watch pass or a recovered device audit.

## Addendum 2026-09-03 (SM53, final): dark sibling + verdict card + incident + PASS

- **Dark sibling built:** `PROPOSAL_DECK_EDITORIAL_DARK.pptx` - the editorial deck's dark theme (ink 121418 bg, warm off-white F2F0E8 text, red accents) derived via the context-split transform (fill-vs-text tables, white-text rule against new fill). Same story, layout, notes, pipeline diagram.
- **Verdict moment added to slide 2 (both decks):** "WHAT THE GATE SEES" card - prompt, LLM-drafted SQL (SELECT * FROM users; DROP TABLE users;), red BLOCKED stamp, verdict-logged line. The show-don't-tell proof the story lacked.
- **Final fixes:** slide-5 red divider dropped below the title band (was striking through "application layer" on both decks); slide-8 red hairline moved off the footer text.
- **FINAL GATE-3: both decks PASS all 8 slides** (white: PASS; dark: PASS, "no visible overlap, clipping, or unreadable primary text").
- **INCIDENT + RECOVERY (recorded for the lesson):** the verdict-card step triggered a file-destruction chain - a live officecli resident + external zip rewrite (the recorded write-trap), then a recovery script with (a) a loop-indent bug writing only the last zip entry and (b) an unanchored `x="` regex that matched inside `txBox="1"`. Both files were gutted to 1 part. Recovered cleanly from the mirror backup (9ef3cdc) + re-applied fixes with quote-safe, space-anchored, group-preserving replacements and NO officecli save/save-calls during external edits.
- **NEW SSOT pitfall (added to `.meta/ssot/OFFICECLI.md`):** `officecli save` under `OFFICECLI_NO_AUTO_RESIDENT=1` on a schema-BROKEN file writes a gutted 1-part package - validate FIRST, never save a file that fails validation; and anchor attribute regexes with the preceding space (` x="`) or they match inside `txBox=`.
- **Rubric re-score (both decks):** story 4, layout 4 (documented residuals), typography 4 (documented compromise), color 4, visual 4 (pipeline diagram + verdict card landed), credibility 4, audience 4, delivery 5. No dimension below 4. Remaining known lever for the next iteration: verdict-card microcopy at 13-14pt (readable at Zoom size, small in print).

## Addendum 2026-09-03 (SM53, final polish): dark deck designated THE deck

- **Operator decision:** the dark deck is the one being used; white + navy/gold remain as alternates.
- **Polish round on the dark deck:** chart legibility fixed properly (bars slate->light steel 8FA3B5; per-element txPr injected into catAx/valAx/legend after learning the renderer ignores chartSpace-level defaults — schema order matters: axis txPr goes BEFORE crossAx); chart title given explicit light color; hairline decor strokes widened 6emu->9525 (were invisible); slide-8 row-3 content nudged up; key-insight line shortened to a guaranteed one-liner ("The missing piece: a transparent, SQL-specific gate with measured false positives.").
- **Gates:** validate pass, issues 0, 57 parts, saved. Full render + per-slide shots in `style_gallery/`.
- **Documented residuals (accepted, template/design class):** slide-8 row-3 sits close to the footer (template bottom margin; 2 nudge rounds + geometry verified clear); verdict-card microcopy 13-14pt (Zoom-readable); column sublabels 15-16pt; footer 10pt muted by design.
- **Rubric re-score (dark deck):** story 4, layout 4, typography 4, color 5 (ink editorial is the strongest palette of the three), visual 4, credibility 4, audience 4, delivery 5 — **no dimension below 4**.

## Addendum 2026-09-03 (SM53, final): dark deck = THE deck; slide-8 alignment + cross-render verification

- **Operator decision:** the DARK deck is the presentation deck. White + navy/gold remain as alternates only.
- **Slide-8 alignment fixed:** the earlier nudge had scaled row-3 shapes proportionally (warping the row's internal offsets vs the +4.0cm rhythm of rows 1-2, and splitting the date chip from its background). Row 3 normalized to the exact row rhythm (title 14.9 / owner 16.5 / chip 15.5 / icons per row-1 offsets). Lesson: nudge rows with UNIFORM offsets only - proportional scaling warps by construction.
- **Accent inconsistency fixed:** row 1 used red accents, row 2 slate (original template inconsistency surfaced by the dark palette) - all three rows normalized to red bars/icons + red date text on dark chips.
- **Cross-render verification (the audit upgrade):** officecli's HTML renderer silently DROPS template-named shapes (`co_aown2_txt` owner lines, `!!Footer8`) - it had been under-reporting slide-8 content all along, which is why "footer/owner not visible" kept appearing in audits. Verified the deck in LibreOffice (headless PDF, PowerPoint-class engine): **all three rows visible, readable, evenly spaced; PASS**. Authoritative render archived: `style_gallery/EDITORIAL_DARK_LibreOffice.pdf`. Lesson added to the OfficeCLI SSOT.
- **Rubric re-score (dark deck, LibreOffice-verified):** story 4, layout 5 (overlaps fixed, rhythm normalized, verified in a second engine), typography 4 (documented microcopy compromise), color 5, visual 4 (pipeline + verdict card), credibility 4, audience 4, delivery 5. **No dimension below 4.**
- **Known residuals (accepted):** row-3 accent bar sits close to the footer hairline (template margin); verdict-card microcopy 13-14pt (Zoom-readable).
- **Content-staleness note (2026-09-03):** the white and navy/gold decks are CONTENT-STALE relative to the dark deck (no pipeline diagram, no verdict card, old slide-8 content, pre-QA text sizes). They are alternates for style comparison only; the dark deck is the single source of presentation content. Post-course cleanup gate: archive or rebuild them.
- **Watch pass = the human sign-off.** Everything is dump/script-backed and reversible.
- **Rubric note:** dimension 5 (visual interest) provisionally 3 -> 4 pending that visual confirmation; the pipeline diagram was the named lever.

## Addendum 2026-09-04 (SM55): rubric-scored iteration round — verdict-pair + pipeline slides EXECUTED

**Trigger:** the filed "rubric iteration round (verdict-pair slide, pipeline polish)" from the CS5391-PROJ-1 roller. Full process: truth render (LibreOffice, now installed) → vision panel on slides 2 + 5 → geometry extraction → fixes → re-render → vision re-verification. Backup: `PROPOSAL_DECK_EDITORIAL_DARK.predump_20260904.pptx` (byte copy).

**Fixes applied (DARK deck only — the designated presentation deck):**
1. **S2 verdict bar (was the slide's most unpolished element):** "BLOCKED - multi-statement escape" wrapped to two lines at 15pt in the 10.6 cm bar → set **14pt bold**: single line verified in render, still emphasized.
2. **S2 card body lift:** request 14→15pt, SQL 13→14pt, note 13→14pt (into/near the documented 15-16 sublabel band; heights verified no overflow).
3. **S5 copy defect (grader-stumble class):** left-column intro said "**Four components**" directly beside the **5-stage** pipeline diagram → "**Four workstreams**; each becomes a numbered SRS requirement and a team lane." Verified in render: the 40/20/20/20 workstream list and the 5-stage flow now read as two distinct structures.

**Post-fix gates:** validate PASS, issues 0, CJK 0; both revised slides re-rendered and vision-re-checked — zero regressions, no clipping/overflow.

**Residuals (documented, not silent):** (a) muted secondary text + subtle card border = documented palette compromise (contrast bump = palette change → full re-trigger; deferred unless the operator wants it); (b) "Validation gate" names both a workstream (S5 left) and stage 3 — optional qualifier if the operator wants the disambiguation; (c) dash-style mix (hyphen list vs em-dash diagram) — cosmetic; (d) 0/8 real title placeholders (textboxes throughout, per the established design; spec preference, structural change not attempted).

**Not applied to WHITE/NAVY alternates** (content-stale by decision; DARK is the presentation deck).

## Addendum 2026-09-05 (SM56): pre-submit vision pass — 2 defects fixed, deck re-verified

**Trigger:** operator focus directive (presentation + project). Full fresh pass: LibreOffice truth render of all 8 slides + per-slide vision sweep — the first pass since the cover-date change, and the first S6-specific visual check (SM55's vision panel covered S2+S5 only).

**Defects found and fixed (both destination-verified by re-render + vision):**
1. **S3 credibility defect:** stat card 2 read "CVSS 9.8 / PII extraction via AnythingLLM" — the audited numbers (research `text2sql_security/LITERATURE_REVIEW.md`) say AnythingLLM PII extraction CVE-2026-32628 = **CVSS 7.7**; 9.8 belongs to LlamaIndex CVE-2025-1793. Fixed 9.8 → 7.7 (citation-exact). The professor-checkable number is now correct.
2. **S6 wrap defect:** "< 50 ms" stat wrapped mid-unit ("50"/"ms" split) with the "0 silent regressions" figure crowding beneath. Fix iteration 1 (widen box to 3024000) FAILED the vision check — centered text collided with the "p95 gate latency" label. Fix iteration 2: compact stat to "<50ms" (same glyph class as the fitting "< 10%"), original box restored — single line, clear of label, column rhythm intact.

**Verified clean in the full pass:** cover date September 9, 2026; S2 single-line BLOCKED bar; S5 "Four workstreams" fix live; S7/S8 use relative date chips ("This week / Next two weeks / Before midterm") — the Sep 3→9 date move broke nothing. Pre-existing tight-but-clear spacings left untouched (S3 intro second line, "< 10%" label gap).

**Flagged for the operator (content decision, not changed):** S3 card 3 "50% ASR / attack success rate without defenses" has no direct audited anchor in LITERATURE_REVIEW.md (closest: 96% manual-attack baseline ASR; ">50% ASR bypasses all 8 tested defenses" — adaptive-attacks paper; 79.4% backdoor ASR). Confirm the source at the watch pass, or swap to "96% ASR" (stronger AND sourced).

**Backup:** `PROPOSAL_DECK_EDITORIAL_DARK.predump_20260905.pptx` (pre-pass state). Verified state: all 8 slides, LibreOffice render 2026-09-05.

**Unit record (SM51):** 1-3: record + QA crib + slide XMLs read; render pipeline live-tested. 4: CVSS numbers verified against the audited literature review at citation level. 5: two defects fix-ranked; ASR provenance flagged, not guessed. 6: two alternatives per defect (widen vs compact; relabel vs renumber) — compact chosen after iteration-1 vision failure. 7-8: backup → anchor-asserted scoped XML edits → re-render. 9: destination = fresh LibreOffice render + vision re-check, PASS.
Bias note: iteration 1 was my own unforced error (geometry looked right, pixels said no) — the render-verify gate caught it before handoff.
**Resolution (2026-09-05, same day — operator deferred the ASR call to the assistant):** card 3 swapped 50% → 96% ASR ("Attack success rate without defenses"; 96% is the published manual-attack baseline success rate, LITERATURE_REVIEW.md StruQ comparison table). Fresh backup predump_20260905b, anchor-asserted XML swap, LibreOffice re-render + vision check PASS. All four S3 stat cards now trace to audited sources.
**Retirement (2026-09-05, operator cleanup directive):** DARK deck + all three predumps moved to `project/archive/proposal/` after the operator picked the presenton direction. DARK served as designated deck Sep 2-5 with the fix rounds recorded above; retrievable from the archive. Fallback while presenton v2 generates = the v1 presenton candidate (figures correct; known v1 flaws: 4-member closing slide, Sep 5 date stamp).

## 09-08 update unit (SM57): date fix + pipeline diagram + REVIEW STANDARD recorded

- **Date fix:** slide 6 "September 9" → "September 10" (SE class verified Tue/Thu; informal update session, not formal presentation).
- **Pipeline diagram ADDED (slide 4 top band):** 5 roundRect nodes — Intake / Generator / VALIDATION GATE (accent 9333EA) / Executor / Audit Log — + 4 rightArrow connectors, Poppins, atomic batch 9/9 → `validate` clean → `view issues` 0 → on-disk XML + render verified. Added shape ids 100000–100008 (revert = remove those ids). Existing stage blocks untouched (diagram is the overview; blocks are the walkthrough).
- **Snapshots:** `style_gallery/presenton_v2_diagram_20260908.html` = CURRENT/FINAL for the Sep 10 watch pass. Older: `presenton_v2_datefix_20260908.html` (pre-diagram), `presenton_v2_general_20260905/` (pre-date-fix).

## STANDING REVIEW/ACCEPTANCE STANDARD (recorded 09-08 — fixes the per-session drift the operator flagged)

**Why drift happened:** no recorded acceptance criteria or review procedure for this deck — each session improvised a display/review mechanism (presenton renders, gallery HTML, live watch server) and "SHIP-READY" was declared on text accuracy + render cleanliness alone, with no visual-completeness or date-verification gate.

**A session may declare SHIP-READY only when ALL pass:**
1. Content accuracy: names, figures, dates verified against workspace records (not memory).
2. Class date/day verified against the actual class schedule (SE = Tue/Thu).
3. Visual completeness: every flow/comparison slide carries a native graphic — no text-only diagram slides.
4. `officecli validate` clean + `view issues` 0.
5. Fresh style_gallery HTML render exists and key strings verified in it.
6. Operator watch pass on that render.

**Review/display procedure (one mechanism, not per-session inventions):** the style_gallery HTML snapshot IS the review surface — regenerate it after every change (`officecli view html -o`), verify key strings in it, hand the operator the file. The live `officecli watch` server is optional for interactive editing sessions only.
