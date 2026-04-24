-- Injeksi Knowledge Collections
INSERT INTO knowledge (id, user_id, name, description, created_at, updated_at)
VALUES 
('k-ai', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'AI & Machine Learning Repository', 'Koleksi makalah, dataset, dan teori terkait Deep Learning, Neural Networks, dan AI Generatif.', 1713876000, 1713876000),
('k-enterprise', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'Enterprise Systems Architecture', 'Dokumentasi arsitektur sistem skala besar, Microservices, dan infrastruktur Big Data.', 1713876000, 1713876000),
('k-iot', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'IoT & Embedded Systems', 'Fokus pada riset Smart Systems, protokol MQTT/HTTP, dan integrasi hardware-software.', 1713876000, 1713876000),
('k-academic', 'ea299ab9-51d8-4b6f-af77-7ead081f4ab4', 'Academic Methodology & IEEE Std', 'Pedoman penulisan ilmiah, struktur jurnal, dan standar etika riset Informatika.', 1713876000, 1713876000)
ON CONFLICT (id) DO NOTHING;
