"""Deploy fixed workflow to n8n instance."""
import json, urllib.request

N8N_URL = "http://localhost:5678"
N8N_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlYzJjNTY1Ni0zOTA5LTRlNzctOTZjYy00N2E2MjNmZDcwNGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiM2I3YWZiNjQtZDI0OC00M2QxLTlkNWItOGFhMGYxNzIxOTc1IiwiaWF0IjoxNzc3NzMxMDU3fQ.GV2V96vGSJjq1sBMJvKOcl72QLZCXPNlX7__i4npKTU"
WF_ID = "Lw6qRiO9ozSr6EeW"

with open("d:/Andrej/vsCode-workspace/BelPro/n8n/workflows/volunteer_entry.json", "r", encoding="utf-8") as f:
    wf = json.load(f)

settings = {}
if wf.get("settings"):
    allowed = {"saveManualExecutions", "saveExecutionProgress", "executionTimeout",
               "maxConcurrentExecutions", "timezone", "executionOrder", "callerPolicy"}
    for k, v in wf["settings"].items():
        if k in allowed:
            settings[k] = v

put_payload = {
    "name": wf["name"],
    "description": wf.get("description") or "",
    "nodes": wf["nodes"],
    "connections": wf["connections"],
    "settings": settings,
}

body = json.dumps(put_payload).encode()
req = urllib.request.Request(
    f"{N8N_URL}/api/v1/workflows/{WF_ID}",
    data=body,
    method="PUT",
    headers={"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as r:
    result = json.loads(r.read())
    print(f"PUT result id: {result.get('id')}, active: {result.get('active')}")

# Verify
vf = json.loads(urllib.request.urlopen(urllib.request.Request(
    f"{N8N_URL}/api/v1/workflows/{WF_ID}",
    headers={"X-N8N-API-KEY": N8N_KEY},
)).read())

nv = {n["name"]: n for n in vf["nodes"]}
for name in ["Code: Clear State Popravi", "Code: Clear State Prekliči"]:
    js = nv[name]["parameters"]["jsCode"]
    ok = "Nalozi Stanje" in js and "$input" not in js
    print(f"  {name}: {'OK' if ok else 'FAIL'}")
