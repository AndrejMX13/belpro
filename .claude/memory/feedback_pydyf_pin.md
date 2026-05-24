---
name: pydyf pin for WeasyPrint
description: WeasyPrint 62.3 requires pydyf==0.10.0 pinned explicitly or it installs a newer pydyf that breaks PDF generation
type: feedback
originSessionId: 2257b4c6-b995-4509-83e8-5fd7e8b5a4f8
---
Always add `pydyf==0.10.0` to requirements.txt alongside `weasyprint==62.3`.

**Why:** pip resolves pydyf to a newer version (0.11.0+) that removed the `transform` method from its `Stream` class. WeasyPrint 62.3 calls `super().transform(...)` expecting pydyf 0.10.0's API, causing `AttributeError: 'super' object has no attribute 'transform'` at runtime.

**How to apply:** Any time WeasyPrint is added or upgraded, check that pydyf is explicitly pinned to the version WeasyPrint was tested against.
