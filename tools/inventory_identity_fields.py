#!/usr/bin/env python3
"""Write literal field inventories; these are review evidence, never full validation PASS."""
from pathlib import Path
import yaml,json,re,hashlib
r=Path(__file__).resolve().parents[1];p=r/'SmartCore_Platform_Docs_v1/Identity';o=yaml.safe_load((p/'openapi.yaml').read_text());s=json.loads((p/'services.schema.json').read_text());e=json.loads((p/'events.schema.json').read_text());m=yaml.safe_load((p/'capability.machine.yaml').read_text());rows=[]
keys=('type','format','enum','const','pattern','minLength','maxLength','minimum','maximum','writeOnly','readOnly','additionalProperties')
def walk(v,source,path=''):
 if isinstance(v,dict):
  if 'properties' in v:
   for k,a in v['properties'].items():
    rows.append({'source':source,'pointer':path+'/properties/'+k,'field':k,'requiredInLocalObject':k in v.get('required',[]),'constraints':{z:a[z] for z in keys if z in a},'conditionalContext':any('/'+z+'/' in path for z in ('oneOf','allOf','anyOf','then','else','if'))})
  for k,a in v.items():walk(a,source,path+'/'+k)
 elif isinstance(v,list):
  for i,a in enumerate(v):walk(a,source,path+'/'+str(i))
for f,v in [('openapi.yaml',o),('services.schema.json',s),('events.schema.json',e),('capability.machine.yaml',m)]:walk(v,f)
x={'platformInput':'add04692a155fc05dfbbb3008326b923bab9b25c','identityInput':'ee9ffb767ed84165557793d8583b0750d887027b','snapshot':'working tree; identify revision by containing commit and artifact hashes','method':'Every explicit JSON Schema properties occurrence, including nested conditional branches. Local required flags do not resolve inherited/composed requiredness. Machine semantic entries are separately captured; not an equivalence PASS.','fields':rows,'machine':{'aggregates':m['aggregates'],'commands':m['commands'],'queries':m['queries'],'events':m['events'],'contracts':m['contracts']},'artifactHashes':{f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ('openapi.yaml','services.schema.json','events.schema.json','capability.machine.yaml')}}
(r/'_Copilot_Reports/Identity_Field_Inventory.json').write_text(json.dumps(x,indent=2)+'\n')
# Exact envelope/payload names and requiredness against the tables in 06.
t=(p/'06_Domain_Events.md').read_text();out=[]
for name,v in e['$defs'].items():
 block=re.search(r'^## 4\.\d+ '+name+r'\n(.*?)(?=^## 4\.\d+ |^# 5\.|\Z)',t,re.M|re.S).group(1)
 payload=block.split('### Payload',1)[1]
 cols=[]
 for line in payload.splitlines():
  if not line.startswith('|'):continue
  cells=[c.strip() for c in re.split(r'(?<!\\)\|', line.strip('|'))]
  if len(cells)==3 and cells[0] not in ('Field','---'):cols.append(cells)
 actual=v['properties']['Payload'];expected={c[0] for c in cols}
 out.append({'event':name,'narrativePayloadFields':sorted(expected),'schemaPayloadFields':sorted(actual['properties']),'fieldNamesEqual':expected==set(actual['properties']),'narrativeRequired':sorted(c[0] for c in cols if c[2].startswith('Required')),'schemaRequired':sorted(actual['required']),'requiredEqual':set(c[0] for c in cols if c[2].startswith('Required'))==set(actual['required'])})
(r/'_Copilot_Reports/Identity_Event_Payload_Comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print('field occurrences',len(rows),'definitions',len(o['components']['schemas']),len(s['$defs']),len(e['$defs']),'event payload names/required',all(v['fieldNamesEqual'] and v['requiredEqual'] for v in out))
