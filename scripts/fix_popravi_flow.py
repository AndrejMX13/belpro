"""Fix Popravi flow: show transcript for editing instead of just discarding."""
import json, sys, io, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = "d:/Andrej/vsCode-workspace/BelPro/n8n/workflows/volunteer_entry.json"
with open(PATH, "r", encoding="utf-8") as f:
    wf = json.load(f)

nodes = wf["nodes"]
conns = wf["connections"]

# ── 1. Remove old Popravi nodes ──
nodes_by_id = {n["id"]: n for n in nodes}
nodes[:] = [n for n in nodes if n["id"] not in ("http_brisi_popravi", "code_clear_popravi")]

# ── 2. Modify HTTP: WA Popravi to use dynamic text ──
for n in nodes:
    if n["id"] == "http_wa_popravi":
        for p in n["parameters"]["bodyParameters"]["parameters"]:
            if p["name"] == "text":
                p["value"] = "={{ $json.text }}"
        break

# ── 3. Add Code: Pripravi Popravek (replaces HTTP: Brisi Popravi) ──
pripravi_popravek = {
    "id": "code_pripravi_popravek",
    "name": "Code: Pripravi Popravek",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1800, 560],
    "parameters": {
        "jsCode": (
            'const st = $("Nalozi Stanje").first().json;\n'
            'const phone = st.phone;\n'
            'const remoteJid = st.remoteJid;\n'
            'const sd = $getWorkflowStaticData("global");\n'
            'const state = sd[phone] || {};\n'
            'state.mode = "editing";\n'
            'sd[phone] = state;\n'
            'const d = st.entry_date ? new Date(st.entry_date) : new Date();\n'
            'const dateStr = d.toLocaleDateString("sl-SI", {day:"2-digit",month:"2-digit",year:"numeric"});\n'
            'const locStr = st.location ? " v " + st.location : "";\n'
            'const msg = "Popravite vaš vnos:\\n📅 " + dateStr + "\\n⏱ " + st.hours + " ur\\n📍" + locStr + "\\n📝 " + st.activity_description + "\\n\\nPošljite popravljeno besedilo.";\n'
            'return [{json: {phone, remoteJid, text: msg}}];'
        )
    }
}
nodes.append(pripravi_popravek)

# ── 4. Add Code: Preveri Nacin (reads edit mode, sets mode field) ──
preveri_nacin = {
    "id": "code_preveri_nacin",
    "name": "Code: Preveri Nacin",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1280, 300],
    "parameters": {
        "jsCode": (
            'const inp = $input.first().json;\n'
            'const sd = $getWorkflowStaticData("global");\n'
            'const state = sd[inp.phone] || {};\n'
            'if (state.mode === "editing") {\n'
            '  return [{json: {...inp, mode: "editing", entry_id: state.entry_id,\n'
            '    volunteer_name: state.volunteer_name, old_remoteJid: state.remoteJid}}];\n'
            '}\n'
            'return [{json: {...inp, mode: "new"}}];'
        )
    }
}
nodes.append(preveri_nacin)

# ── 4b. Add Switch: Je v urejanju? (routes edit vs new text) ──
switch_urejanje = {
    "id": "switch_je_v_urejanju",
    "name": "Je v urejanju?",
    "type": "n8n-nodes-base.switch",
    "typeVersion": 3.2,
    "position": [1540, 300],
    "parameters": {
        "mode": "rules",
        "rules": {
            "values": [
                {
                    "conditions": {
                        "options": {
                            "caseSensitive": True,
                            "leftValue": "",
                            "typeValidation": "strict"
                        },
                        "combinator": "and",
                        "conditions": [
                            {
                                "id": "edt1",
                                "leftValue": "={{ $json.mode }}",
                                "rightValue": "editing",
                                "operator": {
                                    "type": "string",
                                    "operation": "equals",
                                    "name": "filter.operator.equals"
                                }
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "Urejanje"
                },
                {
                    "conditions": {
                        "options": {
                            "caseSensitive": True,
                            "leftValue": "",
                            "typeValidation": "strict"
                        },
                        "combinator": "and",
                        "conditions": [
                            {
                                "id": "edt2",
                                "leftValue": "={{ $json.mode }}",
                                "rightValue": "new",
                                "operator": {
                                    "type": "string",
                                    "operation": "equals",
                                    "name": "filter.operator.equals"
                                }
                            }
                        ]
                    },
                    "renameOutput": True,
                    "outputKey": "Novo Besedilo"
                }
            ]
        },
        "options": {}
    }
}
nodes.append(switch_urejanje)

# ── 5. Add Code: Procesiraj Popravek (parse corrected text) ──
# Same extraction logic as Text Extract, plus carries forward edit metadata
procesiraj = {
    "id": "code_procesiraj_popravek",
    "name": "Code: Procesiraj Popravek",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1800, 300],
    "parameters": {
        "jsCode": (
            'function parseHours(text) {\n'
            '  const numM = text.match(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/i);\n'
            '  if (numM) return parseFloat(numM[1].replace(",", "."));\n'
            '  const words = {\n'
            '    "ena": 1, "eno": 1, "eni": 1, "dve": 2, "dva": 2, "dveh": 2,\n'
            '    "tri": 3, "treh": 3, "štiri": 4, "štirih": 4, "pet": 5, "petih": 5,\n'
            '    "šest": 6, "šestih": 6, "sedem": 7, "sedmih": 7, "osem": 8, "osmih": 8,\n'
            '    "devet": 9, "devetih": 9, "deset": 10, "desetih": 10,\n'
            '    "enajst": 11, "enajstih": 11, "dvanajst": 12, "dvanajstih": 12,\n'
            '    "trinajst": 13, "štirinajst": 14, "petnajst": 15, "šestnajst": 16,\n'
            '    "sedemnajst": 17, "osemnajst": 18, "devetnajst": 19, "dvajset": 20,\n'
            '    "enaindvajset": 21, "dvaindvajset": 22, "triindvajset": 23,\n'
            '  };\n'
            '  const tl = text.toLowerCase();\n'
            '  const wordM = tl.match(/(\\w+)\\s*ur/i);\n'
            '  if (wordM && words[wordM[1]] !== undefined) return words[wordM[1]];\n'
            '  return 1.0;\n'
            '}\n'
            'function extractLocation(text) {\n'
            '  const locKraj = text.match(/\\bkraj\\s*[,;:]?\\s*([A-Za-zŠŽČĆĐšžčćđ][^\\.,!?\\n]{0,50})/i);\n'
            '  if (locKraj) return locKraj[1].trim().replace(/\\s*(?:uro|uri|ure|ur\\b).*/i, "").trim();\n'
            '  const locM = text.match(/\\b(?:v|pri|na)\\s+([A-ZŠŽČĆĐ][a-zšžčćđ]+(?:\\s+[A-ZŠŽČĆĐ][a-zšžčćđ]+)*)/);\n'
            '  return locM ? locM[1] : null;\n'
            '}\n'
            'function extractDate(text) {\n'
            '  const today = new Date();\n'
            '  let entryDate = new Date(today);\n'
            '  const tl = text.toLowerCase();\n'
            '  if (tl.includes("včeraj") || tl.includes("vceraj")) {\n'
            '    entryDate.setDate(today.getDate() - 1);\n'
            '  } else {\n'
            '    const days = [{n:"ponedeljek",d:1},{n:"torku",d:2},{n:"torek",d:2},{n:"sredo",d:3},{n:"sredi",d:3},{n:"četrtek",d:4},{n:"cetrtek",d:4},{n:"petek",d:5},{n:"soboto",d:6},{n:"nedeljo",d:0}];\n'
            '    for (const {n, d} of days) {\n'
            '      if (tl.includes(n)) { const diff = ((today.getDay()-d)+7)%7||7; entryDate=new Date(today); entryDate.setDate(today.getDate()-diff); break; }\n'
            '    }\n'
            '    const dm = text.match(/\\b(\\d{1,2})[.\\s]+(\\d{1,2})\\. /);\n'
            '    if (dm) entryDate = new Date(today.getFullYear(), parseInt(dm[2])-1, parseInt(dm[1]));\n'
            '  }\n'
            '  return entryDate.toISOString().split("T")[0];\n'
            '}\n'
            'const inp = $input.first().json;\n'
            'const phone = inp.phone;\n'
            'const remoteJid = inp.old_remoteJid || inp.remoteJid;\n'
            'const text = inp.text || "";\n'
            'const hours = parseHours(text);\n'
            'const location = extractLocation(text);\n'
            'const entry_date = extractDate(text);\n'
            'let activity = text.replace(/(\\d+(?:[.,]\\d+)?)\\s*(?:uro|uri|ure|ur\\b)/gi,"")\n'
            '  .replace(/\\b(danes|včeraj|vceraj|ponedeljek|torek|torku|sredo|sredi|četrtek|cetrtek|petek|soboto|nedeljo)\\b/gi,"")\n'
            '  .replace(/\\s{2,}/g," ").trim() || text.trim();\n'
            'return [{json: {phone, remoteJid, entry_id: inp.entry_id, entry_date, hours, activity_description: activity, location, volunteer_name: inp.volunteer_name, raw_transcript: null}}];'
        )
    }
}
nodes.append(procesiraj)

# ── 6. Add HTTP: Brisi Stari Vnos (DELETE old entry) ──
brisi_stari = {
    "id": "http_brisi_stari_vnos",
    "name": "HTTP: Brisi Stari Vnos",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [2060, 300],
    "parameters": {
        "method": "DELETE",
        "url": "=http://api:8000/api/log-entries/{{ $json.entry_id }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "options": {}
    },
    "credentials": {
        "httpBasicAuth": {
            "id": "UqZlwzClZfiYKanN",
            "name": "BelPro API (Basic Auth)"
        }
    }
}
nodes.append(brisi_stari)

# ── 7. Add Code: Shrani Stanje Popravek (update state + build confirmation) ──
shrani_popravek = {
    "id": "code_shrani_popravek",
    "name": "Code: Shrani Stanje Popravek",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [2580, 300],
    "parameters": {
        "jsCode": (
            'const entryResp = $input.first().json;\n'
            'const up = $("Code: Procesiraj Popravek").first().json;\n'
            'const phone = up.phone;\n'
            'const remoteJid = up.remoteJid;\n'
            'const entry_id = entryResp.id;\n'
            'const sd = $getWorkflowStaticData("global");\n'
            'sd[phone] = {\n'
            '  entry_id,\n'
            '  volunteer_id: up.volunteer_id,\n'
            '  entry_date: up.entry_date,\n'
            '  hours: up.hours,\n'
            '  activity_description: up.activity_description,\n'
            '  location: up.location,\n'
            '  volunteer_name: up.volunteer_name,\n'
            '  remoteJid\n'
            '};\n'
            'const d = up.entry_date ? new Date(up.entry_date) : new Date();\n'
            'const dateStr = d.toLocaleDateString("sl-SI", {day:"2-digit",month:"2-digit",year:"numeric"});\n'
            'const locStr = up.location ? " v " + up.location : "";\n'
            'const msg = "Zabeležili smo vaš vnos:\\n📅 " + dateStr + "\\n⏱ " + up.hours + " ur\\n📍" + locStr + "\\n📝 " + up.activity_description + "\\n\\nAli je vse pravilno?\\n1 - Potrdi\\n2 - Popravi\\n3 - Prekliči";\n'
            'return [{json: {phone, remoteJid, text: msg}}];'
        )
    }
}
nodes.append(shrani_popravek)

# ── 8. Add HTTP: WA Potrditev Popravek (send confirmation) ──
wa_potrditev_popravek = {
    "id": "http_wa_potrditev_popravek",
    "name": "HTTP: WA Potrditev Popravek",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [2840, 300],
    "parameters": {
        "method": "POST",
        "url": "http://evolution-api:8080/message/sendText/belpro",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": True,
        "contentType": "json",
        "bodyParameters": {
            "parameters": [
                {"name": "number", "value": "={{ $json.remoteJid }}"},
                {"name": "text", "value": "={{ $json.text }}"}
            ]
        },
        "options": {}
    },
    "credentials": {
        "httpHeaderAuth": {
            "id": "QXGVac2NwnJcQf9V",
            "name": "BelPro Evolution API"
        }
    }
}
nodes.append(wa_potrditev_popravek)

# ── 9. Update connections ──
# Remove old connections for removed nodes
for key in list(conns.keys()):
    if key in ("HTTP: Brisi Popravi", "Code: Clear State Popravi"):
        del conns[key]

# Remove connections TO removed nodes
for src, outputs in conns.items():
    for out_list in outputs.get("main", []):
        out_list[:] = [c for c in out_list if c["node"] not in ("HTTP: Brisi Popravi", "Code: Clear State Popravi")]

# Vrsta Odziva[1] (Popravi) → Code: Pripravi Popravek (instead of HTTP: Brisi Popravi)
# Vrsta Odziva[1] already points to Code: Pripravi Popravek via the rename below... actually no.
# Vrsta Odziva outputs: [0]=Potrdi, [1]=Popravi, [2]=Preklici
# Output [1] needs to go to Code: Pripravi Popravek
conns["Vrsta Odziva"]["main"][1] = [{"node": "Code: Pripravi Popravek", "type": "main", "index": 0}]

# Code: Pripravi Popravek → HTTP: WA Popravi
conns["Code: Pripravi Popravek"] = {
    "main": [[{"node": "HTTP: WA Popravi", "type": "main", "index": 0}]]
}

# Razpotje[1] (Besedilo) → Code: Preveri Nacin (instead of Text Extract)
conns["Razpotje"]["main"][1] = [{"node": "Code: Preveri Nacin", "type": "main", "index": 0}]

# Code: Preveri Nacin → Je v urejanju?
conns["Code: Preveri Nacin"] = {
    "main": [[{"node": "Je v urejanju?", "type": "main", "index": 0}]]
}

# Je v urejanju?[0] (Urejanje) → Code: Procesiraj Popravek
# Je v urejanju?[1] (Novo Besedilo) → Text Extract
conns["Je v urejanju?"] = {
    "main": [
        [{"node": "Code: Procesiraj Popravek", "type": "main", "index": 0}],
        [{"node": "Text Extract", "type": "main", "index": 0}]
    ]
}

# Code: Procesiraj Popravek → HTTP: Brisi Stari Vnos
conns["Code: Procesiraj Popravek"] = {
    "main": [[{"node": "HTTP: Brisi Stari Vnos", "type": "main", "index": 0}]]
}

# HTTP: Brisi Stari Vnos → HTTP: Ustvari Nov Vnos (dedicated for edit path)
conns["HTTP: Brisi Stari Vnos"] = {
    "main": [[{"node": "HTTP: Ustvari Nov Vnos", "type": "main", "index": 0}]]
}

# HTTP: Ustvari Vnos already connects to Code: Shrani Stanje → HTTP: WA Potrditev
# BUT in the edit path we need: HTTP: Ustvari Vnos → Code: Shrani Stanje Popravek → HTTP: WA Potrditev Popravek
# Since HTTP: Ustvari Vnos already has an outgoing connection to Code: Shrani Stanje,
# we need to be careful. The edit path and new-entry path converge at HTTP: Ustvari Vnos.
#
# Actually, both paths can share HTTP: Ustvari Vnos but then diverge:
# - New entry: Ustvari Vnos → Shrani Stanje → WA Potrditev
# - Edit: Ustvari Vnos → Shrani Stanje Popravek → WA Potrditev Popravek
#
# Since n8n nodes can only have one set of outgoing connections, we can't have Ustvari Vnos
# connect to both Shrani Stanje AND Shrani Stanje Popravek based on context.
#
# Solution: Create a separate HTTP node for creating the entry in the edit path.

# Replace the shared approach with a dedicated HTTP node for edit path
# HTTP: Brisi Stari Vnos → HTTP: Ustvari Nov Vnos (new, dedicated for edit path)
ustvari_nov = {
    "id": "http_ustvari_nov_vnos",
    "name": "HTTP: Ustvari Nov Vnos",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [2320, 300],
    "parameters": {
        "method": "POST",
        "url": "http://api:8000/api/log-entries",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "options": {},
        "sendBody": True,
        "contentType": "json",
        "bodyParameters": {
            "parameters": [
                {"name": "volunteer_id", "value": "={{ $json.volunteer_id }}"},
                {"name": "entry_date", "value": "={{ $json.entry_date }}"},
                {"name": "activity_description", "value": "={{ $json.activity_description }}"},
                {"name": "hours", "value": "={{ $json.hours }}"},
                {"name": "location", "value": "={{ $json.location }}"},
                {"name": "raw_transcript", "value": "={{ $json.raw_transcript }}"},
                {"name": "status", "value": "pending_volunteer"}
            ]
        }
    },
    "credentials": {
        "httpBasicAuth": {
            "id": "UqZlwzClZfiYKanN",
            "name": "BelPro API (Basic Auth)"
        }
    }
}
nodes.append(ustvari_nov)

# Update HTTP: Brisi Stari Vnos connection to go to HTTP: Ustvari Nov Vnos instead
conns["HTTP: Brisi Stari Vnos"]["main"] = [[{"node": "HTTP: Ustvari Nov Vnos", "type": "main", "index": 0}]]

# HTTP: Ustvari Nov Vnos → Code: Shrani Stanje Popravek
conns["HTTP: Ustvari Nov Vnos"] = {
    "main": [[{"node": "Code: Shrani Stanje Popravek", "type": "main", "index": 0}]]
}

# Code: Shrani Stanje Popravek → HTTP: WA Potrditev Popravek
conns["Code: Shrani Stanje Popravek"] = {
    "main": [[{"node": "HTTP: WA Potrditev Popravek", "type": "main", "index": 0}]]
}

# But wait - Procesiraj Popravek doesn't output volunteer_id.
# We need to either:
# a) Store volunteer_id in static data (modify Shrani Stanje)
# b) Look up volunteer in Procesiraj Popravek
#
# Let's modify Shrani Stanje to also store volunteer_id. And add volunteer_id to Procesiraj Popravek.
# Actually, Procesiraj Popravek reads from static data, but it doesn't have volunteer_id.
# Let's also store volunteer_id in static data.

# Modify Code: Shrani Stanje to also store volunteer_id
for n in nodes:
    if n["id"] == "code_shrani_stanje":
        js = n["parameters"]["jsCode"]
        # Add volunteer_id to sd[phone] object
        js = js.replace(
            '"sd[phone] = {\\n  entry_id,\\n"',
            '"sd[phone] = {\\n  entry_id,\\n  volunteer_id: up.volunteer_id,\\n"'
        )
        n["parameters"]["jsCode"] = js
        break

# And update Code: Procesiraj Popravek to pass volunteer_id from state
for n in nodes:
    if n["id"] == "code_procesiraj_popravek":
        js = n["parameters"]["jsCode"]
        # Add volunteer_id to the returned object
        js = js.replace(
            '"return [{json: {phone, remoteJid, entry_id: inp.entry_id,"',
            '"const sd2 = $getWorkflowStaticData("global");\nconst st2 = sd2[phone] || {};\nreturn [{json: {phone, remoteJid, entry_id: inp.entry_id, volunteer_id: st2.volunteer_id,"'
        )
        n["parameters"]["jsCode"] = js
        break

# Also update Nalozi Stanje to include volunteer_id in its output
for n in nodes:
    if n["id"] == "loadstate11":
        js = n["parameters"]["jsCode"]
        js = js.replace(
            '"volunteer_name: state.volunteer_name\n"',
            '"volunteer_name: state.volunteer_name,\n  volunteer_id: state.volunteer_id\n"'
        )
        n["parameters"]["jsCode"] = js
        break

# ── 10. Verify ──
errors = []
node_names = {n["name"] for n in nodes}
node_ids = {n["id"] for n in nodes}

# Check required nodes exist
required = [
    "Code: Pripravi Popravek", "Code: Preveri Nacin", "Je v urejanju?",
    "Code: Procesiraj Popravek", "HTTP: Brisi Stari Vnos", "HTTP: Ustvari Nov Vnos",
    "Code: Shrani Stanje Popravek", "HTTP: WA Potrditev Popravek"
]
for name in required:
    if name not in node_names:
        errors.append(f"Missing node: {name}")

# Check removed nodes are gone
for name in ["HTTP: Brisi Popravi", "Code: Clear State Popravi"]:
    if name in node_names:
        errors.append(f"Should have been removed: {name}")

# Check all connection targets exist
for src, outputs in conns.items():
    if src not in node_names:
        errors.append(f"Connection source does not exist: {src}")
    for i, out_list in enumerate(outputs.get("main", [])):
        for conn in out_list:
            if isinstance(conn, dict) and "node" in conn:
                if conn["node"] not in node_names:
                    errors.append(f"Connection target '{conn['node']}' (from {src}[{i}]) does not exist")

# Check all nodes have connections (unless they're terminal)
terminal_nodes = {
    "HTTP: WA Ni Registriran", "HTTP: WA Popravi", "HTTP: WA Preklici",
    "HTTP: WA Potrditev", "HTTP: WA Potrjeno", "HTTP: WA Upravljalcu",
    "HTTP: WA Potrditev Popravek", "HTTP: WA Ni Aktivnega Vnosa",
    "Sticky Note"
}
for name in node_names:
    if name in terminal_nodes:
        continue
    found_as_source = name in conns
    found_as_target = any(
        any((isinstance(c, dict) and c.get("node") == name) for c in out_list)
        for outputs in conns.values()
        for out_list in outputs.get("main", [])
    )
    if not found_as_target and name != "Webhook: WhatsApp":
        errors.append(f"Node '{name}' is not a connection target (orphan input)")
    if not found_as_source and name not in terminal_nodes:
        errors.append(f"Node '{name}' has no outgoing connections (orphan output)")

if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  {e}")
else:
    print("All checks passed.")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("File saved.")
