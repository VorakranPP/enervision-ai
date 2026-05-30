# pdf_report.py
# PDF Energy Report Generator using ReportLab

import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(latest_power, latest_battery, latest_solar, carbon_emission):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("EnerVision AI Energy Report", styles["Title"])
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(f"Latest Power Usage: {latest_power:.2f} kW", styles["BodyText"])
    )

    elements.append(
        Paragraph(f"Battery Level: {latest_battery}%", styles["BodyText"])
    )

    elements.append(
        Paragraph(f"Solar Output: {latest_solar:.2f} kW", styles["BodyText"])
    )

    elements.append(
        Paragraph(f"Estimated CO₂ Emission: {carbon_emission:.2f} kg CO₂", styles["BodyText"])
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer