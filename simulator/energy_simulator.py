import time
import random
from datetime import datetime

print("EnerVision AI Simulator Started")

while True:
    telemetry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "power_usage": round(random.uniform(2.0, 8.0), 2),
        "battery_level": random.randint(40, 100),
        "solar_output": round(random.uniform(0.5, 5.0), 2)
    }

    print(telemetry)
    time.sleep(2)