"""Fix Code: Clear State Popravi and Preklici to read from Nalozi Stanje instead of $input."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = 'd:/Andrej/vsCode-workspace/BelPro/n8n/workflows/volunteer_entry.json'
with open(PATH, 'r', encoding='utf-8') as f:
    wf = json.load(f)

nodes = {n['name']: n for n in wf['nodes']}

new_code = (
    'const st = $("Nalozi Stanje").first().json;\n'
    'const phone = st.phone;\n'
    'const remoteJid = st.remoteJid;\n'
    'const sd = $getWorkflowStaticData("global");\n'
    'delete sd[phone];\n'
    'return [{json: {phone, remoteJid}}];'
)

for name in ['Code: Clear State Popravi', 'Code: Clear State Preklici']:
    if name in nodes:
        nodes[name]['parameters']['jsCode'] = new_code
        print(f'  Fixed: {name}')
    else:
        print(f'  NOT FOUND: {name}')
        for n in sorted(nodes):
            if 'clear' in n.lower() and 'state' in n.lower():
                print(f'    similar: [{n}]')

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print('File saved.')
