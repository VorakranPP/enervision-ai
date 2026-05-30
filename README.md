# ⚡ EnerVision AI

## Overview

EnerVision AI is an AI-powered energy monitoring and analytics platform designed for realtime telemetry processing, anomaly detection, energy forecasting, sustainability reporting, solar investment planning, and EV charging station monitoring.

The platform combines:

- Realtime MQTT telemetry
- AI analytics (Prophet ML)
- Secure authentication (JWT + RBAC)
- Solar ROI estimation
- EV Charging Station monitoring
- Dashboard visualization
- PDF/CSV reporting

---

# 🚀 Features

- Realtime energy monitoring dashboard
- MQTT-based telemetry streaming
- AI anomaly detection
- **48-hour energy forecasting with Prophet (Meta)**
- Carbon emission analytics
- Upload & AI file analysis
- CSV export and PDF reporting
- Real-time email alerts
- Dynamic alert threshold slider
- Live battery gauge UI
- System health monitoring
- Email alerts with cooldown
- **EV Charging Station Monitor (Frankfurt Network)**
- **Modern login UI with error handling**
- Admin dashboard
- User creation / role updates / deletion
- Admin-only user management
- **Modular architecture (separated tab files)**

## 🔐 Authentication & User Management

- JWT authentication
- Modern login UI
- **Connection error handling**
- Dashboard login/logout
- User registration
- Password hashing with bcrypt
- SQLite user management
- Role-based access control (RBAC)
- Admin and viewer roles

## ☀️ Solar ROI Calculator

- Roof area estimation
- Solar panel recommendation
- Installation cost estimation
- Monthly savings prediction
- Payback period calculation
- 10-year savings estimation

## 🚛 EV Charging Monitor *(New)*

- 5 EV Charging Stations — Frankfurt Network
- Live station status (Charging / Available / Offline)
- State of Charge (SoC) tracking
- Energy delivered per session
- Cost per session (€)
- Carbon saved vs petrol vehicles
- Interactive map (Frankfurt)
- Daily sessions trend
- Revenue analytics

## 📊 Dashboard Modules

- Realtime Dashboard
- Upload & AI Analysis
- Solar ROI Calculator
- **EV Charging Monitor**
- Admin Panel

---

# 🧠 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Messaging | MQTT |
| Database | SQLite |
| Authentication | JWT + bcrypt + RBAC |
| AI / ML | **Prophet (Meta) + scikit-learn** |
| Data Processing | Pandas / NumPy |
| Visualization | **Plotly** |
| Reporting | ReportLab |
| Deployment | Docker |

---

# 📸 Dashboard Modules

## 📊 Realtime Dashboard

- Realtime telemetry monitoring
- AI anomaly detection
- **48-hour Prophet ML forecasting**
- Carbon analytics
- PDF & CSV reporting

## 📁 Upload & AI Analysis

- Upload CSV files
- AI analysis and recommendations
- Peak usage detection
- Battery health analysis

## ☀️ Solar ROI Calculator

- Roof area estimation
- Solar panel recommendation
- Installation cost estimation
- Monthly savings calculation
- Payback period estimation
- 10-year savings prediction

## 🚛 EV Charging Monitor *(New)*

- 5 stations Frankfurt network
- Live status monitoring
- SoC tracking per session
- Revenue and carbon analytics
- Interactive map

## 👑 Admin Panel

- View all users
- Create new users
- Update user roles
- Delete users
- Admin-only access

---

## 📧 Notifications

- Email alerts for abnormal power usage
- SMTP integration with Gmail
- Configurable alert threshold
- Alert cooldown system
- Battery alerts

---

# 📸 Screenshots

## 🔐 Login

![Login](screenshots/login.png)

## 📊 Realtime Dashboard

![Dashboard](screenshots/dashboard1.1.png)
![Dashboard](screenshots/dashboard1.2.png)

## 📁 Upload & AI Analysis

![Upload](screenshots/Upload1.1.png)
![Upload](screenshots/Upload1.2.png)

## ☀️ Solar ROI Calculator

![Solar](screenshots/SolarCal1.1.png)
![Solar](screenshots/SolarCal1.2.png)

---

# 🏗️ Architecture Diagram

```text
                    ┌──────────────────────┐
                    │     User / Client    │
                    └──────────┬───────────┘
                               │
                               │ Login / JWT
                               ▼
                    ┌──────────────────────┐
                    │ Authentication Layer │
                    │ JWT + bcrypt + RBAC  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │ Protected Endpoints  │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┴─────────────────────┐
         │                                           │
         ▼                                           ▼
┌──────────────────────┐                ┌──────────────────────┐
│      SQLite DB       │                │   MQTT Telemetry     │
│ Users + Energy Data  │                │  Energy Simulator    │
│ + EV Charging Data   │                └──────────┬───────────┘
└──────────┬───────────┘                           │
           └─────────────────┬─────────────────────┘
                             ▼
                  ┌─────────────────────────┐
                  │ AI Analytics Engine     │
                  │ Prophet ML + Alerts     │
                  └──────────┬──────────────┘
                             ▼
                  ┌─────────────────────────┐
                  │ Streamlit Dashboard     │
                  │ Energy + EV Monitoring  │
                  └─────────────────────────┘
```

---

# 📦 Local Setup

## Clone Repository

```bash
git clone https://github.com/VorakranPP/enervision-ai.git
cd enervision-ai
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Seed Data

```bash
# Energy data (30 days)
python seed_data.py

# EV charging data (5 stations)
python seed_ev_data.py
```

## Run Dashboard

```bash
streamlit run dashboard/dashboard.py
```

## Run API

```bash
uvicorn backend.api:app --reload
```

---

# 🐳 Docker Deployment

```bash
docker build -t enervision-ai .
docker run -p 8000:8000 -p 8501:8501 enervision-ai
```

---

# 🔌 FastAPI Endpoints

| Endpoint | Description |
|---|---|
| POST `/token` | Login & generate JWT |
| GET `/me` | Current user profile |
| GET `/users` | List all users (admin only) |
| PUT `/users/{username}/role` | Update user role (admin only) |
| DELETE `/users/{username}` | Delete user (admin only) |
| POST `/register` | Register new user (admin only) |
| GET `/telemetry` | Latest telemetry data |
| GET `/summary` | Energy analytics summary |
| GET `/alerts` | Active system alerts |
| GET `/recommendations` | AI recommendations |
| GET `/system-status` | System health |
| GET `/trend-analysis` | Historical trend |

---

# 🔮 Future Roadmap

- PostgreSQL migration
- Cloud deployment (AWS EC2/ECS)
- AWS IoT Core integration
- Multi-site monitoring
- Predictive maintenance
- Kubernetes deployment
- Grafana integration
- CI/CD pipeline with GitHub Actions
- German multilingual dashboard 🇩🇪

---

# 👨‍💻 Author

**Vorakran Trisilanun (PP)**

Network Engineer | Cloud & Infrastructure Enthusiast | AI & IoT Builder

---

## ⭐ Current Version

EnerVision AI v3.0

Latest additions:

- 🚛 EV Charging Station Monitor (Frankfurt Network)
- 🔮 Prophet ML 48-hour energy forecasting
- 🎨 Modern login UI with animated background
- ⚠️ Error handling & connection error messages
- 🏗️ Modular architecture (separated tab files)
- 🔐 Environment variables (.env) for security
- 🐳 Docker multi-service deployment