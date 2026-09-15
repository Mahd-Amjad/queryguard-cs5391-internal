"""Mock generator (FR-02): deterministic prompt -> candidate SQL lookup."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

FALLBACK_ID = "MOCK-FALLBACK"


class MockGenerator:
    def __init__(self):
        self.candidates = json.loads((DATA / "candidates.json").read_text())
        self.by_prompt = {}
        corpus = DATA / "corpus.jsonl"
        if corpus.exists():
            for line in corpus.read_text().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                self.by_prompt[entry["prompt"].strip().lower()] = entry["id"]

    def generate(self, question: str) -> dict:
        pid = self.by_prompt.get(question.strip().lower(), FALLBACK_ID)
        return {
            "prompt_id": pid,
            "sql": self.candidates[pid],
            "fallback": pid == FALLBACK_ID,
            "mode": "mock",
        }


class LiveGenerator:
    """Placeholder behind the same interface; the group opts in later."""

    def __init__(self, client=None):
        self.client = client

    def generate(self, question: str) -> dict:
        raise NotImplementedError("live mode not configured; use mock mode")
