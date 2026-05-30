# styles.py
# EnerVision UI Styles — Login Page CSS

import streamlit as st


def apply_login_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; }

    .stApp {
        background: #0D1B2A !important;
        background-image:
            linear-gradient(rgba(0,168,232,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,168,232,0.04) 1px, transparent 1px) !important;
        background-size: 60px 60px !important;
    }

    div[data-testid="stVerticalBlock"] {
        max-width: 420px;
        margin: 80px auto;
        background: rgba(26,43,60,0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0,168,232,0.2);
        border-radius: 24px;
        padding: 48px 44px;
        box-shadow: 0 32px 64px rgba(0,0,0,0.4);
    }

    h1 {
        font-family: 'Syne', sans-serif !important;
        color: #F0F4F8 !important;
        font-size: 28px !important;
    }

    label {
        font-family: 'DM Sans', sans-serif !important;
        color: #00A8E8 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    input[type="text"], input[type="password"] {
        background: rgba(0,168,232,0.05) !important;
        border: 1px solid rgba(0,168,232,0.15) !important;
        border-radius: 12px !important;
        color: #0F4F8 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    input[type="text"]:focus, input[type="password"]:focus {
        border-color: #FFA8E8 !important;
        box-shadow: 0 0 0 3px rgba(0,168,232,0.1) !important;
    }

    div[data-testid="stButton"] button {
        width: 100% !important;
        background: linear-gradient(135deg, #00A8E8, #00D4FF) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #0D1B2A !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 15px !important;
        transition: all 0.2s !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 24px rgba(0,168,232,0.35) !important;
    }
            

    </style>
    """, unsafe_allow_html=True)


def render_login_header(t):
    st.markdown(f"""
    <div style='text-align:center; margin-bottom: 8px;'>
        <div style='font-size:44px'>⚡</div>
        <div style='font-family:Syne,sans-serif; font-weight:800;
                    font-size:28px; color:#F0F4F8;'>
            Ener<span style='color:#00A8E8'>Vision</span>
        </div>
        <div style='color:#8899AA; font-size:14px; margin-top:4px;'>
            {t["login_subtitle"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
