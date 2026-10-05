#!/usr/bin/env python3
"""Focused schema/narrative field checks. Not runtime tests or full 065 validation."""
from pathlib import Path
import copy, json, re, sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker
P=Path(__file__).resolve().parents[1]/'SmartCore_Platform_Docs_v1'/'Identity'
a=yaml.safe_load((P/'openapi.yaml').read_text());e=json.loads((P/'events.schema.json').read_text());s=json.loads((P/'services.schema.json').read_text())
results=[]
uid='7aad209e-11f0-4ad0-9415-f4854a8e6904';time='2026-09-24T10:00:00Z'
def resolve(doc,ref):
 for k in ref.removeprefix('#/').split('/'):doc=doc[k.replace('~1','/').replace('~0','~')]
 return doc
def sample(v,doc):
 if '$ref' in v:return sample(resolve(doc,v['$ref']),doc)
 if 'const' in v:return v['const']
 if 'enum' in v:return v['enum'][0]
 if v.get('type')=='object':
  value={k:sample(v['properties'][k],doc) for k in v.get('required',[])}
  if {'email','mobile'} <= set(v.get('properties',{})):value['mobile']='+12025550123'
  return value
 if 'oneOf' in v:return sample(v['oneOf'][0],doc)
 if v.get('type')=='array':return []
 if v.get('type')=='integer':return max(1,v.get('minimum',1))
 if v.get('type')=='boolean':return True
 if v.get('format')=='uuid':return uid
 if v.get('format')=='date-time':return time
 if v.get('format')=='email':return 'person@example.test'
 pat=v.get('pattern','')
 if pat==r'^[0-9]{6}$':return '123456'
 if pat==r'^[A-Za-z0-9_-]{43}$':return 'x'*43
 if pat.startswith('^\\+'):return '+12025550123'
 return 'x'*max(1,v.get('minLength',1))
def valid(doc,ref,value):
 schema=dict(doc);schema['$ref']=ref
 return Draft202012Validator(schema,format_checker=FormatChecker()).is_valid(value)
def check(label,ok):results.append({'check':label,'pass':bool(ok)})
for doc,path in [(a,'/components/schemas/'),(s,'/$defs/'),(e,'/$defs/')]:
 defs=resolve(doc,'#'+path[:-1])
 for name,v in defs.items():
  x=sample(v,doc)
  # Supply conditional required fields for the chosen synthetic branch.
  if name=='StartRegistration' or name=='Login' or name=='Person':x['mobile']='+12025550123'
  if name=='RecoveryCompleted':x['cleanupState']='Pending'
  if name=='LoginFailed':x.pop('ActorIdentity',None);x.pop('AggregateId',None)
  if name in e['$defs'] and doc is e and x.get('ActorIdentity')!='System':x['ExecutionContext']={'CorrelationId':'test-correlation'}
  ref='#'+path+name
  check(name+' synthetic positive shape',valid(doc,ref,x))
  if isinstance(x,dict):
   bad=dict(x,__unknown=True);check(name+' rejects unknown root field',not valid(doc,ref,bad))
   for k in x:
    bad=copy.deepcopy(x);bad[k]=None;check(name+' rejects null '+k,not valid(doc,ref,bad))
start={'mobile':'+12025550123','password':'example-long-password','displayName':'Example','bindingSecret':'x'*43}
for label,mutation,want in [('email only',dict(start,email='person@example.test'),False),('no contact',{k:v for k,v in start.items() if k!='mobile'},False),('blank name',dict(start,displayName=' \t\n'),False),('nonblank padded name',dict(start,displayName=' Example '),True)]:check('StartRegistration '+label,valid(a,'#/components/schemas/StartRegistration',mutation)==want)
email=dict(start,email='person@example.test');email.pop('mobile');check('StartRegistration true email-only',valid(a,'#/components/schemas/StartRegistration',email))
for n in ('StartRegistration','Person','UpdateProfile'):check(n+' declares nonblank DisplayName',a['components']['schemas'][n]['properties']['displayName'].get('pattern')==r'\S')
for path,methods in a['paths'].items():
 for method,op in methods.items():
  for code,response in op['responses'].items():check(method+' '+path+' '+code+' no-store',response.get('headers',{}).get('Cache-Control',{}).get('schema',{}).get('const')=='no-store')
# Compare each event's payload field names/requiredness to its narrative table.
text=(P/'06_Domain_Events.md').read_text()
for name,v in e['$defs'].items():
 block=re.search(r'^## 4\.\d+ '+name+r'\n(.*?)(?=^## 4\.\d+ |^# 5\.|\Z)',text,re.M|re.S).group(1).split('### Payload',1)[1]
 cells=[list(map(str.strip,re.split(r'(?<!\\)\|',l.strip('|')))) for l in block.splitlines() if l.startswith('|')]
 cells=[c for c in cells if len(c)==3 and c[0] not in ('Field','---')]
 payload=v['properties']['Payload']
 check(name+' payload field names match 06 table',{c[0] for c in cells}==set(payload['properties']))
 check(name+' payload requiredness matches 06 table',{c[0] for c in cells if c[2].startswith('Required')}==set(payload['required']))
# Show the deliberate limits of shape validation: mismatched bindings still pass.
req=sample(s['$defs']['EnsureInitialCredentialRequest'],s);req['materialOwner']='96f710c5-e04b-4670-9446-6be075393b23'
check('documented limit: unequal materialOwner accepted by schema',valid(s,'#/$defs/EnsureInitialCredentialRequest',req))
summary={'checks':len(results),'passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results)}
output={'summary':summary,'results':results,'not_checked':['Runtime, authentication/authorization, normalization, crypto, expiry, transaction/crash/concurrency, deployed consumers, full 065 validation','Cross-field identity/time equality, T16 transport positions, SESSION policy, V-002/V-003 governance dispositions','Synthetic positive per definition is not exhaustive conditional/union coverage']}
if '--json' in sys.argv:print(json.dumps(output,indent=2))
else:
 print(summary)
 for x in results:
  if not x['pass']:print('FAIL',x['check'])
sys.exit(1 if summary['failed'] else 0)
