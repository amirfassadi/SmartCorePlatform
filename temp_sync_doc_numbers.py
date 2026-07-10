import pathlib
import re
from collections import defaultdict

root = pathlib.Path('f:/projects/SmartCorePlatform')
md_files = sorted([p for p in root.rglob('*.md') if p.is_file()])

basename_to_path = {p.name: p for p in md_files}
suffix_to_basenames = defaultdict(list)

for base in basename_to_path:
    m = re.match(r'^(\d{3})_(.+)$', base)
    if m:
        suffix_to_basenames[m.group(2)].append(base)

ref_pattern = re.compile(r'(?P<path>(?:[A-Za-z0-9_./%&@()+\- ]*/)?)(?P<base>(?P<num>\d{3})_(?P<suffix>[^\s\)\]\"\']+?\.md))')
header_pattern = re.compile(r'^(?P<leading>#+\s*)(?P<base>\d{3}_[^\s]+\.md)(?P<rest>.*)$', re.MULTILINE)
docid_pattern = re.compile(r'^(?P<leading>\s*Document ID:\s*)(?P<num>\d{2,3})(?P<rest>\s*)$', re.MULTILINE)

modified_files = []
modified_references = []
header_mismatches = []
docid_mismatches = []
unresolved_references = []

for p in md_files:
    text = p.read_text(encoding='utf-8')
    original = text
    basename = p.name
    own_num = basename[:3] if len(basename) >= 3 and basename[:3].isdigit() else None
    own_suffix = basename[4:] if own_num else None

    def header_repl(m):
        base = m.group('base')
        if own_suffix and base.endswith(own_suffix) and base != basename:
            header_mismatches.append((p, base, basename))
            return m.group('leading') + basename + m.group('rest')
        return m.group(0)
    text = header_pattern.sub(header_repl, text)

    def docid_repl(m):
        if own_num and m.group('num') != own_num:
            docid_mismatches.append((p, m.group(0), own_num))
            return m.group('leading') + own_num + m.group('rest')
        return m.group(0)
    text = docid_pattern.sub(docid_repl, text)

    def ref_repl(m):
        path = m.group('path')
        base = m.group('base')
        suffix = m.group('suffix')
        if base in basename_to_path:
            return m.group(0)
        candidates = suffix_to_basenames.get(suffix, [])
        if len(candidates) == 1:
            replacement = candidates[0]
            if replacement != base:
                modified_references.append((p, base, replacement))
                return path + replacement
        elif len(candidates) > 1:
            # ambiguous; if one candidate has current file number matching old prefix? maybe not
            unresolved_references.append((p, base, candidates))
        else:
            unresolved_references.append((p, base, None))
        return m.group(0)

    text = ref_pattern.sub(ref_repl, text)

    if text != original:
        p.write_text(text, encoding='utf-8')
        modified_files.append(p)

# Validate
still_unresolved = []
for p in md_files:
    text = p.read_text(encoding='utf-8')
    for m in ref_pattern.finditer(text):
        base = m.group('base')
        if base not in basename_to_path:
            still_unresolved.append((p, base))

report = {
    'modified_files': sorted({str(p.relative_to(root)).replace('\\','/') for p in modified_files}),
    'modified_references': [(str(p.relative_to(root)).replace('\\','/'), old, new) for p, old, new in modified_references],
    'header_mismatches': [(str(p.relative_to(root)).replace('\\','/'), old, new) for p, old, new in header_mismatches],
    'docid_mismatches': [(str(p.relative_to(root)).replace('\\','/'), old, new) for p, old, new in docid_mismatches],
    'initial_unresolved': [(str(p.relative_to(root)).replace('\\','/'), base, candidates) for p, base, candidates in unresolved_references],
    'still_unresolved': sorted({(str(p.relative_to(root)).replace('\\','/'), base) for p, base in still_unresolved}),
}
print('FILES_MODIFIED:', len(report['modified_files']))
for f in report['modified_files']:
    print('FILE', f)
print('REFERENCES_FIXED:', len(report['modified_references']))
for f, old, new in report['modified_references']:
    print('REF', f, old, '->', new)
print('HEADER_MISMATCHES_FIXED:', len(report['header_mismatches']))
for f, old, new in report['header_mismatches']:
    print('HEADER', f, old, '->', new)
print('DOCID_MISMATCHES_FIXED:', len(report['docid_mismatches']))
for f, old, new in report['docid_mismatches']:
    print('DOCID', f, old, '->', new)
print('INITIAL_UNRESOLVED:', len(report['initial_unresolved']))
for f, base, candidates in report['initial_unresolved']:
    print('UNRESOLVED', f, base, 'candidates:', candidates)
print('STILL_UNRESOLVED:', len(report['still_unresolved']))
for f, base in report['still_unresolved']:
    print('STILL_UNRESOLVED', f, base)
