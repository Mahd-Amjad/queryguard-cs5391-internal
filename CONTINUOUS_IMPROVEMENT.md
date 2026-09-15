# QueryGuard - Continuous Improvement Contract

**Adopted:** 2026-09-15 (operator directive: keep an open mind, keep exploring, learning and
improving - engrained, not remembered).

This contract binds every session that works on this project. It supplements (never replaces)
the QA_CHECKLIST gates and the two-phase work protocol.

## The commitments

1. **Every finished unit ends with one self-critique question:** "what would make this
   meaningfully better?" - answered in writing (even if the answer is "nothing, and here is
   why"), so improvement is considered, not assumed absent.
2. **References are studied in code, not in screenshots.** Any UI/UX judgment cites the
   actual implementation (repo, built CSS, DOM) of the reference - never a visual impression.
3. **The landscape is re-scanned per phase, not per whim:** one broad pass (repos, tools,
   templates) at each phase gate; findings land in the reference study doc, not in ad-hoc
   rewrites.
4. **Visual verification uses the strongest available reader:** screenshots are reviewed with
   explicit checks (overflow, hierarchy, contrast, density); where the working model's visual
   judgment is uncertain, a second reader (stronger model or the operator) reviews before
   "done" is claimed.
5. **Artifacts of learning are filed, not narrated:** tool discoveries, pattern findings and
   rejected ideas go to INDEX.md / the reference study / DECISIONS.md - one line each, in the
   canonical file, the same day.

## The failure this prevents

Sessions declaring done on self-graded visual quality (three recorded failures: D-013,
D-015, the SM62 reskin) and sessions treating "done" as the end of learning rather than the
start of the next reference study.
