"""Plain-language explanations shown in the UI so a first-time viewer never
needs internal rule ids to understand what happened (stakeholder-facing copy)."""

import re

RULE_EXPLAIN = {
    "G-01": {"name": "No destructive statements",
             "plain": "Queries that change or delete data (DELETE, UPDATE, DROP and friends) never run. The database is read-only."},
    "G-02": {"name": "One query at a time",
             "plain": "A question may produce exactly one query. Stacking a second command onto it is blocked."},
    "G-03": {"name": "No hidden write commands",
             "plain": "Write commands disguised with comment tricks are caught, because the gate cleans and re-parses the query before judging it."},
    "G-04": {"name": "Only allowed tables",
             "plain": "Only the tables the clinic published can be queried. Anything outside that list is refused."},
    "G-05": {"name": "Private columns stay private",
             "plain": "Columns like SSN or billing status are never shown. They are removed from answers, and sneaky routes such as grouping, ordering, or combined lists are blocked too."},
    "G-06": {"name": "No system-table snooping",
             "plain": "Queries that try to list the database's own internal structure are refused."},
    "G-07": {"name": "No execution tricks",
             "plain": "Commands that run code, attach outside files, or flip database settings are refused."},
    "G-09": {"name": "Huge answers get a hint",
             "plain": "A read with no row limit still runs, but the gate suggests adding a LIMIT so results stay fast."},
    "G-10": {"name": "Answer must match the question",
             "plain": "Stretch goal: the generated query must actually do what the question asked. Not required for the core demo."},
    "PARSE": {"name": "Unreadable means blocked",
              "plain": "If the gate cannot cleanly understand a query, it is blocked by default. Confusing is treated as unsafe."},
}

VERDICT_PLAIN = {
    "PASS": "Ran normally. The query only reads data the gate allows.",
    "MASK": "Answered with private columns removed. The query touched private data, so those columns were stripped before the result reached you.",
    "BLOCK": "Blocked. This query breaks a safety rule, so nothing ran and nothing was changed.",
    "ERROR": "Something went wrong on our side. Nothing ran, nothing changed.",
}


_REASON_PREFIX = (
    ("sensitive columns masked:", "Private columns removed:"),
    ("no rule violations; unbounded read", "Nothing unsafe, but the answer has no row limit."),
    ("no rule violations detected", "Nothing unsafe in this query."),
)


def plain_reason(reason: str) -> str:
    """Gate reasons are audit-facing; the UI shows viewer-friendly text (D-014:
    no developer strings - python list reprs, internal phrasing - on screen)."""
    if not reason:
        return ""
    text = reason.strip()
    for raw, plain in _REASON_PREFIX:
        if text.startswith(raw):
            text = plain + text[len(raw):]
            break
    text = re.sub(r"\[([^\]]*)\]", lambda m: m.group(1).replace("'", ""), text)
    return text
