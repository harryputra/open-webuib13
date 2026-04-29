import requests, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNDhhMWQ5LTc3NzAtNDQ0Ni05Mzg4LTQxOWU2ZDY5YzEwYSIsImV4cCI6MTc3OTQ5MTIzNywianRpIjoiN2Y3NjhlNmUtMjA0OC00NjMwLTk5NzgtMzM2YzU2ZWE5NThkIiwiaWF0IjoxNzc3MDcyMDM3fQ.eJ7VE_jfFilMPNwefsZNiPdM_drjnSCN5UgDxLFCoGg'
H = {'Authorization': f'Bearer {TOKEN}'}

r = requests.get('http://localhost:3013/api/v1/chats/list', headers=H)
chats = r.json()
cid = chats[0]['id']
title = chats[0].get('title', '?')
print(f"Chat: {title}")

r2 = requests.get(f'http://localhost:3013/api/v1/chats/{cid}', headers=H)
data = r2.json()

# Dump the structure
chat_obj = data.get('chat', {})
print(f"Chat keys: {list(chat_obj.keys())}")

# Check history
history = chat_obj.get('history', {})
if history:
    print(f"History keys: {list(history.keys())[:5]}")
    messages = history.get('messages', {})
    print(f"Messages type: {type(messages)}, len: {len(messages) if messages else 0}")
    
    if isinstance(messages, dict):
        for mid, msg in list(messages.items())[:5]:
            role = msg.get('role', '?')
            content = msg.get('content', '')
            if isinstance(content, str):
                has_b64 = 'data:image' in content
                print(f"  [{role}] len={len(content)} | base64={has_b64}")
                if has_b64:
                    print(f"    >>> FOUND BASE64 IMAGE!")
    elif isinstance(messages, list):
        for msg in messages[:5]:
            role = msg.get('role', '?')
            content = msg.get('content', '')
            if isinstance(content, str):
                has_b64 = 'data:image' in content
                print(f"  [{role}] len={len(content)} | base64={has_b64}")

# Also directly check 'messages' at top level
direct_msgs = chat_obj.get('messages', [])
if direct_msgs:
    print(f"\nDirect messages: {len(direct_msgs)}")
    for msg in direct_msgs[:5]:
        role = msg.get('role', '?')
        content = msg.get('content', '')
        if isinstance(content, str):
            has_b64 = 'data:image' in content
            print(f"  [{role}] len={len(content)} | base64={has_b64}")
