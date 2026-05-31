# tab_realtime.py
# Realtime Energy Monitoring Dashboard - Tab 1

import time
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

from alerts import send_alert_email
from battery import show_battery_gauge
from forecast import render_forecast
from pdf_report import generate_pdf
from db_paths import DB_ENERGY


def render_realtime(token, username, role, last_alert_time, t):

    st.subheader(t["realtime_title"])

    connection = sqlite3.connect(DB_ENERGY)

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
    col1.metric(t["power_usage"], f"{latest_power:.2f} kW")
    col2.metric(t["battery_level"], f"{latest_battery}%")
    col3.metric(t["solar_output"], f"{latest_solar:.2f} kW")
    show_battery_gauge(latest_battery)

    # === Carbon ===
    carbon_emission = latest_power * 1 * 0.4  # kW × 1hr × 0.4 kg/kWh
    st.subheader(t["carbon_title"])
    st.metric(t["carbon_metric"], f"{carbon_emission:.2f} kg CO₂/hr")

    # === System Health ===
    st.subheader(t["health_title"])
    if latest_power > 9:
        st.error(t["health_critical"])
    elif latest_battery < 45:
        st.warning(t["health_warning"])
    else:
        st.success(t["health_normal"])

    # === Anomaly Detection ===
    st.subheader(t["anomaly_title"])
    alert_threshold = st.slider(
        t["alert_threshold"],
        min_value=1,
        max_value=20,
        value=9
    )

    if latest_power > alert_threshold:
        st.error(f"{t['high_power_alert']}: {latest_power} kW")
        current_time = time.time()
        if current_time - last_alert_time > 1200:
            email_sent = send_alert_email(
                "⚠️ EnerVision Alert",
                f"High power usage: {latest_power} kW"
            )
            if email_sent:
                st.session_state.last_alert_time = current_time
                st.success(t["alert_sent"])
            else:
                st.warning(t["alert_failed"])
        else:
            st.caption(t["cooldown"])

    elif latest_battery < 45:
        st.warning(f"{t['low_battery_alert']}: {latest_battery}%")
        current_time = time.time()
        if current_time - last_alert_time > 300:
            email_sent = send_alert_email(
                "🔋 EnerVision Battery Alert",
                f"Battery level low: {latest_battery}%"
            )
            if email_sent:
                st.session_state.last_alert_time = current_time
                st.success(t["alert_sent"])
            else:
                st.warning(t["alert_failed"])
        else:
            st.caption(t["cooldown"])

    else:
        st.success(t["system_normal"])

    render_forecast(connection, t)

    # === Monthly Summary ===
    st.subheader(t["monthly_title"])
    total_power = df["power_usage"].sum()
    average_power = df["power_usage"].mean()
    total_carbon = average_power * 0.4  # kg CO₂/hr based on average kW
    peak_usage = df["power_usage"].max()

    st.write(f"{t['total_energy']}: {total_power:.2f} kWh")
    st.write(f"{t['avg_power']}: {average_power:.2f} kW")
    st.write(f"{t['total_carbon']}: {total_carbon:.2f} kg CO₂/hr")

    fig_monthly = px.bar(
        df,
        x=df.index,
        y="power_usage",
        title="Power Usage (Latest 20 Records)",
        labels={"power_usage": "kW", "index": "Record"},
        color="power_usage",
        color_continuous_scale="Blues"
    )
    fig_monthly.update_layout(template="plotly_dark")
    st.plotly_chart(fig_monthly, use_container_width=True)

    # === Peak Usage ===
    st.subheader(t["peak_title"])
    peak_row = df.loc[df["power_usage"].idxmax()]
    peak_power = peak_row["power_usage"]
    st.write(f"{t['peak_usage']}: {peak_usage:.2f} kW")
    st.write(t["peak_desc"])

    if peak_power > alert_threshold:
        st.warning(t["peak_warning"])
    else:
        st.success(t["peak_ok"])

    # === Cost Impact ===
    st.subheader(t["cost_title"])
    electricity_rate = 0.35
    estimated_cost = total_power * electricity_rate
    reduced_peak_power = peak_usage * 0.8
    estimated_saving = (peak_usage - reduced_peak_power) * electricity_rate * 30

    col1, col2, col3 = st.columns(3)
    col1.metric(t["cost_metric"], f"€{estimated_cost:,.2f}")
    col2.metric(t["saving_metric"], f"€{estimated_saving:,.2f}")
    col3.metric(t["highest_power"], f"{peak_power:.2f} kW")

    # === Charts ===
    st.subheader(t["telemetry_title"])
    st.dataframe(df)
    st.subheader(t["power_trend"])

    avg_line = df["power_usage"].mean()
    anomaly_mask = df["power_usage"] > (avg_line + 2 * df["power_usage"].std())

    # Area chart + anomaly markers + average reference line
    fig_power = go.Figure()

    fig_power.add_trace(go.Scatter(
        x=df.index, y=df["power_usage"],
        fill="tozeroy",
        name="Power Usage",
        line=dict(color="#00A8E8"),
        fillcolor="rgba(0,168,232,0.15)"
    ))

    fig_power.add_trace(go.Scatter(
        x=df.index[anomaly_mask], y=df["power_usage"][anomaly_mask],
        mode="markers",
        name="Anomaly",
        marker=dict(color="red", size=10, symbol="x")
    ))

    fig_power.add_hline(
        y=avg_line,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Avg: {avg_line:.2f} kW"
    )

    fig_power.update_layout(template="plotly_dark", title="Power Usage Trend")
    st.plotly_chart(fig_power, use_container_width=True)

    # Multi-line: Power + Solar + Battery
    st.subheader(t["solar_trend"])

    fig_multi = go.Figure()

    fig_multi.add_trace(go.Scatter(
        x=df.index, y=df["power_usage"],
        name="Power Usage (kW)",
        line=dict(color="#00A8E8")
    ))

    fig_multi.add_trace(go.Scatter(
        x=df.index, y=df["solar_output"],
        name="Solar Output (kW)",
        line=dict(color="#FFD700")
    ))

    fig_multi.add_trace(go.Scatter(
        x=df.index, y=df["battery_level"],
        name="Battery (%)",
        line=dict(color="#00E5A0", dash="dot"),
        yaxis="y2"
    ))

    fig_multi.update_layout(
        template="plotly_dark",
        title="Power / Solar / Battery Overview",
        yaxis=dict(title="kW"),
        yaxis2=dict(title="Battery %", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig_multi, use_container_width=True)

    # Bar + average line combo for battery
    st.subheader(t["battery_trend"])

    avg_battery = df["battery_level"].mean()

    fig_battery = go.Figure()

    fig_battery.add_trace(go.Bar(
        x=df.index, y=df["battery_level"],
        name="Battery Level",
        marker_color=df["battery_level"].apply(
            lambda v: "#00E5A0" if v >= 50 else "#FF6B6B"
        )
    ))

    fig_battery.add_hline(
        y=avg_battery,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Avg: {avg_battery:.1f}%"
    )

    fig_battery.update_layout(template="plotly_dark", title="Battery Level Trend")
    st.plotly_chart(fig_battery, use_container_width=True)

    # === PDF ===
    st.subheader(t["pdf_title"])
    if st.button(t["generate_pdf"]):
        pdf_buffer = generate_pdf(
            latest_power,
            latest_battery,
            latest_solar,
            carbon_emission
        )
        st.download_button(
            label=t["download_pdf"],
            data=pdf_buffer,
            file_name="energy_report.pdf",
            mime="application/pdf"
        )

    connection.close()