#!/usr/bin/env python3
"""Mode interaktif: pilih kategori, tentukan jumlah, lalu buat ZIP prompt acak."""

import random
import sys
from datetime import datetime
from pathlib import Path

from pack_prompts import (
    build_zip,
    load_data,
    prompts_for_category,
    safe_name,
)

ROOT = Path(__file__).resolve().parent.parent


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    if not value and default is not None:
        return default
    return value


def print_categories(data: dict) -> list[dict]:
    counts = {c["id"]: 0 for c in data["categories"]}
    for rel in data.get("prompt_categories", []):
        if rel["category_id"] in counts:
            counts[rel["category_id"]] += 1

    cats = sorted(data["categories"], key=lambda c: c["name"].lower())
    print("\nDaftar kategori:\n")
    for i, c in enumerate(cats, 1):
        print(f"  {i:2d}. {c['name']:<20} {counts[c['id']]} prompt")
    print()
    return cats


def pick_category(cats: list[dict]) -> dict:
    while True:
        raw = ask("Pilih kategori (nomor atau nama)").strip()
        if not raw:
            continue
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(cats):
                return cats[idx - 1]
            print(f"Nomor harus 1-{len(cats)}.")
            continue
        matches = [c for c in cats if c["name"].lower() == raw.lower()]
        if matches:
            return matches[0]
        matches = [c for c in cats if raw.lower() in c["name"].lower()]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            print("Terlalu umum, pilih salah satu:", ", ".join(c["name"] for c in matches))
            continue
        print("Kategori tidak ditemukan.")


def pick_count(max_count: int) -> int:
    while True:
        raw = ask(f"Mau berapa prompt? (1-{max_count})").strip()
        try:
            count = int(raw)
        except ValueError:
            print("Masukkan angka.")
            continue
        if 1 <= count <= max_count:
            return count
        print(f"Jumlah harus 1 sampai {max_count}.")


def main() -> int:
    data = load_data()
    cats = print_categories(data)
    category = pick_category(cats)

    pool = prompts_for_category(data, category["name"])
    if not pool:
        print(f"Kategori {category['name']} belum punya prompt.")
        return 1

    print(f"Kategori dipilih: {category['name']} ({len(pool)} prompt tersedia)\n")
    count = pick_count(len(pool))

    seed_raw = ask("Pakai seed? (kosongkan untuk acak penuh)", "").strip()
    seed = int(seed_raw) if seed_raw.isdigit() else None

    default_out = f"prompt-pack_{safe_name(category['name'], 'pack')}_{count}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"
    out_raw = ask("Nama file output", default_out).strip()
    out_path = Path(out_raw)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    combined = ask("Gabung satu file prompts.txt? (y/N)", "N").lower().startswith("y")
    include_manifest = not ask("Sertakan manifest.csv? (Y/n)", "Y").lower().startswith("n")

    print("\nRingkasan:")
    print(f"  Kategori : {category['name']}")
    print(f"  Jumlah   : {count}")
    print(f"  Seed     : {seed if seed is not None else 'acak'}")
    print(f"  Output   : {out_path}")
    confirm = ask("Lanjutkan? (Y/n)", "Y").lower()
    if confirm.startswith("n"):
        print("Dibatalkan.")
        return 0

    selected = random.Random(seed).sample(pool, count)
    build_zip(selected, out_path, f"{category['name']} — {count} prompt", combined, include_manifest)
    print(f"\nOK: {out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nDibatalkan.")
        raise SystemExit(130)
