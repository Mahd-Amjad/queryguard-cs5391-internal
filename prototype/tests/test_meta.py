"""Metamorphic relations: equivalent rewrites must not change verdicts."""
from scripts.run_metamorphic import run


def test_metamorphic_relations_hold():
    violations, checked = run()
    assert checked > 0
    assert violations == []
