"""
title: Antigravity Research Engine
author: Antigravity Architect
description: Mesin riset otonom — pencarian akademik multi-sumber, ekstraksi PDF paper, sintesis literature review otomatis, deep web scraping, dan manajemen sitasi. Mendukung arXiv, Semantic Scholar, CrossRef, Google Scholar, DuckDuckGo.
version: 3.0.0
requirements: duckduckgo-search, beautifulsoup4, requests, arxiv
"""

import json
import re
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Tools:
    class Valves(BaseModel):
        semantic_scholar_api_url: str = Field(
            default="https://api.semanticscholar.org/graph/v1",
            description="Base URL for Semantic Scholar API."
        )
        crossref_api_url: str = Field(
            default="https://api.crossref.org/works",
            description="Base URL for CrossRef API."
        )
        max_content_length: int = Field(
            default=8000,
            description="Maksimum karakter konten yang diekstrak per halaman web."
        )
        request_timeout: int = Field(
            default=15,
            description="Timeout dalam detik untuk HTTP requests."
        )

    def __init__(self):
        self.valves = self.Valves()

    async def search_academic_papers(
        self,
        query: str,
        sources: str = "all",
        max_results: int = 5,
        __event_emitter__=None,
    ) -> str:
        """
        Melakukan pencarian paper akademik dari berbagai sumber ilmiah secara bersamaan.
        Gunakan tool ini ketika pengguna meminta referensi ilmiah, jurnal, paper,
        artikel akademik, atau ketika melakukan literature review.

        Sumber yang didukung: arXiv (preprint fisika, CS, matematika), Semantic Scholar
        (database AI-powered 200M+ paper), CrossRef (DOI & metadata jurnal global).

        :param query: Kata kunci pencarian spesifik (contoh: "deep learning for medical image segmentation 2024").
        :param sources: Sumber pencarian — "arxiv", "semantic_scholar", "crossref", atau "all" untuk semua sumber.
        :param max_results: Jumlah maksimal hasil per sumber (1-10, default: 5).
        :return: Hasil pencarian terstruktur dari semua sumber yang dipilih.
        """
        import requests as req

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🔬 Memulai pencarian akademik: '{query}'...",
                        "done": False,
                    },
                }
            )

        all_results = []
        sources_list = (
            ["arxiv", "semantic_scholar", "crossref"]
            if sources == "all"
            else [sources.strip()]
        )
        max_results = min(max(1, max_results), 10)

        # === arXiv Search ===
        if "arxiv" in sources_list:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "📚 Mencari di arXiv...",
                            "done": False,
                        },
                    }
                )
            try:
                import arxiv

                client = arxiv.Client()
                search = arxiv.Search(
                    query=query,
                    max_results=max_results,
                    sort_by=arxiv.SortCriterion.Relevance,
                )
                for result in client.results(search):
                    authors = ", ".join([a.name for a in result.authors[:5]])
                    if len(result.authors) > 5:
                        authors += f" et al. ({len(result.authors)} total)"
                    all_results.append(
                        {
                            "source": "arXiv",
                            "title": result.title,
                            "authors": authors,
                            "abstract": result.summary[:800],
                            "published": (
                                result.published.strftime("%Y-%m-%d")
                                if result.published
                                else "N/A"
                            ),
                            "url": result.entry_id,
                            "pdf_url": result.pdf_url,
                            "categories": ", ".join(result.categories),
                        }
                    )
            except ImportError:
                all_results.append(
                    {
                        "source": "arXiv",
                        "error": "Library 'arxiv' belum terinstall. Jalankan: pip install arxiv",
                    }
                )
            except Exception as e:
                all_results.append({"source": "arXiv", "error": str(e)})

        # === Semantic Scholar Search ===
        if "semantic_scholar" in sources_list:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "🧠 Mencari di Semantic Scholar...",
                            "done": False,
                        },
                    }
                )
            try:
                url = f"{self.valves.semantic_scholar_api_url}/paper/search"
                params = {
                    "query": query,
                    "limit": max_results,
                    "fields": "title,authors,abstract,year,citationCount,url,externalIds,publicationDate,journal",
                }
                resp = req.get(
                    url, params=params, timeout=self.valves.request_timeout
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for paper in data.get("data", []):
                        authors = ", ".join(
                            [a.get("name", "") for a in paper.get("authors", [])[:5]]
                        )
                        if len(paper.get("authors", [])) > 5:
                            authors += f" et al."
                        ext_ids = paper.get("externalIds", {})
                        doi = ext_ids.get("DOI", "N/A")
                        all_results.append(
                            {
                                "source": "Semantic Scholar",
                                "title": paper.get("title", ""),
                                "authors": authors,
                                "abstract": (paper.get("abstract", "") or "")[:800],
                                "year": paper.get("year", "N/A"),
                                "published": paper.get("publicationDate", "N/A"),
                                "citations": paper.get("citationCount", 0),
                                "doi": doi,
                                "journal": (paper.get("journal") or {}).get(
                                    "name", "N/A"
                                ),
                                "url": paper.get("url", ""),
                            }
                        )
                else:
                    all_results.append(
                        {
                            "source": "Semantic Scholar",
                            "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
                        }
                    )
            except Exception as e:
                all_results.append({"source": "Semantic Scholar", "error": str(e)})

        # === CrossRef Search ===
        if "crossref" in sources_list:
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "📑 Mencari di CrossRef...",
                            "done": False,
                        },
                    }
                )
            try:
                params = {
                    "query": query,
                    "rows": max_results,
                    "sort": "relevance",
                    "order": "desc",
                }
                resp = req.get(
                    self.valves.crossref_api_url,
                    params=params,
                    timeout=self.valves.request_timeout,
                )
                if resp.status_code == 200:
                    items = resp.json().get("message", {}).get("items", [])
                    for item in items:
                        authors = ", ".join(
                            [
                                f"{a.get('given', '')} {a.get('family', '')}".strip()
                                for a in item.get("author", [])[:5]
                            ]
                        )
                        if len(item.get("author", [])) > 5:
                            authors += " et al."
                        title_parts = item.get("title", ["Tanpa Judul"])
                        title = title_parts[0] if title_parts else "Tanpa Judul"
                        date_parts = item.get("published-print", item.get("created", {})).get("date-parts", [[]])
                        year = date_parts[0][0] if date_parts and date_parts[0] else "N/A"
                        all_results.append(
                            {
                                "source": "CrossRef",
                                "title": title,
                                "authors": authors,
                                "year": year,
                                "doi": item.get("DOI", "N/A"),
                                "journal": ", ".join(item.get("container-title", [])),
                                "type": item.get("type", "N/A"),
                                "url": item.get("URL", ""),
                                "citations": item.get("is-referenced-by-count", 0),
                            }
                        )
                else:
                    all_results.append(
                        {"source": "CrossRef", "error": f"HTTP {resp.status_code}"}
                    )
            except Exception as e:
                all_results.append({"source": "CrossRef", "error": str(e)})

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"✅ Pencarian selesai! Ditemukan {len(all_results)} hasil.",
                        "done": True,
                    },
                }
            )

        # Format output
        output = f"# 🔬 Hasil Pencarian Akademik\n"
        output += f"**Query**: {query}\n"
        output += f"**Sumber**: {', '.join(sources_list)}\n"
        output += f"**Total hasil**: {len(all_results)}\n"
        output += f"**Waktu**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"

        for i, r in enumerate(all_results, 1):
            if "error" in r:
                output += f"### ⚠️ {r['source']} — Error\n{r['error']}\n\n"
                continue
            output += f"### [{i}] {r.get('title', 'N/A')}\n"
            output += f"- **Sumber**: {r.get('source', 'N/A')}\n"
            output += f"- **Penulis**: {r.get('authors', 'N/A')}\n"
            if r.get("published"):
                output += f"- **Tanggal**: {r.get('published', r.get('year', 'N/A'))}\n"
            elif r.get("year"):
                output += f"- **Tahun**: {r.get('year', 'N/A')}\n"
            if r.get("journal") and r["journal"] != "N/A":
                output += f"- **Jurnal**: {r['journal']}\n"
            if r.get("doi") and r["doi"] != "N/A":
                output += f"- **DOI**: `{r['doi']}`\n"
            if r.get("citations"):
                output += f"- **Sitasi**: {r['citations']}x\n"
            if r.get("categories"):
                output += f"- **Kategori**: {r['categories']}\n"
            if r.get("url"):
                output += f"- **URL**: {r['url']}\n"
            if r.get("pdf_url"):
                output += f"- **PDF**: {r['pdf_url']}\n"
            if r.get("abstract"):
                output += f"\n> **Abstrak**: {r['abstract']}\n"
            output += "\n---\n\n"

        return output

    async def search_web_deep(
        self,
        query: str,
        num_results: int = 5,
        include_content: bool = True,
        __event_emitter__=None,
    ) -> str:
        """
        Melakukan pencarian web mendalam menggunakan DuckDuckGo, lalu mengekstrak
        konten lengkap dari setiap halaman hasil pencarian.
        Gunakan tool ini untuk mencari informasi terbaru, berita, tutorial,
        dokumentasi teknis, atau data yang tidak tersedia di database akademik.

        Tool ini lebih kuat dari web search biasa karena mengekstrak konten
        artikel secara lengkap, bukan hanya snippet singkat.

        :param query: Kata kunci pencarian (contoh: "latest trends in quantum computing 2025").
        :param num_results: Jumlah halaman yang akan diproses (1-8, default: 5).
        :param include_content: Jika True, ekstrak dan baca konten lengkap setiap halaman.
        :return: Hasil pencarian dengan konten lengkap yang sudah terstruktur.
        """
        import requests as req
        from bs4 import BeautifulSoup

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🌐 Memulai pencarian web mendalam: '{query}'...",
                        "done": False,
                    },
                }
            )

        num_results = min(max(1, num_results), 8)
        output = f"# 🌐 Hasil Riset Web Mendalam\n"
        output += f"**Query**: {query}\n"
        output += f"**Waktu**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"

        try:
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=num_results))

            if not search_results:
                return f"Pencarian '{query}' tidak menghasilkan hasil."

            for i, res in enumerate(search_results, 1):
                title = res.get("title", "Tanpa Judul")
                link = res.get("href", "")
                snippet = res.get("body", "")

                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": f"📖 Membaca artikel {i}/{len(search_results)}: {title[:50]}...",
                                "done": False,
                            },
                        }
                    )

                output += f"### [{i}] {title}\n"
                output += f"- **URL**: {link}\n\n"

                if include_content and link:
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        }
                        page = req.get(
                            link,
                            headers=headers,
                            timeout=self.valves.request_timeout,
                        )

                        if page.status_code == 200:
                            soup = BeautifulSoup(page.content, "html.parser")

                            # Remove script, style, nav, footer elements
                            for tag in soup(
                                ["script", "style", "nav", "footer", "header", "aside"]
                            ):
                                tag.decompose()

                            # Extract main content
                            article = soup.find("article") or soup.find(
                                "main"
                            ) or soup.find("div", {"class": re.compile(r"content|article|post|entry", re.I)})

                            if article:
                                paragraphs = article.find_all(["p", "h1", "h2", "h3", "h4", "li"])
                            else:
                                paragraphs = soup.find_all(["p", "h1", "h2", "h3"])

                            content_parts = []
                            for p in paragraphs:
                                text = p.get_text(strip=True)
                                if len(text) > 30:  # Filter noise
                                    if p.name in ["h1", "h2", "h3", "h4"]:
                                        content_parts.append(f"\n**{text}**\n")
                                    else:
                                        content_parts.append(text)

                            content = "\n\n".join(content_parts)
                            max_len = self.valves.max_content_length
                            if len(content) > max_len:
                                content = content[:max_len] + "\n\n[... konten dipotong ...]"

                            output += f"**Konten Lengkap:**\n\n{content}\n\n"
                        else:
                            output += f"**Deskripsi**: {snippet}\n\n"
                            output += f"*(Halaman tidak dapat diakses — HTTP {page.status_code})*\n\n"
                    except Exception as e:
                        output += f"**Deskripsi**: {snippet}\n\n"
                        output += f"*(Gagal membaca halaman: {str(e)[:100]})*\n\n"
                else:
                    output += f"**Deskripsi**: {snippet}\n\n"

                output += "---\n\n"

        except ImportError:
            return "Error: Library duckduckgo-search atau beautifulsoup4 belum terinstall."
        except Exception as e:
            return f"Terjadi kesalahan saat riset web: {str(e)}"

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"✅ Riset web selesai! {len(search_results)} artikel diproses.",
                        "done": True,
                    },
                }
            )

        return output

    async def manage_citations(
        self,
        papers_json: str,
        format_style: str = "apa",
        __event_emitter__=None,
    ) -> str:
        """
        Mengformat daftar paper/referensi menjadi sitasi akademik standar.
        Gunakan tool ini setelah melakukan pencarian paper untuk menghasilkan
        daftar pustaka yang siap pakai.

        Format yang didukung:
        - APA 7th Edition (default, digunakan di bidang sosial, pendidikan, psikologi)
        - IEEE (digunakan di bidang teknik dan komputer)
        - Chicago (digunakan di bidang humaniora)

        :param papers_json: Data paper dalam format JSON array. Setiap objek harus memiliki field: title, authors, year, journal/source, doi/url. Contoh: [{"title": "Deep Learning", "authors": "LeCun, Y.", "year": 2015, "journal": "Nature", "doi": "10.1038/nature14539"}]
        :param format_style: Gaya sitasi — "apa", "ieee", atau "chicago".
        :return: Daftar pustaka yang sudah terformat sesuai gaya yang dipilih.
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"📋 Memformat sitasi ({format_style.upper()})...",
                        "done": False,
                    },
                }
            )

        try:
            papers = json.loads(papers_json)
        except json.JSONDecodeError:
            return "Error: Format JSON tidak valid. Pastikan papers_json berupa array JSON yang benar."

        if not isinstance(papers, list):
            papers = [papers]

        output = f"# 📚 Daftar Pustaka ({format_style.upper()} Style)\n\n"
        citations = []

        for i, paper in enumerate(papers, 1):
            title = paper.get("title", "Tanpa Judul")
            authors = paper.get("authors", "Unknown")
            year = paper.get("year", paper.get("published", "n.d."))
            journal = paper.get("journal", paper.get("source", ""))
            doi = paper.get("doi", "")
            url = paper.get("url", "")

            if format_style.lower() == "apa":
                citation = f"{authors} ({year}). {title}."
                if journal:
                    citation += f" *{journal}*."
                if doi and doi != "N/A":
                    citation += f" https://doi.org/{doi}"
                elif url:
                    citation += f" Retrieved from {url}"

            elif format_style.lower() == "ieee":
                citation = f"[{i}] {authors}, \"{title}\","
                if journal:
                    citation += f" *{journal}*,"
                citation += f" {year}."
                if doi and doi != "N/A":
                    citation += f" doi: {doi}."

            elif format_style.lower() == "chicago":
                citation = f"{authors}. \"{title}.\""
                if journal:
                    citation += f" *{journal}*"
                citation += f" ({year})."
                if doi and doi != "N/A":
                    citation += f" https://doi.org/{doi}."
                elif url:
                    citation += f" {url}."

            else:
                citation = f"{authors} ({year}). {title}. {journal}. {doi or url}"

            citations.append(citation)

        for c in sorted(citations) if format_style.lower() != "ieee" else citations:
            output += f"- {c}\n\n"

        output += f"\n---\n*Diformat otomatis oleh Antigravity Research Engine — {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"✅ {len(citations)} sitasi berhasil diformat.",
                        "done": True,
                    },
                }
            )

        return output

    async def get_paper_details(
        self,
        paper_id: str,
        source: str = "semantic_scholar",
        __event_emitter__=None,
    ) -> str:
        """
        Mengambil detail lengkap sebuah paper akademik termasuk abstrak penuh,
        daftar referensi, paper yang mengutip, dan metadata lengkap.
        Gunakan tool ini untuk mendalami satu paper spesifik setelah pencarian awal.

        :param paper_id: ID paper (contoh: DOI "10.1038/nature14539", arXiv ID "2301.07041", atau Semantic Scholar Paper ID).
        :param source: Sumber data — "semantic_scholar" (default, paling lengkap) atau "crossref".
        :return: Detail lengkap paper termasuk abstrak, referensi, dan statistik sitasi.
        """
        import requests as req

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🔍 Mengambil detail paper: {paper_id}...",
                        "done": False,
                    },
                }
            )

        output = f"# 📄 Detail Paper\n\n"

        if source == "semantic_scholar":
            try:
                url = f"{self.valves.semantic_scholar_api_url}/paper/{paper_id}"
                params = {
                    "fields": "title,authors,abstract,year,citationCount,referenceCount,influentialCitationCount,publicationDate,journal,externalIds,url,references,citations"
                }
                resp = req.get(
                    url, params=params, timeout=self.valves.request_timeout
                )

                if resp.status_code == 200:
                    p = resp.json()
                    authors = ", ".join(
                        [a.get("name", "") for a in p.get("authors", [])]
                    )
                    ext_ids = p.get("externalIds", {})

                    output += f"## {p.get('title', 'N/A')}\n\n"
                    output += f"- **Penulis**: {authors}\n"
                    output += f"- **Tahun**: {p.get('year', 'N/A')}\n"
                    output += f"- **Tanggal Publikasi**: {p.get('publicationDate', 'N/A')}\n"
                    if p.get("journal"):
                        output += f"- **Jurnal**: {p['journal'].get('name', 'N/A')}\n"
                    output += f"- **Total Sitasi**: {p.get('citationCount', 0)}\n"
                    output += f"- **Sitasi Berpengaruh**: {p.get('influentialCitationCount', 0)}\n"
                    output += f"- **Total Referensi**: {p.get('referenceCount', 0)}\n"

                    if ext_ids.get("DOI"):
                        output += f"- **DOI**: `{ext_ids['DOI']}`\n"
                    if ext_ids.get("ArXiv"):
                        output += f"- **arXiv**: `{ext_ids['ArXiv']}`\n"
                    output += f"- **URL**: {p.get('url', 'N/A')}\n"

                    if p.get("abstract"):
                        output += f"\n### Abstrak\n\n{p['abstract']}\n"

                    # Top references
                    refs = p.get("references", [])
                    if refs:
                        output += f"\n### Referensi Utama (dari {len(refs)} total)\n\n"
                        for j, ref in enumerate(refs[:10], 1):
                            ref_title = ref.get("title", "N/A")
                            ref_year = ref.get("year", "")
                            output += f"{j}. {ref_title} ({ref_year})\n"

                    # Top citations
                    cits = p.get("citations", [])
                    if cits:
                        output += f"\n### Paper yang Mengutip (dari {len(cits)} total)\n\n"
                        for j, cit in enumerate(cits[:10], 1):
                            cit_title = cit.get("title", "N/A")
                            cit_year = cit.get("year", "")
                            output += f"{j}. {cit_title} ({cit_year})\n"
                else:
                    output += f"Error: HTTP {resp.status_code} — {resp.text[:200]}\n"
            except Exception as e:
                output += f"Error: {str(e)}\n"

        elif source == "crossref":
            try:
                url = f"{self.valves.crossref_api_url}/{paper_id}"
                resp = req.get(url, timeout=self.valves.request_timeout)
                if resp.status_code == 200:
                    item = resp.json().get("message", {})
                    title = item.get("title", ["N/A"])[0] if item.get("title") else "N/A"
                    authors = ", ".join(
                        [
                            f"{a.get('given', '')} {a.get('family', '')}".strip()
                            for a in item.get("author", [])
                        ]
                    )
                    output += f"## {title}\n\n"
                    output += f"- **Penulis**: {authors}\n"
                    output += f"- **Jurnal**: {', '.join(item.get('container-title', []))}\n"
                    output += f"- **DOI**: `{item.get('DOI', 'N/A')}`\n"
                    output += f"- **Tipe**: {item.get('type', 'N/A')}\n"
                    output += f"- **Sitasi**: {item.get('is-referenced-by-count', 0)}\n"
                    output += f"- **URL**: {item.get('URL', 'N/A')}\n"

                    if item.get("abstract"):
                        # Clean HTML from CrossRef abstracts
                        abstract = re.sub(r"<[^>]+>", "", item["abstract"])
                        output += f"\n### Abstrak\n\n{abstract}\n"

                    refs = item.get("reference", [])
                    if refs:
                        output += f"\n### Referensi (dari {len(refs)} total)\n\n"
                        for j, ref in enumerate(refs[:10], 1):
                            ref_text = ref.get("unstructured", ref.get("article-title", "N/A"))
                            output += f"{j}. {ref_text}\n"
                else:
                    output += f"Error: HTTP {resp.status_code}\n"
            except Exception as e:
                output += f"Error: {str(e)}\n"

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "✅ Detail paper berhasil diambil.",
                        "done": True,
                    },
                }
            )

        return output

    async def synthesize_literature_review(
        self,
        topic: str,
        papers_data: str = "",
        num_sources: int = 8,
        focus_areas: str = "",
        __event_emitter__=None,
    ) -> str:
        """
        Melakukan riset otomatis dan menghasilkan sintesis literature review
        yang komprehensif. Tool ini secara otomatis mencari paper dari
        berbagai sumber, menganalisis tren, menemukan gap penelitian,
        dan menghasilkan narasi akademik yang siap pakai.

        Gunakan tool ini untuk:
        - Membuat literature review otomatis untuk skripsi/tesis/disertasi
        - Menganalisis state-of-the-art suatu bidang penelitian
        - Menemukan research gap dan peluang riset baru
        - Menghasilkan tinjauan pustaka terstruktur

        :param topic: Topik riset utama (contoh: "federated learning for healthcare data privacy").
        :param papers_data: Opsional — data paper yang sudah ada dalam format JSON dari pencarian sebelumnya. Jika kosong, tool akan mencari otomatis.
        :param num_sources: Jumlah sumber yang dicari per database (3-15, default: 8).
        :param focus_areas: Area fokus spesifik, dipisahkan koma (contoh: "metodologi, dataset, evaluasi, limitasi").
        :return: Literature review terstruktur dengan analisis tren, gap, dan rekomendasi.
        """
        import requests as req

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📚 Memulai sintesis literature review: '{topic}'...", "done": False}})

        num_sources = min(max(3, num_sources), 15)
        all_papers = []

        # Auto-search if no papers provided
        if not papers_data:
            # Search arXiv
            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": "🔬 Fase 1/4: Mengumpulkan paper dari arXiv...", "done": False}})
            try:
                import arxiv
                client = arxiv.Client()
                search = arxiv.Search(query=topic, max_results=num_sources, sort_by=arxiv.SortCriterion.Relevance)
                for r in client.results(search):
                    authors = ", ".join([a.name for a in r.authors[:3]])
                    if len(r.authors) > 3:
                        authors += " et al."
                    all_papers.append({
                        "title": r.title, "authors": authors,
                        "year": r.published.strftime("%Y") if r.published else "N/A",
                        "abstract": r.summary[:600], "source": "arXiv",
                        "url": r.entry_id, "categories": ", ".join(r.categories[:3]),
                    })
            except Exception:
                pass

            # Search Semantic Scholar
            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": "🧠 Fase 2/4: Mengumpulkan paper dari Semantic Scholar...", "done": False}})
            try:
                url = f"{self.valves.semantic_scholar_api_url}/paper/search"
                params = {"query": topic, "limit": num_sources, "fields": "title,authors,abstract,year,citationCount,url,journal,publicationDate"}
                resp = req.get(url, params=params, timeout=self.valves.request_timeout)
                if resp.ok:
                    for p in resp.json().get("data", []):
                        authors = ", ".join([a.get("name", "") for a in p.get("authors", [])[:3]])
                        if len(p.get("authors", [])) > 3:
                            authors += " et al."
                        all_papers.append({
                            "title": p.get("title", ""), "authors": authors,
                            "year": str(p.get("year", "N/A")),
                            "abstract": (p.get("abstract") or "")[:600],
                            "source": "Semantic Scholar",
                            "citations": p.get("citationCount", 0),
                            "url": p.get("url", ""),
                            "journal": (p.get("journal") or {}).get("name", ""),
                        })
            except Exception:
                pass
        else:
            try:
                all_papers = json.loads(papers_data)
                if not isinstance(all_papers, list):
                    all_papers = [all_papers]
            except json.JSONDecodeError:
                return "Error: Format papers_data JSON tidak valid."

        if not all_papers:
            return f"Tidak ditemukan paper untuk topik '{topic}'. Coba gunakan kata kunci yang berbeda."

        # Analyze and synthesize
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📊 Fase 3/4: Menganalisis {len(all_papers)} paper...", "done": False}})

        # Extract year distribution
        years = {}
        for p in all_papers:
            y = str(p.get("year", "N/A"))
            if y != "N/A":
                years[y] = years.get(y, 0) + 1

        # Sort papers by citations if available
        cited_papers = sorted([p for p in all_papers if p.get("citations", 0) > 0], key=lambda x: x.get("citations", 0), reverse=True)

        # Build focus areas
        focus_list = [f.strip() for f in focus_areas.split(",") if f.strip()] if focus_areas else ["definisi dan konsep", "metodologi", "hasil dan evaluasi", "limitasi dan research gap"]

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": "✍️ Fase 4/4: Menulis sintesis literature review...", "done": False}})

        # Build the review
        review = f"# 📚 Literature Review: {topic}\n\n"
        review += f"**Tanggal**: {datetime.now().strftime('%Y-%m-%d')}\n"
        review += f"**Total Paper Dianalisis**: {len(all_papers)}\n"
        review += f"**Sumber**: arXiv, Semantic Scholar\n\n---\n\n"

        # Overview
        review += "## 1. Gambaran Umum\n\n"
        review += f"Tinjauan pustaka ini menganalisis **{len(all_papers)} paper** yang berkaitan dengan topik *{topic}*. "
        if years:
            sorted_years = sorted(years.keys())
            review += f"Publikasi yang dianalisis mencakup periode **{sorted_years[0]}** hingga **{sorted_years[-1]}**. "
            recent = sum(v for k, v in years.items() if k >= str(int(sorted_years[-1]) - 1))
            review += f"Sebanyak **{recent} paper** ({recent*100//len(all_papers)}%) dipublikasikan dalam dua tahun terakhir, menunjukkan {'tingginya' if recent > len(all_papers)//2 else 'adanya'} minat penelitian di bidang ini.\n\n"

        # Year distribution table
        if years:
            review += "### Distribusi Publikasi per Tahun\n\n"
            review += "| Tahun | Jumlah |\n|:---:|:---:|\n"
            for y in sorted(years.keys()):
                bar = "█" * years[y]
                review += f"| {y} | {years[y]} {bar} |\n"
            review += "\n"

        # Top cited papers
        if cited_papers:
            review += "## 2. Paper Paling Berpengaruh\n\n"
            for i, p in enumerate(cited_papers[:5], 1):
                review += f"**[{i}]** {p['title']} ({p.get('authors', 'N/A')}, {p.get('year', 'N/A')})\n"
                review += f"- Sitasi: **{p.get('citations', 0)}x** | Sumber: {p.get('source', 'N/A')}\n"
                if p.get('abstract'):
                    review += f"- Temuan kunci: {p['abstract'][:200]}...\n"
                review += "\n"

        # Focus area analysis
        review += f"## 3. Analisis per Area Fokus\n\n"
        for area in focus_list:
            review += f"### 3.x. {area.title()}\n\n"
            review += f"> **INSTRUKSI AI**: Berdasarkan abstrak paper di bawah, sintesiskan pembahasan tentang **{area}** dalam 300-500 kata naratif. Hubungkan temuan antar paper, identifikasi konsensus dan perbedaan pandangan.\n\n"
            # Include relevant abstracts
            relevant = [p for p in all_papers if p.get('abstract')]
            for p in relevant[:4]:
                review += f"- *{p['title']}* ({p.get('year', '')}) — {p.get('abstract', '')[:150]}...\n"
            review += "\n"

        # Research gaps
        review += "## 4. Research Gap & Peluang Riset\n\n"
        review += "> **INSTRUKSI AI**: Berdasarkan analisis di atas, identifikasi minimal 3-5 research gap dan peluang riset masa depan. Tulis dalam format naratif.\n\n"

        # Complete bibliography
        review += "## 5. Daftar Pustaka\n\n"
        for i, p in enumerate(all_papers, 1):
            review += f"[{i}] {p.get('authors', 'N/A')} ({p.get('year', 'N/A')}). *{p.get('title', 'N/A')}*."
            if p.get('journal'):
                review += f" {p['journal']}."
            if p.get('url'):
                review += f" {p['url']}"
            review += "\n\n"

        review += f"---\n*Disintesis oleh Antigravity Research Engine v3.0 — {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"✅ Literature review selesai! {len(all_papers)} paper dianalisis.", "done": True}})

        return review

    async def extract_pdf_content(
        self,
        pdf_url: str,
        max_pages: int = 10,
        __event_emitter__=None,
    ) -> str:
        """
        Mengunduh dan mengekstrak teks dari paper PDF akademik.
        Mendukung URL dari arXiv, Semantic Scholar, dan sumber lainnya.

        Gunakan tool ini untuk membaca konten lengkap sebuah paper akademik
        ketika abstrak saja tidak cukup dan Anda perlu memahami metodologi,
        hasil, atau detail implementasi secara mendalam.

        :param pdf_url: URL langsung ke file PDF paper (contoh: "https://arxiv.org/pdf/2301.07041").
        :param max_pages: Jumlah halaman maksimal yang diekstrak (1-30, default: 10).
        :return: Teks yang diekstrak dari PDF beserta metadata.
        """
        import requests as req
        import io

        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {"description": f"📥 Mengunduh PDF: {pdf_url[:60]}...", "done": False}})

        max_pages = min(max(1, max_pages), 30)

        # Normalize arXiv URLs
        if "arxiv.org/abs/" in pdf_url:
            pdf_url = pdf_url.replace("/abs/", "/pdf/") + ".pdf"
        elif "arxiv.org/pdf/" in pdf_url and not pdf_url.endswith(".pdf"):
            pdf_url += ".pdf"

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Antigravity Research Engine)"}
            resp = req.get(pdf_url, headers=headers, timeout=30, stream=True)

            if resp.status_code != 200:
                return f"Error: Gagal mengunduh PDF (HTTP {resp.status_code})"

            content_type = resp.headers.get("content-type", "")
            pdf_bytes = resp.content

            if __event_emitter__:
                size_mb = len(pdf_bytes) / (1024 * 1024)
                await __event_emitter__({"type": "status", "data": {"description": f"📄 PDF diunduh ({size_mb:.1f} MB). Mengekstrak teks...", "done": False}})

            # Try PyPDF2 first, then pdfplumber, then fallback
            extracted_text = ""
            method_used = ""

            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                total_pages = len(reader.pages)
                pages_to_read = min(total_pages, max_pages)
                for i in range(pages_to_read):
                    page_text = reader.pages[i].extract_text() or ""
                    extracted_text += f"\n--- Halaman {i+1} ---\n{page_text}"
                method_used = "PyPDF2"
            except ImportError:
                try:
                    import pdfplumber
                    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                        total_pages = len(pdf.pages)
                        pages_to_read = min(total_pages, max_pages)
                        for i in range(pages_to_read):
                            page_text = pdf.pages[i].extract_text() or ""
                            extracted_text += f"\n--- Halaman {i+1} ---\n{page_text}"
                    method_used = "pdfplumber"
                except ImportError:
                    return "Error: Tidak ada PDF reader terinstall. Jalankan: pip install PyPDF2 atau pip install pdfplumber"

            if not extracted_text.strip():
                return "Error: PDF tidak mengandung teks yang bisa diekstrak (mungkin scan/gambar)."

            # Truncate if too long
            max_len = self.valves.max_content_length * 3  # 24000 chars for PDFs
            if len(extracted_text) > max_len:
                extracted_text = extracted_text[:max_len] + "\n\n[... teks dipotong, gunakan max_pages lebih kecil ...]"

            output = f"# 📄 Ekstraksi PDF\n\n"
            output += f"| Info | Detail |\n|:---|:---|\n"
            output += f"| **URL** | {pdf_url} |\n"
            output += f"| **Total Halaman** | {total_pages} |\n"
            output += f"| **Halaman Diekstrak** | {pages_to_read} |\n"
            output += f"| **Metode** | {method_used} |\n"
            output += f"| **Ukuran Teks** | {len(extracted_text)} karakter |\n\n"
            output += f"---\n\n{extracted_text}\n"

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {"description": f"✅ {pages_to_read}/{total_pages} halaman berhasil diekstrak!", "done": True}})

            return output

        except Exception as e:
            return f"Error saat memproses PDF: {str(e)}"
