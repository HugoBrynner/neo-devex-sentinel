from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

TYPE_RE = re.compile(
    r"\bpublic\s+(?:(?:abstract|sealed|static|partial|readonly)\s+)*"
    r"(?P<kind>class|interface|enum|record|struct)\s+"
    r"(?P<name>[A-Za-z_]\w*)(?:\s*<[^>{}]+>)?"
)
METHOD_RE = re.compile(
    r"\bpublic\s+(?:(?:static|virtual|override|abstract|sealed|new|extern|async|partial)\s+)*"
    r"(?P<ret>[A-Za-z_][\w<>,.\[\]?\s]*)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*\((?P<params>[^)]*)\)"
)
TARGET_RE = re.compile(r"^net(?P<major>\d+)(?:\.(?P<minor>\d+))?", re.I)

GENERIC_TOKENS = {
    "neo", "smart", "contract", "framework", "token", "base", "class", "service",
    "services", "native", "management", "state"
}

@dataclass(frozen=True)
class ApiSymbol:
    kind: str
    name: str
    signature: str
    path: str

@dataclass
class Change:
    kind: str
    symbol: str
    path: str
    before: str | None = None
    after: str | None = None
    severity: str = "medium"
    docs_exact: list[str] | None = None
    docs_related: list[str] | None = None
    note: str | None = None

    def to_dict(self):
        return asdict(self)


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def public_api(root: Path) -> dict[tuple[str, str], ApiSymbol]:
    api: dict[tuple[str, str], ApiSymbol] = {}
    for path in root.rglob("*.cs"):
        text = _read(path)
        rel = str(path.relative_to(root)).replace("\\", "/")
        for m in TYPE_RE.finditer(text):
            sym = ApiSymbol("type", m.group("name"), _norm_ws(m.group(0)), rel)
            api[("type", sym.name)] = sym
        for m in METHOD_RE.finditer(text):
            # Constructors are handled as methods only if they include a return type; regex naturally excludes most.
            ret = _norm_ws(m.group("ret"))
            params = _norm_ws(m.group("params"))
            sig = f"{ret} {m.group('name')}({params})"
            key = ("method", f"{m.group('name')}({params})")
            api[key] = ApiSymbol("method", m.group("name"), sig, rel)
    return api


def target_frameworks(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in root.rglob("*.csproj"):
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue
        found = None
        for elem in tree.iter():
            if elem.tag.split("}")[-1] == "TargetFramework" and elem.text:
                found = elem.text.strip()
                break
        if found:
            rel = str(path.relative_to(root)).replace("\\", "/")
            out[rel] = found
    return out


def _camel_tokens(name: str) -> list[str]:
    parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\b)|[A-Z]?[a-z]+|\d+", name)
    return [p.lower() for p in parts if len(p) >= 3 and p.lower() not in GENERIC_TOKENS]


def _docs_index(docs_root: Path) -> dict[str, str]:
    idx = {}
    for ext in ("*.md", "*.mdx", "*.rst", "*.txt"):
        for p in docs_root.rglob(ext):
            rel = str(p.relative_to(docs_root)).replace("\\", "/")
            idx[rel] = _read(p)
    return idx


def _map_symbol(symbol: str, docs: dict[str, str]) -> tuple[list[str], list[str]]:
    exact, related = [], []
    rx = re.compile(rf"\b{re.escape(symbol)}\b", re.I)
    tokens = _camel_tokens(symbol)
    for path, text in docs.items():
        if rx.search(text):
            exact.append(path)
            continue
        lower = text.lower()
        token_hits = sum(1 for t in tokens if t in lower)
        if tokens and (token_hits >= min(2, len(tokens)) or (len(tokens) == 1 and token_hits == 1)):
            related.append(path)
    return sorted(exact), sorted(related)


def _framework_major(tf: str) -> int | None:
    m = TARGET_RE.match(tf)
    return int(m.group("major")) if m else None


def _doc_net_majors(text: str) -> set[int]:
    majors: set[int] = set()
    for rx in (
        re.compile(r"\bnet(?P<m>\d+)(?:\.0)?\b", re.I),
        re.compile(r"\.NET(?:\s+Core)?\s*(?P<m>\d+)(?:\.0)?\b", re.I),
    ):
        for m in rx.finditer(text):
            majors.add(int(m.group("m")))
    return majors


def _map_framework(old_tf: str, new_tf: str, docs: dict[str, str]) -> tuple[list[str], list[str]]:
    old_major, new_major = _framework_major(old_tf), _framework_major(new_tf)
    exact, related = [], []
    if old_major is None or new_major is None:
        return exact, related
    for path, text in docs.items():
        majors = _doc_net_majors(text)
        if not majors:
            continue
        # A release can outrun docs by more than one major. Flag pages that mention
        # an older runtime but do not mention the new target at all. This is an
        # impact signal (review required), not an assertion that historical docs are wrong.
        if new_major not in majors and any(m < new_major for m in majors):
            exact.append(path)
        elif old_major in majors:
            related.append(path)
    return sorted(exact), sorted(related)


def scan(old_root: Path, new_root: Path, docs_root: Path, old_label: str = "old", new_label: str = "new") -> dict:
    old_root, new_root, docs_root = map(Path, (old_root, new_root, docs_root))
    docs = _docs_index(docs_root)
    changes: list[Change] = []

    old_tf = target_frameworks(old_root)
    new_tf = target_frameworks(new_root)
    for path in sorted(set(old_tf) & set(new_tf)):
        if old_tf[path] != new_tf[path]:
            exact, related = _map_framework(old_tf[path], new_tf[path], docs)
            changes.append(Change(
                kind="target_framework_changed",
                symbol=Path(path).stem,
                path=path,
                before=old_tf[path], after=new_tf[path], severity="high",
                docs_exact=exact, docs_related=related,
                note="Runtime/framework requirement changed; docs mentioning the old runtime require review."
            ))

    old_api, new_api = public_api(old_root), public_api(new_root)
    old_types = {k: v for k, v in old_api.items() if k[0] == "type"}
    new_types = {k: v for k, v in new_api.items() if k[0] == "type"}

    for key in sorted(set(new_types) - set(old_types)):
        sym = new_types[key]
        exact, related = _map_symbol(sym.name, docs)
        sev = "low" if exact else "medium"
        changes.append(Change("public_type_added", sym.name, sym.path, after=sym.signature,
                              severity=sev, docs_exact=exact, docs_related=related,
                              note="New public API surface; documentation coverage should be reviewed."))

    for key in sorted(set(old_types) - set(new_types)):
        sym = old_types[key]
        exact, related = _map_symbol(sym.name, docs)
        changes.append(Change("public_type_removed", sym.name, sym.path, before=sym.signature,
                              severity="high", docs_exact=exact, docs_related=related,
                              note="Removed public type may leave stale documentation/examples."))

    old_methods = {k: v for k, v in old_api.items() if k[0] == "method"}
    new_methods = {k: v for k, v in new_api.items() if k[0] == "method"}
    old_by_name: dict[str, list[ApiSymbol]] = {}
    new_by_name: dict[str, list[ApiSymbol]] = {}
    for sym in old_methods.values(): old_by_name.setdefault(sym.name, []).append(sym)
    for sym in new_methods.values(): new_by_name.setdefault(sym.name, []).append(sym)

    handled_old: set[tuple[str, str]] = set()
    handled_new: set[tuple[str, str]] = set()
    for name in sorted(set(old_by_name) & set(new_by_name)):
        old_sigs = {s.signature: s for s in old_by_name[name]}
        new_sigs = {s.signature: s for s in new_by_name[name]}
        removed = [s for sig, s in old_sigs.items() if sig not in new_sigs]
        added = [s for sig, s in new_sigs.items() if sig not in old_sigs]
        if len(removed) == 1 and len(added) == 1:
            before, after = removed[0], added[0]
            exact, related = _map_symbol(name, docs)
            changes.append(Change("public_method_signature_changed", name, after.path,
                                  before=before.signature, after=after.signature, severity="high",
                                  docs_exact=exact, docs_related=related,
                                  note="Public method signature changed; examples and API docs may no longer compile."))
            handled_old.add(("method", f"{before.name}({before.signature.split('(',1)[1]}"))
            handled_new.add(("method", f"{after.name}({after.signature.split('(',1)[1]}"))

    for key in sorted(set(new_methods) - set(old_methods)):
        if key in handled_new:
            continue
        sym = new_methods[key]
        exact, related = _map_symbol(sym.name, docs)
        changes.append(Change("public_method_added", sym.name, sym.path, after=sym.signature,
                              severity="low" if exact else "medium", docs_exact=exact, docs_related=related))
    for key in sorted(set(old_methods) - set(new_methods)):
        if key in handled_old:
            continue
        sym = old_methods[key]
        exact, related = _map_symbol(sym.name, docs)
        changes.append(Change("public_method_removed", sym.name, sym.path, before=sym.signature,
                              severity="high", docs_exact=exact, docs_related=related))

    counts = {"high": 0, "medium": 0, "low": 0}
    for c in changes:
        counts[c.severity] = counts.get(c.severity, 0) + 1
    return {
        "tool": "Neo DevEx Sentinel",
        "version": "0.1.0",
        "old_label": old_label,
        "new_label": new_label,
        "summary": {"total_changes": len(changes), **counts},
        "changes": [c.to_dict() for c in changes],
    }


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        "# Neo DevEx Sentinel — Release Impact Report",
        "",
        f"**Release:** `{report['old_label']}` → `{report['new_label']}`",
        "",
        f"**Detected:** {s['total_changes']} developer-facing changes — {s['high']} high / {s['medium']} medium / {s['low']} low",
        "",
    ]
    if not report["changes"]:
        lines.append("No developer-facing changes detected by v0.1 rules.")
        return "\n".join(lines) + "\n"
    for c in report["changes"]:
        lines += [f"## {c['severity'].upper()} — {c['kind']} — `{c['symbol']}`", ""]
        lines.append(f"Source: `{c['path']}`")
        if c.get("before") is not None:
            lines.append(f"- Before: `{c['before']}`")
        if c.get("after") is not None:
            lines.append(f"- After: `{c['after']}`")
        exact = c.get("docs_exact") or []
        related = c.get("docs_related") or []
        lines.append(f"- Exact docs hits: {', '.join(f'`{p}`' for p in exact) if exact else 'none'}")
        lines.append(f"- Related docs hits: {', '.join(f'`{p}`' for p in related) if related else 'none'}")
        if c.get("note"):
            lines.append(f"- Note: {c['note']}")
        lines.append("")
    return "\n".join(lines)


def write_report(report: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "release-impact.json"
    md_path = out_dir / "release-impact.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, md_path
