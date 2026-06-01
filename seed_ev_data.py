# seed_ev_data.py
# สร้างตาราง stations + charging_sessions ใน ev_data.db
# ใส่ข้อมูล 5 สถานี Frankfurt และ sessions ย้อนหลัง 30 วัน — รันครั้งเดียวตอน setup

import sqlite3
import numpy as np
from datetime import datetime, timedelta

conn = sqlite3.connect("backend/ev_data.db")
cursor = conn.cursor()

# สร้าง tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    max_power_kw REAL,
    status TEXT
);

CREATE TABLE IF NOT EXISTS charging_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    timestamp TEXT,
    soc_start REAL,
    soc_end REAL,
    energy_delivered_kwh REAL,
    cost_eur REAL,
    carbon_saved_kg REAL,
    duration_min INTEGER,
    status TEXT
);
""")

# 5 Stations ในแฟรงก์เฟิร์ต
stations = [
    (1, "Frankfurt Hauptbahnhof",     50.1069, 8.6634, 150.0, "Available"),
    (2, "Frankfurt Messe",            50.1109, 8.6476, 100.0, "Charging"),
    (3, "Frankfurt Airport",          50.0379, 8.5622, 350.0, "Charging"),
    (4, "Frankfurt Sachsenhausen",    50.0988, 8.6833, 50.0,  "Available"),
    (5, "Frankfurt Ostend",           50.1136, 8.7147, 100.0, "Offline"),
]

cursor.executemany(
    "INSERT OR REPLACE INTO stations VALUES (?, ?, ?, ?, ?, ?)",
    stations
)

# จำลอง charging sessions ย้อนหลัง 30 วัน
start = datetime.now() - timedelta(days=30)
records = []

for day in range(30):
    for station_id in range(1, 6):

        # แต่ละ station มี 3-8 sessions ต่อวัน
        sessions_per_day = np.random.randint(3, 9)

        for _ in range(sessions_per_day):

            ts = start + timedelta(
                days=day,
                hours=np.random.randint(6, 22),
                minutes=np.random.randint(0, 59)
            )

            soc_start = round(np.random.uniform(10, 40), 1)
            soc_end = round(np.random.uniform(70, 100), 1)
            energy = round((soc_end - soc_start) * 0.6, 2)  # ~60kWh battery
            cost = round(energy * 0.35, 2)  # €0.35 per kWh
            carbon_saved = round(energy * 0.21, 2)  # 0.21 kg CO₂ saved per kWh vs petrol
            duration = int(energy / (stations[station_id - 1][4] / 60))

            records.append((
                station_id,
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                soc_start,
                soc_end,
                energy,
                cost,
                carbon_saved,
                duration,
                "Completed"
            ))

cursor.executemany("""
    INSERT INTO charging_sessions
    (station_id, timestamp, soc_start, soc_end,
     energy_delivered_kwh, cost_eur, carbon_saved_kg, duration_min, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", records)

conn.commit()
conn.close()
print(f"✅ Inserted {len(records)} charging sessions across 5 stations")