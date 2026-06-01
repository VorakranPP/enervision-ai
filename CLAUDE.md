# CLAUDE.md — EnerVision AI

> โหลดไฟล์นี้ทุกครั้งก่อนเริ่มทำงาน ข้อมูลครอบคลุมทุกสิ่งที่ต้องรู้ ไม่ต้อง explore ไฟล์ซ้ำ

---

## 1. PROJECT IDENTITY

| | |
|---|---|
| **Name** | EnerVision AI v3.2 |
| **Goal** | Portfolio project สมัครงาน MOVOLT Solutions GmbH Frankfurt — Blue Card visa |
| **GitHub** | github.com/VorakranPP/enervision-ai |
| **Docker Hub** | pumpuyz/enervision-api + pumpuyz/enervision-dashboard |
| **Local path** | `/Users/Vorakran.T/Documents/Desktop/EnerVision-AI` |
| **Owner** | Vorakran Trisilanun — Network Engineer / Cloud & Infrastructure / AI & IoT |

**คำอธิบายสั้น:** AI-powered Energy Monitoring & EV Charging Platform สำหรับ industrial + EV charging environment ใช้ IoT telemetry, ML forecasting, multi-role dashboard บน Docker Compose

---

## 2. TECH STACK

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Database | SQLite (2 files) |
| IoT | MQTT paho → HiveMQ public broker |
| Auth | JWT (python-jose) + bcrypt + RBAC (admin/viewer) |
| AI/ML | Prophet (Meta) — 48h forecast + Z-score anomaly |
| Visualization | Plotly |
| Reporting | ReportLab (PDF) |
| Container | Docker + Docker Compose |
| Language | Python 3.11 (.venv ที่ root) |
| CI/CD | GitHub Actions → Docker Hub |

---

## 3. ARCHITECTURE FLOW

```
IoT Sensor / energy_simulator.py
        │ MQTT (topic: enervision/telemetry)
        ▼
HiveMQ public broker (broker.hivemq.com:1883)
        │
        ▼
backend/mqtt_subscriber.py  →  backend/energy_data.db (SQLite)
                                        │
                          ┌─────────────┴──────────────┐
                          ▼                             ▼
               backend/api.py (FastAPI)     dashboard/*.py (Streamlit)
               JWT + RBAC                  อ่าน DB โดยตรงผ่าน db_paths.py
               port 8000                   port 8501
```

**สำคัญ:** Dashboard อ่าน DB โดยตรง (SQLite) สำหรับบางหน้า ไม่ได้ผ่าน API ทุก tab
- Tab 1 (Realtime): ผ่าน API (`/telemetry`, `/summary`, `/alerts` ฯลฯ)
- Tab 4 (EV): อ่าน `ev_data.db` โดยตรง ไม่ผ่าน API
- Tab 3 (Solar): ไม่ใช้ DB เลย — pure calculation

---

## 4. FILE MAP (24 ไฟล์หลัก)

### backend/
| ไฟล์ | หน้าที่ |
|---|---|
| `api.py` | FastAPI ทุก endpoint + JWT auth + RBAC logic |
| `database.py` | สร้างตาราง `telemetry` ใน energy_data.db (รัน 1 ครั้ง) |
| `mqtt_subscriber.py` | subscribe HiveMQ → parse JSON → INSERT telemetry |
| `init_users.py` | สร้าง admin user ครั้งแรก |
| `create_user.py` | helper script สร้าง user เพิ่ม |

### dashboard/
| ไฟล์ | หน้าที่ |
|---|---|
| `dashboard.py` | entry point — login, session state, load 5 tabs |
| `translations.py` | language pack DE/EN — dict `TRANSLATIONS["DE"]` / `["EN"]` |
| `db_paths.py` | constants: `DB_ENERGY`, `DB_EV` (path สู่ SQLite files) |
| `forecast.py` | Prophet forecasting component |
| `alerts.py` | Gmail SMTP email alert (yagmail) |
| `battery.py` | Plotly gauge UI สำหรับแสดง battery level |
| `pdf_report.py` | ReportLab PDF export |
| `styles.py` | CSS inject ใน login page |

### dashboard/tabs/
| ไฟล์ | หน้าที่ |
|---|---|
| `tab_realtime.py` | Tab 1 — real-time energy ผ่าน API + email alert + PDF |
| `tab_upload.py` | Tab 2 — CSV upload + AI analysis (anomaly, forecast, recommend) |
| `tab_solar.py` | Tab 3 — Solar ROI Calculator (อิงข้อมูลเยอรมนี) |
| `tab_ev.py` | Tab 4 — EV Charging Monitor (Frankfurt / MOVOLT 5 สถานี) |
| `tab_admin.py` | Tab 5 — User management (admin only) |
| `tab_upload_B.py` | เวอร์ชัน B ของ upload tab (ยังทดสอบอยู่) |

### root/
| ไฟล์ | หน้าที่ |
|---|---|
| `seed_data.py` | seed telemetry data ลง energy_data.db |
| `seed_ev_data.py` | seed EV session data ลง ev_data.db |
| `generate_sample_csv.py` | สร้าง CSV ตัวอย่างสำหรับทดสอบ tab_upload |
| `simulator/energy_simulator.py` | publish MQTT telemetry data ปลอม |
| `command.py` | helper commands สำหรับ dev |

---

## 5. DATABASE SCHEMA

### `backend/energy_data.db`
```sql
-- telemetry (IoT data จาก MQTT)
CREATE TABLE telemetry (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT,
    power_usage   REAL,    -- kW
    battery_level INTEGER, -- %
    solar_output  REAL     -- kW
);

-- users (auth)
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT,          -- bcrypt hash
    role     TEXT           -- 'admin' | 'viewer'
);
```

### `backend/ev_data.db`
```sql
-- stations (5 สถานี Frankfurt)
CREATE TABLE stations (
    id           INTEGER PRIMARY KEY,
    name         TEXT,
    lat          REAL,
    lon          REAL,
    max_power_kw REAL,
    status       TEXT  -- 'Charging' | 'Available' | 'Offline'
);

-- charging_sessions
CREATE TABLE charging_sessions (
    id                 INTEGER PRIMARY KEY,
    station_id         INTEGER,
    timestamp          TEXT,
    energy_delivered_kwh REAL,
    soc_start          INTEGER,
    soc_end            INTEGER,
    duration_min       INTEGER,
    cost_eur           REAL,
    carbon_saved_kg    REAL
);
```

---

## 6. API ENDPOINTS (backend/api.py)

| Method | Path | Auth | หน้าที่ |
|---|---|---|---|
| POST | `/token` | Public | Login → JWT |
| GET | `/me` | JWT | ดู profile ตัวเอง |
| GET | `/telemetry` | JWT | 20 รายการล่าสุด |
| GET | `/summary` | JWT | avg/peak power, lowest battery, CO₂ |
| GET | `/alerts` | JWT | power>7, battery<30, solar<1 |
| GET | `/recommendations` | JWT | AI text recommendations |
| GET | `/system-status` | JWT | healthy/warning/critical |
| GET | `/trend-analysis` | JWT | increasing/decreasing/stable |
| GET | `/users` | Admin | list all users |
| POST | `/register` | Admin | สร้าง user ใหม่ |
| PUT | `/users/{username}/role` | Admin | เปลี่ยน role |
| DELETE | `/users/{username}` | Admin | ลบ user |

**Alert thresholds:** power_usage > 7 kW, battery_level < 30%, solar_output < 1 kW

---

## 7. AUTH PATTERN

```python
# ทุก protected endpoint ใช้ Depends() แบบนี้
@app.get("/endpoint")
def my_endpoint(current_user: str = Depends(verify_token)):   # viewer+
    ...

@app.get("/admin-endpoint")
def admin_endpoint(current_user: str = Depends(require_admin)):  # admin only
    ...
```

- Token: JWT HS256, หมดอายุ 30 นาที
- SECRET_KEY: อ่านจาก `.env` ผ่าน `os.getenv("SECRET_KEY")`
- RBAC roles: `"admin"` หรือ `"viewer"` เท่านั้น

---

## 8. TRANSLATION SYSTEM

```python
# translations.py — โครงสร้าง
TRANSLATIONS = {
    "DE": { "key": "German text", ... },
    "EN": { "key": "English text", ... }
}

# dashboard.py — เลือกภาษา
lang = st.sidebar.selectbox("🌐 Sprache / Language", ["DE", "EN"])
t = TRANSLATIONS[lang]

# ทุก tab รับ t แล้วใช้แบบนี้
st.subheader(t["solar_title"])

# ถ้าเป็น key ใหม่ที่ยังไม่มีใน translations ใช้ .get() มี fallback
st.write(t.get("new_key", "Default English text"))
```

**กฎ:** ถ้าเพิ่ม UI text ใหม่ → ต้องเพิ่มใน TRANSLATIONS["DE"] และ ["EN"] ทั้งคู่เสมอ

---

## 9. GERMAN BASELINE DATA (tab_solar.py)

ค่าเหล่านี้ hardcode ใน `GERMAN_DEFAULTS` dict และ `CITY_SUN_HOURS` dict:

| ค่า | ตัวเลข | อ้างอิง |
|---|---|---|
| Electricity rate | €0.32/kWh | BDEW Strompreisanalyse 2024 |
| Feed-in tariff | €0.082/kWh | Bundesnetzagentur 2024 (< 10 kWp) |
| CO₂ grid factor | 0.434 kg/kWh | UBA (Umweltbundesamt) 2023 |
| Panel degradation | 0.5%/year | Industry standard |
| Self-consumption | 70% | German average |
| Frankfurt sun hours | 3.2h/day | Solargis / PVGIS |
| Munich sun hours | 3.8h/day | Solargis / PVGIS |
| Hamburg sun hours | 2.9h/day | Solargis / PVGIS |

---

## 10. EV CONTEXT (tab_ev.py)

- 5 สถานี Frankfurt ใช้ชื่อ/location จริงของ MOVOLT Solutions GmbH
- DB: `backend/ev_data.db` (อ่านตรง ไม่ผ่าน API)
- สถานะ: `Charging` / `Available` / `Offline`
- แสดงบนแผนที่ด้วย Plotly Mapbox

---

## 11. ENVIRONMENT VARIABLES (.env)

```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password   # Gmail App Password (ไม่ใช่ password จริง)
SECRET_KEY=your-strong-secret-key
API_URL=http://127.0.0.1:8000            # local dev
# API_URL=http://api:8000               # inside Docker Compose
```

---

## 12. HOW TO RUN

```bash
# Local dev (แนะนำ)
source .venv/bin/activate
python backend/init_users.py     # ครั้งแรกเท่านั้น
python seed_data.py              # ครั้งแรกเท่านั้น
python seed_ev_data.py           # ครั้งแรกเท่านั้น
uvicorn backend.api:app --reload                    # terminal 1 → :8000
streamlit run dashboard/dashboard.py               # terminal 2 → :8501

# Docker
docker-compose up --build                          # api + dashboard
docker-compose --profile simulator up --build     # + simulator

# Test Python (ต้องใช้ .venv)
.venv/bin/python3 -c "..."
```

**Default accounts:**
- admin: `admin` / `admin123`
- demo: `demo@enervision.ai` / `Demo123!`

---

## 13. WHAT HAS BEEN BUILT

- [x] FastAPI backend — JWT auth, RBAC, 12 endpoints
- [x] Streamlit dashboard — 5 tabs, DE/EN language
- [x] MQTT IoT pipeline → SQLite
- [x] Prophet 48h energy forecast
- [x] AI anomaly detection (Z-score)
- [x] Email alert system (Gmail SMTP)
- [x] EV Charging Monitor — 5 Frankfurt stations, Plotly map
- [x] Solar ROI Calculator — German baseline data, feed-in tariff, 10yr Plotly chart
- [x] PDF energy report (ReportLab)
- [x] CSV upload + AI analysis
- [x] Docker Compose (api + dashboard + simulator)
- [x] CI/CD GitHub Actions → Docker Hub
- [x] User management (admin panel)

**Roadmap (ยังไม่ทำ):**
- [ ] PostgreSQL migration (ตอนนี้ SQLite)
- [ ] OAuth login (Google/Facebook)
- [ ] AWS IoT Core (ตอนนี้ HiveMQ public)
- [ ] Terraform + Kubernetes
- [ ] Multi-site monitoring

---

## 14. HOW TO THINK (วิธีคิดก่อนแก้โค้ด)

### ก่อนเพิ่มฟีเจอร์ใหม่ถามตัวเองว่า:
1. **มัน UI หรือ data?** → UI = แก้ `dashboard/tabs/tab_*.py` + `translations.py` / Data = แก้ `backend/api.py` หรือ DB
2. **ต้องใช้ API ไหม?** → ถ้าต้องการ auth/RBAC → ผ่าน API / ถ้าแค่อ่าน data → อ่าน SQLite ตรงผ่าน `db_paths.py`
3. **มี translation key แล้วหรือยัง?** → เพิ่มใน DE และ EN ทั้งคู่เสมอ
4. **ค่า default เหมาะกับเยอรมนีไหม?** → โปรเจกต์นี้ target MOVOLT Frankfurt

### Pattern ที่ใช้ซ้ำ:
```python
# เปิด SQLite
conn = sqlite3.connect(DB_ENERGY)
conn.row_factory = sqlite3.Row  # ถ้าต้องการ dict-like access
cursor = conn.cursor()
cursor.execute("SELECT ...", (param,))
rows = cursor.fetchall()
conn.close()

# ส่งข้อมูลจาก API
return [dict(row) for row in rows]
```

### อย่าทำ:
- อย่าใช้ค่า hardcode ไทย (บาท, sun hours เขตร้อน, ราคา THB)
- อย่าเพิ่ม UI text โดยไม่เพิ่มใน translations.py
- อย่า `git add .` — มี `.venv/` ที่ใหญ่มาก ใช้ specific file แทน
- อย่าเพิ่ม endpoint ใหม่โดยไม่มี `Depends(verify_token)` หรือ `Depends(require_admin)`

---

## 15. DOCKER SERVICES

| Service | Container | Port | Image |
|---|---|---|---|
| API | enervision-api | 8000 | pumpuyz/enervision-api |
| Dashboard | enervision-dashboard | 8501 | pumpuyz/enervision-dashboard |
| Simulator | enervision-simulator | — | (profile: simulator) |

- Dashboard ใน Docker ใช้ `API_URL=http://api:8000` (internal Docker network)
- Database share ผ่าน named volume `db-data` mount ที่ `/app/backend`
- API healthcheck: `curl http://localhost:8000/system-status`

---

## 16. MQTT CONFIG

```python
MQTT_BROKER = "broker.hivemq.com"  # public, ไม่ต้อง auth
MQTT_PORT   = 1883
MQTT_TOPIC  = "enervision/telemetry"

# payload format (JSON)
{
  "timestamp": "2024-01-01T12:00:00",
  "power_usage": 5.2,      # kW
  "battery_level": 75,     # %
  "solar_output": 3.1      # kW
}
```

---

## 17. QUICK REFERENCE

```bash
# ดู logs Docker
docker logs enervision-api
docker logs enervision-dashboard

# reset database
rm backend/energy_data.db
.venv/bin/python3 backend/database.py
.venv/bin/python3 backend/init_users.py
.venv/bin/python3 seed_data.py

# push to Docker Hub (หลัง build)
docker push pumpuyz/enervision-api
docker push pumpuyz/enervision-dashboard

# API docs
open http://localhost:8000/docs
```
