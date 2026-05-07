"""Patch volunteer_entry workflow: thread remoteJid + fix location regex."""
import json
import urllib.request
import urllib.error

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

# Fetch current workflow
wf = api("GET", f"/api/v1/workflows/{WF_ID}")

# Build node map
nodes = {n["name"]: n for n in wf["nodes"]}

# ── 1. Code: Transcribe + Extract ─────────────────────────────────────────────
nodes["Code: Transcribe + Extract"]["parameters"]["jsCode"] = (
    "const razpotje = $('Razpotje').first().json;\n"
    "const phone = razpotje.phone;\n"
    "const remoteJid = razpotje.remoteJid;\n"
    "const b64raw = $('HTTP: Fetch Media').first().json.base64 || '';\n"
    "const b64 = b64raw.replace(/^data:[^,]*,/, '');\n"
    "if (!b64) throw new Error('Ni zvočnega posnetka v sporočilu');\n"
    "const wResp = await this.helpers.httpRequest({\n"
    "  method: 'POST',\n"
    "  url: 'http://whisper:8001/transcribe',\n"
    "  headers: {'Content-Type': 'application/json'},\n"
    "  body: JSON.stringify({audio_base64: b64}),\n"
    "  returnFullResponse: true\n"
    "});\n"
    "const transcript = (typeof wResp.body === 'string' ? wResp.body : wResp.body.toString('utf-8')).trim();\n"
    "const hoursM = transcript.match(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/i);\n"
    "const hours = hoursM ? parseFloat(hoursM[1].replace(',', '.')) : 1.0;\n"
    "const today = new Date();\n"
    "let entryDate = new Date(today);\n"
    "const tl = transcript.toLowerCase();\n"
    "if (tl.includes('včeraj') || tl.includes('vceraj')) {\n"
    "  entryDate.setDate(today.getDate() - 1);\n"
    "} else {\n"
    "  const days = [{n:'ponedeljek',d:1},{n:'torku',d:2},{n:'torek',d:2},{n:'sredo',d:3},{n:'sredi',d:3},{n:'četrtek',d:4},{n:'cetrtek',d:4},{n:'petek',d:5},{n:'soboto',d:6},{n:'nedeljo',d:0}];\n"
    "  for (const {n, d} of days) {\n"
    "    if (tl.includes(n)) { const diff = ((today.getDay()-d)+7)%7||7; entryDate=new Date(today); entryDate.setDate(today.getDate()-diff); break; }\n"
    "  }\n"
    "  const dm = transcript.match(/\\b(\\d{1,2})[.\\s]+(\\d{1,2})\\. /);\n"
    "  if (dm) entryDate = new Date(today.getFullYear(), parseInt(dm[2])-1, parseInt(dm[1]));\n"
    "}\n"
    "let location = null;\n"
    "const locKraj = transcript.match(/\\bkraj\\s*[,;:]?\\s*([A-Za-z\\u0160\\u017D\\u010C\\u0106\\u0110\\u0161\\u017E\\u010D\\u0107\\u0111][^\\.,!?\\n]{0,50})/i);\n"
    "if (locKraj) {\n"
    "  location = locKraj[1].trim().replace(/\\s*(?:uro|uri|ure|ur\\b).*/i, '').trim();\n"
    "} else {\n"
    "  const locM = transcript.match(/\\b(?:v|pri|na)\\s+([A-Z\\u0160\\u017D\\u010C\\u0106\\u0110][a-z\\u0161\\u017E\\u010D\\u0107\\u0111]+(?:\\s+[A-Z\\u0160\\u017D\\u010C\\u0106\\u0110][a-z\\u0161\\u017E\\u010D\\u0107\\u0111]+)*)/);\n"
    "  location = locM ? locM[1] : null;\n"
    "}\n"
    "let activity = transcript.replace(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/gi,'').replace(/\\b(danes|včeraj|vceraj|ponedeljek|torek|torku|sredo|sredi|četrtek|cetrtek|petek|soboto|nedeljo)\\b/gi,'').replace(/\\s{2,}/g,' ').trim()||transcript.trim();\n"
    "return [{json: {phone, remoteJid, entry_date: entryDate.toISOString().split('T')[0], hours, activity_description: activity, location, raw_transcript: transcript}}];"
)

# ── 2. Text Extract ────────────────────────────────────────────────────────────
nodes["Text Extract"]["parameters"]["jsCode"] = (
    "const inp = $input.first().json;\n"
    "const phone = inp.phone;\n"
    "const remoteJid = inp.remoteJid;\n"
    "const text = inp.text || '';\n"
    "const hoursM = text.match(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/i);\n"
    "const hours = hoursM ? parseFloat(hoursM[1].replace(',', '.')) : 1.0;\n"
    "const today = new Date();\n"
    "let entryDate = new Date(today);\n"
    "const tl = text.toLowerCase();\n"
    "if (tl.includes('včeraj') || tl.includes('vceraj')) {\n"
    "  entryDate.setDate(today.getDate() - 1);\n"
    "} else {\n"
    "  const days = [{n:'ponedeljek',d:1},{n:'torku',d:2},{n:'torek',d:2},{n:'sredo',d:3},{n:'sredi',d:3},{n:'četrtek',d:4},{n:'cetrtek',d:4},{n:'petek',d:5},{n:'soboto',d:6},{n:'nedeljo',d:0}];\n"
    "  for (const {n, d} of days) {\n"
    "    if (tl.includes(n)) { const diff = ((today.getDay()-d)+7)%7||7; entryDate=new Date(today); entryDate.setDate(today.getDate()-diff); break; }\n"
    "  }\n"
    "  const dm = text.match(/\\b(\\d{1,2})[.\\s]+(\\d{1,2})\\. /);\n"
    "  if (dm) entryDate = new Date(today.getFullYear(), parseInt(dm[2])-1, parseInt(dm[1]));\n"
    "}\n"
    "let location = null;\n"
    "const locKraj = text.match(/\\bkraj\\s*[,;:]?\\s*([A-Za-z\\u0160\\u017D\\u010C\\u0106\\u0110\\u0161\\u017E\\u010D\\u0107\\u0111][^\\.,!?\\n]{0,50})/i);\n"
    "if (locKraj) {\n"
    "  location = locKraj[1].trim().replace(/\\s*(?:uro|uri|ure|ur\\b).*/i, '').trim();\n"
    "} else {\n"
    "  const locM = text.match(/\\b(?:v|pri|na)\\s+([A-Z\\u0160\\u017D\\u010C\\u0106\\u0110][a-z\\u0161\\u017E\\u010D\\u0107\\u0111]+(?:\\s+[A-Z\\u0160\\u017D\\u010C\\u0106\\u0110][a-z\\u0161\\u017E\\u010D\\u0107\\u0111]+)*)/);\n"
    "  location = locM ? locM[1] : null;\n"
    "}\n"
    "let activity = text.replace(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/gi,'').replace(/\\b(danes|včeraj|vceraj|ponedeljek|torek|torku|sredo|sredi|četrtek|cetrtek|petek|soboto|nedeljo)\\b/gi,'').replace(/\\s{2,}/g,' ').trim()||text.trim();\n"
    "return [{json: {phone, remoteJid, entry_date: entryDate.toISOString().split('T')[0], hours, activity_description: activity, location, raw_transcript: null}}];"
)

# ── 3. Code: Pripravi Prostovoljca ────────────────────────────────────────────
nodes["Code: Pripravi Prostovoljca"]["parameters"]["jsCode"] = (
    "const apiResp = $input.first().json;\n"
    "let upstream;\n"
    "try { upstream = $('Code: Transcribe + Extract').first().json; } catch(e) {}\n"
    "if (!upstream || !upstream.phone) { try { upstream = $('Text Extract').first().json; } catch(e) {} }\n"
    "const found = apiResp.total > 0 && apiResp.items && apiResp.items.length > 0;\n"
    "const vol = found ? apiResp.items[0] : null;\n"
    "return [{ json: {\n"
    "  phone: upstream.phone,\n"
    "  remoteJid: upstream.remoteJid,\n"
    "  entry_date: upstream.entry_date,\n"
    "  hours: upstream.hours,\n"
    "  activity_description: upstream.activity_description,\n"
    "  location: upstream.location,\n"
    "  raw_transcript: upstream.raw_transcript,\n"
    "  found,\n"
    "  volunteer_id: found ? vol.id : null,\n"
    "  volunteer_name: found ? (vol.first_name + ' ' + vol.last_name) : null\n"
    "}}];"
)

# ── 4. Code: Shrani Stanje ────────────────────────────────────────────────────
nodes["Code: Shrani Stanje"]["parameters"]["jsCode"] = (
    "const entryResp = $input.first().json;\n"
    "const up = $('Code: Pripravi Prostovoljca').first().json;\n"
    "const phone = up.phone;\n"
    "const remoteJid = up.remoteJid;\n"
    "const entry_id = entryResp.id;\n"
    "const sd = $getWorkflowStaticData('global');\n"
    "sd[phone] = {\n"
    "  entry_id,\n"
    "  entry_date: up.entry_date,\n"
    "  hours: up.hours,\n"
    "  activity_description: up.activity_description,\n"
    "  location: up.location,\n"
    "  volunteer_name: up.volunteer_name,\n"
    "  remoteJid\n"
    "};\n"
    "const d = up.entry_date ? new Date(up.entry_date) : new Date();\n"
    "const dateStr = d.toLocaleDateString('sl-SI', {day:'2-digit',month:'2-digit',year:'numeric'});\n"
    "const locStr = up.location ? ` v ${up.location}` : '';\n"
    "const msg = `Zabeležili smo vaš vnos:\\n📅 ${dateStr}\\n⏱ ${up.hours} ur\\n📍${locStr}\\n📝 ${up.activity_description}\\n\\nAli je vse pravilno?\\n1 - Potrdi\\n2 - Popravi\\n3 - Prekliči`;\n"
    "return [{json: {phone, remoteJid, text: msg}}];"
)

# ── 5. Naloži Stanje ──────────────────────────────────────────────────────────
nodes["Naloži Stanje"]["parameters"]["jsCode"] = (
    "const inp = $input.first().json;\n"
    "const phone = inp.phone;\n"
    "const remoteJid = inp.remoteJid;\n"
    "const responseType = inp.responseType;\n"
    "const sd = $getWorkflowStaticData('global');\n"
    "const state = sd[phone] || null;\n"
    "if (!state) return [{json: {phone, remoteJid, responseType, entry_id: null}}];\n"
    "return [{json: {\n"
    "  phone,\n"
    "  remoteJid: state.remoteJid || remoteJid,\n"
    "  responseType,\n"
    "  entry_id: state.entry_id,\n"
    "  entry_date: state.entry_date,\n"
    "  hours: state.hours,\n"
    "  activity_description: state.activity_description,\n"
    "  location: state.location,\n"
    "  volunteer_name: state.volunteer_name\n"
    "}}];"
)

# ── 6. Code: Clear State Confirm ──────────────────────────────────────────────
nodes["Code: Clear State Confirm"]["parameters"]["jsCode"] = (
    "const st = $input.first().json;\n"
    "const phone = st.phone;\n"
    "const remoteJid = st.remoteJid;\n"
    "const sd = $getWorkflowStaticData('global');\n"
    "delete sd[phone];\n"
    "return [{json: {\n"
    "  phone,\n"
    "  remoteJid,\n"
    "  entry_date: st.entry_date,\n"
    "  hours: st.hours,\n"
    "  activity_description: st.activity_description,\n"
    "  location: st.location,\n"
    "  volunteer_name: st.volunteer_name\n"
    "}}];"
)

# ── 7. Code: Clear State Popravi ─────────────────────────────────────────────
nodes["Code: Clear State Popravi"]["parameters"]["jsCode"] = (
    "const st = $input.first().json;\n"
    "const phone = st.phone;\n"
    "const remoteJid = st.remoteJid;\n"
    "const sd = $getWorkflowStaticData('global');\n"
    "delete sd[phone];\n"
    "return [{json: {phone, remoteJid}}];"
)

# ── 8. Code: Clear State Prekliči ─────────────────────────────────────────────
nodes["Code: Clear State Prekliči"]["parameters"]["jsCode"] = (
    "const st = $input.first().json;\n"
    "const phone = st.phone;\n"
    "const remoteJid = st.remoteJid;\n"
    "const sd = $getWorkflowStaticData('global');\n"
    "delete sd[phone];\n"
    "return [{json: {phone, remoteJid}}];"
)

# ── 9. WA HTTP nodes — switch number param to $json.remoteJid ─────────────────
wa_nodes = [
    "HTTP: WA Ni Registriran",
    "HTTP: WA Potrditev",
    "HTTP: WA Ni Aktivnega Vnosa",
    "HTTP: WA Potrjeno",
    "HTTP: WA Upravljalcu",
    "HTTP: WA Popravi",
    "HTTP: WA Prekliči",
]
for name in wa_nodes:
    if name not in nodes:
        print(f"WARNING: node '{name}' not found, skipping")
        continue
    params = nodes[name]["parameters"]
    bp = params.get("bodyParameters", {}).get("parameters", [])
    for p in bp:
        if p.get("name") == "number":
            p["value"] = "={{ $json.remoteJid }}"
    params["bodyParameters"] = {"parameters": bp}

# ── Build PUT payload ─────────────────────────────────────────────────────────
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
print("Node count:", len(result.get("nodes", [])))
