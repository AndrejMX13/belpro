---
name: feedback_superpowers_discipline
description: Always invoke relevant skills at the start of every task — before any response or action
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5e3ac5db-cd9e-4fd5-a92c-87d9a93aacce
---

Invoke relevant skills at the very start of every task — before planning, researching, or taking any action. This gates every task from the first message, so there is no such thing as a complex task "already in progress" that bypassed the check.

**Why:** Happened twice now with `superpowers:systematic-debugging` specifically. The logo deletion bug burned multiple sessions of thrashing (backup-restore variants, monkeypatch, interceptor) before the skill was finally invoked — at which point the root cause (container not rebuilt) was found in one diagnostic run. The skill's "3+ fixes failed → question architecture" rule would have triggered much earlier.

**How to apply:** Before ANY task — debugging, feature work, brainstorming, n8n workflows, refactoring, anything — check whether a skill applies. Even a 1% chance means invoke it. This is not optional and cannot be rationalized away ("this is simple", "I need context first", "let me just do this one thing"). For debugging specifically: the moment a bug resists a second fix attempt, invoke `superpowers:systematic-debugging` before attempting a third.
