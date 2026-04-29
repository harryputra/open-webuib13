# 🧠 Panduan Penggunaan RAG Auto-Sync (SAPBA)
**(Retrieval-Augmented Generation)**

Fitur RAG Auto-Sync memungkinkan AI Persona di dalam SAPBA (Sistem Asisten Penulisan Buku Ajar) untuk "membaca" dokumen PDF atau referensi resmi milik Anda secara otomatis tanpa Anda harus mengunggahnya satu per satu ke dalam antarmuka web.

---

## 📂 1. Memahami Struktur Folder RAG

Sistem ini memonitor (mengawasi) folder lokal di komputer Anda. Folder ini sudah saya buat di dalam proyek Open WebUI:
**Path Utama:** `E:\AntiGravityProject\openwebui\rag_docs\`

Di dalamnya terdapat 3 sub-folder yang masing-masing terhubung ke *Knowledge Base* (Otak) yang berbeda:

1. `\Kurikulum` ➡️ Menjadi otak `RAG_Kurikulum_Merdeka`
   *(Masukkan file: PDF Capaian Pembelajaran, Silabus, Panduan Kemdikbud)*
2. `\BSNP` ➡️ Menjadi otak `RAG_Standar_BSNP`
   *(Masukkan file: Rubrik Kelayakan Buku, Standar Penilaian)*
3. `\Bahasa` ➡️ Menjadi otak `RAG_Pedoman_Bahasa`
   *(Masukkan file: KBBI, PUEBI, EYD Edisi V)*

---

## 🚀 2. Cara Memasukkan Dokumen (Data Entry)

Anda tidak perlu membuka website Open WebUI untuk memasukkan dokumen.
1. Buka **File Explorer** di Windows Anda.
2. Navigasi ke folder `E:\AntiGravityProject\openwebui\rag_docs\`.
3. Buka salah satu sub-folder (misalnya `Kurikulum`).
4. **Copy / Paste (salin)** file PDF atau TXT yang ingin Anda jadikan referensi ke dalam folder tersebut.

---

## ⚙️ 3. Menyalakan Mesin RAG Watcher

Agar sistem menyadari ada file baru yang Anda masukkan, Anda harus menjalankan skrip penjaga (Watcher).

1. Buka aplikasi **Terminal** (PowerShell / Command Prompt) di Windows Anda.
2. Pindah ke folder skrip dengan mengetik:
   ```bash
   cd E:\AntiGravityProject\openwebui\scripts
   ```
3. Jalankan skrip penjaga:
   ```bash
   python sapba_rag_watcher.py
   ```
4. **Biarkan jendela terminal ini tetap terbuka.** Skrip ini akan melakukan *scanning* setiap 10 detik. Jika mendeteksi PDF baru, ia akan mengunggah, mengekstrak teks, dan menyuntikkannya ke *database vector* secara otomatis.
   *(Tulisan `[+] Upload successful` akan muncul di layar hitam Anda jika berhasil).*

---

## 🔗 4. Menyambungkan Otak ke Persona (Satu Kali Saja)

Setelah mesin RAG menyedot dokumen Anda, saatnya memasang otak tersebut ke Persona yang tepat. **Langkah ini hanya perlu dilakukan SATU KALI seumur hidup.**

1. Buka Open WebUI di browser Anda (`http://localhost:3013`).
2. Masuk ke menu **Workspace** (Ruang Kerja) > **Models** (Model).
3. Cari **📐 Arsitek Kurikulum** dan klik **ikon Pensil** (Edit).
4. Pada menu sebelah kiri, klik tab **Knowledge** (Pengetahuan).
5. Klik tombol **Pilih Pengetahuan**.
6. Centang/pilih `RAG_Kurikulum_Merdeka`.
7. Klik **Save** (Simpan & Perbarui).

**Rekomendasi Pemasangan Otak:**
- **Arsitek Kurikulum** ➡️ Pasangkan dengan `RAG_Kurikulum_Merdeka`
- **Analis Kelayakan BSNP** ➡️ Pasangkan dengan `RAG_Standar_BSNP`
- **Editor Bahasa** ➡️ Pasangkan dengan `RAG_Pedoman_Bahasa`

---

## ✅ 5. Cara Menguji Apakah RAG Bekerja

1. Buka obrolan baru dengan **📐 Arsitek Kurikulum**.
2. Berikan instruksi biasa, misalnya: *"Buatkan struktur bab biologi SMA Kelas X."*
3. Di dalam obrolan, Anda akan melihat AI **secara otomatis menampilkan indikator bahwa ia sedang "mencari" (Searching/Retrieving) di dokumen Anda** sebelum ia mulai mengetik jawaban.
4. Jawaban yang dihasilkan akan merujuk pada isi dari PDF yang Anda masukkan ke folder tadi.

> **💡 Catatan Penting:** Semakin spesifik PDF yang Anda masukkan (misalnya hanya PDF materi biologi, bukan PDF panduan umum sekolah), semakin presisi dan cerdas hasil *outline* buku yang dibuat oleh AI.
