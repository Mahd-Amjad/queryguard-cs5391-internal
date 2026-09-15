"""QueryGuard validation gate.

Every candidate SQL string is normalized (comments stripped), parsed into a
normalized AST (sqlglot, SQLite dialect), and checked against the rule
catalog FR-G01..FR-G09 (+ stretch FR-G10). One rule fires per decision; the
first match in precedence order wins.

Verdicts: PASS, BLOCK, MASK. SUGGEST is an action attached to a PASS.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import sqlglot
from sqlglot import exp
DML_KINDS = tuple(
    getattr(exp, name)
    for name in ("Insert", "Update", "Delete", "Drop", "Alter", "Create", "Truncate")
    if hasattr(exp, name)
)

_COMMENT_BLOCK = re.compile(r"/\*.*?\*/", re.S)
_COMMENT_LINE = re.compile(r"--.*?$", re.M)


@dataclass
class GateResult:
    verdict: str                 # PASS | BLOCK | MASK
    rule_id: str                 # G-xx or PARSE / OK
    reason: str
    action: str = ""             # MASK | SUGGEST (informational for the UI)
    suggestion: str = ""
    final_sql: str = ""
    elapsed_ms: float = 0.0
    notes: list = field(default_factory=list)


def normalize_variants(sql: str) -> tuple[str, str, bool]:
    """Return (spaced, concat, had_comment). Spaced keeps tokens apart (the
    standard parse). Concat joins tokens across comments — the bypass-hunting
    form: if ONLY the concat form parses, the comment was load-bearing (G-03)."""
    had = bool(_COMMENT_BLOCK.search(sql) or _COMMENT_LINE.search(sql))
    spaced = _COMMENT_LINE.sub(" ", _COMMENT_BLOCK.sub(" ", sql)).strip()
    concat = _COMMENT_LINE.sub("", _COMMENT_BLOCK.sub("", sql)).strip()
    return spaced, concat, had


def _parse(sql: str):
    stmts = [s for s in sqlglot.parse(sql, read="sqlite") if s is not None]
    return stmts or None


def _is_catalog_table(t, catalog: set[str]) -> bool:
    name = t.name.lower()
    qualifier = (t.db or "").lower()
    return name in catalog or qualifier in catalog or f"{qualifier}.{name}" in catalog


def _projection_columns(stmt) -> set[str]:
    """Column names that appear in the SELECT list only (not WHERE/GROUP BY).
    B-11 filters on a sensitive column in WHERE and must still PASS."""
    cols: set[str] = set()
    for item in stmt.expressions:
        for c in item.find_all(exp.Column):
            cols.add(c.name.lower())
    return cols


def _is_fully_aggregated(stmt) -> bool:
    return any(item.find(exp.AggFunc) for item in stmt.expressions)


def _nonprojection_sensitive(stmt, sensitive: set[str]) -> list[str]:
    """Sensitive columns referenced in GROUP BY / ORDER BY / HAVING. WHERE is
    deliberately excluded (D-002: filtering on a sensitive column is not
    exfiltration; corpus B-11). Grouping and ordering leak value channels (D-012)."""
    found: list[str] = []
    for key in ("group", "order", "having"):
        arg = stmt.args.get(key)
        if arg is not None:
            for c in arg.find_all(exp.Column):
                name = c.name.lower()
                if name in sensitive and name not in found:
                    found.append(name)
    return found


def _mask_select(stmt, sensitive: set[str], table_columns: dict) -> tuple[object, list[str]]:
    """Drop projections that expose sensitive columns. Expands * where needed.
    Returns (new_stmt, dropped_names)."""
    new_items, dropped = [], []
    for item in stmt.expressions:
        item_cols = {c.name.lower() for c in item.find_all(exp.Column)}
        if isinstance(item, exp.Star):
            tables = {t.name.lower() for t in stmt.find_all(exp.Table)} or {"patients"}
            exposed = set()
            for t in tables:
                exposed |= {c for c in table_columns.get(t, [])}
            hidden = sorted(exposed & sensitive)
            if hidden:
                dropped.extend(hidden)
                for c in sorted(exposed - sensitive):
                    new_items.append(sqlglot.parse_one(c, read="sqlite").this)
            else:
                new_items.append(item)
            continue
        if isinstance(item, exp.Column) and item.name.lower() in sensitive:
            dropped.append(item.name.lower())
            continue
        if item_cols & sensitive:
            dropped.extend(sorted(item_cols & sensitive))
            if len(item_cols) > len(item_cols & sensitive):
                new_items.append(item)
            continue
        new_items.append(item)
    stmt.set("expressions", new_items)
    return stmt, dropped


def evaluate(raw_sql: str, allowlist: dict, table_columns: dict) -> GateResult:
    sensitive = {c.lower() for c in allowlist["sensitive_columns"]}
    allowed_tables = {t.lower() for t in allowlist["queryable_tables"]}
    catalog = {t.lower() for t in allowlist["catalog_tables"]}
    blocked_funcs = {f.lower() for f in allowlist["blocked_functions"]}

    spaced, concat, had_comment = normalize_variants(raw_sql)
    concat_used = False
    try:
        stmts = _parse(spaced)
    except sqlglot.errors.ParseError:
        stmts = None
    if stmts is None:
        try:
            stmts = _parse(concat)
            concat_used = True
        except sqlglot.errors.ParseError as exc:
            return GateResult("BLOCK", "PARSE", f"unparseable candidate: {exc}", final_sql=raw_sql)

    if concat_used:
        return GateResult("BLOCK", "G-03",
                          "comment characters join into a hidden statement",
                          final_sql=raw_sql)

    # G-02 multi-query
    if len(stmts) > 1:
        return GateResult("BLOCK", "G-02",
                          f"stacked statements ({len(stmts)}) are not allowed",
                          final_sql=raw_sql)

    stmt = stmts[0]

    # G-07 execution escape
    if isinstance(stmt, (exp.Pragma, exp.Attach)):
        return GateResult("BLOCK", "G-07", f"{type(stmt).__name__} is not allowed", final_sql=raw_sql)
    for fn in stmt.find_all(exp.Anonymous):
        if str(fn.this).lower() in blocked_funcs:
            return GateResult("BLOCK", "G-07", f"side-effecting function {fn.this}()", final_sql=raw_sql)

    # G-06 schema reconnaissance
    if any(_is_catalog_table(t, catalog) for t in stmt.find_all(exp.Table)):
        return GateResult("BLOCK", "G-06", "catalog tables are not queryable", final_sql=raw_sql)

    tables = {t.name.lower() for t in stmt.find_all(exp.Table)}
    is_dml = isinstance(stmt, DML_KINDS)
    if is_dml and had_comment:
        return GateResult("BLOCK", "G-03",
                          "comment characters are hiding a write statement",
                          final_sql=raw_sql)

    # G-01 direct DML
    if is_dml:
        return GateResult("BLOCK", "G-01",
                          f"{type(stmt).__name__} statements are not allowed",
                          final_sql=raw_sql)

    # G-04 schema allowlist
    if not tables <= allowed_tables:
        bad = sorted(tables - allowed_tables)
        return GateResult("BLOCK", "G-04", f"tables outside the allowlist: {bad}", final_sql=raw_sql)

    # G-05 compound SELECT (D-011): verify every arm; set operations never skip masking
    if isinstance(stmt, exp.SetOperation):
        arm_nodes: list = []

        def _collect_arms(node):
            if isinstance(node, exp.SetOperation):
                _collect_arms(node.this)
                _collect_arms(node.expression)
            else:
                arm_nodes.append(node)

        _collect_arms(stmt)
        masked_any = False
        for arm in arm_nodes:
            if not isinstance(arm, exp.Select):
                return GateResult("BLOCK", "G-05",
                                  "compound select contains a non-SELECT arm",
                                  final_sql=raw_sql)
            side = _nonprojection_sensitive(arm, sensitive)
            if side:
                return GateResult("BLOCK", "G-05",
                                  f"sensitive columns in grouping/ordering leak values: {sorted(set(side))}",
                                  final_sql=raw_sql)
            masked, dropped = _mask_select(arm, sensitive, table_columns)
            if dropped:
                if not masked.expressions:
                    return GateResult("BLOCK", "G-05",
                                      "a select arm projects only sensitive columns",
                                      final_sql=raw_sql)
                masked_any = True
        if masked_any:
            return GateResult("MASK", "G-05",
                              "sensitive columns masked in select arm(s)",
                              action="MASK", final_sql=stmt.sql())
        return GateResult("PASS", "OK", "compound select: all arms verified", final_sql=stmt.sql())

    if isinstance(stmt, exp.Select):
        side = _nonprojection_sensitive(stmt, sensitive)
        if side:
            return GateResult("BLOCK", "G-05",
                              f"sensitive columns in grouping/ordering leak values: {sorted(set(side))}",
                              final_sql=raw_sql)
        proj_cols = _projection_columns(stmt)
        exposed = proj_cols & sensitive
        has_star = any(isinstance(i, (exp.Star,)) for i in stmt.expressions) or \
            any(isinstance(i, exp.Column) and isinstance(i.this, exp.Star) for i in stmt.expressions)
        # G-05 read exfiltration -> MASK (only when something is actually dropped)
        if exposed or has_star:
            masked, dropped = _mask_select(stmt, sensitive, table_columns)
            if dropped:
                if not masked.expressions:
                    return GateResult("BLOCK", "G-05",
                                      "every projected column is sensitive",
                                      final_sql=raw_sql)
                return GateResult("MASK", "G-05",
                                  f"sensitive columns masked: {sorted(set(dropped))}",
                                  action="MASK", final_sql=masked.sql())
            # star over tables with no sensitive columns -> fall through to PASS
            stmt.set("expressions", masked.expressions)
        if stmt.args.get("limit") is None and not _is_fully_aggregated(stmt):
            return GateResult("PASS", "G-09",
                              "no rule violations; unbounded read",
                              action="SUGGEST",
                              suggestion="consider adding a LIMIT to bound the result size",
                              final_sql=stmt.sql())

    return GateResult("PASS", "OK", "no rule violations detected", final_sql=stmt.sql())
