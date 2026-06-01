# alerts.py
# ระบบส่ง email alert ผ่าน Gmail SMTP เมื่อพลังงานผิดปกติ
# ต้องตั้งค่า GMAIL_USER และ GMAIL_PASSWORD ใน .env

import os
import yagmail
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


# ส่ง email alert ผ่าน Gmail SMTP — ใช้ yagmail library
# คืนค่า True ถ้าส่งสำเร็จ, False ถ้า error (แสดง warning ใน UI)
def send_alert_email(subject, body):
    try:
        yag = yagmail.SMTP(
            user=os.getenv("GMAIL_USER"),
            password=os.getenv("GMAIL_PASSWORD")
        )
        yag.send(
            to=os.getenv("GMAIL_USER"),
            subject=subject,
            contents=body
        )
        return True

    except Exception as e:
        st.warning(f"Email alert failed: {e}")
        return False
