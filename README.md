# ⚡ EnerVision AI

**AI-powered Energy Monitoring & EV Charging Infrastructure Platform**

Built for smart energy management in industrial and EV charging environments. Combines real-time IoT telemetry, machine learning forecasting, and a multi-role web dashboard — containerized with Docker Compose for cloud-ready deployment.

---

## Quick Start (Docker)

```bash
git clone https://github.com/VorakranPP/enervision-ai.git
cd enervision-ai

cp .env.example .env        # configure credentials
docker-compose up --build
```

| Service   | URL                   |
|-----------|-----------------------|
| Dashboard | http://localhost:8501 |
| API       | http://localhost:8000 |
| API Docs  | http://localhost:8000/docs |

| Account | Username | Password | Role |
|---------|----------|----------|------|
| Admin | `admin` | `admin123` | admin |
| Demo | `demo@enervision.ai` | `Demo123!` | viewer |

---

## Architecture

```
IoT Sensors / Simulator
        │ MQTT (paho)
        ▼
  HiveMQ Broker ──────────────────────────────┐
                                              │
                                              ▼
                                   ┌─────────────────┐
                                   │  MQTT Subscriber │
                                   │  mqtt_subscriber │
                                   └────────┬─────────┘
                                            │
                                            ▼
                              ┌─────────────────────────┐
                              │       SQLite DB          │
                              │  telemetry + users       │
                              │  + EV charging sessions  │
                              └────────────┬─────────────┘
                                           │
                    ┌──────────────────────┤
                    ▼                      ▼
          ┌──────────────────┐   ┌──────────────────────┐
          │   FastAPI (API)  │   │  AI Analytics Engine │
          │  JWT + RBAC      │   │  Prophet ML Forecast │
          │  /token /me      │   │  Anomaly Detection   │
          │  /telemetry ...  │   │  Recommendations     │
          └────────┬─────────┘   └──────────┬───────────┘
                   │                        │
                   └───────────┬────────────┘
                               ▼
                   ┌───────────────────────┐
                   │  Streamlit Dashboard  │
                   │  Real-time + Upload   │
                   │  Solar + EV + Admin   │
                   └───────────────────────┘
```

---

## Features

### Real-time Energy Monitoring
- Live telemetry via MQTT (power usage, battery level, solar output)
- Configurable alert threshold with cooldown system
- Email alerts via Gmail SMTP for anomalies
- System health status indicator

### AI & Machine Learning
- **48-hour energy forecasting** using Prophet (Meta)
- AI anomaly detection (Z-score statistical model)
- Carbon emission analytics (kg CO₂ per kWh)
- AI-powered recommendations engine

### EV Charging Station Monitor
- 5-station Frankfurt charging network (MOVOLT)
- Live station status: Charging / Available / Offline
- State of Charge (SoC) tracking per session
- Energy delivered, cost (€), and carbon saved per session
- Interactive map (Plotly Mapbox)
- Daily sessions trend and revenue analytics

### Upload & AI Analysis
- CSV upload with automatic column detection
- Date range and site filtering
- Temperature correlation analysis
- Forecast export as CSV
- Anomaly visualization

### Solar ROI Calculator
- Roof area and panel configuration
- Installation cost estimation
- Monthly savings and payback period calculation
- 10-year return projection

### Security & Access Control
- JWT authentication (30-minute token expiry)
- Role-based access control (Admin / Viewer)
- Password hashing with bcrypt
- Environment variable secrets management

### Reporting
- PDF energy report generation (ReportLab)
- CSV export for processed data and forecasts

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| IoT Messaging | MQTT (paho-mqtt → HiveMQ) |
| Database | SQLite |
| Authentication | JWT (python-jose) + bcrypt + RBAC |
| AI / Forecasting | Prophet (Meta) |
| Data Processing | Pandas, NumPy, scikit-learn |
| Visualization | Plotly |
| Reporting | ReportLab |
| Containerization | Docker + Docker Compose |
| Language | Python 3.11 |

---

## Project Structure

```
enervision-ai/
├── backend/
│   ├── api.py                 # FastAPI — all endpoints
│   ├── database.py            # SQLite schema initialization
│   ├── mqtt_subscriber.py     # MQTT → SQLite listener
│   └── energy_data.db         # Main database
│
├── dashboard/
│   ├── dashboard.py           # Streamlit entry point
│   ├── db_paths.py            # Centralized DB path constants
│   ├── translations.py        # DE / EN language pack
│   ├── forecast.py            # Prophet forecasting component
│   ├── alerts.py              # Email alert system
│   ├── battery.py             # Battery gauge UI
│   ├── pdf_report.py          # PDF report generation
│   ├── styles.py              # Login page CSS
│   └── tabs/
│       ├── tab_realtime.py    # Real-time energy dashboard
│       ├── tab_upload.py      # CSV upload + AI analysis
│       ├── tab_solar.py       # Solar ROI calculator
│       ├── tab_ev.py          # EV charging monitor
│       └── tab_admin.py       # User management (admin)
│
├── simulator/
│   └── energy_simulator.py    # MQTT sensor simulator
│
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.dashboard
├── requirements.txt
└── .env.example
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/token` | Login — returns JWT | Public |
| GET | `/me` | Current user profile | JWT |
| GET | `/telemetry` | Latest 20 telemetry records | JWT |
| GET | `/summary` | Energy analytics summary | JWT |
| GET | `/alerts` | Active system alerts | JWT |
| GET | `/recommendations` | AI recommendations | JWT |
| GET | `/system-status` | Health check | Public |
| GET | `/trend-analysis` | Historical trend data | JWT |
| GET | `/users` | List all users | Admin |
| POST | `/register` | Create new user | Admin |
| PUT | `/users/{username}/role` | Update user role | Admin |
| DELETE | `/users/{username}` | Delete user | Admin |

Full interactive docs: `http://localhost:8000/docs`

---

## Local Setup (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database and admin user
python backend/init_users.py

# Seed sample data
python seed_data.py
python seed_ev_data.py

# Start API
uvicorn backend.api:app --reload

# Start Dashboard (separate terminal)
streamlit run dashboard/dashboard.py
```

---

## Docker Compose Services

| Service | Description | Port |
|---------|-------------|------|
| `api` | FastAPI backend | 8000 |
| `dashboard` | Streamlit frontend | 8501 |
| `simulator` | MQTT sensor simulator (optional) | — |

Run with simulator:
```bash
docker-compose --profile simulator up --build
```

---

## Environment Variables

```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password
SECRET_KEY=your-strong-secret-key
API_URL=http://127.0.0.1:8000        # http://api:8000 in Docker
```

---

## Screenshots

### Login
![Login](screenshots/login.png)

### Real-time Dashboard
![Dashboard](screenshots/dashboard1.1.png)
![Dashboard](screenshots/dashboard1.2.png)

### Upload & AI Analysis
![Upload](screenshots/Upload1.1.png)
![Upload](screenshots/Upload1.2.png)

### Solar ROI Calculator
![Solar](screenshots/SolarCal1.1.png)
![Solar](screenshots/SolarCal1.2.png)

---

## Roadmap

- [ ] PostgreSQL migration (replace SQLite for production)
- [ ] Google / Facebook OAuth login
- [ ] AWS IoT Core integration (replace HiveMQ)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Kubernetes deployment (Helm chart)
- [ ] Grafana dashboard integration
- [ ] Multi-site energy monitoring
- [ ] Predictive maintenance alerts

---

## Author

**Vorakran Trisilanun**
Network Engineer | Cloud & Infrastructure | AI & IoT

---

*EnerVision AI v3.1 — Docker Compose release*
