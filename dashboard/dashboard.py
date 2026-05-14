import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="EnerVision AI Dashboard")

st.title("⚡ EnerVision AI Dashboard Mai 2026")



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

forecast_value = df["power_usage"].tail(5).mean()

forecast_data = [forecast_value] * 10

st.line_chart(forecast_data)

st.info(f"Predicted Average Power Usage: {forecast_value:.2f} kW")