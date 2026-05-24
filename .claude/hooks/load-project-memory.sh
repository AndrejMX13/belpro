#!/bin/bash
# Inject public project memory index into session context at startup.
# Runs from project root. Memory files live in .claude/memory/.
if [ -f .claude/memory/MEMORY.md ]; then
  python3 -c "
import json, sys
content = open('.claude/memory/MEMORY.md', encoding='utf-8').read()
msg = 'Project memory index (load individual files when relevant):\n\n' + content
out = {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': msg}}
print(json.dumps(out))
"
fi
