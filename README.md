# Nihongo — Koleksi Prompt AI

Situs statis untuk menjelajahi, mencari, dan menyalin kumpulan prompt AI. Dibuat dan dikurasi oleh **Nihongo**, siswa **XI TJKT, SMK Negeri 1 Maluku Tengah**.

Berjalan sepenuhnya offline: tidak ada backend, tidak ada request jaringan, tidak ada API key. Seluruh data prompt disimpan di satu berkas JavaScript dan dimuat langsung oleh peramban.

**Isi saat ini:** 183 prompt · 15 kategori · 330 relasi · ±2,76 MB teks.

---

## Fitur

- **Pencarian instan** pada judul, deskripsi, dan isi prompt.
- **Filter kategori AI** — DeepSeek, Gemini, Grok, Dola, Kimi, Claude, ChatGPT, Qwen, Z.AI, Le Chat, Perplexity, OpenCode Zen, Nemotron, Qwerty AI, Umum.
- **Filter panjang prompt** — pendek (<1.000 karakter), sedang (1.000–4.000), panjang (>4.000).
- **Urutan** — terbaru, terlama, A–Z, atau jumlah karakter.
- **Paginasi** dengan jumlah item per halaman.
- **Modal detail** berisi estimasi jumlah kata dan token, plus tombol salin.
- **Salin ke clipboard** satu klik, langsung dari kartu maupun dari modal.
- **Unduh prompt** sebagai berkas `.txt`.
- **Badge `NEW!`** otomatis untuk prompt yang ditambahkan dalam 4 jam terakhir.
- **Tema gelap/terang** yang tersimpan di peramban.
- **Tambah prompt & kategori sendiri** lewat modal di header, tersimpan di `localStorage`.

---

## Menjalankan

Cukup buka `index.html` di peramban — tidak perlu server.

Kalau ingin lewat server lokal (misalnya untuk uji di perangkat lain):

```bash
python3 -m http.server 8000
# lalu buka http://localhost:8000
```

Situs ini juga siap dipasang di GitHub Pages, Netlify, Vercel, atau hosting statis apa pun tanpa konfigurasi tambahan.

---

## Struktur

```
.
├── index.html          # seluruh situs: markup, CSS, dan logika JS
├── data/
│   └── pv-data.js      # basis data prompt (window.__PV_DATA__)
├── fonts/
│   ├── fonts.css       # @font-face Space Grotesk & Inter
│   └── *.woff2         # 10 berkas font, di-host lokal
├── .nojekyll           # agar GitHub Pages tidak memproses lewat Jekyll
└── README.md
```

---

## Skema data

`data/pv-data.js` mengekspor satu objek global:

```js
window.__PV_DATA__ = {
  categories: [],        // { id, name, emoji, created_at }
  prompts: [],           // { id, title, description, content, created_at }
  prompt_categories: []  // { prompt_id, category_id }
};
```

Aturan yang dijaga:

- Setiap `prompt_id` dan `category_id` pada `prompt_categories` harus merujuk baris yang ada — tidak boleh ada relasi yatim.
- Setiap prompt minimal punya satu kategori.
- Setiap kategori terpakai minimal satu prompt.

### Menambah prompt secara manual

**Lewat antarmuka (disarankan).** Klik **+ Tambah** di header, isi judul, deskripsi (opsional), kategori, dan isi prompt. Kategori baru bisa dibuat dari dropdown (`＋ Kategori baru…`) atau dari blok **Kategori Baru**. Data tersimpan di `localStorage` dengan key `nihongo-user-data` pada struktur yang sama seperti di atas, lalu digabung ke data dasar saat halaman dimuat.

**Lewat berkas data.** Tambahkan entri ke `prompts` dan relasinya ke `prompt_categories`, lalu muat ulang halaman.

---

## Penyimpanan lokal

| Aspek | Nilai |
|---|---|
| Key | `nihongo-user-data` |
| Cakupan | Per peramban, per origin |
| Isi | `{ prompts, categories, prompt_categories }` |
| ID | `up-<uuid>` untuk prompt, `uc-<uuid>` untuk kategori |
| Batas | Kuota `localStorage` (±5 MB). Bila penuh, prompt tetap tampil di sesi berjalan tetapi ditandai gagal disimpan permanen. |
| Hapus | Tombol **Hapus semua data tambahan** di modal Tambah — hanya menghapus data lokal, data dasar tidak tersentuh. |

---

## Teknologi

HTML5 · CSS3 (custom properties, grid, flexbox) · JavaScript vanilla (ES2017+, tanpa framework, tanpa build step) · Local Snapshot · font yang di-host sendiri.

---

## Kredit

Dibuat dan dikurasi oleh **Nihongo** — XI TJKT, SMK Negeri 1 Maluku Tengah.
