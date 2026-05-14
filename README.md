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

---

# 🧠 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Messaging | MQTT |
| Database | SQLite |
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
                           │   Energy Simulator   │
                           │  (Fake IoT Sensors)  │
                           └──────────┬───────────┘
                                      │
                                      │ MQTT Telemetry
                                      ▼
                           ┌──────────────────────┐
                           │     MQTT Broker      │
                           │     HiveMQ / IoT     │
                           └──────────┬───────────┘
                                      │
                                      │ Streamed Messages
                                      ▼
                           ┌──────────────────────┐
                           │  Backend Subscriber  │
                           │   Python + MQTT      │
                           └──────────┬───────────┘
                                      │
                                      │ Store Telemetry
                                      ▼
                           ┌──────────────────────┐
                           │     SQLite DB        │
                           │  Historical Storage  │
                           └──────────┬───────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌──────────────────────┐          ┌────────────────────────┐
        │  Realtime Dashboard  │          │     AI Analytics       │
        │      Streamlit       │          │ Anomaly + Forecasting  │
        └──────────────────────┘          └────────────────────────┘
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      ▼
                           ┌──────────────────────┐
                           │ Upload & AI Analysis │
                           │ CSV / Report Engine  │
                           └──────────────────────┘
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

Open:

```text
http://localhost:8501
```

---

# 🧠 AI Analytics

The platform includes:

- Threshold-based anomaly detection
- Energy forecasting using Linear Regression
- Carbon emission estimation
- AI-generated operational recommendations

## Example Recommendations

- Reduce HVAC usage during peak hours
- Shift non-critical loads
- Improve battery charging schedules
- Optimize solar utilization

---

# 📈 Example Use Cases

- Smart Building Monitoring
- Renewable Energy Analytics
- Energy Consumption Optimization
- ESG & Sustainability Reporting
- Operational Energy Insights

---

# 🌍 Business Value

EnerVision AI helps organizations:

- Monitor realtime energy usage
- Detect abnormal consumption patterns
- Improve operational visibility
- Support sustainability initiatives
- Generate AI-driven recommendations
- Analyze historical energy trends

---

# 🔮 Future Roadmap

- AWS IoT Core integration
- Multi-site monitoring
- Predictive maintenance
- Advanced ML forecasting
- Email alerting
- Kubernetes deployment

---

# 👨‍💻 Author

Vorakran Trisilanun (PP)

Built as a portfolio and learning project focused on AI, IoT, realtime analytics, and cloud-native energy systems.