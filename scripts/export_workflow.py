"""Export volunteer_entry workflow from n8n to JSON file."""
import json
import urllib.request

N8N_URL = "http://localhost:5678"
N8N_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlYzJjNTY1Ni0zOTA5LTRlNzctOTZjYy00N2E2MjNmZDcwNGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiM2I3YWZiNjQtZDI0OC00M2QxLTlkNWItOGFhMGYxNzIxOTc1IiwiaWF0IjoxNzc3NzMxMDU3fQ.GV2V96vGSJjq1sBMJvKOcl72QLZCXPNlX7__i4npKTU"
WF_ID = "Lw6qRiO9ozSr6EeW"
OUT = "d:/Andrej/vsCode-workspace/BelPro/n8n/workflows/volunteer_entry.json"

req = urllib.request.Request(
    f"{N8N_URL}/api/v1/workflows/{WF_ID}",
    headers={"X-N8N-API-KEY": N8N_KEY},
)
wf = json.loads(urllib.request.urlopen(req).read())
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)
print(f"Exported {len(wf['nodes'])} nodes to {OUT}")
