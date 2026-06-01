# battery.py
# แสดง battery gauge แบบ progress bar พร้อมสี status

import streamlit as st


# แสดง progress bar และข้อความ status ของ battery
# สีเขียว = ≥70%, เหลือง = 45-69%, แดง = <45%
def show_battery_gauge(latest_battery):
    st.subheader("🔋 Live Battery Gauge")

    battery_value = int(latest_battery)
    st.progress(battery_value / 100)

    if battery_value >= 70:
        st.success(f"Battery status: Healthy ({battery_value}%)")
    elif battery_value >= 45:
        st.warning(f"Battery status: Medium ({battery_value}%)")
    else:
        st.error(f"Battery status: Low ({battery_value}%)")
