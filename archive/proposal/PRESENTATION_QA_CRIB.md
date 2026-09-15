# QueryGuard Proposal Presentation - Q&A Crib + Lens Notes

**Created:** 2026-09-02 (SM53, operator-approved recording; multi-lens brainstorm, no implementation)
**Use:** pre-presentation review for Tue Sep 9; absorb/archive at the project cleanup gate after the presentation.

## Presentation posture

- **Grade what the professor grades:** Chen scores SE process - SRS-numbered requirements, milestones-with-receipts, CI lane. Lead the walkthrough there; the CVE drama is the hook, not the payload.
- Slides are now floor-compliant (18pt key lines, 36pt titles); epigram closes via speaker notes on slide 8.

## Lens findings (terse)

| Lens | Finding / ready answer |
|---|---|
| End-user dev | FP fatigue kills gates; our FP-visibility promise is the differentiator - say it twice. Unanswered: who sees the verdict → "developer log by default; end-user message only for BLOCK." |
| Security analyst | Wants CWE/CVE per rule (G-catalog maps), rule-set tamper story (answer: CI-gated rules), and **log hygiene: verdict logs are themselves PII sinks** - a logged blocked-exfil query stored the PII. Answer: redact/retain-by-policy in logs; one-line fix candidate for SRS. |
| Privacy legal | Gate sees user data = mini data processor; detection ≠ compliance; LLM vendor saw the prompt upstream (out of scope - say so). One sentence if asked, not a slide. |
| Legal/liability | Mis-BLOCK of a legitimate medical/financial query → present BLOCK as configurable policy (SUGGEST default), not a hard default. |
| SEO/publicity | Near-empty niche ("LLM SQL guard", "text-to-SQL security") - claimable AFTER publication decisions. **Anonymity collision risk until then - see below.** |
| Product engineer | Risk is breadth not depth; 40/20/20/20 is right; keep web app thin (one endpoint + minimal UI); engine + harness carry the grade. Demo: rehearse with recorded fallback. |

## Content risks to fix or pre-answer (before/during Q&A)

1. **Slide 4 "Tools: gates exist, numbers don't"** - HeimdaLLM reports evaluations. Soften to "not SQL-specific / not reproducible side-by-side" if challenged; do not defend the absolute claim.
2. **n=30 corpus** - never let a rate sound precise; framing: "small-n by design, first course-scale checkpoint; confidence stated honestly."
3. **SQL dialect portability** (SQLite vs Postgres AST differences) - rehearse one sentence: rules operate on a normalized AST; dialect-specific behaviors are rule-scoped and tested per dialect in the corpus.
4. **Slide 3 stat provenance — RESOLVED 2026-09-05 (operator deferred to assistant):** "CVSS 7.7 = AnythingLLM PII extraction" is citation-exact; the ASR card was swapped 50% → 96% (the published manual-attack baseline success rate without defenses). All four stat cards now trace to audited sources.

## Anonymity separation (until SaTML decisions, ~Sep 29+)

The research artifact is anonymous; QueryGuard (course) may go public via portfolio publication decisions (`CAR-GH-1`). Keep them **name-separated and content-separated**: no shared distinctive phrasing, CVE-set framing, or cross-links in any public course repo until the submission window closes. After decisions: the terminology niche is worth claiming publicly.

## Process note (deferred, needs operator go)

Fold the size-floor checklist + Gate-3 screenshot audit into `.meta/DELIVERABLE_SPECS/presentation_pptx_spec.md` as the default pre-handoff pass (tonight it ran as a rescue; make it standard).
