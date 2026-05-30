import streamlit as st
import requests
from styles import apply_login_styles, render_login_header
from translations import TRANSLATIONS

##Separate File##
from tabs.tab_realtime import render_realtime
from tabs.tab_upload import render_upload
from tabs.tab_solar import render_solar
from tabs.tab_admin import render_admin
from tabs.tab_ev import render_ev

st.set_page_config(page_title="EnerVision AI Dashboard")

# Language selector
lang = st.sidebar.selectbox(
    "🌐 Sprache / Language",
    ["DE", "EN"],
    index=0
)
t = TRANSLATIONS[lang]

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

# Login
if st.session_state.token is None:

    apply_login_styles()
    render_login_header(t)

    username = st.text_input(t["login_username"])
    password = st.text_input(t["login_password"], type="password")

    if st.button(t["login_button"]):

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
                st.success(t["login_success"])
                st.rerun()

            elif response.status_code == 401:
                st.error(t["login_invalid"])

            elif response.status_code == 500:
                st.error(t["login_server_error"])

            else:
                st.error(f"⚠️ Unexpected error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error(t["login_connection_error"])

        except requests.exceptions.Timeout:
            st.error(t["login_timeout"])

        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

    st.stop()

# Profile + Logout
col1, col2 = st.columns([6, 2])

with col1:
    st.markdown(f"👤 {st.session_state.username} | 🔐 {st.session_state.role}")

with col2:
    if st.button(t["logout"]):
        st.session_state.token = None
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

st.title(t["app_title"])

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t["tab_realtime"],
    t["tab_upload"],
    t["tab_solar"],
    t["tab_ev"],
    t["tab_admin"]
])

with tab1:
    render_realtime(
        st.session_state.token,
        st.session_state.username,
        st.session_state.role,
        st.session_state.last_alert_time,
        t
    )

with tab2:
    render_upload(t)

with tab3:
    render_solar(t)

with tab4:
    render_ev(t)

with tab5:
    render_admin(
        st.session_state.token,
        st.session_state.username,
        t)