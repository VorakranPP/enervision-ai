# database.py
# สร้างตาราง telemetry ใน energy_data.db — รันครั้งเดียวตอน setup
# หลังรันแล้ว table จะอยู่ถาวร (CREATE TABLE IF NOT EXISTS)

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy_data.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    power_usage REAL,
    battery_level INTEGER,
    solar_output REAL
)
""")

connection.commit()
connection.close()

print(f"Database and telemetry table created successfully at {DB_PATH}")