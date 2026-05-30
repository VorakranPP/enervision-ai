# tab_solar.py
# Solar ROI Calculator - Tab 3

import streamlit as st


def render_solar(t):

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
    required_panels = int((required_kw * 1000) / panel_watt) + 1
    recommended_panels = min(max_panels_by_area, required_panels)
    system_kw = (recommended_panels * panel_watt) / 1000
    monthly_generation = system_kw * sun_hours * 30
    monthly_savings = min(monthly_generation, monthly_units) * electricity_rate
    total_cost = (recommended_panels * panel_price) + installation_cost

    if monthly_savings > 0:
        payback_years = total_cost / (monthly_savings * 12)
    else:
        payback_years = 0

    ten_year_savings = monthly_savings * 12 * 10

    st.subheader("📊 Solar Recommendation Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Panels", f"{recommended_panels}")
    col2.metric("Install Cost", f"{total_cost:,.0f} THB")
    col3.metric("Save / Month", f"{monthly_savings:,.0f} THB")
    col4.metric("Payback", f"{payback_years:.1f} yrs")

    st.write(f"🏠 Maximum panels by roof area: {max_panels_by_area} panels")
    st.write(f"⚡ Estimated monthly solar generation: {monthly_generation:.0f} kWh")
    st.write(f"💰 Estimated total installation cost: {total_cost:,.0f} THB")
    st.write(f"⏳ Estimated payback period: {payback_years:.1f} years")
    st.write(f"📈 Estimated 10-year savings: {ten_year_savings:,.0f} THB")

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
        st.success("This installation has a strong return on investment.")
    elif payback_years <= 8:
        st.info("This installation has a moderate payback period.")
    else:
        st.warning(
            "Payback period is quite long. Consider reducing system cost or reviewing electricity usage."
        )