#!/usr/bin/env python
"""Render Mermaid diagrams in docs/images/ to SVG.

Finds every .md file in docs/images/ that contains a ```mermaid block,
extracts the diagram source, and runs mmdc to produce a matching .svg file.

Usage:
    python scripts/render_diagrams.py

Requirements:
    mmdc (Mermaid CLI) must be installed globally:
        npm install -g @mermaid-js/mermaid-cli
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "docs" / "images"
MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


def render(md_file: Path) -> bool:
    """Extract Mermaid source from md_file and render to a matching .svg."""
    source = md_file.read_text(encoding="utf-8")
    match = MERMAID_BLOCK.search(source)
    if not match:
        return False

    svg_file = md_file.with_suffix(".svg")

    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", encoding="utf-8", delete=False) as tmp:
        tmp.write(match.group(1))
        tmp_path = Path(tmp.name)

    try:
        result = subprocess.run(
            f'mmdc -i "{tmp_path}" -o "{svg_file}"',
            capture_output=True,
            text=True,
            shell=True,
        )
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip()}")
            return False
    finally:
        tmp_path.unlink(missing_ok=True)

    return True


def main() -> None:
    """Render all Mermaid diagrams in docs/images/."""
    md_files = sorted(IMAGES_DIR.glob("*.md"))
    if not md_files:
        print("No .md files found in docs/images/")
        return

    ok = fail = skip = 0
    for md_file in md_files:
        if not MERMAID_BLOCK.search(md_file.read_text(encoding="utf-8")):
            skip += 1
            continue
        svg = md_file.with_suffix(".svg")
        print(f"  {md_file.name} -> {svg.name}", end=" ")
        if render(md_file):
            print("OK")
            ok += 1
        else:
            print("FAIL")
            fail += 1

    print(f"\n{ok} rendered, {fail} failed, {skip} skipped (no mermaid block)")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
