# 🎨 SAPBA Diagram Style Catalog

Berikut **8 tema warna** yang tersedia untuk diagram Mermaid di SAPBA.

## Cara Penggunaan

Ketik `/diagram-styled` di Open WebUI, lalu isi:
- **topik**: Topik diagram yang diinginkan
- **style**: Nama tema (contoh: `ocean`, `galaxy`, `rainbow`)

---

## 🌊 1. Ocean Blue (`ocean`)
Profesional, tenang — cocok untuk **jaringan & teknologi**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e3f2fd', 'primaryTextColor': '#000', 'lineColor': '#0d47a1'}}}%%
graph LR
    A["📡 Router"] -->|WAN| B["🔀 Switch"]
    B --> C["🖥️ PC 1"]
    B --> D["🖥️ PC 2"]
    B --> E["🗄️ Server"]

    style A fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#000
    style B fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style C fill:#90caf9,stroke:#1976d2,stroke-width:2px,color:#000
    style D fill:#90caf9,stroke:#1976d2,stroke-width:2px,color:#000
    style E fill:#b3e5fc,stroke:#0288d1,stroke-width:2px,color:#000
```

---

## 🌿 2. Forest Green (`forest`)
Natural, segar — cocok untuk **biologi & lingkungan**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e8f5e9', 'primaryTextColor': '#000', 'lineColor': '#2e7d32'}}}%%
graph TD
    A["🌱 Fotosintesis"] --> B["💧 Air"]
    A --> C["☀️ Cahaya"]
    A --> D["💨 CO2"]
    A --> E["🍃 Glukosa"]

    style A fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
    style B fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000
    style C fill:#dcedc8,stroke:#558b2f,stroke-width:2px,color:#000
    style D fill:#a5d6a7,stroke:#388e3c,stroke-width:2px,color:#000
    style E fill:#f1f8e9,stroke:#689f38,stroke-width:2px,color:#000
```

---

## 🌅 3. Sunset Warm (`sunset`)
Hangat, energik — cocok untuk **proses & alur kerja**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fff3e0', 'primaryTextColor': '#000', 'lineColor': '#e65100'}}}%%
graph LR
    A["📝 Input"] --> B["⚙️ Proses"]
    B --> C{"✅ Valid?"}
    C -->|Ya| D["💾 Simpan"]
    C -->|Tidak| E["❌ Tolak"]

    style A fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    style B fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px,color:#000
    style C fill:#ffcc80,stroke:#f57c00,stroke-width:2px,color:#000
    style D fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#000
    style E fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#000
```

---

## 🔮 4. Purple Galaxy (`galaxy`)
Elegan, modern — cocok untuk **arsitektur & sistem**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ede7f6', 'primaryTextColor': '#000', 'lineColor': '#4a148c'}}}%%
graph TD
    A["🌐 Frontend"] --> B["⚡ API Gateway"]
    B --> C["🗄️ Backend"]
    B --> D["🔐 Auth Service"]
    C --> E[("💾 Database")]

    style A fill:#ede7f6,stroke:#4a148c,stroke-width:2px,color:#000
    style B fill:#d1c4e9,stroke:#6a1b9a,stroke-width:2px,color:#000
    style C fill:#b39ddb,stroke:#7b1fa2,stroke-width:2px,color:#000
    style D fill:#e8eaf6,stroke:#304ffe,stroke-width:2px,color:#000
    style E fill:#f3e5f5,stroke:#aa00ff,stroke-width:2px,color:#000
```

---

## 🏢 5. Corporate (`corporate`)
Formal, rapi — cocok untuk **presentasi bisnis & proposal**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#eceff1', 'primaryTextColor': '#000', 'lineColor': '#263238'}}}%%
graph LR
    A["📊 Analisis"] --> B["📋 Perencanaan"]
    B --> C["🔨 Implementasi"]
    C --> D["🧪 Testing"]
    D --> E["🚀 Deploy"]

    style A fill:#eceff1,stroke:#263238,stroke-width:2px,color:#000
    style B fill:#e8eaf6,stroke:#1a237e,stroke-width:2px,color:#000
    style C fill:#cfd8dc,stroke:#37474f,stroke-width:2px,color:#000
    style D fill:#fff8e1,stroke:#ff8f00,stroke-width:2px,color:#000
    style E fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#000
```

---

## 🌈 6. Pastel Rainbow (`rainbow`)
Berwarna, ceria — cocok untuk **edukasi & layer/tingkat**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#bbdefb', 'primaryTextColor': '#000', 'lineColor': '#555'}}}%%
graph TD
    L7["Layer 7: Application"]
    L6["Layer 6: Presentation"]
    L5["Layer 5: Session"]
    L4["Layer 4: Transport"]
    L3["Layer 3: Network"]
    L2["Layer 2: Data Link"]
    L1["Layer 1: Physical"]

    L7 --> L6 --> L5 --> L4 --> L3 --> L2 --> L1

    style L7 fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#000
    style L6 fill:#ffe0b2,stroke:#e65100,stroke-width:2px,color:#000
    style L5 fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#000
    style L4 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#000
    style L3 fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style L2 fill:#d1c4e9,stroke:#6a1b9a,stroke-width:2px,color:#000
    style L1 fill:#f8bbd0,stroke:#ad1457,stroke-width:2px,color:#000
```

---

## 🖤 7. Monochrome (`mono`)
Minimalis, bersih — cocok untuk **dokumen formal & cetak**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fafafa', 'primaryTextColor': '#000', 'lineColor': '#424242'}}}%%
graph LR
    A["Input Data"] --> B["Proses"]
    B --> C{"Validasi"}
    C -->|OK| D["Output"]
    C -->|Gagal| E["Error Log"]

    style A fill:#fafafa,stroke:#212121,stroke-width:2px,color:#000
    style B fill:#eeeeee,stroke:#424242,stroke-width:2px,color:#000
    style C fill:#e0e0e0,stroke:#616161,stroke-width:2px,color:#000
    style D fill:#f5f5f5,stroke:#757575,stroke-width:2px,color:#000
    style E fill:#bdbdbd,stroke:#9e9e9e,stroke-width:2px,color:#000
```

---

## 🍬 8. Candy Pop (`candy`)
Ceria, playful — cocok untuk **infografis & media sosial**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fce4ec', 'primaryTextColor': '#000', 'lineColor': '#e91e63'}}}%%
graph TD
    A["🎯 Goal"] --> B["📚 Belajar"]
    A --> C["💪 Latihan"]
    B --> D["🧠 Pahami"]
    C --> D
    D --> E["🏆 Berhasil!"]

    style A fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#000
    style B fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    style C fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#000
    style D fill:#e0f7fa,stroke:#00bcd4,stroke-width:2px,color:#000
    style E fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
```

## 🌋 9. Volcano (`volcano`)
Dark Red, berani — cocok untuk **keamanan & peringatan**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffebee', 'primaryTextColor': '#000', 'lineColor': '#b71c1c'}}}%%
graph LR
    A["🛡️ Security"] --> B["⚠️ Threat"]
    B --> C["🚨 Alert"]
    
    style A fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
    style B fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px,color:#000
    style C fill:#ef9a9a,stroke:#f44336,stroke-width:2px,color:#000
```

---

## 🌻 10. Sunflower (`sunflower`)
Bright Yellow, cerah — cocok untuk **ideasi & brainstorming**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#fffde7', 'primaryTextColor': '#000', 'lineColor': '#f57f17'}}}%%
mindmap
  root((💡 Ide))
    Inovasi
    Kreativitas
    
    style root fill:#fffde7,stroke:#f57f17,stroke-width:2px,color:#000
```

---

## ☕ 11. Coffee (`coffee`)
Brown Warm, klasik — cocok untuk **sejarah & struktur**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#efebe9', 'primaryTextColor': '#000', 'lineColor': '#3e2723'}}}%%
graph TD
    A["🏛️ Fondasi"] --> B["🧱 Struktur"]
    
    style A fill:#efebe9,stroke:#3e2723,stroke-width:2px,color:#000
    style B fill:#d7ccc8,stroke:#5d4037,stroke-width:2px,color:#000
```

---

## 🧊 12. Ice (`ice`)
Cool Cyan, segar — cocok untuk **data & analitik**.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e0f7fa', 'primaryTextColor': '#000', 'lineColor': '#006064'}}}%%
graph LR
    A["📊 Data"] --> B["📈 Insight"]
    
    style A fill:#e0f7fa,stroke:#006064,stroke-width:2px,color:#000
    style B fill:#b2ebf2,stroke:#0097a7,stroke-width:2px,color:#000
```

---

## Quick Reference

| Tema | Keyword | Cocok Untuk |
|------|---------|-------------|
| 🌊 Ocean Blue | `ocean` | Jaringan, Teknologi |
| 🌿 Forest Green | `forest` | Biologi, Lingkungan |
| 🌅 Sunset Warm | `sunset` | Proses, Alur Kerja |
| 🔮 Purple Galaxy | `galaxy` | Arsitektur, Sistem |
| 🏢 Corporate | `corporate` | Bisnis, Proposal |
| 🌈 Pastel Rainbow | `rainbow` | Edukasi, Layer |
| 🖤 Monochrome | `mono` | Dokumen Formal |
| 🍬 Candy Pop | `candy` | Infografis, Fun |
| 🌋 Volcano | `volcano` | Keamanan, Peringatan |
| 🌻 Sunflower | `sunflower` | Ideasi, Brainstorming |
| ☕ Coffee | `coffee` | Sejarah, Struktur Klasik |
| 🧊 Ice | `ice` | Data, Analitik |
