# tab_realtime.py
# Realtime Energy Monitoring Dashboard - Tab 1

import time
import streamlit as st
import pandas as pd
import sqlite3

from alerts import send_alert_email
from battery import show_battery_gauge
from forecast import render_forecast
from pdf_report import generate_pdf


def render_realtime(token, username, role, last_alert_time):

    st.subheader("Realtime Energy Monitoring")

    connection = sqlite3.connect("backend/energy_data.db")

    query = """
    SELECT *
    FROM telemetry
    ORDER BY id DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, connection)

    if df.empty:
        st.warning("No telemetry data found.")
        connection.close()
        return

    latest_power = df["power_usage"].iloc[0]
    latest_battery = df["battery_level"].iloc[0]
    latest_solar = df["solar_output"].iloc[0]

    # === Metrics ===
    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ Power Usage", f"{latest_power:.2f} kW")
    col2.metric("🔋 Battery Level", f"{latest_battery}%")
    col3.metric("☀️ Solar Output", f"{latest_solar:.2f} kW")

    show_battery_gauge(latest_battery)

    # === Carbon ===
    carbon_emission = latest_power * 0.4
    st.subheader("🌍 Carbon Emission Analytics")
    st.metric("Estimated CO₂ Emission", f"{carbon_emission:.2f} kg CO₂")

    # === System Health ===
    st.subheader("🖥️ System Health")
    if latest_power > 9:
        st.error("🔴 Critical")
    elif latest_battery < 45:
        st.warning("🟠 Warning")
    else:
        st.success("🟢 Healthy")

    # === Anomaly Detection ===
    st.subheader("AI Anomaly Detection")

    alert_threshold = st.slider(
        "⚡ Alert Threshold (kW)",
        min_value=1,
        max_value=20,
        value=9
    )

    if latest_power > alert_threshold:
        st.error(f"⚠️ High Power Usage Detected: {latest_power} kW")
        current_time = time.time()
        if current_time - last_alert_time > 1200:
            email_sent = send_alert_email(
                "⚠️ EnerVision Alert",
                f"High power usage: {latest_power} kW"
            )
            if email_sent:
                st.session_state.last_alert_time = current_time
                st.success("📧 Alert email sent")
            else:
                st.warning("Email alert failed")
        else:
            st.caption("⏳ Cooldown active")

    elif latest_battery < 45:
        st.warning(f"🔋 Low Battery Level: {latest_battery}%")
        current_time = time.time()
        if current_time - last_alert_time > 300:
            email_sent = send_alert_email(
                "🔋 EnerVision Battery Alert",
                f"Battery level low: {latest_battery}%"
            )
            if email_sent:
                st.session_state.last_alert_time = current_time
                st.success("📧 Battery alert sent")
            else:
                st.warning("Email alert failed")
        else:
            st.caption("⏳ Cooldown active")

    else:
        st.success("✅ System Operating Normally")

    # === Monthly Summary ===
    st.subheader("📅 Monthly Energy Summary")
    total_power = df["power_usage"].sum()
    average_power = df["power_usage"].mean()
    total_carbon = total_power * 0.4
    peak_usage = df["power_usage"].max()

    st.write(f"⚡ Total Energy Usage: {total_power:.2f} kW")
    st.write(f"📈 Average Power Usage: {average_power:.2f} kW")
    st.write(f"🌍 Estimated Total CO₂: {total_carbon:.2f} kg CO₂")

    # === Peak Usage ===
    st.subheader("⚡ Peak Usage Analysis")
    peak_row = df.loc[df["power_usage"].idxmax()]
    peak_power = peak_row["power_usage"]
    st.write(f"🔥 Peak Usage: {peak_usage:.2f} kW")
    st.write("This is the highest power usage found in the latest telemetry data.")

    if peak_power > alert_threshold:
        st.warning("Recommendation: Reduce non-critical loads during peak usage periods.")
    else:
        st.success("Peak usage is within the current alert threshold.")

    # === Cost Impact ===
    st.subheader("💰 Cost Impact Analysis")
    electricity_rate = 4.5
    estimated_cost = total_power * electricity_rate
    reduced_peak_power = peak_usage * 0.8
    estimated_saving = (peak_usage - reduced_peak_power) * electricity_rate * 30

    col1, col2, col3 = st.columns(3)
    col1.metric("Estimated Energy Cost", f"{estimated_cost:,.2f} THB")
    col2.metric("Potential Saving if Peak Reduced 20%", f"{estimated_saving:,.2f} THB")
    col3.metric("Highest Power Usage", f"{peak_power:.2f} kW")

    # === Charts ===
    st.subheader("Realtime Energy Telemetry")
    st.dataframe(df)
    st.subheader("Power Usage Trend")
    st.line_chart(df["power_usage"])
    st.subheader("Solar Output Trend")
    st.line_chart(df["solar_output"])
    st.subheader("Battery Level Trend")
    st.line_chart(df["battery_level"])

    # === Forecast ===
    render_forecast(connection)

    # === PDF ===
    st.subheader("📄 PDF Energy Report")
    if st.button("Generate PDF Report"):
        pdf_buffer = generate_pdf(
            latest_power,
            latest_battery,
            latest_solar,
            carbon_emission
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="energy_report.pdf",
            mime="application/pdf"
        )

    connection.close()