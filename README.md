
# ⚡ EnerVision AI

AI-powered smart energy monitoring prototype for realtime telemetry, anomaly detection, forecasting, and sustainability analytics.

---

# 🚀 Features

- Realtime telemetry simulation
- MQTT-based data streaming
- Realtime dashboard visualization
- AI anomaly detection
- Energy forecasting
- Carbon emission analytics
- Upload & AI file analysis
- CSV export and PDF reporting
- Docker deployment support
- JWT authentication
- User registration & login
- SQLite user management
- Password hashing with bcrypt
- Protected API endpoints

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

# 📊 Dashboard Features

## 📊 Realtime Dashboard

- Live telemetry monitoring
- KPI metrics
- Trend visualization
- Forecast analytics
- Carbon emission tracking

## 📁 Upload & AI Analysis

- Upload CSV energy data
- Analyze energy usage
- Detect abnormal values
- Generate AI recommendations
- Export reports

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
- Protected APIs

## Authentication Flow

```text
Register
↓
SQLite
↓
bcrypt hash
↓
Login
↓
JWT token
↓
Protected APIs
```


## Protected Endpoints

| Endpoint | Authentication |
|---|---|
| GET `/summary` | 🔒 Required |
| GET `/alerts` | 🔒 Required |
| GET `/recommendations` | 🔒 Required |
| GET `/system-status` | 🔒 Required |
| GET `/trend-analysis` | 🔒 Required |

## Public Endpoints

| Endpoint | Description |
|---|---|
| POST `/register` | Register user |
| POST `/token` | Login |
| GET `/telemetry` | Telemetry |
| GET `/health` | Health check |

# 🔮 Future Roadmap

- [ ] Role-based access control (RBAC)
- [ ] Refresh tokens
- [ ] PostgreSQL migration
- [ ] AWS IoT Core integration
- [ ] Cloud deployment (AWS)
- [ ] Multi-site monitoring
- [ ] Predictive maintenance
- [ ] Advanced ML forecasting
- [ ] Email alerting
- [ ] Kubernetes deployment
- [ ] Grafana integration
- [ ] User profile management
- [ ] Password reset
- [ ] Multi-user roles

# 👨‍💻 Author

**Vorakran Trisilanun (PP)**

Netzwerkingenieurin | Cloud & Infrastructure Enthusiast | AI & IoT Learner

Built as a portfolio project focused on:

- AI analytics
- IoT systems
- Secure backend architecture
- Cloud-native applications
- Smart energy monitoring