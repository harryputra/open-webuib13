# 🎨 Panduan SAPBA Auto-Illustrator v8 (Gemini Nano Banana)

## Cara Penggunaan

### Langkah 1: Buka Open WebUI
Akses `http://localhost:3013` di browser Anda.

### Langkah 2: Buat Obrolan Baru
Klik **"Obrolan Baru"** di sidebar kiri, lalu pilih model (contoh: `gemma4:latest`).

### Langkah 3: Ketik Pesan dengan Tag `[ILUSTRASI]`
Sisipkan tag `[ILUSTRASI: deskripsi gambar]` di dalam pesan Anda.

### Langkah 4: Tunggu & Refresh
Setelah AI selesai menjawab, **tekan F5** (refresh browser) untuk melihat gambar yang sudah di-embed.

---

## Contoh Penggunaan

### 📌 Contoh 1: Ilustrasi Sederhana
```
Jelaskan topologi star dalam jaringan komputer.
[ILUSTRASI: Diagram topologi star dengan 5 komputer terhubung ke switch pusat]
```

### 📌 Contoh 2: Diagram Perbandingan
```
Bandingkan model OSI dan TCP/IP.
[ILUSTRASI: Perbandingan OSI 7-layer vs TCP/IP 4-layer side by side dengan warna berbeda]
```

### 📌 Contoh 3: Anatomi/Biologi
```
Jelaskan proses fotosintesis pada tumbuhan.
[ILUSTRASI: Diagram proses fotosintesis menunjukkan cahaya matahari, air, CO2, dan glukosa]
```

### 📌 Contoh 4: Dalam Sub-Bab Buku Ajar
```
/tulis-subbab Jaringan Komputer > Bab 3 > Subbab: Topologi Jaringan
Sertakan [ILUSTRASI: Perbandingan topologi bus, star, ring, dan mesh]
```

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────┐
│  User mengetik pesan dengan [ILUSTRASI: ...]    │
└──────────────────────┬──────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────┐
│  AI (gemma4) memproses & menjawab               │
└──────────────────────┬──────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────┐
│  Filter SAPBA v8 (outlet) aktif otomatis        │
│  ┌───────────────────────────────────────────┐  │
│  │ 1. Scan pesan user → cari [ILUSTRASI:]   │  │
│  │ 2. Scan respons AI → cari [ILUSTRASI:]   │  │
│  └───────────────────┬───────────────────────┘  │
│                      ▼                          │
│  ┌───────────────────────────────────────────┐  │
│  │ Gemini Nano Banana API                    │  │
│  │ (gemini-2.5-flash-image)                  │  │
│  │ → Gambar HD, teks akurat, label jelas     │  │
│  └──────────┬───────────┬────────────────────┘  │
│        OK ──┘     GAGAL ┘                       │
│                      ▼                          │
│  ┌───────────────────────────────────────────┐  │
│  │ Fallback: Pollinations.ai                 │  │
│  │ → Gambar standar (selalu tersedia)        │  │
│  └───────────────────────────────────────────┘  │
│                      ▼                          │
│  Base64 image di-embed ke respons AI            │
└──────────────────────┬──────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────┐
│  Refresh (F5) → Gambar muncul di chat! 🎨      │
└─────────────────────────────────────────────────┘
```

## Konfigurasi (Valves)

Filter ini memiliki pengaturan yang bisa diubah di **Admin > Functions > SAPBA Auto-Illustrator**:

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `gemini_api_key` | `AIzaSyAZ...` | API Key Google Gemini |
| `gemini_model` | `gemini-2.5-flash-image` | Model Nano Banana yang digunakan |
| `fallback_to_pollinations` | `true` | Otomatis fallback jika Gemini gagal |

### Model yang Tersedia:
- `gemini-2.5-flash-image` — Nano Banana (cepat, efisien)
- `gemini-3.1-flash-image-preview` — Nano Banana 2 (kualitas tertinggi)
- `gemini-3-pro-image-preview` — Nano Banana Pro (profesional)

## Tips

1. **Deskripsi yang detail = hasil lebih baik.** Tulis spesifik apa yang ingin divisualisasikan.
2. **Gunakan bahasa Inggris di deskripsi** untuk hasil optimal (contoh: `[ILUSTRASI: Star topology diagram]`).
3. **Satu tag per pesan** — filter memproses satu gambar per request untuk menghindari timeout.
4. **Selalu tekan F5** setelah AI selesai menjawab untuk melihat gambar.

---
*SAPBA Auto-Illustrator v8 — Powered by Google Gemini Nano Banana 🍌*
