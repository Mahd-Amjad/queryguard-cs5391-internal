# QueryGuard Submission Checklist - SRS + Review + Presentation (Group Project 1, second half)

**Created:** 2026-09-12 (SE checkpoint unit, SM61). **Due:** presentation Tue Sep 16 (class); SRS + review before midterm (date TBA).
**Rule:** this is a pointer manifest, not a file bundle - canonical files stay where they live; copies would violate the register discipline.

## Destination and stakeholders (pinned 2026-09-12, before any more work)

**Destination (updated 2026-09-15, operator fact):** (1) Tuesday Sep 16 is an INFORMAL in-class
update, not a graded presentation - the deck goes up as built; no rehearsal gate; the in-room
demo is optional (S8 announces it; skip freely). (2) The graded item is the "SRS, review, and
presentation 10%" package by midterm: SRS v1.x + recorded group review + presentation, with
receipt captured (course index grading table).

**Stakeholders and what each needs:**

- **Dr. Chen (grader):** visible SE-process artifacts (user stories, test-first, CI, requirement
  doc), his labeled-block slide style, exact product names, no em dashes, on-time delivery.
- **Arwa (co-presenter, reviewer):** a reviewable SRS snapshot that does not shift under her, her
  four slides rehearsed, lane ownership visible.
- **Classmates (quiz source):** slides self-explanatory without narration.
- **Operator (presenter, grade):** rehearsed 5-8, demo script, receipt capture.
- **Future us (Project 2):** the SRS as the build source of truth; the conformance yardstick reusable.

**Research standard for this project:** course-project grade context, NOT conference-paper
standards. IEEE 830/29148 vocabulary is used only where Chen's own arc (requirement doc, XP,
CI) intersects it.

## Adopted yardstick (the axe)

- IEEE 830 + ISO/IEC/IEEE 29148 quality characteristics: unambiguous, complete, consistent,
  ranked, verifiable, traceable, modifiable.
- Reference template: github.com/jam01/SRS-Template (448 stars, CC0, IEEE 830 + 29148 aligned).
- Professor-style requirements: `../PROFESSOR_STYLE.md` (labeled parallel blocks; every option
  priced with limitations + a decision guide; exact product names; no em dashes; process graded).

## Items

| # | Item | Canonical file | Status | Owner |
|---|---|---|---|---|
| 1 | SRS presentation deck (8 slides, render-verified 09-12) | `prototype/presentation/QueryGuard_SRS.pptx` (+ `build_deck.py`) | READY | both |
| 2 | Deck presenter split visible (S1-4 Arwa, S5-8 Mahd, labels on-slide) | build_deck.py lines 87-223 | READY | both |
| 3 | SRS v1.1 | `srs/SRS.md` + `SRS.html` + `SRS.docx` | CURRENT 09-15; review notes fold in as received - not a gate | Mahd |
| 4 | Review comments folded into the SRS | `srs/SRS.md` | OPERATOR-SIDE CONVERSATION - folds in when comments exist; submission proceeds regardless (09-15: never rely on external parties) | operator |
| 5 | SRS v1.1 improvements from the adopted standard | `srs/SRS.md` | DONE 09-15 (D-020): (a) priority table = SRS section 3.6; (b) revision-history block in the header. Applied ahead of Arwa's return - additive-only, her snapshot review is unaffected; her comments fold in as the next revision. | Mahd |
| 6 | Review recorded in DECISIONS | `DECISIONS.md` entry | WITH REVIEW NOTES - one entry when the conversation happens; not a submit gate | Mahd |
| 7 | Professor-style pass on deck | `../PROFESSOR_STYLE.md` | DONE (labeled blocks, presenter labels, exact product names, no em dashes; render + vision verified 09-12) | done |
| 8 | Rubric walk: "SRS, review, and presentation 10% by midterm" | `../00_COURSE_INDEX.md` grading table | ON TRACK | - |
| 9 | Rehearsal: DROPPED as a gate 09-15 (Tuesday is an informal update); optional look-through at operator discretion | build_deck.py content | DROPPED | - |
| 10 | Demo boot check - mechanical (serve app, safe ask, blocked attack, masked column, audit row); in-room demo optional | `prototype/` via `qg.sh serve` | DONE 09-15 (SM62): all beats verified live over HTTP; paraphrase gotcha found + scripted into TECH_PLAN section 8; app left serving on :5055 | Mahd |
| 11 | Submission receipt capture | -> `assignments/` register | AT SUBMIT TIME | Mahd |

## Notes

- S8 close slide already announces the live demo + repo URL; keep the demo scripted (TECH_PLAN §8)
  and mock-mode only (no live LLM on stage).
- Presentations through Sep 22 are quiz material for classmates - keep on-screen text
  self-explanatory.
- The two SRS v1.1 items (5a, 5b) come straight from the adopted standard's characteristics; they
  are the only conformance gaps found. Everything the standard checks (verifiability, traceability,
  measured results) is already our strongest section.
- Speaker note for S8 (from research pass #4, say it - do not edit the slide mid-review): "Industry
  declared the SRS dead during agile. AI-era spec-driven development brought specs back as the
  control artifact for code-generating agents - which is exactly what our SRS + nine-rule gate is,
  and we measured it." Sources in `../COMPETITION_SCAN.md` research pass #4.
