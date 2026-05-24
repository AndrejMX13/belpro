---
name: Serena replace_symbol_body pitfalls
description: Two cases where replace_symbol_body corrupts code — decorators and module-level string constants
type: feedback
originSessionId: 4be1c125-bd42-44b7-ad30-6b7c75405ac0
---
## Pitfall 1 — Decorated functions

Never use `mcp__serena__replace_symbol_body` on a Python function that has a decorator (e.g. `@router.get`, `@router.post`, `@app.on_event`). The tool treats the decorator as a "preceding comment" and excludes it from the replacement, silently unregistering the route.

**Why:** The tool's own docs say "The body does NOT include any preceding docstrings/comments or imports." Decorators fall into this excluded category.

**How to apply:** When editing a decorated function, use the `Edit` tool with enough surrounding context to include the decorator. Only use `replace_symbol_body` for plain (undecorated) functions or class methods.

---

## Pitfall 2 — Module-level string constants

Never use `mcp__serena__replace_symbol_body` on a module-level string constant (e.g. `_BASE_CSS = """..."""`). The tool appends ` = """` followed by the old value after the replacement body, producing a syntax error with a dangling duplicate fragment.

**Why:** The tool is designed for code symbols (functions, classes). A bare string assignment is not a proper symbol body — the tool inserts an extra `= "old_content"` trailer after the replacement.

**How to apply:** Use `Edit` (or `mcp__serena__replace_content`) for module-level constants. `replace_symbol_body` is safe only for function and class definitions.
