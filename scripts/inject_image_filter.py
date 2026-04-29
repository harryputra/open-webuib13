"""
SAPBA Image Filter v8 - Gemini Nano Banana Integration
Uses Google Gemini API for high-quality image generation
Falls back to Pollinations.ai if Gemini fails (rate limit, etc.)
"""
import requests, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'http://localhost:3013'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

GEMINI_API_KEY = "AIzaSyAZctHDG38zQ7mMhRzLcSKiyMHF3rYDox8"

FILTER_CODE = (
    '"""\n'
    'title: SAPBA Auto-Illustrator Pipeline\n'
    'author: Antigravity Architect\n'
    'description: Auto-generate educational images using Gemini Nano Banana with Pollinations fallback\n'
    'version: 8.0.0\n'
    '"""\n'
    '\n'
    'import re\n'
    'import urllib.parse\n'
    'import random\n'
    'import base64\n'
    'import json\n'
    'import logging\n'
    'import traceback\n'
    'from typing import Optional\n'
    'from pydantic import BaseModel, Field\n'
    '\n'
    'log = logging.getLogger(__name__)\n'
    '\n'
    '\n'
    'class Filter:\n'
    '    class Valves(BaseModel):\n'
    f'        gemini_api_key: str = Field(default="{GEMINI_API_KEY}", description="Google Gemini API Key")\n'
    '        gemini_model: str = Field(default="gemini-2.5-flash-image", description="Gemini image model")\n'
    '        fallback_to_pollinations: bool = Field(default=True, description="Fallback to Pollinations if Gemini fails")\n'
    '\n'
    '    def __init__(self):\n'
    '        self.valves = self.Valves()\n'
    '        log.warning("SAPBA v8 (Gemini Nano Banana): Loaded!")\n'
    '\n'
    '    def _get_image_gemini(self, desc):\n'
    '        """Generate image using Gemini Nano Banana API"""\n'
    '        import requests as req\n'
    '        try:\n'
    '            api_key = self.valves.gemini_api_key\n'
    '            model = self.valves.gemini_model\n'
    '            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"\n'
    '            \n'
    '            prompt = (\n'
    '                f"Create a professional educational textbook illustration for: {desc}. "\n'
    '                f"Style: clean, labeled diagram, professional 2D vector art, "\n'
    '                f"high contrast, white background, suitable for academic textbook. "\n'
    '                f"Include clear labels and annotations in the illustration."\n'
    '            )\n'
    '            \n'
    '            payload = {\n'
    '                "contents": [{"parts": [{"text": prompt}]}],\n'
    '                "generationConfig": {"responseModalities": ["IMAGE"]}\n'
    '            }\n'
    '            \n'
    '            log.warning(f"SAPBA v8: Gemini request for: {desc[:60]}...")\n'
    '            r = req.post(url, json=payload, timeout=60)\n'
    '            log.warning(f"SAPBA v8: Gemini response: {r.status_code}")\n'
    '            \n'
    '            if r.status_code == 200:\n'
    '                data = r.json()\n'
    '                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])\n'
    '                for part in parts:\n'
    '                    if "inlineData" in part:\n'
    '                        mime = part["inlineData"].get("mimeType", "image/png")\n'
    '                        b64 = part["inlineData"]["data"]\n'
    '                        log.warning(f"SAPBA v8: Gemini image received! ~{len(b64)*3//4//1024} KB")\n'
    '                        return f"data:{mime};base64,{b64}"\n'
    '                log.warning("SAPBA v8: Gemini returned no image data")\n'
    '            else:\n'
    '                err = r.json().get("error", {}).get("message", "Unknown error")\n'
    '                log.warning(f"SAPBA v8: Gemini error: {err[:150]}")\n'
    '        except Exception as e:\n'
    '            log.error(f"SAPBA v8: Gemini exception: {e}")\n'
    '        return None\n'
    '\n'
    '    def _get_image_pollinations(self, desc):\n'
    '        """Fallback: Generate image using Pollinations.ai"""\n'
    '        import requests as req\n'
    '        try:\n'
    '            style = "educational textbook illustration, clean, professional, labeled diagram"\n'
    '            prompt = f"{desc}, {style}"\n'
    '            encoded = urllib.parse.quote(prompt)\n'
    '            seed = random.randint(1, 999999)\n'
    '            url = f"https://image.pollinations.ai/prompt/{encoded}?model=turbo&seed={seed}&nologo=true"\n'
    '            log.warning(f"SAPBA v8: Pollinations fallback for: {desc[:60]}...")\n'
    '            r = req.get(url, timeout=30)\n'
    '            if r.status_code == 200 and len(r.content) > 500:\n'
    '                b64 = base64.b64encode(r.content).decode("utf-8")\n'
    '                log.warning(f"SAPBA v8: Pollinations OK, {len(r.content)} bytes")\n'
    '                return f"data:image/jpeg;base64,{b64}"\n'
    '        except Exception as e:\n'
    '            log.error(f"SAPBA v8: Pollinations error: {e}")\n'
    '        return None\n'
    '\n'
    '    def _get_image(self, desc):\n'
    '        """Try Gemini first, fallback to Pollinations"""\n'
    '        result = self._get_image_gemini(desc)\n'
    '        if result:\n'
    '            return result\n'
    '        if self.valves.fallback_to_pollinations:\n'
    '            log.warning("SAPBA v8: Falling back to Pollinations...")\n'
    '            return self._get_image_pollinations(desc)\n'
    '        return None\n'
    '\n'
    '    def _extract_tags(self, text):\n'
    '        """Extract [ILUSTRASI: ...] tags using string search (no regex escaping issues)"""\n'
    '        results = []\n'
    '        upper = text.upper()\n'
    '        idx = 0\n'
    '        while True:\n'
    '            pos = upper.find("[ILUSTRASI:", idx)\n'
    '            if pos == -1:\n'
    '                break\n'
    '            end = text.find("]", pos + 11)\n'
    '            if end != -1:\n'
    '                desc = text[pos + 11:end].strip()\n'
    '                if desc:\n'
    '                    results.append((pos, end + 1, desc))\n'
    '            idx = pos + 1\n'
    '        return results\n'
    '\n'
    '    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:\n'
    '        try:\n'
    '            log.warning("SAPBA v8: outlet() called")\n'
    '            messages = body.get("messages", [])\n'
    '            if len(messages) < 2:\n'
    '                return body\n'
    '\n'
    '            last_ai = messages[-1]\n'
    '            ai_content = last_ai.get("content", "")\n'
    '            if not isinstance(ai_content, str):\n'
    '                return body\n'
    '\n'
    '            modified = False\n'
    '            processed = set()\n'
    '\n'
    '            # PASS 1: Replace [ILUSTRASI:...] in AI response (inline)\n'
    '            ai_tags = self._extract_tags(ai_content)\n'
    '            if ai_tags:\n'
    '                log.warning(f"SAPBA v8: {len(ai_tags)} tags in AI response")\n'
    '                for pos, end, desc in reversed(ai_tags):\n'
    '                    if desc.lower() not in processed:\n'
    '                        data_uri = self._get_image(desc)\n'
    '                        if data_uri:\n'
    '                            img_md = f"\\n\\n![{desc}]({data_uri})\\n*Ilustrasi: {desc}*\\n"\n'
    '                            ai_content = ai_content[:pos] + img_md + ai_content[end:]\n'
    '                            modified = True\n'
    '                            processed.add(desc.lower())\n'
    '                            log.warning(f"SAPBA v8: Replaced inline: {desc}")\n'
    '                        break  # Only one at a time\n'
    '\n'
    '            # PASS 2: Check last user message for tags\n'
    '            for msg in reversed(messages[:-1]):\n'
    '                if msg.get("role") == "user":\n'
    '                    user_content = msg.get("content", "")\n'
    '                    if isinstance(user_content, str):\n'
    '                        user_tags = self._extract_tags(user_content)\n'
    '                        for pos, end, desc in user_tags:\n'
    '                            if desc.lower() not in processed:\n'
    '                                data_uri = self._get_image(desc)\n'
    '                                if data_uri:\n'
    '                                    ai_content += f"\\n\\n---\\n\\n![{desc}]({data_uri})\\n*Ilustrasi: {desc}*\\n"\n'
    '                                    modified = True\n'
    '                                    processed.add(desc.lower())\n'
    '                                    log.warning(f"SAPBA v8: Appended from user: {desc}")\n'
    '                                break\n'
    '                    break\n'
    '\n'
    '            if modified:\n'
    '                body["messages"][-1]["content"] = ai_content\n'
    '                log.warning("SAPBA v8: Content updated!")\n'
    '            else:\n'
    '                log.warning("SAPBA v8: No modifications")\n'
    '\n'
    '        except Exception as e:\n'
    '            log.error(f"SAPBA v8 ERROR: {e}")\n'
    '            log.error(traceback.format_exc())\n'
    '\n'
    '        return body\n'
)

payload = {
    "id": "sapba_image_filter",
    "name": "SAPBA Auto-Illustrator (Gemini)",
    "meta": {"description": "Educational image gen via Gemini Nano Banana + Pollinations fallback"},
    "content": FILTER_CODE,
    "type": "filter",
    "is_active": True,
    "is_global": True
}

r = requests.get(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter', headers=HEADERS)
if r.ok:
    print("Updating to v8 (Gemini Nano Banana)...")
    r2 = requests.post(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter/update', headers=HEADERS, json=payload)
    print(f"  Status: {r2.status_code}")
    if not r2.ok:
        print(f"  Error: {r2.text[:300]}")
else:
    r2 = requests.post(f'{BASE_URL}/api/v1/functions/create', headers=HEADERS, json=payload)
    print(f"  Create: {r2.status_code}")

# Ensure active+global
r3 = requests.get(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter', headers=HEADERS)
d = r3.json()
if not d.get('is_active'):
    requests.post(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter/toggle', headers=HEADERS)
if not d.get('is_global'):
    requests.post(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter/toggle/global', headers=HEADERS)

r4 = requests.get(f'{BASE_URL}/api/v1/functions/id/sapba_image_filter', headers=HEADERS)
d2 = r4.json()
print(f"Final: active={d2.get('is_active')}, global={d2.get('is_global')}")

# Verify
c = d2.get('content', '')
has_gemini = 'generativelanguage.googleapis.com' in c
has_fallback = 'pollinations' in c
has_key = GEMINI_API_KEY[:10] in c
print(f"Gemini endpoint: {has_gemini}")
print(f"Pollinations fallback: {has_fallback}")
print(f"API key embedded: {has_key}")
