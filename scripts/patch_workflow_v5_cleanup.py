"""Patch v5: Remove pushName and name-based fallback — phone-only lookup is reliable now."""
import json
import urllib.request

N8N_URL = "http://localhost:5678"
N8N_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlYzJjNTY1Ni0zOTA5LTRlNzctOTZjYy00N2E2MjNmZDcwNGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiM2I3YWZiNjQtZDI0OC00M2QxLTlkNWItOGFhMGYxNzIxOTc1IiwiaWF0IjoxNzc3NzMxMDU3fQ.GV2V96vGSJjq1sBMJvKOcl72QLZCXPNlX7__i4npKTU"
WF_ID = "Lw6qRiO9ozSr6EeW"


def api(method, path, data=None):
    url = N8N_URL + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


wf = api("GET", f"/api/v1/workflows/{WF_ID}")
nodes = {n["name"]: n for n in wf["nodes"]}

# ── 1. Filter & Route ─────────────────────────────────────────────────────
js = nodes["Filter & Route"]["parameters"]["jsCode"]
js = js.replace("\nconst pushName = data.pushName || '';", "")
js = js.replace("pushName, ", "")
nodes["Filter & Route"]["parameters"]["jsCode"] = js

# ── 2. Text Extract ────────────────────────────────────────────────────────
js = nodes["Text Extract"]["parameters"]["jsCode"]
js = js.replace("\nconst pushName = inp.pushName || '';", "")
js = js.replace("pushName, ", "")
nodes["Text Extract"]["parameters"]["jsCode"] = js

# ── 3. Code: Transcribe + Extract ──────────────────────────────────────────
js = nodes["Code: Transcribe + Extract"]["parameters"]["jsCode"]
js = js.replace("\nconst pushName = razpotje.pushName || '';", "")
js = js.replace("pushName, ", "")
nodes["Code: Transcribe + Extract"]["parameters"]["jsCode"] = js

# ── 4. Code: Pripravi Prostovoljca ─────────────────────────────────────────
js = nodes["Code: Pripravi Prostovoljca"]["parameters"]["jsCode"]
# Remove dead name-fallback block
old_block = (
    "\n// If phone lookup found nothing, try name-based lookup via HTTP (best-effort)\n"
    "if (!found && upstream.pushName) {\n"
    "  const nameParts = upstream.pushName.trim().split(/\\s+/);\n"
    "  // Try to match against common name patterns in pushName\n"
    "  // We'll set a flag so that WA message to unregistered user still goes out\n"
    "  // Full name search would need another HTTP call — mark as name_hint for now\n"
    "}"
)
if old_block in js:
    js = js.replace(old_block, "")
    print("  Removed name fallback block")
else:
    print("  WARNING: name fallback block not found")

# Remove pushName from return object body
js = js.replace("  pushName: upstream.pushName,\n", "")
js = js.replace("pushName, ", "")
nodes["Code: Pripravi Prostovoljca"]["parameters"]["jsCode"] = js

# ── PUT — strip problematic settings fields ────────────────────────────────
settings = {}
if wf.get("settings"):
    allowed = {"saveManualExecutions", "saveExecutionProgress", "executionTimeout",
               "maxConcurrentExecutions", "timezone", "executionOrder",
               "callerPolicy"}
    for k, v in wf["settings"].items():
        if k in allowed:
            settings[k] = v

put_payload = {
    "name": wf["name"],
    "description": wf.get("description") or "",
    "nodes": list(nodes.values()),
    "connections": wf["connections"],
    "settings": settings,
}
result = api("PUT", f"/api/v1/workflows/{WF_ID}", put_payload)
print("PUT result id:", result.get("id"), "active:", result.get("active"))

# ── Verify ─────────────────────────────────────────────────────────────────
wf2 = api("GET", f"/api/v1/workflows/{WF_ID}")
n2 = {n["name"]: n for n in wf2["nodes"]}
all_ok = True
for name in [
    "Filter & Route",
    "Text Extract",
    "Code: Transcribe + Extract",
    "Code: Pripravi Prostovoljca",
]:
    count = n2[name]["parameters"]["jsCode"].count("pushName")
    status = "OK" if count == 0 else f"FAIL ({count})"
    if count > 0:
        all_ok = False
    print(f"  {name}: {status}")

print("ALL CLEAN" if all_ok else "SOME FAILURES")
