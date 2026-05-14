from fastapi import FastAPI
import sqlite3
from pathlib import Path

app = FastAPI(title="EnerVision AI API")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy_data.db"


@app.get("/")
def read_root():
    return {"message": "EnerVision AI API is running"}


@app.get("/telemetry")
def get_telemetry():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM telemetry
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]