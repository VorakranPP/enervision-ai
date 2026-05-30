# tab_ev.py
# EV Charging Station Monitor - Tab 5
# Designed for MOVOLT Solutions GmbH Frankfurt

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def render_ev(t):

    st.subheader("🚛 EV Charging Station Monitor")
    st.caption("Frankfurt Charging Network — MOVOLT Solutions GmbH")

    conn = sqlite3.connect("backend/ev_data.db")

    # === Load Data ===
    stations_df = pd.read_sql_query(
        "SELECT * FROM stations", conn
    )

    sessions_df = pd.read_sql_query("""
        SELECT cs.*, s.name as station_name, s.max_power_kw
        FROM charging_sessions cs
        JOIN stations s ON cs.station_id = s.id
        ORDER BY cs.timestamp DESC
    """, conn)

    sessions_df["timestamp"] = pd.to_datetime(sessions_df["timestamp"])

    # === Summary Metrics ===
    st.subheader("📊 Network Overview")

    total_energy = sessions_df["energy_delivered_kwh"].sum()
    total_cost = sessions_df["cost_eur"].sum()
    total_carbon = sessions_df["carbon_saved_kg"].sum()
    total_sessions = len(sessions_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚡ Total Energy", f"{total_energy:,.0f} kWh")
    col2.metric("💰 Total Revenue", f"€{total_cost:,.0f}")
    col3.metric("🌍 CO₂ Saved", f"{total_carbon:,.0f} kg")
    col4.metric("🔌 Total Sessions", f"{total_sessions:,}")

    st.divider()

    # === Station Status ===
    st.subheader("🔌 Station Status")

    for _, station in stations_df.iterrows():

        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

        # Status badge
        if station["status"] == "Charging":
            badge = "🟢 Charging"
        elif station["status"] == "Available":
            badge = "🔵 Available"
        else:
            badge = "🔴 Offline"

        # Stats for this station
        s_sessions = sessions_df[
            sessions_df["station_id"] == station["id"]
        ]
        s_energy = s_sessions["energy_delivered_kwh"].sum()
        s_cost = s_sessions["cost_eur"].sum()
        s_carbon = s_sessions["carbon_saved_kg"].sum()

        with col1:
            st.write(f"**{station['name']}**")
        with col2:
            st.write(badge)
        with col3:
            st.write(f"⚡ {s_energy:,.0f} kWh")
        with col4:
            st.write(f"💰 €{s_cost:,.0f}")
        with col5:
            st.write(f"🌍 {s_carbon:,.0f} kg CO₂")

    st.divider()

    # === Map ===
    st.subheader("🗺️ Station Map — Frankfurt")

    color_map = {
        "Charging": "green",
        "Available": "blue",
        "Offline": "red"
    }

    stations_df["color"] = stations_df["status"].map(color_map)
    stations_df["size"] = 15

    fig_map = px.scatter_mapbox(
        stations_df,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data={"status": True, "max_power_kw": True},
        color="status",
        color_discrete_map=color_map,
        size="size",
        size_max=20,
        zoom=11,
        height=450,
        mapbox_style="open-street-map",
        title="EV Charging Stations — Frankfurt"
    )

    st.plotly_chart(fig_map, width='stretch')

    st.divider()

    # === Energy per Station Chart ===
    st.subheader("⚡ Energy Delivered per Station")

    energy_by_station = sessions_df.groupby("station_name")[
        "energy_delivered_kwh"
    ].sum().reset_index()

    fig_bar = px.bar(
        energy_by_station,
        x="station_name",
        y="energy_delivered_kwh",
        color="energy_delivered_kwh",
        color_continuous_scale="Blues",
        labels={
            "station_name": "Station",
            "energy_delivered_kwh": "Energy (kWh)"
        },
        title="Total Energy Delivered by Station"
    )
    fig_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_bar, width='stretch')

    # === Daily Sessions Trend ===
    st.subheader("📈 Daily Charging Sessions")

    sessions_df["date"] = sessions_df["timestamp"].dt.date
    daily = sessions_df.groupby("date").size().reset_index(name="sessions")

    fig_line = px.line(
        daily,
        x="date",
        y="sessions",
        title="Daily Charging Sessions (Last 30 Days)",
        labels={"date": "Date", "sessions": "Sessions"}
    )
    fig_line.update_traces(line_color="#00A8E8")
    fig_line.update_layout(template="plotly_dark")
    st.plotly_chart(fig_line, width='stretch')

    # === SoC Distribution ===
    st.subheader("🔋 State of Charge Distribution")

    col1, col2 = st.columns(2)

    with col1:
        fig_soc_start = px.histogram(
            sessions_df,
            x="soc_start",
            nbins=20,
            title="SoC at Arrival (%)",
            color_discrete_sequence=["#FF6B6B"]
        )
        fig_soc_start.update_layout(template="plotly_dark")
        st.plotly_chart(fig_soc_start, width='stretch')

    with col2:
        fig_soc_end = px.histogram(
            sessions_df,
            x="soc_end",
            nbins=20,
            title="SoC at Departure (%)",
            color_discrete_sequence=["#00A8E8"]
        )
        fig_soc_end.update_layout(template="plotly_dark")
        st.plotly_chart(fig_soc_end, width='stretch')

    # === Carbon Saved Chart ===
    st.subheader("🌍 Carbon Saved per Station")

    carbon_by_station = sessions_df.groupby("station_name")[
        "carbon_saved_kg"
    ].sum().reset_index()

    fig_carbon = px.pie(
        carbon_by_station,
        names="station_name",
        values="carbon_saved_kg",
        title="CO₂ Saved Distribution",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig_carbon.update_layout(template="plotly_dark")
    st.plotly_chart(fig_carbon, width='stretch')

    # === Recent Sessions Table ===
    st.subheader("📋 Recent Charging Sessions")

    recent = sessions_df[[
        "timestamp", "station_name", "soc_start",
        "soc_end", "energy_delivered_kwh",
        "cost_eur", "carbon_saved_kg", "duration_min"
    ]].head(20)

    recent.columns = [
        "Time", "Station", "SoC Start (%)",
        "SoC End (%)", "Energy (kWh)",
        "Cost (€)", "CO₂ Saved (kg)", "Duration (min)"
    ]

    st.dataframe(recent, width='stretch')

    conn.close()