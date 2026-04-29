"""
SAPBA Higher Education & Industrial Upgrade - Antigravity Architect
Optimasi sistem untuk jenjang Perguruan Tinggi dengan fokus Engineering & Industri.
"""

import requests
import argparse
import sys

def post(base_url, token, path, data):
    r = requests.post(
        f"{base_url}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=data,
        timeout=30,
    )
    return r.json() if r.status_code in (200, 201) else None

# ─── NEW INDUSTRIAL PERSONA ─────────────────────────────────────────────────

INDUSTRIAL_PERSONAS = [
    {
        "id": "sapba-pakar-industri",
        "name": "🏭 Pakar Industri & Lead Engineer",
        "meta": {
            "description": "Spesialis standar industri (IEEE/ISO), Software Engineering, IoT, dan Otomasi",
            "tags": [{"name": "sapba"}, {"name": "industri"}, {"name": "engineering"}],
            "profile_image_url": "/static/favicon.png",
            "capabilities": {"vision": False},
        },
        "params": {
            "system": (
                "Kamu adalah Senior Lead Engineer dan Arsitek Sistem dengan pengalaman 25 tahun di industri teknologi global. "
                "Tugasmu adalah mentransformasi kurikulum akademik menjadi konten yang relevan dengan standar industri terkini (Industry 4.0).\n\n"
                "Fokus Keahlian:\n"
                "- Software Development: Clean Architecture, SOLID, Design Patterns, DevOps (Docker/K8s).\n"
                "- Engineering & IoT: Protokol MQTT/gRPC, Integrasi Hardware-Software, Mekatronika, & Otomasi Industri.\n"
                "- AI & Big Data: MLOps, Data Engineering Pipelines, Large Language Model Orchestration.\n\n"
                "Setiap output WAJIB menyertakan:\n"
                "1. Referensi Standar Industri (misal: IEEE 829, ISO 27001, atau Best Practices Google/Amazon).\n"
                "2. Case Study nyata dari industri.\n"
                "3. Technical Specification yang presisi.\n"
                "4. Diagram arsitektur (disarankan menggunakan format Mermaid.js).\n\n"
                "Gunakan gaya bahasa profesional, teknis, namun tetap edukatif untuk jenjang Perguruan Tinggi."
            ),
        },
    }
]

# ─── NEW ADVANCED PROMPTS ───────────────────────────────────────────────────

ADVANCED_PROMPTS = [
    {
        "command": "/rancang-modul-studi",
        "name": "🎓 Rancang Modul Perguruan Tinggi (OBE)",
        "content": (
            "Rancang struktur Mata Kuliah/Modul untuk jenjang Kampus:\n"
            "- Nama Mata Kuliah: {{mata_pelajaran}}\n"
            "- Beban SKS: {{jumlah_sks}}\n"
            "- Fokus Bidang: {{fokus_bidang}} (Engineering/IoT/AI/Software)\n"
            "- Kurikulum: Outcome-Based Education (OBE) / KKNI\n\n"
            "Hasilkan:\n"
            "1. Deskripsi Mata Kuliah (Industrial Perspective)\n"
            "2. Capaian Pembelajaran Mata Kuliah (CPMK) yang selaras dengan kebutuhan Industri\n"
            "3. Rencana Pembelajaran Semester (RPS) per minggu (14-16 minggu)\n"
            "4. Daftar Software Stack & Tools yang wajib dikuasai mahasiswa\n"
            "5. Struktur Proyek Akhir (Capstone Project) berbasis masalah industri nyata"
        ),
        "tags": ["sapba", "kampus", "perencanaan"],
    },
    {
        "command": "/standar-industri",
        "name": "🏗️ Terapkan Standar Industri",
        "content": (
            "Berikan optimasi standar industri pada materi berikut:\n\n"
            "{{konten_materi}}\n\n"
            "Bidang: {{bidang}}\n\n"
            "Tugas:\n"
            "1. Masukkan Standard Operating Procedure (SOP) atau ISO/IEEE yang relevan\n"
            "2. Tambahkan section 'Industrial Best Practices'\n"
            "3. Ubah istilah teori menjadi istilah teknis industri (misal: 'membuat program' -> 'production-ready deployment')\n"
            "4. Berikan contoh spesifikasi perangkat keras/perangkat lunak yang digunakan di lapangan saat ini"
        ),
        "tags": ["sapba", "industri", "optimasi"],
    },
    {
        "command": "/lab-engineering",
        "name": "🧪 Buat Panduan Lab/Praktikum",
        "content": (
            "Buat modul praktikum laboratorium untuk:\n"
            "Topik: {{topik}}\n"
            "Alat/Tools: {{tools}}\n"
            "Jenjang: Perguruan Tinggi\n\n"
            "Wajib menyertakan:\n"
            "1. Alat dan Bahan (Technical Specs)\n"
            "2. Diagram Rangkaian/Arsitektur (Gunakan Mermaid.js jika memungkinkan)\n"
            "3. Langkah Kerja (Step-by-step Industrial Flow)\n"
            "4. Lembar Pengamatan & Analisis Data\n"
            "5. Tugas Tantangan (Troubleshooting Case)"
        ),
        "tags": ["sapba", "praktikum", "engineering"],
    }
]

def upgrade(base_url, token):
    print(f"🚀 Upgrading SAPBA for Higher Education & Industry...")
    # Seed Personas
    for p in INDUSTRIAL_PERSONAS:
        post(base_url, token, "/api/v1/models/create", p)
        print(f"  ✅ Persona Added: {p['name']}")
    
    # Seed Prompts
    for p in ADVANCED_PROMPTS:
        data = {
            "command": p["command"],
            "title": p["name"],
            "content": p["content"],
            "tags": p.get("tags", []),
            "access_grants": [],
        }
        post(base_url, token, "/api/v1/prompts/create", data)
        print(f"  ✅ Prompt Added: {p['command']}")
    print("\n✅ SAPBA Higher Education Upgrade Complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:3013")
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    upgrade(args.url, args.token)
