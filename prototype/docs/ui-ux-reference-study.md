# UI/UX Reference Study - Zapply products + SoftwareJobs.dev

**Date:** 2026-09-15 (SM62, operator-directed study unit; no implementation).
**Sources studied:** live zapply.jobs (rendered + built CSS, 44.5KB) · live softwarejobs.dev (rendered + built CSS, 49.1KB) · `Business/Zapply/zapply-web-app` source (App Router, index.css 311 lines, providers.tsx, ThemeContext) · `Business/Zapply/zapply-backend` (repo survey). The landing's own Astro source is NOT in the local repos - its built output was studied instead.

---

## 1. The Zapply design system (one system, three products)

One token set spans marketing (zapply.jobs), board (softwarejobs.dev), app (app.zapply.jobs):

- **Canvas:** white (marketing/board), brand ink #231f20 (app + footer/dark sections).
- **Ink:** #231f20 near-black; secondary #808080/#b8b8b8.
- **Accent:** #ff5e3c, hover #ff6b4a, pressed/gradient #e45638; dark-mode accent LIGHTENS to #ff8a6b (contrast-first: the accent changes per theme instead of staying fixed).
- **Buttons are a two-family system:** (1) primary = black gradient (#231f20 -> #514a4c, white text) for neutral-primary actions; (2) accent = orange gradient (#ff5e3c -> #e45638, white text) for the money action. Hover = gradient shifts angle/color + a drop shadow that is DEFINED AS A TOKEN PAIR with the gradient (`--light-gradient-hover` + `-shadow`) so they always move together.
- **Type:** Montserrat 400-800 everywhere, Caveat 400-700 as the handwriting accent for emphasis words inside headlines ("in *Seconds*.", "*Software Job.*"). Body sizes 14-18px; display sizes 48-56px - a 4x scale contrast that IS the look.
- **Radii:** 10px dominant, 16px cards, 999px pills. Borders #e0e0e0 / rgba(0,0,0,.08).
- **Surfaces are gradient-layered, not flat:** hero = linear-gradient(#e8e8e8 -> #fff); chart sections get their own gradients; stat grids sit on rgba(232,232,232,.4) + an SVG texture; FAQ on #fff -> #fffaf8. Depth comes from these subtle washes, not heavy shadows.

## 2. Theme methodology (the part we got wrong)

- **Token count with 1:1 light/dark parity:** the app's index.css defines ~120 custom properties by ROLE (`--color-bg-jobs-section`, `--selected-job-bg`, `--color-edit-accordion-header`), and the dark block redefines every one. Nothing falls through; no component hardcodes a color.
- **Dark mode is warm and inverted, not dimmed:** dark background = the brand ink #231f20; dark text = warm cream #d1cfc0 (never pure white); the accent lightens; BUTTON COLORS INVERT (cream gradient + black text on dark). Dark mode is a designed counterpart, not a brightness slider.
- **Theme switch mechanics:** a `dark` class on html (server-rendered to avoid flash), cookie persistence (365 days), a tiny React context exposing isDarkMode/toggleTheme. Body carries `transition: background-color .25s ease, color .25s ease` so the switch animates.
- **MUI is deliberately subdued:** the MUI theme sets only fontFamily + borderRadius 8px - all real theming lives in the owned CSS variables. Framework chrome is minimized.

## 3. Genre patterns (what transfers to QueryGuard)

QueryGuard is a data-dense tool - the closest genre is softwarejobs.dev (the board), not the marketing page. Patterns observed there, all demonstrated live:

| Pattern | Evidence | QueryGuard application |
|---|---|---|
| Numbers as credibility | hero strip: "18,541 ACTIVE JOBS · 821 COMPANIES · 15M REFRESH CADENCE" | metrics tiles already do this; lead with total + attacks-stopped |
| Freshness/transparency line | "Last updated: 9/15/2026, 1:54:16 PM" under the table | audit view: "last entry" timestamp from the API |
| Cadence badge | pulsing-dot pill "BOARD REFRESH EVERY 15M" | metrics: "live - refreshes every 5s" pill |
| Row genre | logo / title / location / posted / level pill / category / per-row CTA | audit rows: verdict pill + rule + question + latency - badges per row, not raw text tables |
| Pagination done plainly | numbered pages + Prev/Next + "Page 1 of 1855 · 1854 jobs" summary line | audit pagination summary |
| Pill badges for enums | "SENIOR" / "HYBRID" pills | verdict + rule pills (already shipped) |
| One CTA per row | orange Apply per job | per-row action reserved (Project 2: "explain this verdict") |
| Dark footer bookends the page | #231f20 footer with newsletter | candidate: dark footer strip on the how page |
| Script accent in headlines | Caveat words inside H1/H2 | ours: sidebar tagline + one accent word per page title |

## 4. Accessibility observations

- Good: single H1 with clean H2 section order; 148 aria attribute occurrences on the landing; semantic button/anchor elements everywhere (13 buttons, 35 links, all text-labeled); visible focus styling in the built CSS.
- Gap found (do not copy): 73 img tags vs 11 alt attributes - the company-logo ticker images are decorative but unmarked (no empty-alt/aria-hidden). Our rule: decorative SVGs get aria-hidden, informative icons get labels, every img carries alt.
- Contrast: ink #231f20 on white = 16.3:1; accent #ff5e3c on white = 3.2:1 (fine for large text/buttons, not for body copy - they never use accent for body text; we must not either).
- Selection styled (::selection accent) - small dignity detail worth copying.

## 5. Methodology findings (how they build)

- Owned semantic CSS: 435 rules (landing) / ~49KB (board) - no CSS framework, custom properties by role, ~11 media queries per site. Hand-authored, tiny, complete.
- Astro for BOTH content properties (static, zero-JS by default); Next.js+MUI only where the product is genuinely interactive. Genre decides the stack, not fashion.
- The brand system is ONE css file per property (311 lines in the app) - a designer could re-theme the whole product from that single file. That is the real design system: a complete, role-named token file with enforced light/dark parity.

## 6. Transfer plan for QueryGuard (prioritized; NOT implemented - Phase 2 continuation)

1. **Complete the token file to zapply parity:** every surface/state in our four views gets a role-named variable; dark block redefines 100% of them; accent lightens on dark (#ff8a6b-class shift); button pairs (gradient + shadow) as tokens. Current gap: our dark block covers ~12 of ~40 effective surfaces.
2. **Type-scale contrast:** one display size (48-56px) for page heroes (ask headline), 14-16px body. Today our pages are uniformly small - the flatness reads as template.
3. **Gradient washes** on hero/metrics section backgrounds + hover token pairs on buttons.
4. **Data-density patterns:** freshness line (audit), live pill (metrics), row badges - partially shipped; finish per section 3 table.
5. **A11y pass:** aria-hidden on decorative svgs (we ship several unlabeled), alt policy, ::selection token, contrast rule (accent never for body text).
6. Fonts already vendored (Caveat/Montserrat) - add the 400 weight for body use.

## 7. Unit record (9-step, compressed)

READ: live sites fetched + parsed (44.5KB/49.1KB built CSS, structure inventories); app index.css read in full; providers/ThemeContext read; backend repo surveyed (Node/Supabase/Cloudflare - no UI). UNDERSTAND: consumers = Phase 2 continuation, Arwa (frontend lane), the operator's quality bar. EXPLORE: local repos searched for the Astro source (absent - recorded); built output studied instead. RESEARCH: token extraction scripts run against both built CSS files; every number in this doc comes from those extractions. REVIEW: perspectives applied - UI/UX/FE/a11y/PM. IDEATE: transfer plan prioritized; copying the websites rejected by operator directive (references, not templates). DRY RUN: n/a (study unit); claims carry extraction sources. Bias checks: confirmation (assumed cream background - falsified by the tokens, recorded); availability (zapply treated as the only reference - softwarejobs.dev studied as its own genre with different applicable patterns); premature-done (this is a study doc, not a to-do list).
