# Nihongo — Koleksi Prompt AI

Situs statis untuk menjelajahi, mencari, dan menyalin kumpulan prompt AI. Dibuat dan dikurasi oleh **Nihongo**, siswa **XI TJKT, SMK Negeri 1 Maluku Tengah**.

Seluruh situs berjalan offline: tidak ada backend, tidak ada panggilan jaringan, tidak ada API key, tidak ada analitik. Data prompt disimpan di satu berkas JavaScript yang dimuat langsung oleh peramban, sehingga halaman bisa dibuka dari `file://` tanpa server sama sekali.

![prompt](https://img.shields.io/badge/prompt-183-6366f1?style=flat-square)
![kategori](https://img.shields.io/badge/kategori-15-ec4899?style=flat-square)
![relasi](https://img.shields.io/badge/relasi-330-10b981?style=flat-square)
![ukuran data](https://img.shields.io/badge/data-3%2C0%20MB-f59e0b?style=flat-square)
![dependensi](https://img.shields.io/badge/dependensi-0-8b5cf6?style=flat-square)
![mode](https://img.shields.io/badge/mode-offline-0ea5e9?style=flat-square)

---

## Daftar Isi

- [Ringkasan](#ringkasan)
- [Pratinjau antarmuka](#pratinjau-antarmuka)
- [Fitur](#fitur)
- [Statistik koleksi](#statistik-koleksi)
- [Menjalankan](#menjalankan)
- [Panduan antarmuka](#panduan-antarmuka)
- [Struktur repositori](#struktur-repositori)
- [Skema data](#skema-data)
- [Menambah prompt](#menambah-prompt)
- [Penyimpanan lokal](#penyimpanan-lokal)
- [Arsitektur](#arsitektur)
- [Performa](#performa)
- [Keamanan dan privasi](#keamanan-dan-privasi)
- [Kustomisasi](#kustomisasi)
- [Deployment](#deployment)
- [Pemecahan masalah](#pemecahan-masalah)
- [Roadmap](#roadmap)
- [Kontribusi](#kontribusi)
- [Lisensi dan kredit](#lisensi-dan-kredit)

---

## Ringkasan

Nihongo adalah katalog prompt satu halaman. Semua prompt dikelompokkan per kategori model AI (DeepSeek, Gemini, Grok, Claude, dan seterusnya), diberi metadata panjang, dan bisa dicari, disaring, diurutkan, disalin, atau diunduh.

Tiga hal yang membedakan proyek ini dari katalog prompt biasa:

1. **Nol dependensi runtime.** Tidak ada React, tidak ada Tailwind, tidak ada CDN, tidak ada `npm install`. Satu berkas HTML berisi markup, CSS, dan logika; satu berkas JS berisi data. Font di-host sendiri.
2. **Nol permintaan jaringan.** Setelah halaman dimuat, tidak ada satu pun request keluar. Bisa dipakai di lab tanpa internet, di HP dengan mode pesawat, atau dari flashdisk.
3. **Bisa ditambah sendiri.** Ada modal bawaan untuk menambahkan prompt dan kategori baru. Data tambahan disimpan di `localStorage` peramban, digabung ke data dasar setiap halaman dimuat, dan bisa dihapus kembali tanpa menyentuh data asli.

Cocok dipakai sebagai arsip pribadi, bahan belajar prompt engineering, atau template kalau ingin membangun katalog data statis sendiri.

---

## Pratinjau antarmuka

Tata letak desktop, disederhanakan:

```
┌──────────────────────────────────────────────────────────────────────┐
│  [⚡] Nihongo            [☾ tema]  [+ Tambah]  [Tentang]              │
├───────────────┬──────────────────────────────────────────────────────┤
│  Koleksi      │  Koleksi Prompt by Nihongo                           │
│  Prompt AI    │  Kumpulan prompt AI pilihan — dikurasi oleh Nihongo…  │
│               │  ┌────────────────────────────────────────────────┐  │
│  183 Prompt   │  │ 🔍 Cari prompt...                             │  │
│  15 Kategori  │  └────────────────────────────────────────────────┘  │
│               │  [📖 Semua Panjang ▾]              Urut: [Terbaru ▾] │
│  KATEGORI     │  ┌───────────┐ ┌───────────┐ ┌───────────┐           │
│  ▸ Semua 183  │  │ DeepSeek  │ │ Gemini    │ │ Grok      │           │
│  ▸ DeepSeek   │  │ Judul     │ │ Judul     │ │ Judul     │           │
│  ▸ Gemini     │  │ deskripsi │ │ deskripsi │ │ deskripsi │           │
│  ▸ Grok       │  │ cuplikan… │ │ cuplikan… │ │ cuplikan… │           │
│  ▸ Dola       │  │ 8.340 chr │ │ 4.120 chr │ │ 12.900 chr│           │
│  ▸ Kimi       │  │ [Salin][⬇]│ │ [Salin][⬇]│ │ [Salin][⬇]│           │
│  …            │  └───────────┘ └───────────┘ └───────────┘           │
│               │            ‹ 1 2 3 … 19 ›                            │
├───────────────┴──────────────────────────────────────────────────────┤
│  © 2026 Nihongo · XI TJKT · SMK Negeri 1 Maluku Tengah               │
└──────────────────────────────────────────────────────────────────────┘
```

Di layar sempit (<640 px) sidebar berubah menjadi deretan tombol kategori horizontal, label tombol **Tambah** menyusut jadi ikon saja, dan grid turun menjadi satu kolom.

Ada empat lapisan antarmuka: **selamat datang** (kartu sambutan sekali per muat halaman), **katalog** (halaman utama), **modul detail prompt**, dan **modal tambah** (form + daftar data lokal). Semuanya bisa ditutup dengan tombol `Esc`.

---

## Fitur

### Pencarian dan penyaringan

| Fitur | Detail |
|---|---|
| Pencarian teks | Mencocokkan judul, deskripsi, **dan** isi prompt. Pencarian isi berarti prompt sepanjang 200 ribu karakter tetap bisa ditemukan lewat frasa di tengahnya. |
| Filter kategori | 15 kategori. Satu klik pada tombol kategori di sidebar. Prompt yang punya lebih dari satu kategori muncul di semua kategori terkait. |
| Filter panjang | Pendek (<1.000 karakter), sedang (1.000–4.000), panjang (>4.000). |
| Pengurutan | Terbaru, terlama, A–Z, jumlah karakter naik, jumlah karakter turun. |
| Kombinasi | Semua filter bisa dipakai bersamaan; hasil dihitung ulang setiap kali salah satu berubah. |
| Paginasi | 10 kartu per halaman, dengan tombol pertama/terakhir dan elipsis kalau halaman banyak. |

### Tampilan kartu

- Badge kategori berwarna, warnanya diambil dari palet 10 warna dan diputar berdasarkan indeks kategori agar tiap kategori konsisten.
- Judul, deskripsi satu baris (kalau ada), dan cuplikan isi.
- Penghitung karakter berwarna sesuai kelas panjang: hijau (pendek), kuning (sedang), merah (panjang).
- Badge **`NEW!`** otomatis untuk prompt dengan `created_at` dalam 4 jam terakhir.
- Dua aksi cepat tanpa membuka modal: **Salin** dan **Unduh**.

### Detail prompt

Modal detail menampilkan badge kategori + `NEW!`, judul, deskripsi, tanggal, tiga angka (karakter, kata, estimasi token), isi lengkap prompt dengan pemformatan `pre-wrap`, dan tombol **Copy Prompt** selebar modal.

Estimasi token memakai pembagi 4 karakter per token — cukup akurat untuk teks bahasa Inggris/Indonesia dan sengaja dibuat sederhana supaya tidak perlu tabel tokenizer.

### Aksi

- **Salin** ke clipboard dengan umpan balik visual (`Tersalin!`) dan notifikasi melayang.
- **Unduh** prompt sebagai `.txt`; nama berkas dibersihkan dari karakter ilegal (`sanitizeFilename`), spasi jadi tanda hubung.
- Semua aksi tersedia di kartu maupun di modal.

### Personalisasi

- **Tema gelap/terang** dengan tombol di header; pilihan disimpan di `localStorage` (`pv-theme`) dan diterapkan sebelum render pertama sehingga tidak ada kedipan tema.
- **Tambah prompt**: judul (wajib), deskripsi (opsional), kategori (wajib), isi (wajib), dengan penghitung karakter dan estimasi token langsung.
- **Kategori baru** bisa dibuat dari dua tempat: dropdown `＋ Kategori baru…` di form, atau blok **Kategori Baru** terpisah yang langsung menambahkan kategori kosong.
- **Kelola data lokal**: daftar prompt dan kategori buatan sendiri, hapus per item, atau reset semuanya.

### Pengalaman kecil yang sering terlewat

- Overlay selamat datang saat pertama membuka, bisa ditutup dengan tombol, klik latar, atau `Esc`.
- Modal Tentang berisi statistik hidup (jumlah prompt, kategori, total karakter) yang dihitung dari data, bukan angka statis.
- Notifikasi melayang (toast) diposisikan di bawah header agar tidak menutupi tombol aksi pada layar pendek.
- Angka diformat lokal: `2,76 jt` karakter, `31.777` token, tanggal `3 Nov 2026`.

---

## Statistik koleksi

Angka di bawah dihitung langsung dari `data/pv-data.js` pada snapshot 3 November 2026.

| Metrik | Nilai |
|---|---:|
| Prompt | 183 |
| Kategori | 15 |
| Relasi prompt–kategori | 330 |
| Prompt dengan lebih dari satu kategori | 68 |
| Prompt tanpa deskripsi | 51 |
| Total karakter | 2.764.407 |
| Total kata | 400.197 |
| Rata-rata karakter per prompt | 15.106 |
| Median karakter | 8.340 |
| Prompt terpendek | 655 karakter (`XoXo AI`) |
| Prompt terpanjang | 202.502 karakter (`myth ai`) |
| Rentang `created_at` | 12 Mar 2026 → 3 Nov 2026 |

Distribusi panjang: **1** pendek, **50** sedang, **132** panjang — koleksi ini memang berat di prompt panjang.

### Distribusi per kategori

| Kategori | Prompt | Porsi |
|---|---:|---:|
| DeepSeek | 104 | 56,8% |
| Gemini | 60 | 32,8% |
| Grok | 28 | 15,3% |
| Dola | 26 | 14,2% |
| Kimi | 22 | 12,0% |
| Umum | 18 | 9,8% |
| Z.AI | 15 | 8,2% |
| Le Chat (Mistral) | 12 | 6,6% |
| OpenCode Zen | 11 | 6,0% |
| ChatGPT | 9 | 4,9% |
| Perplexity | 8 | 4,4% |
| Claude | 8 | 4,4% |
| Qwen | 7 | 3,8% |
| Qwerty AI | 1 | 0,5% |
| Nemotron | 1 | 0,5% |

Porsi dijumlah lebih dari 100% karena 68 prompt punya lebih dari satu kategori.

---

## Menjalankan

### Cara tercepat

```bash
git clone https://github.com/Ikyletwar/nihongo-prompts.git
cd nihongo-prompts
xdg-open index.html        # Linux
# open index.html          # macOS
# start index.html         # Windows
```

Tidak ada langkah build, tidak ada `npm install`. Berkas yang dibuka langsung adalah situs final.

### Lewat server lokal

Dipakai kalau ingin menguji di HP dalam satu jaringan Wi-Fi:

```bash
python3 -m http.server 8000
# buka http://localhost:8000
```

Atau:

```bash
npx serve .               # kalau sudah ada Node
php -S localhost:8000     # kalau sudah ada PHP
```

### Kompatibilitas peramban

| Peramban | Versi minimum | Catatan |
|---|---|---|
| Chrome / Edge | 90+ | jalur utama pengembangan |
| Firefox | 90+ | `backdrop-filter` didukung sejak 103 |
| Safari | 15.4+ | `-webkit-backdrop-filter` sudah disertakan |
| Chrome Android | 90+ | tata letak satu kolom |
| Safari iOS | 15.4+ | idem |

Tanpa JavaScript, halaman tetap menampilkan kerangka dan footer, tetapi daftar prompt tidak muncul karena seluruh render dilakukan di sisi klien.

### Batasan `file://`

Sebagian peramban membatasi `localStorage` pada origin `file://`, dan setiap berkas lokal bisa dianggap origin berbeda. Akibatnya data tambahan yang dibuat saat membuka lewat `file://` bisa tidak terlihat saat membuka lewat server lokal, dan sebaliknya. Ini bukan bug aplikasi. Untuk pemakaian jangka panjang, pakai server lokal atau hosting statis agar origin-nya tetap.

---

## Panduan antarmuka

### Header

| Elemen | Fungsi |
|---|---|
| Logo `Nihon` + `go` | Kembali ke halaman utama. |
| Tombol bulan/matahari | Beralih tema gelap ↔ terang, tersimpan permanen. |
| **+ Tambah** | Membuka modal tambah prompt dan kategori. |
| **Tentang** | Membuka modal tentang: identitas, statistik, daftar fitur, teknologi, detail snapshot. |

### Sidebar

- Tiga angka ringkas: total prompt, total kategori, label bagian.
- Daftar kategori berisi jumlah prompt per kategori. Kategori dengan 0 prompt (baru dibuat, belum dipakai) tetap tampil supaya bisa dikelola.
- Tombol **Semua** mengembalikan filter ke seluruh koleksi.

### Toolbar

Dua dropdown bersebelahan: filter panjang dan pengurutan. Di layar sempit keduanya menumpuk.

### Pintasan papan ketik

| Tombol | Aksi |
|---|---|
| `Esc` | Menutup lapisan teratas: modal Tambah → modal Tentang → detail prompt → kartu selamat datang |
| `Tab` / `Shift+Tab` | Berpindah antar kontrol (perilaku bawaan peramban) |
| `Enter` | Mengirim form tambah prompt saat fokus di dalam form |
| `Space` | Mengaktifkan tombol/kartu yang sedang fokus |

Tidak ada pintasan global seperti `Ctrl+K`; pencarian difokuskan dengan klik atau `Tab`.

### Alur menambah prompt

1. Klik **+ Tambah** → modal terbuka, fokus otomatis ke kolom judul.
2. Isi judul (wajib), deskripsi (opsional).
3. Pilih kategori dari dropdown, atau pilih `＋ Kategori baru…` lalu isi nama kategori di kolom yang muncul.
4. Tempel isi prompt. Penghitung di bawah kolom langsung menunjukkan `N karakter · ~N token`.
5. Klik **Simpan Prompt** → modal tertutup, toast muncul, prompt langsung ada di urutan teratas dengan badge `NEW!`, statistik dan sidebar ikut diperbarui.

Kalau kolom wajib kosong, pesan kesalahan muncul di dalam modal (bukan `alert`), dan fokus berpindah ke kolom yang bermasalah.

---

## Struktur repositori

```
nihongo-prompts/
├── index.html            # 87.613 byte — markup + CSS + seluruh logika JS
├── data/
│   └── pv-data.js        # 3.022.319 byte — basis data prompt (window.__PV_DATA__)
├── fonts/
│   ├── fonts.css         # 14.585 byte — 10 deklarasi @font-face
│   └── *.woff2           # 10 berkas font Space Grotesk & Inter
├── .nojekyll             # berkas kosong; menonaktifkan pemrosesan Jekyll di GitHub Pages
├── .gitignore            # mengabaikan berkas sistem/editor
└── README.md             # dokumen ini
```

Ukuran total repo (termasuk riwayat git): sekitar 4,9 MB.

Tidak ada folder `src/`, `build/`, `dist/`, atau `node_modules/`. Yang ada di repo adalah yang dilayani ke peramban.

---

## Skema data

`data/pv-data.js` mengekspor satu variabel global:

```js
window.__PV_DATA__ = {
  categories: [],
  prompts: [],
  prompt_categories: []
};
```

### `categories`

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | string (UUID) | Kunci utama. |
| `name` | string | Nama tampilan, unik tanpa membedakan huruf besar/kecil. |
| `emoji` | string \| null | Disiapkan untuk ikon kategori; saat ini selalu `null` karena UI memakai ikon SVG. |
| `created_at` | string (ISO 8601) | Waktu pembuatan. |

### `prompts`

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | string (UUID) | Kunci utama. |
| `title` | string | Judul pendek dan deskriptif. |
| `description` | string | Satu baris ringkasan; boleh kosong. |
| `content` | string | Isi prompt lengkap, termasuk baris baru dan penanda format. |
| `created_at` | string (ISO 8601) | Dipakai untuk urutan "Terbaru" dan badge `NEW!`. |

### `prompt_categories`

| Field | Tipe | Keterangan |
|---|---|---|
| `prompt_id` | string | Merujuk `prompts.id`. |
| `category_id` | string | Merujuk `categories.id`. |

Tabel relasi ini memungkinkan satu prompt berada di beberapa kategori sekaligus (68 prompt memakainya).

### Invarian yang dijaga

1. Setiap `prompt_id` pada relasi harus ada di `prompts`.
2. Setiap `category_id` pada relasi harus ada di `categories`.
3. Setiap prompt minimal punya satu kategori.
4. Setiap kategori terpakai minimal satu prompt.
5. `id` unik di dalam tabelnya masing-masing.
6. Nama kategori unik tanpa membedakan huruf besar/kecil.

Kondisi saat ini: 183 prompt, 15 kategori, 330 relasi, **0 relasi yatim**, **0 prompt tanpa kategori**, **0 kategori kosong**.

### Contoh entri

```js
{
  id: "db2cbfa8-0303-5607-96b6-adbcecfd4d04",
  title: "Systems Integrity Consultant",
  description: "Persona konsultan integritas sistem",
  content: "# Nihongo — Systems Integrity Consultant\n\n## Character\n\nNihongo is a systems integrity consultant…",
  created_at: "2026-11-03T10:29:28.273979Z"
}
```

---

## Menambah prompt

### 1. Lewat antarmuka (paling mudah)

Klik **+ Tambah**, isi form, simpan. Data masuk ke `localStorage`, bukan ke `pv-data.js`, jadi tidak akan ikut ter-commit dan hanya terlihat di peramban itu. Cocok untuk catatan pribadi.

### 2. Menyunting `data/pv-data.js` langsung

Berkas ini satu baris panjang berisi `window.__PV_DATA__ = {…};`. Jangan disunting dengan editor teks biasa — lebih aman lewat skrip.

```python
#!/usr/bin/env python3
"""Tambah satu prompt ke data/pv-data.js."""
import json, uuid, hashlib, datetime, pathlib

DATA = pathlib.Path("data/pv-data.js")
CATEGORY = "Umum"
TITLE = "Judul Prompt Baru"
DESCRIPTION = "Satu baris ringkasan"
CONTENT = "Isi prompt lengkap di sini."

raw = DATA.read_text(encoding="utf-8")
data = json.loads(raw.split("=", 1)[1].rstrip().rstrip(";"))

# tolak duplikat berdasarkan isi
fingerprint = hashlib.md5(CONTENT.encode()).hexdigest()
for p in data["prompts"]:
    if hashlib.md5(p["content"].encode()).hexdigest() == fingerprint:
        raise SystemExit(f"Duplikat dari: {p['title']}")

cat_id = {c["name"]: c["id"] for c in data["categories"]}
if CATEGORY not in cat_id:
    raise SystemExit(f"Kategori tidak ada: {CATEGORY}")

prompt = {
    "id": str(uuid.uuid4()),
    "title": TITLE,
    "description": DESCRIPTION,
    "content": CONTENT,
    "created_at": datetime.datetime.now(datetime.timezone.utc)
        .isoformat().replace("+00:00", "Z"),
}
data["prompts"].append(prompt)
data["prompt_categories"].append(
    {"prompt_id": prompt["id"], "category_id": cat_id[CATEGORY]}
)

DATA.write_text(
    "window.__PV_DATA__ = "
    + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    + ";\n",
    encoding="utf-8",
)
print("Ditambahkan:", TITLE)
```

Jalankan dari akar repo:

```bash
python3 tambah_prompt.py
```

### 3. Impor banyak berkas `.txt` sekaligus

Pola yang dipakai untuk membangun koleksi ini: satu berkas teks = satu prompt, judul diambil dari nama berkas, kategori ditentukan per berkas.

```python
#!/usr/bin/env python3
"""Impor semua .txt dari satu folder sebagai prompt. Duplikat dilewati."""
import json, uuid, hashlib, datetime, pathlib

DATA = pathlib.Path("data/pv-data.js")
SRC = pathlib.Path("prompts-masuk")     # folder berisi .txt
CATEGORY = "Umum"

data = json.loads(DATA.read_text(encoding="utf-8").split("=", 1)[1].rstrip().rstrip(";"))
known = {hashlib.md5(p["content"].encode()).hexdigest() for p in data["prompts"]}
cat_id = {c["name"]: c["id"] for c in data["categories"]}

added = 0
for path in sorted(SRC.glob("*.txt")):
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").rstrip()
    if not text:
        continue
    if hashlib.md5(text.encode()).hexdigest() in known:
        print("lewati duplikat:", path.name)
        continue

    prompt_id = str(uuid.uuid5(uuid.NAMESPACE_URL, "file://impor/" + path.name))
    created = datetime.datetime.fromtimestamp(
        path.stat().st_mtime, datetime.timezone.utc
    ).isoformat().replace("+00:00", "Z")

    data["prompts"].append({
        "id": prompt_id,
        "title": path.stem,
        "description": "",
        "content": text,
        "created_at": created,
    })
    data["prompt_categories"].append(
        {"prompt_id": prompt_id, "category_id": cat_id[CATEGORY]}
    )
    known.add(hashlib.md5(text.encode()).hexdigest())
    added += 1

DATA.write_text(
    "window.__PV_DATA__ = "
    + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    + ";\n",
    encoding="utf-8",
)
print(f"{added} prompt ditambahkan, total {len(data['prompts'])}")
```

Catatan penting soal impor massal:

- Deduplikasi sebaiknya memakai hash isi, bukan nama berkas — banyak sumber memakai nama generik seperti `message (1).txt`.
- Kalau mengimpor ulang dari sumber yang sama, pakai `uuid.uuid5` dengan nama berkas sebagai bagian dari namespace agar ID stabil dan impor kedua ditolak.
- Bersihkan nama orang sebelum masuk: ganti dengan `Nihongo`, jangan hapus, supaya kalimat tetap terbaca.

### Setelah menambah data

1. Muat ulang halaman, cek jumlah prompt di sidebar dan modal Tentang.
2. Pastikan tidak ada relasi yatim:

```bash
python3 - <<'PY'
import json
d = json.loads(open("data/pv-data.js", encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
ids = {p["id"] for p in d["prompts"]}
cids = {c["id"] for c in d["categories"]}
rels = d["prompt_categories"]
badi = sum(1 for r in rels if r["prompt_id"] not in ids or r["category_id"] not in cids)
nokat = sum(1 for p in d["prompts"] if not any(r["prompt_id"] == p["id"] for r in rels))
kosong = sum(1 for c in d["categories"] if not any(r["category_id"] == c["id"] for r in rels))
print("prompt", len(d["prompts"]), "| kategori", len(d["categories"]), "| relasi", len(rels))
print("yatim", badi, "| tanpa kategori", nokat, "| kategori kosong", kosong)
PY
```

3. Commit dan push.

---

## Penyimpanan lokal

| Aspek | Nilai |
|---|---|
| Key data pengguna | `nihongo-user-data` |
| Key tema | `pv-theme` |
| Cakupan | Per peramban, per origin |
| Format | JSON: `{ prompts, categories, prompt_categories }` |
| ID prompt baru | `up-<uuid>` |
| ID kategori baru | `uc-<uuid>` |
| Batas kuota | sekitar 5 MB per origin di peramban modern |
| Pembersihan | tombol **Hapus semua data tambahan** di modal Tambah |

Saat `init()` berjalan:

1. Data dasar dibaca dari `pv-data.js`.
2. Data pengguna dibaca dari `localStorage`. Kalau rusak atau bukan JSON valid, dipakai objek kosong — tidak ada crash.
3. Kategori pengguna digabung, nama yang sama (tanpa membedakan huruf besar/kecil) dilewati.
4. Prompt pengguna digabung, `id` yang sudah ada di data dasar dilewati.
5. Relasi dengan kategori yang tidak valid dibuang.
6. Hasil gabungan dipakai untuk render, lalu `saveUserData()` menulis ulang versi yang sudah bersih.

Kalau kuota penuh, `saveUserData()` mengembalikan `false`, prompt tetap tampil selama sesi berjalan, dan toast memberi tahu bahwa penyimpanan permanen gagal. Modal juga menandai kalau `localStorage` diblokir sejak awal (mode privat ketat, kebijakan situs, atau `file://` yang membatasi).

Menghapus data tambahan hanya menyentuh `localStorage`; data dasar di `pv-data.js` tidak pernah diubah dari antarmuka.

---

## Arsitektur

Alur satu kali muat halaman:

```
index.html
   │
   ├─ <script src="data/pv-data.js">     → window.__PV_DATA__
   ├─ <link href="fonts/fonts.css">      → 10 woff2 lokal
   │
   ├─ tema dibaca dari localStorage ('pv-theme'), diterapkan ke <html data-theme>
   │
   ├─ init()
   │    ├─ db.from(...).select().order()   ← shim, meniru subset API supabase-js
   │    ├─ loadUserData()                  ← localStorage 'nihongo-user-data'
   │    ├─ gabung kategori + prompt + relasi
   │    ├─ hydratePrompts()                ← category_ids, categories, charCount, lengthClass
   │    ├─ refreshStats()                  ← angka sidebar + modal Tentang
   │    ├─ renderCats()
   │    ├─ renderUserLists()
   │    └─ applyFiltersAndRender()
   │
   └─ setTimeout(showWelcome, 500)
```

### Lapisan data

`db` adalah objek kecil yang meniru sebagian API `supabase-js`:

```js
db.from('prompts').select('*').order('created_at', { ascending: false })
```

Ia mengembalikan objek *thenable*, jadi bisa di-`await` persis seperti query sungguhan. Tujuannya menjaga kode render tetap sama seperti versi berbasis server, tanpa benar-benar memanggil jaringan. Kalau suatu saat data dipindah ke API nyata, yang perlu diganti hanya objek `db`.

### Peta fungsi

| Fungsi | Tanggung jawab |
|---|---|
| `init()` | Orkestrasi muat data, gabung data lokal, render awal |
| `loadUserData()` / `saveUserData()` | Baca/tulis `localStorage`, toleran terhadap data rusak |
| `hydratePrompts()` | Menempelkan `category_ids`, `categories`, `charCount`, `lengthClass` ke tiap prompt |
| `refreshStats()` | Menyinkronkan angka prompt/kategori/karakter ke sidebar dan Tentang |
| `getFilteredData()` | Menerapkan pencarian + filter kategori + filter panjang + pengurutan |
| `applyFiltersAndRender()` | Titik render tunggal setelah filter berubah; mereset halaman ke 1 |
| `renderGrid()` | Membangun HTML kartu, termasuk badge kategori dan `NEW!` |
| `renderPagination()` | Tombol halaman dengan elipsis |
| `openModal()` / `closeModal()` | Detail prompt, hitung kata/token |
| `copyModal()` / `quickCopy()` | Clipboard + umpan balik tombol |
| `quickDownload()` | Blob `.txt` + `URL.createObjectURL` |
| `toggleTheme()` | Ganti `data-theme`, simpan ke `localStorage` |
| `openAdd()` / `closeAdd()` | Modal tambah, isi ulang dropdown kategori |
| `submitPrompt()` | Validasi, buat prompt + relasi, simpan, render ulang |
| `ensureCategory()` | Cari kategori berdasarkan nama, buat kalau belum ada |
| `createCategoryOnly()` | Membuat kategori tanpa prompt |
| `deletePrompt()` / `deleteCategory()` | Hapus dari state + `localStorage`; kategori dipakai tidak bisa dihapus |
| `resetUserData()` | Kosongkan data lokal, muat ulang halaman |
| `renderUserLists()` | Daftar prompt/kategori buatan sendiri + tombol hapus |
| `showToast()` | Notifikasi melayang 2,4 detik |
| `escapeHtml()` | Sanitasi semua nilai yang masuk ke `innerHTML` |

### Gaya

Semua warna, radius, dan transisi didefinisikan sebagai CSS custom property di `:root`, dengan satu blok override `[data-theme="light"]`. Tema terang bukan inversi otomatis — nilai latar, border, dan bayangan ditulis ulang agar tetap terbaca.

Ikon memakai SVG inline (stroke `currentColor`), bukan font ikon, sehingga tidak ada request tambahan dan warna ikon otomatis mengikuti tema.

---

## Performa

| Metrik | Nilai |
|---|---|
| Berkas yang dimuat | 4 inti (HTML, JS data, CSS font, favicon) + 2–4 `woff2` yang benar-benar terpakai |
| Ukuran JS data | 3,0 MB |
| Ukuran HTML | 87,6 KB |
| Ukuran font (total 10 berkas) | 266 KB; peramban hanya mengunduh berkas untuk glyph yang dipakai |
| Total transfer awal | sekitar 3,0 MB |
| Dependensi runtime | 0 |
| Langkah build | 0 |
| Request jaringan setelah muat | 0 |

Konsekuensi yang perlu diketahui:

- **Parse data satu kali.** 3 MB JSON dieksekusi sebagai literal JavaScript, biasanya 100–300 ms di desktop dan 0,5–1,5 detik di HP kelas menengah. Setelah itu semua filter berjalan di memori tanpa I/O.
- **Render per halaman.** Hanya 10 kartu dibangun per halaman, jadi jumlah prompt besar tidak membuat DOM meledak.
- **Pencarian memakai `includes`.** Untuk isi seluruh koleksi (±2,76 juta karakter) ini masih di bawah 10 ms per ketikan di perangkat modern; belum perlu indeks atau `Fuse.js`.
- **Tidak ada `debounce`.** Pencarian memfilter langsung pada event `input`; dengan skala data sekarang ini terasa instan.

Kalau koleksi tumbuh ke puluhan MB, urutan optimasi yang masuk akal: pindah data ke JSON terpisah + `fetch` malas, tambahkan indeks pencarian sederhana (lowercase cache), lalu `debounce` 120 ms.

---

## Keamanan dan privasi

- **Nol telemetri.** Tidak ada Google Analytics, tidak ada pixel, tidak ada log server karena tidak ada server.
- **Nol permintaan keluar.** Font, ikon, dan data semuanya lokal. Satu-satunya permintaan jaringan yang pernah terjadi adalah saat halaman pertama kali diunduh dari hosting.
- **Sanitasi keluaran.** Semua nilai dinamis (judul, deskripsi, isi, nama kategori) melewati `escapeHtml()` sebelum masuk ke `innerHTML`, sehingga prompt yang berisi `<script>` atau tanda kutip tidak bisa menyuntikkan HTML.
- **Data tambahan milik peramban.** Prompt yang kamu simpan lewat UI tidak pernah dikirim ke mana pun dan tidak masuk repo.
- **Tanpa autentikasi.** Tidak ada akun, tidak ada token, tidak ada sesi. Risiko kebocoran kredensial nol karena tidak ada kredensial.
- **Konten prompt** berasal dari berbagai sumber publik. Sebelum dipublikasikan, nama penulis/persona di dalam teks diganti menjadi `Nihongo`; identitas pihak ketiga tidak ditampilkan di antarmuka maupun di data.

Yang perlu diwaspadai saat menambah data sendiri: prompt yang kamu tempel bisa berisi instruksi apa pun. Halaman ini hanya menyimpan dan menampilkannya sebagai teks biasa — tidak ada eksekusi, tidak ada evaluasi.

---

## Kustomisasi

### Warna dan tema

Ubah di blok `:root` pada `index.html`:

```css
:root {
  --bg: #0a0a0f;
  --bg-elevated: #12121a;
  --bg-card: #16161f;
  --accent: #6366f1;        /* warna utama */
  --accent-secondary: #ec4899;
  --accent-tertiary: #10b981;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --radius: 12px;
}
```

Warna kelas panjang prompt: `--length-short`, `--length-medium`, `--length-long`.

### Jumlah kartu per halaman

```js
const ITEMS_PER_PAGE = 10;
```

### Ambang badge `NEW!`

```js
const isNew = (new Date() - new Date(p.created_at)) / (1000 * 60 * 60) <= 4;
```

Ganti `4` sesuai kebutuhan (dalam jam).

### Nama, judul, dan identitas

Tersebar di beberapa tempat yang semuanya statis:

| Lokasi | Contoh |
|---|---|
| `<title>` | `Nihongo — Koleksi Prompt AI` |
| `<meta name="description">` | `Nihongo — kumpulan prompt AI pilihan. XI TJKT, SMK Negeri 1 Maluku Tengah.` |
| Logo header | `Nihon<span class="accent">go</span>` |
| H1 | `Koleksi Prompt by Nihongo` |
| Footer | `© 2026 Nihongo · XI TJKT · SMK Negeri 1 Maluku Tengah` |
| Modal Tentang | bagian identitas dan detail snapshot |

### Palet badge kategori

```js
const PALETTE = [
  { bg: 'rgba(99,102,241,0.1)',  color: '#6366f1', border: 'rgba(99,102,241,0.3)'  },
  { bg: 'rgba(236,72,153,0.1)',  color: '#ec4899', border: 'rgba(236,72,153,0.3)'  },
  // …
];
```

Warna dipilih dengan `PALETTE[indeksKategori % PALETTE.length]`, jadi menambah entri palet otomatis memperkaya variasi.

---

## Deployment

### GitHub Pages

1. Buka **Settings → Pages**.
2. **Source**: `Deploy from a branch`.
3. **Branch**: `main`, folder `/ (root)` → **Save**.
4. Tunggu 1–2 menit → `https://<pengguna>.github.io/nihongo-prompts/`.

`.nojekyll` sudah ada supaya GitHub Pages tidak memproses berkas lewat Jekyll (mencegah folder berawalan garis bawah diabaikan dan mempercepat deploy).

Semua path di `index.html` relatif (`data/pv-data.js`, `fonts/fonts.css`), jadi situs jalan di sub-path tanpa perubahan.

### Hosting statis lain

| Layanan | Setelan |
|---|---|
| Netlify | Drag-and-drop folder, atau hubungkan repo dengan build command kosong dan publish directory `.` |
| Vercel | Framework preset **Other**, build command kosong, output directory `.` |
| Cloudflare Pages | Build command kosong, output directory `/` |
| Server sendiri | Salin seluruh isi repo ke document root; tidak perlu PHP/Node |

Karena tidak ada proses build, setiap perubahan di repo langsung menjadi versi yang dilayani.

### Cache

Berkas statis tanpa hash nama bisa tersangkut cache setelah update. Kalau pengunjung masih melihat versi lama:

```bash
# paksa ambil ulang di sisi pengunjung: buka dengan query string
https://situs.example/?v=2
```

Untuk produksi jangka panjang, tambahkan header cache pendek (`Cache-Control: max-age=300`) pada hosting, atau ganti nama berkas data setiap rilis.

---

## Pemecahan masalah

**Halaman kosong, hanya spinner.**
Buka konsol peramban. Penyebab paling umum: `data/pv-data.js` gagal dimuat. Pastikan berkas ada di `data/`, path-nya relatif, dan tidak ada ekstensi berkas yang berubah (mis. `pv-data.js.txt`).

**`window.__PV_DATA__ is not defined`.**
Urutan `<script>` berubah — skrip data harus dimuat sebelum skrip utama. Jangan menambahkan `defer`/`async` pada tag data.

**Prompt yang saya tambahkan hilang setelah menutup peramban.**
Kemungkinan `localStorage` diblokir (mode privat, kebijakan situs, atau batasan `file://`). Modal Tambah menampilkan peringatan saat penyimpanan tidak tersedia. Solusi: buka lewat `http://localhost` atau hosting statis, bukan `file://`.

**Toast "gagal disimpan permanen" muncul.**
Kuota `localStorage` penuh (±5 MB). Hapus prompt lokal yang tidak terpakai, atau pakai **Hapus semua data tambahan** lalu tambahkan lagi seperlunya.

**Font tampil berbeda / jatuh ke font sistem.**
Pastikan folder `fonts/` ikut tersalin, dan `fonts/fonts.css` bisa diakses. Berkas `woff2` harus berada di folder yang sama dengan `fonts.css`.

**Modal tidak bisa ditutup.**
Klik latar gelap di luar kotak modal, tekan `Esc`, atau klik tombol `×` di kanan atas.

**Angka di sidebar tidak cocok dengan isi tabel.**
Sidebar menghitung relasi (prompt bisa masuk beberapa kategori), jadi jumlah per kategori bisa melebihi total prompt. Total prompt dihitung dari tabel `prompts`.

**Data terlihat berbeda di dua peramban.**
`localStorage` tidak tersinkron antar peramban atau perangkat. Data dasar selalu sama; hanya data tambahan yang berbeda.

---

## Roadmap

Sudah ada:

- [x] Katalog dengan pencarian, filter kategori, filter panjang, dan pengurutan
- [x] Paginasi dan modal detail dengan estimasi kata/token
- [x] Salin ke clipboard dan unduh `.txt`
- [x] Tema gelap/terang persisten
- [x] Tambah/hapus prompt dan kategori lewat UI (`localStorage`)
- [x] Responsif hingga lebar 360 px
- [x] Font lokal, tanpa permintaan jaringan

Kandidat berikutnya:

- [ ] Ekspor/impor seluruh koleksi lokal sebagai JSON (backup antar perangkat)
- [ ] Mode "favorit" dengan penyimpanan lokal
- [ ] Sorotan kata kunci pada hasil pencarian
- [ ] Indeks pencarian lowercase yang dibangun sekali saat muat
- [ ] `debounce` pencarian untuk koleksi yang jauh lebih besar
- [ ] Filter berdasarkan rentang tanggal
- [ ] Label `aria` lengkap untuk tombol ikon dan modal (saat ini mengandalkan atribut `title` dan teks tombol)

---

## Kontribusi

Repositori ini bersifat pribadi sebagai arsip pembelajaran, tetapi saran dan perbaikan diterima lewat *issue*.

Kalau mengirim *pull request*, jaga hal berikut:

1. **Tanpa dependensi baru.** Tidak ada npm, CDN, atau pustaka eksternal. Kalau butuh sesuatu, tulis sendiri di `index.html`.
2. **Tanpa permintaan jaringan.** Jangan menambahkan analitik, font CDN, atau panggilan API.
3. **Jaga invarian data.** Setelah mengubah `pv-data.js`, jalankan pemeriksaan relasi yatim di bagian [Menambah prompt](#setelah-menambah-data).
4. **Sanitasi keluaran.** Nilai dinamis wajib lewat `escapeHtml()` sebelum masuk ke `innerHTML`.
5. **Satu bahasa di UI.** Semua teks antarmuka berbahasa Indonesia; istilah teknis boleh tetap dalam bahasa aslinya.
6. **Tanpa identitas pihak ketiga.** Nama orang atau merek lain tidak boleh muncul di UI maupun di data.

Format commit yang dipakai:

```
Tambah <N> prompt dari <sumber>
Perbaiki <gejala> pada <bagian>
Ubah <bagian>: <alasan singkat>
```

---

## Lisensi dan kredit

**Kode** (`index.html`, struktur, gaya) bebas dipelajari, dimodifikasi, dan dipakai ulang untuk keperluan belajar dan proyek pribadi.

**Isi prompt** dikumpulkan dari berbagai sumber publik dan disimpan untuk keperluan arsip serta pembelajaran. Nama penulis/persona asli di dalam teks telah diganti menjadi `Nihongo`; hak atas materi asli tetap milik pembuatnya masing-masing. Kalau kamu pemilik salah satu materi dan ingin isinya dihapus, buka *issue* di repositori ini.

**Font**: Space Grotesk dan Inter, di-host lokal dalam format `woff2`, masing-masing berada di bawah SIL Open Font License.

**Dibuat dan dikurasi oleh Nihongo — XI TJKT, SMK Negeri 1 Maluku Tengah.**

Snapshot data: 3 November 2026 · 183 prompt · 15 kategori · 330 relasi · 2.764.407 karakter.
