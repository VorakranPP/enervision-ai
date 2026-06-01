# generate_sample_csv.py
# สร้างไฟล์ sample_energy.csv สำหรับทดสอบ Tab 2 (Upload & AI Analysis)
# output: 7 วัน ทุก 15 นาที มี columns: timestamp, power_usage, solar_output, battery_level, site, temperature_c

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

start = datetime.now() - timedelta(days=7)
records = []

for i in range(7 * 24 * 4):
    ts = start + timedelta(minutes=i * 15)
    hour = ts.hour
    base_power = 3.0
    day_pattern = np.sin((hour - 6) * np.pi / 12) * 2.5
    noise = np.random.normal(0, 0.3)
    power = max(0.5, base_power + day_pattern + noise)
    solar = max(0, np.sin((hour - 6) * np.pi / 12) * 4 + np.random.normal(0, 0.2)) if 6 <= hour <= 18 else 0
    battery = max(20, min(100, 60 + solar * 5 - power * 2 + np.random.normal(0, 2)))

    records.append({
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "power_usage": round(power, 2),
        "solar_output": round(solar, 2),
        "battery_level": int(battery),
        "site": f"Site-{np.random.choice(['A', 'B', 'C'])}",
        "temperature_c": round(np.random.uniform(20, 35), 1)
    })

df = pd.DataFrame(records)
df.to_csv("sample_energy.csv", index=False)
print(f"✅ Generated {len(records)} rows")
