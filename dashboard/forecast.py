# forecast.py
# Replaced Linear Regression with Prophet (Meta) for 48-hour energy forecasting

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

def render_forecast(connection):

    st.subheader("🔮 AI Energy Forecast (Prophet)")

    try:
        query_forecast = """
        SELECT timestamp, power_usage
        FROM telemetry
        ORDER BY id DESC
        LIMIT 200
        """
        df_forecast = pd.read_sql_query(query_forecast, connection)

        df_prophet = df_forecast.rename(columns={
            "timestamp": "ds",
            "power_usage": "y"
        })
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
        df_prophet = df_prophet.sort_values("ds")

        if len(df_prophet) < 10:
            st.warning("ข้อมูลยังน้อยเกินไปสำหรับ forecast")
            return

        # ✅ เพิ่ม spinner ตรงนี้
        with st.spinner("🔮 Generating 48-hour forecast..."):

            model = Prophet(
                changepoint_prior_scale=0.05,
                yearly_seasonality=False,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            model.fit(df_prophet)

            future = model.make_future_dataframe(periods=48, freq="h")
            forecast = model.predict(future)

        # แสดงผลหลัง spinner เสร็จ
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_prophet["ds"],
            y=df_prophet["y"],
            name="Actual",
            line=dict(color="cyan")
        ))

        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            name="Forecast",
            line=dict(color="orange", dash="dash")
        ))

        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_upper"],
            fill=None,
            line=dict(color="rgba(255,165,0,0.2)"),
            name="Upper Bound"
        ))

        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_lower"],
            fill="tonexty",
            line=dict(color="rgba(255,165,0,0.2)"),
            name="Lower Bound"
        ))

        fig.update_layout(
            title="48-Hour Power Usage Forecast",
            xaxis_title="Time",
            yaxis_title="Power Usage (kW)",
            template="plotly_dark"
        )

        st.plotly_chart(fig, width='stretch')

        next_48h = forecast[forecast["ds"] > df_prophet["ds"].max()]
        peak_forecast = next_48h["yhat"].max()
        avg_forecast = next_48h["yhat"].mean()

        col1, col2 = st.columns(2)
        col1.metric("📈 Peak (48h)", f"{peak_forecast:.2f} kW")
        col2.metric("📊 Average (48h)", f"{avg_forecast:.2f} kW")

    except Exception as e:
        st.error(f"⚠️ Forecast error: {e}")
        st.info("Try refreshing the page or check database connection.")