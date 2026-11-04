#!/usr/bin/env python3
# Prompt Packer — ambil prompt dari data/pv-data.js, pilih kategori & jumlah,
# ambil acak, lalu kemas jadi .zip siap kirim ke customer.
#
# Pakai:
#   python3 tools/prompt_packer.py --kategori DeepSeek --jumlah 10
#   python3 tools/prompt_packer.py --kategori "Le Chat (Mistral)" --jumlah 5 --urut panjang
#   python3 tools/prompt_packer.py --kategori Semua --jumlah 25 --seed 42
#   python3 tools/prompt_packer.py --list

import argparse
import json
import random
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "pv-data.js"


def load_data():
    src = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(r"window\.__PV_DATA__\s*=\s*(\{.*\});?\s*$", src, re.S)
    if not m:
        sys.exit("Gagal parse data/pv-data.js")
    d = json.loads(m.group(1))
    cat_by_id = {c["id"]: c for c in d["categories"]}
    # map prompt -> daftar kategori
    cats_of = {}
    for r in d["prompt_categories"]:
        cats_of.setdefault(r["prompt_id"], []).append(cat_by_id[r["category_id"]]["name"])
    return d, cats_of


def normalize(name, categories):
    names = {c["name"]: c["name"].lower() for c in categories}
    if name.lower() == "semua":
        return "Semua"
    low = name.lower()
    for n, l in names.items():
        if l == low:
            return n
    # substring match kalau tidak persis sama
    cands = [n for n, l in names.items() if low in l]
    if len(cands) == 1:
        return cands[0]
    sys.exit(f"Kategori '{name}' tidak ditemukan / ambigu. Lihat pilihan dengan --list")


def main():
    ap = argparse.ArgumentParser(description="Packer prompt acak per kategori")
    ap.add_argument("--kategori", "-k", help="nama kategori, atau 'Semua'")
    ap.add_argument("--jumlah", "-j", type=int, default=10, help="jumlah prompt")
    ap.add_argument("--out", "-o", help="nama zip keluaran")
    ap.add_argument("--urut", choices=["judul", "panjang", "acak"], default="acak")
    ap.add_argument("--seed", type=int, help="seed random (agar hasil bisa diulang)")
    ap.add_argument("--list", action="store_true", help="daftar kategori & jumlah promptnya")
    ap.add_argument("--flat", action="store_true", help="taruh semua file langsung di root zip")
    args = ap.parse_args()

    d, cats_of = load_data()
    cats = d["categories"]

    if args.list:
        cat_by_id = {c["id"]: c for c in d["categories"]}
        counts = {}
        for r in d["prompt_categories"]:
            counts[cat_by_id[r["category_id"]]["name"]] = counts.get(cat_by_id[r["category_id"]]["name"], 0) + 1
        per_prompt = {}
        for r in d["prompt_categories"]:
            per_prompt[r["prompt_id"]] = per_prompt.get(r["prompt_id"], 0) + 1
        total = len(d["prompts"])
        print(f"{'KATEGORI':<22}{'PROMPT':>7}")
        for c in sorted(cats, key=lambda x: x["name"].lower()):
            print(f"{c['name']:<22}{counts.get(c['name'], 0):>7}")
        print(f"{'(total prompt unik)':<22}{total:>7}")
        return

    if not args.kategori:
        ap.error("--kategori wajib (atau pakai --list untuk melihat pilihan)")

    kat = normalize(args.kategori, cats)
    if kat == "Semua":
        pool = list(d["prompts"])
    else:
        sel = {c["id"] for c in cats if c["name"] == kat}
        ids = {r["prompt_id"] for r in d["prompt_categories"] if r["category_id"] in sel}
        pool = [p for p in d["prompts"] if p["id"] in ids]

    if not pool:
        sys.exit(f"Kategori '{kat}' kosong.")

    rng = random.Random(args.seed)
    sample = pool if len(pool) <= args.jumlah else rng.sample(pool, args.jumlah)
    if len(pool) < args.jumlah:
        print(f"Peringatan: hanya {len(pool)} prompt tersedia di '{kat}', ambil semua.",
              file=sys.stderr)

    if args.urut == "judul":
        sample.sort(key=lambda p: p["title"].lower())
    elif args.urut == "panjang":
        sample.sort(key=lambda p: len(p["content"]), reverse=True)

    out = Path(args.out) if args.out else Path(
        f"pack-{kat.lower().replace(' ', '-').replace('(', '').replace(')', '')}"
        f"{'-' + str(args.jumlah) if args.jumlah != 10 else ''}"
        f"-{datetime.now():%Y%m%d-%H%M%S}.zip")

    subdir = "" if args.flat else "prompts/"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        manifest = ["Daftar isi pack:", ""]
        for i, p in enumerate(sample, 1):
            safe = re.sub(r'[^\w\-]+', '-', p["title"]).strip('-').lower()[:40] or f"prompt-{i}"
            fname = f"{i:02d}-{safe}.txt"
            content = (f"Judul    : {p['title']}\n"
                       f"Kategori : {', '.join(sorted(cats_of.get(p['id'], ['Umum'])))}\n"
                       f"Panjang  : {len(p['content'])} karakter\n\n"
                       f"=== PROMPT ===\n\n{p['content']}\n")
            z.writestr(f"{subdir}{fname}", content)
            manifest.append(f"{i:>2}. {fname}")
            manifest.append(f"    {p['title']}")
        z.writestr(f"{subdir}DAFTAR-ISI.txt", "\n".join(manifest) + "\n")
        z.writestr("README-pemberian.txt",
                   f"Pack: {len(sample)} prompt ({kat}) untuk customer\n"
                   f"Dibuat: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
                   f"Sumber: koleksi Nihongo\n")

    print(f"OK -> {out} ({len(sample)} prompt, kategori '{kat}')")


if __name__ == "__main__":
    main()
