# tab_solar.py
# Solar ROI Calculator - Tab 3

import streamlit as st


def render_solar(t):

    st.subheader(t["solar_title"])

    roof_area = st.number_input(t["roof_area"], min_value=1.0, value=30.0, key="solar_roof_area")
    monthly_units = st.number_input(t["monthly_units"], min_value=1.0, value=500.0, key="solar_monthly_units")
    electricity_rate = st.number_input(t["electricity_rate"], min_value=1.0, value=4.5, key="solar_electricity_rate")
    panel_watt = st.number_input(t["panel_watt"], min_value=100, value=550, key="solar_panel_watt")
    panel_price = st.number_input(t["panel_price"], min_value=1000, value=4500, key="solar_panel_price")
    installation_cost = st.number_input(t["installation_cost"], min_value=0, value=80000, key="solar_installation_cost")
    sun_hours = st.number_input(t["sun_hours"], min_value=1.0, value=4.5, key="solar_sun_hours")

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

    st.subheader(t["summary_title"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["panels"], f"{recommended_panels}")
    col2.metric(t["install_cost"], f"{total_cost:,.0f}")
    col3.metric(t["save_month"], f"{monthly_savings:,.0f}")
    col4.metric(t["payback"], f"{payback_years:.1f} yrs")

    st.write(f"🏠 {t['roof_area']}: {max_panels_by_area} panels")
    st.write(f"⚡ {t['monthly_units']}: {monthly_generation:.0f} kWh")
    st.write(f"💰 {t['install_cost']}: {total_cost:,.0f}")
    st.write(f"⏳ {t['payback']}: {payback_years:.1f} years")
    st.write(f"📈 10-year savings: {ten_year_savings:,.0f}")

    st.subheader(t["recommendation"])

    if recommended_panels < required_panels:
        st.warning(t["roof_warning"])
    else:
        st.success(t["roof_ok"])

    if payback_years <= 5:
        st.success(t["roi_strong"])
    elif payback_years <= 8:
        st.info(t["roi_moderate"])
    else:
        st.warning(t["roi_long"])