import requests, sys, io, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API = "AIzaSyAZctHDG38zQ7mMhRzLcSKiyMHF3rYDox8"

# Test 1: Quick text to verify key works
print("=== Test 1: API Key validity ===")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API}"
r = requests.post(url, json={"contents":[{"parts":[{"text":"Say OK"}]}]}, timeout=15)
print(f"  Text model: {r.status_code}")
if r.status_code == 200:
    print("  [OK] API key is valid!")
else:
    print(f"  Error: {r.text[:200]}")

# Test 2: Image generation
print("\n=== Test 2: Image Generation (Nano Banana) ===")
url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API}"
payload = {
    "contents": [{"parts": [{"text": "Create a clean educational diagram showing OSI 7-layer network model with colored layers and labels. Professional textbook style."}]}],
    "generationConfig": {"responseModalities": ["IMAGE"]}
}
print("  Sending image request...")
r2 = requests.post(url2, json=payload, timeout=90)
print(f"  Status: {r2.status_code}")

if r2.status_code == 200:
    data = r2.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for part in parts:
        if "inlineData" in part:
            mime = part["inlineData"].get("mimeType", "image/png")
            b64 = part["inlineData"]["data"]
            img = base64.b64decode(b64)
            with open("gemini_test_new_key.png", "wb") as f:
                f.write(img)
            print(f"  IMAGE: {mime}, {len(img)} bytes")
            print(f"  Saved to gemini_test_new_key.png")
            print("\n  [SUCCESS] Gemini Nano Banana IMAGE GENERATION WORKS!")
        elif "text" in part:
            print(f"  Text: {part['text'][:100]}")
else:
    err = r2.json().get("error", {}).get("message", r2.text[:300])
    print(f"  Error: {err[:300]}")
