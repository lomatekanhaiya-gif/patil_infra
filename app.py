# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application with SQLite Database)
import streamlit as st
import math
import sqlite3
import os
import datetime
import pandas as pd
import time
import urllib.parse
import random
import string

# Official Google GenAI SDK Import
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 🚨 Streamlit नियम: set_page_config नेहमी सर्वात आधी असावे!
st.set_page_config(page_title="PATIL INFRATECH", page_icon="🏗️", layout="centered")

# ==========================================
# 🕒 भारतीय वेळ (IST - Indian Standard Time) मिळवण्याचे फंक्शन
# ==========================================
def get_ist_time():
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    return ist_now

# ==========================================
# 🗄️ SQLITE DATABASE MANAGEMENT
# ==========================================
DB_FILE = "patil_infratech.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_key TEXT PRIMARY KEY,
            id TEXT,
            uid TEXT UNIQUE,
            pin TEXT,
            mobile TEXT,
            password TEXT,
            comment TEXT,
            admin_message TEXT,
            unread_notification INTEGER,
            is_premium INTEGER,
            premium_expiry TEXT,
            requested_code INTEGER,
            seen_popup INTEGER,
            master_code_uses INTEGER,
            last_active TEXT,
            activated_by TEXT
        )
    ''')

    # 2. History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            timestamp TEXT,
            user_note TEXT,
            report_data TEXT,
            FOREIGN KEY (user_key) REFERENCES users (user_key)
        )
    ''')

    # 3. Premium Codes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_codes (
            code TEXT PRIMARY KEY,
            assigned_to TEXT,
            used INTEGER,
            used_by TEXT,
            used_date TEXT,
            created_at TEXT
        )
    ''')

    # 4. Feature Locks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feature_locks (
            feature_name TEXT PRIMARY KEY,
            access_level TEXT
        )
    ''')

    # 5. Master Market Rates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_rates (
            material TEXT PRIMARY KEY,
            rate REAL
        )
    ''')

    # 6. Ads Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            desc TEXT,
            link TEXT,
            media_type TEXT,
            media_url TEXT,
            position TEXT,
            active INTEGER,
            date TEXT
        )
    ''')

    # Master Admin Default Entry
    cursor.execute("SELECT * FROM users WHERE user_key = ?", ("9999999999",))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (user_key, id, uid, pin, mobile, password, comment, admin_message, unread_notification, is_premium, premium_expiry, requested_code, seen_popup, master_code_uses, last_active, activated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("9999999999", "kanha", "KANHA_1P", "1234", "9999999999", "patiladmin123", "मास्टर ॲडमीन अकाउंट", "स्वागत आहे मास्टर कन्हैया! आपले पाटील इन्फ्राटेक मध्ये सर्व अधिकार अनलॉक्ड आहेत ⚡", 0, 1, "2099-12-31 23:59:59", 0, 1, 0, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), "Master Admin"))

    # Default Feature Locks
    default_locks = {
        "Civil Calculator": "Free",
        "Rate Analysis": "Free",
        "BBS": "Free",
        "WhatsApp Share": "Premium",
        "Civil AI Assistant": "Premium"
    }
    for f_name, f_lvl in default_locks.items():
        cursor.execute("INSERT OR IGNORE INTO feature_locks (feature_name, access_level) VALUES (?, ?)", (f_name, f_lvl))

    # Default Market Rates
    default_rates = {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0}
    for mat, rat in default_rates.items():
        cursor.execute("INSERT OR IGNORE INTO market_rates (material, rate) VALUES (?, ?)", (mat, rat))

    conn.commit()
    conn.close()

init_db()

# DB Helper Functions
def get_user_data(user_key):
    if not user_key: return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_key = ?", (user_key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_market_rates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT material, rate FROM market_rates")
    rows = cursor.fetchall()
    conn.close()
    return {row["material"]: row["rate"] for row in rows}

def get_feature_locks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT feature_name, access_level FROM feature_locks")
    rows = cursor.fetchall()
    conn.close()
    return {row["feature_name"]: row["access_level"] for row in rows}

# Session State & Query Params Initialization (Auto-Login Support)
if "app_user_name" not in st.session_state:
    st.session_state.app_user_name = None

query_params = st.query_params
if st.session_state.app_user_name is None and "saved_uid" in query_params:
    saved_uid = query_params["saved_uid"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_key FROM users WHERE uid = ?", (saved_uid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        st.session_state.app_user_name = row["user_key"]

if "is_admin_logged" not in st.session_state:
    st.session_state.is_admin_logged = False
if "admin_dashboard_tab" not in st.session_state:
    st.session_state.admin_dashboard_tab = "rates"
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "admin_view" not in st.session_state:
    st.session_state.admin_view = "main"
if "admin_selected_user" not in st.session_state:
    st.session_state.admin_selected_user = None

current_user_name = st.session_state.app_user_name

# 🟢 युझर ॲक्टिव्ह असेल तर त्याची वेळ अपडेट करणे (Live Activity Tracker)
if current_user_name:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_active = ? WHERE user_key = ?", (get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), current_user_name))
    conn.commit()
    conn.close()

# ⏳ प्रिमियम स्टेटस व अचूक एक्सपायरी तपासणी
def check_user_premium_status(username):
    if not username: return False, "Free"
    if username.lower() == "kanha" or username == "9999999999":
        return True, "Master Lifetime VIP"
    
    u_info = get_user_data(username)
    if u_info and u_info.get("is_premium") == 1:
        exp_date_str = u_info.get("premium_expiry")
        if exp_date_str:
            try:
                exp_datetime = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d %H:%M:%S")
                now_datetime = get_ist_time()
                
                if now_datetime > exp_datetime:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE user_key = ?", (username,))
                    conn.commit()
                    conn.close()
                    return False, "Expired"
                else:
                    diff = exp_datetime - now_datetime
                    if diff.days > 0:
                        return True, f"{diff.days} Days Left"
                    elif diff.seconds >= 3600:
                        hrs = diff.seconds // 3600
                        return True, f"{hrs} Hours Left"
                    else:
                        mins = max(1, diff.seconds // 60)
                        return True, f"{mins} Mins Left"
            except:
                pass
        return True, "Active"
    return False, "Free"

is_curr_premium, _ = check_user_premium_status(current_user_name)

# ==========================================
# 🎨 ULTRA-PREMIUM ROYAL METALLIC GOLD & EXECUTIVE ADMIN STYLING
# ==========================================
touch_glow_color = "rgba(255, 179, 0, 0.45)" if is_curr_premium else "rgba(59, 130, 246, 0.25)"
touch_border_color = "#FFD54F" if is_curr_premium else "#3b82f6"
card_border_color = "rgba(255, 179, 0, 0.45)" if is_curr_premium else "rgba(59, 130, 246, 0.25)"
input_inner_shadow = "inset 0 0 10px rgba(255, 179, 0, 0.3)" if is_curr_premium else "inset 0 2px 4px rgba(0, 0, 0, 0.4)"

st.markdown(f"""
    <style>
    #MainMenu {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ visibility: hidden; height: 0%; display: none !important; }}
    footer {{ visibility: hidden; display: none !important; }}
    .stAppHeader {{ display: none !important; }}
    [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ visibility: hidden !important; }}
    
    button[title="Increment"], button[title="Decrement"] {{ display: none !important; }}
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {{ display: none !important; }}

    .stApp {{
        background: linear-gradient(135deg, #070a12 0%, #0d1322 100%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp:active {{
        box-shadow: inset 0 0 80px {touch_glow_color} !important;
    }}

    .stMarkdown table {{
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        width: 100%;
        border-collapse: collapse;
    }}
    .stMarkdown th, .stMarkdown td {{
        padding: 10px 14px !important;
        border: 1px solid #374151 !important;
    }}

    div.stForm, div[data-testid="stExpander"] {{
        background: rgba(17, 24, 39, 0.8) !important;
        backdrop-filter: blur(16px);
        border: 1px solid {card_border_color} !important;
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), {input_inner_shadow};
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    input, select, textarea {{
        border-color: {touch_border_color} !important;
        border-radius: 14px !important;
        background-color: #121929 !important;
        color: #ffffff !important;
        outline: none !important;
        font-weight: 500 !important;
        box-shadow: {input_inner_shadow} !important;
        transition: all 0.25s ease-in-out !important;
    }}

    div[data-baseweb="select"]:focus-within > div,
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="base-input"]:focus-within,
    input:focus, select:focus, textarea:focus {{
        border-color: {touch_border_color} !important;
        background-color: #1a233a !important;
        box-shadow: 0 0 18px {touch_glow_color}, {input_inner_shadow} !important;
    }}

    label, div[data-testid="stWidgetLabel"] p {{
        color: #9ca3af !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
        width: 100%;
    }}

    .main-header {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 22px 15px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.35);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}

    .gold-vip-badge {{
        background: linear-gradient(135deg, #FFE082 0%, #FFB300 50%, #FF6F00 100%);
        color: #000000;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 14px;
        letter-spacing: 0.5px;
        box-shadow: 0 0 20px rgba(255, 179, 0, 0.7);
        display: inline-block;
        border: 1px solid #FFF59D;
    }}

    .free-user-badge {{
        background: rgba(31, 41, 55, 0.9);
        color: #9ca3af;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        border: 1px solid #374151;
        display: inline-block;
    }}

    /* 👑 ॲडमीन स्पेशल रॉयल एक्झिक्युटिव्ह ऑफिस थीम */
    .admin-command-center {{
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        border: 2px solid #FFD54F !important;
        border-radius: 24px !important;
        padding: 25px !important;
        box-shadow: 0 15px 40px rgba(255, 179, 0, 0.25), inset 0 0 20px rgba(255, 179, 0, 0.15);
        margin-bottom: 25px;
    }}

    .admin-user-card {{
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #FFB300;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }}

    @media print {{
        @page {{ size: A3 landscape; margin: 10mm; }}
        body * {{ visibility: hidden; }}
        .print-container, .print-container * {{ visibility: visible; }}
        .print-container {{ position: absolute; left: 0; top: 0; width: 100%; background: white !important; color: black !important; padding: 15px; }}
    }}
    </style>
""", unsafe_allow_html=True)

# 🔑 रँडम ५ अक्षरी युनिक कोड जनरेटर
def generate_random_code():
    return "PATIL-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# ==========================================
# 🔐 ॲप व्हॉट्सॲप फीचर अनलॉक/प्रीमियम फंक्शन
# ==========================================
def render_whatsapp_feature(encoded_msg, key_prefix):
    is_prem, status_str = check_user_premium_status(current_user_name)
    locks_cfg = get_feature_locks()
    wa_lock_setting = locks_cfg.get("WhatsApp Share", "Premium")

    if wa_lock_setting == "Free" or is_prem:
        st.markdown(f'''
            <a href="https://wa.me/?text={encoded_msg}" target="_blank">
                <button style="width: 100%; background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px;">
                    📱 Share Full Report on WhatsApp {'(🆓 Free Access)' if wa_lock_setting == 'Free' else '(👑 VIP Premium Active)'}
                </button>
            </a>
        ''', unsafe_allow_html=True)
    else:
        with st.expander("🔒 WhatsApp Report Sharing - Unlock Premium"):
            st.warning("⚠️ व्हॉट्सॲपवर पूर्ण रिपोर्ट शेअर करण्याचे फीचर प्रिमियम युझर्ससाठी आहे.")
            st.caption("💡 अनलॉक करण्यासाठी Admin कडून आलेला प्रिमियम कोड खाली टाका:")
            
            p_code = st.text_input("Enter Activation Code:", key=f"{key_prefix}_code_input").strip()
            
            w_col1, w_col2 = st.columns(2)
            with w_col1:
                if st.button("🔓 Unlock WhatsApp Share Now", key=f"{key_prefix}_unlock_btn"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM premium_codes WHERE code = ?", (p_code,))
                    row = cursor.fetchone()
                    
                    if row:
                        c_info = dict(row)
                        if c_info.get("used") == 1:
                            st.error("❌ हा कोड आधीच वापरला गेला आहे! तो आता व्हॅलिड नाही.")
                            conn.close()
                        else:
                            exp_datetime = get_ist_time() + datetime.timedelta(days=28)
                            exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                            cursor.execute("UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?", (current_user_name, now_str, p_code))
                            
                            disp_name = current_user_name if current_user_name else ""
                            welcome_msg = f"{disp_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                            
                            cursor.execute('''
                                UPDATE users 
                                SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?, admin_message = ?, unread_notification = 0
                                WHERE user_key = ?
                            ''', (exp_str, "Kanhaiya (Founder of Patil Infratech)", welcome_msg, current_user_name))
                            
                            conn.commit()
                            conn.close()
                            st.rerun()
                    else:
                        conn.close()
                        st.error("❌ चुकीचा प्रिमियम कोड! कृपया अचूक कोड टाका.")

            with w_col2:
                if st.button("📩 Request Code from Admin", key=f"{key_prefix}_req_btn"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET requested_code = 1 WHERE user_key = ?", (current_user_name,))
                    conn.commit()
                    conn.close()
                    st.success("✅ ॲडमीनला कोडसाठी रिक्वेस्ट पाठवली आहे!")

# ==========================================
# --- १. वेलकम स्क्रीन ॲनिमेशन (Loading Page with Title Sponsor) ---
# ==========================================
welcome_placeholder = st.empty()

if 'welcome_completed' not in st.session_state:
    st.session_state.welcome_completed = False

if not st.session_state.welcome_completed:
    with welcome_placeholder.container():
        st.markdown("""
            <style>
            div.stButton > button {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: transparent !important; border: none !important;
                color: transparent !important; z-index: 99999; cursor: pointer;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("Skip Welcome", key="invisible_skip_btn"):
            st.session_state.welcome_completed = True
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #60a5fa;'>🏗️ WELCOME TO PATIL INFRATECH...</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #9ca3af;'>तुमचे स्वप्न, आमचे एस्टिमेशन!</h3>", unsafe_allow_html=True)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads WHERE active = 1 AND position = 'Loading Page (Title Sponsor)'")
        ads_rows = cursor.fetchall()
        conn.close()

        for ad in ads_rows:
            ad_dict = dict(ad)
            st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); padding: 6px 10px; border-radius: 10px; text-align: center; margin: 15px auto; max-width: 280px;">
                    <span style="font-size: 9px; color: #93c5fd; font-weight: bold;">⭐ SPONSOR</span><br>
                    <b style="color: #ffffff; font-size: 12px;">{ad_dict.get('title')}</b>
                    <p style="color: #9ca3af; font-size: 10px; margin: 2px 0;">{ad_dict.get('desc')}</p>
                    {"<img src='" + ad_dict.get('media_url') + "' style='max-height:50px; border-radius:6px; margin-top:3px;'/>" if ad_dict.get('media_type') == 'Photo (PNG/JPG)' and ad_dict.get('media_url') else ""}
                    <br><a href="{ad_dict.get('link')}" target="_blank" style="color: #fbbf24; font-weight: bold; text-decoration: underline; font-size: 11px;">👉 Visit Link</a>
                </div>
            """, unsafe_allow_html=True)

        st.caption("<p style='text-align: center; color: #6b7280;'>(पुढे जाण्यासाठी स्क्रीनवर कुठेही टच करा)</p>", unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        construction_stages = [
            "🧱 पाया खोदण्याचे काम सुरू आहे...",
            "🏗️ खांब आणि कॉलम उभे राहत आहेत...",
            "🧱 विटांचे बांधकाम (Brickwork) प्रगतीपथावर आहे...",
            "🏠 छताचे (Slab) काम पूर्ण होत आहे...",
            "✨ फिनिशिंग आणि रंगकाम पूर्ण झाले! घर तयार आहे! 🎉"
        ]
        
        for i in range(5):
            status_text.markdown(f"<p style='text-align: center; font-size: 18px; font-weight: bold; color: #f3f4f6;'>{construction_stages[i]}</p>", unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.5)

    welcome_placeholder.empty()
    st.session_state.welcome_completed = True

# मुख्य टायटल बॅनर
st.markdown("""
    <div class="main-header">
        <h1 style='color: white; margin:0; font-size: 26px;'>🏗️ PATIL INFRATECH</h1>
        <p style='color: #e0e7ff; margin:5px 0 0 0; font-size: 14px;'>📐 Quantity Surveyor & Cost Estimator</p>
        <small style='color: #93c5fd;'>Concept & Logic by: Kanhaiya (Founder of Patil Infratech)</small>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 🛡️ ADMIN PANEL (👑 ROYAL CEO COMMAND CENTER VIBE)
# ==========================================
if st.session_state.is_admin_logged:
    st.markdown("""
        <div class="admin-command-center">
            <h1 style='color: #FFD54F; margin:0; font-size: 28px; text-align: center;'>⚡ KANHAIYA'S EXECUTIVE COMMAND CENTER</h1>
            <p style='color: #cbd5e1; margin:5px 0 0 0; font-size: 14px; text-align: center;'>👑 Patil Infratech Master Control & Management Hub</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_logout, _ = st.columns([1, 3])
    with col_logout:
        if st.button("🔒 Admin Logout"):
            st.session_state.is_admin_logged = False
            st.rerun()

    st.write("---")
    
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        if st.button("📈 Update Market Rates", use_container_width=True):
            st.session_state.admin_dashboard_tab = "rates"
    with ac2:
        if st.button("⚙️ Feature Lock Manager", use_container_width=True):
            st.session_state.admin_dashboard_tab = "locks"
    with ac3:
        if st.button("👥 User Data", use_container_width=True):
            st.session_state.admin_dashboard_tab = "users"
    with ac4:
        if st.button("📢 Ad Sponsor", use_container_width=True):
            st.session_state.admin_dashboard_tab = "ads"

    st.write("---")
    current_tab = st.session_state.admin_dashboard_tab

    if current_tab == "rates":
        st.markdown("### 📈 Update Master Market Rates")
        m_rates = get_market_rates()
        
        adm_cem = st.number_input("Cement (per bag ₹):", min_value=0.0, value=float(m_rates.get("cement", 400.0)), step=1.0)
        adm_snd = st.number_input("Sand (per m³ ₹):", min_value=0.0, value=float(m_rates.get("sand", 2500.0)), step=1.0)
        adm_brk = st.number_input("Brick (per nos ₹):", min_value=0.0, value=float(m_rates.get("bricks", 8.0)), step=0.1)
        adm_agg = st.number_input("Aggregate (per m³ ₹):", min_value=0.0, value=float(m_rates.get("aggregate", 2200.0)), step=1.0)
        adm_ste = st.number_input("Steel Rate (per kg ₹):", min_value=0.0, value=float(m_rates.get("steel", 60.0)), step=1.0)
        
        if st.button("💾 Save Master Market Rates", type="primary"):
            conn = get_db_connection()
            cursor = conn.cursor()
            updated_rates = {"cement": adm_cem, "sand": adm_snd, "bricks": adm_brk, "aggregate": adm_agg, "steel": adm_ste}
            for mat, rat in updated_rates.items():
                cursor.execute("REPLACE INTO market_rates (material, rate) VALUES (?, ?)", (mat, rat))
            conn.commit()
            conn.close()
            st.success("✅ आजचे मास्टर मार्केट दर डेटाबेसमध्ये यशस्वीरित्या अपडेट झाले!")

    elif current_tab == "locks":
        st.markdown("### ⚙️ Feature Lock Manager")
        cur_locks = get_feature_locks()

        fl_calc = st.selectbox("Civil Calculator Access:", ["Free", "Premium"], index=0 if cur_locks.get("Civil Calculator", "Free") == "Free" else 1)
        fl_ra = st.selectbox("Rate Analysis Module Access:", ["Free", "Premium"], index=0 if cur_locks.get("Rate Analysis", "Free") == "Free" else 1)
        fl_bbs = st.selectbox("BBS Calculator Access:", ["Free", "Premium"], index=0 if cur_locks.get("BBS", "Free") == "Free" else 1)
        fl_wa = st.selectbox("WhatsApp Full Report Share:", ["Free", "Premium"], index=0 if cur_locks.get("WhatsApp Share", "Free") == "Free" else 1)
        fl_ai = st.selectbox("Civil AI Assistant Access:", ["Free", "Premium"], index=0 if cur_locks.get("Civil AI Assistant", "Premium") == "Free" else 1)

        if st.button("💾 Save Feature Lock Settings", type="primary"):
            conn = get_db_connection()
            cursor = conn.cursor()
            new_locks = {
                "Civil Calculator": fl_calc,
                "Rate Analysis": fl_ra,
                "BBS": fl_bbs,
                "WhatsApp Share": fl_wa,
                "Civil AI Assistant": fl_ai
            }
            for f_name, f_lvl in new_locks.items():
                cursor.execute("REPLACE INTO feature_locks (feature_name, access_level) VALUES (?, ?)", (f_name, f_lvl))
            conn.commit()
            conn.close()
            st.success("✅ प्रिमियम/फ्री फीचर्स सेटिंग्स यशस्वीरित्या बदलल्या!")

    elif current_tab == "users":
        st.markdown("### 📋 User Database Master List")
        
        if st.session_state.admin_view == "user_detail" and st.session_state.admin_selected_user is not None:
            target_user = st.session_state.admin_selected_user
            if st.button("⬅️ Back to All Users List"):
                st.session_state.admin_view = "main"
                st.session_state.admin_selected_user = None
                st.rerun()

            info = get_user_data(target_user) or {}
            
            u_name = info.get("id", target_user)
            u_uid = info.get("uid", "N/A")
            u_mob = info.get("mobile", "N/A")
            u_pin = info.get("pin", "N/A")
            u_comm = info.get("comment", "काही नाही")
            u_prem = bool(info.get("is_premium", 0))
            exp_date = info.get("premium_expiry", "N/A")
            is_req = bool(info.get("requested_code", 0))
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history WHERE user_key = ? ORDER BY id DESC", (target_user,))
            u_hist = [dict(r) for r in cursor.fetchall()]

            cursor.execute("SELECT code FROM premium_codes WHERE assigned_to = ? AND used = 0", (u_name,))
            c_row = cursor.fetchone()
            conn.close()
            assigned_code = c_row["code"] if c_row else None

            status_badge = f"👑 VIP MEMBER: {u_name.upper()}" if u_prem else ("🚨 CODE REQUESTED!" if is_req else f"🆓 FREE: {u_name.upper()}")

            st.markdown(f"#### 👤 MANAGE USER: <span style='color:#60a5fa;'>{u_name.upper()}</span>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="admin-user-card">
                    <p style="margin:5px 0; font-size:16px;"><b>माहिती/स्टेटस:</b> <span class="gold-vip-badge">{status_badge}</span></p>
                    <p style="margin:5px 0; font-size:15px;"><b>UID:</b> <code style="color:#60a5fa; font-size:15px;">{u_uid}</code> | <b>Mobile:</b> <code>{u_mob}</code> | <b>PIN:</b> <code style="color:#f59e0b; font-size:15px;">{u_pin}</code></p>
                    <p style="margin:8px 0 5px 0; font-size:15px;"><b>प्रिमियम मुदत (Expiry):</b> <code>{exp_date}</code></p>
                    <p style="margin:5px 0; font-size:15px;"><b>ॲक्टिव्ह कोड (Unused):</b> <code style="color:#10b981; font-size:16px;">{assigned_code if assigned_code else 'काही नाही'}</code></p>
                    <p style="margin:5px 0; font-size:14px; color:#9ca3af;"><b>युझर कमेंट:</b> {u_comm}</p>
                </div>
            """, unsafe_allow_html=True)

            if assigned_code:
                st.info(f"💡 {u_name} साठी आधीच एक कोड तयार आहे: `{assigned_code}`")
            else:
                if st.button(f"🚀 Generate & Send Unique Code to {u_name}", key=f"win_gen_send_{target_user}"):
                    new_c = generate_random_code()
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO premium_codes (code, assigned_to, used, created_at) VALUES (?, ?, 0, ?)", (new_c, u_name, now_str))
                    msg = f"तुमचा प्रिमियम कोड: {new_c} (ॲपमध्ये टाकून प्रिमियम अनलॉक करा)"
                    cursor.execute("UPDATE users SET admin_message = ?, requested_code = 0 WHERE user_key = ?", (msg, target_user))
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 {u_name} ला ऑटोमॅटिकली कोड पाठवला: `{new_c}`")
                    st.rerun()

            st.markdown("---")
            st.markdown("##### ⏱️ प्रिमियम वेळ सेट करा / वाढवा (Custom Expiry):")
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                time_val = st.number_input("संख्या (Value):", min_value=1, value=28, key=f"win_t_val_{target_user}")
            with t_col2:
                time_unit = st.selectbox("युनिट (Unit):", ["Minutes", "Hours", "Days"], index=2, key=f"win_t_unit_{target_user}")

            if st.button(f"⚡ Set Premium Time ({time_val} {time_unit})", key=f"win_btn_custom_{target_user}"):
                now = get_ist_time()
                if time_unit == "Minutes":
                    exp_time = now + datetime.timedelta(minutes=time_val)
                elif time_unit == "Hours":
                    exp_time = now + datetime.timedelta(hours=time_val)
                else:
                    exp_time = now + datetime.timedelta(days=time_val)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET is_premium = 1, premium_expiry = ?, requested_code = 0, seen_popup = 0, activated_by = ?
                    WHERE user_key = ?
                ''', (exp_time.strftime("%Y-%m-%d %H:%M:%S"), "Kanhaiya (Founder of Patil Infratech)", target_user))
                conn.commit()
                conn.close()
                st.success(f"✅ {u_name} साठी {time_val} {time_unit} सेव्ह केले!")
                st.rerun()

            if u_prem:
                if st.button(f"🔻 Revoke Premium: {u_name}", key=f"win_rev_{target_user}"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE user_key = ?", (target_user,))
                    conn.commit()
                    conn.close()
                    st.warning(f"❌ {u_name} चे प्रिमियम काढले आहे.")
                    st.rerun()

            st.markdown("---")
            current_msg = info.get("admin_message", "Admin message...")
            new_msg = st.text_input(f"✍️ {u_name} साठी इनबॉक्स मेसेज बदलणे (Notification Send):", value=current_msg, key=f"win_msg_{target_user}")
            if st.button(f"✉️ मेसेज सेव्ह करा व पाठवा ({u_name})", key=f"win_btn_msg_{target_user}"):
                if new_msg.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET admin_message = ?, unread_notification = 1 WHERE user_key = ?", (new_msg.strip(), target_user))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ '{u_name}' च्या इनबॉक्समध्ये नवीन मेसेज पाठवला (Notification Sent)!")
                    st.rerun()

            if st.button(f"🗑️ Delete User: {u_name}", key=f"win_del_{target_user}"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_key = ?", (target_user,))
                cursor.execute("DELETE FROM history WHERE user_key = ?", (target_user,))
                conn.commit()
                conn.close()
                st.session_state.admin_view = "main"
                st.session_state.admin_selected_user = None
                st.error(f"❌ युझर '{u_name}' डिलीट केला आहे!")
                st.rerun()
            
            st.markdown("---")
            st.markdown(f"##### 📜 {u_name} चे जनरेट केलेले एस्टिमेशन रिपोर्ट्स ({len(u_hist)})")
            if u_hist:
                for idx, hist in enumerate(u_hist, 1):
                    ts = hist.get('timestamp', 'N/A')
                    with st.expander(f"🗓️ रिपोर्ट #{idx} | तारीख व वेळ: `{ts}`"):
                        st.markdown(hist.get("report_data", "डेटा उपलब्ध नाही"))
            else:
                st.info("ℹ️ या युझरने अजून एकही रिपोर्ट जनरेट केलेला नाही.")
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_key != '9999999999' ORDER BY id ASC")
            all_users = [dict(r) for r in cursor.fetchall()]
            conn.close()

            if all_users:
                now_time = get_ist_time()
                for info in all_users:
                    mob = info.get("user_key")
                    u_name = info.get("id", mob)
                    u_uid = info.get("uid", "N/A")
                    u_prem = bool(info.get("is_premium", 0))
                    is_req = bool(info.get("requested_code", 0))
                    last_active_str = info.get("last_active", None)

                    is_online = False
                    if last_active_str:
                        try:
                            last_active_dt = datetime.datetime.strptime(last_active_str, "%Y-%m-%d %H:%M:%S")
                            diff_seconds = (now_time - last_active_dt).total_seconds()
                            if diff_seconds <= 120:
                                is_online = True
                        except:
                            pass

                    status_indicator = "🟢 Active (Online)" if is_online else "🔴 Inactive (Offline)"

                    col_u1, col_u2 = st.columns([3.2, 1.8])
                    if u_prem:
                        col_u1.markdown(f"<span class='gold-vip-badge'>👑 VIP: {u_name.upper()}</span> (UID: <code>{u_uid}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)
                    elif is_req:
                        col_u1.markdown(f"#### 👤 **{u_name}** `[🚨 CODE]` (UID: `{u_uid}`)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)
                    else:
                        col_u1.markdown(f"<span class='free-user-badge'>🆓 FREE: {u_name.upper()}</span> (UID: <code>{u_uid}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)

                    if col_u2.button(f"👁️ View / Manage", key=f"open_user_win_{mob}"):
                        st.session_state.admin_view = "user_detail"
                        st.session_state.admin_selected_user = mob
                        st.rerun()
                    st.write("---")
            else:
                st.info("ℹ️ डेटाबेसमध्ये सध्या कोणताही सामान्य युझर नाही.")

    elif current_tab == "ads":
        st.markdown("### 📢 Ad & Sponsor Manager")
        st.caption("💡 इथून तू दोन प्रकारचे स्पॉन्सरशिप्स (Ads) मॅनेज करू शकतोस:")

        with st.form("add_ad_form"):
            ad_title = st.text_input("Sponsor / Ad Title:")
            ad_desc = st.text_area("Offer / Description:")
            ad_link = st.text_input("Target Link (URL or WhatsApp link):")
            media_type = st.selectbox("Media Type:", ["Photo (PNG/JPG)", "Video Ad"])
            media_url = st.text_input("Media Direct URL (Image/Video Link):")
            position = st.selectbox("Display Position:", [
                "Loading Page (Title Sponsor)", 
                "Main App Header (Top Banner)"
            ])
            is_active = st.checkbox("Make Active / Live", value=True)
            
            submit_ad = st.form_submit_button("🚀 Publish Ad Sponsor", type="primary")
            if submit_ad:
                if ad_title.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute('''
                        INSERT INTO ads (title, desc, link, media_type, media_url, position, active, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (ad_title.strip(), ad_desc.strip(), ad_link.strip(), media_type, media_url.strip(), position, 1 if is_active else 0, now_str))
                    conn.commit()
                    conn.close()
                    st.success("✅ स्पॉन्सर ॲड यशस्वीरित्या पब्लिश झाली!")
                    st.rerun()
                else:
                    st.warning("⚠️ कृपया ॲडचे नाव टाका!")

        st.markdown("---")
        st.markdown("##### 📋 सध्या चालू असलेल्या जाहिराती (Active Ads List):")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads ORDER BY id DESC")
        ads_list = [dict(r) for r in cursor.fetchall()]
        conn.close()

        if ads_list:
            for ad in ads_list:
                ad_id = ad.get("id")
                st.info(f"**#{ad_id} | {ad.get('title')}** ({ad.get('position')})\n- *Status:* {'🟢 Active' if ad.get('active')==1 else '🔴 Inactive'}")
                if st.button(f"🗑️ Delete Ad #{ad_id}", key=f"del_ad_{ad_id}"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
                    conn.commit()
                    conn.close()
                    st.success("🗑️ ॲड डिलीट केली!")
                    st.rerun()
        else:
            st.info("ℹ️ सध्या कोणतीही ॲड किंवा स्पॉन्सरशिप उपलब्ध नाही.")

    st.stop()

# ==========================================
# 👤 UID & PIN SECURE LOGIN / SIGNUP SYSTEM (With Auto-Login / Remember Me)
# ==========================================
if st.session_state.app_user_name is None:
    st.markdown("### 🏗️ PATIL INFRATECH - SECURE LOGIN")
    
    auth_mode = st.radio("निवडा (Select Option):", ["🔑 UID Login (लॉगिन करा)", "✨ Register (नवीन अकाउंट)", "❓ Forgot UID/PIN (आयडी/पिन रिकव्हर करा)"], horizontal=True)

    if "Login" in auth_mode:
        with st.form("uid_login_form"):
            input_uid = st.text_input("Enter your UID:").strip().upper()
            remember_me = st.checkbox("📌 या डिव्हाइसवर अकाउंट सेव्ह ठेवा (Remember Me)", value=False)
            submit_login = st.form_submit_button("🚀 Login Now", type="primary")

            if submit_login:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT user_key FROM users WHERE uid = ?", (input_uid,))
                row = cursor.fetchone()
                conn.close()

                if row:
                    found_user = row["user_key"]
                    st.session_state.app_user_name = found_user
                    if remember_me:
                        st.query_params["saved_uid"] = input_uid
                    st.success("🎉 यशस्वीरित्या लॉगिन झाले!")
                    st.rerun()
                else:
                    st.error("❌ चुकीचा UID! कृपया बरोबर UID टाका.")

    elif "Register" in auth_mode:
        with st.form("uid_reg_form"):
            reg_name = st.text_input("नाव (Name):", placeholder="नाव टाका").strip()
            reg_mob = st.text_input("मोबाईल नंबर (Mobile Number):", placeholder="१० अंकी नंबर").strip()
            reg_pin = st.text_input("4-Digit सिक्रेट पिन सेट करा (Set PIN):", type="password", max_chars=4, placeholder="1234").strip()
            remember_me_reg = st.checkbox("📌 या डिव्हाइसवर अकाउंट सेव्ह ठेवा (Remember Me)", value=False, key="reg_rem")
            submit_reg = st.form_submit_button("✨ Create Account & Get UID", type="primary")

            if submit_reg:
                if reg_name and len(reg_mob) >= 10 and len(reg_pin) == 4:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT user_key FROM users WHERE mobile = ?", (reg_mob,))
                    mob_exists = cursor.fetchone()

                    if mob_exists:
                        conn.close()
                        st.error("❌ या मोबाईल नंबरवर आधीच अकाउंट तयार आहे!")
                    else:
                        first_name = reg_name.split()[0].upper()
                        last_4_mob = reg_mob[-4:]
                        generated_uid = f"{first_name}{last_4_mob}"

                        cursor.execute("SELECT user_key FROM users WHERE uid = ?", (generated_uid,))
                        if cursor.fetchone():
                            generated_uid = f"{first_name}{random.randint(1000, 9999)}"

                        cursor.execute("SELECT user_key FROM users WHERE user_key = ?", (reg_name,))
                        if not cursor.fetchone():
                            new_welcome_msg = f"{reg_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                            
                            cursor.execute('''
                                INSERT INTO users (user_key, id, uid, pin, mobile, password, comment, admin_message, unread_notification, is_premium, premium_expiry, requested_code, seen_popup, master_code_uses, last_active, activated_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, NULL, 0, 0, 0, ?, ?)
                            ''', (reg_name, reg_name, generated_uid, reg_pin, reg_mob, "user123", "काही नाही", new_welcome_msg, now_str, "Free User"))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success(f"🎉 अकाउंट यशस्वीरित्या तयार झाले! तुमचा युनिक UID हा आहे: **{generated_uid} and pin {reg_pin}**")
                            st.info("💡 कृपया हा UID लक्षात ठेवा आणि वर 'UID Login' वर क्लिक करून लॉगिन करा!")
                            st.stop()
                        else:
                            conn.close()
                            st.error("❌ या नावाने आधीच अकाउंट आहे! कृपया दुसरे नाव वापरून रजिस्टर करा.")
                else:
                    st.warning("⚠️ कृपया नाव, १० अंकी मोबाईल नंबर आणि अचूक ४ अंकी पिन (PIN) टाकल्याची खात्री करा!")

    else:
        with st.form("forgot_uid_form"):
            forgot_mob = st.text_input("नोंदणीकृत मोबाईल नंबर (Registered Mobile):").strip()
            forgot_pin = st.text_input("तुमचा 4-Digit सिक्रेट पिन (Secret PIN):", type="password", max_chars=4).strip()
            submit_forgot = st.form_submit_button("🔍 Recover My UID", type="primary")

            if submit_forgot:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id, uid FROM users WHERE mobile = ? AND pin = ?", (forgot_mob, forgot_pin))
                matched_users = cursor.fetchall()
                conn.close()

                if matched_users:
                    st.success("✅ तुमचे अकाउंट तपशील सापडले आहेत:")
                    for row in matched_users:
                        st.info(f"👤 नाव: **{row['id']}** | 🔑 UID: **{row['uid']}** (आता या UID ने लॉगिन करा)")
                else:
                    st.error("❌ चुकीचा मोबाईल नंबर किंवा PIN! तपशील जुळत नाहीत.")

    st.write("---")
    
    with st.expander("🛡️ Admin Login Panel"):
        with st.form("admin_login_form"):
            admin_id = st.text_input("Admin ID:")
            admin_pass = st.text_input("Password:", type="password")
            submit_admin = st.form_submit_button("🔓 Login to Admin Panel", type="primary")
            
            secret_admin_id = st.secrets.get("ADMIN_ID", "kanha_1p") if hasattr(st, "secrets") else "kanha_1p"
            secret_admin_pass = st.secrets.get("ADMIN_PASS", "@Dellg15") if hasattr(st, "secrets") else "@Dellg15"

            if submit_admin:
                if admin_id == secret_admin_id and admin_pass == secret_admin_pass:
                    st.session_state.is_admin_logged = True
                    st.rerun()
                else:
                    st.error("❌ चुकीचा Admin ID किंवा Password!")
            
    st.stop()

# ==========================================
# 🚀 MAIN DASHBOARD (USER LOGGED IN)
# ==========================================
current_user_name = st.session_state.app_user_name

is_user_premium, status_text_str = check_user_premium_status(current_user_name)

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM ads WHERE active = 1 AND position = 'Main App Header (Top Banner)'")
ads_list = [dict(r) for r in cursor.fetchall()]
conn.close()

for ad in ads_list:
    st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); padding: 6px 10px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
            <span style="font-size: 9px; color: #93c5fd; font-weight: bold;">📢 SPONSOR AD</span><br>
            <b style="color: #fff; font-size: 12px;">{ad.get('title')}</b> — <span style="color: #cbd5e1; font-size: 11px;">{ad.get('desc')}</span>
            {"<img src='" + ad.get('media_url') + "' style='max-height:50px; border-radius:6px; margin-top:3px;'/>" if ad.get('media_type') == 'Photo (PNG/JPG)' and ad.get('media_url') else ""}
            <a href="{ad.get('link')}" target="_blank" style="color: #fbbf24; font-weight: bold; text-decoration: underline; font-size: 11px; margin-left: 6px;">[Visit]</a>
        </div>
    """, unsafe_allow_html=True)

col_u, col_lo = st.columns([3.5, 1.5])
if is_user_premium:
    col_u.markdown(f"<span class='gold-vip-badge'>👑 VIP MEMBER: {current_user_name.upper()} ({status_text_str})</span>", unsafe_allow_html=True)
else:
    col_u.markdown(f"<span class='free-user-badge'>🆓 FREE USER: {current_user_name.upper()}</span>", unsafe_allow_html=True)

if col_lo.button("🔄 Logout / ॲप बदला"):
    st.session_state.app_user_name = None
    if "saved_uid" in st.query_params:
        del st.query_params["saved_uid"]
    st.session_state.current_comment = "काही नाही"
    st.session_state.selected_module = None
    st.rerun()

current_user_data = get_user_data(current_user_name) or {}
disp_name_inbox = current_user_name if current_user_name else ""

if current_user_data.get("unread_notification") == 1:
    admin_msg = current_user_data.get("admin_message", "")
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #047857 0%, #065f46 100%); padding: 16px 20px; border-radius: 16px; margin-bottom: 15px; border: 1px solid #34d399; box-shadow: 0 4px 20px rgba(52, 211, 153, 0.3);">
            <h4 style="color: #6ee7b7; margin: 0 0 5px 0;">🔔 नवीन नोटिफिकेशन</h4>
            <p style="color: #ffffff; font-size: 16px; margin: 0;">{admin_msg}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ Mark as Read & Clear (वाचले आहे)", type="primary"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET unread_notification = 0, admin_message = ? WHERE user_key = ?", (f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳", current_user_name))
        conn.commit()
        conn.close()
        st.success("✅ मेसेज वाचून क्लियर केला आहे!")
        st.rerun()
else:
    admin_msg = current_user_data.get("admin_message", f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳")
    st.markdown("### 📥 Admin Message / Code Inbox")
    st.info(f"📢 **Admin:** {admin_msg}")

st.write("---")

if not is_user_premium:
    with st.expander("🔑 प्रिमियम अनलॉक करा (Enter Premium Code)"):
        input_code = st.text_input("Enter Code (e.g. PATIL-XXXXX):", key="home_code_input").strip()
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔓 Activate Premium", type="primary"):
                u_info = get_user_data(current_user_name) or {}
                
                if input_code == "4528":
                    uses_count = u_info.get("master_code_uses", 0)
                    if uses_count >= 3:
                        st.error("❌ हा मास्टर कोड तुम्ही आधीच ३ वेळा वापरला आहे! मर्यादा संपली आहे.")
                    else:
                        exp_datetime = get_ist_time() + datetime.timedelta(hours=8)
                        exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE users 
                            SET master_code_uses = ?, is_premium = 1, premium_expiry = ?, seen_popup = 0,
                                activated_by = ?, admin_message = ?, unread_notification = 0
                            WHERE user_key = ?
                        ''', (uses_count + 1, exp_str, "Master Code 4528 (8 Hours VIP)", f"🎉 मास्टर कोड 4528 द्वारे तुला ८ तासांचे प्रिमियम मिळाले आहे! (वापर: {uses_count + 1}/3)", current_user_name))
                        conn.commit()
                        conn.close()
                        
                        st.success("🎉 मास्टर कोड द्वारे ८ तासांचे प्रिमियम अनलॉक झाले!")
                        st.rerun()

                elif input_code == "kanha_1p":
                    exp_datetime = get_ist_time() + datetime.timedelta(days=1)
                    exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users 
                        SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?,
                            admin_message = ?, unread_notification = 0
                        WHERE user_key = ?
                    ''', (exp_str, "Master Code", f"{current_user_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳", current_user_name))
                    conn.commit()
                    conn.close()
                    
                    st.success("🎉 मास्टर कोडद्वारे प्रिमियम यशस्वीरित्या सुरू झाले!")
                    st.rerun()
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM premium_codes WHERE code = ?", (input_code,))
                    c_row = cursor.fetchone()
                    
                    if c_row and dict(c_row).get("used") == 0:
                        exp_datetime = get_ist_time() + datetime.timedelta(days=28)
                        exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                        cursor.execute("UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?", (current_user_name, now_str, input_code))
                        cursor.execute('''
                            UPDATE users 
                            SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?,
                                admin_message = ?, unread_notification = 0
                            WHERE user_key = ?
                        ''', (exp_str, "Patil Infratech", f"{current_user_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳", current_user_name))
                        conn.commit()
                        conn.close()
                        st.success("🎉 प्रिमियम यशस्वीरित्या सुरू झाले!")
                        st.rerun()
                    else:
                        conn.close()
                        st.error("❌ चुकीचा किंवा आधीच वापरलेला कोड!")
        with c_btn2:
            if st.button("📩 Request Code"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET requested_code = 1 WHERE user_key = ?", (current_user_name,))
                conn.commit()
                conn.close()
                st.success("✅ ॲडमीनला रिक्वेस्ट पाठवली!")

locks_cfg = get_feature_locks()
ai_lock_setting = locks_cfg.get("Civil AI Assistant", "Premium")

if ai_lock_setting == "Free" or is_user_premium:
    with st.expander("🤖 Patil Infratech Civil AI Assistant (Ask Anything)"):
        user_ai_query = st.text_input("तुमचा प्रश्न किंवा शंका इथे लिहा:", placeholder="उदा. dry volume factor for concrete...", key="civil_ai_input")
        if st.button("🚀 Ask Civil AI"):
            if user_ai_query.strip():
                with st.spinner("🤖 Civil AI is analyzing... (कृपया ५ सेकंद वाट पाहा)"):
                    time.sleep(5.0)
                    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                    ai_response_text = ""
                    if HAS_GENAI and api_key:
                        try:
                            client = genai.Client(api_key=api_key)
                            prompt = f"You are a Senior Civil Engineer for Patil Infratech. Provide a direct, professional, final answer to the user query without showing calculation steps: {user_ai_query}"
                            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                            if response and response.text: ai_response_text = response.text
                        except Exception as e:
                            ai_response_text = f"⚠️ AI Error: {e}"
                    if not ai_response_text or "Error" in ai_response_text:
                        ai_response_text = f"👷‍♂️ **Patil Infratech Expert Engineer Analysis:** Regarding your query *\"{user_ai_query}\"*, please use our Rate Analysis or BBS Calculator modules."
                    
                    st.markdown(f"""
                        <div style="background: rgba(31, 41, 55, 0.95); border-left: 5px solid #FFB300; padding: 15px; border-radius: 12px; margin-top: 10px;">
                            <b>🎯 Civil AI Answer:</b><br><br>{ai_response_text}
                        </div>
                    """, unsafe_allow_html=True)

# ==========================================
# 🎛️ DASHBOARD / MODULE SELECTION SCREEN
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("### 🚀 तुम्हाला काय करायचे आहे ते निवडा:")
    
    calc_lock = locks_cfg.get("Civil Calculator", "Free")
    ra_lock = locks_cfg.get("Rate Analysis", "Free")
    bbs_lock = locks_cfg.get("BBS", "Free")

    col_icon1, col_icon2, col_icon3 = st.columns(3)
    
    with col_icon1:
        calc_badge = "🆓 Free" if calc_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 40px; margin:0;">🧮</h1>
                <h4 style="margin: 8px 0 4px 0; color: #f3f4f6;">Calculator</h4>
                <p style="font-size: 11px; color: #9ca3af;">युनिट कनव्हर्टर [{calc_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🧮 Open Calculator", key="btn_open_calc", use_container_width=True):
            if calc_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
            else:
                st.session_state.selected_module = "Civil Calculator"
                st.rerun()

    with col_icon2:
        ra_badge = "🆓 Free" if ra_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 40px; margin:0;">📊</h1>
                <h4 style="margin: 8px 0 4px 0; color: #f3f4f6;">Rate Analysis</h4>
                <p style="font-size: 11px; color: #9ca3af;">दर विश्लेषण [{ra_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Open Rate Analysis", key="btn_open_ra", use_container_width=True):
            if ra_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
            else:
                st.session_state.selected_module = "Rate Analysis"
                st.rerun()

    with col_icon3:
        bbs_badge = "🆓 Free" if bbs_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 40px; margin:0;">🏗️</h1>
                <h4 style="margin: 8px 0 4px 0; color: #f3f4f6;">BBS</h4>
                <p style="font-size: 11px; color: #9ca3af;">Bar Bending [{bbs_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏗️ Open BBS", key="btn_open_bbs", use_container_width=True):
            if bbs_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
            else:
                st.session_state.selected_module = "BBS"
                st.rerun()

# ==========================================
# 🧮 MODULE 0: CIVIL CALCULATOR & UNIT CONVERTER (Google Style Smart Converter)
# ==========================================
elif st.session_state.selected_module == "Civil Calculator":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_calc"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("🧮 Civil Smart Unit Converter")
    st.caption("💡 एकाच बॉक्समध्ये मूल्य भरा आणि सर्व युनिट्समधील अचूक हिशोब एकाच झटक्यात मिळवा!")

    conv_category = st.selectbox("कनव्हर्शन प्रकार निवडा:", [
        "📦 Volume / Brass Converter (घनफळ आणि ब्रास)", 
        "📏 Length Converter (लांबी मोजमाप)", 
        "📐 Area Converter (क्षेत्रफळ मोजमाप)"
    ])

    if "Volume / Brass" in conv_category:
        st.markdown("#### 📦 Volume & Brass Converter")
        val = st.number_input("मूल्य भरा (Value):", min_value=0.0, value=1.0, step=0.1, key="v_val")
        unit_from = st.selectbox("मूळ युनिट (From Unit):", ["Cubic Meter (m³)", "Cubic Feet (CFT)", "Brass"])

        if st.button("⚡ Convert Now", type="primary", key="btn_conv_vol"):
            if "Cubic Meter" in unit_from:
                m3 = val
            elif "Cubic Feet" in unit_from:
                m3 = val / 35.3147
            else:
                m3 = val * 2.83168

            brass = m3 / 2.83168
            cft = m3 * 35.3147
            liters = m3 * 1000.0

            st.success("✅ कनव्हर्शन निकाल (Results):")
            st.markdown(f"""
                <div style="background: rgba(31, 41, 55, 0.95); padding: 18px; border-radius: 16px; border-left: 5px solid #3b82f6;">
                    <p style="margin: 6px 0; font-size: 16px;"><b>📦 एकूण ब्रास (Brass):</b> <span style="color:#fbbf24; font-size:18px; font-weight:bold;">{brass:.4f} Brass</span></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>📐 घन फूट (Cubic Feet / CFT):</b> <code>{cft:.2f} CFT</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>📏 घन मीटर (Cubic Meter / m³):</b> <code>{m3:.4f} m³</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>💧 लिटर (Liters):</b> <code>{liters:.2f} Ltrs</code></p>
                </div>
            """, unsafe_allow_html=True)

    elif "Length Converter" in conv_category:
        st.markdown("#### 📏 Length Converter")
        val = st.number_input("लांबी भरा (Length Value):", min_value=0.0, value=1.0, step=0.1, key="l_val")
        unit_from = st.selectbox("मूळ युनिट (From Unit):", ["Meters", "Feet", "Inches", "Millimeters (mm)", "Centimeters (cm)"])

        if st.button("⚡ Convert Now", type="primary", key="btn_conv_len"):
            if "Meters" in unit_from:
                meters = val
            elif "Feet" in unit_from:
                meters = val / 3.28084
            elif "Inches" in unit_from:
                meters = val / 39.3701
            elif "Millimeters" in unit_from:
                meters = val / 1000.0
            else:
                meters = val / 100.0

            feet = meters * 3.28084
            inches = meters * 39.3701
            mm = meters * 1000.0
            cm = meters * 100.0

            st.success("✅ कनव्हर्शन निकाल (Results):")
            st.markdown(f"""
                <div style="background: rgba(31, 41, 55, 0.95); padding: 18px; border-radius: 16px; border-left: 5px solid #3b82f6;">
                    <p style="margin: 6px 0; font-size: 15px;"><b>📏 मीटर (Meters):</b> <span style="color:#fbbf24; font-weight:bold;">{meters:.4f} m</span></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>🦶 फूट (Feet):</b> <code>{feet:.4f} ft</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>📐 इंच (Inches):</b> <code>{inches:.2f} inches</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>🔍 मिलिमीटर (mm):</b> <code>{mm:.2f} mm</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>📍 सेंटीमीटर (cm):</b> <code>{cm:.2f} cm</code></p>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("#### 📐 Area Converter")
        val = st.number_input("क्षेत्रफळ भरा (Area Value):", min_value=0.0, value=100.0, step=10.0, key="a_val")
        unit_from = st.selectbox("मूळ युनिट (From Unit):", ["Sq. Meters (m²)", "Sq. Feet (Sq. Ft.)", "Guntha", "Acre"])

        if st.button("⚡ Convert Now", type="primary", key="btn_conv_area"):
            if "Sq. Feet" in unit_from:
                sqft = val
            elif "Sq. Meters" in unit_from:
                sqft = val * 10.7639
            elif "Guntha" in unit_from:
                sqft = val * 1089.0
            else:
                sqft = val * 43560.0

            sqm = sqft / 10.7639
            guntha = sqft / 1089.0
            acre = sqft / 43560.0

            st.success("✅ कनव्हर्शन निकाल (Results):")
            st.markdown(f"""
                <div style="background: rgba(31, 41, 55, 0.95); padding: 18px; border-radius: 16px; border-left: 5px solid #3b82f6;">
                    <p style="margin: 6px 0; font-size: 15px;"><b>📐 स्क्वेअर फूट (Sq. Ft.):</b> <span style="color:#fbbf24; font-weight:bold;">{sqft:.2f} sq.ft.</span></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>📏 स्क्वेअर मीटर (m²):</b> <code>{sqm:.2f} m²</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>🌾 गुंठा (Guntha):</b> <code>{guntha:.4f} Guntha</code></p>
                    <p style="margin: 6px 0; font-size: 15px;"><b>🌳 हेक्टर/एकर (Acre):</b> <code>{acre:.4f} Acre</code></p>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 🛑 MODULE 1: RATE ANALYSIS MODULE (Concrete Work, Brickwork & Plaster Work)
# ==========================================
elif st.session_state.selected_module == "Rate Analysis":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    
    master_rates = get_market_rates()
    st.markdown(
        f"<div style='background: linear-gradient(90deg, #1f2937 0%, #111827 100%); padding: 12px; border-radius: 14px; text-align: center; font-size: 13px; font-weight: bold; color: #f3f4f6; margin-bottom: 15px; border-left: 5px solid #3b82f6; border: 1px solid rgba(255,255,255,0.08);'>"
        f"📢 आजचे मार्केट दर 🏷️ cement: ₹{master_rates.get('cement', 400.0)}/bag | sand: ₹{master_rates.get('sand', 2500.0)}/m³ | aggregate: ₹{master_rates.get('aggregate', 2200.0)}/m³ | steel: ₹{master_rates.get('steel', 60.0)}/Kg | brick: ₹{master_rates.get('bricks', 8.0)}/nos"
        f"</div>", 
        unsafe_allow_html=True
    )

    main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)", "Plaster Work (प्लास्टर काम)"])

    if "Concrete Work" in main_choice:
        st.subheader("🧱 Concrete Work Estimation")
        col1, col2 = st.columns(2)
        with col1:
            grade = st.selectbox("काँक्रीट ग्रेड निवडा:", ["M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"])
        with col2:
            component = st.selectbox("आरसीसी घटक (Component) निवडा:", 
                                     ["Footing (0.8% Steel)", "Slab (1.0% Steel)", "Beam (2.0% Steel)", "Column (2.5% Steel)", "Plain Concrete (0% Steel)"])

        if "M10" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 3, 6
        elif "M15" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 2, 4
        elif "M20" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 1.5, 3
        else: cement_ratio, sand_ratio, aggregate_ratio = 1, 1, 2

        if "Footing" in component: steel_percentage = 0.8
        elif "Slab" in component: steel_percentage = 1.0
        elif "Beam" in component: steel_percentage = 2.0
        elif "Column" in component: steel_percentage = 2.5
        else: steel_percentage = 0.0

        st.markdown("#### [A] साहित्याची माहिती आणि दर (थेट टाईप करा)")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, value=1.0, key="cc_vol")
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="cc_cem_r")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="cc_snd_r")
        with v_col2:
            aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, value=float(master_rates.get("aggregate", 2200.0)), key="cc_agg_r")
            steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, value=float(master_rates.get("steel", 60.0)), key="cc_stl_r") if steel_percentage > 0 else 0.0

        st.markdown("#### [B] लेबर खर्च (नसल्यास ० ठेवा)")
        l_col1, l_col2, l_col3 = st.columns(3)
        with l_col1:
            mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, value=0.0, key="cc_msn_q")
            mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=600.0, key="cc_msn_r")
        with l_col2:
            mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, value=0.0, key="cc_mzd_q")
            mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=400.0, key="cc_mzd_r")
        with l_col3:
            bb_qty = st.number_input("बार बेंडर संख्या:", min_value=0.0, value=0.0, key="cc_bb_q")
            bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=550.0, key="cc_bb_r")

        st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
        o_col1, o_col2 = st.columns(2)
        with o_col1:
            scaffolding_cost = st.number_input("स्कॅफोल्डिंग/सेंटरिंग खर्च (₹):", min_value=0.0, value=0.0, key="cc_scaf")
            contingency_cost = st.number_input("आकस्मिक खर्च (Contingencies) (₹):", min_value=0.0, value=0.0, key="cc_cont")
        with o_col2:
            water_pct = st.number_input("वॉटर charge टक्केवारी (%):", min_value=0.0, value=1.0, key="cc_wat_p")
            profit_pct = st.number_input("कंत्राटदार नफा टक्केवारी (%):", min_value=0.0, value=10.0, key="cc_prof_p")

        st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
        user_note = st.text_area("या एस्टिमेशन संदर्भात काही नोट किंवा कमेंट लिहायची असल्यास इथे लिहा:", placeholder="उदा. ग्राउंड फ्लोअर काम...", key="cc_note")
        if st.button("💬 कमेंट सबमिट करा", key="cc_comm_btn"):
            if user_note.strip():
                st.session_state.current_comment = user_note.strip()
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET comment = ? WHERE user_key = ?", (user_note.strip(), current_user_name))
                conn.commit()
                conn.close()
                st.success("✅ कमेंट सेव्ह झाली!")

        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="cc_report_btn"):
            dry_volume = volume * 1.54
            total_parts = cement_ratio + sand_ratio + aggregate_ratio
            c_bags = math.ceil(((cement_ratio / total_parts) * dry_volume) * 28.8) if total_parts > 0 else 0
            s_m3 = (sand_ratio / total_parts) * dry_volume if total_parts > 0 else 0.0
            a_m3 = (aggregate_ratio / total_parts) * dry_volume if total_parts > 0 else 0.0
            steel_qty = volume * (steel_percentage / 100) * 7850 if steel_percentage > 0 else 0.0

            total_cement_cost = c_bags * cement_rate
            total_sand_cost = s_m3 * sand_rate
            total_aggregate_cost = a_m3 * aggregate_rate
            total_steel_cost = steel_qty * steel_rate

            mat_cost = total_cement_cost + total_aggregate_cost + total_sand_cost + total_steel_cost
            lab_cost = (mason_qty * mason_rate) + (mazdoor_qty * mazdoor_rate) + (bb_qty * bb_rate)
            base_total = mat_cost + lab_cost + scaffolding_cost + contingency_cost
            w_amt = base_total * (water_pct / 100)
            p_amt = base_total * (profit_pct / 100)
            grand_total = base_total + w_amt + p_amt

            st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
            st.markdown(f"### 📊 RATE ANALYSIS SHEET - CONCRETE WORK")
            st.info(f"👤 **Prepared For:** {current_user_name} | **घटक:** {component.split(' ')[0]} | **ग्रेड:** {grade.split(' ')[0]} | **एकूण घनफळ:** {volume} m³")
            
            report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] MATERIAL** | | | | |
| Cement | {c_bags} | Bags | {cement_rate:.2f} | {total_cement_cost:.2f} |
| Sand | {s_m3:.2f} | m³ | {sand_rate:.2f} | {total_sand_cost:.2f} |
| Aggregate | {a_m3:.2f} | m³ | {aggregate_rate:.2f} | {total_aggregate_cost:.2f} |
| Steel | {steel_qty:.2f} | Kg | {steel_rate:.2f} | {total_steel_cost:.2f} |
| **[B] LABOUR** | | | | |
| Mason | {mason_qty} | Nos | {mason_rate:.2f} | {mason_qty*mason_rate:.2f} |
| Mazdoor | {mazdoor_qty} | Nos | {mazdoor_rate:.2f} | {mazdoor_qty*mazdoor_rate:.2f} |
| Bar Bender | {bb_qty} | Nos | {bb_rate:.2f} | {bb_qty*bb_rate:.2f} |
| **[C] OTHER EXPENSES** | | | | |
| Scaffolding / Centering | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies | - | L.S. | - | {contingency_cost:.2f} |
| **TOTAL (A + B + C)** | | | | **{base_total:.2f}** |
| Water Charge ({water_pct}%) | | | | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | | | | {p_amt:.2f} |
| **GRAND TOTAL** | | | | **₹ {grand_total:.2f}/-** |
"""
            st.markdown(report_table)
            
            msg_text = f"🏗️ *PATIL INFRATECH - RATE ANALYSIS REPORT*\n"
            msg_text += f"👤 *Prepared For:* {current_user_name}\n"
            msg_text += f"🧱 *Work:* Concrete Work ({component.split(' ')[0]})\n"
            msg_text += f"📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
            msg_text += f"📋 *DETAILS:*\n"
            msg_text += f"• Cement: {c_bags} Bags @ ₹{cement_rate} = ₹{total_cement_cost:.2f}\n"
            msg_text += f"• Sand: {s_m3:.2f} m³ @ ₹{sand_rate} = ₹{total_sand_cost:.2f}\n"
            msg_text += f"• Aggregate: {a_m3:.2f} m³ @ ₹{aggregate_rate} = ₹{total_aggregate_cost:.2f}\n"
            if steel_percentage > 0:
                msg_text += f"• Steel: {steel_qty:.2f} Kg @ ₹{steel_rate} = ₹{total_steel_cost:.2f}\n"
            msg_text += f"• Labour Total: ₹{lab_cost:.2f}\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"_Generated by Patil Infratech_"

            encoded_msg = urllib.parse.quote(msg_text)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                render_whatsapp_feature(encoded_msg, "ra_conc")
            with btn_col2:
                st.markdown('''
                    <button onclick="window.print()" style="width: 100%; background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px;">
                        📄 Print / Download A3 Size PDF
                    </button>
                ''', unsafe_allow_html=True)

            if current_user_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO history (user_key, timestamp, user_note, report_data) VALUES (?, ?, ?, ?)", (current_user_name, now_str, st.session_state.current_comment, report_table))
                conn.commit()
                conn.close()

    elif "Brickwork" in main_choice:
        st.subheader("🧱 Brickwork Estimation")
        mortar_choice = st.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio) निवडा:", 
                                     ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])
        
        if "1:3" in mortar_choice: c_part, s_part = 1, 3
        elif "1:4" in mortar_choice: c_part, s_part = 1, 4
        elif "1:5" in mortar_choice: c_part, s_part = 1, 5
        else: c_part, s_part = 1, 6

        st.markdown("#### [A] साहित्याची माहिती आणि दर (थेट टाईप करा)")
        bm_col1, bm_col2 = st.columns(2)
        with bm_col1:
            volume = st.number_input("वीटकामाचे एकूण घनफळ भरा (Volume in m³):", min_value=0.0, value=1.0, key="bw_vol")
            brick_rate = st.number_input("विटांचा दर प्रति हजार नग (₹ per 1000 Bricks):", min_value=0.0, value=8000.0, key="bw_br")
        with bm_col2:
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="bw_cr")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="bw_sr")

        st.markdown("#### [B] लेबर खर्च (नसल्यास ० ठेवा)")
        bl_col1, bl_col2 = st.columns(2)
        with bl_col1:
            mason_qty = st.number_input("मेसन संख्या (Brickwork Days):", min_value=0.0, value=0.0, key="bw_mq")
            mason_rate = st.number_input("मेसन प्रतिदिन दर (₹/Day):", min_value=0.0, value=650.0, key="bw_mr")
        with bl_col2:
            mazdoor_qty = st.number_input("मजदूर संख्या (Brickwork Days):", min_value=0.0, value=0.0, key="bw_mzq")
            mazdoor_rate = st.number_input("मजदूर प्रतिदिन दर (₹/Day):", min_value=0.0, value=400.0, key="bw_mzr")

        st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
        bo_col1, bo_col2 = st.columns(2)
        with bo_col1:
            scaffolding_cost = st.number_input("पाळत/स्कॅफोल्डिंग खर्च (₹):", min_value=0.0, value=0.0, key="bw_sc")
            contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=0.0, key="bw_cc")
        with bo_col2:
            water_pct = st.number_input("वॉटर charge (%):", min_value=0.0, value=1.0, key="bw_wp")
            profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0, key="bw_pp")

        st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
        user_note = st.text_area("या एस्टिमेशन संदर्भात काही नोट किंवा कमेंट लिहायची असल्यास इथे लिहा:", placeholder="उदा. ग्राउंड फ्लोअर वीटकाम...", key="bw_note")
        if st.button("💬 कमेंट सबमिट करा", key="bw_comment_btn"):
            if user_note.strip():
                st.session_state.current_comment = user_note.strip()
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET comment = ? WHERE user_key = ?", (user_note.strip(), current_user_name))
                conn.commit()
                conn.close()
                st.success("✅ कमेंट सेव्ह झाली!")

        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="bw_report_btn"):
            total_bricks = math.ceil(volume * 500)
            dry_mortar_vol = volume * 0.30
            total_mortar_parts = c_part + s_part
            
            cement_vol = (c_part / total_mortar_parts) * dry_mortar_vol if total_mortar_parts > 0 else 0.0
            sand_m3 = (s_part / total_mortar_parts) * dry_mortar_vol if total_mortar_parts > 0 else 0.0
            cement_bags = math.ceil(cement_vol * 28.8)

            total_brick_cost = (total_bricks / 1000) * brick_rate
            total_cement_cost = cement_bags * cement_rate
            total_sand_cost = sand_m3 * sand_rate

            mat_cost = total_brick_cost + total_cement_cost + total_sand_cost
            lab_cost = (mason_qty * mason_rate) + (mazdoor_qty * mazdoor_rate)
            base_total = mat_cost + lab_cost + scaffolding_cost + contingency_cost
            
            w_amt = base_total * (water_pct / 100)
            p_amt = base_total * (profit_pct / 100)
            grand_total = base_total + w_amt + p_amt

            st.success("🎉 वीटकाम रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
            st.markdown(f"### 📊 RATE ANALYSIS SHEET - BRICKWORK")
            st.info(f"👤 **Prepared For:** {current_user_name} | **गुणोत्तर:** {mortar_choice.split(' ')[0]} | **एकूण घनफळ:** {volume} m³")
            
            report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] MATERIAL** | | | | |
| Bricks | {total_bricks} | Nos | {(brick_rate/1000):.2f} / नग | {total_brick_cost:.2f} |
| Cement | {cement_bags} | Bags | {cement_rate:.2f} | {total_cement_cost:.2f} |
| Sand | {sand_m3:.2f} | m³ | {sand_rate:.2f} | {total_sand_cost:.2f} |
| **[B] LABOUR** | | | | |
| Mason | {mason_qty} | Nos | {mason_rate:.2f} | {mason_qty*mason_rate:.2f} |
| Mazdoor | {mazdoor_qty} | Nos | {mazdoor_rate:.2f} | {mazdoor_qty*mazdoor_rate:.2f} |
| **[C] OTHER EXPENSES** | | | | |
| Scaffolding / Centering | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies | - | L.S. | - | {contingency_cost:.2f} |
| **TOTAL (A + B + C)** | | | | **{base_total:.2f}** |
| Water Charge ({water_pct}%) | | | | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | | | | {p_amt:.2f} |
| **GRAND TOTAL** | | | | **₹ {grand_total:.2f}/-** |
"""
            st.markdown(report_table)

            msg_text = f"🏗️ *PATIL INFRATECH - BRICKWORK REPORT*\n"
            msg_text += f"👤 *Prepared For:* {current_user_name}\n"
            msg_text += f"🧱 *Ratio:* {mortar_choice.split(' ')[0]} | *Vol:* {volume} m³\n"
            msg_text += f"📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
            msg_text += f"📋 *DETAILS:*\n"
            msg_text += f"• Bricks: {total_bricks} Nos = ₹{total_brick_cost:.2f}\n"
            msg_text += f"• Cement: {cement_bags} Bags = ₹{total_cement_cost:.2f}\n"
            msg_text += f"• Sand: {sand_m3:.2f} m³ = ₹{total_sand_cost:.2f}\n"
            msg_text += f"• Labour: {lab_cost:.2f}\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"_Generated by Patil Infratech_"

            encoded_msg = urllib.parse.quote(msg_text)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                render_whatsapp_feature(encoded_msg, "ra_bw")
            with btn_col2:
                st.markdown('''
                    <button onclick="window.print()" style="width: 100%; background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px;">
                        📄 Print / Download A3 Size PDF
                    </button>
                ''', unsafe_allow_html=True)

            if current_user_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO history (user_key, timestamp, user_note, report_data) VALUES (?, ?, ?, ?)", (current_user_name, now_str, st.session_state.current_comment, report_table))
                conn.commit()
                conn.close()

    else:  # Plaster Work
        st.subheader("🎨 Plaster Work Estimation")
        
        thickness_mm = st.number_input("प्लास्टरची जाडी (Thickness in mm):", min_value=5.0, max_value=50.0, value=12.0, step=1.0, key="pl_thick")

        plaster_mortar = st.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio):", [
            "1:3 (सिमेंट : वाळू)",
            "1:4 (सिमेंट : वाळू)", 
            "1:5 (सिमेंट : वाळू)",
            "1:6 (सिमेंट : वाळू)"
        ])

        if "1:3" in plaster_mortar: p_c_part, p_s_part = 1, 3
        elif "1:4" in plaster_mortar: p_c_part, p_s_part = 1, 4
        elif "1:5" in plaster_mortar: p_c_part, p_s_part = 1, 5
        else: p_c_part, p_s_part = 1, 6

        st.markdown("#### [A] साहित्याची माहिती आणि दर (क्षेत्रफळ, दर व वॉटरप्रूफिंग)")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            plaster_area = st.number_input("प्लास्टरचे एकूण क्षेत्रफळ (Area in m²):", min_value=0.0, value=10.0, key="pl_area")
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="pl_cem_r")
            use_waterproofing = st.checkbox("💧 वॉटरप्रूफिंग कंपाउंड ॲड करा (Waterproofing Compound)", value=False)
        with p_col2:
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="pl_snd_r")
            wp_rate = st.number_input("वाटरप्रूफिंग दर (प्रति किलोग्रॅम/लिटर ₹):", min_value=0.0, value=150.0, key="pl_wp_r") if use_waterproofing else 0.0

        st.markdown("#### [B] लेबर खर्च (दिवसानुसार किंवा लांप सम)")
        pl_l1, pl_l2 = st.columns(2)
        with pl_l1:
            pl_mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, value=0.0, key="pl_mq")
            pl_mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=650.0, key="pl_mr")
        with pl_l2:
            pl_mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, value=0.0, key="pl_mzq")
            pl_mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=400.0, key="pl_mzr")

        st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
        po_c1, po_c2 = st.columns(2)
        with po_c1:
            scaffolding_cost = st.number_input("स्कॅफोल्डिंग/पाळत खर्च (₹):", min_value=0.0, value=0.0, key="pl_sc")
            contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=0.0, key="pl_cc")
        with po_c2:
            water_pct = st.number_input("वॉटर charge (%):", min_value=0.0, value=1.0, key="pl_wp")
            profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0, key="pl_pp")

        st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
        user_note = st.text_area("या प्लास्टर एस्टिमेशन संदर्भात काही नोंद लिहायची असल्यास इथे लिहा:", placeholder="उदा. फ्रंट वॉल प्लास्टर...", key="pl_note")
        if st.button("💬 कमेंट सबमिट करा", key="pl_comm_btn"):
            if user_note.strip():
                st.session_state.current_comment = user_note.strip()
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET comment = ? WHERE user_key = ?", (user_note.strip(), current_user_name))
                conn.commit()
                conn.close()
                st.success("✅ कमेंट सेव्ह झाली!")

        if st.button("📊 GENERATE PLASTER REPORT", type="primary", key="pl_report_btn"):
            wet_volume = plaster_area * (thickness_mm / 1000.0)
            dry_volume = wet_volume * 1.33
            total_parts = p_c_part + p_s_part

            cement_vol = (p_c_part / total_parts) * dry_volume if total_parts > 0 else 0.0
            sand_m3 = (p_s_part / total_parts) * dry_volume if total_parts > 0 else 0.0
            cement_bags = math.ceil(cement_vol * 28.8)

            total_cement_cost = cement_bags * cement_rate
            total_sand_cost = sand_m3 * sand_rate

            wp_qty_kg = cement_bags * 1.0 if use_waterproofing else 0.0
            total_wp_cost = wp_qty_kg * wp_rate

            mat_cost = total_cement_cost + total_sand_cost + total_wp_cost
            lab_cost = (pl_mason_qty * pl_mason_rate) + (pl_mazdoor_qty * pl_mazdoor_rate)
            base_total = mat_cost + lab_cost + scaffolding_cost + contingency_cost
            
            w_amt = base_total * (water_pct / 100)
            p_amt = base_total * (profit_pct / 100)
            grand_total = base_total + w_amt + p_amt

            st.success("🎉 प्लास्टर काम रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
            st.markdown(f"### 📊 RATE ANALYSIS SHEET - PLASTER WORK")
            st.info(f"👤 **Prepared For:** {current_user_name} | **जाडी:** {thickness_mm} mm | **क्षेत्रफळ:** {plaster_area} m² | **गुणोत्तर:** {plaster_mortar.split(' ')[0]}")
            
            wp_row_table = f"| Waterproofing Compound | {wp_qty_kg:.2f} | Kg/Ltr | {wp_rate:.2f} | {total_wp_cost:.2f} |\n" if use_waterproofing else ""

            report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] MATERIAL** | | | | |
| Cement | {cement_bags} | Bags | {cement_rate:.2f} | {total_cement_cost:.2f} |
| Sand | {sand_m3:.2f} | m³ | {sand_rate:.2f} | {total_sand_cost:.2f} |
{wp_row_table}| **[B] LABOUR** | | | | |
| Mason | {pl_mason_qty} | Nos | {pl_mason_rate:.2f} | {pl_mason_qty*pl_mason_rate:.2f} |
| Mazdoor | {pl_mazdoor_qty} | Nos | {pl_mazdoor_rate:.2f} | {pl_mazdoor_qty*pl_mazdoor_rate:.2f} |
| **[C] OTHER EXPENSES** | | | | |
| Scaffolding / Centering | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies | - | L.S. | - | {contingency_cost:.2f} |
| **TOTAL (A + B + C)** | | | | **{base_total:.2f}** |
| Water Charge ({water_pct}%) | | | | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | | | | {p_amt:.2f} |
| **GRAND TOTAL** | | | | **₹ {grand_total:.2f}/-** |
"""
            st.markdown(report_table)

            msg_text = f"🏗️ *PATIL INFRATECH - PLASTER REPORT*\n"
            msg_text += f"👤 *Prepared For:* {current_user_name}\n"
            msg_text += f"🎨 *Thickness:* {thickness_mm}mm | *Area:* {plaster_area} m²\n"
            msg_text += f"📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
            msg_text += f"📋 *DETAILS:*\n"
            msg_text += f"• Cement: {cement_bags} Bags = ₹{total_cement_cost:.2f}\n"
            msg_text += f"• Sand: {sand_m3:.2f} m³ = ₹{total_sand_cost:.2f}\n"
            if use_waterproofing:
                msg_text += f"• Waterproofing: {wp_qty_kg:.2f} Kg = ₹{total_wp_cost:.2f}\n"
            msg_text += f"• Labour: {lab_cost:.2f}\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n"
            msg_text += f"--------------------------------\n"
            msg_text += f"_Generated by Patil Infratech_"

            encoded_msg = urllib.parse.quote(msg_text)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                render_whatsapp_feature(encoded_msg, "ra_pl")
            with btn_col2:
                st.markdown('''
                    <button onclick="window.print()" style="width: 100%; background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px;">
                        📄 Print / Download A3 Size PDF
                    </button>
                ''', unsafe_allow_html=True)

            if current_user_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO history (user_key, timestamp, user_note, report_data) VALUES (?, ?, ?, ?)", (current_user_name, now_str, st.session_state.current_comment, report_table))
                conn.commit()
                conn.close()

# ==========================================
# 🛑 MODULE 2: BBS MODULE
# ==========================================
elif st.session_state.selected_module == "BBS":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_bbs"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("🏗️ Bar Bending Schedule (BBS Calculator)")
    
    default_covers = {
        "Footing": 50,
        "Column": 40,
        "Beam": 25,
        "Slab": 20
    }

    def update_cover_from_component():
        selected_comp = st.session_state.get("bbs_rcc_component", "Footing")
        st.session_state["bbs_cover"] = default_covers.get(selected_comp, 25)

    if "bbs_cover" not in st.session_state:
        st.session_state["bbs_cover"] = 50

    rcc_comp = st.selectbox(
        "घटक (RCC Component) निवडा:", 
        ["Footing", "Column", "Beam", "Slab"],
        key="bbs_rcc_component",
        on_change=update_cover_from_component
    )

    st.markdown("#### [१] घटकाचे आकारमान (Dimensions in Meters - m)")
    dim_col1, dim_col2, dim_col3 = st.columns(3)
    with dim_col1:
        length_m = st.number_input("लांबी L (m):", min_value=0.1, value=3.0, step=0.1, key="bbs_l")
    with dim_col2:
        width_m = st.number_input("रुंदी B (m):", min_value=0.1, value=0.3, step=0.05, key="bbs_b")
    with dim_col3:
        height_m = st.number_input("उंची/खोली H/Depth (m):", min_value=0.1, value=0.45, step=0.05, key="bbs_h")

    st.markdown("#### [२] Clear Cover (मिमी मध्ये)")
    cover = st.number_input(
        "Clear Cover (mm):", 
        min_value=10, 
        max_value=100, 
        step=5, 
        key="bbs_cover"
    )
    st.caption(f"💡 **टीप:** {rcc_comp} साठी मानांकित Clear Cover **{cover} mm** आपोआप सेट केला आहे.")

    st.markdown("#### [३] स्टील बारचे प्रकार आणि व्यास (Steel Reinforcement Details)")
    
    dia_list = [8, 10, 12, 16, 20, 25, 32]
    num_members = st.number_input("एकूण घटक संख्या (No. of Identical Members):", min_value=1, value=1, step=1, key="bbs_mem")

    if rcc_comp == "Footing":
        c1, c2 = st.columns(2)
        with c1:
            f_main_dia = st.selectbox("Main Bar DIA (mm):", dia_list, index=2, key="f_m_dia")
            f_main_spacing = st.number_input("Main Bar Spacing (mm):", min_value=50, value=150, step=10, key="f_m_sp")
        with c2:
            f_dist_dia = st.selectbox("Distribution Bar DIA (mm):", dia_list, index=1, key="f_d_dia")
            f_dist_spacing = st.number_input("Distribution Bar Spacing (mm):", min_value=50, value=150, step=10, key="f_d_sp")

    elif rcc_comp == "Column":
        c1, c2, c3 = st.columns(3)
        with c1:
            col_main_dia = st.selectbox("Main Vertical Bar DIA (mm):", dia_list, index=3, key="col_m_dia")
            col_main_nos = st.number_input("Main Bars (नग/Nos):", min_value=4, value=4, step=2, key="col_m_nos")
        with c2:
            col_st_dia = st.selectbox("Stirrup/Ring DIA (mm):", dia_list, index=0, key="col_s_dia")
            col_st_spacing = st.number_input("Stirrup Spacing (mm):", min_value=50, value=150, step=10, key="col_s_sp")
        with c3:
            col_hook_angle = st.selectbox("Ring Hook Angle:", ["135° (Hook = 10d)", "90° (Hook = 6d)"], key="col_h_ang")

    elif rcc_comp == "Beam":
        c1, c2, c3 = st.columns(3)
        with c1:
            bm_top_dia = st.selectbox("Top Main Bar DIA (mm):", dia_list, index=2, key="bm_t_dia")
            bm_top_nos = st.number_input("Top Bars (नग/Nos):", min_value=2, value=2, step=1, key="bm_t_nos")
        with c2:
            bm_bot_dia = st.selectbox("Bottom Main Bar DIA (mm):", dia_list, index=3, key="bm_b_dia")
            bm_bot_nos = st.number_input("Bottom Bars (नग/Nos):", min_value=2, value=2, step=1, key="bm_b_nos")
        with c3:
            bm_st_dia = st.selectbox("Stirrup/Ring DIA (mm):", dia_list, index=0, key="bm_s_dia")
            bm_st_spacing = st.number_input("Stirrup Spacing (mm):", min_value=50, value=150, step=10, key="bm_s_sp")

    else:  # Slab
        c1, c2 = st.columns(2)
        with c1:
            sl_main_dia = st.selectbox("Main Bar DIA (mm):", dia_list, index=1, key="sl_m_dia")
            sl_main_spacing = st.number_input("Main Bar Spacing (mm):", min_value=50, value=150, step=10, key="sl_m_sp")
        with c2:
            sl_dist_dia = st.selectbox("Distribution Bar DIA (mm):", dia_list, index=0, key="sl_d_dia")
            sl_dist_spacing = st.number_input("Distribution Bar Spacing (mm):", min_value=50, value=150, step=10, key="sl_d_spacing")

    master_rates = get_market_rates()
    steel_rate_kg = st.number_input("आजचा स्टील दर (₹/Kg):", min_value=0.0, value=float(master_rates.get("steel", 60.0)), key="bbs_rate")

    st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
    user_note = st.text_area("या BBS बाबत काही नोंद लिहायची असल्यास इथे लिहा:", placeholder="उदा. Column C1 BBS Details...", key="bbs_note")
    if st.button("💬 कमेंट सबमिट करा", key="bbs_comment_btn"):
        if user_note.strip():
            st.session_state.current_comment = user_note.strip()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET comment = ? WHERE user_key = ?", (user_note.strip(), current_user_name))
            conn.commit()
            conn.close()
            st.success("✅ कमेंट सेव्ह झाली!")

    if st.button("🧮 CALCULATE BBS REPORT", type="primary", key="bbs_calc_btn"):
        length_mm = length_m * 1000.0
        width_mm = width_m * 1000.0
        height_mm = height_m * 1000.0

        l_net = length_mm - (2 * cover)
        b_net = width_mm - (2 * cover)
        h_net = height_mm - (2 * cover)

        calc_list = []

        if rcc_comp == "Footing":
            m_leg = 200.0
            m_cut_m = (l_net + (2 * m_leg) - (4 * f_main_dia)) / 1000.0
            m_nos = (math.ceil(width_mm / f_main_spacing) + 1) * num_members
            m_tot_len = m_cut_m * m_nos
            m_unit_wt = (f_main_dia ** 2) / 162.0
            m_tot_wt = m_tot_len * m_unit_wt
            calc_list.append({"Desc": "Main Bars (Longitudinal)", "Nos": m_nos, "Dia": f_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt})

            d_leg = 200.0
            d_cut_m = (b_net + (2 * d_leg) - (4 * f_dist_dia)) / 1000.0
            d_nos = (math.ceil(length_mm / f_dist_spacing) + 1) * num_members
            d_tot_len = d_cut_m * d_nos
            d_unit_wt = (f_dist_dia ** 2) / 162.0
            d_tot_wt = d_tot_len * d_unit_wt
            calc_list.append({"Desc": "Distribution Bars (Transverse)", "Nos": d_nos, "Dia": f_dist_dia, "Len": d_cut_m, "TotLen": d_tot_len, "Wt": d_unit_wt, "TotWt": d_tot_wt})

        elif rcc_comp == "Column":
            m_ld = 300.0
            m_cut_m = (height_mm + m_ld) / 1000.0
            m_nos = col_main_nos * num_members
            m_tot_len = m_cut_m * m_nos
            m_unit_wt = (col_main_dia ** 2) / 162.0
            m_tot_wt = m_tot_len * m_unit_wt
            calc_list.append({"Desc": "Main Vertical Bars", "Nos": m_nos, "Dia": col_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt})

            hook_len = 10 * col_st_dia if "135°" in col_hook_angle else 6 * col_st_dia
            st_cut_m = ((2 * (b_net + h_net)) + (2 * hook_len) - (3 * 2 * col_st_dia)) / 1000.0
            st_nos = (math.ceil(height_mm / col_st_spacing) + 1) * num_members
            st_tot_len = st_cut_m * st_nos
            st_unit_wt = (col_st_dia ** 2) / 162.0
            st_tot_wt = st_tot_len * st_unit_wt
            calc_list.append({"Desc": "Stirrups / Ties (Rings)", "Nos": st_nos, "Dia": col_st_dia, "Len": st_cut_m, "TotLen": st_tot_len, "Wt": st_unit_wt, "TotWt": st_tot_wt})

        elif rcc_comp == "Beam":
            t_ld = max(300.0, 30 * bm_top_dia)
            t_cut_m = (l_net + (2 * t_ld) - (4 * bm_top_dia)) / 1000.0
            t_nos = bm_top_nos * num_members
            t_tot_len = t_cut_m * t_nos
            t_unit_wt = (bm_top_dia ** 2) / 162.0
            t_tot_wt = t_tot_len * t_unit_wt
            calc_list.append({"Desc": "Top Main Bars", "Nos": t_nos, "Dia": bm_top_dia, "Len": t_cut_m, "TotLen": t_tot_len, "Wt": t_unit_wt, "TotWt": t_tot_wt})

            b_ld = max(300.0, 30 * bm_bot_dia)
            b_cut_m = (l_net + (2 * b_ld) - (4 * bm_bot_dia)) / 1000.0
            b_nos = bm_bot_nos * num_members
            b_tot_len = b_cut_m * b_nos
            b_unit_wt = (bm_bot_dia ** 2) / 162.0
            b_tot_wt = b_tot_len * b_unit_wt
            calc_list.append({"Desc": "Bottom Main Bars", "Nos": b_nos, "Dia": bm_bot_dia, "Len": b_cut_m, "TotLen": b_tot_len, "Wt": b_unit_wt, "TotWt": b_tot_wt})

            st_cut_m = ((2 * (b_net + h_net)) + (2 * 10 * bm_st_dia) - (3 * 2 * bm_st_dia)) / 1000.0
            st_nos = (math.ceil(length_mm / bm_st_spacing) + 1) * num_members
            st_tot_len = st_cut_m * st_nos
            st_unit_wt = (bm_st_dia ** 2) / 162.0
            st_tot_wt = st_tot_len * st_unit_wt
            calc_list.append({"Desc": "Stirrups / Rings", "Nos": st_nos, "Dia": bm_st_dia, "Len": st_cut_m, "TotLen": st_tot_len, "Wt": st_unit_wt, "TotWt": st_tot_wt})

        else:  # Slab
            m_hook = 10 * sl_main_dia
            m_cut_m = (l_net + (2 * m_hook)) / 1000.0
            m_nos = (math.ceil(width_mm / sl_main_spacing) + 1) * num_members
            m_tot_len = m_cut_m * m_nos
            m_unit_wt = (sl_main_dia ** 2) / 162.0
            m_tot_wt = m_tot_len * m_unit_wt
            calc_list.append({"Desc": "Main Bars", "Nos": m_nos, "Dia": sl_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt})

            d_hook = 10 * sl_dist_dia
            d_cut_m = (b_net + (2 * d_hook)) / 1000.0
            d_nos = (math.ceil(length_mm / sl_dist_spacing) + 1) * num_members
            d_tot_len = d_cut_m * d_nos
            d_unit_wt = (sl_dist_dia ** 2) / 162.0
            d_tot_wt = d_tot_len * d_unit_wt
            calc_list.append({"Desc": "Distribution Bars", "Nos": d_nos, "Dia": sl_dist_dia, "Len": d_cut_m, "TotLen": d_tot_len, "Wt": d_unit_wt, "TotWt": d_tot_wt})

        total_weight_kg = sum(item["TotWt"] for item in calc_list)
        total_cost = total_weight_kg * steel_rate_kg

        st.success("🎉 BBS रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 🏗️ BAR BENDING SCHEDULE (BBS) REPORT")
        st.info(f"👤 **Prepared For:** {current_user_name} | **घटक:** {rcc_comp} | **Clear Cover:** {cover} mm | **एकूण घटक संख्या:** {num_members}")

        table_rows = ""
        for item in calc_list:
            table_rows += f"| {item['Desc']} | {item['Nos']} | {item['Dia']} mm | {item['Len']:.3f} m | {item['TotLen']:.2f} m | {item['Wt']:.3f} Kg/m | {item['TotWt']:.2f} Kg |\n"

        report_table = f"""
<div class="print-container">
<h2>🏗️ PATIL INFRATECH - BAR BENDING SCHEDULE (BBS)</h2>
<p><strong>Prepared For:</strong> {current_user_name} | <strong>Component:</strong> {rcc_comp} | <strong>Date:</strong> {get_ist_time().strftime('%d-%m-%Y')}</p>

| DESCRIPTION | NOS | DIA | LENGTH | TOTAL LENGTH | WEIGHT | TOTAL WEIGHT |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{table_rows}

---
### 📌 SUMMARY DETAILS
* **Dimensions (L x B x H):** {length_m:.2f} m x {width_m:.2f} m x {height_m:.2f} m
* **Total Steel Weight:** **{total_weight_kg:.2f} Kg** ({total_weight_kg/1000:.3f} MT)
* **Steel Rate:** ₹ {steel_rate_kg:.2f} / Kg
* **GRAND TOTAL COST:** **₹ {total_cost:.2f}/-**
</div>
"""
        st.markdown(report_table, unsafe_allow_html=True)

        msg_text = f"🏗️ *PATIL INFRATECH - BAR BENDING SCHEDULE (BBS)*\n"
        msg_text += f"👤 *Prepared For:* {current_user_name}\n"
        msg_text += f"📐 *Component:* {rcc_comp}\n"
        msg_text += f"📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n"
        msg_text += f"📐 *Size:* {length_m:.2f}m x {width_m:.2f}m x {height_m:.2f}m\n\n"
        msg_text += f"📊 *DETAILED BAR SCHEDULE:*\n"
        msg_text += f"--------------------------------\n"

        for idx, item in enumerate(calc_list, 1):
            msg_text += f"*{idx}. {item['Desc']}*\n"
            msg_text += f"  • Nos: {item['Nos']} | Dia: {item['Dia']}mm\n"
            msg_text += f"  • Cutting Len: {item['Len']:.3f} m\n"
            msg_text += f"  • Total Len: {item['TotLen']:.2f} m\n"
            msg_text += f"  • Total Weight: {item['TotWt']:.2f} Kg\n\n"

        msg_text += f"--------------------------------\n"
        msg_text += f"⚖️ *TOTAL STEEL WEIGHT:* {total_weight_kg:.2f} Kg ({total_weight_kg/1000:.3f} MT)\n"
        msg_text += f"💵 *Steel Rate:* ₹ {steel_rate_kg:.2f} / Kg\n"
        msg_text += f"💰 *ESTIMATED COST:* ₹ {total_cost:.2f}/-\n"
        msg_text += f"--------------------------------\n"
        msg_text += f"_Generated by Patil Infratech_"

        encoded_msg = urllib.parse.quote(msg_text)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            render_whatsapp_feature(encoded_msg, "bbs_main")
        with btn_col2:
            st.markdown('''
                <button onclick="window.print()" style="width: 100%; background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px;">
                    📄 Print / Save A3 Size PDF
                </button>
            ''', unsafe_allow_html=True)

        if current_user_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO history (user_key, timestamp, user_note, report_data) VALUES (?, ?, ?, ?)", (current_user_name, now_str, st.session_state.current_comment, report_table))
            conn.commit()
            conn.close()
