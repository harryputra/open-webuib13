# 📚 Panduan Pengguna SAPBA v1.0
**(Sistem Asisten Penulisan Buku Ajar)**

Selamat datang di **SAPBA**, sebuah sistem "pabrik buku" otonom di dalam Open WebUI Anda. SAPBA mengubah proses penulisan buku ajar menjadi alur kerja yang terstruktur, melibatkan 6 AI Personas yang bertindak sebagai ahli di bidangnya masing-masing.

Dokumen ini akan memandu Anda mengubah ide abstrak menjadi buku ajar yang mematuhi **4 Pilar Kelayakan BSNP** (Isi, Penyajian, Kebahasaan, Kegrafikaan).

---

## 👥 Mengenal 6 AI Personas
Setiap kali Anda membuat Chat Baru, Anda wajib memilih salah satu persona di pojok kiri atas. Jangan menggunakan 1 persona untuk semua pekerjaan!

1. 📐 **Arsitek Kurikulum:** Ahli bedah Capaian Pembelajaran (CP). Gunakan di awal untuk membuat daftar isi dan *outline*.
2. ✍️ **Penulis Konten:** Spesialis penulisan materi berstandar BSNP (termasuk pembuatan soal HOTS dan elemen visual).
3. 🎓 **Desainer Pedagogi:** Ahli metode mengajar. Gunakan untuk merancang aktivitas kelas dan membuat visualisasi diagram (mindmap/flowchart).
4. 🔍 **Editor Bahasa:** "Polisi" EYD Edisi V. Gunakan untuk mengoreksi kalimat yang ambigu atau terlalu panjang.
5. 🔬 **Asisten Riset:** Pustakawan ahli pengelola daftar pustaka format APA 7th Edition dan pencarian fakta.
6. 🤖 **Expert Architect:** Agen otonom untuk pengembangan teknis. Gunakan untuk membuat skrip, mengelola file, atau memperbaiki sistem SAPBA secara otomatis.
7. ⚖️ **Analis Kelayakan BSNP:** Reviewer *Quality Assurance* (QA) final. Gunakan untuk menilai kelayakan naskah sebelum dicetak.

---

## 🚀 Alur Kerja Pembuatan Buku (Workflow)

Ikuti 4 langkah berurutan ini untuk hasil maksimal:

### TAHAP 1: Perencanaan & *Outline*
*Jangan menulis materi sebelum daftar isi Anda disetujui.*

1. Buat obrolan baru dengan **📐 Arsitek Kurikulum**.
2. Ketik garis miring `/` di kolom chat, lalu pilih `/rancang-buku`.
3. Isi parameter yang diminta, misalnya:
   - *Mata Pelajaran:* Biologi
   - *Jenjang:* SMA Kelas X
   - *Total Jam:* 18 JP
4. AI akan mengeluarkan Peta Kompetensi dan Daftar Bab secara rinci.
5. **Simpan output ini** sebagai kompas utama Anda.

### TAHAP 2: Penulisan Draf Kasar (Bab per Bab)
*Saatnya memproduksi teks. Kerjakan sub-bab demi sub-bab, jangan langsung 1 bab utuh.*

1. Buat obrolan baru dengan **✍️ Penulis Konten**.
2. Ketik `/buat-pendahuluan` untuk membuat bagian pembuka bab (hook & motivasi siswa).
3. Ketik `/tulis-subbab` untuk menghasilkan materi inti.
   - 💡 **Fitur Visual Otomatis:** Saat menggunakan `/tulis-subbab`, AI akan otomatis menyisipkan **Tabel Rangkuman** dan panduan gambar berupa `[ILUSTRASI: ...]` agar Anda tahu gambar apa yang harus ditaruh oleh layout desainer nantinya.
4. Ulangi `/tulis-subbab` sampai semua materi di bab tersebut habis.

### TAHAP 3: Pengayaan Visual & Latihan
*Materi yang penuh teks sangat membosankan. Kita perlu pengayaan.*

1. **Diagram:** Copy teks materi yang rumit, ganti model ke **🎓 Desainer Pedagogi**, lalu ketik `/buat-diagram`.
   - 🎨 **Custom Style:** Sekarang Anda bisa memilih **Tema Warna** (seperti *Ocean, Forest, Sunset, dll*) langsung dari menu dropdown saat memanggil perintah ini.
   - 🌓 **Dark Mode Ready:** Diagram otomatis menyesuaikan teks agar tetap terbaca jelas baik di mode terang maupun gelap.
2. **Soal HOTS:** Kembali ke **✍️ Penulis Konten**, ketik `/buat-soal-hots` untuk menghasilkan soal level C4-C6 lengkap dengan rubrik penilaian.
3. **Rangkuman & Glosarium:** Ketik `/buat-rangkuman` dan `/buat-glosarium` di akhir bab.
4. **Daftar Pustaka:** Pindah ke **🔬 Asisten Riset**, ketik `/buat-daftar-pustaka` untuk memformat referensi Anda menjadi APA 7th Edition.

### TAHAP 4: Koreksi & Uji Kelayakan BSNP
*Tahap pemolesan naskah sebelum dikirim ke penerbit/percetakan.*

1. **Koreksi EYD:** Buka obrolan dengan **🔍 Editor Bahasa**, ketik `/edit-bahasa` dan paste naskah Anda. AI akan memperbaiki salah tik dan struktur kalimat yang kaku.
2. **Cek Konsistensi:** Ketik `/cek-konsistensi` untuk memastikan tidak ada istilah yang tertukar (misal: kadang pakai "oksigen", kadang "O2").
3. **Uji BSNP (Final):** Buka obrolan dengan **⚖️ Analis Kelayakan BSNP**. Ketik `/review-bsnp` dan masukkan draf final bab Anda. AI akan mengeluarkan Skor /16 dan daftar revisi yang wajib diperbaiki.

---

## 🛠️ Daftar Lengkap 14 *Prompt Templates* (Cheat Sheet)

Kapanpun Anda butuh bantuan, ketik `/` di chat:

| Kode Prompt | Fungsi Utama | Persona yang Cocok |
|---|---|---|
| `/rancang-buku` | Membuat daftar isi & arsitektur buku | Arsitek Kurikulum |
| `/analisis-cp` | Memecah CP menjadi Indikator Bloom | Arsitek Kurikulum |
| `/buat-pendahuluan`| Menulis pembukaan bab yang menarik | Penulis Konten |
| `/architect` | Mode pengembang otonom (tulis file & jalankan terminal) | Expert Architect |
| `/tulis-bab` | Menulis isi bab lengkap (Naratif-Deskriptif) | Penulis Konten |
| `/tulis-subbab` | Menulis isi detail (termasuk Tabel & Ilustrasi)| Penulis Konten |
| `/buat-diagram` | Mengubah teks jadi Flowchart/Mindmap visual | Desainer Pedagogi |
| `/buat-soal-hots` | Membuat soal analisis C4-C6 + Rubrik | Penulis Konten |
| `/buat-rangkuman` | Merangkum poin materi jadi padat | Penulis Konten |
| `/buat-glosarium` | Mengekstrak kamus istilah teknis | Editor Bahasa / Penulis |
| `/buat-daftar-pustaka`| Merapikan sitasi format APA 7 | Asisten Riset |
| `/edit-bahasa` | Koreksi EYD dan struktur kalimat | Editor Bahasa |
| `/cek-konsistensi` | Memastikan keseragaman istilah | Editor Bahasa |
| `/review-bsnp` | Uji kelayakan 4 pilar (Isi, Bahasa, dll) | Analis Kelayakan BSNP |
| `/quality-tracker` | Laporan manajemen progres buku | Analis Kelayakan BSNP |

---

> **Pro-Tip:** Anda bisa melakukan *tagging* persona lain di dalam satu jendela chat dengan menekan tombol `@`. Misalnya, saat Penulis Konten selesai menulis teks, ketik: *"@Editor_Bahasa tolong periksa tata bahasanya."*

---

## 🛠️ Pemecahan Masalah (Troubleshooting)

| Masalah | Solusi |
|---|---|
| **Pesan: "Backend Required"** | Biasanya karena penyimpanan (disk) penuh. Sistem akan otomatis membersihkan cache, cukup tunggu 1 menit lalu refresh browser. |
| **Diagram Tidak Muncul** | Pastikan Anda menggunakan trigger `[SAPBA_DIAGRAM_TRIGGER]` atau memanggilnya via perintah `/buat-diagram`. |
| **Error: "No module named docx"** | Masalah ini sudah diperbaiki secara permanen di sistem backend. Jika muncul lagi, hubungi Antigravity Architect. |
