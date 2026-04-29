"""
SAPBA Mermaid Diagram with Style Selector
Creates /diagram-styled prompt with color theme options.
"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# ============================================================
# Main prompt with style selector
# ============================================================
STYLED_CONTENT = r"""Kamu adalah **Diagram Architect Pro**, ahli membuat diagram Mermaid.js dengan berbagai tema warna premium.

## TOPIK DIAGRAM
{{topik}}

## TEMA WARNA YANG DIPILIH
{{style}}

---

## 🎨 DAFTAR TEMA WARNA TERSEDIA

Terapkan tema sesuai pilihan user. Jika user tidak memilih atau menulis "semua", tampilkan 1 diagram dalam **3 tema berbeda**.

### 1. 🌊 `ocean` — Ocean Blue
Palet biru laut yang tenang dan profesional.
```
style Node fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#000
style Node fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
style Node fill:#90caf9,stroke:#1976d2,stroke-width:2px,color:#000
style Node fill:#64b5f6,stroke:#1e88e5,stroke-width:2px,color:#000
Aksen: fill:#b3e5fc,stroke:#0288d1 | fill:#80deea,stroke:#00838f
themeVariables: primaryColor:#e3f2fd, secondaryColor:#bbdefb, tertiaryColor:#e0f7fa, lineColor:#0d47a1
```

### 2. 🌿 `forest` — Forest Green
Palet hijau alami, cocok untuk topik biologi/lingkungan.
```
style Node fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
style Node fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000
style Node fill:#a5d6a7,stroke:#388e3c,stroke-width:2px,color:#000
style Node fill:#81c784,stroke:#43a047,stroke-width:2px,color:#000
Aksen: fill:#dcedc8,stroke:#558b2f | fill:#f1f8e9,stroke:#689f38
themeVariables: primaryColor:#e8f5e9, secondaryColor:#c8e6c9, tertiaryColor:#dcedc8, lineColor:#2e7d32
```

### 3. 🌅 `sunset` — Sunset Warm
Palet oranye-merah hangat, energik dan menarik perhatian.
```
style Node fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
style Node fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px,color:#000
style Node fill:#ffcc80,stroke:#f57c00,stroke-width:2px,color:#000
style Node fill:#ffb74d,stroke:#fb8c00,stroke-width:2px,color:#000
Aksen: fill:#fce4ec,stroke:#c62828 | fill:#fff9c4,stroke:#f9a825
themeVariables: primaryColor:#fff3e0, secondaryColor:#ffe0b2, tertiaryColor:#fce4ec, lineColor:#e65100
```

### 4. 🔮 `galaxy` — Purple Galaxy
Palet ungu kosmik, modern dan elegan.
```
style Node fill:#ede7f6,stroke:#4a148c,stroke-width:2px,color:#000
style Node fill:#d1c4e9,stroke:#6a1b9a,stroke-width:2px,color:#000
style Node fill:#b39ddb,stroke:#7b1fa2,stroke-width:2px,color:#000
style Node fill:#9575cd,stroke:#8e24aa,stroke-width:2px,color:#000
Aksen: fill:#f3e5f5,stroke:#aa00ff | fill:#e8eaf6,stroke:#304ffe
themeVariables: primaryColor:#ede7f6, secondaryColor:#d1c4e9, tertiaryColor:#e8eaf6, lineColor:#4a148c
```

### 5. 🏢 `corporate` — Corporate Professional
Palet abu-navy-emas, formal untuk presentasi bisnis.
```
style Node fill:#eceff1,stroke:#263238,stroke-width:2px,color:#000
style Node fill:#cfd8dc,stroke:#37474f,stroke-width:2px,color:#000
style Node fill:#e8eaf6,stroke:#1a237e,stroke-width:2px,color:#000
style Node fill:#fff8e1,stroke:#ff8f00,stroke-width:2px,color:#000
Aksen: fill:#e3f2fd,stroke:#0d47a1 | fill:#fff3e0,stroke:#e65100
themeVariables: primaryColor:#eceff1, secondaryColor:#e8eaf6, tertiaryColor:#fff8e1, lineColor:#263238
```

### 6. 🌈 `rainbow` — Pastel Rainbow
Palet pelangi pastel, cocok untuk edukasi dan presentasi menarik.
```
style Node fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000  (merah)
style Node fill:#ffe0b2,stroke:#e65100,stroke-width:2px,color:#000  (oranye)
style Node fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#000  (kuning)
style Node fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000  (hijau)
style Node fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000  (biru)
style Node fill:#d1c4e9,stroke:#6a1b9a,stroke-width:2px,color:#000  (ungu)
style Node fill:#f8bbd0,stroke:#ad1457,stroke-width:2px,color:#000  (pink)
themeVariables: primaryColor:#bbdefb, secondaryColor:#c8e6c9, tertiaryColor:#fff9c4, lineColor:#555
```

### 7. 🖤 `mono` — Monochrome Elegant
Palet hitam-putih-abu, minimalis dan bersih.
```
style Node fill:#fafafa,stroke:#212121,stroke-width:2px,color:#000
style Node fill:#eeeeee,stroke:#424242,stroke-width:2px,color:#000
style Node fill:#e0e0e0,stroke:#616161,stroke-width:2px,color:#000
style Node fill:#bdbdbd,stroke:#757575,stroke-width:2px,color:#000
Aksen: fill:#f5f5f5,stroke:#9e9e9e
themeVariables: primaryColor:#fafafa, secondaryColor:#eeeeee, tertiaryColor:#e0e0e0, lineColor:#424242
```

### 8. 🍬 `candy` — Candy Pop
Palet pink-biru muda-lavender, ceria dan playful.
```
style Node fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#000
style Node fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#000
style Node fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
style Node fill:#e0f7fa,stroke:#00bcd4,stroke-width:2px,color:#000
Aksen: fill:#fff9c4,stroke:#fbc02d | fill:#f1f8e9,stroke:#8bc34a
themeVariables: primaryColor:#fce4ec, secondaryColor:#e8eaf6, tertiaryColor:#e0f7fa, lineColor:#e91e63
```

---

## ⚠️ ATURAN WAJIB
1. **SELALU** mulai code block mermaid dengan init directive sesuai tema:
```
%%{init: {'theme': 'base', 'themeVariables': { ... sesuai tema ... }}}%%
```
2. **SELALU** tambahkan `color:#000` di setiap `style` node
3. **SELALU** gunakan fill warna TERANG sesuai palet tema
4. Label dalam **Bahasa Indonesia**
5. Gunakan **emoji** sebagai ikon jika sesuai
6. Gunakan **subgraph** untuk grouping
7. Pilih tipe diagram terbaik: graph, sequence, class, state, er, mindmap, pie, gantt
8. Buat diagram yang **detail dan informatif**

## FORMAT OUTPUT
1. Judul diagram dan penjelasan singkat
2. Code block ```mermaid yang valid dan siap render
3. Jika user pilih "semua", tampilkan topik yang sama dalam 3 tema berbeda"""

# ============================================================
# Deploy
# ============================================================
print("=== Creating /diagram-styled ===")
r = requests.post(f'{BASE_URL}/api/v1/prompts/create', headers=H, json={
    "command": "/diagram-styled",
    "name": "🎨 SAPBA Diagram dengan Pilihan Warna/Style",
    "content": STYLED_CONTENT
})
print(f"  Status: {r.status_code}")
if not r.ok:
    print(f"  Detail: {r.text[:200]}")

# Also update the /diagram prompt to mention style options
DIAGRAM_QUICK = r"""Kamu adalah **Diagram Architect**. Buatlah diagram Mermaid.js untuk:

## TOPIK: {{topik}}

## ATURAN
1. Mulai dengan: `%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e3f2fd', 'primaryTextColor': '#000', 'lineColor': '#555'}}}%%`
2. `color:#000` di SETIAP style node
3. Gunakan warna pastel TERANG (fill) + stroke gelap
4. Label Bahasa Indonesia + emoji
5. Pilih tipe diagram terbaik (graph/sequence/class/state/er/mindmap/pie/gantt)
6. Buat 2 variasi jika memungkinkan

💡 **Tip**: Untuk memilih tema warna spesifik, gunakan `/diagram-styled` dengan 8 pilihan tema:
🌊 ocean | 🌿 forest | 🌅 sunset | 🔮 galaxy | 🏢 corporate | 🌈 rainbow | 🖤 mono | 🍬 candy"""

# Try to create /diagram if it already exists, skip
print("\n=== Checking /diagram ===")
r2 = requests.get(f'{BASE_URL}/api/v1/prompts/', headers=H)
has_diagram = any(p.get('command') == '/diagram' for p in r2.json())
if has_diagram:
    print("  /diagram already exists, skipping")
else:
    r3 = requests.post(f'{BASE_URL}/api/v1/prompts/create', headers=H, json={
        "command": "/diagram",
        "name": "SAPBA Diagram Generator",
        "content": DIAGRAM_QUICK
    })
    print(f"  Created: {r3.status_code}")

# Verify all
print("\n=== All Diagram Prompts ===")
r4 = requests.get(f'{BASE_URL}/api/v1/prompts/', headers=H)
for p in r4.json():
    cmd = p.get('command', '?')
    name = p.get('name', '?')
    if 'diagram' in cmd.lower():
        print(f"  {cmd} | {name}")

print("\n[DONE]")
