
# ⚡ EnerVision AI

AI-powered smart energy monitoring prototype for realtime telemetry, anomaly detection, forecasting, and sustainability analytics.

---

# 🚀 Features

- Realtime energy monitoring dashboard

- MQTT-based telemetry streaming

- AI anomaly detection

- Energy forecasting analytics

- Carbon emission analytics

- Upload & AI file analysis

- CSV export and PDF reporting

- Solar ROI calculator
  - Roof area estimation
  - Solar panel recommendation
  - Installation cost estimation
  - Monthly savings prediction
  - Payback period calculation
  - 10-year savings estimation

- Dashboard authentication
  - Login / Logout
  - JWT authentication
  - Session management
  - User profile display

- User management
  - User registration & login
  - SQLite user database
  - Password hashing with bcrypt
  - Role-based access control (RBAC)
  - Admin and viewer roles

- Protected API endpoints

- Cross-platform deployment
  - MacOS
  - Windows

- Docker deployment support
---

# 🧠 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Messaging | MQTT |
| Database | SQLite |
| Authentication | JWT + bcrypt |
| AI / ML | scikit-learn |
| Data Processing | Pandas / NumPy |
| Reporting | ReportLab |
| Deployment | Docker |

---

## 📸 Dashboard Modules

### 📊 Realtime Dashboard

- Realtime telemetry monitoring
- AI anomaly detection
- Energy forecasting
- Carbon analytics
- PDF & CSV reporting


### 📁 Upload & AI Analysis

- Upload CSV files
- AI analysis and recommendations
- Peak usage detection
- Battery health analysis


### ☀️ Solar ROI Calculator

- Roof area estimation
- Solar panel recommendation
- Installation cost estimation
- Monthly savings calculation
- Payback period estimation
- 10-year savings prediction

---
## 📸 Screenshots

### Login

![Login](screenshots/login.png)


### Dashboard

![Dashboard](screenshots/dashboard1.1.png)
![Dashboard](screenshots/dashboard1.2.png)

### Upload & AI Analysis

![Upload](screenshots/Upload1.1.png)
![Upload](screenshots/Upload1.2.png)


### Solar ROI

![Solar](screenshots/SolarCal1.1.png)
![Solar](screenshots/SolarCal1.2.png)

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
                    │ JWT + bcrypt + Users │
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
└──────────┬───────────┘                └──────────┬───────────┘
           │                                       │
           └─────────────────┬─────────────────────┘
                             ▼
                  ┌─────────────────────────┐
                  │ AI Analytics Engine     │
                  │ Alerts + Forecasting    │
                  └──────────┬──────────────┘
                             ▼
                  ┌─────────────────────────┐
                  │ Streamlit Dashboard     │
                  │ Monitoring & Reports    │
                  └─────────────────────────┘
```


# 📦 Local Setup

## Clone Repository

```bash
git clone https://github.com/VorakranPP/enervision-ai.git
cd enervision-ai
```

## Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Run Dashboard

```bash
python3 -m streamlit run dashboard/dashboard.py
```

---

# 🐳 Docker Deployment

## Build Docker Image

```bash
docker build -t enervision-ai .
```

## Run Container

```bash
docker run -p 8501:8501 enervision-ai
```

# 📦 Git Workflow

```bash
git add .
git commit -m "Add FastAPI backend"
git push
```

---
# 🔌 FastAPI Backend

## Run API

```bash
uvicorn backend.api:app --reload
```

## API Documentation

```text
http://127.0.0.1:8000/docs
```

## Available API Endpoints

| Endpoint | Description |
|---|---|
| GET `/` | API root endpoint |
| POST `/register` | Register new user |
| POST `/token` | Login & generate JWT |
| GET `/health` | System health check |
| GET `/telemetry` | Latest telemetry data |
| GET `/summary` | Energy analytics summary |
| GET `/alerts` | Active system alerts |
| GET `/recommendations` | AI operational recommendations |
| GET `/system-status` | Overall system condition |
| GET `/trend-analysis` | Historical energy trend analysis |

# 🌐 Dashboard

```text
http://localhost:8501
```

---

# 🧠 AI Analytics

The platform includes:

* Threshold-based anomaly detection
* Energy forecasting using Linear Regression
* Carbon emission estimation
* AI-generated operational recommendations

## Example Recommendations

* Reduce HVAC usage during peak hours
* Shift non-critical loads
* Improve battery charging schedules
* Optimize solar utilization

---

# 📈 Example Use Cases

* Smart Building Monitoring
* Renewable Energy Analytics
* Energy Consumption Optimization
* ESG & Sustainability Reporting
* Operational Energy Insights

---

# 🌍 Business Value

EnerVision AI helps organizations:

* Monitor realtime energy usage
* Detect abnormal consumption patterns
* Improve operational visibility
* Support sustainability initiatives
* Generate AI-driven recommendations
* Analyze historical energy trends

---

# 🔐 Authentication & User Management

EnerVision AI includes:

- User registration (`POST /register`)
- User login (`POST /token`)
- JWT authentication
- bcrypt password hashing
- SQLite user storage
- Role-based access control (RBAC)
- Protected APIs

## Authentication Flow

```text
Register User
↓
Store User in SQLite
↓
Hash Password (bcrypt)
↓
Login
↓
Generate JWT Token
↓
Role Verification (admin / viewer)
↓
Access Protected APIs
```

## Roles

| Role | Permissions |
|---|---|
| admin | Create users, access protected APIs |
| viewer | Read-only access |

## Protected Endpoints

| Endpoint | Authentication |
|---|---|
| GET `/summary` | 🔒 Required |
| GET `/alerts` | 🔒 Required |
| GET `/recommendations` | 🔒 Required |
| GET `/system-status` | 🔒 Required |
| GET `/trend-analysis` | 🔒 Required |
| POST `/register` | 🔒 Admin only |

## Public Endpoints

| Endpoint | Description |
|---|---|
| POST `/token` | Login |
| GET `/telemetry` | Telemetry |
| GET `/health` | Health check |

🔮 Future Roadmap

- PostgreSQL migration
- Cloud deployment (AWS)
- AWS IoT Core integration
- Multi-site monitoring
- Predictive maintenance
- Advanced ML forecasting
- Email alerting
- Kubernetes deployment
- Real solar recommendation engine
- Dynamic role management

# 👨‍💻 Author

**Vorakran Trisilanun (PP)**

Netzwerkingenieurin | Cloud & Infrastructure Enthusiast | AI & IoT Learner

Built as a portfolio and learning project focused on:

- AI
- IoT
- Energy analytics
- Solar planning
- Secure backend systems
- Cloud-native architecture
- Authentication and RBAC