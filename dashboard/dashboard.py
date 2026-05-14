import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="EnerVision AI Dashboard")

st.title("⚡ EnerVision AI Dashboard Mai 2026")
st_autorefresh(interval=3000, key="datarefresh")


##connection = sqlite3.connect("energy_data.db")
##connection = sqlite3.connect("../energy_data.db")
connection = sqlite3.connect("backend/energy_data.db")
query = """
SELECT *
FROM telemetry
ORDER BY id DESC
LIMIT 20
"""

df = pd.read_sql_query(query, connection)

latest_power = df["power_usage"].iloc[0]
latest_battery = df["battery_level"].iloc[0]
latest_solar = df["solar_output"].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "⚡ Power Usage",
    f"{latest_power:.2f} kW"
)

col2.metric(
    "🔋 Battery Level",
    f"{latest_battery}%"
)

col3.metric(
    "☀️ Solar Output",
    f"{latest_solar:.2f} kW"
)

carbon_emission = latest_power * 0.4

st.subheader("🌍 Carbon Emission Analytics")


st.metric(
    "Estimated CO₂ Emission",
    f"{carbon_emission:.2f} kg CO₂"
)

st.subheader("AI Anomaly Detection")

latest_power = df["power_usage"].iloc[0]
latest_battery = df["battery_level"].iloc[0]

if latest_power > 7:
    st.error(f"⚠️ High Power Usage Detected: {latest_power} kW")

elif latest_battery < 45:
    st.warning(f"🔋 Low Battery Level: {latest_battery}%")

else:
    st.success("✅ System Operating Normally")

connection.close()

st.subheader("Realtime Energy Telemetry")

st.dataframe(df)

st.subheader("Power Usage Trend")

st.line_chart(df["power_usage"])

st.subheader("Solar Output Trend")

st.line_chart(df["solar_output"])

st.subheader("Battery Level Trend")

st.line_chart(df["battery_level"])

st.subheader("Energy Usage Forecast")

##forecast_value = df["power_usage"].tail(5).mean()

##forecast_data = [forecast_value] * 10

##st.line_chart(forecast_data)

##st.info(f"Predicted Average Power Usage: {forecast_value:.2f} kW")

st.subheader("🔮 AI Energy Forecast")

power_data = df["power_usage"].values[::-1]

X = np.array(range(len(power_data))).reshape(-1, 1)
y = power_data

model = LinearRegression()
model.fit(X, y)

future_x = np.array(range(len(power_data), len(power_data) + 10)).reshape(-1, 1)

forecast = model.predict(future_x)

st.line_chart(forecast)

forecast_value = forecast[-1]

st.info(f"Predicted Future Power Usage: {forecast_value:.2f} kW")