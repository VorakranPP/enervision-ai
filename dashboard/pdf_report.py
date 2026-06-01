# pdf_report.py
# สร้าง PDF Energy Report ด้วย ReportLab — ใช้ใน Tab 1 (Realtime)

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# สร้าง PDF report จากข้อมูล telemetry ล่าสุด — คืนค่า BytesIO buffer
# ใช้ st.download_button() รับ buffer นี้เพื่อ download ไฟล์
def generate_pdf(latest_power, latest_battery, latest_solar, carbon_emission):
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("EnerVision AI Energy Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Latest Power Usage: {latest_power:.2f} kW",    styles["BodyText"]))
    elements.append(Paragraph(f"Battery Level: {latest_battery}%",             styles["BodyText"]))
    elements.append(Paragraph(f"Solar Output: {latest_solar:.2f} kW",          styles["BodyText"]))
    elements.append(Paragraph(f"Estimated CO₂ Emission: {carbon_emission:.2f} kg CO₂", styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer
