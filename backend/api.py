from fastapi import FastAPI
import sqlite3
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
##from fastapi import Depends, HTTPException
##from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
# บนสุดของไฟล์
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI(title="EnerVision AI API")

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "energy_data.db"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ตั้งค่า OAuth2 token scheme (อ่าน Bearer token จาก header) และ bcrypt hashing context
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
# สร้าง JWT access token จาก dict ข้อมูล (เช่น {"sub": username})
# กำหนดอายุ 30 นาที เซ็นด้วย SECRET_KEY — คืนค่า token string
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ถอดรหัส JWT token จาก Authorization header — ดึง username (sub) ออกมา
# ถ้า token ผิดหรือหมดอายุ → raise HTTP 401 | ใช้เป็น Depends() ใน protected endpoints
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency สำหรับ endpoint ที่ต้องการสิทธิ์ admin เท่านั้น
# ตรวจ role จาก database — ถ้าไม่ใช่ admin → raise HTTP 403
def require_admin(current_user: str = Depends(verify_token)):

    user = get_user_from_db(current_user)

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

# เปรียบเทียบ plaintext password กับ bcrypt hash ใน database — ใช้ passlib verify
# คืนค่า True ถ้าตรงกัน, False ถ้าไม่ตรง
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ค้นหา user จาก database ด้วย username — คืนค่า Row object (dict-like) หรือ None ถ้าไม่พบ
def get_user_from_db(username: str):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

    return user

# สร้าง user ใหม่ใน database — hash password ด้วย bcrypt ก่อน INSERT เสมอ
# ฟังก์ชัน internal เรียกจาก /register endpoint เท่านั้น
def create_user(
    username,
    password,
    role="viewer"
):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    hashed_password = pwd_context.hash(password)
    cursor.execute("""
    INSERT INTO users (
        username,
        password,
        role
    )
    VALUES (?,?,?)
    """, (username, hashed_password, role))

    connection.commit()
    connection.close()

# POST /register — สร้าง user ใหม่ (admin เท่านั้น)
# ตรวจ username ซ้ำก่อน → ถ้าซ้ำ raise HTTP 400
@app.post("/register")
def register(
    username: str,
    password: str,
    role: str = "viewer",
    current_user: str = Depends(require_admin)
):

    existing_user = get_user_from_db(username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    create_user(
        username,
        password,
        role
    )

    return {
        "message": f"User {username} created successfully",
        "role": role,
        "created_by": current_user
    }

# POST /token — ตรวจสอบ username/password แล้วคืน JWT access token
# รับข้อมูลเป็น form data (OAuth2PasswordRequestForm) ไม่ใช่ JSON
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = get_user_from_db(form_data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    if not verify_password(form_data.password, user["password"]):
    ##if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

 
# GET /users — ดึงรายชื่อ user ทั้งหมด (admin เท่านั้น) คืน list of {username, role}
@app.get("/users")
def get_users(

    current_user:
    str = Depends(
        require_admin
    )

):

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()


    cursor.execute(

        """
        SELECT
        username,
        role

        FROM users
        """

    )


    users = cursor.fetchall()


    connection.close()


    return [

        {

            "username":
            user[0],

            "role":
            user[1]

        }

        for user in users

    ]


# GET /me — ดึงข้อมูล profile ของ user ที่ login อยู่ (อ่าน username จาก JWT)
@app.get("/me")
def get_me(current_user: str = Depends(verify_token)):

    user = get_user_from_db(current_user)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "username": user["username"],
        "role": user["role"] if "role" in user.keys() else "viewer"
    }

# GET /telemetry — ดึงข้อมูล IoT telemetry ล่าสุด 20 รายการ เรียงใหม่ไปเก่า
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

# GET /summary — คำนวณสรุปพลังงานจาก telemetry ทั้งหมด: avg/peak power, lowest battery
# CO₂ = average_power × 0.4 kg/kWh (ค่ากริดไฟฟ้าเฉลี่ย)
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

# PUT /users/{username}/role — เปลี่ยน role ของ user (admin เท่านั้น)
# role รับค่า: 'admin' หรือ 'viewer'
@app.put("/users/{username}/role")

def update_role(

    username: str,

    role: str,

    current_user:

    str = Depends(

        require_admin

    )

):


    connection = sqlite3.connect(

        DB_PATH

    )


    cursor = connection.cursor()


    cursor.execute(

        """

        UPDATE users

        SET role=?

        WHERE username=?

        """,

        (

            role,

            username

        )

    )


    connection.commit()

    connection.close()


    return {

        "message":

        f"{username} updated to {role}"

    }
# DELETE /users/{username} — ลบ user จาก database (admin เท่านั้น)
# ป้องกันลบตัวเองจาก dashboard UI (ไม่ได้ block ที่ API level)
@app.delete("/users/{username}")
def delete_user(
    username: str,
    current_user: str = Depends(require_admin)
):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )

    connection.commit()
    connection.close()

    return {
        "message": f"{username} deleted"
    }


# GET /alerts — ตรวจสอบ telemetry 20 รายการล่าสุด สร้าง alert list
# เงื่อนไข: power_usage > 7 kW, battery_level < 30%, solar_output < 1 kW
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

# GET /recommendations — สร้างคำแนะนำ AI จาก telemetry ล่าสุด 20 รายการ
# dedup ด้วย set() เพื่อไม่ให้คำแนะนำซ้ำกัน
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

# GET /system-status — ตรวจสถานะระบบจาก telemetry ล่าสุด 1 รายการ
# คืน: healthy / warning / critical — ใช้เป็น Docker healthcheck ด้วย
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

# GET /trend-analysis — วิเคราะห์แนวโน้ม 50 รายการแรก
# เปรียบเทียบ power_usage แรกสุด vs ล่าสุด → increasing / decreasing / stable
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