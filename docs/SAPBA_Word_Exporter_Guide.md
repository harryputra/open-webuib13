# 📄 Panduan Penggunaan SAPBA Word Exporter
**(Konversi Chat Naskah menjadi File Microsoft Word Otomatis)**

Fitur **SAPBA Word Exporter** adalah *Custom Tool* (Alat Khusus) yang ditanamkan secara eksklusif ke dalam ruang kerja (Workspace) Open WebUI Anda. Alat ini memungkinkan AI untuk mengubah teks materi panjang yang baru saja ia buat menjadi file `.docx` siap pakai.

---

## 🛠️ 1. Persiapan Awal
Karena alat ini sudah diinjeksi ke dalam sistem, pastikan alat ini aktif (On) di jendela *chat* Anda.

1. Buat **Obrolan Baru** (Pilih persona apapun, misalnya **✍️ Penulis Konten**).
2. Tepat di sebelah kiri tombol kirim (Ketik pesan...), terdapat ikon **+ (Plus)** atau ikon berbentuk **Kunci Pas (Tools)**.
3. Klik ikon tersebut, dan pastikan alat bernama **SAPBA Word Exporter** dalam keadaan **Aktif / Dicentang (✓)**.

---

## 🚀 2. Cara Eksekusi (Prompting)

AI tidak akan memanggil alat ini secara sembarangan. Ia **hanya** akan memanggilnya jika Anda secara eksplisit (jelas) memerintahkannya untuk mengekspor teks.

### Skenario 1: Mengekspor Hasil Jawaban Terakhir
Jika AI baru saja menyelesaikan tulisan panjang yang sangat bagus, ketikkan prompt berikut:
> *"Bagus sekali! Tolong kompilasi teks yang baru saja kamu tulis di atas dan ekspor menjadi file Word. Judulnya: Bab 1 Sistem Pencernaan."*

### Skenario 2: Menyusun Ulang Sebelum Diekspor
Jika Anda memiliki beberapa jawaban di chat yang terpisah-pisah, instruksikan penggabungan terlebih dahulu:
> *"Tolong rangkum semua materi sub-bab A dan sub-bab B yang sudah kita bahas sebelumnya. Setelah rapi, ekspor teks gabungannya menjadi file Word dengan judul 'Kompilasi Bab 1'."*

---

## 📥 3. Cara Mengunduh (Download)

1. Setelah Anda mengirim prompt perintah ekspor, Anda akan melihat AI menampilkan tulisan **"Calling Tool: SAPBA Word Exporter..."** yang berputar (*loading*). Ini berarti AI sedang merakit dokumen Anda di latar belakang.
2. Tunggu beberapa detik.
3. AI akan merespons dengan pesan konfirmasi dan memunculkan **Tombol Biru Besar** berbunyi:
   `📄 Download Bab_1_Sistem_Pencernaan.docx`
4. **Klik tombol tersebut!** File akan seketika terunduh dan masuk ke folder *Downloads* di komputer/laptop Anda, persis seolah Anda mengunduh lampiran email.

---

## 📐 4. Detail Teknis (Apa yang Bisa Dilakukan Alat Ini?)
Alat ini dibangun dengan library `python-docx`. Saat ia menerima naskah dari AI, ia secara cerdas memformat ulang teksnya:

- Teks berawalan `# ` otomatis menjadi **Heading 1** di Microsoft Word.
- Teks berawalan `## ` otomatis menjadi **Heading 2**.
- Teks berawalan `- ` otomatis diubah menjadi **Bullet Points** (Format Daftar) yang rapi.
- Teks berawalan `1. ` diubah menjadi **Numbered List**.
- Paragraf standar akan tercetak sebagai teks normal.

> **💡 Catatan Desain:** Alat ini dikhususkan untuk ekspor **TEKS**. Gambar *placeholder* seperti `[ILUSTRASI: ...]` akan tetap diekspor sebagai teks pengingat bagi *layout desainer* saat merancang buku di InDesign atau Word nantinya.
