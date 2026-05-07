"""Patch v4: Use remoteJidAlt from v2.3.7 webhook; remove unreliable findContacts lookup."""
import json
import urllib.request

N8N_URL = "http://localhost:5678"
N8N_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlYzJjNTY1Ni0zOTA5LTRlNzctOTZjYy00N2E2MjNmZDcwNGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiM2I3YWZiNjQtZDI0OC00M2QxLTlkNWItOGFhMGYxNzIxOTc1IiwiaWF0IjoxNzc3NzMxMDU3fQ.GV2V96vGSJjq1sBMJvKOcl72QLZCXPNlX7__i4npKTU"
WF_ID = "Lw6qRiO9ozSr6EeW"

def api(method, path, data=None):
    url = N8N_URL + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method,
        headers={"X-N8N-API-KEY": N8N_KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

wf = api("GET", f"/api/v1/workflows/{WF_ID}")
nodes = {n["name"]: n for n in wf["nodes"]}

# ── Filter & Route: clean @lid resolution using remoteJidAlt (v2.3.7+) ───────
# Falls back to @lid itself for sending (v2.3.7 sendText accepts @lid directly)
nodes["Filter & Route"]["parameters"]["jsCode"] = (
    "const body = $input.first().json.body;\n"
    "if (!body || body.event !== 'messages.upsert') return [];\n"
    "const data = body.data;\n"
    "if (!data || !data.key || data.key.fromMe === true) return [];\n"
    "const rawJid = data.key.remoteJid || '';\n"
    "// v2.3.7: remoteJidAlt contains @s.whatsapp.net when remoteJid is @lid\n"
    "const resolvedJid = (rawJid.endsWith('@lid') && data.remoteJidAlt)\n"
    "  ? data.remoteJidAlt\n"
    "  : rawJid;\n"
    "// For sending: prefer resolved @s.whatsapp.net; @lid also works in v2.3.7\n"
    "const remoteJid = resolvedJid;\n"
    "const phone = resolvedJid.split('@')[0].split(':')[0];\n"
    "if (!phone || phone.length < 5) return [];\n"
    "const pushName = data.pushName || '';\n"
    "const msg = data.message || {};\n"
    "const messageType = data.messageType || Object.keys(msg)[0] || '';\n"
    "let route = 'skip', text = '', responseType = '';\n"
    "if (messageType === 'audioMessage' || messageType === 'pttMessage') {\n"
    "  route = 'audio';\n"
    "} else if (messageType === 'buttonsResponseMessage') {\n"
    "  responseType = ((msg.buttonsResponseMessage || {}).selectedButtonId || '').toLowerCase();\n"
    "  if (!['confirm','edit','cancel'].includes(responseType)) responseType = 'unknown';\n"
    "  route = 'response';\n"
    "} else if (messageType === 'conversation' || messageType === 'extendedTextMessage') {\n"
    "  text = msg.conversation || ((msg.extendedTextMessage || {}).text) || '';\n"
    "  const t = text.trim().toLowerCase();\n"
    "  if (t === '1' || t === 'potrdi') { route = 'response'; responseType = 'confirm'; }\n"
    "  else if (t === '2' || t === 'popravi') { route = 'response'; responseType = 'edit'; }\n"
    "  else if (t === '3' || t.startsWith('prekli')) { route = 'response'; responseType = 'cancel'; }\n"
    "  else { route = 'text_new'; }\n"
    "} else { return []; }\n"
    "if (route === 'skip') return [];\n"
    "return [{json: {phone, remoteJid, pushName, route, text, responseType, messageKey: data.key, messageData: msg}}];"
)

put_payload = {
    "name": wf["name"],
    "description": wf.get("description") or "",
    "nodes": list(nodes.values()),
    "connections": wf["connections"],
    "settings": wf.get("settings", {}),
    "staticData": wf.get("staticData"),
}

result = api("PUT", f"/api/v1/workflows/{WF_ID}", put_payload)
print("PUT result id:", result.get("id"), "active:", result.get("active"))
