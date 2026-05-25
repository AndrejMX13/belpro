---
name: reference-render-diagrams
description: How to re-render Mermaid architecture diagrams to SVG after editing the source .md files
metadata:
  type: reference
---

`scripts/render_diagrams.py` renders all Mermaid diagrams in `docs/images/` to SVG.

**When to run:** After editing any `.md` file in `docs/images/` that contains a `\`\`\`mermaid` block.

**Command:**
```
python scripts/render_diagrams.py
```

**What it does:** Finds every `.md` file in `docs/images/` with a mermaid block, extracts the source, runs `mmdc`, and writes a matching `.svg` alongside it.

**Requirement:** `mmdc` (Mermaid CLI) must be installed globally: `npm install -g @mermaid-js/mermaid-cli`

**Current diagram files:**
- `docs/images/belpro-architecture-component.md` → `.svg` (EN component diagram)
- `docs/images/belpro-architecture-sequence.md` → `.svg` (EN sequence diagram)
- `docs/images/belpro-arhitektura-komponente.md` → `.svg` (SL component diagram)
- `docs/images/belpro-arhitektura-zaporedje.md` → `.svg` (SL sequence diagram)

**Why:** `shell=True` is required on Windows because mmdc installs as a `.cmd` file that Python subprocess cannot find otherwise.
