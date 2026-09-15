# The story of QueryGuard

## The problem

Organizations are starting to let people ask databases questions in plain English. An AI
writes the SQL. That is genuinely useful and genuinely dangerous: a wrong or malicious
query could delete records, or walk private data (SSNs, billing status) out the front door.
Nobody in that pipeline checks the AI's work.

## The idea

Put a deterministic safety gate between the AI and the database. The gate is not another
AI judging another AI; it is a fixed set of nine rules applied to the parsed query:

- destructive statements never run (the database is read-only at the connection level)
- one query per question, no stacked commands
- hidden write commands (comment tricks) are caught by cleaning and re-parsing
- only published tables are queryable
- private columns never appear in answers, including indirect routes (grouping, ordering,
  combined lists)
- system tables, execution tricks, and unreadable queries are refused
- unbounded reads still run, with a suggested limit

Three outcomes exist: PASS (runs as asked), MASK (answered with private columns removed),
BLOCK (stopped with a plain-English reason). Every decision lands in an append-only audit
log anyone can read afterward.

## Practices we followed (mapped to the course)

| Course practice | Where it shows up |
|---|---|
| User stories (XP) | SRS §2.3.1: five stories, each traced to numbered requirements and tests |
| Test-first / refactoring | a real defect (compound SELECTs skipping the masking rules) was caught by probing, fixed, and pinned by regression tests |
| Continuous integration | every push runs the test suite plus a 64-case labeled corpus; any expected-verdict miss fails the build |
| Security lectures (CIA, least privilege, masking) | read-only connections, column masking, allowlists, audit trail |
| AI-era SE (lecture 1) | the entire premise: keep the AI useful and unsafe-by-default output under control |

## The numbers (September 12, 2026)

- 40 automated tests passing
- 64-entry labeled corpus: every attack stopped, zero false alarms on safe questions
- gate decision time: p95 under 0.6 ms (target was 50 ms)
- 384 metamorphic rewrite checks: equivalent rewrites never change a verdict

## What is next

Live-LLM mode (the demo currently uses a deterministic stand-in so nothing depends on an
external service), intent matching (does the query do what was asked), and corpus
hardening with fuzzed attack variants.
