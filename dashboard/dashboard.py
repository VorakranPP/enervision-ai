import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from sklearn.linear_model import LinearRegression
import numpy as np
##Report
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="EnerVision AI Dashboard")

st.title("⚡ EnerVision AI Dashboard Mai 2026")

##add Tap
tab1, tab2 = st.tabs(["📊 Realtime Dashboard", "📁 Upload & AI Analysis"])

with tab1:
    st.subheader("Realtime Energy Monitoring")
    # code dashboard เดิมทั้งหมดไว้ตรงนี้

with tab2:
    st.subheader("📁 Upload & AI Analysis")

    uploaded_file = st.file_uploader(
        "Upload energy data file",
        type=["csv"]
    )

    if uploaded_file is not None:
        upload_df = pd.read_csv(uploaded_file)

        st.success("File uploaded successfully")
        st.dataframe(upload_df)

        peak_usage = upload_df["power_usage"].max()
        avg_usage = upload_df["power_usage"].mean()
        lowest_battery = upload_df["battery_level"].min()

        st.metric("⚡ Peak Usage", f"{peak_usage:.2f} kW")
        st.metric("📈 Average Usage", f"{avg_usage:.2f} kW")
        st.metric("🔋 Lowest Battery", f"{lowest_battery}%")

        st.subheader("AI Analysis Result")

        if peak_usage > 7:
            st.error("⚠️ High energy usage detected")
            st.write("Recommendation: Reduce non-critical loads during peak hours.")
        else:
            st.success("✅ Energy usage is within normal range.")

        if lowest_battery < 45:
            st.warning("🔋 Battery level dropped below recommended threshold")
            st.write("Recommendation: Improve battery charging schedule.")

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

##Report 
st.subheader("📥 Export Energy Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Telemetry CSV",
    data=csv,
    file_name="energy_telemetry.csv",
    mime="text/csv"
)

##Generate PDF Report

def generate_pdf():

    doc = SimpleDocTemplate("energy_report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("EnerVision AI Energy Report", styles['Title'])
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Latest Power Usage: {latest_power:.2f} kW",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Battery Level: {latest_battery}%",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Solar Output: {latest_solar:.2f} kW",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Estimated CO₂ Emission: {carbon_emission:.2f} kg CO₂",
            styles['BodyText']
        )
    )

    doc.build(elements)

    ##Generate PDFpip3 install reportlab

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

##Automated Monthly Reports
st.subheader("📅 Monthly Energy Summary")

total_power = df["power_usage"].sum()

average_power = df["power_usage"].mean()

total_carbon = total_power * 0.4

peak_usage = df["power_usage"].max()

st.write(f"⚡ Total Energy Usage: {total_power:.2f} kW")

st.write(f"📈 Average Power Usage: {average_power:.2f} kW")

st.write(f"🔥 Peak Usage: {peak_usage:.2f} kW")

st.write(f"🌍 Estimated Total CO₂: {total_carbon:.2f} kg CO₂")