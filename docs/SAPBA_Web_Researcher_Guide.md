# 🌐 Panduan Penggunaan SAPBA Live Web Researcher
**(Asisten Riset Internet & Penarikan Data Aktual)**

Fitur **SAPBA Live Web Researcher** adalah *Custom Tool* (Alat Khusus) yang memungkinkan AI—terutama persona **🔬 Asisten Riset**—untuk keluar dari batasan *database* internalnya dan melakukan pencarian langsung di internet (menggunakan mesin pencari DuckDuckGo).

Alat ini tidak hanya membaca judul artikel, tetapi juga "mengklik" *link* tersebut dan membaca paragraf di dalamnya untuk merangkum fakta terbaru untuk Anda.

---

## 🛠️ 1. Persiapan Awal
Pastikan alat ini diaktifkan di ruang obrolan (*chat*) Anda:

1. Buat **Obrolan Baru**. Disarankan menggunakan persona **🔬 Asisten Riset** atau **✍️ Penulis Konten**.
2. Klik ikon **+ (Plus)** atau ikon berbentuk **Kunci Pas (Tools)** di sebelah kiri kotak tempat Anda mengetik.
3. Pastikan **SAPBA Web Researcher** dalam keadaan **Aktif / Dicentang (✓)**.

---

## 🚀 2. Kapan Harus Menggunakannya?

Jangan gunakan alat ini untuk pertanyaan umum (seperti "Siapa penemu lampu?"). AI sudah tahu jawabannya.
Gunakan alat ini secara khusus untuk **3 Skenario** berikut:

1. **Mencari Data Statistik Terbaru:**
   *"Tolong carikan data BPS terbaru tahun 2024 tentang jumlah penduduk miskin di Indonesia."*
2. **Mencari Jurnal atau Penemuan Ilmiah Terkini:**
   *"Cari 3 artikel jurnal terbaru tahun 2025 yang membahas dampak Artificial Intelligence pada pendidikan."*
3. **Konfirmasi Fakta / Berita Terbaru:**
   *"Siapa Menteri Pendidikan Indonesia saat ini? Tolong cek ke internet untuk memastikan."*

---

## 💬 3. Contoh *Prompting* (Cara Memerintah)

AI akan otomatis memanggil alat ini jika kalimat Anda menyiratkan kebutuhan akses internet. Berikut contoh *prompt* yang paling efektif:

> *"Sebagai Asisten Riset, saya butuh referensi terbaru untuk buku ajar Sosiologi saya. Tolong gunakan internet untuk mencari studi kasus terbaru (tahun 2024-2025) tentang 'Fenomena Cyberbullying di kalangan remaja Indonesia'. Rangkum inti temuan dari artikel-artikel tersebut dan sertakan URL sumbernya."*

---

## 🔍 4. Proses yang Terjadi di Latar Belakang

1. Setelah Anda menekan Enter, tulisan **"Calling Tool: SAPBA Web Researcher..."** akan muncul berputar. Ini bisa memakan waktu sekitar **10 - 20 detik**.
2. **Apa yang dilakukan AI?**
   - Ia mengetikkan kata kunci di DuckDuckGo.
   - Ia mengambil 3-5 hasil pencarian teratas.
   - *Web Scraper* akan mengunjungi *website* tersebut satu per satu dan menyedot paragraf teks utamanya.
3. Setelah selesai, AI akan membaca seluruh data mentah itu, lalu merangkumnya dengan gaya bahasa manusia untuk disajikan kepada Anda, lengkap dengan tautan (URL) agar Anda bisa memverifikasi langsung.

> **⚠️ Penting:** Jika website sumber memiliki pengamanan ketat (seperti *paywall* jurnal berlangganan atau pemblokiran *bot* tingkat tinggi), AI mungkin hanya bisa membaca *snippet* (deskripsi singkat) dari Google/DuckDuckGo, namun ia tetap akan memberikan linknya kepada Anda.
