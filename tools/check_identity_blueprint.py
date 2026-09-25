#!/usr/bin/env python3
"""Limited, reproducible documentation checks; NOT the full 065 validator.
Requires Python 3.10+ and PyYAML. No network, runtime implementation or secrets.
"""
from pathlib import Path
import copy,json,re,sys,uuid,datetime
import yaml
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'SmartCore_Platform_Docs_v1'/'Identity'
checks=[]
def check(ok,label):
    checks.append((bool(ok),label))
    if not ok: print('FAIL:',label)
def pointer(doc,path):
    for bit in path.removeprefix('#/').split('/'):
        doc=doc[bit.replace('~1','/').replace('~0','~')]
    return doc

def fixture_matches(value,schema,doc):
    """Fixture helper for constructs in these schemas, NOT general JSON Schema validation."""
    if '$ref' in schema:return fixture_matches(value,pointer(doc,schema['$ref']),doc)
    def match(s):return fixture_matches(value,s,doc)
    if 'const' in schema and value!=schema['const']:return False
    if 'enum' in schema and value not in schema['enum']:return False
    if 'allOf' in schema and not all(map(match,schema['allOf'])):return False
    if 'anyOf' in schema and not any(map(match,schema['anyOf'])):return False
    if 'oneOf' in schema and sum(map(match,schema['oneOf']))!=1:return False
    if 'not' in schema and match(schema['not']):return False
    if 'if' in schema and not match(schema.get('then' if match(schema['if']) else 'else',{})):return False
    types={'object':dict,'array':list,'string':str,'integer':int,'boolean':bool}
    if 'type' in schema and not isinstance(value,types[schema['type']]):return False
    if isinstance(value,dict):
        if any(k not in value for k in schema.get('required',[])):return False
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False and set(value)-set(props):return False
        if any(not fixture_matches(v,props[k],doc) for k,v in value.items() if k in props):return False
    if isinstance(value,list) and 'items' in schema and not all(fixture_matches(v,schema['items'],doc) for v in value):return False
    if isinstance(value,str):
        if schema.get('format')=='uuid':
            try: uuid.UUID(value)
            except ValueError: return False
        if schema.get('format')=='date-time':
            try:
                dt=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
                if dt.tzinfo is None:return False
            except ValueError:return False
        if len(value)<schema.get('minLength',0) or len(value)>schema.get('maxLength',float('inf')):return False
        if 'pattern' in schema and re.search(schema['pattern'],value) is None:return False
    return True

m=yaml.safe_load((P/'capability.machine.yaml').read_text())
a=yaml.safe_load((P/'openapi.yaml').read_text())
e=json.loads((P/'events.schema.json').read_text())
expected=['00_Overview','01_Domain_Model','02_Use_Cases','03_Aggregates','04_Commands','05_Queries','06_Domain_Events','07_Contracts','08_API','09_Persistence','10_Configuration','11_Security','12_Validation','13_Testing','14_MVP','15_Extensibility','16_Examples']
manifest={x['path']:x for x in m['documents']}
for name in expected:
    f=P/(name+'.md');check(f.exists(),name+' exists')
    s=f.read_text();header=s.split('-->',1)[0]
    check(header.startswith('<!--') and all(k+':' in header for k in ['Document ID','Title','Version','Status','Purpose','Dependencies','Change Log']),name+' metadata')
    check(re.search(r'^Status: DRAFT$',header,re.M) is not None,name+' DRAFT')
    check(manifest[f.name]['version']==re.search(r'^Version: (.+)$',header,re.M)[1],name+' version manifest')
    check(s.count('```')%2==0,name+' closed fences')
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',s):
        if '://' not in target and not target.startswith('#'):
            check((f.parent/target.split('#')[0]).exists(),name+' link '+target)
commands={x['name'] for x in m['commands']};queries={x['name'] for x in m['queries']}
check(len(commands)==6 and len(queries)==5,'six Commands and five Queries')
check(len(m['aggregates'])==5,'five Aggregates')
check(set(e['$defs'])=={x['name'] for x in m['events']} and len(e['$defs'])==10,'ten schemas match event manifest')
check(sum(x['classification']=='SecurityEvent' for x in m['events'])==1 and next(x for x in m['events'] if x['name']=='LoginFailed')['classification']=='SecurityEvent','LoginFailed alone classified SecurityEvent')
check({x['name'] for x in m['events'] if x['stream']=='PersonRegistrationProfile'}=={'PersonRegistered','PersonUpdated'},'stream excludes audit/auth events')
ops={o['operationId']:o for methods in a['paths'].values() for o in methods.values()}
check(len(ops)==14,'14 REST protocol operations')
check({o['x-business-operation'] for o in ops.values()}==commands|(queries-{'GetPersonById'}),'REST business coverage')
for c in m['commands']:
    check(set(c['operations'])=={k for k,v in ops.items() if v['x-business-operation']==c['name']},c['name']+' operation mapping')
service=json.loads((P/'services.schema.json').read_text())
for doc,label in [(a,'OpenAPI'),(e,'events'),(service,'services')]:
    def walk(x):
        if isinstance(x,dict):
            if '$ref' in x:
                try:pointer(doc,x['$ref']);ok=True
                except (KeyError,TypeError):ok=False
                check(ok,label+' reference '+x['$ref'])
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(doc)
for methodpath in [(method.upper(),path) for path,v in a['paths'].items() for method in v]:
    check(' '.join(methodpath) in (P/'08_API.md').read_text(),'narrative route '+' '.join(methodpath))
for contract in m['contracts']['services']:
    for target in contract['schemas']:
        file,fragment=target.split('#',1)
        try:pointer(json.loads((P/file).read_text()),'#'+fragment);valid=True
        except (KeyError,FileNotFoundError):valid=False
        check(valid,'service schema '+target)
for name,c in m['configuration'].items():
    check(re.search(r'\| '+name+r' \| '+str(c['default'])+r' \|',(P/'10_Configuration.md').read_text()) is not None,'config '+name)
# Positive/negative contact, proof, readiness and event fixtures.
schemas=a['components']['schemas']
base={'mobile':'+12025550123','password':'example-long-password','displayName':'Example','bindingSecret':'x'*43}
for label,value,valid in [('mobile-only',base,True),('email-only',dict(base,email='person@example.test',**{}) ,False),('both',dict(base,email='person@example.test'),False),('null email',dict(base,email=None),False),('no contact',{k:v for k,v in base.items() if k!='mobile'},False),('weak binding',dict(base,bindingSecret='short'),False)]:
    if label=='email-only':value.pop('mobile');valid=True
    check(fixture_matches(value,schemas['StartRegistration'],a)==valid,'fixture '+label)
check(not fixture_matches({'email':'x@example.test'},schemas['UpdateProfile'],a),'profile rejects contact mutation')
pending={'registrationId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','status':'PendingCredential','ownershipCommittedAt':'2026-09-24T00:00:00Z'}
check(fixture_matches(pending,schemas['RegistrationResult'],a),'pending result without ReadyAt')
check(not fixture_matches(dict(pending,readyAt='later'),schemas['RegistrationResult'],a),'pending rejects ReadyAt')
check(not fixture_matches(dict(pending,status='Ready'),schemas['RegistrationResult'],a),'Ready requires ReadyAt')
event={'EventId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','EventType':'PersonRegistered','AggregateType':'Person','AggregateId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','OccurredAt':'2026-09-24T01:00:00Z','ActorIdentity':'System','Payload':{'PersonId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','DisplayName':'Example','OrganizationId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','MembershipId':'7aad209e-11f0-4ad0-9415-f4854a8e6904','OwnershipCommittedAt':'2026-09-24T00:00:00Z'}}
check(fixture_matches(event,e['$defs']['PersonRegistered'],e),'mobile-only registration event')
check(not fixture_matches(dict(event,SessionReference='7aad209e-11f0-4ad0-9415-f4854a8e6904'),e['$defs']['PersonRegistered'],e),'registration event rejects SessionReference')
bad=copy.deepcopy(event);bad['Payload']['Email']=None
check(not fixture_matches(bad,e['$defs']['PersonRegistered'],e),'registration event rejects Email null')
bad=copy.deepcopy(event);bad['Payload']['Mobile']='+12025550123'
check(not fixture_matches(bad,e['$defs']['PersonRegistered'],e),'registration event excludes Mobile payload')
check(m['governance']['generationAllowed'] is False,'machine generation disabled')
adr=(P.parent/'ADR-0002_Identity_Foundation_Clarifications.md').read_text()
check('**Status**: Proposed' in adr and '**Version**: 1.7' in adr,'ADR remains Proposed v1.7')
# ADR-0004 propagation fixtures: wire constraints only, not runtime guarantees.
d=service['$defs']
def service_fixture(name,value,expected,label):
    check(fixture_matches(value,d[name],service)==expected,'ADR4 fixture '+label)
uid='7aad209e-11f0-4ad0-9415-f4854a8e6904'
winner=dict(registrationId=uid,personId=uid,credentialId=uid,operationIdOfWinner=uid,provisioningVersion='winner-generation-1',status='Active',phase='ProvisionedAwaitingReady')
service_fixture('GetInitialCredentialResultResponse',winner,True,'guarded active evidence')
service_fixture('GetInitialCredentialResultResponse',dict(winner,phase='ReadyAcknowledged'),False,'active evidence cannot be historical')
historical=dict(winner,status='AlreadyCompleted',phase='ReadyAcknowledged',readyFactId=uid)
service_fixture('GetInitialCredentialResultResponse',historical,True,'historical result separately typed')
ack=dict(registrationId=uid,personId=uid,credentialId=uid,provisioningVersion='winner-generation-1',readyFactId=uid)
service_fixture('AcknowledgeRegistrationReadyRequest',ack,True,'bound acknowledgment')
for key in ('readyFactId','provisioningVersion'):
    service_fixture('AcknowledgeRegistrationReadyRequest',{k:v for k,v in ack.items() if k!=key},False,'ack requires '+key)
request=dict(action='ReconcileCommittedRegistration',targetKind='Registration',targetId=uid,reasonCode='STALLED',ticketReference='INC-1234',correlationId=uid,expectedState='PendingCredential',expectedVersion='1',recoveryRequestId='r'*43,admissionPermit='p'*64)
service_fixture('AdminRecoverStalledRegistrationRequest',request,True,'prepared internal recovery')
service_fixture('AdminRecoverStalledRegistrationRequest',dict(request,targetKind='VerificationSession'),False,'reject mismatched action target')
service_fixture('AdminRecoverStalledRegistrationRequest',dict(request,expectedState='AwaitingVerification'),False,'reject mismatched snapshot state')
for key,value in [('force',True),('password','secret'),('readyFactId',uid),('operatorId','admin')]:
    service_fixture('AdminRecoverStalledRegistrationRequest',dict(request,**{key:value}),False,'reject supplied '+key)
ready=dict(pending,status='Ready',readyAt='2026-09-25T00:00:00Z',credentialOutcome='ExistingWinner')
check(fixture_matches(ready,schemas['CompletionResult'],a),'ADR4 completion discloses existing winner')
check(not fixture_matches(dict(ready,credentialOutcome='Undetermined'),schemas['CompletionResult'],a),'ADR4 Ready cannot report undetermined candidate')
check(m['governance']['adr0004']=='Accepted' and m['governance']['adr0002']=='Proposed','scoped architecture acceptance')
check('T16' in m['governance']['openArchitectureItems'],'T16 remains open')
check(m['governance']['adr0004ApprovalCommit']=='16b720c9cb9afdd60769dcad7b2c4d8c1e2e983c','pinned owner approval')
check((P/m['governance']['adr0004ApprovalRecord']).exists(),'owner approval record exists')
for key,setting in m['requiredConfiguration'].items():
    check(setting['default'] is None and key in (P/'10_Configuration.md').read_text(),'unapproved deployment value remains unset '+key)
check((P/'Registration_Recovery_Runbook.md').exists(),'recovery runbook exists')

failed=sum(not ok for ok,_ in checks)
print(f'{len(checks)-failed}/{len(checks)} limited package checks passed.')
print('NOT CHECKED: full JSON Schema/OpenAPI conformance (including all format semantics), complete 065 semantics/governance, deployed consumers, runtime/security behavior, visual rendering.')
sys.exit(bool(failed))
