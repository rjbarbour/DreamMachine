#!/usr/bin/env python3
"""Maintain the reference manifest and the local cache of source material.

The manifest (references/manifest.jsonl) is committed. It has one JSON record per
source: bibliographic identifiers, the URL that was opened, whether we actually
opened it, what we use it for, and, when a copy was downloaded, its SHA-256.

Raw copies live in references/cache/, which is git-ignored because most of the
material is copyrighted. `fetch` rebuilds the cache from the manifest and `verify`
checks that cached files still match their recorded checksums.

Usage:
    python scripts/refs.py list
    python scripts/refs.py import FILE.jsonl --report NAME
    python scripts/refs.py fetch [--key KEY]
    python scripts/refs.py verify

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "references" / "manifest.jsonl"
CACHE = ROOT / "references" / "cache"

FIELDS = [
    "key", "type", "title", "authors", "year", "venue", "doi", "pmid", "url",
    "open_access", "licence", "opened", "used_for", "source_report", "added",
    "fetch_url", "local_file", "sha256", "bytes", "retrieved",
]
DEFAULTS = {
    "type": "paper", "title": "", "authors": "", "year": "", "venue": "", "doi": "",
    "pmid": "", "url": "", "open_access": "unknown", "licence": "", "opened": False,
    "used_for": "", "source_report": "", "added": "", "fetch_url": "",
    "local_file": "", "sha256": "", "bytes": 0, "retrieved": "",
}


def load() -> list[dict]:
    if not MANIFEST.exists():
        return []
    return [json.loads(line) for line in MANIFEST.read_text().splitlines() if line.strip()]


def save(records: list[dict]) -> None:
    records = sorted(records, key=lambda r: r["key"])
    lines = [json.dumps({k: r.get(k, DEFAULTS.get(k, "")) for k in FIELDS}, ensure_ascii=False)
             for r in records]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text("\n".join(lines) + "\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def same_source(a: dict, b: dict) -> bool:
    """Two records describe the same source if they share a key, DOI, PMID or URL."""
    for field in ("key", "doi", "pmid", "url"):
        if a.get(field) and str(a.get(field)).lower() == str(b.get(field, "")).lower():
            return True
    return False


def cmd_import(args: argparse.Namespace) -> int:
    records = load()
    today = dt.date.today().isoformat()
    added = merged = bad = 0
    for n, line in enumerate(Path(args.file).read_text().splitlines(), 1):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            new = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"line {n}: not valid JSON ({exc})", file=sys.stderr)
            bad += 1
            continue
        if not new.get("key"):
            print(f"line {n}: no key, skipped", file=sys.stderr)
            bad += 1
            continue
        new = {k: v for k, v in new.items() if k in FIELDS}
        existing = next((r for r in records if same_source(r, new)), None)
        if existing is None:
            rec = {**DEFAULTS, **new, "source_report": args.report, "added": today}
            records.append(rec)
            added += 1
        else:
            # Keep what we have; fill gaps; a source opened by anyone counts as opened.
            for k, v in new.items():
                if k == "key":
                    continue
                if existing.get(k) in ("", None, "unknown", 0) and v not in ("", None):
                    existing[k] = v
            existing["opened"] = bool(existing.get("opened")) or bool(new.get("opened"))
            if args.report not in existing.get("source_report", ""):
                existing["source_report"] = ", ".join(
                    x for x in (existing.get("source_report", ""), args.report) if x)
            merged += 1
    save(records)
    print(f"imported from {args.file}: {added} added, {merged} merged, {bad} rejected; "
          f"manifest now has {len(records)} records")
    return 1 if bad else 0


def cmd_fetch(args: argparse.Namespace) -> int:
    records = load()
    failures = 0
    for rec in records:
        if args.key and rec["key"] != args.key:
            continue
        if not rec.get("fetch_url") or not rec.get("local_file"):
            continue
        dest = CACHE / rec["local_file"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["curl", "-sS", "-L", "--fail", "-m", "120", "-A", "Mozilla/5.0",
             "-o", str(dest), rec["fetch_url"]],
            capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FAILED  {rec['key']}: {result.stderr.strip()}")
            failures += 1
            continue
        digest = sha256(dest)
        if rec.get("sha256") and rec["sha256"] != digest:
            print(f"CHANGED {rec['key']}: content differs from the recorded checksum "
                  f"(was {rec['sha256'][:12]}, now {digest[:12]}); manifest left unchanged")
            failures += 1
            continue
        if not rec.get("sha256"):
            rec["sha256"] = digest
            rec["bytes"] = dest.stat().st_size
            rec["retrieved"] = dt.date.today().isoformat()
        print(f"ok      {rec['key']} -> references/cache/{rec['local_file']}")
    save(records)
    return 1 if failures else 0


def cmd_verify(args: argparse.Namespace) -> int:
    problems = 0
    for rec in load():
        if not rec.get("local_file"):
            continue
        path = CACHE / rec["local_file"]
        if not path.exists():
            print(f"missing  {rec['key']} (run: python scripts/refs.py fetch --key {rec['key']})")
            problems += 1
        elif sha256(path) != rec.get("sha256"):
            print(f"MISMATCH {rec['key']}")
            problems += 1
        else:
            print(f"ok       {rec['key']}")
    return 1 if problems else 0


def cmd_list(args: argparse.Namespace) -> int:
    records = load()
    for rec in records:
        flags = ("opened" if rec.get("opened") else "UNVERIFIED") + (
            ", cached" if rec.get("sha256") else "")
        ident = rec.get("doi") or (f"PMID {rec['pmid']}" if rec.get("pmid") else rec.get("url", ""))
        print(f"{rec['key']:<34} {str(rec.get('year', '')):<5} {flags:<18} {ident}")
    opened = sum(1 for r in records if r.get("opened"))
    print(f"\n{len(records)} sources, {opened} opened, {len(records) - opened} unverified, "
          f"{sum(1 for r in records if r.get('sha256'))} with a cached copy")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(func=cmd_list)
    p = sub.add_parser("import")
    p.add_argument("file")
    p.add_argument("--report", required=True, help="name of the notes file these sources came from")
    p.set_defaults(func=cmd_import)
    p = sub.add_parser("fetch")
    p.add_argument("--key")
    p.set_defaults(func=cmd_fetch)
    sub.add_parser("verify").set_defaults(func=cmd_verify)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
