#!/usr/bin/env python3
"""Isolated detector controls; use the same installed dependencies as the checker."""
import tempfile,shutil,subprocess,os,json,sys
from pathlib import Path
src=Path(__file__).resolve().parent.parent; cases=[]
for label,mode in [('missing-heading','heading'),('broken-dependency','dependency'),('broken-schema-pointer','pointer'),('duplicate-command','duplicate')]:
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);shutil.copytree(src/'tools',p/'tools');shutil.copytree(src/'SmartCore_Platform_Docs_v1',p/'SmartCore_Platform_Docs_v1');shutil.copytree(src/'_Copilot_Reports',p/'_Copilot_Reports');d=p/'SmartCore_Platform_Docs_v1/Identity'
  if mode=='heading':
   f=d/'05_Queries.md';f.write_text('\n'.join(l for l in f.read_text().splitlines() if not l.startswith('#')))
  elif mode=='dependency':
   f=d/'05_Queries.md';f.write_text(f.read_text().replace('064_SmartCore_Blueprint_Standard','064_MISSING_STANDARD'))
  elif mode=='pointer':
   f=d/'capability.machine.yaml';f.write_text(f.read_text().replace('events.schema.json#/$defs/PersonRegistered','events.schema.json#/$defs/MISSING_EVENT'))
  else:
   f=d/'capability.machine.yaml';f.write_text(f.read_text().replace('- name: RefreshSession','- name: LogoutSession'))
  env=dict(os.environ);cp=subprocess.run([sys.executable,str(p/'tools/slice0_structural_065.py'),'--json'],env=env,capture_output=True,text=True)
  x=json.loads(cp.stdout);fail=[r for r in x['results'] if r[1]=='FAIL'];assert cp.returncode==1 and fail and not cp.stderr,(label,cp.returncode,cp.stderr)
  cases.append({'case':label,'exit':cp.returncode,'fails':fail})
print(json.dumps(cases,indent=2))
