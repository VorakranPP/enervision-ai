from fastapi import FastAPI
import sqlite3
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
##from fastapi import Depends, HTTPException
##from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI(title="EnerVision AI API")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy_data.db"
SECRET_KEY = "enervision-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_user = {
    "username": "admin",
    "password": "admin123"
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.get("/")
def read_root():
    return {
        "message": "EnerVision AI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EnerVision AI API"
    }

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

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


##@app.get("/summary")
##def get_summary():
@app.get("/summary")
def get_summary(current_user: str = Depends(verify_token)):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM telemetry
    """)

    rows = cursor.fetchall()
    connection.close()

    if not rows:
        return {
            "message": "No telemetry data found"
        }

    power_values = [row["power_usage"] for row in rows]
    battery_values = [row["battery_level"] for row in rows]

    average_power = sum(power_values) / len(power_values)
    peak_power = max(power_values)
    lowest_battery = min(battery_values)

    carbon_emission = average_power * 0.4

    return {
        "total_records": len(rows),
        "average_power_usage": round(average_power, 2),
        "peak_power_usage": round(peak_power, 2),
        "lowest_battery_level": lowest_battery,
        "estimated_co2_emission": round(carbon_emission, 2)
    }

@app.get("/alerts")
def get_alerts(current_user: str = Depends(verify_token)):
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

    alerts = []

    for row in rows:

        if row["power_usage"] > 7:
            alerts.append({
                "type": "High Power Usage",
                "value": row["power_usage"],
                "message": "Power usage exceeded safe threshold"
            })

        if row["battery_level"] < 30:
            alerts.append({
                "type": "Low Battery",
                "value": row["battery_level"],
                "message": "Battery level is critically low"
            })

        if row["solar_output"] < 1:
            alerts.append({
                "type": "Low Solar Output",
                "value": row["solar_output"],
                "message": "Solar production is lower than expected"
            })

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }

@app.get("/recommendations")
def get_recommendations(current_user: str = Depends(verify_token)):

    recommendations = []

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

    for row in rows:

        if row["power_usage"] > 7:
            recommendations.append(
                "Reduce HVAC usage during peak hours"
            )

        if row["battery_level"] < 30:
            recommendations.append(
                "Schedule battery charging immediately"
            )

        if row["solar_output"] < 1:
            recommendations.append(
                "Inspect solar panels for possible shading or faults"
            )

    recommendations = list(set(recommendations))

    return {
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }

@app.get("/system-status")
def get_system_status(current_user: str = Depends(verify_token)):

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM telemetry
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    connection.close()

    if not row:
        return {
            "status": "unknown",
            "message": "No telemetry data available"
        }

    status = "healthy"

    if row["power_usage"] > 8:
        status = "critical"

    elif row["battery_level"] < 30:
        status = "warning"

    elif row["solar_output"] < 1:
        status = "warning"

    return {
        "status": status,
        "latest_power_usage": row["power_usage"],
        "latest_battery_level": row["battery_level"],
        "latest_solar_output": row["solar_output"]
    }

@app.get("/trend-analysis")
def trend_analysis(current_user: str = Depends(verify_token)):

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM telemetry
        ORDER BY id ASC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    connection.close()

    if len(rows) < 2:
        return {
            "message": "Not enough telemetry data"
        }

    first_power = rows[0]["power_usage"]
    last_power = rows[-1]["power_usage"]

    trend = "stable"

    if last_power > first_power:
        trend = "increasing"

    elif last_power < first_power:
        trend = "decreasing"

    return {
        "trend": trend,
        "starting_power_usage": first_power,
        "latest_power_usage": last_power,
        "data_points_analyzed": len(rows)
    }