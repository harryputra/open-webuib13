import requests, sys, io, time, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API = "AIzaSyD0qKtrnkDW3kyaQvHSVUm94E536IKSJ-U"

print("Waiting 60s for rate limit reset...")
time.sleep(60)

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API}"
payload = {
    "contents": [{"parts": [{"text": "Draw a simple red circle on white background"}]}],
    "generationConfig": {"responseModalities": ["IMAGE"]}
}

print("Sending request...")
r = requests.post(url, json=payload, timeout=60)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    data = r.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    print(f"Parts count: {len(parts)}")
    for part in parts:
        if "inlineData" in part:
            b64 = part["inlineData"]["data"]
            img = base64.b64decode(b64)
            with open("circle_test.png", "wb") as f:
                f.write(img)
            print(f"IMAGE saved! {len(img)} bytes")
    print("[SUCCESS]")
else:
    data = r.json()
    msg = data.get("error", {}).get("message", "?")
    print(f"Error: {msg[:300]}")
    
    # Check if it's a permanent quota issue
    if "limit: 0" in msg:
        print("\n[INFO] Your API key has limit:0 for image generation.")
        print("This means you need to ENABLE BILLING on Google Cloud Console.")
        print("Steps:")
        print("  1. Go to https://console.cloud.google.com/billing")
        print("  2. Link a billing account to your project")
        print("  3. Or go to https://aistudio.google.com/apikey and create a NEW key")
