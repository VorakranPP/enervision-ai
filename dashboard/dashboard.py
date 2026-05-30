import streamlit as st
import requests
from styles import apply_login_styles, render_login_header

##Separate File##
from tabs.tab_realtime import render_realtime
from tabs.tab_upload import render_upload
from tabs.tab_solar import render_solar
from tabs.tab_admin import render_admin
from tabs.tab_ev import render_ev

st.set_page_config(page_title="EnerVision AI Dashboard")


if "token" not in st.session_state:
    st.session_state.token = None

# ใส่ apply_login_styles() เฉพาะตอน token เป็น None เท่านั้น
if st.session_state.token is None:
    apply_login_styles()
    render_login_header()

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In →"):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/token",
                data={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token = token
                st.session_state.username = username

                me = requests.get(
                    "http://127.0.0.1:8000/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                )
                st.session_state.role = me.json()["role"]
                st.success("Login successful")
                st.rerun()

            elif response.status_code == 401:
                st.error("❌ Invalid username or password")

            elif response.status_code == 500:
                st.error("⚠️ Server error. Please contact admin.")

            else:
                st.error(f"⚠️ Unexpected error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to server. Please make sure backend is running.")

        except requests.exceptions.Timeout:
            st.error("⚠️ Server timeout. Please try again.")

        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

    st.stop()

if "role" not in st.session_state:
    st.session_state.role = None

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

# Login
if st.session_state.token is None:

    render_login_header()

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In →"):

        response = requests.post(
            "http://127.0.0.1:8000/token",
            data={"username": username, "password": password}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state.token = token
            st.session_state.username = username

            me = requests.get(
                "http://127.0.0.1:8000/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            st.session_state.role = me.json()["role"]
            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")

    st.stop()

# Profile + Logout
col1, col2 = st.columns([6, 2])

with col1:
    st.markdown(f"👤 {st.session_state.username} | 🔐 {st.session_state.role}")

with col2:
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

st.title("⚡ EnerVision Dashboard")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Realtime Dashboard",
    "📁 Upload & AI Analysis",
    "☀️ Solar ROI Calculator",
    "🚛 EV Charging",
    "👑 Admin",
])

with tab1:
    render_realtime(
        st.session_state.token,
        st.session_state.username,
        st.session_state.role,
        st.session_state.last_alert_time
    )

with tab2:
    render_upload()

with tab3:
    render_solar()

with tab4:
    render_ev()

with tab5:
    render_admin(
        st.session_state.token,
        st.session_state.username
    )