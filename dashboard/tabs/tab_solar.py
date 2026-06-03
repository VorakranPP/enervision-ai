# tab_solar.py
# Solar ROI Calculator — Tab 3
# คำนวณผลตอบแทนการลงทุนโซลาร์เซลล์ อิงข้อมูลพื้นฐานเยอรมนี (BDEW / Bundesnetzagentur 2024)

import streamlit as st
import plotly.graph_objects as go

# ข้อมูลอ้างอิงพื้นฐานของเยอรมนี — ใช้เป็นค่า default ในทุกการคำนวณ
# อ้างอิง: BDEW Strompreisanalyse 2024, Bundesnetzagentur, UBA 2023
GERMAN_DEFAULTS = {
    "electricity_rate": 0.32,         # ราคาไฟฟ้าเฉลี่ย (€/kWh)
    "feed_in_tariff": 0.082,          # Einspeisevergütung สำหรับระบบ < 10 kWp (€/kWh)
    "co2_grid_factor": 0.434,         # CO₂ ของกริดไฟฟ้าเยอรมนี (kg CO₂/kWh)
    "panel_degradation_pct": 0.5,     # แผงเสื่อมสภาพ 0.5% ต่อปี — มาตรฐานอุตสาหกรรม
    "annual_maintenance": 150,        # ค่าบำรุงรักษาโดยประมาณ (€/ปี)
    "panel_watt": 400,                # กำลังวัตต์แผงที่นิยมในยุโรป
    "panel_price": 200,               # ราคาต่อแผง 400W (€)
    "installation_cost": 3000,        # ค่าติดตั้งเริ่มต้น — ระบบขนาดเล็ก (€)
    "panel_area_m2": 2.0,             # พื้นที่แผง 400W (m²)
    "self_consumption_ratio": 0.70,   # สัดส่วนไฟที่ใช้เองเฉลี่ยในเยอรมนี
}

# ชั่วโมงแดดสูงสุด (Peak Sun Hours/day) รายเมืองในเยอรมนี
# อ้างอิง: Solargis / PVGIS EU Commission
CITY_SUN_HOURS = {
    "Frankfurt am Main": 3.2,
    "München (Munich)":  3.8,
    "Berlin":            3.1,
    "Hamburg":           2.9,
    "Stuttgart":         3.5,
    "Köln (Cologne)":    3.0,
    "Düsseldorf":        2.9,
    "Leipzig":           3.2,
}


# คำนวณ ROI ของการติดตั้งโซลาร์เซลล์ทั้งหมด
# รองรับ feed-in tariff (Einspeisevergütung), CO₂ savings, และ panel degradation
# คืนค่า dict ผลลัพธ์รวมถึงข้อมูลรายปี 10 ปีสำหรับกราฟ
def calculate_solar_roi(
    roof_area, monthly_units, electricity_rate, panel_watt,
    panel_price, installation_cost, sun_hours, feed_in_tariff,
    annual_maintenance, panel_degradation
):
    panel_area          = GERMAN_DEFAULTS["panel_area_m2"]
    self_ratio          = GERMAN_DEFAULTS["self_consumption_ratio"]
    annual_demand       = monthly_units * 12

    # คำนวณจำนวนแผงที่เหมาะสมจากพื้นที่หลังคาและความต้องการไฟ
    max_by_area         = int(roof_area / panel_area)
    required_kw         = monthly_units / (30 * sun_hours)
    required_panels     = int((required_kw * 1000) / panel_watt) + 1
    recommended_panels  = min(max_by_area, required_panels)
    system_kw           = (recommended_panels * panel_watt) / 1000

    # พลังงานที่ผลิตได้ต่อปี (kWh)
    annual_generation   = system_kw * sun_hours * 365

    # แยกพลังงานเป็น self-consumed vs ขายคืน grid
    self_consumed       = min(annual_generation * self_ratio, annual_demand)
    grid_export         = annual_generation * (1 - self_ratio)

    # ผลประโยชน์ปีแรก: ประหยัดค่าไฟ + รายได้ feed-in - ค่าบำรุงรักษา
    savings_self        = self_consumed * electricity_rate
    income_export       = grid_export * feed_in_tariff
    annual_benefit_yr1  = savings_self + income_export - annual_maintenance

    total_cost          = (recommended_panels * panel_price) + installation_cost
    payback_years       = (total_cost / annual_benefit_yr1) if annual_benefit_yr1 > 0 else 0

    # CO₂ ที่ประหยัดได้ต่อปี (kg)
    co2_saved_kg        = annual_generation * GERMAN_DEFAULTS["co2_grid_factor"]

    # คำนวณ 10 ปี โดยลดประสิทธิภาพแผง (degradation) ทุกปี
    yearly_data     = []
    cumulative_net  = -total_cost
    for year in range(1, 11):
        factor      = (1 - panel_degradation) ** year
        gen         = annual_generation * factor
        used        = min(gen * self_ratio, annual_demand)
        exported    = gen * (1 - self_ratio)
        benefit     = used * electricity_rate + exported * feed_in_tariff - annual_maintenance
        cumulative_net += benefit
        yearly_data.append({
            "year":       year,
            "benefit":    round(benefit, 2),
            "cumulative": round(cumulative_net, 2),
        })

    return {
        "recommended_panels": recommended_panels,
        "required_panels":    required_panels,
        "system_kw":          round(system_kw, 2),
        "annual_generation":  round(annual_generation, 1),
        "savings_self":       round(savings_self, 2),
        "income_export":      round(income_export, 2),
        "annual_benefit":     round(annual_benefit_yr1, 2),
        "total_cost":         round(total_cost, 2),
        "payback_years":      round(payback_years, 1),
        "co2_saved_kg":       round(co2_saved_kg, 1),
        "ten_year_net":       round(yearly_data[-1]["cumulative"], 2),
        "yearly_data":        yearly_data,
    }


# สร้างกราฟ Plotly แสดง ROI สะสม 10 ปี และรายได้รายปี
# แท่งสีส้ม = รายได้ต่อปี, เส้นสีเขียว = ROI สะสม, เส้นประ = จุดคืนทุน
def render_10yr_chart(yearly_data, t):
    years       = [d["year"]       for d in yearly_data]
    benefits    = [d["benefit"]    for d in yearly_data]
    cumulatives = [d["cumulative"] for d in yearly_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=years, y=benefits,
        name=t.get("solar_annual_benefit", "Annual Benefit (€)"),
        marker_color="#FFA500",
        opacity=0.8,
    ))

    fig.add_trace(go.Scatter(
        x=years, y=cumulatives,
        name=t.get("solar_cumulative", "Cumulative ROI (€)"),
        mode="lines+markers",
        line=dict(color="#00CC44", width=2),
    ))

    # เส้นประแสดงจุด breakeven (0 = คืนทุน)
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="rgba(255,255,255,0.4)",
        annotation_text=t.get("solar_breakeven", "Breakeven"),
        annotation_font_color="white",
    )

    fig.update_layout(
        title=t.get("solar_10yr_title", "10-Year ROI Projection"),
        xaxis_title=t.get("solar_year", "Year"),
        yaxis_title="€",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )

    return fig


# ฟังก์ชันหลักที่ dashboard.py เรียกใช้ — แสดง UI ทั้งหมดของ Solar ROI tab
# รับ t = translation dictionary (DE หรือ EN) จาก translations.py
def render_solar(t):
    st.subheader(t["solar_title"])

    col_left, col_right = st.columns(2)

    with col_left:
        # เลือกเมือง → ดึงค่า sun hours อัตโนมัติ และ reset เมื่อเปลี่ยนเมือง
        city = st.selectbox(
            t.get("solar_city", "City / Region"),
            options=list(CITY_SUN_HOURS.keys()),
            index=0,
            key="solar_city",
        )

        # reset ค่า sun hours ในรั้วตัวแปรเมื่อ city เปลี่ยน
        if st.session_state.get("_solar_city_last") != city:
            st.session_state["solar_sun_hours"] = CITY_SUN_HOURS[city]
            st.session_state["_solar_city_last"] = city

        roof_area = st.number_input(
            t["roof_area"], min_value=1.0, value=30.0,
            key="solar_roof_area",
        )
        monthly_units = st.number_input(
            t["monthly_units"], min_value=1.0, value=300.0,
            key="solar_monthly_units",
            help=t.get("solar_monthly_help", "Average German household: 250–350 kWh/month"),
        )
        electricity_rate = st.number_input(
            t["electricity_rate"], min_value=0.01,
            value=GERMAN_DEFAULTS["electricity_rate"],
            step=0.01, format="%.3f",
            key="solar_electricity_rate",
            help=t.get("solar_rate_help", "BDEW 2024 average: €0.32/kWh"),
        )

    with col_right:
        panel_watt = st.number_input(
            t["panel_watt"], min_value=100,
            value=GERMAN_DEFAULTS["panel_watt"],
            key="solar_panel_watt",
        )
        panel_price = st.number_input(
            t["panel_price"], min_value=50,
            value=GERMAN_DEFAULTS["panel_price"],
            key="solar_panel_price",
            help=t.get("solar_panel_help", "Typical 400W panel in Germany: €150–250"),
        )
        installation_cost = st.number_input(
            t["installation_cost"], min_value=0,
            value=GERMAN_DEFAULTS["installation_cost"],
            key="solar_installation_cost",
            help=t.get("solar_install_help", "German average: €1,000–1,500 per kWp"),
        )
        
        sun_hours = st.number_input(
            t["sun_hours"], min_value=1.0,
            value=CITY_SUN_HOURS["Frankfurt am Main"],
            step=0.1, format="%.1f",
            key="solar_sun_hours_input",  # ← เปลี่ยน key ใหม่
            help=t.get("solar_sun_help", "Frankfurt 3.2h | Munich 3.8h | Hamburg 2.9h"),
        )

    # การตั้งค่าขั้นสูง — ซ่อนไว้ใน expander เพื่อไม่รบกวนผู้ใช้ทั่วไป
    with st.expander(t.get("solar_advanced", "⚙️ Advanced Settings")):
        feed_in_tariff = st.number_input(
            t.get("solar_feed_in", "Feed-in Tariff — Einspeisevergütung (€/kWh)"),
            min_value=0.0, value=GERMAN_DEFAULTS["feed_in_tariff"],
            step=0.001, format="%.3f",
            key="solar_feed_in",
            help=t.get("solar_feed_help", "Germany 2024: €0.082/kWh for < 10 kWp (Bundesnetzagentur)"),
        )
        annual_maintenance = st.number_input(
            t.get("solar_maintenance", "Annual Maintenance (€/year)"),
            min_value=0, value=GERMAN_DEFAULTS["annual_maintenance"],
            key="solar_maintenance",
            help=t.get("solar_maint_help", "Typical German residential: €100–200/year"),
        )
        # slider แสดง % ต่อปี (0.1–1.0), หาร 100 เพื่อใช้ในสูตร
        panel_degradation = st.slider(
            t.get("solar_degradation", "Panel Degradation (%/year)"),
            min_value=0.1, max_value=1.0,
            value=float(GERMAN_DEFAULTS["panel_degradation_pct"]),
            step=0.1,
            key="solar_degradation",
            help=t.get("solar_deg_help", "Standard: 0.5%/year. Most panels warranted for 25 years."),
        ) / 100

    # --- คำนวณ ROI ---
    result = calculate_solar_roi(
        roof_area, monthly_units, electricity_rate, panel_watt,
        panel_price, installation_cost, sun_hours, feed_in_tariff,
        annual_maintenance, panel_degradation,
    )

    # --- แสดงผลสรุป Row 1: ตัวเลขหลัก ---
    st.subheader(t["summary_title"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["panels"],       f"{result['recommended_panels']}",        f"{result['system_kw']} kWp")
    col2.metric(t["install_cost"], f"€{result['total_cost']:,.0f}")
    col3.metric(t["save_month"],   f"€{result['annual_benefit'] / 12:,.0f}/mo")
    col4.metric(t["payback"],      f"{result['payback_years']:.1f} yrs")

    # --- แสดงผลสรุป Row 2: รายละเอียด ---
    col5, col6, col7, col8 = st.columns(4)
    col5.metric(t.get("solar_annual_gen",   "Annual Generation"),  f"{result['annual_generation']:,.0f} kWh")
    col6.metric(t.get("solar_self_savings", "Self-use Savings"),   f"€{result['savings_self']:,.0f}/yr")
    col7.metric(t.get("solar_feed_income",  "Feed-in Income"),     f"€{result['income_export']:,.0f}/yr")
    col8.metric(t.get("solar_co2_saved",    "CO₂ Saved"),          f"{result['co2_saved_kg']:,.0f} kg/yr")

    # ผลตอบแทนสุทธิ 10 ปี — สีเขียว = กำไร, สีแดง = ขาดทุน
    net_color = "normal" if result["ten_year_net"] > 0 else "inverse"
    st.metric(
        t.get("solar_10yr_net", "10-Year Net Return"),
        f"€{result['ten_year_net']:,.0f}",
        delta=f"€{result['ten_year_net']:,.0f}",
        delta_color=net_color,
    )

    # --- กราฟ ROI 10 ปี ---
    fig = render_10yr_chart(result["yearly_data"], t)
    st.plotly_chart(fig, use_container_width=True)

    # --- คำแนะนำ ---
    st.subheader(t["recommendation"])

    if result["recommended_panels"] < result["required_panels"]:
        st.warning(t["roof_warning"])
    else:
        st.success(t["roof_ok"])

    if result["payback_years"] <= 8:
        st.success(t["roi_strong"])
    elif result["payback_years"] <= 14:
        st.info(t["roi_moderate"])
    else:
        st.warning(t["roi_long"])

    # แสดง CO₂ เทียบเท่าต้นไม้ (ต้นไม้ 1 ต้นดูด CO₂ ~22 kg/ปี)
    trees = int(result["co2_saved_kg"] / 22)
    st.info(
        f"🌳 {result['co2_saved_kg']:,.0f} kg CO₂/yr — "
        f"{t.get('solar_co2_trees', 'equivalent to planting')} "
        f"{trees} {t.get('solar_trees_unit', 'trees')}"
    )
