-- Injeksi Prompts
INSERT INTO prompt (id, command, user_id, name, content, created_at, updated_at, is_active)
VALUES 
('p-1', 'lit-review', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'Literature Review Expert', 'Lakukan tinjauan pustaka mendalam untuk topik [TOPIC]. Fokus pada 3 tahun terakhir dan identifikasi kesenjangan riset (research gaps). Berikan sitasi jika perlu.', 1713876000, 1713876000, true),
('p-2', 'coder-architect', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'System Architecture Designer', 'Rancang arsitektur sistem untuk [NAMA PROYEK] menggunakan pola Microservices. Berikan diagram MermaidJS dan jelaskan pilihan tumpukan teknologinya.', 1713876000, 1713876000, true)
ON CONFLICT (command) DO NOTHING;

-- Injeksi Functions (IEEE Filter)
INSERT INTO function (id, user_id, name, type, content, meta, created_at, updated_at, is_active, is_global)
VALUES
('f-1', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'IEEE Academic Formatter', 'filter', 'class Filter:\n    def inlet(self, body, __user__=None):\n        if "messages" in body:\n            body["messages"][-1]["content"] += "\n\n(FORMAT: Tulis dalam gaya akademik IEEE standard)." \n        return body', '{}', 1713876000, 1713876000, true, true)
ON CONFLICT (id) DO NOTHING;
