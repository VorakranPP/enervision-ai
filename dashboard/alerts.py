# alerts.py
import os
import yagmail
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


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