"""
SAPBA Mermaid Fixer & Style Injector
- Outlet: Fixes dark mode visibility for any Mermaid block
- Inlet: Intercepts [SAPBA_DIAGRAM_TRIGGER] to inject style palettes invisibly
"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

FILTER_CODE = r'''"""
title: SAPBA Mermaid Enhancer
author: Antigravity Architect
description: Auto-inject light theme for dark mode & manage diagram styles invisibly
version: 1.1.0
"""

import re
import logging
from typing import Optional
from pydantic import BaseModel

log = logging.getLogger(__name__)

THEME_DIRECTIVE = "%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e3f2fd', 'primaryTextColor': '#000000', 'primaryBorderColor': '#333', 'lineColor': '#555555', 'secondaryColor': '#fff3e0', 'tertiaryColor': '#e8f5e9', 'background': '#ffffff', 'mainBkg': '#ffffff', 'nodeBorder': '#333', 'clusterBkg': '#f5f5f5', 'clusterBorder': '#999', 'titleColor': '#000', 'edgeLabelBackground': '#ffffff'}}}%%"

STYLE_INSTRUCTIONS = """
## 🎨 INSTRUKSI TEMA WARNA DIAGRAM MERMAID

Terapkan tema sesuai permintaan user. Jika "semua", buat 3 tema berbeda.

1. `ocean` (Ocean Blue): style Node fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px,color:#000
2. `forest` (Forest Green): style Node fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
3. `sunset` (Sunset Warm): style Node fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
4. `galaxy` (Purple Galaxy): style Node fill:#ede7f6,stroke:#4a148c,stroke-width:2px,color:#000
5. `corporate` (Corporate): style Node fill:#eceff1,stroke:#263238,stroke-width:2px,color:#000
6. `rainbow` (Pastel Rainbow): Gunakan warna pastel pelangi berbeda tiap node, pastikan color:#000
7. `mono` (Monochrome): style Node fill:#fafafa,stroke:#212121,stroke-width:2px,color:#000
8. `candy` (Candy Pop): style Node fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#000
9. `volcano` (Dark Red): style Node fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
10. `sunflower` (Bright Yellow): style Node fill:#fffde7,stroke:#f57f17,stroke-width:2px,color:#000
11. `coffee` (Brown Warm): style Node fill:#efebe9,stroke:#3e2723,stroke-width:2px,color:#000
12. `ice` (Cool Cyan): style Node fill:#e0f7fa,stroke:#006064,stroke-width:2px,color:#000

ATURAN WAJIB:
1. Mulai dengan directive: %%{init: {'theme': 'base', 'themeVariables': {...}}}%%
2. SELALU tambahkan `color:#000` di setiap `style` node
3. Gunakan label Bahasa Indonesia & tambahkan emoji yang relevan.
"""

class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        log.warning("SAPBA Mermaid Enhancer v1.1: Loaded!")

    def _fix_mermaid_block(self, block):
        lines = block.strip().split("\\n")
        if any("%%{init:" in line for line in lines):
            return block
        return THEME_DIRECTIVE + "\\n" + block.strip()

    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        try:
            messages = body.get("messages", [])
            if not messages:
                return body

            last_msg = messages[-1]
            content = last_msg.get("content", "")
            
            if "[SAPBA_DIAGRAM_TRIGGER]" in content:
                log.warning("SAPBA Mermaid Enhancer: Intercepted trigger, injecting styles...")
                # Remove the trigger text from the user's visible message to the AI
                content = content.replace("[SAPBA_DIAGRAM_TRIGGER]", "").strip()
                last_msg["content"] = content
                
                # Prepend the system instructions to the first message or create a system message
                # We inject it invisibly into the context
                injected = False
                for msg in messages:
                    if msg.get("role") == "system":
                        msg["content"] += "\\n\\n" + STYLE_INSTRUCTIONS
                        injected = True
                        break
                
                if not injected:
                    messages.insert(0, {"role": "system", "content": "Kamu adalah Diagram Architect Pro." + STYLE_INSTRUCTIONS})
                
                body["messages"] = messages
                
        except Exception as e:
            log.error(f"SAPBA Mermaid Enhancer inlet error: {e}")
            
        return body

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        try:
            messages = body.get("messages", [])
            if not messages:
                return body

            last_msg = messages[-1]
            content = last_msg.get("content", "")
            if not isinstance(content, str) or "```mermaid" not in content:
                return body

            parts = content.split("```mermaid")
            if len(parts) <= 1:
                return body

            new_content = parts[0]
            for i, part in enumerate(parts[1:]):
                end_idx = part.find("```")
                if end_idx == -1:
                    new_content += "```mermaid" + part
                    continue

                mermaid_code = part[:end_idx]
                rest = part[end_idx:]
                fixed = self._fix_mermaid_block(mermaid_code)
                new_content += "```mermaid\\n" + fixed + "\\n" + rest

            if new_content != content:
                body["messages"][-1]["content"] = new_content

        except Exception as e:
            log.error(f"SAPBA Mermaid Enhancer outlet error: {e}")

        return body
'''

# Update the filter
payload = {
    "id": "sapba_mermaid_fixer",
    "name": "SAPBA Mermaid Enhancer",
    "meta": {"description": "Auto-inject dark mode fixes and invisible style rules for diagrams"},
    "content": FILTER_CODE,
    "type": "filter",
    "is_active": True,
    "is_global": True
}

r = requests.get(f'{BASE_URL}/api/v1/functions/id/sapba_mermaid_fixer', headers=H)
if r.ok:
    print("Updating Filter...")
    r2 = requests.post(f'{BASE_URL}/api/v1/functions/id/sapba_mermaid_fixer/update', headers=H, json=payload)
else:
    print("Creating Filter...")
    r2 = requests.post(f'{BASE_URL}/api/v1/functions/create', headers=H, json=payload)
print(f"Status: {r2.status_code}")
