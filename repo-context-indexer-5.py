#!/usr/bin/env python3
"""
Repo Context Indexer v3
========================
Scans ANY repository (NestJS/TypeScript, Python, C++/Arduino firmware, or
mixed) and generates a single CONTEXT.md (+ optional CONTEXT.json) that you
can paste at the start of a Claude conversation so it instantly understands
the full project structure, the module dependency graph, database schema,
and the content of key entry-point files.

Usage:
    python repo-context-indexer.py --repo "/path/to/your/project" --output CONTEXT.md
    python repo-context-indexer.py --repo . --output CONTEXT.md --json --include-content main.ts,app.module.ts

No external dependencies required — pure standard library.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import deque
import json
import re


@dataclass(slots=True)
class Fact:
    """One normalized (subject, predicate, object) triple with provenance.
    Every graph the tool produces (imports, DB relations, calls, events,
    DB usage, enums, guard clauses) is expressed as a list of these, so
    downstream tools (GraphML, Neo4j, an MCP server) have one consistent
    shape to consume instead of five different graph structures.

    Deliberately has NO numeric confidence score: every Fact here comes
    from a literal pattern in the source (an import statement, a decorator,
    a call site, a thrown exception) — not inferred meaning.
    `extraction_method` says exactly which pattern produced it, and
    `evidence` carries the raw matched text, so a human can verify instead
    of trusting a made-up probability."""
    subject: str
    predicate: str
    object: str
    source_file: str
    line: int | None = None
    extraction_method: str = "unknown"
    evidence: str | None = None

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next",
    "__pycache__", ".cache", "coverage", ".nyc_output", "vendor",
    ".angular", ".vscode", ".idea", "bin", "obj", "packages",
    "TestResults", ".vs", "migrations", "venv", ".venv", "env",
    ".pytest_cache", ".mypy_cache", "target"
}

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff",
    ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".tar", ".gz",
    ".map", ".min.js", ".min.css", ".kicad_pcb", ".kicad_sch",
    ".kicad_pro", ".docx", ".xlsx", ".lock", ".pyc", ".so", ".dll"
}

SKIP_FILENAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    ".prettierrc", ".eslintrc.json", ".eslintrc.js",
    Path(__file__).name,  # never index this indexer itself
}

# Files Claude almost always needs full context on, if present.
DEFAULT_KEY_FILENAMES = {
    "main.ts", "app.module.ts", "app.py", "manage.py", "settings.py",
    "index.ts", "index.js", "server.ts", "server.js", "wsgi.py", "asgi.py"
}

MAX_FILE_SIZE_KB = 80          # above this -> summarized, not skipped
LARGE_FILE_HEAD_LINES = 60     # how many lines to show for large/key files
LARGE_FILE_TAIL_LINES = 15     # plus a tail, so trailing exports aren't lost

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def normalize(content: str) -> str:
    """Collapse multi-line signatures so single-line regexes still match
    things like:
        export class Foo
            extends Bar
            implements Baz {
    """
    # Join lines that end mid-signature (no ; { } at end) with the next line.
    lines = content.split("\n")
    out = []
    buf = ""
    for line in lines:
        stripped = line.rstrip()
        buf += (" " if buf else "") + stripped.strip()
        if stripped.endswith(("{", ";", "}", ",")) or stripped == "":
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return "\n".join(out)


def head_tail(content: str, head: int, tail: int) -> str:
    lines = content.splitlines()
    if len(lines) <= head + tail:
        return content
    return "\n".join(
        lines[:head] + [f"... ({len(lines) - head - tail} lines omitted) ..."] + lines[-tail:]
    )


# ─────────────────────────────────────────────
# Parsers
# ─────────────────────────────────────────────

def parse_imports_ts(content: str) -> list:
    """Extract local (relative) imports so we can build a dependency graph."""
    imports = []
    for m in re.finditer(r'''import\s+(?:[\w*{}\s,]+\s+from\s+)?['"](\.[^'"]+)['"]''', content):
        imports.append(m.group(1))
    return imports


def parse_imports_py(content: str) -> list:
    imports = []
    for m in re.finditer(r'^\s*from\s+(\.[\w.]*)\s+import', content, re.MULTILINE):
        imports.append(m.group(1))
    for m in re.finditer(r'^\s*import\s+(\.[\w.]*)', content, re.MULTILINE):
        imports.append(m.group(1))
    return imports


def strip_comments(content: str) -> str:
    """Remove // line comments and /* */ block comments so they never get
    mistaken for real code (e.g. validator error-message comments matching
    a 'name: type' pattern)."""
    no_block = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    no_line = re.sub(r'(?<!:)//.*', '', no_block)
    return no_line


def parse_class_fields(content: str) -> list:
    """Extract real TS class property declarations only (not arbitrary
    'word: word' matches), correctly handling generic types like
    Record<string, number> or Array<{ a: string }> by requiring the
    declaration to end in ';' or '=' rather than stopping at the first
    comma/colon found anywhere in the file."""
    clean = strip_comments(content)
    fields = []
    skip_names = {"constructor", "if", "for", "while", "switch", "function", "return"}

    pattern = re.compile(
        r'^[ \t]*(?:@\w+(?:\([^()]*(?:\([^()]*\)[^()]*)*\))?\s*)*'  # optional decorator(s)
        r'(?:public\s+|private\s+|readonly\s+|protected\s+|static\s+)*'
        r'(\w+)\s*[?!]?\s*:\s*'
        r'((?:[^;=\n{}]|\{[^{}]*\})+?)'   # type, allowing one level of {} (inline object types)
        r'\s*(?:=[^;]*)?;',
        re.MULTILINE
    )
    for m in pattern.finditer(clean):
        name, ftype = m.group(1), " ".join(m.group(2).split())
        if name in skip_names or not ftype:
            continue
        fields.append(f"{name}: {ftype}")
    return fields


# Recognized class-validator decorator names. Restricting to a known set
# (rather than accepting any @Whatever) keeps this from picking up unrelated
# decorators (like @ApiProperty) and mislabeling them as validation rules.
KNOWN_VALIDATOR_DECORATORS = {
    "IsNotEmpty", "IsOptional", "IsEmail", "IsString", "IsNumber", "IsInt",
    "IsBoolean", "IsEnum", "IsUUID", "IsDate", "IsDateString", "Min", "Max",
    "MinLength", "MaxLength", "Length", "Matches", "IsPositive", "IsNegative",
    "IsArray", "IsObject", "ArrayMinSize", "ArrayMaxSize", "IsUrl",
    "IsPhoneNumber", "IsAlpha", "IsAlphanumeric", "IsIn", "IsNotIn",
    "ValidateNested", "IsJSON", "IsLatitude", "IsLongitude", "IsDecimal",
}


def parse_validation_rules(norm_content: str) -> list:
    """Pair each field with the class-validator decorators directly above it
    (on normalized content, since normalize() already joins a decorator line
    to the field it decorates). This gives real, code-backed constraints —
    not inferred business logic — so it's safe to present as fact."""
    pattern = re.compile(r'((?:@\w+(?:\([^()]*\))?\s*)+)(\w+)\s*[?!]?\s*:', re.MULTILINE)
    results = []
    for m in pattern.finditer(norm_content):
        decorator_names = re.findall(r'@(\w+)', m.group(1))
        rules = [d for d in decorator_names if d in KNOWN_VALIDATOR_DECORATORS]
        if rules:
            results.append({"field": m.group(2), "rules": rules})
    return results


def parse_typescript(content: str, filepath: str) -> dict:
    info = {}
    norm = normalize(content)

    imports = parse_imports_ts(content)
    if imports:
        info["imports"] = imports

    # Decorators (NestJS)
    decorators = re.findall(
        r'@(Controller|Injectable|Module|Guard|Pipe|Interceptor|Middleware|'
        r'Resolver|Query|Mutation|Subscription|EventPattern|MessagePattern)\s*[(\n]',
        content
    )
    if decorators:
        info["nestjs"] = sorted(set(decorators))

    # Controller routes (base path + per-method paths)
    base_path = ""
    base_match = re.search(r'@Controller\s*\(\s*[\'"]([^\'"]*)[\'"]\s*\)', content)
    if base_match:
        base_path = base_match.group(1)
    if "Controller" in decorators:
        routes = []
        for m in re.finditer(r'@(Get|Post|Put|Patch|Delete|Options)\s*\(\s*[\'"]?([^\'")\s]*)[\'"]?\s*\)', content):
            full = "/".join(p.strip("/") for p in (base_path, m.group(2)) if p)
            routes.append(f"{m.group(1)} /{full}")
        if routes:
            info["routes"] = routes[:15]

    # Classes with inheritance (run on normalized content so multi-line works)
    classes = []
    for m in re.finditer(
        r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)'
        r'(?:\s+extends\s+([\w<>,\. ]+?))?'
        r'(?:\s+implements\s+([\w<>,\. ]+?))?\s*\{',
        norm
    ):
        entry = m.group(1)
        if m.group(2):
            entry += f" extends {m.group(2).strip()}"
        if m.group(3):
            entry += f" implements {m.group(3).strip()}"
        classes.append(entry)
    if classes:
        info["classes"] = classes

    # Constructor-injected dependencies (common NestJS DI pattern)
    ctor_match = re.search(r'constructor\s*\(([^)]*)\)', norm)
    injected_map = {}  # varName -> TypeName, used below to build the call graph
    if ctor_match:
        deps = re.findall(r'(?:private|public|readonly|protected|\s)+(\w+)\s*:\s*(\w+)', ctor_match.group(1))
        if deps:
            info["injected"] = [f"{n}: {t}" for n, t in deps]
            injected_map = {n: t for n, t in deps}

    # Real, mechanical call graph: find this.<injectedVar>.<method>(...) call
    # sites and resolve <injectedVar> back to its injected TYPE via the
    # constructor mapping above. This is genuine static analysis (not a
    # guess) — it shows which injected services/repositories a class
    # actually calls methods on, which is the backbone of a call graph.
    if injected_map:
        calls = []
        for m in re.finditer(r'this\.(\w+)\.(\w+)\s*\(', content):
            var, method = m.group(1), m.group(2)
            target_type = injected_map.get(var)
            if target_type and method not in ("constructor",):
                calls.append({"target": target_type, "method": method})
        if calls:
            # de-duplicate while preserving order
            seen = set()
            deduped = []
            for c in calls:
                key = (c["target"], c["method"])
                if key not in seen:
                    seen.add(key)
                    deduped.append(c)
            info["calls"] = deduped[:30]

    # Event producer/consumer extraction — string literals passed to
    # .emit()/.publish() (produced) or @OnEvent()/.subscribe() (consumed).
    # Only matches on quoted string event/topic names, so it can't
    # hallucinate an event that isn't literally referenced in code.
    produces = [m.group(1) for m in re.finditer(
        r'\.(?:emit|publish)\s*\(\s*[\'"]([\w.\-/:]+)[\'"]', content)]
    consumes = [m.group(1) for m in re.finditer(
        r'@OnEvent\s*\(\s*[\'"]([\w.\-/:]+)[\'"]', content)]
    consumes += [m.group(1) for m in re.finditer(
        r'\.subscribe\s*\(\s*[\'"]([\w.\-/:]+)[\'"]', content)]
    if produces:
        info["produces_events"] = sorted(set(produces))
    if consumes:
        info["consumes_events"] = sorted(set(consumes))

    # Database read/write usage — resolves this.<prismaVar>.<model>.<method>()
    # call sites, using the injected-type map above to find which variable
    # is actually a PrismaService, then classifies the method as a read or
    # write by name. Fully mechanical: no guess about intent, just naming.
    prisma_vars = [n for n, t in injected_map.items() if "prisma" in t.lower()]
    if prisma_vars:
        var_alt = "|".join(re.escape(v) for v in prisma_vars)
        write_methods = {"create", "update", "delete", "upsert",
                          "createmany", "updatemany", "deletemany"}
        usage = []
        for m in re.finditer(rf'this\.(?:{var_alt})\.(\w+)\.(\w+)\s*\(', content):
            model_field, method = m.group(1), m.group(2)
            op = "write" if method.lower() in write_methods else "read"
            usage.append({"model_field": model_field, "method": method, "op": op})
        if usage:
            seen_u = set()
            deduped_u = []
            for u in usage:
                key = (u["model_field"], u["method"])
                if key not in seen_u:
                    seen_u.add(key)
                    deduped_u.append(u)
            info["db_usage"] = deduped_u[:30]

    # Guard-clause extraction: `if (<condition>) { throw new X(...) }`.
    # The condition text is kept EXACTLY as written — this is deliberately
    # not translated into a claim like "requires positive balance", because
    # that translation is an interpretation the regex can't verify.
    guard_pattern = re.compile(r'if\s*\(([^{;]{1,200}?)\)\s*\{?\s*throw\s+new\s+(\w+)\s*\(')
    guard_clauses = []
    for m in guard_pattern.finditer(content):
        condition = " ".join(m.group(1).split())
        guard_clauses.append({
            "condition": condition,
            "exception": m.group(2),
            "line": content.count("\n", 0, m.start()) + 1
        })
    if guard_clauses:
        info["guard_clauses"] = guard_clauses[:20]

    # TypeORM relation decorators (for DB relationship graph).
    # Matches things like:
    #   @OneToMany(() => Post, post => post.author)
    #   posts: Post[];
    orm_rel_pattern = re.compile(
        r'@(OneToMany|ManyToOne|OneToOne|ManyToMany)\s*\(\s*\(?\)?\s*=>\s*(\w+)[^)]*\)'
        r'\s*(?:@\w+\([^)]*\)\s*)*'
        r'(\w+)\s*[?!]?\s*:'
    )
    orm_relations = [
        {"kind": m.group(1), "target": m.group(2), "field": m.group(3)}
        for m in orm_rel_pattern.finditer(norm)
    ]
    if orm_relations:
        info["orm_relations"] = orm_relations

    # Entity name this file's relations belong to (needed to build DB graph edges)
    entity_match = re.search(r'@Entity\s*\([^)]*\)\s*(?:export\s+)?class\s+(\w+)', norm)
    if entity_match:
        info["entity_name"] = entity_match.group(1)
    elif orm_relations and classes:
        info["entity_name"] = classes[0].split()[0]

    # Interfaces
    interfaces = re.findall(r'(?:export\s+)?interface\s+(\w+)', content)
    if interfaces:
        info["interfaces"] = sorted(set(interfaces))

    # Enums
    ts_enums = []
    for m in re.finditer(r'(?:export\s+)?enum\s+(\w+)\s*\{([^}]*)\}', content):
        values = []
        for part in m.group(2).split(","):
            ident = part.strip().split("=")[0].strip()
            if ident:
                values.append(ident)
        ts_enums.append({"name": m.group(1), "values": values})
    if ts_enums:
        info["enums"] = [e["name"] for e in ts_enums]      # kept for existing display line
        info["enum_values"] = ts_enums                       # full data, used for Fact building

    # Exported functions/consts
    exports = re.findall(r'export\s+(?:async\s+)?(?:function|const|class|enum|type|interface)\s+(\w+)', content)
    if exports:
        info["exports"] = sorted(set(exports))

    # DTO fields (also useful on entities files, kept scoped to filenames
    # that suggest a plain data shape to avoid noisy output)
    if "dto" in filepath.lower() or "entity" in filepath.lower():
        fields = parse_class_fields(content)
        if fields:
            info["dto_fields"] = fields[:15]
        val_rules = parse_validation_rules(norm)
        if val_rules:
            info["validation_rules"] = val_rules[:15]

    # Service / generic class methods — only match real method declarations
    # (indented, inside a class body, not control-flow keywords, not arrow
    # functions assigned elsewhere).
    if "service" in filepath.lower() or "controller" in filepath.lower() or "repository" in filepath.lower():
        method_re = re.compile(
            r'^\s{2,}(?:public\s+|private\s+|protected\s+|static\s+|async\s+)*'
            r'(\w+)\s*\([^)]*\)\s*(?::\s*[\w<>\[\]., |]+)?\s*\{',
            re.MULTILINE
        )
        skip = {"constructor", "if", "for", "while", "switch", "catch"}
        methods = [m for m in method_re.findall(content) if m not in skip]
        if methods:
            info["methods"] = list(dict.fromkeys(methods))[:15]

    return info


def parse_python(content: str, filepath: str) -> dict:
    info = {}
    imports = parse_imports_py(content)
    if imports:
        info["imports"] = imports

    classes = []
    for m in re.finditer(r'^class\s+(\w+)\s*(?:\(([^)]*)\))?\s*:', content, re.MULTILINE):
        entry = m.group(1)
        if m.group(2) and m.group(2).strip():
            entry += f"({m.group(2).strip()})"
        classes.append(entry)
    if classes:
        info["classes"] = classes

    funcs = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)
    if funcs:
        info["functions"] = funcs[:15]

    methods = re.findall(r'^\s{4,}def\s+(\w+)\s*\(', content, re.MULTILINE)
    methods = [m for m in methods if not m.startswith("__") or m == "__init__"]
    if methods:
        info["methods"] = list(dict.fromkeys(methods))[:15]

    decorators = re.findall(r'@(app\.route|router\.\w+|api_view|action|task)', content)
    if decorators:
        info["decorators"] = sorted(set(decorators))

    routes = re.findall(r'@app\.route\s*\(\s*[\'"]([^\'"]+)[\'"](?:.*methods\s*=\s*\[([^\]]*)\])?', content)
    if routes:
        info["routes"] = [f"{(m or 'GET').replace(chr(39),'').strip()} {r}" for r, m in routes][:15]

    return info


def parse_prisma(content: str) -> dict:
    """Extract models and enums from a Prisma schema, including relation
    fields. NOTE: keeps ALL model fields (no truncation here) since relation
    object fields are often declared last in a model — truncating early
    would silently hide relationships from the DB graph. Display-time
    truncation happens later, in the markdown renderer, not here."""
    models = []
    for m in re.finditer(r'model\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL):
        model_name = m.group(1)
        fields_text = m.group(2)
        fields = []
        for line in fields_text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('@@'):
                parts = line.split()
                if len(parts) >= 2:
                    fields.append(f"{parts[0]}: {parts[1]}")
        models.append({"name": model_name, "fields": fields})

    enums = []
    for m in re.finditer(r'enum\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL):
        values = [v.strip() for v in m.group(2).strip().split('\n')
                  if v.strip() and not v.strip().startswith('//')]
        enums.append({"name": m.group(1), "values": values})

    result = {}
    if models:
        result["prisma_models"] = models
    if enums:
        result["prisma_enums"] = enums
    return result


def parse_cpp(content: str) -> dict:
    info = {}
    classes = re.findall(r'class\s+(\w+)', content)
    if classes:
        info["classes"] = sorted(set(classes))
    includes = re.findall(r'#include\s+[<"]([^>"]+)[>"]', content)
    if includes:
        info["includes"] = includes[:10]
    if 'void setup()' in content:
        info["arduino"] = True
    return info


def parse_markdown_headings(content: str) -> list:
    headings = []
    for m in re.finditer(r'^(#{1,3})\s+(.+)$', content, re.MULTILINE):
        level = len(m.group(1))
        headings.append(("  " * (level - 1)) + "- " + m.group(2).strip())
    return headings[:20]


# ─────────────────────────────────────────────
# File Analyzer
# ─────────────────────────────────────────────

def analyze_file(path: Path, repo_root: Path, key_filenames: set) -> dict | None:
    rel = str(path.relative_to(repo_root)).replace("\\", "/")
    ext = path.suffix.lower()
    name = path.name

    if ext in SKIP_EXTENSIONS:
        return None
    if name in SKIP_FILENAMES:
        return None
    if name.endswith(".d.ts"):
        return None

    try:
        size_kb = path.stat().st_size / 1024
    except OSError:
        return None

    result = {"path": rel, "size_kb": round(size_kb, 1), "ext": ext}
    is_key = name in key_filenames

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        if size_kb > MAX_FILE_SIZE_KB:
            result["note"] = f"Large file ({size_kb:.0f}KB), unreadable"
        return result

    large = size_kb > MAX_FILE_SIZE_KB
    if large:
        result["note"] = f"Large file ({size_kb:.0f}KB) — summarized below"

    # Parse by type (still run for large files so structure isn't lost)
    if ext in {".ts", ".tsx"}:
        result.update(parse_typescript(content, rel))
    elif ext == ".py":
        result.update(parse_python(content, rel))
    elif name == "schema.prisma" or ext == ".prisma":
        result.update(parse_prisma(content))
    elif ext in {".cpp", ".cc", ".h", ".hpp"}:
        result.update(parse_cpp(content))
    elif ext == ".md":
        headings = parse_markdown_headings(content)
        if headings:
            result["headings"] = headings
    elif name == "package.json":
        try:
            data = json.loads(content)
            result["pkg_name"] = data.get("name")
            result["pkg_version"] = data.get("version")
            result["scripts"] = list(data.get("scripts", {}).keys())
            result["main_deps"] = list(data.get("dependencies", {}).keys())[:20]
        except json.JSONDecodeError:
            pass

    # Attach raw content snippet for large files or explicitly key files,
    # instead of just skipping/listing them with no detail.
    if large or is_key:
        result["snippet"] = head_tail(content, LARGE_FILE_HEAD_LINES, LARGE_FILE_TAIL_LINES)
        result["is_key"] = is_key

    return result


# ─────────────────────────────────────────────
# Tree Builder
# ─────────────────────────────────────────────

def build_tree(repo_root: Path, max_depth: int = 4) -> str:
    lines = []

    def walk(path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except OSError:
            return

        dirs = [e for e in entries if e.is_dir() and e.name not in SKIP_DIRS]
        files = [e for e in entries if e.is_file()
                 and e.suffix.lower() not in SKIP_EXTENSIONS
                 and e.name not in SKIP_FILENAMES]

        for d in dirs:
            lines.append(f"{prefix}📁 {d.name}/")
            walk(d, prefix + "   ", depth + 1)

        for f in files[:8]:
            lines.append(f"{prefix}📄 {f.name}")
        if len(files) > 8:
            lines.append(f"{prefix}   (+{len(files) - 8} more)")

    walk(repo_root)
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Dependency Graph
# ─────────────────────────────────────────────

def resolve_relative_import(from_path: str, imp: str) -> str:
    """Best-effort resolution of a relative import to a repo-relative path
    (without extension, since we don't know if it's .ts/.tsx/index etc.)."""
    base_dir = Path(from_path).parent
    resolved = (base_dir / imp).as_posix()
    # Normalize ../ and ./ segments
    parts = []
    for part in resolved.split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part == "." or part == "":
            continue
        else:
            parts.append(part)
    return "/".join(parts)


def build_dependency_graph(all_files: list) -> dict:
    """Map: file -> [resolved local files it imports]"""
    graph = {}
    by_stem = {}
    for f in all_files:
        stem = f["path"].rsplit(".", 1)[0]
        by_stem[stem] = f["path"]
        by_stem[stem.replace("/index", "")] = f["path"]

    for f in all_files:
        imports = f.get("imports")
        if not imports:
            continue
        resolved = []
        for imp in imports:
            target = resolve_relative_import(f["path"], imp)
            match = by_stem.get(target)
            if match and match != f["path"]:
                resolved.append(match)
        if resolved:
            graph[f["path"]] = sorted(set(resolved))
    return graph


# ─────────────────────────────────────────────
# Event Producer / Consumer Graph (mechanical)
# ─────────────────────────────────────────────

def build_event_graph(all_files: list) -> dict:
    """Map: event/topic name -> {producers: [...], consumers: [...]}.
    Built from literal .emit()/.publish() and @OnEvent()/.subscribe() call
    sites found per file — every entry traces back to an actual string
    literal in the code."""
    graph = {}
    for f in all_files:
        classes = f.get("classes")
        source = classes[0].split()[0] if classes else Path(f["path"]).stem
        for e in f.get("produces_events", []):
            graph.setdefault(e, {"producers": set(), "consumers": set()})["producers"].add(source)
        for e in f.get("consumes_events", []):
            graph.setdefault(e, {"producers": set(), "consumers": set()})["consumers"].add(source)
    return {e: {"producers": sorted(v["producers"]), "consumers": sorted(v["consumers"])}
            for e, v in graph.items()}


def generate_mermaid_event_graph(event_graph: dict, max_events: int = 60) -> str | None:
    if not event_graph:
        return None
    events = list(event_graph.items())[:max_events]
    lines = ["```mermaid", "flowchart LR"]
    for event, sides in events:
        eid = sanitize_mermaid_id(event)
        lines.append(f'  {eid}(["📡 {event}"])')
        for p in sides["producers"]:
            lines.append(f'  {sanitize_mermaid_id(p)} -->|emits| {eid}')
        for c in sides["consumers"]:
            lines.append(f'  {eid} -->|consumed by| {sanitize_mermaid_id(c)}')
    lines.append("```")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Database Usage Graph — who reads/writes which model (mechanical)
# ─────────────────────────────────────────────

def build_db_usage_graph(all_files: list, model_names: list) -> list:
    """Resolve each this.prisma.<model>.<method>() call site to a typed
    read/write edge against the actual model name (matched case-insensitively
    since Prisma client properties are lowerCamelCase of the model name)."""
    lower_map = {n[0].lower() + n[1:]: n for n in model_names} if model_names else {}
    edges = []
    for f in all_files:
        usage = f.get("db_usage")
        if not usage:
            continue
        classes = f.get("classes")
        source = classes[0].split()[0] if classes else Path(f["path"]).stem
        for u in usage:
            model = lower_map.get(u["model_field"], u["model_field"])
            edges.append({"source": source, "model": model, "method": u["method"], "op": u["op"]})
    return edges


# ─────────────────────────────────────────────
# Database Relationship Graph
# ─────────────────────────────────────────────

def build_db_graph(all_files: list) -> dict:
    """Collect DB-level relationships from Prisma schema(s) and/or TypeORM
    entity decorators, producing one unified graph of model/entity relations:
        {"models": [...], "edges": [{"source","target","field","kind","source_type"}]}
    """
    models = set()
    edges = []

    # ---- Prisma: infer relations by matching field types to model names ----
    prisma_model_names = {
        model["name"]
        for f in all_files
        for model in f.get("prisma_models", [])
    }
    for f in all_files:
        for model in f.get("prisma_models", []):
            models.add(model["name"])
            for field in model["fields"]:
                if ":" not in field:
                    continue
                fname, ftype = (p.strip() for p in field.split(":", 1))
                is_array = ftype.endswith("[]")
                base_type = ftype.rstrip("[]").rstrip("?").strip()
                if base_type in prisma_model_names and base_type != model["name"]:
                    edges.append({
                        "source": model["name"], "target": base_type, "field": fname,
                        "kind": "many" if is_array else "one", "source_type": "prisma"
                    })

    # ---- TypeORM: use @OneToMany/@ManyToOne/etc decorators directly ----
    for f in all_files:
        entity = f.get("entity_name")
        if not entity or not f.get("orm_relations"):
            continue
        models.add(entity)
        for rel in f["orm_relations"]:
            target = rel["target"]
            models.add(target)
            kind = "many" if rel["kind"] in ("OneToMany", "ManyToMany") else "one"
            edges.append({
                "source": entity, "target": target, "field": rel["field"],
                "kind": kind, "source_type": "orm"
            })

    return {"models": sorted(models), "edges": edges}


def sanitize_mermaid_id(s: str) -> str:
    """Mermaid node IDs can't contain slashes, dots, dashes, etc."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', s)


def generate_mermaid_dependency_graph(dep_graph: dict, max_nodes: int = 120) -> str | None:
    """Visual flowchart of file-to-file (local import) dependencies,
    clustered into subgraphs by top-level folder."""
    if not dep_graph:
        return None

    nodes = set()
    for src, targets in dep_graph.items():
        nodes.add(src)
        nodes.update(targets)

    truncated = False
    if len(nodes) > max_nodes:
        # Keep the most-connected files (highest in+out degree) for readability
        degree = {}
        for src, targets in dep_graph.items():
            degree[src] = degree.get(src, 0) + len(targets)
            for t in targets:
                degree[t] = degree.get(t, 0) + 1
        nodes = set(sorted(degree, key=lambda k: -degree[k])[:max_nodes])
        truncated = True

    groups = {}
    for n in nodes:
        top = n.split("/")[0] if "/" in n else "_root"
        groups.setdefault(top, []).append(n)

    lines = ["```mermaid", "flowchart LR"]
    for group, members in sorted(groups.items()):
        lines.append(f'  subgraph {sanitize_mermaid_id(group)}["📁 {group}"]')
        for n in sorted(members):
            lines.append(f'    {sanitize_mermaid_id(n)}["{Path(n).name}"]')
        lines.append("  end")

    for src, targets in dep_graph.items():
        if src not in nodes:
            continue
        for t in targets:
            if t not in nodes:
                continue
            lines.append(f'  {sanitize_mermaid_id(src)} --> {sanitize_mermaid_id(t)}')
    lines.append("```")

    if truncated:
        lines.append(f"\n*Graph truncated to the {max_nodes} most-connected files for readability "
                      f"(use --max-graph-nodes to change this).*")
    return "\n".join(lines)


def generate_mermaid_er_graph(db_graph: dict) -> str | None:
    """Visual entity-relationship diagram built from Prisma / TypeORM relations."""
    if not db_graph or not db_graph.get("edges"):
        return None

    lines = ["```mermaid", "erDiagram"]
    seen = set()
    for e in db_graph["edges"]:
        src, tgt = sanitize_mermaid_id(e["source"]), sanitize_mermaid_id(e["target"])
        key = (src, tgt, e["field"])
        if key in seen:
            continue
        seen.add(key)
        # left side is always "one" (the row holding/declaring the relation);
        # right side depends on whether it's a to-many or to-one relation.
        card = '||--o{' if e["kind"] == "many" else '||--||'
        lines.append(f'  {src} {card} {tgt} : "{e["field"]}"')
    lines.append("```")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Service Call Graph (mechanical, not inferred)
# ─────────────────────────────────────────────

def build_call_graph(all_files: list) -> list:
    """Turn each file's `calls` (this.injected.method()) into edges between
    the file's own primary class and the class/type it calls into.
    Purely structural — every edge corresponds to an actual call site."""
    edges = []
    for f in all_files:
        calls = f.get("calls")
        if not calls:
            continue
        classes = f.get("classes")
        source = classes[0].split()[0] if classes else Path(f["path"]).stem
        for c in calls:
            edges.append({
                "source": source, "target": c["target"], "method": c["method"],
                "file": f["path"]
            })
    return edges


def generate_mermaid_call_graph(call_graph: list, max_edges: int = 150) -> str | None:
    if not call_graph:
        return None

    truncated = False
    edges = call_graph
    if len(edges) > max_edges:
        edges = edges[:max_edges]
        truncated = True

    lines = ["```mermaid", "flowchart TD"]
    seen_edges = set()
    for e in edges:
        src, tgt = sanitize_mermaid_id(e["source"]), sanitize_mermaid_id(e["target"])
        key = (src, tgt, e["method"])
        if key in seen_edges or src == tgt:
            continue
        seen_edges.add(key)
        lines.append(f'  {src} -->|{e["method"]}()| {tgt}')
    lines.append("```")

    if truncated:
        lines.append(f"\n*Graph truncated to the first {max_edges} call edges "
                      f"(use --max-graph-nodes to change limits).*")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Cross-References: which docs mention which DB models
# ─────────────────────────────────────────────

def build_doc_cross_references(repo_root: Path, all_files: list, model_names: list) -> dict:
    """For each known domain model/entity, find which markdown docs mention
    it by name. Pure text search — no interpretation, so it can't hallucinate,
    but it can definitely produce false positives on generic names."""
    if not model_names:
        return {}

    # Skip overly generic/short names that would match too much noise
    candidates = [n for n in model_names if len(n) >= 4]
    patterns = {n: re.compile(r'\b' + re.escape(n) + r'\b') for n in candidates}

    refs = {n: [] for n in candidates}
    doc_files = [f for f in all_files if f["ext"] == ".md"]
    for f in doc_files:
        fpath = repo_root / f["path"]
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(content):
                refs[name].append(f["path"])

    return {n: paths for n, paths in refs.items() if paths}


# ─────────────────────────────────────────────
# Facts: the single normalized representation every graph reduces to
# ─────────────────────────────────────────────

def build_facts(all_files: list, dep_graph: dict, db_graph: dict, call_graph: list,
                 event_graph: dict, db_usage_graph: list) -> list:
    """Reduce every extracted relationship (imports, DB relations, calls,
    events, DB usage, enum values, guard clauses, validation rules) into one
    flat list of Fact triples with provenance. This is purely a reshape —
    no new extraction happens here — but it gives every downstream consumer
    (GraphML, Neo4j, an MCP server, the trace() query below) one consistent
    shape instead of five different graph structures."""
    facts: list[Fact] = []

    for src, targets in dep_graph.items():
        for tgt in targets:
            facts.append(Fact(src, "IMPORTS", tgt, src, extraction_method="import_statement"))

    for e in db_graph.get("edges", []):
        pred = "HAS_MANY" if e["kind"] == "many" else "HAS_ONE"
        facts.append(Fact(e["source"], pred, e["target"], e["source"],
                           extraction_method=f"{e['source_type']}_relation", evidence=e["field"]))

    for e in call_graph:
        facts.append(Fact(e["source"], "CALLS", f"{e['target']}.{e['method']}", e["file"],
                           extraction_method="call_site",
                           evidence=f"this.<injected {e['target']}>.{e['method']}()"))

    for event, sides in event_graph.items():
        for p in sides["producers"]:
            facts.append(Fact(p, "EMITS", event, p, extraction_method="emit_call"))
        for c in sides["consumers"]:
            facts.append(Fact(event, "CONSUMED_BY", c, c, extraction_method="event_listener"))

    for e in db_usage_graph:
        pred = "WRITES" if e["op"] == "write" else "READS"
        facts.append(Fact(e["source"], pred, e["model"], e["source"],
                           extraction_method="prisma_call_site", evidence=e["method"]))

    for f in all_files:
        classes = f.get("classes")
        source = classes[0].split()[0] if classes else Path(f["path"]).stem

        for g in f.get("guard_clauses", []):
            facts.append(Fact(source, "THROWS_IF", g["exception"], f["path"],
                               line=g["line"], extraction_method="guard_clause",
                               evidence=g["condition"]))

        for e in f.get("enum_values", []):
            for v in e["values"]:
                facts.append(Fact(e["name"], "HAS_VALUE", v, f["path"],
                                   extraction_method="ts_enum_declaration"))

        for e in f.get("prisma_enums", []):
            for v in e["values"]:
                facts.append(Fact(e["name"], "HAS_VALUE", v, f["path"],
                                   extraction_method="prisma_enum_declaration"))

        for r in f.get("validation_rules", []):
            for rule in r["rules"]:
                facts.append(Fact(source, "VALIDATES", f"{r['field']}:{rule}", f["path"],
                                   extraction_method="class_validator_decorator"))

    return facts


def export_graphml(facts: list, path: Path) -> None:
    """Write facts as a GraphML file — importable into Gephi, yEd, or as a
    staging step before loading into Neo4j (`neo4j-admin` and most graph
    tools accept GraphML directly)."""
    def esc(s: str) -> str:
        return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    node_ids: dict[str, int] = {}
    for f in facts:
        node_ids.setdefault(f.subject, len(node_ids))
        node_ids.setdefault(f.object, len(node_ids))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
        '  <key id="predicate" for="edge" attr.name="predicate" attr.type="string"/>',
        '  <key id="evidence" for="edge" attr.name="evidence" attr.type="string"/>',
        '  <key id="source_file" for="edge" attr.name="source_file" attr.type="string"/>',
        '  <graph id="G" edgedefault="directed">',
    ]
    for name, nid in node_ids.items():
        lines.append(f'    <node id="n{nid}"><data key="label">{esc(name)}</data></node>')
    for i, f in enumerate(facts):
        lines.append(
            f'    <edge id="e{i}" source="n{node_ids[f.subject]}" target="n{node_ids[f.object]}">'
            f'<data key="predicate">{esc(f.predicate)}</data>'
            f'<data key="evidence">{esc(f.evidence or "")}</data>'
            f'<data key="source_file">{esc(f.source_file)}</data></edge>'
        )
    lines.append('  </graph>')
    lines.append('</graphml>')
    path.write_text("\n".join(lines), encoding="utf-8")


def trace_from(facts: list, start: str, max_depth: int = 3) -> list:
    """BFS over Facts (subject -> object edges) starting at `start`. Returns
    a list of paths (each a list of Facts), so a request/route/class can be
    followed through CALLS/EMITS/READS/WRITES/etc without reading every file
    by hand. This is a query over already-extracted data, not new inference."""
    adjacency: dict[str, list[Fact]] = {}
    for f in facts:
        adjacency.setdefault(f.subject, []).append(f)

    paths = []
    queue = deque([(start, [], {start})])
    while queue:
        node, path_facts, visited = queue.popleft()
        if len(path_facts) >= max_depth:
            continue
        for f in adjacency.get(node, []):
            if f.object in visited:
                continue
            new_path = path_facts + [f]
            paths.append(new_path)
            queue.append((f.object, new_path, visited | {f.object}))
    return paths


def format_trace_paths(start: str, paths: list) -> str:
    if not paths:
        return f"(no outgoing facts found for '{start}' — check the exact class/model name)"
    lines = []
    for p in paths:
        chain = start
        for f in p:
            chain += f" --{f.predicate}--> {f.object}"
        lines.append(chain)
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Markdown Generator
# ─────────────────────────────────────────────

def summarize_module(mod_name: str, mod_files: list, modules: dict, dep_graph: dict) -> list:
    """Auto-generate a one-shot summary of a module's responsibilities purely
    from data already extracted (routes, injected deps, cross-module imports).
    No guessing about *why* — only *what*, derived from structure."""
    lines = []

    # Route count by HTTP verb
    verb_counts = {}
    for f in mod_files:
        for r in f.get("routes", []):
            verb = r.split()[0]
            verb_counts[verb] = verb_counts.get(verb, 0) + 1
    if verb_counts:
        breakdown = ", ".join(f"{v}:{c}" for v, c in sorted(verb_counts.items()))
        lines.append(f"- 🛣️ **Routes:** {sum(verb_counts.values())} total ({breakdown})")

    # Injected dependency types, excluding the module's own services
    own_types = set()
    for f in mod_files:
        for cls in f.get("classes", []):
            own_types.add(cls.split()[0])
    injected_types = set()
    for f in mod_files:
        for inj in f.get("injected", []):
            t = inj.split(":")[-1].strip()
            if t not in own_types:
                injected_types.add(t)
    if injected_types:
        lines.append(f"- 🧩 **Depends on services:** {', '.join(sorted(injected_types))}")

    # Which other modules this module imports from (via resolved dep_graph)
    mod_paths = {f["path"] for f in mod_files}
    other_modules = set()
    for src in mod_paths:
        for tgt in dep_graph.get(src, []):
            parts = Path(tgt).parts
            if "modules" in parts:
                mod_idx = parts.index("modules")
                if len(parts) > mod_idx + 1:
                    other = parts[mod_idx + 1]
                    if other != mod_name:
                        other_modules.add(other)
    if other_modules:
        lines.append(f"- 🔀 **Talks to modules:** {', '.join(sorted(other_modules))}")

    return lines


def render_file_info(f: dict) -> str:
    lines = [f"- `{f['path']}`"]
    if f.get("note") and not (f.get("snippet")):
        lines[0] += f" ⚠️ {f['note']}"
        return lines[0]

    details = []
    if f.get("note"):
        details.append(f"  - ⚠️ {f['note']}")
    if f.get("nestjs"):
        details.append(f"  - 🏷️ NestJS: {', '.join(f['nestjs'])}")
    if f.get("routes"):
        details.append(f"  - 🛣️ Routes: {', '.join(f['routes'])}")
    if f.get("classes"):
        details.append(f"  - 📦 Classes: {', '.join(f['classes'][:3])}")
    if f.get("injected"):
        details.append(f"  - 🧩 Injects: {', '.join(f['injected'])}")
    if f.get("interfaces"):
        details.append(f"  - 🔷 Interfaces: {', '.join(f['interfaces'][:4])}")
    if f.get("enums"):
        details.append(f"  - 🔢 Enums: {', '.join(f['enums'])}")
    if f.get("methods"):
        details.append(f"  - ⚙️ Methods: {', '.join(f['methods'][:8])}")
    if f.get("functions"):
        details.append(f"  - ⚙️ Functions: {', '.join(f['functions'][:8])}")
    if f.get("dto_fields"):
        details.append(f"  - 📋 Fields: {', '.join(f['dto_fields'][:6])}")
    if f.get("validation_rules"):
        rule_strs = [f"{r['field']}({','.join(r['rules'])})" for r in f["validation_rules"][:6]]
        details.append(f"  - ✅ Validation: {', '.join(rule_strs)}")
    if f.get("exports") and not f.get("classes"):
        details.append(f"  - 📤 Exports: {', '.join(f['exports'][:4])}")
    if f.get("arduino"):
        details.append("  - 🔌 Arduino firmware (setup/loop)")
    if f.get("includes"):
        details.append(f"  - 📎 Includes: {', '.join(f['includes'][:5])}")
    if f.get("imports"):
        details.append(f"  - 🔗 Local imports: {', '.join(f['imports'][:6])}")

    return "\n".join([lines[0]] + details)


def generate_markdown(repo_root: Path, all_files: list, dep_graph: dict,
                       db_graph: dict | None = None, max_graph_nodes: int = 120,
                       call_graph: list | None = None, doc_refs: dict | None = None,
                       event_graph: dict | None = None, db_usage_graph: list | None = None) -> str:
    md = []

    # ── Header ──
    md.append(f"# {repo_root.name} — Claude Context")
    md.append(f"\n> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    md.append(f"> Files indexed: {len(all_files)}  ")
    md.append(f"> Repo: {repo_root.name}\n")
    md.append("> **How to use:** Paste this file at the start of a Claude session.")
    md.append("> Claude will understand the full project structure, the module dependency graph,")
    md.append("> and the content of key entry-point files, and can help with any module.\n")
    md.append("---\n")

    # ── README ──
    readme = repo_root / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()[:40]
        md.append("## Project Overview\n")
        md.append("```markdown")
        md.append("\n".join(lines))
        md.append("```\n")

    # ── Package.json ──
    pkg_files = [f for f in all_files if f["path"].endswith("package.json") and f.get("pkg_name")]
    if pkg_files:
        md.append("## Packages\n")
        for pkg in pkg_files:
            md.append(f"### `{pkg['path']}`")
            md.append(f"- Name: `{pkg.get('pkg_name')}` v{pkg.get('pkg_version', '?')}")
            if pkg.get("scripts"):
                md.append(f"- Scripts: `{' | '.join(pkg['scripts'][:8])}`")
            if pkg.get("main_deps"):
                md.append(f"- Dependencies: {', '.join(pkg['main_deps'])}")
            md.append("")

    # ── Prisma Schema ──
    prisma_files = [f for f in all_files if f.get("prisma_models")]
    if prisma_files:
        md.append("## Database Schema (Prisma)\n")
        for pf in prisma_files:
            md.append(f"**File:** `{pf['path']}`\n")
            for model in pf["prisma_models"]:
                md.append(f"### Model: `{model['name']}`")
                shown = model["fields"][:14]
                for field in shown:
                    md.append(f"  - {field}")
                hidden = len(model["fields"]) - len(shown)
                if hidden > 0:
                    md.append(f"  - *(+{hidden} more field(s))*")
            md.append("")

    # ── Database Relationship Graph (Prisma relations + TypeORM decorators) ──
    if db_graph and db_graph.get("edges"):
        md.append("## 🗄️ Database Relationship Graph\n")
        md.append(f"*{len(db_graph['models'])} model(s)/entity(ies), "
                   f"{len(db_graph['edges'])} relationship(s) detected "
                   f"(from Prisma schema and/or TypeORM `@OneToMany`/`@ManyToOne`/etc decorators).*\n")
        er_graph = generate_mermaid_er_graph(db_graph)
        if er_graph:
            md.append(er_graph)
        md.append("")

    # ── Service Call Graph (mechanical: real this.injected.method() calls) ──
    if call_graph:
        md.append("## 🔗 Service Call Graph\n")
        md.append(f"*{len(call_graph)} call site(s) detected — real `this.injected.method()` calls "
                   f"resolved through constructor-injected dependencies. This is structural, not inferred: "
                   f"it shows which class calls which method on which injected service/repository.*\n")
        cg = generate_mermaid_call_graph(call_graph)
        if cg:
            md.append(cg)
        md.append("")

    # ── Event Producer/Consumer Graph (mechanical: literal emit/OnEvent/subscribe) ──
    if event_graph:
        md.append("## 📡 Event Producer/Consumer Graph\n")
        md.append(f"*{len(event_graph)} distinct event/topic name(s) detected from literal "
                   f"`.emit()`/`.publish()`/`@OnEvent()`/`.subscribe()` call sites.*\n")
        eg = generate_mermaid_event_graph(event_graph)
        if eg:
            md.append(eg)
        md.append("")
        for event in sorted(event_graph.keys()):
            sides = event_graph[event]
            md.append(f"- **`{event}`** — produced by: {', '.join(sides['producers']) or '—'} "
                       f"| consumed by: {', '.join(sides['consumers']) or '—'}")
        md.append("")

    # ── Database Usage Graph — who reads/writes which model ──
    if db_usage_graph:
        md.append("## 🗄️ Database Usage Graph (Reads/Writes)\n")
        md.append(f"*{len(db_usage_graph)} `this.prisma.<model>.<method>()` call site(s) resolved "
                   f"to read/write operations against actual models.*\n")
        by_model = {}
        for e in db_usage_graph:
            by_model.setdefault(e["model"], []).append(e)
        for model in sorted(by_model.keys()):
            entries = by_model[model]
            reads = sorted({e["source"] for e in entries if e["op"] == "read"})
            writes = sorted({e["source"] for e in entries if e["op"] == "write"})
            md.append(f"- **`{model}`** — read by: {', '.join(reads) or '—'} "
                       f"| written by: {', '.join(writes) or '—'}")
        md.append("")

    # ── Cross-References: which docs mention which DB models ──
    if doc_refs:
        md.append("## 🔎 Cross-References (Docs ↔ DB Models)\n")
        md.append("*Plain text-match between model/entity names and markdown docs — "
                   "helps locate where a model is discussed.*\n")
        for name in sorted(doc_refs.keys()):
            paths = doc_refs[name]
            md.append(f"- **`{name}`** → {', '.join(f'`{p}`' for p in paths[:6])}"
                       + (f" *(+{len(paths) - 6} more)*" if len(paths) > 6 else ""))
        md.append("")

    # ── Directory Tree ──
    md.append("## Directory Structure\n")
    md.append("```")
    md.append(build_tree(repo_root))
    md.append("```\n")

    # ── Key Entry-Point Files (full/summarized content) ──
    key_files = [f for f in all_files if f.get("is_key")]
    if key_files:
        md.append("## Key Entry-Point Files\n")
        md.append("*Full or head/tail content shown so Claude sees real implementation, not just a summary.*\n")
        for f in key_files:
            md.append(f"### `{f['path']}`")
            lang = "typescript" if f["ext"] in (".ts", ".tsx") else f["ext"].lstrip(".")
            md.append(f"```{lang}")
            md.append(f.get("snippet", ""))
            md.append("```\n")

    # ── Module Dependency Graph ──
    if dep_graph:
        md.append("## Module Dependency Graph\n")
        md.append("*Local (relative) imports resolved between indexed files — use this to trace how modules connect.*\n")
        for src in sorted(dep_graph.keys()):
            targets = dep_graph[src]
            md.append(f"- `{src}` → {', '.join(f'`{t}`' for t in targets)}")
        md.append("")

        md.append("### 🌐 Visual Dependency Graph\n")
        mermaid_dep = generate_mermaid_dependency_graph(dep_graph, max_nodes=max_graph_nodes)
        if mermaid_dep:
            md.append(mermaid_dep)
        md.append("")

    # ── Docs ──
    doc_files = [f for f in all_files if f["ext"] == ".md" and f.get("headings")
                 and ("Docs" in f["path"] or "docs" in f["path"])]
    if doc_files:
        md.append("## Documentation Files\n")
        for f in doc_files[:25]:
            md.append(f"### `{f['path']}`")
            md.append("\n".join(f["headings"]))
            md.append("")

    # ── Backend Modules (NestJS) ──
    module_files = [f for f in all_files if "modules" in f["path"] and f["ext"] == ".ts"]
    modules = {}
    for f in module_files:
        parts = Path(f["path"]).parts
        try:
            mod_idx = list(parts).index("modules")
            mod_name = parts[mod_idx + 1]
            modules.setdefault(mod_name, []).append(f)
        except (ValueError, IndexError):
            pass

    if modules:
        md.append("## Backend Modules (NestJS)\n")
        md.append(f"*{len(modules)} modules found*\n")
        for mod_name in sorted(modules.keys()):
            mod_files = modules[mod_name]
            md.append(f"### `{mod_name}`")
            summary_lines = summarize_module(mod_name, mod_files, modules, dep_graph)
            if summary_lines:
                md.extend(summary_lines)
                md.append("")
            for f in sorted(mod_files, key=lambda x: x["path"]):
                md.append(render_file_info({**f, "path": Path(f["path"]).name}))
            md.append("")

    # ── Python Modules (generic) ──
    py_files = [f for f in all_files if f["ext"] == ".py" and (f.get("classes") or f.get("functions"))]
    if py_files:
        md.append("## Python Modules\n")
        for f in sorted(py_files, key=lambda x: x["path"])[:60]:
            md.append(render_file_info(f))
        md.append("")

    # ── Firmware ──
    fw_files = [f for f in all_files if "firmware" in f["path"].lower()]
    if fw_files:
        md.append("## Firmware\n")
        for f in fw_files:
            md.append(render_file_info(f))
        md.append("")

    # ── Stats ──
    md.append("## Statistics\n")
    by_ext = {}
    for f in all_files:
        by_ext[f["ext"]] = by_ext.get(f["ext"], 0) + 1
    for ext, count in sorted(by_ext.items(), key=lambda x: -x[1])[:10]:
        md.append(f"- `{ext or 'no-ext'}`: {count} files")

    large_files = [f for f in all_files if f.get("note") and "Large" in f.get("note", "")]
    if large_files:
        md.append(f"\n*{len(large_files)} large file(s) were summarized (head/tail) rather than skipped.*")

    md.append("\n---")
    md.append("*Generated by repo-context-indexer.py v3*")

    return "\n".join(md)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Repo Context Indexer v3 — generate CONTEXT.md for Claude")
    parser.add_argument("--repo", required=True, help='Path to repo, e.g. "D:\\path\\to\\SmartCorePlatform"')
    parser.add_argument("--output", default="CONTEXT.md", help="Output filename (default: CONTEXT.md)")
    parser.add_argument("--json", action="store_true", help="Also write a CONTEXT.json with raw structured data")
    parser.add_argument(
        "--include-content", default="",
        help="Comma-separated extra filenames to always include full content for, "
             "e.g. 'main.ts,app.module.ts'"
    )
    parser.add_argument("--max-depth", type=int, default=4, help="Max directory tree depth (default 4)")
    parser.add_argument("--max-graph-nodes", type=int, default=120,
                         help="Max nodes shown in the visual Mermaid dependency graph (default 120)")
    parser.add_argument("--graphml", action="store_true",
                         help="Also write CONTEXT.graphml (all Facts, importable into Neo4j/Gephi/yEd)")
    parser.add_argument("--trace", default=None,
                         help="Query mode: trace outgoing Facts from a class/model/event name "
                              "(e.g. --trace ReservationController) and print the reachable chains, "
                              "then exit without writing any files")
    parser.add_argument("--trace-depth", type=int, default=4,
                         help="Max hops for --trace (default 4)")
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    if not repo_root.exists():
        print(f"❌ Not found: {repo_root}")
        sys.exit(1)

    key_filenames = set(DEFAULT_KEY_FILENAMES)
    if args.include_content:
        key_filenames |= {x.strip() for x in args.include_content.split(",") if x.strip()}

    print(f"📂 Indexing: {repo_root}")

    all_files = []
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            info = analyze_file(fpath, repo_root, key_filenames)
            if info:
                all_files.append(info)

    print(f"✅ Indexed {len(all_files)} files")

    dep_graph = build_dependency_graph(all_files)
    print(f"🔗 Resolved {len(dep_graph)} files with local dependency links")

    db_graph = build_db_graph(all_files)
    if db_graph["edges"]:
        print(f"🗄️  Found {len(db_graph['models'])} DB model(s) with {len(db_graph['edges'])} relationship(s)")

    call_graph = build_call_graph(all_files)
    if call_graph:
        print(f"🔗 Traced {len(call_graph)} service call site(s)")

    doc_refs = build_doc_cross_references(repo_root, all_files, db_graph["models"])
    if doc_refs:
        print(f"📚 Cross-referenced {len(doc_refs)} model(s) against documentation")

    event_graph = build_event_graph(all_files)
    if event_graph:
        print(f"📡 Found {len(event_graph)} distinct event/topic name(s)")

    db_usage_graph = build_db_usage_graph(all_files, db_graph["models"])
    if db_usage_graph:
        print(f"🗄️  Traced {len(db_usage_graph)} DB read/write call site(s)")

    facts = build_facts(all_files, dep_graph, db_graph, call_graph, event_graph, db_usage_graph)
    print(f"🧬 Built {len(facts)} Fact(s) (unified subject-predicate-object triples)")

    if args.trace:
        paths = trace_from(facts, args.trace, max_depth=args.trace_depth)
        print(f"\n🔎 Trace from '{args.trace}' (max depth {args.trace_depth}):\n")
        print(format_trace_paths(args.trace, paths))
        return

    markdown = generate_markdown(repo_root, all_files, dep_graph, db_graph, args.max_graph_nodes,
                                  call_graph, doc_refs, event_graph, db_usage_graph)

    out = Path(args.output)
    out.write_text(markdown, encoding="utf-8")
    size = out.stat().st_size / 1024
    print(f"📄 Output: {out} ({size:.1f} KB)")

    if size > 300:
        print(f"⚠️  File is {size:.0f}KB — consider splitting by module if Claude struggles")

    if args.graphml:
        graphml_out = out.with_suffix(".graphml")
        export_graphml(facts, graphml_out)
        print(f"📄 Also wrote: {graphml_out}")

    if args.json:
        json_out = out.with_suffix(".json")
        # Strip large snippets from JSON to keep it lean; markdown already has them.
        slim_files = [{k: v for k, v in f.items() if k != "snippet"} for f in all_files]
        json_out.write_text(
            json.dumps(
                {
                    "files": slim_files, "dependency_graph": dep_graph, "db_graph": db_graph,
                    "call_graph": call_graph, "doc_cross_references": doc_refs,
                    "event_graph": event_graph, "db_usage_graph": db_usage_graph,
                    "facts": [asdict(f) for f in facts]
                },
                indent=2
            ),
            encoding="utf-8"
        )
        print(f"📄 Also wrote: {json_out}")


if __name__ == "__main__":
    main()
