"""Rename non-ASCII node names to ASCII and fix all references."""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = "d:/Andrej/vsCode-workspace/BelPro/n8n/workflows/volunteer_entry.json"
with open(PATH, "r", encoding="utf-8") as f:
    wf = json.load(f)

RENAMES = {
    "Naloži Stanje": "Nalozi Stanje",
    "HTTP: Briši Popravi": "HTTP: Brisi Popravi",
    "HTTP: Briši Prekliči": "HTTP: Brisi Preklici",
    "Code: Clear State Prekliči": "Code: Clear State Preklici",
    "HTTP: WA Prekliči": "HTTP: WA Preklici",
}

# 1. Rename nodes
for node in wf["nodes"]:
    if node["name"] in RENAMES:
        old = node["name"]
        node["name"] = RENAMES[old]

# 2. Rename inside connections (recursive walk for target node names)
def rename_in_conn(obj):
    if isinstance(obj, dict):
        if "node" in obj and obj["node"] in RENAMES:
            obj["node"] = RENAMES[obj["node"]]
        for v in obj.values():
            rename_in_conn(v)
    elif isinstance(obj, list):
        for item in obj:
            rename_in_conn(item)

rename_in_conn(wf["connections"])

# Also rename connection source keys
new_connections = {}
for src_name, outputs in wf["connections"].items():
    new_src = RENAMES.get(src_name, src_name)
    new_connections[new_src] = outputs
wf["connections"] = new_connections

# 3. Update JS code $() references
for node in wf["nodes"]:
    js = node.get("parameters", {}).get("jsCode", "")
    if not js:
        continue
    for old, new in RENAMES.items():
        js = js.replace('$("' + old + '")', '$("' + new + '")')
        js = js.replace("$('" + old + "')", "$('" + new + "')")
    node["parameters"]["jsCode"] = js

# Verify
errors = []
for name in ["Nalozi Stanje", "HTTP: Brisi Popravi", "HTTP: Brisi Preklici",
             "Code: Clear State Preklici", "HTTP: WA Preklici"]:
    found_in_nodes = any(n["name"] == name for n in wf["nodes"])
    if not found_in_nodes:
        errors.append(f"Node missing: {name}")

# Check all connection targets exist
node_names = {n["name"] for n in wf["nodes"]}
for src, outputs in wf["connections"].items():
    for out_list in outputs.get("main", []):
        for conn in out_list:
            if conn["node"] not in node_names:
                errors.append(f"Connection target {conn['node']} (from {src}) does not exist")

if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  {e}")
else:
    print("All checks passed.")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("File saved.")
