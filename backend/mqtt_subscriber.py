import paho.mqtt.client as mqtt
import sqlite3
import json
from pathlib import Path

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "enervision/telemetry"


def save_to_database(data):

    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "energy_data.db"

    connection = sqlite3.connect("backend/energy_data.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO telemetry (
        timestamp,
        power_usage,
        battery_level,
        solar_output
    )
    VALUES (?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["power_usage"],
        data["battery_level"],
        data["solar_output"]
    ))

    connection.commit()
    connection.close()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):

    payload = msg.payload.decode()

    print("Received:", payload)

    data = json.loads(payload)

    save_to_database(data)

    print("Saved to database")


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("EnerVision AI Subscriber Started")

client.loop_forever()