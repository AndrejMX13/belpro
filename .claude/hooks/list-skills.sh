#!/bin/bash
# Inject available project-local skills into session context at startup.
# Runs from project root. Skills are directories under .claude/skills/.
skills=$(ls .claude/skills/ 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
if [ -n "$skills" ]; then
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"Project-local skills available (invoke with Skill tool by name): $skills\"}}"
fi
