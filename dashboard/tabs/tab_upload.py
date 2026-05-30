# tab_upload.py
# Upload & AI Analysis - Tab 2

import streamlit as st
import pandas as pd


def render_upload():

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
            for col in ["power_usage", "battery_level"]
        ):
            st.error(
                "CSV must include power_usage and battery_level columns."
            )

        else:

            peak_usage = upload_df["power_usage"].max()
            avg_usage = upload_df["power_usage"].mean()
            lowest_battery = upload_df["battery_level"].min()

            col1, col2, col3 = st.columns(3)
            col1.metric("⚡ Peak Usage", f"{peak_usage:.2f} kW")
            col2.metric("📈 Average Usage", f"{avg_usage:.2f} kW")
            col3.metric("🔋 Lowest Battery", f"{lowest_battery}%")

            st.subheader("AI Analysis Result")

            if peak_usage > 7:
                st.error("⚠️ High energy usage detected")
                st.write(
                    "Recommendation: Reduce non-critical loads during peak hours."
                )
            else:
                st.success("✅ Energy usage is within normal range.")

            if lowest_battery < 45:
                st.warning(
                    "🔋 Battery level dropped below recommended threshold"
                )
                st.write(
                    "Recommendation: Improve battery charging schedule."
                )