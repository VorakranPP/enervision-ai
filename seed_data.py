# seed_data.py
import sqlite3
import numpy as np
from datetime import datetime, timedelta

conn = sqlite3.connect("backend/energy_data.db")
cursor = conn.cursor()

start = datetime.now() - timedelta(days=30)
records = []

for i in range(30 * 24 * 6):  # ทุก 10 นาที 30 วัน
    ts = start + timedelta(minutes=i * 10)
    hour = ts.hour

    # Pattern กลางวันใช้ไฟมาก กลางคืนใช้น้อย
    base_power = 3.0
    day_pattern = np.sin((hour - 6) * np.pi / 12) * 2.5
    noise = np.random.normal(0, 0.3)
    power = max(1.0, base_power + day_pattern + noise)

    solar = max(0, np.sin((hour - 6) * np.pi / 12) * 4 + np.random.normal(0, 0.2)) if 6 <= hour <= 18 else 0
    battery = max(20, min(100, 60 + solar * 5 - power * 2 + np.random.normal(0, 2)))

    records.append((
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        round(power, 2),
        int(battery),
        round(solar, 2)
    ))

cursor.executemany(
    "INSERT INTO telemetry (timestamp, power_usage, battery_level, solar_output) VALUES (?, ?, ?, ?)",
    records
)

conn.commit()
conn.close()
print(f"Inserted {len(records)} records")
