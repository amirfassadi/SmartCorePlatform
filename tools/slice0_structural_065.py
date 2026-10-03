#!/usr/bin/env python3
"""Slice 0 structural check of the Identity Blueprint package (065 section 5, applicable subset).

Read-only. Reports PASS/FAIL/WARN per check and an explicit NOT CHECKED list.
Usage: python3 tools/slice0_structural_065.py [--json]
Requires: PyYAML, jsonschema, openapi-spec-validator.
"""
import json, re, sys, pathlib, yaml
from jsonschema import Draft202012Validator
from openapi_spec_validator import validate as oas_validate

ROOT = pathlib.Path(__file__).resolve().parent.parent / "SmartCore_Platform_Docs_v1"
ID = ROOT / "Identity"
REQ_MD = ["00_Overview", "01_Domain_Model", "02_Use_Cases", "03_Aggregates", "04_Commands", "05_Queries",
          "06_Domain_Events", "07_Contracts", "08_API", "09_Persistence", "10_Configuration", "11_Security",
          "12_Validation", "13_Testing", "14_MVP", "15_Extensibility", "16_Examples"]
HEADER_FIELDS = ["Document ID", "Title", "Version", "Status", "Purpose", "Dependencies", "Change Log"]
results = []
def rec(cid, level, msg): results.append((cid, level, msg))

# S1 required files (064 section 7)
for n in REQ_MD:
    rec("S1", "PASS" if (ID / f"{n}.md").exists() else "FAIL", f"required file {n}.md")
rec("S1", "PASS" if (ID / "capability.machine.yaml").exists() else "FAIL", "required file capability.machine.yaml")
extra = sorted(p.name for p in ID.iterdir() if p.is_file() and p.stem not in REQ_MD and p.name != "capability.machine.yaml"
               and p.suffix in (".md", ".yaml", ".yml", ".json"))
for e in extra:
    rec("S1x", "WARN", f"non-standard file in package directory (064 section 7 allows working docs only during drafting): {e}")

# S2 header metadata, S3 version/status vs machine spec
try:
    mach = yaml.safe_load((ID / "capability.machine.yaml").read_text(encoding="utf8"))
    if not isinstance(mach, dict): raise ValueError("machine root must be a mapping")
except (OSError, ValueError, yaml.YAMLError) as exc:
    result = {"results": results + [("S3m", "FAIL", str(exc))],
              "not_checked": ["subsequent checks skipped: machine specification unavailable"]}
    print(json.dumps(result, indent=1))
    sys.exit(1)
mdocs = {pathlib.PurePosixPath(d["path"]).stem: d for d in mach.get("documents", [])}
hdr = {}
for n in REQ_MD:
    p = ID / f"{n}.md"
    if not p.exists(): continue
    head = p.read_text(encoding="utf8")[:6000]
    m = re.search(r"<!--(.*?)-->", head, re.S)
    block = m.group(1) if m else ""
    fields = {f: re.search(rf"^{f}:\s*(.*)$", block, re.M) for f in HEADER_FIELDS}
    miss = [f for f, v in fields.items() if not v]
    rec("S2", "PASS" if not miss else "FAIL", f"{n} header fields" + (f" missing {miss}" if miss else ""))
    hdr[n] = {f: (v.group(1).strip() if v else None) for f, v in fields.items()}
    top = re.search(r"^\s*-\s*Version\s+(\d+\.\d+\.\d+)", block, re.M)
    if top and hdr[n]["Version"]:
        rec("S3", "PASS" if top.group(1) == hdr[n]["Version"] else "FAIL",
            f"{n} header Version {hdr[n]['Version']} vs first change-log entry {top.group(1)}")
    else:
        rec("S3", "FAIL", f"{n} missing header version or first versioned change-log entry")
    d = mdocs.get(n)
    if d:
        ok = str(d.get("version")) == hdr[n]["Version"] and str(d.get("status")).upper() == (hdr[n]["Status"] or "").upper()
        rec("S3m", "PASS" if ok else "FAIL", f"{n} machine documents[] version/status {d.get('version')}/{d.get('status')} vs header {hdr[n]['Version']}/{hdr[n]['Status']}")
    else:
        rec("S3m", "FAIL", f"{n} absent from machine documents[]")

# S4 relative markdown links resolve
for p in sorted(ID.glob("*.md")):
    for t in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", p.read_text(encoding="utf8")):
        if re.match(r"[a-z]+://|mailto:", t): continue
        ok = (p.parent / t).resolve().exists()
        if not ok: rec("S4", "FAIL", f"{p.name}: broken relative link {t}")
rec("S4", "INFO", "relative-link scan finished (only failures listed above)")

# S4h heading structure: structural checks, not a prescribed wording template.
for n in REQ_MD:
    p = ID / f"{n}.md"
    if not p.exists(): continue
    body = re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf8"), flags=re.S)
    body = re.sub(r"^```.*?^```[^\n]*", "", body, flags=re.M | re.S)
    headings = re.findall(r"^#{1,6} +(.+)$", body, re.M)
    rec("S4h", "PASS" if headings else "FAIL", f"{n} has section headings")
    numbered = [int(x) for x in re.findall(r"^# +(\d+)\.", body, re.M)]
    rec("S4-order", "PASS" if numbered == sorted(set(numbered)) else "FAIL",
        f"{n} numbered top-level headings unique and ascending; semantic order not inferred")

# Exhaustive 064 section 8 content-class inventory. These are evidence locators,
# never content PASS: 8.3-8.7 additionally require per-instance review.
inventory = json.loads((pathlib.Path(__file__).parent / "slice0_content_inventory.json").read_text())
if {d["document"] for d in inventory["documents"]} != {n + ".md" for n in REQ_MD}:
    rec("S4-inventory", "FAIL", "required-content inventory does not cover exactly all 17 documents")
for d in inventory["documents"]:
    p = ID / d["document"]
    body = re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf8"), flags=re.S) if p.exists() else ""
    for q in d["requirements"]:
        pos = body.find(q["locator"])
        rec("S4-content-locator", "INFO" if pos >= 0 else "WARN",
            f"{d['document']} {d['source']} {q['requirement']}: " +
            ("document-level evidence located; satisfaction/per-instance coverage requires review" if pos >= 0
             else "reviewed locator absent; review required, not proof of missing requirement"))

# Header dependency references are documentary identifiers, not runtime dependencies.
for n in REQ_MD:
    p = ID / f"{n}.md"
    if not p.exists(): continue
    block = re.search(r"<!--(.*?)-->", p.read_text(encoding="utf8"), re.S)
    dep = re.search(r"^Dependencies:(.*?)(?=^Change Log|^Cross-Checked|^Contract boundaries|\Z)",
                    block.group(1) if block else "", re.M | re.S)
    refs = re.findall(r"(?:ADR-\d{4}_[\w-]+|\d{3}_[\w-]+|\d{2}_[\w-]+)(?:\.md)?", dep.group(1) if dep else "")
    rec("S4-dependencies", "PASS" if refs else "FAIL", f"{n} has resolvable dependency identifiers to check")
    for ref in refs:
        stem = ref.removesuffix(".md")
        hits = [x for root in (ID, ROOT) for x in root.glob(stem + ".md")]
        rec("S4-dependency-target", "PASS" if len(hits) == 1 else "FAIL", f"{n}: dependency {ref} resolves exactly once")

# Machine path and local JSON pointer resolution, recursively across the specification.
def machine_refs(node):
    if isinstance(node, dict):
        for key, val in node.items():
            if key in ("path", "narrative", "schema", "runbook", "adr0004ApprovalRecord", "acceptanceGates") and isinstance(val, str):
                target, _, fragment = val.partition("#")
                path = ID / target
                ok = path.is_file()
                if ok and fragment.startswith("/"):
                    try:
                        value = json.loads(path.read_text())
                        for token in fragment[1:].split("/"):
                            token = token.replace("~1", "/").replace("~0", "~")
                            value = value[int(token)] if isinstance(value, list) else value[token]
                    except (ValueError, KeyError, IndexError, TypeError, OSError): ok = False
                rec("S4-machine-ref", "PASS" if ok else "FAIL", f"machine {key}: {val}")
            machine_refs(val)
    elif isinstance(node, list):
        for val in node: machine_refs(val)
machine_refs(mach)
for kind in ("documents", "aggregates", "commands", "queries", "events"):
    entries = mach.get(kind, [])
    key = "path" if kind == "documents" else "name"
    ids = [v.get(key) for v in entries]
    rec("S9-identifiers", "PASS" if all(ids) and len(ids) == len(set(ids)) else "FAIL",
        f"machine {kind}: nonempty unique {key}")

# Per-instance structural anchors. These do not substitute for each item's
# required behavior, authorization, alternatives, consumers or field mapping.
for kind, filename in (("aggregates", "03_Aggregates.md"), ("commands", "04_Commands.md"),
                       ("queries", "05_Queries.md"), ("events", "06_Domain_Events.md")):
    p = ID / filename
    body = re.sub(r"<!--.*?-->", "", p.read_text(), flags=re.S) if p.exists() else ""
    for entry in mach.get(kind, []):
        name = entry["name"]
        if kind == "queries":
            ok = bool(re.search(r"^\| " + re.escape(name) + r" \|", body, re.M))
        else:
            ok = bool(re.search(r"^#{1,2} \d+(?:\.\d+)?\.? " + re.escape(name) +
                                (r" Aggregate" if kind == "aggregates" else "") + r"$", body, re.M))
        rec("S4-item-anchor", "PASS" if ok else "FAIL", f"{filename}: {name} specification anchor")

# S5 JSON / YAML / OpenAPI
for f in ("events.schema.json", "services.schema.json"):
    try:
        d = json.loads((ID / f).read_text(encoding="utf8")); Draft202012Validator.check_schema(d)
        rec("S5", "PASS", f"{f} parses and is a valid draft-2020-12 schema")
    except Exception as e: rec("S5", "FAIL", f"{f}: {str(e)[:160]}")
try:
    oas_validate(yaml.safe_load((ID / "openapi.yaml").read_text(encoding="utf8"))); rec("S5", "PASS", "openapi.yaml valid OpenAPI document")
except Exception as e: rec("S5", "FAIL", f"openapi.yaml: {str(e)[:200]}")

# S6 repository/producer presence and MVP baseline counts (not complete V-001/V-005)
for a in mach["aggregates"]:
    rec("V-001-presence-only", "PASS" if a.get("repository") else "FAIL", f"aggregate {a.get('name')} declares repository")
for e in mach["events"]:
    rec("S9-producer-presence-only", "PASS" if e.get("producer") else "FAIL", f"event {e.get('name')} declares producer")
counts = (len(mach["aggregates"]), len(mach["commands"]), len(mach["queries"]), len(mach["events"]))
rec("S6", "PASS" if counts == (5, 6, 5, 10) else "FAIL", f"machine counts aggregates/commands/queries/events {counts} vs pinned review expectation (5,6,5,10); narrative equality not checked")

# V-008 unresolved TODO in MVP docs
for n in REQ_MD:
    p = ID / f"{n}.md"
    if p.exists():
        for i, l in enumerate(p.read_text(encoding="utf8").splitlines(), 1):
            if re.search(r"\b(TODO|TBD|FIXME)\b", l): rec("V-008", "WARN", f"{n}.md:{i} {l.strip()[:100]}")

NOT_CHECKED = [
 "V-001 exactly-one repository and V-005 owning Capability Platform (repository/producer presence is not these complete rules)",
 "064 section 8 semantic sufficiency, per-instance 8.3-8.7 coverage and conditional applicability; locator inventory is not PASS",
 "064 semantic section ordering/naming, required plain-text normative references, Markdown anchor validity; only top-level numerical order and dependency targets checked",
 "V-002/V-003/V-004/V-007/V-009 (need narrative-to-machine mapping; not automated here)",
 "V-006 machine-vs-narrative semantic equality; 065 sections 6-8, 10 semantic/contract/dependency/MVP validation",
 "OpenAPI/JSON-Schema conformance of DTO examples against schemas; consumer compatibility",
 "V-011 external references; V-012 full naming conventions; runtime/security behaviour; rendering",
 "Overall Structural/Semantic/Architectural/AI Readiness gates: NOT ESTABLISHED; exit 0 only means no executed FAIL"]
if "--json" in sys.argv:
    print(json.dumps({"results": results, "not_checked": NOT_CHECKED}, indent=1))
else:
    from collections import Counter
    c = Counter(r[1] for r in results)
    for cid, lvl, msg in results:
        if lvl != "PASS": print(f"[{lvl}] {cid}: {msg}")
    print(f"\nSUMMARY: {dict(c)}")
    print("NOT CHECKED:"); [print(" -", x) for x in NOT_CHECKED]
sys.exit(1 if any(r[1] == "FAIL" for r in results) else 0)
