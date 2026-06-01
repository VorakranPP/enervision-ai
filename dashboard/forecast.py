# forecast.py
# Prophet ML forecasting component สำหรับพยากรณ์การใช้ไฟฟ้า 48 ชั่วโมงข้างหน้า
# ใช้ใน Tab 1 (Realtime) — รับ connection ที่เปิดอยู่แล้วจาก tab_realtime.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet


# ดึงข้อมูล telemetry ล่าสุด 200 รายการ แล้วเทรน Prophet model เพื่อพยากรณ์ 48h
# แสดงกราฟ Plotly พร้อม confidence band (yhat_upper/yhat_lower) และ metric สรุป
def render_forecast(connection, t):
    st.subheader(t["forecast_title"])

    try:
        df_forecast = pd.read_sql_query("""
            SELECT timestamp, power_usage FROM telemetry
            ORDER BY id DESC LIMIT 200
        """, connection)

        # Prophet ต้องการ column ชื่อ ds (datetime) และ y (value)
        df_prophet = df_forecast.rename(columns={"timestamp": "ds", "power_usage": "y"})
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
        df_prophet = df_prophet.sort_values("ds")

        if len(df_prophet) < 10:
            st.warning("ข้อมูลยังน้อยเกินไปสำหรับ forecast")
            return

        with st.spinner("🔮 Generating 48-hour forecast..."):
            model = Prophet(
                changepoint_prior_scale=0.05,
                yearly_seasonality=False,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            model.fit(df_prophet)
            future   = model.make_future_dataframe(periods=48, freq="h")
            forecast = model.predict(future)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_prophet["ds"], y=df_prophet["y"],
            name="Actual", line=dict(color="cyan")
        ))
        fig.add_trace(go.Scatter(
            x=forecast["ds"], y=forecast["yhat"],
            name="Forecast", line=dict(color="orange", dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=forecast["ds"], y=forecast["yhat_upper"],
            fill=None, line=dict(color="rgba(255,165,0,0.2)"),
            name="Upper Bound"
        ))
        fig.add_trace(go.Scatter(
            x=forecast["ds"], y=forecast["yhat_lower"],
            fill="tonexty", line=dict(color="rgba(255,165,0,0.2)"),
            name="Lower Bound"
        ))

        fig.update_layout(
            title="48-Hour Power Usage Forecast",
            xaxis_title="Time", yaxis_title="Power Usage (kW)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, width="stretch")

        # แสดง metric สรุปจาก 48 ชั่วโมงถัดไปเท่านั้น
        next_48h      = forecast[forecast["ds"] > df_prophet["ds"].max()]
        peak_forecast = next_48h["yhat"].max()
        avg_forecast  = next_48h["yhat"].mean()

        col1, col2 = st.columns(2)
        col1.metric(t["forecast_peak"], f"{peak_forecast:.2f} kW")
        col2.metric(t["forecast_avg"],  f"{avg_forecast:.2f} kW")

    except Exception as e:
        st.error(f"⚠️ Forecast error: {e}")
        st.info("Try refreshing the page or check database connection.")
