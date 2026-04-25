import sqlite3
import os

db_path = '/app/backend/data/webui.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE model SET base_model_id = 'gemma4:latest' WHERE id LIKE '%antigravity%' OR id LIKE '%sim-kkn%'")
    conn.commit()
    print(f"SUCCESS: {cursor.rowcount} models updated to gemma4:latest.")
    conn.close()
else:
    print(f"ERROR: DB not found at {db_path}")
