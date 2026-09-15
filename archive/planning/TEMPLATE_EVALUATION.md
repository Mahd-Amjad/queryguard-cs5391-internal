# Template Acquisition and Redesign Plan (proposal deck)

**Created:** 2026-09-01 (CS5391-PROJ-1; operator-directed template sourcing + design exploration). **Revised 2026-09-01 later same day:** design critique corrected after actual fill inspection.

---

## 1. Sources explored (all verified live this session)

| Source | Result |
|---|---|
| GitHub template repos | Mostly templater TOOLS (libraries that fill templates), not designed decks. One candidate skills repo had no bundled .pptx |
| ai-ppt-template/free-ppt-template (595 decks, CC BY 4.0, direct CDN downloads) | **UNUSABLE: decks are picture-flattened** (0 editable shapes, 0 words, 10 pictures per deck) - verified on the top 3 tech/security candidates. Cannot content-fill |
| ppt-master (51k stars) | No bundled .pptx templates (generates dynamically) |
| OfficeCLI vendor repo examples | `budget_review_v2.pptx`: a DESIGNED 8-slide business deck (cover with kicker/title/subtitle/division, pull-quote transition slide, numbered overview cards). `Alien_Guide.pptx`, chart examples: exercise fixtures |
| Slidesgo / SlidesCarnival / Microsoft Create | Professional templates exist but downloads are browser/account-gated for automation; 2-minute operator download path works |
| GLM Slide Agent | API not exposed (key lists only base GLM chat models); chat.z.ai browser use = operator-only; PDF-only export anyway (operator: skipping) |

## 2. Design assessment of the current deck (CORRECTED - assumption retracted)

Initial written critique ("white background, plain, no palette identity") was an UNVERIFIED ASSUMPTION and is retracted. Verified fill inventory: the deck is a **cohesive dark design system** — full-bleed `#0A0F1A` backgrounds on all 13 slides, sky-cyan `#38BDF8` accent underline on every slide, dark card containers `#111C28` (stat cards, the five defense camps, pipeline boxes), cyan accent chips on the pipeline. It is composed, not plain.

What remains open is a TASTE question, not a defect question: whether the operator prefers this dark system, a re-accented variant, or a light/different identity. That call needs the operator to SEE the deck (render snapshot or `officecli watch`), not another assistant assumption.

## 3. Options (revised to match reality)

| Option | Scope | Notes |
|---|---|---|
| A. Keep the dark system, operator renders and gives a verdict | Zero build effort; possible small tweaks (accent hue, card contrast) from the verdict | Recommended first step: `officecli view PROPOSAL_DECK.pptx html -o snapshot.html` or `officecli watch` |
| B. Re-accent the existing dark system | Small: swap the `#38BDF8` accent family (e.g., to the supporting blue `CADCFC` + a red `C0392B` reserved for BLOCK verdicts) | Review-gated edits on the live deck |
| C. Operator downloads 1-2 Slidesgo/SlidesCarnival templates they like | 2-5 min operator; assistant rebuilds the deck inside the winner | The "designed look" path if the dark system is judged plain |

Constraints kept in all options: explicit fonts everywhere, contrast floors, spec margins/grid, one palette.

## 4. Retained lessons recorded this session

| Lesson | Disposition |
|---|---|
| Same-course reuse is a template FALLBACK, not template sourcing; search public/vendor sources first | Added to VISUAL_DELIVERABLE_METHODOLOGY Rule 1 (done) |
| Gate rules need SQL AST parsing, not substring matching | In TECH_PLAN (done) |
| Silent REWRITE removed; BLOCK/MASK/SUGGEST only | In TECH_PLAN (done) |
| Edit anchors must come from same-turn reads | SM51 control; 3 stale-anchor slips this session, all caught by read-back — pattern named in SM51 chronicle |
| Clipped-read text is never pasted as-is | Applied (abstract completion re-extracted) |
| Inspect before critiquing (the deck critique was written without reading fills) | NEW - same family as verify-at-destination; applied in this revision |
| hallucinator.science reference validation before security-paper submissions | In field sheet pre-flight |
| GLM Slide Agent: design-reference only until PPTX export ships; API not exposed (key lists base models only) | Monitored in SSOT; re-verified live 2026-09-01 |

## Unit record (SM51 control)

Steps: 1 READ (vendor skill design principles in full; spec sheet; methodology Rules 1-5) · 2 UNDERSTAND (consumers: operator review pass, Chen, class; failure mode: redesigning a deck that was never actually seen) · 3 EXPLORE (5 sources verified live; full fill inventory extracted from the real file) · 4 RESEARCH (vendor palette seeds; budget deck design system inspected at destination) · 5 REVIEW (3 acquisition routes dispositioned; redesign deferred pending operator visual verdict) · 6 IDEATE (3 options tabled; assumptions stripped) · 7 DRY RUN (palette contrast checks; options tested against the verified inventory) · 8 PLAN (this file) · 9 IMPLEMENT (acquisition findings + corrected assessment delivered; deck edits deliberately deferred to the operator's visual verdict).
Findings: the deck already has a design system; the "plain" critique was wrong; the earlier §3 redesign plan was built on that wrong premise and is replaced by the options table.
Alternatives: redesign now on assumption (rejected - exactly the bias pattern the operator flagged).
Bias note: this unit caught its own unverified-assumption bias before executing an unnecessary redesign; the earlier wrong critique is preserved in the chronicle trail rather than silently deleted.
