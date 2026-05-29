import streamlit as st
import sqlite3
import pandas as pd
import requests
import numpy as np
import yagmail
import time
import plotly.graph_objects as go
from prophet import Prophet
from streamlit_autorefresh import st_autorefresh
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


st.set_page_config(page_title="EnerVision AI Dashboard")


def send_alert_email(subject, body):

    try:
        yag = yagmail.SMTP(
            user="XXXX@gmail.com",
            password="Your Password"
        )

        yag.send(
            to="XXXX@gmail.com",
            subject=subject,
            contents=body
        )

        return True

    except Exception as e:
        st.warning(f"Email alert failed: {e}")
        return False


if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0


# Login
if st.session_state.token is None:

    st.title("🔐 EnerVision Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            "http://127.0.0.1:8000/token",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.token = token
            st.session_state.username = username

            headers = {
                "Authorization": f"Bearer {token}"
            }

            me = requests.get(
                "http://127.0.0.1:8000/me",
                headers=headers
            )

            st.session_state.role = me.json()["role"]

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")

    st.stop()


# Profile + Logout
col1, col2 = st.columns([6, 2])

with col1:
    st.markdown(
        f"👤 {st.session_state.username} | 🔐 {st.session_state.role}"
    )

with col2:
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()


st.title("🔐 EnerVision Dashboard May 2026")


tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Realtime Dashboard",
    "📁 Upload & AI Analysis",
    "☀️ Solar ROI Calculator",
    "👑 Admin"
])


# =========================
# TAB 1: Realtime Dashboard
# =========================
with tab1:

    st.subheader("Realtime Energy Monitoring")

    st_autorefresh(
        interval=3000,
        key="datarefresh"
    )

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
        st.stop()

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
    st.subheader("🔋 Live Battery Gauge")

    battery_value = int(latest_battery)

    st.progress(
          battery_value / 100
        )

    if battery_value >= 70:
            st.success(
        f"Battery status: Healthy ({battery_value}%)"
            )

    elif battery_value >= 45:
            st.warning(
            f"Battery status: Medium ({battery_value}%)"
        )

    else:
            st.error(
            f"Battery status: Low ({battery_value}%)"
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

# =========================
# System Health
# =========================

    st.subheader("🖥️ System Health")

    if latest_power > 9:

        st.error("🔴 Critical")


    elif latest_battery < 45:

        st.warning("🟠 Warning")


    else:

        st.success("🟢 Healthy")

# =========================
# E-mail Alert
# =========================
    
    st.subheader("AI Anomaly Detection")

    alert_threshold = st.slider(

    "⚡ Alert Threshold (kW)",

    min_value=1,

    max_value=20,

    value=9

    )
    if latest_power > alert_threshold:

        st.error(
            f"⚠️ High Power Usage Detected: {latest_power} kW"
        )

        current_time = time.time()

        if current_time - st.session_state.last_alert_time > 1200:

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

        st.warning(
            f"🔋 Low Battery Level: {latest_battery}%"
        )

        current_time = time.time()

        if current_time - st.session_state.last_alert_time > 300:

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

# =========================
# Summary
# =========================
    st.subheader("📅 Monthly Energy Summary")

    total_power = df["power_usage"].sum()
    average_power = df["power_usage"].mean()
    total_carbon = total_power * 0.4
    peak_usage = df["power_usage"].max()


    st.write(f"⚡ Total Energy Usage: {total_power:.2f} kW")
    st.write(f"📈 Average Power Usage: {average_power:.2f} kW")
    st.write(f"🌍 Estimated Total CO₂: {total_carbon:.2f} kg CO₂")


# ===========Peak Usage Analysi==============

    st.subheader("⚡ Peak Usage Analysis")

    peak_row = df.loc[
        df["power_usage"].idxmax()
    ]

    peak_power = peak_row["power_usage"]

    st.write(f"🔥 Peak Usage: {peak_usage:.2f} kW")

    st.write(
        "This is the highest power usage found in the latest telemetry data."
    )

    if peak_power > alert_threshold:

        st.warning(
            "Recommendation: Reduce non-critical loads during peak usage periods."
        )

    else:

        st.success(
            "Peak usage is within the current alert threshold."
        )
    
    # ===========Cost Impact Analysis==============
    
    st.subheader("💰 Cost Impact Analysis")

    electricity_rate = 4.5

    estimated_cost = total_power * electricity_rate

    reduced_peak_power = peak_usage * 0.8

    estimated_saving = (peak_usage - reduced_peak_power) * electricity_rate * 30
    col1, col2, col3 = st.columns(3)
    
    col1.metric(
        "Estimated Energy Cost",
        f"{estimated_cost:,.2f} THB"
    )

    col2.metric(
        "Potential Saving if Peak Reduced 20%",
        f"{estimated_saving:,.2f} THB"
    )
    col3.metric(
        "Highest Power Usage",
        f"{peak_power:.2f} kW"
    )

    st.subheader("Realtime Energy Telemetry")

    st.dataframe(df)

    st.subheader("Power Usage Trend")
    st.line_chart(df["power_usage"])

    st.subheader("Solar Output Trend")
    st.line_chart(df["solar_output"])

    st.subheader("Battery Level Trend")
    st.line_chart(df["battery_level"])

### Replaced Linear Regression with Prophet (Meta) for 48-hour energy forecasting##cat backend/mqtt_simulator.py | grep -i "sleep\|interval\|time"

    st.subheader("🔮 AI Energy Forecast (Prophet)")

# ดึงข้อมูลเพิ่มขึ้น 200 แถว
    query_forecast = """
    SELECT timestamp, power_usage
    FROM telemetry
    ORDER BY id DESC
    LIMIT 200
    """
    df_forecast = pd.read_sql_query(query_forecast, connection)

    # เตรียมข้อมูลให้ Prophet
    df_prophet = df_forecast.rename(columns={
        "timestamp": "ds",
        "power_usage": "y"
    })
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
    df_prophet = df_prophet.sort_values("ds")

    if len(df_prophet) < 10:
        st.warning("ข้อมูลยังน้อยเกินไปสำหรับ forecast")
    else:
        model = Prophet(
            changepoint_prior_scale=0.05,
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=True
        )
        model.fit(df_prophet)

    # Forecast 48 ชั่วโมงข้างหน้า
        future = model.make_future_dataframe(
            periods=48,
            freq="h"
        )
        forecast = model.predict(future)

    # Plot ด้วย Plotly
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

    st.plotly_chart(fig, use_container_width=True)

    next_48h = forecast[forecast["ds"] > df_prophet["ds"].max()]
    peak_forecast = next_48h["yhat"].max()
    avg_forecast = next_48h["yhat"].mean()

    col1, col2 = st.columns(2)
    col1.metric("📈 Peak (48h)", f"{peak_forecast:.2f} kW")
    col2.metric("📊 Average (48h)", f"{avg_forecast:.2f} kW")


    st.subheader("📥 Export Energy Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Telemetry CSV",
        data=csv,
        file_name="energy_telemetry.csv",
        mime="text/csv"
    )

# =========================
# -----PDF-----
# =========================
    def generate_pdf():

        doc = SimpleDocTemplate("energy_report.pdf")

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "EnerVision AI Energy Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph(
                f"Latest Power Usage: {latest_power:.2f} kW",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Battery Level: {latest_battery}%",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Solar Output: {latest_solar:.2f} kW",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Estimated CO₂ Emission: {carbon_emission:.2f} kg CO₂",
                styles["BodyText"]
            )
        )

        doc.build(elements)


    st.subheader("📄 PDF Energy Report")

    if st.button("Generate PDF Report"):

        generate_pdf()

        with open("energy_report.pdf", "rb") as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name="energy_report.pdf",
                mime="application/pdf"
            )

    connection.close()


# =========================
# TAB 2: Upload Analysis
# =========================
with tab2:

    st.subheader("📁 Upload & AI Analysis")

    uploaded_file = st.file_uploader(
        "Upload energy data file",
        type=["csv"]
    )

    if uploaded_file is not None:

        upload_df = pd.read_csv(
            uploaded_file,
            sep=",",
            on_bad_lines="skip"
        )

        st.success("File uploaded successfully")
        st.dataframe(upload_df)

        if not all(
            col in upload_df.columns
            for col in [
                "power_usage",
                "battery_level"
            ]
        ):
            st.error(
                "CSV must include power_usage and battery_level columns."
            )

        else:

            peak_usage = upload_df["power_usage"].max()
            avg_usage = upload_df["power_usage"].mean()
            lowest_battery = upload_df["battery_level"].min()

            st.metric(
                "⚡ Peak Usage",
                f"{peak_usage:.2f} kW"
            )

            st.metric(
                "📈 Average Usage",
                f"{avg_usage:.2f} kW"
            )

            st.metric(
                "🔋 Lowest Battery",
                f"{lowest_battery}%"
            )

            st.subheader("AI Analysis Result")

            if peak_usage > 7:
                st.error("⚠️ High energy usage detected")
                st.write(
                    "Recommendation: Reduce non-critical loads during peak hours."
                )
            else:
                st.success(
                    "✅ Energy usage is within normal range."
                )

            if lowest_battery < 45:
                st.warning(
                    "🔋 Battery level dropped below recommended threshold"
                )
                st.write(
                    "Recommendation: Improve battery charging schedule."
                )


# =========================
# TAB 3: Solar ROI Calculator
# =========================
with tab3:

    st.subheader("☀️ Solar Installation ROI Calculator")

    roof_area = st.number_input(
        "Roof area available for solar panels (sqm)",
        min_value=1.0,
        value=30.0
    )

    monthly_units = st.number_input(
        "Monthly electricity usage (kWh)",
        min_value=1.0,
        value=500.0
    )

    electricity_rate = st.number_input(
        "Electricity rate (THB per kWh)",
        min_value=1.0,
        value=4.5
    )

    panel_watt = st.number_input(
        "Solar panel size (Watt per panel)",
        min_value=100,
        value=550
    )

    panel_price = st.number_input(
        "Estimated price per panel (THB)",
        min_value=1000,
        value=4500
    )

    installation_cost = st.number_input(
        "Installation and equipment cost (THB)",
        min_value=0,
        value=80000
    )

    sun_hours = st.number_input(
        "Average sunlight hours per day",
        min_value=1.0,
        value=4.5
    )

    panel_area = 2.2

    max_panels_by_area = int(roof_area / panel_area)

    required_kw = monthly_units / (30 * sun_hours)

    required_panels = int(
        (required_kw * 1000) / panel_watt
    ) + 1

    recommended_panels = min(
        max_panels_by_area,
        required_panels
    )

    system_kw = (
        recommended_panels * panel_watt
    ) / 1000

    monthly_generation = system_kw * sun_hours * 30

    monthly_savings = min(
        monthly_generation,
        monthly_units
    ) * electricity_rate

    total_cost = (
        recommended_panels * panel_price
    ) + installation_cost

    if monthly_savings > 0:
        payback_years = total_cost / (
            monthly_savings * 12
        )
    else:
        payback_years = 0

    ten_year_savings = monthly_savings * 12 * 10

    st.subheader("📊 Solar Recommendation Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Panels",
        f"{recommended_panels}"
    )

    col2.metric(
        "Install Cost",
        f"{total_cost:,.0f} THB"
    )

    col3.metric(
        "Save / Month",
        f"{monthly_savings:,.0f} THB"
    )

    col4.metric(
        "Payback",
        f"{payback_years:.1f} yrs"
    )

    st.write(
        f"🏠 Maximum panels by roof area: {max_panels_by_area} panels"
    )

    st.write(
        f"⚡ Estimated monthly solar generation: {monthly_generation:.0f} kWh"
    )

    st.write(
        f"💰 Estimated total installation cost: {total_cost:,.0f} THB"
    )

    st.write(
        f"⏳ Estimated payback period: {payback_years:.1f} years"
    )

    st.write(
        f"📈 Estimated 10-year savings: {ten_year_savings:,.0f} THB"
    )

    st.subheader("💡 Recommendation")

    if recommended_panels < required_panels:
        st.warning(
            "Roof area may not be enough to fully cover current electricity usage."
        )
    else:
        st.success(
            "Roof area is sufficient for the estimated solar requirement."
        )

    if payback_years <= 5:
        st.success(
            "This installation has a strong return on investment."
        )
    elif payback_years <= 8:
        st.info(
            "This installation has a moderate payback period."
        )
    else:
        st.warning(
            "Payback period is quite long. Consider reducing system cost or reviewing electricity usage."
        )


# =========================
# TAB 4: User Management
# =========================
with tab4:

    st.subheader("👑 Admin User Management")

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    if st.session_state.role != "admin":

        st.error("Admin only")

    else:

        st.subheader("➕ Add New User")

        new_username = st.text_input("New username")
        new_password = st.text_input(
            "New password",
            type="password"
        )

        new_user_role = st.selectbox(
            "Role for new user",
            ["viewer", "admin"]
        )

        if st.button("Create User"):

            create_response = requests.post(
                "http://127.0.0.1:8000/register",
                params={
                    "username": new_username,
                    "password": new_password,
                    "role": new_user_role
                },
                headers=headers
            )

            if create_response.status_code == 200:
                st.success(
                    f"User {new_username} created successfully"
                )
                st.rerun()
            else:
                st.error(
                    create_response.text
                )


        st.divider()

        st.subheader("👥 Existing Users")

        response = requests.get(
            "http://127.0.0.1:8000/users",
            headers=headers
        )

        if response.status_code == 200:

            users = response.json()

            for user in users:

                col1, col2, col3, col4 = st.columns(
                    [4, 2, 2, 2]
                )

                with col1:
                    st.write(user["username"])

                with col2:
                    selected_role = st.selectbox(
                        "Role",
                        ["viewer", "admin"],
                        index=0 if user["role"] == "viewer" else 1,
                        key=f"role_{user['username']}"
                    )

                with col3:
                    if st.button(
                        "Update",
                        key=f"update_{user['username']}"
                    ):

                        update_response = requests.put(
                            f"http://127.0.0.1:8000/users/{user['username']}/role",
                            params={
                                "role": selected_role
                            },
                            headers=headers
                        )

                        if update_response.status_code == 200:
                            st.success(
                                f"{user['username']} updated"
                            )
                            st.rerun()
                        else:
                            st.error("Update failed")

                with col4:
                    if user["username"] == st.session_state.username:
                        st.caption("Current user")
                    else:
                        if st.button(
                            "Delete",
                            key=f"delete_{user['username']}"
                        ):

                            delete_response = requests.delete(
                                f"http://127.0.0.1:8000/users/{user['username']}",
                                headers=headers
                            )

                            if delete_response.status_code == 200:
                                st.success(
                                    f"{user['username']} deleted"
                                )
                                st.rerun()
                            else:
                                st.error("Delete failed")

        else:
            st.error("Unable to load users")