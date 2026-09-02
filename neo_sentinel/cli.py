from __future__ import annotations
import argparse
from pathlib import Path
from .core import scan, write_report


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="neo-sentinel", description="Compare Neo developer-tooling snapshots and map changes to docs")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("scan", help="scan two local source snapshots")
    s.add_argument("--old", required=True, type=Path)
    s.add_argument("--new", required=True, type=Path)
    s.add_argument("--docs", required=True, type=Path)
    s.add_argument("--old-label", default="old")
    s.add_argument("--new-label", default="new")
    s.add_argument("--out", required=True, type=Path)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    report = scan(args.old, args.new, args.docs, args.old_label, args.new_label)
    json_path, md_path = write_report(report, args.out)
    s = report["summary"]
    print(f"Neo DevEx Sentinel {report['version']}")
    print(f"{report['old_label']} -> {report['new_label']}")
    print(f"changes={s['total_changes']} high={s['high']} medium={s['medium']} low={s['low']}")
    print(md_path)
    print(json_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
