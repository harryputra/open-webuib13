"""
title: Antigravity Book Engine
author: Antigravity Architect
description: Mesin penulisan buku otonom — outline generation, penulisan bab naratif, manajemen state multi-bab, pengecekan konsistensi, dan ekspor multi-format (DOCX, EPUB, PDF, Markdown).
version: 3.0.0
requirements: python-docx, ebooklib, markdown
"""

import json
import os
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        output_dir: str = Field(
            default="/file_rag/books",
            description="Direktori output untuk file buku yang diekspor."
        )
        default_word_target: int = Field(
            default=2000,
            description="Target jumlah kata default per bab."
        )

    def __init__(self):
        self.valves = self.Valves()

    async def generate_book_outline(
        self,
        title: str,
        topic: str,
        num_chapters: int = 8,
        audience: str = "umum",
        book_type: str = "non-fiksi",
        __event_emitter__=None,
    ) -> str:
        """
        Menghasilkan outline/kerangka buku yang komprehensif dan terstruktur
        lengkap dengan judul bab, sub-bab, dan deskripsi singkat setiap bagian.

        Gunakan tool ini sebagai langkah pertama sebelum menulis konten buku.
        Outline yang dihasilkan bisa langsung digunakan sebagai panduan penulisan.

        :param title: Judul buku (contoh: "Kecerdasan Buatan untuk Pendidikan").
        :param topic: Topik utama dan cakupan buku (contoh: "Penerapan AI dan machine learning dalam transformasi sistem pendidikan di Indonesia").
        :param num_chapters: Jumlah bab yang diinginkan (3-20, default: 8).
        :param audience: Target pembaca — "umum", "mahasiswa", "profesional", "akademisi", "pemula".
        :param book_type: Jenis buku — "non-fiksi", "buku-ajar", "panduan-teknis", "monograf", "novel".
        :return: Outline lengkap dalam format Markdown yang siap digunakan.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📖 Merancang outline buku: '{title}'...", "done": False}})

        num_chapters = min(max(3, num_chapters), 20)

        outline = f"# 📖 Outline Buku: {title}\n\n"
        outline += f"| Metadata | Detail |\n|:---|:---|\n"
        outline += f"| **Judul** | {title} |\n"
        outline += f"| **Topik** | {topic} |\n"
        outline += f"| **Jenis** | {book_type} |\n"
        outline += f"| **Target Pembaca** | {audience} |\n"
        outline += f"| **Jumlah Bab** | {num_chapters} |\n"
        outline += f"| **Dibuat** | {datetime.now().strftime('%Y-%m-%d %H:%M')} |\n\n"
        outline += "---\n\n"
        outline += "## Struktur Buku\n\n"

        # Pre-content sections
        outline += "### Bagian Awal\n"
        outline += "- **Kata Pengantar** — Latar belakang penulisan dan ucapan terima kasih\n"
        outline += "- **Daftar Isi** — Navigasi seluruh bab dan sub-bab\n"
        outline += "- **Daftar Gambar & Tabel** — Index visual\n"
        outline += f"- **Pendahuluan** — Konteks {topic}, tujuan buku, cara membaca buku ini\n\n"

        # Chapter structure template
        outline += "### Bagian Inti\n\n"
        outline += f"> **INSTRUKSI UNTUK AI**: Gunakan outline di bawah ini sebagai kerangka.\n"
        outline += f"> Setiap bab harus ditulis dengan gaya **naratif deskriptif**, minimal {self.valves.default_word_target} kata,\n"
        outline += f"> menggunakan kalimat panjang natural, penjelasan mendalam, contoh konkret,\n"
        outline += f"> dan transisi yang halus antar paragraf. BUKAN hanya poin-poin.\n\n"

        for i in range(1, num_chapters + 1):
            outline += f"#### Bab {i}: [Judul Bab {i}]\n"
            outline += f"- **Tujuan Pembelajaran**: [Apa yang pembaca dapatkan setelah membaca bab ini]\n"
            outline += f"- **Sub-bab {i}.1**: [Judul Sub-bab] — [Deskripsi singkat 1-2 kalimat]\n"
            outline += f"- **Sub-bab {i}.2**: [Judul Sub-bab] — [Deskripsi singkat 1-2 kalimat]\n"
            outline += f"- **Sub-bab {i}.3**: [Judul Sub-bab] — [Deskripsi singkat 1-2 kalimat]\n"
            outline += f"- **Studi Kasus / Contoh**: [Relevan dengan konteks {audience}]\n"
            outline += f"- **Rangkuman Bab**: Ringkasan poin-poin kunci\n"
            outline += f"- **Soal Latihan / Refleksi**: [Pertanyaan diskusi atau evaluasi]\n\n"

        # Post-content sections
        outline += "### Bagian Akhir\n"
        outline += "- **Glosarium** — Definisi istilah-istilah penting\n"
        outline += "- **Daftar Pustaka** — Referensi akademik (format APA)\n"
        outline += "- **Indeks** — Pencarian kata kunci\n"
        outline += "- **Tentang Penulis** — Biografi singkat\n\n"
        outline += "---\n\n"
        outline += f"> **Langkah Selanjutnya**: Isi placeholder `[...]` di atas dengan konten spesifik,\n"
        outline += f"> lalu gunakan tool `write_chapter_draft` untuk menulis setiap bab secara detail.\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "✅ Outline buku berhasil dibuat!", "done": True}})

        return outline

    async def write_chapter_draft(
        self,
        chapter_title: str,
        chapter_number: int,
        key_points: str,
        word_target: int = 2000,
        writing_style: str = "naratif-deskriptif",
        additional_context: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Menghasilkan instruksi dan kerangka terstruktur untuk penulisan satu bab buku
        dengan gaya naratif deskriptif yang panjang, natural, dan komprehensif.

        Tool ini BUKAN menghasilkan konten final, melainkan memberikan panduan penulisan
        yang sangat detail agar AI bisa menghasilkan konten bab berkualitas tinggi.

        Gaya yang didukung:
        - naratif-deskriptif: Kalimat panjang, penjelasan mendalam, transisi halus
        - akademis: Formal, banyak referensi, metodologis
        - semi-formal: Campuran narasi dan poin, cocok untuk buku ajar
        - teknis: Fokus pada langkah-langkah, kode, dan spesifikasi

        :param chapter_title: Judul bab (contoh: "Fondasi Kecerdasan Buatan").
        :param chapter_number: Nomor urut bab.
        :param key_points: Poin-poin kunci yang harus dibahas, dipisahkan dengan koma atau newline.
        :param word_target: Target jumlah kata (500-5000, default: 2000).
        :param writing_style: Gaya penulisan — "naratif-deskriptif", "akademis", "semi-formal", "teknis".
        :param additional_context: Konteks tambahan seperti ringkasan bab sebelumnya untuk menjaga konsistensi.
        :return: Kerangka penulisan bab yang terstruktur dan siap dieksekusi AI.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✍️ Menyiapkan kerangka Bab {chapter_number}...", "done": False}})

        word_target = min(max(500, word_target), 5000)
        points = [p.strip() for p in key_points.replace("\n", ",").split(",") if p.strip()]

        style_instructions = {
            "naratif-deskriptif": """
GAYA PENULISAN: Naratif Deskriptif
- Gunakan kalimat PANJANG dan NATURAL, minimal 2-3 kalimat per paragraf
- Setiap paragraf harus MENGALIR ke paragraf berikutnya dengan transisi yang halus
- Jelaskan konsep secara MENDALAM, bukan hanya menyebutkan
- Gunakan ANALOGI dan CONTOH KONKRET untuk memperjelas
- Hindari daftar poin-poin; ubah menjadi narasi yang mengalir
- Sertakan KONTEKS HISTORIS atau LATAR BELAKANG jika relevan
- Paragraf pembuka harus MENARIK PERHATIAN pembaca
- Gunakan variasi panjang kalimat untuk ritme yang enak dibaca""",
            "akademis": """
GAYA PENULISAN: Akademis Formal
- Gunakan bahasa formal dan impersonal (hindari 'saya', 'kita')
- Sertakan referensi dan sitasi dalam teks (Author, Year)
- Setiap klaim harus didukung data atau referensi
- Gunakan terminologi teknis dengan definisi yang jelas
- Struktur paragraf: topik → elaborasi → evidensi → konklusi
- Hindari bahasa emosional atau subjektif""",
            "semi-formal": """
GAYA PENULISAN: Semi-Formal (Buku Ajar)
- Kombinasikan narasi dengan poin-poin terstruktur
- Sertakan kotak 'Tahukah Anda?' atau 'Catatan Penting'
- Gunakan bahasa yang mudah dipahami tapi tetap ilmiah
- Setiap sub-bab diakhiri dengan ringkasan singkat
- Sertakan contoh kasus atau studi kasus nyata""",
            "teknis": """
GAYA PENULISAN: Teknis
- Fokus pada langkah-langkah prosedural yang jelas
- Sertakan blok kode, diagram, atau spesifikasi teknis
- Gunakan format numbered-steps untuk prosedur
- Setiap konsep diikuti dengan implementasi praktis
- Sertakan catatan keamanan atau peringatan jika relevan"""
        }

        style_guide = style_instructions.get(writing_style, style_instructions["naratif-deskriptif"])

        draft = f"# ✍️ Kerangka Penulisan: Bab {chapter_number}\n\n"
        draft += f"## Instruksi Penulisan\n\n"
        draft += f"| Parameter | Nilai |\n|:---|:---|\n"
        draft += f"| **Judul Bab** | {chapter_title} |\n"
        draft += f"| **Nomor Bab** | {chapter_number} |\n"
        draft += f"| **Target Kata** | {word_target} kata |\n"
        draft += f"| **Gaya** | {writing_style} |\n"
        draft += f"| **Jumlah Poin Kunci** | {len(points)} |\n\n"

        draft += f"---\n\n"
        draft += f"### Panduan Gaya\n```\n{style_guide}\n```\n\n"

        draft += f"### Poin Kunci yang Harus Dibahas\n\n"
        for j, point in enumerate(points, 1):
            draft += f"{j}. **{point}** — Elaborasi dalam {word_target // len(points)} kata minimal\n"

        draft += f"\n### Struktur yang Diharapkan\n\n"
        draft += f"```\nBab {chapter_number}: {chapter_title}\n\n"
        draft += f"[Paragraf Pembuka — 150-200 kata]\n"
        draft += f"Hook yang menarik, konteks mengapa topik ini penting\n\n"

        for j, point in enumerate(points, 1):
            draft += f"  {chapter_number}.{j} {point}\n"
            draft += f"    [Narasi mendalam — {word_target // len(points)} kata]\n"
            draft += f"    - Penjelasan konsep\n"
            draft += f"    - Contoh/analogi\n"
            draft += f"    - Implikasi/dampak\n\n"

        draft += f"[Rangkuman Bab — 100-150 kata]\n"
        draft += f"[Soal Latihan/Refleksi — 3-5 pertanyaan]\n```\n\n"

        if additional_context:
            draft += f"### Konteks dari Bab Sebelumnya\n\n{additional_context}\n\n"

        draft += f"---\n\n"
        draft += f"> **PERINTAH**: Tulis konten Bab {chapter_number} sesuai kerangka di atas.\n"
        draft += f"> Gunakan gaya **{writing_style}** dengan target **{word_target} kata**.\n"
        draft += f"> Pastikan setiap sub-bab ditulis secara NARATIF, BUKAN hanya poin-poin.\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Kerangka Bab {chapter_number} siap!", "done": True}})

        return draft

    async def check_writing_consistency(
        self,
        current_text: str,
        reference_text: str = "",
        check_type: str = "all",
        __event_emitter__=None,
    ) -> str:
        """
        Menganalisis konsistensi dan kualitas tulisan dari sebuah teks.
        Memeriksa penggunaan istilah, gaya bahasa, struktur, dan readability.

        Gunakan tool ini untuk memastikan konsistensi antar bab dalam sebuah buku
        atau untuk mendapatkan analisis kualitas tulisan.

        :param current_text: Teks yang akan diperiksa (bab atau bagian buku saat ini).
        :param reference_text: Teks referensi untuk perbandingan (bab sebelumnya, jika ada).
        :param check_type: Jenis pemeriksaan — "all", "terminology", "structure", "readability".
        :return: Laporan analisis konsistensi dan kualitas tulisan.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "🔍 Menganalisis konsistensi tulisan...", "done": False}})

        report = "# 🔍 Laporan Konsistensi & Kualitas Tulisan\n\n"

        # Basic statistics
        words = current_text.split()
        sentences = [s.strip() for s in current_text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        paragraphs = [p.strip() for p in current_text.split("\n\n") if p.strip()]

        word_count = len(words)
        sentence_count = len(sentences)
        paragraph_count = len(paragraphs)
        avg_sentence_length = word_count / max(sentence_count, 1)
        avg_paragraph_length = word_count / max(paragraph_count, 1)

        report += "## 📊 Statistik Dasar\n\n"
        report += f"| Metrik | Nilai |\n|:---|:---|\n"
        report += f"| Jumlah Kata | {word_count} |\n"
        report += f"| Jumlah Kalimat | {sentence_count} |\n"
        report += f"| Jumlah Paragraf | {paragraph_count} |\n"
        report += f"| Rata-rata Kata/Kalimat | {avg_sentence_length:.1f} |\n"
        report += f"| Rata-rata Kata/Paragraf | {avg_paragraph_length:.1f} |\n\n"

        # Readability assessment
        report += "## 📖 Analisis Keterbacaan\n\n"
        if avg_sentence_length < 10:
            report += "⚠️ **Kalimat terlalu pendek** — Rata-rata di bawah 10 kata. Pertimbangkan menggabungkan kalimat untuk narasi yang lebih mengalir.\n\n"
        elif avg_sentence_length > 30:
            report += "⚠️ **Kalimat terlalu panjang** — Rata-rata di atas 30 kata. Pertimbangkan memecah kalimat kompleks.\n\n"
        else:
            report += "✅ **Panjang kalimat baik** — Sesuai untuk tulisan naratif.\n\n"

        if avg_paragraph_length < 50:
            report += "⚠️ **Paragraf terlalu pendek** — Pertimbangkan mengembangkan penjelasan lebih mendalam.\n\n"
        elif avg_paragraph_length > 200:
            report += "⚠️ **Paragraf terlalu panjang** — Pertimbangkan memecah paragraf untuk keterbacaan.\n\n"
        else:
            report += "✅ **Panjang paragraf baik** — Sesuai standar penulisan.\n\n"

        # Structure analysis
        headings = [line for line in current_text.split("\n") if line.strip().startswith("#")]
        report += "## 🏗️ Analisis Struktur\n\n"
        report += f"- Jumlah heading ditemukan: **{len(headings)}**\n"
        if headings:
            for h in headings[:15]:
                level = len(h.split()[0]) if h.split() else 0
                report += f"  - {'  ' * (level - 1)}{h.strip()}\n"
        report += "\n"

        # Terminology consistency (if reference provided)
        if reference_text and check_type in ["all", "terminology"]:
            report += "## 📝 Analisis Terminologi\n\n"
            # Extract potential key terms (capitalized words, technical terms)
            current_terms = set(w for w in words if len(w) > 4 and w[0].isupper())
            ref_words = reference_text.split()
            ref_terms = set(w for w in ref_words if len(w) > 4 and w[0].isupper())

            new_terms = current_terms - ref_terms
            if new_terms:
                report += f"**Istilah baru** (tidak ada di teks referensi): {', '.join(list(new_terms)[:20])}\n\n"
            common_terms = current_terms & ref_terms
            if common_terms:
                report += f"**Istilah konsisten**: {', '.join(list(common_terms)[:20])}\n\n"

        # Recommendations
        report += "## 💡 Rekomendasi\n\n"
        recs = []
        if word_count < 500:
            recs.append("Teks terlalu pendek untuk sebuah bab. Targetkan minimal 1500 kata.")
        if len(headings) < 2:
            recs.append("Tambahkan sub-heading untuk meningkatkan struktur dan navigasi.")
        if avg_sentence_length < 12:
            recs.append("Kembangkan kalimat menjadi narasi yang lebih deskriptif dan mengalir.")

        if not recs:
            report += "✅ Tidak ada masalah signifikan yang ditemukan.\n"
        else:
            for rec in recs:
                report += f"- {rec}\n"

        report += f"\n---\n*Dianalisis oleh Antigravity Book Engine — {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "✅ Analisis konsistensi selesai!", "done": True}})

        return report

    async def export_book(
        self,
        content: str,
        title: str,
        author: str = "Antigravity Author",
        export_format: str = "docx",
        __event_emitter__=None,
    ) -> str:
        """
        Mengekspor konten buku ke file yang bisa didownload.
        Format yang didukung: DOCX (Microsoft Word), EPUB (e-book), Markdown.

        Gunakan tool ini setelah semua bab selesai ditulis untuk menghasilkan
        file buku final yang bisa dicetak atau didistribusikan.

        :param content: Konten lengkap buku dalam format Markdown.
        :param title: Judul buku untuk nama file dan metadata.
        :param author: Nama penulis buku.
        :param export_format: Format ekspor — "docx", "epub", atau "markdown".
        :return: Link download file atau pesan sukses.
        """
        import base64
        import io

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📦 Mengekspor buku ke {export_format.upper()}...", "done": False}})

        safe_title = title.replace(" ", "_").replace("/", "_").replace("\\", "_")

        if export_format.lower() == "docx":
            try:
                from docx import Document
                from docx.shared import Inches, Pt
                from docx.enum.text import WD_ALIGN_PARAGRAPH

                doc = Document()

                # Title page
                title_para = doc.add_paragraph()
                title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = title_para.add_run(title)
                run.bold = True
                run.font.size = Pt(28)

                author_para = doc.add_paragraph()
                author_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = author_para.add_run(f"\n{author}")
                run.font.size = Pt(16)

                date_para = doc.add_paragraph()
                date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = date_para.add_run(f"\n{datetime.now().strftime('%Y')}")
                run.font.size = Pt(14)

                doc.add_page_break()

                # Process markdown content
                for line in content.split("\n"):
                    line = line.rstrip()
                    if not line:
                        continue
                    if line.startswith("#### "):
                        doc.add_heading(line[5:], level=4)
                    elif line.startswith("### "):
                        doc.add_heading(line[4:], level=3)
                    elif line.startswith("## "):
                        doc.add_heading(line[3:], level=2)
                    elif line.startswith("# "):
                        doc.add_heading(line[2:], level=1)
                        doc.add_page_break()
                    elif line.startswith("- "):
                        doc.add_paragraph(line[2:], style="List Bullet")
                    elif line.startswith("> "):
                        p = doc.add_paragraph(line[2:])
                        p.style = doc.styles["Intense Quote"] if "Intense Quote" in [s.name for s in doc.styles] else doc.styles["Quote"]
                    else:
                        doc.add_paragraph(line)

                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)

                b64 = base64.b64encode(buffer.read()).decode("utf-8")
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                html_link = f'<a href="data:{mime};base64,{b64}" download="{safe_title}.docx" style="display:inline-block;padding:12px 24px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;text-decoration:none;border-radius:8px;font-weight:bold;margin:10px 0;">📄 Download {safe_title}.docx</a>'

                result = f"✅ Buku berhasil diekspor ke Word!\n\n{html_link}"

            except ImportError:
                result = "Error: Library python-docx belum terinstall."
            except Exception as e:
                result = f"Error saat ekspor DOCX: {str(e)}"

        elif export_format.lower() == "epub":
            try:
                from ebooklib import epub

                book = epub.EpubBook()
                book.set_identifier(f"antigravity-{safe_title}-{datetime.now().strftime('%Y%m%d')}")
                book.set_title(title)
                book.set_language("id")
                book.add_author(author)

                # Split by chapters (# heading)
                chapters_raw = content.split("\n# ")
                epub_chapters = []

                for idx, ch_content in enumerate(chapters_raw):
                    if not ch_content.strip():
                        continue
                    lines = ch_content.split("\n")
                    ch_title = lines[0].replace("# ", "").strip()
                    ch_body = "\n".join(lines[1:])

                    # Convert markdown to basic HTML
                    html_content = f"<h1>{ch_title}</h1>\n"
                    for line in ch_body.split("\n"):
                        if line.startswith("### "):
                            html_content += f"<h3>{line[4:]}</h3>\n"
                        elif line.startswith("## "):
                            html_content += f"<h2>{line[3:]}</h2>\n"
                        elif line.startswith("- "):
                            html_content += f"<li>{line[2:]}</li>\n"
                        elif line.strip():
                            html_content += f"<p>{line}</p>\n"

                    chapter = epub.EpubHtml(
                        title=ch_title,
                        file_name=f"chap_{idx + 1}.xhtml",
                        lang="id"
                    )
                    chapter.content = html_content
                    book.add_item(chapter)
                    epub_chapters.append(chapter)

                book.toc = tuple(epub_chapters)
                book.add_item(epub.EpubNcx())
                book.add_item(epub.EpubNav())
                book.spine = ["nav"] + epub_chapters

                buffer = io.BytesIO()
                epub.write_epub(buffer, book)
                buffer.seek(0)

                b64 = base64.b64encode(buffer.read()).decode("utf-8")
                mime = "application/epub+zip"
                html_link = f'<a href="data:{mime};base64,{b64}" download="{safe_title}.epub" style="display:inline-block;padding:12px 24px;background:linear-gradient(135deg,#11998e,#38ef7d);color:white;text-decoration:none;border-radius:8px;font-weight:bold;margin:10px 0;">📚 Download {safe_title}.epub</a>'

                result = f"✅ Buku berhasil diekspor ke EPUB!\n\n{html_link}"

            except ImportError:
                result = "Error: Library ebooklib belum terinstall. Jalankan: pip install ebooklib"
            except Exception as e:
                result = f"Error saat ekspor EPUB: {str(e)}"

        elif export_format.lower() == "markdown":
            b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            mime = "text/markdown"
            html_link = f'<a href="data:{mime};base64,{b64}" download="{safe_title}.md" style="display:inline-block;padding:12px 24px;background:linear-gradient(135deg,#333,#666);color:white;text-decoration:none;border-radius:8px;font-weight:bold;margin:10px 0;">📝 Download {safe_title}.md</a>'
            result = f"✅ Buku berhasil diekspor ke Markdown!\n\n{html_link}"

        else:
            result = f"Format '{export_format}' tidak didukung. Gunakan: docx, epub, atau markdown."

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Ekspor {export_format.upper()} selesai!", "done": True}})

        return result

    async def manage_book_state(
        self,
        book_title: str,
        action: str = "view",
        chapter_number: int = 0,
        chapter_title: str = "",
        word_count: int = 0,
        status: str = "draft",
        summary: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Mengelola state/progress penulisan buku lintas sesi — melacak bab mana
        yang sudah ditulis, word count, status, dan ringkasan setiap bab.
        Data disimpan persisten di workspace sehingga progress tidak hilang.

        Gunakan tool ini untuk:
        - Melacak progress penulisan buku multi-bab
        - Melihat bab mana yang sudah selesai dan mana yang belum
        - Menyimpan ringkasan bab untuk konteks antar-bab
        - Menghitung total word count seluruh buku

        :param book_title: Judul buku (identifier unik).
        :param action: Aksi — "view" (lihat progress), "update" (update status bab), "add" (tambah bab baru), "reset" (reset state).
        :param chapter_number: Nomor bab yang akan diupdate/ditambah.
        :param chapter_title: Judul bab.
        :param word_count: Jumlah kata yang sudah ditulis untuk bab ini.
        :param status: Status bab — "draft", "outline", "writing", "review", "done".
        :param summary: Ringkasan singkat bab (untuk konteks cross-chapter).
        :return: Laporan progress buku.
        """
        import os, json

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📖 Managing book state: {book_title}...", "done": False}})

        safe_title = book_title.replace(" ", "_").replace("/", "_")[:50]
        state_dir = os.path.join(self.valves.output_dir, "states")
        os.makedirs(state_dir, exist_ok=True)
        state_file = os.path.join(state_dir, f"{safe_title}_state.json")

        # Load existing state
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
        else:
            state = {
                "title": book_title,
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "chapters": {},
                "total_words": 0,
            }

        if action == "add" and chapter_number > 0:
            key = str(chapter_number)
            state["chapters"][key] = {
                "number": chapter_number,
                "title": chapter_title or f"Bab {chapter_number}",
                "word_count": word_count,
                "status": status,
                "summary": summary,
                "updated": datetime.now().isoformat(),
            }
            state["updated"] = datetime.now().isoformat()
            state["total_words"] = sum(c.get("word_count", 0) for c in state["chapters"].values())
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

            result = f"✅ Bab {chapter_number} ditambahkan: **{chapter_title}** [{status}]"

        elif action == "update" and chapter_number > 0:
            key = str(chapter_number)
            if key in state["chapters"]:
                if chapter_title:
                    state["chapters"][key]["title"] = chapter_title
                if word_count > 0:
                    state["chapters"][key]["word_count"] = word_count
                if status:
                    state["chapters"][key]["status"] = status
                if summary:
                    state["chapters"][key]["summary"] = summary
                state["chapters"][key]["updated"] = datetime.now().isoformat()
                state["updated"] = datetime.now().isoformat()
                state["total_words"] = sum(c.get("word_count", 0) for c in state["chapters"].values())
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
                result = f"✅ Bab {chapter_number} diupdate → [{status}]"
            else:
                result = f"Bab {chapter_number} tidak ditemukan. Gunakan action='add' untuk menambah."

        elif action == "reset":
            state = {"title": book_title, "created": datetime.now().isoformat(), "updated": datetime.now().isoformat(), "chapters": {}, "total_words": 0}
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            result = f"🔄 State buku '{book_title}' direset."

        elif action == "view":
            chapters = state.get("chapters", {})
            if not chapters:
                return f"📖 Buku '{book_title}' belum memiliki data bab. Gunakan action='add' untuk mulai."

            total = len(chapters)
            done = sum(1 for c in chapters.values() if c.get('status') == 'done')
            total_words = state.get('total_words', 0)

            report = f"# 📖 Book Progress: {book_title}\n\n"
            report += f"**Progress**: {done}/{total} bab selesai ({done*100//max(total,1)}%)\n"
            report += f"**Total Kata**: {total_words:,} kata\n"
            report += f"**Estimasi Halaman**: ~{total_words // 250} halaman\n\n"

            # Progress bar
            filled = done * 20 // max(total, 1)
            bar = "█" * filled + "░" * (20 - filled)
            report += f"```\n[{bar}] {done*100//max(total,1)}%\n```\n\n"

            report += "| Bab | Judul | Kata | Status |\n|:---:|:---|:---:|:---:|\n"
            icons = {"draft": "⏳", "outline": "📋", "writing": "✍️", "review": "🔍", "done": "✅"}
            for key in sorted(chapters.keys(), key=lambda x: int(x)):
                ch = chapters[key]
                icon = icons.get(ch.get('status', ''), '❓')
                report += f"| {ch['number']} | {ch.get('title', 'N/A')} | {ch.get('word_count', 0):,} | {icon} {ch.get('status', 'N/A')} |\n"

            # Cross-chapter summaries for context
            has_summaries = [ch for ch in chapters.values() if ch.get('summary')]
            if has_summaries:
                report += "\n### 📝 Ringkasan per Bab (untuk konteks)\n\n"
                for ch in sorted(has_summaries, key=lambda x: x['number']):
                    report += f"**Bab {ch['number']}**: {ch.get('summary', '')}\n\n"

            result = report
        else:
            result = "Aksi tidak valid. Gunakan: view, add, update, reset."

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "✅ Book state updated!", "done": True}})

        return result
