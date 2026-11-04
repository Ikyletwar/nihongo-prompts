#!/usr/bin/env python3
"""Buat paket ZIP berisi sejumlah prompt acak dari data lokal promptvault-clone.

Contoh:
  python3 tools/pack_prompts.py --list
  python3 tools/pack_prompts.py --category DeepSeek --count 10
  python3 tools/pack_prompts.py --category Gemini --count 25 --seed 42 --out /tmp/gemini-25.zip
  python3 tools/pack_prompts.py --category Grok --count 10 --combined
"""

import argparse
import csv
import io
import json
import random
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "pv-data.js"


def load_data(path: Path = DATA_FILE) -> dict:
    src = path.read_text(encoding="utf-8")
    match = re.search(r"window\.__PV_DATA__\s*=\s*(\{.*\})\s*;?\s*$", src, re.S)
    if not match:
        raise SystemExit(f"Format data tidak dikenali: {path}")
    return json.loads(match.group(1))


def safe_name(text: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip()).strip("._")
    return text[:80] or fallback


def category_index(data: dict) -> dict:
    return {c["name"].strip().lower(): c for c in data.get("categories", [])}


def prompts_for_category(data: dict, category_name: str) -> list[dict]:
    cat = category_index(data).get(category_name.strip().lower())
    if cat is None:
        available = ", ".join(c["name"] for c in data.get("categories", []))
        raise SystemExit(f"Kategori '{category_name}' tidak ada. Tersedia: {available}")

    prompt_by_id = {p["id"]: p for p in data.get("prompts", [])}
    prompt_cats = {}
    for rel in data.get("prompt_categories", []):
        prompt_cats.setdefault(rel["prompt_id"], []).append(rel["category_id"])

    selected = []
    for pid, cat_ids in prompt_cats.items():
        if cat["id"] in cat_ids and pid in prompt_by_id:
            p = dict(prompt_by_id[pid])
            p["_category"] = cat["name"]
            p["_category_count"] = len(prompt_cats.get(pid, []))
            selected.append(p)
    return selected


def build_zip(prompts: list[dict], out_path: Path, title: str, combined: bool, include_manifest: bool) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        if combined:
            buf = io.StringIO()
            for i, p in enumerate(prompts, 1):
                buf.write(f"===== {i:03d}. {p.get('title', 'Untitled')} =====\n")
                buf.write(p.get("content", "").rstrip() + "\n\n")
            zf.writestr("prompts.txt", buf.getvalue())
        else:
            for i, p in enumerate(prompts, 1):
                filename = f"{i:03d}_{safe_name(p.get('title', 'untitled'), p['id'][:8])}.txt"
                zf.writestr(filename, p.get("content", "").rstrip() + "\n")

        if include_manifest:
            manifest = io.StringIO()
            writer = csv.writer(manifest)
            writer.writerow(["index", "id", "title", "category", "characters"])
            for i, p in enumerate(prompts, 1):
                writer.writerow([
                    i,
                    p.get("id", ""),
                    p.get("title", ""),
                    p.get("_category", ""),
                    len(p.get("content", "")),
                ])
            zf.writestr("manifest.csv", manifest.getvalue())
            zf.writestr("info.json", json.dumps({
                "title": title,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "count": len(prompts),
                "source": "promptvault-clone (local data/pv-data.js)",
            }, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Paket prompt acak ke ZIP")
    parser.add_argument("--list", action="store_true", help="Tampilkan kategori dan jumlah prompt")
    parser.add_argument("--category", help="Nama kategori, contoh: DeepSeek")
    parser.add_argument("--count", type=int, help="Jumlah prompt yang diambil")
    parser.add_argument("--seed", type=int, default=None, help="Seed agar hasil acak bisa direproduksi")
    parser.add_argument("--out", type=Path, default=None, help="Path output .zip")
    parser.add_argument("--combined", action="store_true", help="Gabungkan semua prompt ke satu prompts.txt")
    parser.add_argument("--no-manifest", action="store_true", help="Jangan sertakan manifest.csv dan info.json")
    args = parser.parse_args()

    data = load_data()

    if args.list:
        counts = {c["id"]: 0 for c in data["categories"]}
        for rel in data.get("prompt_categories", []):
            if rel["category_id"] in counts:
                counts[rel["category_id"]] += 1
        for c in sorted(data["categories"], key=lambda x: x["name"].lower()):
            print(f"{c['name']:<20} {counts[c['id']]}")
        return 0

    if not args.category or args.count is None:
        parser.error("--category dan --count wajib, atau gunakan --list")

    pool = prompts_for_category(data, args.category)
    if not pool:
        raise SystemExit(f"Kategori '{args.category}' tidak punya prompt")
    if args.count < 1:
        raise SystemExit("--count minimal 1")
    if args.count > len(pool):
        raise SystemExit(f"Diminta {args.count}, tersedia {len(pool)} di kategori '{args.category}'")

    rng = random.Random(args.seed)
    selected = rng.sample(pool, args.count)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = args.out or Path(f"prompt-pack_{safe_name(args.category, 'pack')}_{args.count}_{stamp}.zip")
    build_zip(selected, out_path, f"{args.category} — {args.count} prompt", args.combined, not args.no_manifest)
    print(f"OK: {out_path} ({args.count} prompt dari kategori {args.category}, pool {len(pool)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
