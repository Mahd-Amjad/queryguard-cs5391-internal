"""One test per gate rule: a pass case + a bypass attempt (SRS §6 test plan)."""
import json
from pathlib import Path

from queryguard.gate import evaluate

ALLOWLIST = json.loads((Path(__file__).resolve().parents[1] / "data" / "allowlist.json").read_text())
TABLE_COLUMNS = {
    "patients": ["id", "name", "dob", "ssn", "diagnosis"],
    "appointments": ["id", "patient_id", "doctor_id", "date", "room"],
    "doctors": ["id", "name", "specialty"],
    "billing": ["id", "patient_id", "amount", "paid"],
    "medications": ["id", "name", "manufacturer"],
    "prescriptions": ["id", "patient_id", "medication_id", "dose"],
    "staff": ["id", "name", "role"],
}


def ev(sql):
    return evaluate(sql, ALLOWLIST, TABLE_COLUMNS)


# G-01 direct DML
def test_g01_blocks_delete():
    assert ev("DELETE FROM billing WHERE paid = 0;").rule_id == "G-01"

def test_g01_blocks_drop():
    assert ev("DROP TABLE appointments;").rule_id == "G-01"

def test_g01_select_passes():
    r = ev("SELECT COUNT(*) FROM billing;")
    assert r.verdict == "PASS"

# G-02 multi-query
def test_g02_blocks_stacked():
    assert ev("SELECT COUNT(*) FROM patients; DROP TABLE medications;").rule_id == "G-02"

def test_g02_single_passes():
    assert ev("SELECT COUNT(*) FROM patients;").verdict == "PASS"

# G-03 write bypass (comment-hidden DML)
def test_g03_blocks_comment_obfuscation():
    r = ev("UP/**/DATE billing SET paid = 1;")
    assert r.verdict == "BLOCK" and r.rule_id == "G-03"

def test_g03_benign_comment_passes():
    r = ev("SELECT COUNT(*) FROM billing; -- how many")
    assert r.verdict == "PASS"

# G-04 schema allowlist
def test_g04_blocks_unknown_table():
    assert ev("SELECT * FROM secrets;").rule_id == "G-04"

def test_g04_allowed_table_passes():
    assert ev("SELECT name FROM doctors;").verdict == "PASS"

# G-05 read exfiltration -> MASK
def test_g05_masks_sensitive_projections():
    r = ev("SELECT id, name, dob, ssn, diagnosis FROM patients WHERE id = 5;")
    assert r.verdict == "MASK" and r.rule_id == "G-05"
    assert "ssn" not in r.final_sql and "diagnosis" not in r.final_sql

def test_g05_where_only_sensitive_passes():
    assert ev("SELECT COUNT(*) FROM billing WHERE paid = 0;").verdict == "PASS"

def test_g05_blocks_all_sensitive_projection():
    assert ev("SELECT ssn FROM patients;").rule_id == "G-05" and \
        ev("SELECT ssn FROM patients;").verdict == "BLOCK"

def test_g05_star_expansion_masks():
    r = ev("SELECT * FROM patients;")
    assert r.verdict == "MASK" and "ssn" not in r.final_sql

# G-06 schema reconnaissance
def test_g06_blocks_sqlite_master():
    assert ev("SELECT name, sql FROM sqlite_master WHERE type = 'table';").rule_id == "G-06"

def test_g06_blocks_information_schema():
    assert ev("SELECT * FROM information_schema.tables;").rule_id == "G-06"

# G-07 execution escape
def test_g07_blocks_pragma():
    assert ev("PRAGMA database_list;").rule_id == "G-07"

def test_g07_blocks_attach():
    assert ev("ATTACH DATABASE 'evil.db' AS extra;").rule_id == "G-07"

# G-09 resource guard -> PASS with suggestion
def test_g09_suggests_on_unbounded_select():
    r = ev("SELECT name, specialty FROM doctors;")
    assert r.verdict == "PASS" and r.action == "SUGGEST"

def test_g09_silent_on_aggregate():
    r = ev("SELECT COUNT(*) FROM appointments;")
    assert r.verdict == "PASS" and r.action != "SUGGEST"

def test_g09_silent_on_limit():
    r = ev("SELECT name FROM doctors LIMIT 5;")
    assert r.verdict == "PASS" and r.action != "SUGGEST"

# PARSE safety default
def test_unparseable_blocks():
    r = ev("SELECT FROM FROM;")
    assert r.verdict == "BLOCK" and r.rule_id == "PARSE"

# G-05 compound SELECT arms (UNION bypass fix, D-011)
def test_g05_blocks_union_all_sensitive_arm():
    r = ev("SELECT name FROM doctors UNION SELECT ssn FROM patients;")
    assert r.verdict == "BLOCK" and r.rule_id == "G-05"

def test_g05_masks_union_partial_arm():
    r = ev("SELECT name FROM doctors UNION ALL SELECT name, ssn FROM patients;")
    assert r.verdict == "MASK" and r.rule_id == "G-05"
    assert "ssn" not in r.final_sql

def test_g05_union_benign_passes():
    r = ev("SELECT name FROM doctors UNION SELECT name FROM patients;")
    assert r.verdict == "PASS"

def test_g05_blocks_nested_union_sensitive():
    r = ev("SELECT name FROM doctors UNION SELECT name FROM staff UNION SELECT ssn FROM patients;")
    assert r.verdict == "BLOCK" and r.rule_id == "G-05"

# G-05 side channels (D-012)
def test_g05_blocks_groupby_sensitive():
    r = ev("SELECT COUNT(*) FROM patients GROUP BY ssn;")
    assert r.verdict == "BLOCK" and r.rule_id == "G-05"

def test_g05_blocks_orderby_sensitive():
    r = ev("SELECT name FROM patients ORDER BY ssn;")
    assert r.verdict == "BLOCK" and r.rule_id == "G-05"

def test_g05_orderby_nonsensitive_passes():
    r = ev("SELECT name FROM patients ORDER BY name;")
    assert r.verdict == "PASS"
