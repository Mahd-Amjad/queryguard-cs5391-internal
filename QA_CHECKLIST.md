# QueryGuard QA Checklist — run before declaring ANY unit done

Pair with the workspace's review-rigor skill (7-check discipline). This file is the
project-specific surface list. A unit is done when every applicable box is checked
with evidence, not claimed.

## Stakeholder pass (every UI or copy change)

- [ ] Each page: a first-time viewer can say what the page is for in 10 seconds
- [ ] No unexplained jargon: rule ids only appear next to their plain names
      (plain names live in `queryguard/explain.py`)
- [ ] Every number says whether it is good or bad (or links to the context that says it)
- [ ] Empty states written ("no attacks seen yet"), never a blank panel
- [ ] Screenshots of EVERY page at demo resolution (1440x900, full page), compared
      SIDE BY SIDE against the adopted reference kit's own demo/screenshots (currently
      satnaing/shadcn-admin; the named reference changes when the adopted kit does).
      "Looked at" by the same assistant eyes that missed the defects is not
      verification: the comparison is against the reference, and the operator is the
      final arbiter of presentability (09-15 standing rule).
- [ ] Stranger test: a page where every answer is one row, or where an audit log
      shows test debris ("x", ERROR rows, paraphrase probes), is not presentable.
      Demo data volume and log cleanliness are part of done.

## Correctness pass (every engine change)

- [ ] `pytest tests/` green
- [ ] `python scripts/run_eval.py --fail-on-miss` green
- [ ] New behavior probed over live HTTP (not only unit level)
- [ ] Test pins assert behavior, never incidental class names or counts
- [ ] Decision recorded in `DECISIONS.md` with the rejected alternative
- [ ] Residuals named with an owner, never silently dropped

## Process pass (every unit)

- [ ] 9-step run with real EXPLORE (surfaces read at destination, archives checked)
      and real RESEARCH (prior art found and applied, not just collected)
- [ ] review-rigor 7-checks answered at the conclusion
- [ ] No manufactured gates: approved project work proceeds; only named operator
      gates stop work (public visibility, credentials, graded-bar decisions)
- [ ] Framework, template, or tool choices carry a written criteria table
      (criteria from project constraints, verifiable facts, rejected alternatives)
      in DECISIONS.md - not a single number like star count

## Before any submission (proposal / SRS / deck)

- [ ] Professor-style pass (PROFESSOR_STYLE.md sections filled and applied)
- [ ] Rubric walk: every known grading criterion touched by this deliverable
- [ ] Group review recorded in DECISIONS.md before submit

## Session lessons (SM59, standing)

- Research theater is the failure mode: references and examples must CHANGE what gets
  built. Adopt the reference first (vendored, named), then build on it.
- Anything shareable is written for its reader, in their voice: HTML or PPTX, never raw
  markdown; title is the reader's question; answers before argument; honesty labels on
  claims; group documents speak as the two-person team, never as the assistant.
- Test pins assert behavior, never class names or hardcoded counts.
- Choices carry criteria tables (constraints -> facts -> rejected alternatives).
- Approved project work proceeds; artificial gates and "waiting" framing are defects.
- Check the live state before calling anything blocked (the push-guard case: four
  verifiable attempts, then reported and routed around with the staging script).
- Load review-rigor at every conclusion; run this checklist at every unit close.

- [ ] Every claimed file or action has a tool result showing it (write result,
      ls, or read-back). Describing intended work as done is the worst defect class.
- [ ] Sendable messages follow the Legal drafts pattern: one MESSAGE_*.txt of pure
      relayable text, question-style header, key answer bold up front, single
      outstanding ask, no internal annotations; scrutinize for redundant asks,
      omissions, overstatements before handing over.

## Truth pass (every session close; added 2026-09-15, SM62 - the anti-drift gate)

Founded on the SM62 finds: three canonical files stated three different test counts (39 / 40 / 41),
TECH_PLAN listed resolved decisions as "the only open items", and a dropped rehearsal stayed
"pending" in three surfaces. Mechanical checks before declaring a session done:

- [ ] Stated test counts equal the live suite: run `pytest -q`, then
      `grep -n "passing" README.md TECH_PLAN.md srs/SRS.md` - every stated count matches the run.
- [ ] No dead directives: grep canonical docs for "pending", "PENDING", "remaining:",
      "open items" - each hit is still true or carries a DONE / SUPERSEDED marker with a date.
- [ ] Relative pointers in canonical docs resolve (archive/, srs/, prototype/ paths exist).
- [ ] SUBMISSION_CHECKLIST statuses match reality (each READY / PENDING claim has same-session evidence).
