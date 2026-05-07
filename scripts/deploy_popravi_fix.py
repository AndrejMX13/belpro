"""Deploy popravi-fixed workflow to n8n."""
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

# Check new nodes exist
new_nodes = ["Code: Pripravi Popravek", "Code: Preveri Nacin", "Code: Procesiraj Popravek",
             "HTTP: Brisi Stari Vnos", "HTTP: Ustvari Nov Vnos",
             "Code: Shrani Stanje Popravek", "HTTP: WA Potrditev Popravek"]
for name in new_nodes:
    if name in nv:
        print(f"  Found: {name}")
    else:
        print(f"  MISSING: {name}")

# Check removed nodes are gone
for name in ["HTTP: Brisi Popravi", "Code: Clear State Popravi"]:
    if name not in nv:
        print(f"  Correctly removed: {name}")
    else:
        print(f"  STILL PRESENT: {name}")

# Verify WA Popravi uses dynamic text
wa_popravi_text = None
for p in nv["HTTP: WA Popravi"]["parameters"]["bodyParameters"]["parameters"]:
    if p["name"] == "text":
        wa_popravi_text = p["value"]
        break
print(f"  HTTP: WA Popravi text: {wa_popravi_text}")

print("\nDeploy complete.")
