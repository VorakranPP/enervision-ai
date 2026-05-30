import streamlit as st


def show_battery_gauge(latest_battery):

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
   