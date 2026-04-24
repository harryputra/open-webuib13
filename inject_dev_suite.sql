-- Injeksi Developer Tools (GitHub & API Explorer)
INSERT INTO tool (id, user_id, name, type, content, meta, created_at, updated_at)
VALUES 
('t-github', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'GitHub Pro Automator', 'action', 'import os\nimport requests\n\ndef git_push(repo, message):\n    # Logika automasi GitHub menggunakan GITHUB_TOKEN\n    return f"Changes pushed to {repo} with message: {message}"', '{"icon": "github"}', 1713876000, 1713876000),
('t-api-tester', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'API Explorer', 'action', 'import requests\ndef test_endpoint(url, method="GET", data=None):\n    r = requests.request(method, url, json=data)\n    return r.json()', '{"icon": "api"}', 1713876000, 1713876000)
ON CONFLICT (id) DO NOTHING;

-- Skill: Code Formatter & Linter
INSERT INTO skill (id, user_id, name, content, meta, created_at, updated_at)
VALUES
('s-dev-pro', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'DevPro Toolkit', 'Gunakan library Black dan Flake8 untuk setiap blok kode Python yang dihasilkan.', '{}', 1713876000, 1713876000)
ON CONFLICT (id) DO NOTHING;
