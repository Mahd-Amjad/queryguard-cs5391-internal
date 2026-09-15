"""Render a markdown file to the branded standalone HTML (E2-memo styling:
dark editorial, print-safe). Two modes:

  python scripts/md_to_html.py                  # SRS default: render srs/SRS.md,
                                                # mirror both into docs/ for the repo
  python scripts/md_to_html.py SRC OUT --title "..." [--note HTML]

Rerun after any source edit. The markdown is the single source.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]      # prototype/
PROJECT = ROOT.parent                            # project/  (srs/ lives here)
sys.path.insert(0, str(ROOT))

import markdown  # noqa: E402

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body { margin: 0; background: #121418; color: #f2f0e8;
         font: 16px/1.65 -apple-system, "Segoe UI", Roboto, Ubuntu, sans-serif; }
  main { max-width: 860px; margin: 2.5rem auto; padding: 0 1.2rem 4rem; }
  h1 { font-size: 1.35rem; }
  h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.14em;
       color: #a8b2bb; margin-top: 2.4rem; border-top: 1px solid #2a313a; padding-top: 1.4rem; }
  h3 { font-size: 1.02rem; color: #9fb3c8; }
  strong { color: #ffffff; }
  em { color: #a8b2bb; }
  a { color: #9fb3c8; }
  code { background: #232a32; border: 1px solid #2a313a; border-radius: 5px;
         padding: 0.1rem 0.4rem; font-size: 0.88em; }
  table { border-collapse: collapse; width: 100%; margin: 0.8rem 0; font-size: 0.93rem; }
  th, td { border: 1px solid #2a313a; padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
  th { background: #232a32; color: #9fb3c8; text-transform: uppercase;
       font-size: 0.76rem; letter-spacing: 0.08em; }
  tr:nth-child(even) td { background: rgba(255, 255, 255, 0.02); }
  .note { background: #1b2027; border: 1px solid #2a313a; border-left: 3px solid #e8b341;
          border-radius: 8px; padding: 0.8rem 1rem; margin: 1.5rem 0; font-size: 0.95rem; }
  .review { background: #1b2027; border: 1px solid #2a313a; border-left: 3px solid #9fb3c8;
            border-radius: 8px; padding: 0.9rem 1.1rem; margin: 1.6rem 0; }
</style>
</head>
<body>
<main>
{extra}
{body}
</main>
</body>
</html>
"""

SRS_NOTE = ('<div class="note"><strong>How to read this:</strong> Section 2.3.1 is the human '
            'summary (who wants what and why). Sections 3 and 6 are the engineering detail: '
            'one numbered requirement per safety rule, each mapped to a test. Section 8 holds '
            'the measured results.</div>')
SRS_REVIEW_BANNER = ('<div class="review"><strong>Review copy for Arwa.</strong> Read top to bottom '
                     '(about 20 minutes). Mark anything unclear, wrong, or missing: content matters '
                     'more than wording. Comment in the file, in chat, or bring points to the next '
                     'call. Nothing is final until the group signs off.</div>')


def render(md_text: str, title: str, extra: str = "") -> str:
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    return TEMPLATE.replace("{title}", title).replace("{extra}", extra).replace("{body}", body)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="branded markdown -> standalone HTML")
    ap.add_argument("src", nargs="?", help="markdown source (default: srs/SRS.md)")
    ap.add_argument("out", nargs="?", help="html output (default: srs/SRS.html)")
    ap.add_argument("--title", default="QueryGuard: requirement document (review copy)")
    ap.add_argument("--note", default="", help="optional HTML block injected after the first h2")
    ap.add_argument("--banner", default="", help="optional HTML block injected at the top")
    ap.add_argument("--srs", action="store_true", help="SRS mode: review banner + note + mirror into docs/")
    args = ap.parse_args(argv)

    if args.srs or (not args.src and not args.out):
        src = PROJECT / "srs" / "SRS.md"
        dst = PROJECT / "srs" / "SRS.html"
        extra = SRS_REVIEW_BANNER + (args.note or SRS_NOTE)
        mirror = True
    else:
        src = Path(args.src)
        dst = Path(args.out) if args.out else src.with_suffix(".html")
        extra = args.note
        mirror = False

    html = render(src.read_text(), args.title, extra)
    dst.write_text(html)
    print(f"rendered {dst} ({dst.stat().st_size} bytes)")

    if mirror:
        docs = ROOT / "docs"
        docs.mkdir(exist_ok=True)
        (docs / "SRS.md").write_text(src.read_text())
        (docs / "SRS.html").write_text(html)
        print(f"mirrored into {docs} (SRS.md, SRS.html)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
