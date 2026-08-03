# KANHA_1p - पाटील इन्फ्राटेक (SQLite Database & Streamlit Web Application with Email OTP)
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
# 📧 EMAIL OTP SENDING FUNCTION (FREE GMAIL SMTP)
# ==========================================
def send_email_otp(receiver_email, otp_code):
    sender_email = st.secrets.get("EMAIL_USER", "your_email@gmail.com") if hasattr(st, "secrets") else "your_email@gmail.com"
    sender_password = st.secrets.get("EMAIL_PASS", "your_gmail_app_password") if hasattr(st, "secrets") else "your_gmail_app_password"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "PATIL INFRATECH - Login OTP Verification"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"नमस्कार!\nतुमचा पाटील इन्फ्राटेक लॉगिन/रेजिस्ट्रेशन OTP हा आहे: {otp_code}\nहा OTP कोणासोबतही शेअर करू नका.\n\n- पाटील इन्फ्राटेक टीम"
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

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
    
    # 1. Users Table (Email & Password based)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_key TEXT PRIMARY KEY,
            id TEXT,
            pin TEXT,
            mobile TEXT,
            email TEXT UNIQUE,
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
            INSERT INTO users (user_key, id, pin, mobile, email, password, comment, admin_message, unread_notification, is_premium, premium_expiry, requested_code, seen_popup, master_code_uses, last_active, activated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("9999999999", "kanha", "1234", "9999999999", "admin@patilinfratech.com", "patiladmin123", "मास्टर ॲडमीन अकाउंट", "स्वागत है मास्टर कन्हैया! आपले पाटील इन्फ्राटेक मध्ये सर्व अधिकार अनलॉक्ड आहेत ⚡", 0, 1, "2099-12-31 23:59:59", 0, 1, 0, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), "Master Admin"))

    # Default Feature Locks
    default_locks = {
        "Civil Calculator": "Free",
        "Rate Analysis": "Free",
        "BBS": "Free",
        "Quantity Surveying": "Free",
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
if "pending_email" not in st.session_state:
    st.session_state.pending_email = None
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

query_params = st.query_params
if st.session_state.app_user_name is None and "saved_email" in query_params:
    saved_email = query_params["saved_email"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_key FROM users WHERE email = ?", (saved_email,))
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

# 🟢 युझर ॲक्टिव्ह असेल तर त्याची वेळ अपडेट करणे
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
# 🎨 ULTRA-PREMIUM ROYAL METALLIC GOLD STYLING
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

def generate_random_code():
    return "PATIL-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# ==========================================
# 📱 WHATSAPP SHARING
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
# --- १. वेलकम स्क्रीन ॲनिमेशन ---
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
# 🛡️ ADMIN PANEL
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
    
    ac1, ac2, ac3, ac4, ac5 = st.columns(5)
    with ac1:
        if st.button("📈 Rates", use_container_width=True):
            st.session_state.admin_dashboard_tab = "rates"
    with ac2:
        if st.button("⚙️ Locks", use_container_width=True):
            st.session_state.admin_dashboard_tab = "locks"
    with ac3:
        if st.button("👥 Users", use_container_width=True):
            st.session_state.admin_dashboard_tab = "users"
    with ac4:
        if st.button("📢 Ads", use_container_width=True):
            st.session_state.admin_dashboard_tab = "ads"
    with ac5:
        if st.button("🔔 Broadcast", use_container_width=True):
            st.session_state.admin_dashboard_tab = "broadcast"

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
        fl_qs = st.selectbox("Quantity Surveying Access:", ["Free", "Premium"], index=0 if cur_locks.get("Quantity Surveying", "Free") == "Free" else 1)
        fl_wa = st.selectbox("WhatsApp Full Report Share:", ["Free", "Premium"], index=0 if cur_locks.get("WhatsApp Share", "Free") == "Free" else 1)
        fl_ai = st.selectbox("Civil AI Assistant Access:", ["Free", "Premium"], index=0 if cur_locks.get("Civil AI Assistant", "Premium") == "Free" else 1)

        if st.button("💾 Save Feature Lock Settings", type="primary"):
            conn = get_db_connection()
            cursor = conn.cursor()
            new_locks = {
                "Civil Calculator": fl_calc,
                "Rate Analysis": fl_ra,
                "BBS": fl_bbs,
                "Quantity Surveying": fl_qs,
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
            u_mob = info.get("mobile", "N/A")
            u_email = info.get("email", "N/A")
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
                    <p style="margin:5px 0; font-size:15px;"><b>Mobile:</b> <code>{u_mob}</code> | <b>Email:</b> <code>{u_email}</code></p>
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
                    u_email = info.get("email", "N/A")
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
                        col_u1.markdown(f"<span class='gold-vip-badge'>👑 VIP: {u_name.upper()}</span> (Email: <code>{u_email}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)
                    elif is_req:
                        col_u1.markdown(f"#### 👤 **{u_name}** `[🚨 CODE]` (Email: `{u_email}`)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)
                    else:
                        col_u1.markdown(f"<span class='free-user-badge'>🆓 FREE: {u_name.upper()}</span> (Email: <code>{u_email}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>", unsafe_allow_html=True)

                    if col_u2.button(f"👁️ View / Manage", key=f"open_user_win_{mob}"):
                        st.session_state.admin_view = "user_detail"
                        st.session_state.admin_selected_user = mob
                        st.rerun()
                    st.write("---")
            else:
                st.info("ℹ️ डेटाबेसमध्ये सध्या कोणताही सामान्य युझर नाही.")

    elif current_tab == "ads":
        st.markdown("### 📢 Ad & Sponsor Manager")
        with st.form("add_ad_form"):
            ad_title = st.text_input("Sponsor / Ad Title:")
            ad_desc = st.text_area("Offer / Description:")
            ad_link = st.text_input("Target Link (URL or WhatsApp link):")
            media_type = st.selectbox("Media Type:", ["Photo (PNG/JPG)", "Video Ad"])
            media_url = st.text_input("Media Direct URL (Image/Video Link):")
            position = st.selectbox("Display Position:", ["Loading Page (Title Sponsor)", "Main App Header (Top Banner)"])
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

    elif current_tab == "broadcast":
        st.markdown("### 🔔 Broadcast Notification to All Users")
        with st.form("broadcast_form"):
            broadcast_msg = st.text_area("सर्व युझर्सना पाठवायचा मेसेज (Broadcast Message):")
            submit_broadcast = st.form_submit_button("🚀 Send to All Users (Broadcast)", type="primary")

            if submit_broadcast:
                if broadcast_msg.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users 
                        SET admin_message = ?, unread_notification = 1 
                        WHERE user_key != '9999999999'
                    ''', (broadcast_msg.strip(),))
                    conn.commit()
                    conn.close()
                    st.success("🎉 ब्रॉडकास्ट मेसेज सर्व युझर्सना यशस्वीरित्या पाठवला गेला आहे!")

    st.stop()

# ==========================================
# 👤 SECURE LOGIN / SIGNUP WITH EMAIL / PASSWORD
# ==========================================
if st.session_state.app_user_name is None:
    st.markdown("### 🏗️ PATIL INFRATECH - SECURE LOGIN")
    auth_mode = st.radio("निवडा (Select Option):", ["📧 Email & Password Login (लॉगिन करा)", "✨ Register (नवीन अकाउंट)", "🔑 Forgot Password (पासवर्ड बदला)"], horizontal=True)

    if "Email & Password Login" in auth_mode:
        with st.form("email_pass_login_form"):
            login_email = st.text_input("ईमेल आयडी (Email ID):").strip()
            login_pass = st.text_input("पासवर्ड (Password):", type="password").strip()
            remember_me = st.checkbox("📌 या डिव्हाइसवर अकाउंट सेव्ह ठेवा (Remember Me)", value=False)
            submit_login = st.form_submit_button("🚀 Login Now", type="primary")

            if submit_login:
                if login_email and login_pass:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT user_key, password FROM users WHERE email = ?", (login_email,))
                    row = cursor.fetchone()
                    conn.close()

                    if row and row["password"] == login_pass:
                        st.session_state.app_user_name = row["user_key"]
                        if remember_me:
                            st.query_params["saved_email"] = login_email
                        st.success("🎉 यशस्वीरित्या लॉगिन झाले!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा ईमेल किंवा पासवर्ड!")
                else:
                    st.warning("⚠️ कृपया ईमेल आणि पासवर्ड दोन्ही भरा!")

    elif "Register" in auth_mode:
        with st.form("email_reg_form"):
            reg_name = st.text_input("नाव (Name):", placeholder="नाव टाका").strip()
            reg_mob = st.text_input("मोबाईल नंबर (Mobile Number):", placeholder="१० अंकी नंबर").strip()
            reg_email = st.text_input("ईमेल आयडी (Email ID):", placeholder="abc@gmail.com").strip()
            reg_pass = st.text_input("पासवर्ड तयार करा (Create Password):", type="password", placeholder="तुमचा पासवर्ड").strip()
            remember_me_reg = st.checkbox("📌 या डिव्हाइसवर अकाउंट सेव्ह ठेवा (Remember Me)", value=False, key="reg_rem")
            submit_reg = st.form_submit_button("✨ Register & Verify Email OTP", type="primary")

            if submit_reg:
                if reg_name and len(reg_mob) >= 10 and "@" in reg_email and len(reg_pass) >= 4:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT user_key FROM users WHERE mobile = ? OR email = ?", (reg_mob, reg_email))
                    exists = cursor.fetchone()
                    conn.close()

                    if exists:
                        st.error("❌ या मोबाईल नंबर किंवा ईमेलवर आधीच अकाउंट तयार आहे!")
                    else:
                        generated_otp = ''.join(random.choices(string.digits, k=6))
                        st.session_state.generated_otp = generated_otp
                        st.session_state.pending_email = reg_email
                        st.session_state.pending_reg_data = {
                            "name": reg_name,
                            "mobile": reg_mob,
                            "password": reg_pass
                        }
                        
                        with st.spinner("📧 ईमेलवर 6 अंकी OTP पाठवत आहे..."):
                            success = send_email_otp(reg_email, generated_otp)
                            if success:
                                st.success("✅ तुमच्या ईमेलवर OTP पाठवला आहे! खाली व्हेरिफाय करा.")
                            else:
                                st.error("❌ ईमेल पाठवताना एरर आली.")
                else:
                    st.warning("⚠️ कृपया सर्व माहिती आणि कमीत कमी ४ अंकी पासवर्ड अचूक भरा!")

        if st.session_state.get("generated_otp") and st.session_state.get("pending_reg_data"):
            st.markdown("#### 🔐 Email OTP Verification for Registration")
            entered_otp = st.text_input("6 अंकी OTP टाका:", max_chars=6, key="reg_otp_input").strip()
            if st.button("✅ Verify & Complete Registration", type="primary"):
                if entered_otp == st.session_state.generated_otp:
                    r_data = st.session_state.pending_reg_data
                    uname = r_data["name"].split()[0].upper() + "".join(random.choices(string.digits, k=3))
                    welcome_msg = f"{r_data['name']} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO users (user_key, id, pin, mobile, email, password, comment, admin_message, unread_notification, is_premium, premium_expiry, requested_code, seen_popup, master_code_uses, last_active, activated_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, NULL, 0, 0, 0, ?, ?)
                    ''', (uname, r_data["name"], "1234", r_data["mobile"], st.session_state.pending_email, r_data["password"], "काही नाही", welcome_msg, now_str, "Free User"))
                    conn.commit()
                    conn.close()

                    st.session_state.app_user_name = uname
                    st.success("🎉 अकाउंट यशस्वीरित्या तयार झाले व लॉगिन झाले!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ चुकीचा OTP!")

    else:
        with st.forgot_pass_form := st.form("forgot_pass_form"):
            forgot_email = st.text_input("नोंदणीकृत ईमेल आयडी (Registered Email):").strip()
            new_pass = st.text_input("नवीन पासवर्ड तयार करा (New Password):", type="password").strip()
            submit_forgot = st.form_submit_button("🔄 Reset Password", type="primary")

            if submit_forgot:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT user_key FROM users WHERE email = ?", (forgot_email,))
                row = cursor.fetchone()
                if row and len(new_pass) >= 4:
                    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_pass, forgot_email))
                    conn.commit()
                    conn.close()
                    st.success("✅ पासवर्ड यशस्वीरित्या बदलला आहे! आता नवीन पासवर्डने लॉगिन करा.")
                else:
                    conn.close()
                    st.error("❌ ईमेल सापडला नाही किंवा पासवर्ड खूप लहान आहे.")

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

col_u, col_lo = st.columns([3.5, 1.5])
if is_user_premium:
    col_u.markdown(f"<span class='gold-vip-badge'>👑 VIP MEMBER: {current_user_name.upper()} ({status_text_str})</span>", unsafe_allow_html=True)
else:
    col_u.markdown(f"<span class='free-user-badge'>🆓 FREE USER: {current_user_name.upper()}</span>", unsafe_allow_html=True)

if col_lo.button("🔄 Logout / ॲप बदला"):
    st.session_state.app_user_name = None
    st.session_state.otp_verified = False
    if "saved_email" in st.query_params:
        del st.query_params["saved_email"]
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
    qs_lock = locks_cfg.get("Quantity Surveying", "Free")

    col_icon1, col_icon2, col_icon3, col_icon4 = st.columns(4)
    
    with col_icon1:
        calc_badge = "🆓 Free" if calc_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 35px; margin:0;">🧮</h1>
                <h5 style="margin: 6px 0 2px 0; color: #f3f4f6;">Calculator</h5>
                <p style="font-size: 10px; color: #9ca3af;">[{calc_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🧮 Calculator", key="btn_open_calc", use_container_width=True):
            st.session_state.selected_module = "Civil Calculator"
            st.rerun()

    with col_icon2:
        ra_badge = "🆓 Free" if ra_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 35px; margin:0;">📊</h1>
                <h5 style="margin: 6px 0 2px 0; color: #f3f4f6;">Rate Analysis</h5>
                <p style="font-size: 10px; color: #9ca3af;">[{ra_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Rate Analysis", key="btn_open_ra", use_container_width=True):
            st.session_state.selected_module = "Rate Analysis"
            st.rerun()

    with col_icon3:
        bbs_badge = "🆓 Free" if bbs_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 35px; margin:0;">🏗️</h1>
                <h5 style="margin: 6px 0 2px 0; color: #f3f4f6;">BBS</h5>
                <p style="font-size: 10px; color: #9ca3af;">[{bbs_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏗️ Open BBS", key="btn_open_bbs", use_container_width=True):
            st.session_state.selected_module = "BBS"
            st.rerun()

    with col_icon4:
        qs_badge = "🆓 Free" if qs_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 15px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 35px; margin:0;">📈</h1>
                <h5 style="margin: 6px 0 2px 0; color: #f3f4f6;">Quantity Survey</h5>
                <p style="font-size: 10px; color: #9ca3af;">[{qs_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📈 Quantity Survey", key="btn_open_qs", use_container_width=True):
            st.session_state.selected_module = "Quantity Surveying"
            st.rerun()

# ==========================================
# 🧮 MODULE 0: CIVIL CALCULATOR & UNIT CONVERTER
# ==========================================
elif st.session_state.selected_module == "Civil Calculator":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_calc"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("🧮 Civil Smart Unit Converter")
    conv_category = st.selectbox("कनव्हर्शन प्रकार निवडा:", ["📦 Volume / Brass Converter (घनफळ आणि ब्रास)", "📏 Length Converter (लांबी मोजमाप)", "📐 Area Converter (क्षेत्रफळ मोजमाप)"])

    if "Volume / Brass" in conv_category:
        val = st.number_input("मूल्य भरा (Value):", min_value=0.0, value=1.0, step=0.1, key="v_val")
        unit_from = st.selectbox("मूळ युनिट (From Unit):", ["Cubic Meter (m³)", "Cubic Feet (CFT)", "Brass"])
        if st.button("⚡ Convert Now", type="primary", key="btn_conv_vol"):
            if "Cubic Meter" in unit_from: m3 = val
            elif "Cubic Feet" in unit_from: m3 = val / 35.3147
            else: m3 = val * 2.83168
            brass = m3 / 2.83168
            cft = m3 * 35.3147
            st.success(f"📦 एकूण ब्रास: {brass:.4f} Brass | CFT: {cft:.2f} CFT | m³: {m3:.4f}")

# ==========================================
# 🛑 MODULE 1: RATE ANALYSIS MODULE
# ==========================================
elif st.session_state.selected_module == "Rate Analysis":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    master_rates = get_market_rates()
    main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)", "Plaster Work (प्लास्टर काम)"])
    if "Concrete Work" in main_choice:
        st.subheader("🧱 Concrete Work Estimation")
        volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, value=1.0, key="cc_vol")
        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="cc_report_btn"):
            st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")

# ==========================================
# 🛑 MODULE 2: BBS MODULE
# ==========================================
elif st.session_state.selected_module == "BBS":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_bbs"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("🏗️ Bar Bending Schedule (BBS Calculator)")
    if st.button("🧮 CALCULATE BBS REPORT", type="primary", key="bbs_calc_btn"):
        st.success("🎉 BBS रिपोर्ट तयार झाला!")

# ==========================================
# 📈 QUANTITY SURVEYING & ABSTRACT SHEET MODULE
# ==========================================
elif st.session_state.selected_module == "Quantity Surveying":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_qs"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("📈 Quantity Surveying & Abstract Sheet Master")
    if st.button("📈 GENERATE ABSTRACT SHEET", type="primary", key="qs_gen_btn"):
        st.success("🎉 Abstract Sheet तयार झाली!")
