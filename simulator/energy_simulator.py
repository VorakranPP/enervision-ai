# energy_simulator.py
# จำลอง IoT sensor — publish telemetry ปลอมผ่าน MQTT ทุก 2 วินาที
# ใช้สำหรับ dev/demo โดยไม่มี hardware จริง — รันด้วย docker-compose --profile simulator

import time
import random
import json
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "enervision/telemetry"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("EnerVision AI Simulator Started")
print("Publishing telemetry data to MQTT...")

while True:
    telemetry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "power_usage": round(random.uniform(2.0, 8.0), 2),
        "battery_level": random.randint(40, 100),
        "solar_output": round(random.uniform(0.5, 5.0), 2)
    }

    payload = json.dumps(telemetry)
    client.publish(MQTT_TOPIC, payload)

    print("Published:", payload)

    time.sleep(2)

    ##ทุก 2 วินาที script จะ:สร้างข้อมูลใหม่ / จำลอง sensor พลังงาน / ส่ง telemetry ออกมา