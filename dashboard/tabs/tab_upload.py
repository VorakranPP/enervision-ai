# tab_upload.py
# Upload & AI Full Analytics - Tab 2

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet


# แสดง Tab 2: CSV upload + AI analysis แบบครบวงจร
# รวม: summary metrics, carbon/cost, trend charts, temperature correlation,
#       Z-score anomaly detection, Prophet 48h forecast, AI recommendations, CSV export
def render_upload(t):

    st.subheader(t["upload_title"])

    uploaded_file = st.file_uploader(
        t["upload_label"],
        type=["csv"],
        help="CSV ต้องมี column: timestamp, power_usage, battery_level (solar_output optional)"
    )

    if uploaded_file is None:

        st.info(t["upload_no_file"])

        template = pd.DataFrame({
            "timestamp": ["2026-05-01 08:00:00", "2026-05-01 08:15:00"],
            "power_usage": [3.5, 4.2],
            "solar_output": [2.1, 2.8],
            "battery_level": [75, 72],
            "site": ["Site-A", "Site-A"],
            "temperature_c": [28.5, 29.0]
        })

        st.download_button(
            label=t["upload_template_btn"],
            data=template.to_csv(index=False).encode("utf-8"),
            file_name="energy_template.csv",
            mime="text/csv"
        )
        return

    # === Load Data ===
    upload_df = pd.read_csv(uploaded_file, sep=",", on_bad_lines="skip")
    st.success(t["upload_success"])

    required_cols = ["power_usage", "battery_level"]
    if not all(col in upload_df.columns for col in required_cols):
        st.error("❌ CSV ต้องมี column: power_usage และ battery_level")
        return

    if "timestamp" in upload_df.columns:
        upload_df["timestamp"] = pd.to_datetime(upload_df["timestamp"])
        upload_df = upload_df.sort_values("timestamp")

    # === Filters ===
    with st.expander("🔍 Filters", expanded=False):
        filter_col1, filter_col2 = st.columns(2)

        # Site filter
        if "site" in upload_df.columns:
            all_sites = sorted(upload_df["site"].dropna().unique().tolist())
            selected_sites = filter_col1.multiselect(
                "🏭 Site",
                options=all_sites,
                default=all_sites
            )
            if selected_sites:
                upload_df = upload_df[upload_df["site"].isin(selected_sites)]

        # Date range filter
        if "timestamp" in upload_df.columns and len(upload_df) > 0:
            min_date = upload_df["timestamp"].min().date()
            max_date = upload_df["timestamp"].max().date()
            date_range = filter_col2.date_input(
                "📅 Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                start_date, end_date = date_range
                upload_df = upload_df[
                    (upload_df["timestamp"].dt.date >= start_date) &
                    (upload_df["timestamp"].dt.date <= end_date)
                ]

    if len(upload_df) == 0:
        st.warning("⚠️ ไม่มีข้อมูลหลังกรอง — กรุณาปรับ filter")
        return

    st.dataframe(upload_df.head(20), use_container_width=True)
    st.caption(f"{t['upload_total_rows']}: {len(upload_df):,}")

    st.divider()

    # === Summary Metrics ===
    st.subheader(t["upload_summary"])

    peak_usage = upload_df["power_usage"].max()
    avg_usage = upload_df["power_usage"].mean()
    min_usage = upload_df["power_usage"].min()
    lowest_battery = upload_df["battery_level"].min()
    avg_battery = upload_df["battery_level"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("⚡ Peak Usage", f"{peak_usage:.2f} kW")
    col2.metric("📈 Avg Usage", f"{avg_usage:.2f} kW")
    col3.metric("📉 Min Usage", f"{min_usage:.2f} kW")
    col4.metric("🔋 Lowest Battery", f"{lowest_battery}%")
    col5.metric("🔋 Avg Battery", f"{avg_battery:.0f}%")

    st.divider()

    # === Carbon & Cost ===
    st.subheader(t["upload_carbon"])

    interval_hours = 15 / 60  # 15 นาที
    total_kwh = upload_df["power_usage"].sum() * interval_hours
    total_carbon = total_kwh * 0.4
    total_cost = total_kwh * 0.35

    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ Total Energy", f"{total_kwh:.2f} kWh")
    col2.metric("🌍 CO₂ Emission", f"{total_carbon:.2f} kg")
    col3.metric("💰 Est. Cost", f"€{total_cost:.2f}")

    st.divider()

    # === Charts ===
    st.subheader(t["upload_power_trend"])

    if "timestamp" in upload_df.columns:
        fig_power = px.line(
            upload_df,
            x="timestamp",
            y="power_usage",
            title="Power Usage Over Time",
            labels={"power_usage": "kW", "timestamp": "Time"},
            color_discrete_sequence=["#00A8E8"]
        )
        fig_power.update_layout(template="plotly_dark")
        st.plotly_chart(fig_power, use_container_width=True)

        if "solar_output" in upload_df.columns:
            st.subheader(t["upload_solar_compare"])
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Scatter(
                x=upload_df["timestamp"],
                y=upload_df["power_usage"],
                name="Power Usage",
                line=dict(color="#FF6B6B")
            ))
            fig_compare.add_trace(go.Scatter(
                x=upload_df["timestamp"],
                y=upload_df["solar_output"],
                name="Solar Output",
                line=dict(color="#FFD700")
            ))
            fig_compare.update_layout(
                template="plotly_dark",
                title="Power Usage vs Solar Output"
            )
            st.plotly_chart(fig_compare, use_container_width=True)

    st.subheader(t["upload_battery_trend"])
    if "timestamp" in upload_df.columns:
        fig_battery = px.line(
            upload_df,
            x="timestamp",
            y="battery_level",
            title="Battery Level Over Time",
            labels={"battery_level": "%", "timestamp": "Time"},
            color_discrete_sequence=["#00E5A0"]
        )
        fig_battery.update_layout(template="plotly_dark")
        st.plotly_chart(fig_battery, use_container_width=True)

    # === Temperature Correlation ===
    if "temperature_c" in upload_df.columns:
        st.subheader("🌡️ Temperature vs Power Usage")
        corr = upload_df[["power_usage", "temperature_c"]].corr().iloc[0, 1]
        st.caption(f"Pearson Correlation: {corr:.3f}")

        fig_temp = px.scatter(
            upload_df,
            x="temperature_c",
            y="power_usage",
            trendline="ols",
            title="Temperature vs Power Usage",
            labels={"temperature_c": "Temperature (°C)", "power_usage": "Power Usage (kW)"},
            color_discrete_sequence=["#FF6B6B"]
        )
        fig_temp.update_layout(template="plotly_dark")
        st.plotly_chart(fig_temp, use_container_width=True)

    st.divider()

    # === AI Anomaly Detection ===
    st.subheader(t["upload_anomaly_title"])

    mean_power = upload_df["power_usage"].mean()
    std_power = upload_df["power_usage"].std()
    threshold = mean_power + 2 * std_power

    anomalies = upload_df[upload_df["power_usage"] > threshold]

    col1, col2 = st.columns(2)
    col1.metric(t["upload_anomalies"], f"{len(anomalies)}")
    col2.metric(t["upload_threshold"], f"{threshold:.2f} kW")

    if len(anomalies) > 0:
        st.error(f"{t['upload_anomaly_found']}: {len(anomalies)}")
        if "timestamp" in upload_df.columns:
            fig_anomaly = go.Figure()
            fig_anomaly.add_trace(go.Scatter(
                x=upload_df["timestamp"],
                y=upload_df["power_usage"],
                name="Power Usage",
                line=dict(color="cyan")
            ))
            fig_anomaly.add_trace(go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies["power_usage"],
                mode="markers",
                name="Anomaly",
                marker=dict(color="red", size=8, symbol="x")
            ))
            fig_anomaly.add_hline(
                y=threshold,
                line_dash="dash",
                line_color="orange",
                annotation_text=f"Threshold: {threshold:.2f} kW"
            )
            fig_anomaly.update_layout(template="plotly_dark", title="Anomaly Detection")
            st.plotly_chart(fig_anomaly, use_container_width=True)
    else:
        st.success(t["upload_no_anomaly"])

    st.divider()

    # === AI Forecast ===
    st.subheader(t["upload_forecast_title"])

    forecast = None

    if "timestamp" in upload_df.columns and len(upload_df) >= 10:

        with st.spinner(t["upload_spinner"]):
            try:
                df_prophet = upload_df[["timestamp", "power_usage"]].rename(
                    columns={"timestamp": "ds", "power_usage": "y"}
                )

                model = Prophet(
                    changepoint_prior_scale=0.05,
                    yearly_seasonality=False,
                    weekly_seasonality=True,
                    daily_seasonality=True
                )
                model.fit(df_prophet)

                future = model.make_future_dataframe(periods=48, freq="h")
                forecast = model.predict(future)

                fig_forecast = go.Figure()
                fig_forecast.add_trace(go.Scatter(
                    x=df_prophet["ds"], y=df_prophet["y"],
                    name="Actual", line=dict(color="cyan")
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast["ds"], y=forecast["yhat"],
                    name="Forecast", line=dict(color="orange", dash="dash")
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast["ds"], y=forecast["yhat_upper"],
                    fill=None, line=dict(color="rgba(255,165,0,0.2)"),
                    name="Upper Bound"
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast["ds"], y=forecast["yhat_lower"],
                    fill="tonexty", line=dict(color="rgba(255,165,0,0.2)"),
                    name="Lower Bound"
                ))
                fig_forecast.update_layout(
                    template="plotly_dark",
                    title="48-Hour Forecast from Uploaded Data"
                )
                st.plotly_chart(fig_forecast, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Forecast ล้มเหลว: {e}")
                forecast = None

    else:
        st.info(t["upload_forecast_need"])

    st.divider()

    # === AI Recommendations ===
    st.subheader(t["upload_rec_title"])

    avg_solar = upload_df["solar_output"].mean() if "solar_output" in upload_df.columns else 999

    recommendations = []

    if peak_usage > 7:
        recommendations.append(t["upload_rec_high_peak"])
    if avg_usage > 5:
        recommendations.append(t["upload_rec_high_avg"])
    if lowest_battery < 20:
        recommendations.append(t["upload_rec_low_battery"])
    if avg_battery < 50:
        recommendations.append(t["upload_rec_low_avg_battery"])
    if avg_solar < 1:
        recommendations.append(t["upload_rec_low_solar"])
    if len(anomalies) > 5:
        recommendations.append(t["upload_rec_anomaly"])

    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.success(t["upload_rec_ok"])

    st.divider()

    # === Export ===
    st.subheader(t["upload_export"])

    export_col1, export_col2 = st.columns(2)

    csv = upload_df.to_csv(index=False).encode("utf-8")
    export_col1.download_button(
        label=t["upload_export_btn"],
        data=csv,
        file_name="analyzed_energy.csv",
        mime="text/csv"
    )

    if forecast is not None:
        forecast_csv = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(index=False).encode("utf-8")
        export_col2.download_button(
            label="📥 Download Forecast CSV",
            data=forecast_csv,
            file_name="forecast_energy.csv",
            mime="text/csv"
        )
