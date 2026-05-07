"""Patch v3: LID→real JID via findContacts, Slovenian word-hours parsing."""
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

# Shared Slovenian word-to-number hour parser (used in both Code nodes)
WORD_HOURS_JS = r"""
function parseHours(text) {
  const numM = text.match(/(\d+(?:[.,]\d+)?)\s*(?:uro|uri|ure|ur\b)/i);
  if (numM) return parseFloat(numM[1].replace(',', '.'));
  // Slovenian cardinal words
  const words = {
    'ena': 1, 'eno': 1, 'eni': 1,
    'dve': 2, 'dva': 2, 'dveh': 2,
    'tri': 3, 'treh': 3,
    'štiri': 4, 'štirib': 4,
    'pet': 5, 'petih': 5,
    'šest': 6, 'šestih': 6,
    'sedem': 7, 'sedmih': 7,
    'osem': 8, 'osmih': 8,
    'devet': 9, 'devetih': 9,
    'deset': 10, 'desetih': 10,
    'enajst': 11, 'enajstih': 11,
    'dvanajst': 12, 'dvanajstih': 12,
    'trinajst': 13, 'štirinajst': 14,
    'petnajst': 15, 'šestnajst': 16,
    'sedemnajst': 17, 'osemnajst': 18,
    'devetnajst': 19, 'dvajset': 20,
    'enaindvajset': 21, 'dvaindvajset': 22, 'triindvajset': 23,
  };
  const tl = text.toLowerCase();
  const wordM = tl.match(/(\w+)\s*ur/i);
  if (wordM && words[wordM[1]] !== undefined) return words[wordM[1]];
  return 1.0;
}
""".strip()

# Shared location regex (used in both Code nodes)
LOC_JS = r"""
function extractLocation(text) {
  const locKraj = text.match(/\bkraj\s*[,;:]?\s*([A-Za-zŠŽČĆĐšžčćđ][^\.,!?\n]{0,50})/i);
  if (locKraj) return locKraj[1].trim().replace(/\s*(?:uro|uri|ure|ur\b).*/i, '').trim();
  const locM = text.match(/\b(?:v|pri|na)\s+([A-ZŠŽČĆĐ][a-zšžčćđ]+(?:\s+[A-ZŠŽČĆĐ][a-zšžčćđ]+)*)/);
  return locM ? locM[1] : null;
}
""".strip()

# Shared date extraction JS
DATE_JS = r"""
function extractDate(text) {
  const today = new Date();
  let entryDate = new Date(today);
  const tl = text.toLowerCase();
  if (tl.includes('včeraj') || tl.includes('vceraj')) {
    entryDate.setDate(today.getDate() - 1);
  } else {
    const days = [{n:'ponedeljek',d:1},{n:'torku',d:2},{n:'torek',d:2},{n:'sredo',d:3},{n:'sredi',d:3},{n:'četrtek',d:4},{n:'cetrtek',d:4},{n:'petek',d:5},{n:'soboto',d:6},{n:'nedeljo',d:0}];
    for (const {n, d} of days) {
      if (tl.includes(n)) { const diff = ((today.getDay()-d)+7)%7||7; entryDate=new Date(today); entryDate.setDate(today.getDate()-diff); break; }
    }
    const dm = text.match(/\b(\d{1,2})[.\s]+(\d{1,2})\. /);
    if (dm) entryDate = new Date(today.getFullYear(), parseInt(dm[2])-1, parseInt(dm[1]));
  }
  return entryDate.toISOString().split('T')[0];
}
""".strip()

# ── 1. Filter & Route: LID→real JID lookup via findContacts ──────────────────
nodes["Filter & Route"]["parameters"]["jsCode"] = (
    "const body = $input.first().json.body;\n"
    "if (!body || body.event !== 'messages.upsert') return [];\n"
    "const data = body.data;\n"
    "if (!data || !data.key || data.key.fromMe === true) return [];\n"
    "const rawJid = data.key.remoteJid || '';\n"
    "const isLid = rawJid.endsWith('@lid');\n"
    "let phone = rawJid.split('@')[0].split(':')[0];\n"
    "let remoteJid = rawJid;\n"
    "if (isLid) {\n"
    "  // Try data.sender first (some Evolution versions populate it)\n"
    "  const senderRaw = (data.sender || data.senderPn || '').split('@')[0];\n"
    "  if (senderRaw && senderRaw.length >= 7 && !senderRaw.includes('lid')) {\n"
    "    phone = senderRaw;\n"
    "    remoteJid = senderRaw + '@s.whatsapp.net';\n"
    "  } else {\n"
    "    // Resolve via findContacts: get pushName for this LID, then find @s.whatsapp.net entry\n"
    "    try {\n"
    "      const lidResp = await this.helpers.httpRequest({\n"
    "        method: 'POST',\n"
    "        url: 'http://evolution-api:8080/chat/findContacts/belpro',\n"
    "        headers: {'Content-Type': 'application/json', 'apikey': 'fe3ba6358a418966f4034b9206aed25fb21911c93e7ed023'},\n"
    "        body: JSON.stringify({where: {remoteJid: rawJid}}),\n"
    "        returnFullResponse: false\n"
    "      });\n"
    "      const lidData = typeof lidResp === 'string' ? JSON.parse(lidResp) : lidResp;\n"
    "      const lidContacts = lidData.value || lidData;\n"
    "      const lidEntry = Array.isArray(lidContacts) ? lidContacts[0] : null;\n"
    "      if (lidEntry && lidEntry.pushName) {\n"
    "        const pushName = lidEntry.pushName;\n"
    "        // Now find the @s.whatsapp.net entry with same pushName\n"
    "        const nameResp = await this.helpers.httpRequest({\n"
    "          method: 'POST',\n"
    "          url: 'http://evolution-api:8080/chat/findContacts/belpro',\n"
    "          headers: {'Content-Type': 'application/json', 'apikey': 'fe3ba6358a418966f4034b9206aed25fb21911c93e7ed023'},\n"
    "          body: JSON.stringify({where: {pushName}}),\n"
    "          returnFullResponse: false\n"
    "        });\n"
    "        const nameData = typeof nameResp === 'string' ? JSON.parse(nameResp) : nameResp;\n"
    "        const nameContacts = (nameData.value || nameData);\n"
    "        const real = Array.isArray(nameContacts)\n"
    "          ? nameContacts.find(c => c.remoteJid && c.remoteJid.endsWith('@s.whatsapp.net'))\n"
    "          : null;\n"
    "        if (real) {\n"
    "          remoteJid = real.remoteJid;\n"
    "          phone = real.remoteJid.split('@')[0];\n"
    "        }\n"
    "      }\n"
    "    } catch(e) {\n"
    "      // keep rawJid if lookup fails\n"
    "    }\n"
    "  }\n"
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

# ── 2. Code: Transcribe + Extract — add word-based hours ─────────────────────
nodes["Code: Transcribe + Extract"]["parameters"]["jsCode"] = (
    WORD_HOURS_JS + "\n" + LOC_JS + "\n" + DATE_JS + "\n"
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
    "const hours = parseHours(transcript);\n"
    "const location = extractLocation(transcript);\n"
    "const entry_date = extractDate(transcript);\n"
    "let activity = transcript.replace(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/gi,'').replace(/\\b(danes|včeraj|vceraj|ponedeljek|torek|torku|sredo|sredi|četrtek|cetrtek|petek|soboto|nedeljo)\\b/gi,'').replace(/\\s{2,}/g,' ').trim()||transcript.trim();\n"
    "return [{json: {phone, remoteJid, pushName, entry_date, hours, activity_description: activity, location, raw_transcript: transcript}}];"
)

# ── 3. Text Extract — add word-based hours ────────────────────────────────────
nodes["Text Extract"]["parameters"]["jsCode"] = (
    WORD_HOURS_JS + "\n" + LOC_JS + "\n" + DATE_JS + "\n"
    "const inp = $input.first().json;\n"
    "const phone = inp.phone;\n"
    "const remoteJid = inp.remoteJid;\n"
    "const pushName = inp.pushName || '';\n"
    "const text = inp.text || '';\n"
    "const hours = parseHours(text);\n"
    "const location = extractLocation(text);\n"
    "const entry_date = extractDate(text);\n"
    "let activity = text.replace(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/gi,'').replace(/\\b(danes|včeraj|vceraj|ponedeljek|torek|torku|sredo|sredi|četrtek|cetrtek|petek|soboto|nedeljo)\\b/gi,'').replace(/\\s{2,}/g,' ').trim()||text.trim();\n"
    "return [{json: {phone, remoteJid, pushName, entry_date, hours, activity_description: activity, location, raw_transcript: null}}];"
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
