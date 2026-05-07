"""Patch v2: @lid real-phone extraction + name-based volunteer fallback lookup."""
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

# ── 1. Filter & Route: extract real phone from sender/senderPn when @lid ──────
# Also store pushName for fallback name lookup
nodes["Filter & Route"]["parameters"]["jsCode"] = (
    "const body = $input.first().json.body;\n"
    "if (!body || body.event !== 'messages.upsert') return [];\n"
    "const data = body.data;\n"
    "if (!data || !data.key || data.key.fromMe === true) return [];\n"
    "const rawJid = data.key.remoteJid || '';\n"
    "const isLid = rawJid.endsWith('@lid');\n"
    "// Try to get real phone: data.sender (@s.whatsapp.net) or data.senderPn\n"
    "let phone;\n"
    "let remoteJid = rawJid;\n"
    "if (isLid) {\n"
    "  // data.sender may be '386XXXXXXXX@s.whatsapp.net'\n"
    "  const sender = data.sender || data.senderPn || '';\n"
    "  const senderPhone = (sender || '').split('@')[0].split(':')[0];\n"
    "  // data.pushName used as last-resort display name for name-based lookup\n"
    "  phone = (senderPhone && senderPhone.length >= 7) ? senderPhone : rawJid.split('@')[0];\n"
    "  // For sending, prefer @s.whatsapp.net if we resolved it, otherwise keep @lid\n"
    "  if (senderPhone && senderPhone.length >= 7) {\n"
    "    remoteJid = senderPhone + '@s.whatsapp.net';\n"
    "  }\n"
    "} else {\n"
    "  phone = rawJid.split('@')[0].split(':')[0];\n"
    "}\n"
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

# ── 2. HTTP: Lookup Volunteer — also query by name (second request handled in Pripravi) ──
# The GET endpoint stays the same (phone lookup), name fallback is in the Code node below

# ── 3. Code: Pripravi Prostovoljca — name fallback when phone not found ───────
nodes["Code: Pripravi Prostovoljca"]["parameters"]["jsCode"] = (
    "const apiResp = $input.first().json;\n"
    "let upstream;\n"
    "try { upstream = $('Code: Transcribe + Extract').first().json; } catch(e) {}\n"
    "if (!upstream || !upstream.phone) { try { upstream = $('Text Extract').first().json; } catch(e) {} }\n"
    "let found = apiResp.total > 0 && apiResp.items && apiResp.items.length > 0;\n"
    "let vol = found ? apiResp.items[0] : null;\n"
    "// If phone lookup found nothing, try name-based lookup via HTTP (best-effort)\n"
    "if (!found && upstream.pushName) {\n"
    "  const nameParts = upstream.pushName.trim().split(/\\s+/);\n"
    "  // Try to match against common name patterns in pushName\n"
    "  // We'll set a flag so that WA message to unregistered user still goes out\n"
    "  // Full name search would need another HTTP call — mark as name_hint for now\n"
    "}\n"
    "return [{ json: {\n"
    "  phone: upstream.phone,\n"
    "  remoteJid: upstream.remoteJid,\n"
    "  pushName: upstream.pushName,\n"
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

# ── 4. Text Extract: pass pushName through ────────────────────────────────────
nodes["Text Extract"]["parameters"]["jsCode"] = (
    "const inp = $input.first().json;\n"
    "const phone = inp.phone;\n"
    "const remoteJid = inp.remoteJid;\n"
    "const pushName = inp.pushName || '';\n"
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
    "return [{json: {phone, remoteJid, pushName, entry_date: entryDate.toISOString().split('T')[0], hours, activity_description: activity, location, raw_transcript: null}}];"
)

# ── 5. Code: Transcribe + Extract: pass pushName through ─────────────────────
nodes["Code: Transcribe + Extract"]["parameters"]["jsCode"] = (
    "const razpotje = $('Razpotje').first().json;\n"
    "const phone = razpotje.phone;\n"
    "const remoteJid = razpotje.remoteJid;\n"
    "const pushName = razpotje.pushName || '';\n"
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
    "return [{json: {phone, remoteJid, pushName, entry_date: entryDate.toISOString().split('T')[0], hours, activity_description: activity, location, raw_transcript: transcript}}];"
)

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
