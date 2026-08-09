# ==========================================
# 📦 PATIL INFRATECH (SQLite Database & Streamlit Web Application)
# ==========================================
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
import os
import random
import re
import smtplib
import string
import time
import urllib.parse
import pandas as pd
import streamlit as st

# Official Google GenAI SDK Import
try:
    from google import genai

    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 🚨 Streamlit नियम: set_page_config नेहमी सर्वात आधी असावे!
st.set_page_config(
    page_title="PATIL INFRATECH", page_icon="🏗️", layout="centered"
)

# ==========================================
# 📱 MOBILE NATIVE BACK BUTTON INTERCEPTOR (JS ENGINE)
# ==========================================
st.markdown(
    """
    <script>
    window.onpopstate = function(event) {
        const backButtons = Array.from(window.parent.document.querySelectorAll("button"));
        const mainBackButton = backButtons.find(btn => 
            btn.innerText.includes("मुख्य मेनूवर जा") || 
            btn.innerText.includes("Back to Main") ||
            btn.innerText.includes("Back to All Users List") ||
            btn.innerText.includes("Back to Site Manager Menu") ||
            btn.innerText.includes("Back to Estimator Menu")
        );
        if (mainBackButton) {
            mainBackButton.click();
        }
    };
    </script>
""",
    unsafe_allow_html=True,
)


def trigger_push_state():
    st.markdown(
        "<script>window.history.pushState({inSubModule: true}, '');</script>",
        unsafe_allow_html=True,
    )


def get_ist_time():
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    return ist_now


# ==========================================
# 🌐 HAVERSINE FORMULA (DISTANCE IN METERS)
# ==========================================
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ==========================================
# 📧 EMAIL OTP FUNCTION
# ==========================================
def send_email_message(receiver_email, subject, body_text):
    sender_email = (
        st.secrets.get("EMAIL_USER", "your_email@gmail.com")
        if hasattr(st, "secrets")
        else "your_email@gmail.com"
    )
    sender_password = (
        st.secrets.get("EMAIL_PASS", "your_gmail_app_password")
        if hasattr(st, "secrets")
        else "your_gmail_app_password"
    )

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(body_text, "plain")
    message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception:
        return False


def is_strong_password(password):
    if len(password) < 8:
        return False, "पासवर्ड कमीत कमी ८ अक्षरांचा असावा."
    if not re.search(r"\d", password):
        return False, "पासवर्डमध्ये कमीत कमी एक नंबर (0-9) असावा."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "पासवर्डमध्ये कमीत कमी एक विशेष चिन्ह (!@#$%^&*) असावे."
    return True, "Strong"


# ==========================================
# 🗄️ SQLITE DATABASE MANAGEMENT
# ==========================================
DB_FILE = "patil_infratech.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def auto_cleanup_30day_attendance():
    """३० दिवसांपेक्षा जुना हजेरीचा डेटा डेटाबेसवरून ऑटो-डिलीट करणारी स्क्रिप्ट"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cutoff_date = (get_ist_time() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        cursor.execute("DELETE FROM labor_attendance_records WHERE date < ?", (cutoff_date,))
        conn.commit()
        conn.close()
    except Exception:
        pass


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_key TEXT PRIMARY KEY,
            id TEXT,
            uid TEXT UNIQUE,
            pin TEXT,
            mobile TEXT,
            email TEXT,
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
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            timestamp TEXT,
            user_note TEXT,
            report_data TEXT,
            FOREIGN KEY (user_key) REFERENCES users (user_key)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS premium_codes (
            code TEXT PRIMARY KEY,
            assigned_to TEXT,
            used INTEGER,
            used_by TEXT,
            used_date TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feature_locks (
            feature_name TEXT PRIMARY KEY,
            access_level TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_rates (
            material TEXT PRIMARY KEY,
            rate REAL
        )
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            masons INTEGER DEFAULT 0,
            mason_rate REAL DEFAULT 0.0,
            labors INTEGER DEFAULT 0,
            labor_rate REAL DEFAULT 0.0,
            fitters INTEGER DEFAULT 0,
            fitter_rate REAL DEFAULT 0.0,
            supervisor INTEGER DEFAULT 0,
            supervisor_rate REAL DEFAULT 0.0,
            carpenter INTEGER DEFAULT 0,
            carpenter_rate REAL DEFAULT 0.0,
            plumber INTEGER DEFAULT 0,
            plumber_rate REAL DEFAULT 0.0,
            electrician INTEGER DEFAULT 0,
            electrician_rate REAL DEFAULT 0.0,
            painter INTEGER DEFAULT 0,
            painter_rate REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            material_name TEXT,
            transaction_type TEXT,
            quantity INTEGER,
            unit TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            stage_name TEXT,
            progress_percent INTEGER,
            remark TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pre_concreting_checklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            item_text TEXT,
            is_checked INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS labor_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            labor_name TEXT,
            mobile TEXT UNIQUE,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_geo_config (
            user_key TEXT PRIMARY KEY,
            site_name TEXT,
            latitude REAL,
            longitude REAL,
            radius_meters REAL DEFAULT 100.0,
            updated_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_tokens (
            token TEXT PRIMARY KEY,
            user_key TEXT,
            type TEXT,
            date TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS labor_attendance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            labor_mobile TEXT,
            labor_name TEXT,
            date TEXT,
            entry_type TEXT,
            timestamp TEXT,
            distance_m REAL,
            selfie_status TEXT
        )
    """)

    cursor.execute("SELECT * FROM users WHERE user_key = ?", ("9999999999",))
    if not cursor.fetchone():
        cursor.execute(
            """
            INSERT INTO users (user_key, id, uid, pin, mobile, email, password, comment, admin_message, unread_notification, is_premium, premium_expiry, requested_code, seen_popup, master_code_uses, last_active, activated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                "9999999999",
                "kanha",
                "KANHA_1P",
                "1234",
                "9999999999",
                "admin@patilinfratech.com",
                "patiladmin123",
                "मास्टर ॲडमीन अकाउंट",
                "स्वागत आहे मास्टर कन्हैया! आपले पाटील इन्फ्राटेक मध्ये सर्व अधिकार अनलॉक्ड आहेत ⚡",
                0,
                1,
                "2099-12-31 23:59:59",
                0,
                1,
                0,
                get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                "Master Admin",
            ),
        )

    default_locks = {
        "Civil Calculator": "Free",
        "Rate Analysis": "Free",
        "BBS": "Free",
        "Quantity Surveying": "Free",
        "Site Manager": "Free",
        "WhatsApp Share": "Premium",
        "Civil AI Assistant": "Premium",
        "Labor Geo-Attendance": "Free",
    }
    for f_name, f_lvl in default_locks.items():
        cursor.execute(
            "INSERT OR IGNORE INTO feature_locks (feature_name, access_level) VALUES (?, ?)",
            (f_name, f_lvl),
        )

    default_rates = {
        "cement": 400.0,
        "sand": 2500.0,
        "bricks": 8.0,
        "aggregate": 2200.0,
        "steel": 60.0,
    }
    for mat, rat in default_rates.items():
        cursor.execute(
            "INSERT OR IGNORE INTO market_rates (material, rate) VALUES (?, ?)",
            (mat, rat),
        )

    conn.commit()
    conn.close()


init_db()
auto_cleanup_30day_attendance()


def get_user_data(user_key):
    if not user_key:
        return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_key = ?", (user_key,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


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


if "app_user_name" not in st.session_state:
    st.session_state.app_user_name = None

query_params = st.query_params

if st.session_state.app_user_name is None and "saved_user" in query_params:
    saved_key = query_params["saved_user"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_key FROM users WHERE user_key = ?", (saved_key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        st.session_state.app_user_name = row["user_key"]

if "pending_email" not in st.session_state:
    st.session_state.pending_email = None
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False
if "is_admin_logged" not in st.session_state:
    st.session_state.is_admin_logged = False
if "admin_dashboard_tab" not in st.session_state:
    st.session_state.admin_dashboard_tab = "rates"
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "selected_site_sub_module" not in st.session_state:
    st.session_state.selected_site_sub_module = None
if "selected_estimator_sub_module" not in st.session_state:
    st.session_state.selected_estimator_sub_module = None
if "admin_view" not in st.session_state:
    st.session_state.admin_view = "main"
if "admin_selected_user" not in st.session_state:
    st.session_state.admin_selected_user = None

current_user_name = st.session_state.app_user_name

if current_user_name:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_active = ? WHERE user_key = ?",
        (get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), current_user_name),
    )
    conn.commit()
    conn.close()


def check_user_premium_status(username):
    if not username:
        return False, "Free"
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
            except Exception:
                pass
        return True, "Active"
    return False, "Free"


is_curr_premium, _ = check_user_premium_status(current_user_name)

if is_curr_premium:
    bg_gradient = "radial-gradient(circle at 50% -20%, #2a0845 0%, #03001e 50%, #050014 100%)"
    accent_border = "#ec38bc"
    card_bg = "rgba(20, 10, 38, 0.9)"
    header_gradient = "linear-gradient(135deg, #050014 0%, #7303c0 50%, #ec38bc 100%)"
    box_inner_shadow = "inset 0 0 15px rgba(236, 56, 188, 0.25)"
    primary_btn_bg = "linear-gradient(135deg, #7303c0 0%, #ec38bc 100%)"
    primary_btn_shadow = "rgba(236, 56, 188, 0.5)"
    box_bg_color = "#140a28"
else:
    bg_gradient = "linear-gradient(135deg, #030712 0%, #0b0f19 50%, #020617 100%)"
    accent_border = "#00f2fe"
    card_bg = "#0b121e"
    header_gradient = "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)"
    box_inner_shadow = "inset 0 2px 8px rgba(0, 0, 0, 0.9)"
    primary_btn_bg = "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)"
    primary_btn_shadow = "rgba(2, 132, 199, 0.4)"
    box_bg_color = "#111827"

st.markdown(
    f"""
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

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background-color: #030712 !important;
        background: {bg_gradient} !important;
        color: #f8fafc !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    p, span, h1, h2, h3, h4, h5, h6, li, small, label, div {{
        color: #f8fafc !important;
    }}

    div[data-baseweb="input"], div[data-baseweb="input"] *, div[data-baseweb="base-input"], div[data-baseweb="base-input"] *,
    div[data-testid="stNumberInputContainer"], div[data-testid="stNumberInputContainer"] *, div[data-testid="stTextInput"], div[data-testid="stTextInput"] * {{
        background-color: {box_bg_color} !important;
        background: {box_bg_color} !important;
        color: #ffffff !important;
    }}

    div[data-baseweb="input"] > div, div[data-baseweb="base-input"], div[data-testid="stNumberInputContainer"], input, select, textarea {{
        border: 1px solid {accent_border} !important;
        border-radius: 14px !important;
        outline: none !important;
        font-weight: 500 !important;
        box-shadow: {box_inner_shadow} !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: {primary_btn_bg} !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 6px 20px {primary_btn_shadow} !important;
        width: 100%;
        transition: all 0.3s ease;
    }}

    div.stButton > button {{
        color: #f8fafc !important;
        background: {card_bg} !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
    }}

    .main-header {{
        background: {header_gradient};
        padding: 25px 15px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7);
        margin-bottom: 22px;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }}

    .gold-vip-badge {{
        background: linear-gradient(135deg, #7303c0 0%, #ec38bc 100%);
        color: #ffffff !important;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 14px;
        display: inline-block;
        border: 1px solid #f472b6;
    }}
    </style>
""",
    unsafe_allow_html=True,
)


def generate_random_code():
    return "PATIL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


# Header Banner
st.markdown(
    """
    <div class="main-header">
        <h1 style='color: white; margin:0; font-size: 28px; font-weight: 800;'>🏗️ PATIL INFRATECH</h1>
        <p style='color: #e0f2fe; margin:5px 0 0 0; font-size: 15px;'>📐 Quantity Surveyor & Site Geo-Attendance Platform</p>
        <small style='color: #bae6fd;'>Concept & Logic by: Kanhaiya (Founder of Patil Infratech)</small>
    </div>
""",
    unsafe_allow_html=True,
)

# LOGIN CHECK
if st.session_state.app_user_name is None and not st.session_state.is_admin_logged:
    st.markdown("### 🏗️ PATIL INFRATECH - SECURE LOGIN")

    login_tab, otp_tab, labor_portal_tab = st.tabs([
        "🔑 Engineer Login",
        "📧 Register via Email OTP",
        "👷‍♂️ Labor Live Attendance Portal",
    ])

    with login_tab:
        with st.form("direct_login_form"):
            login_email = st.text_input("ईमेल किंवा Username:").strip()
            login_pass = st.text_input("पासवर्ड (Password):", type="password").strip()
            submit_direct = st.form_submit_button("🚀 Login Now", type="primary")

            if submit_direct:
                if login_email and login_pass:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT user_key FROM users WHERE (email = ? OR uid = ? OR user_key = ?) AND pin = ?",
                        (login_email, login_email, login_email, login_pass),
                    )
                    row = cursor.fetchone()
                    conn.close()

                    if row:
                        st.session_state.app_user_name = row["user_key"]
                        st.query_params["saved_user"] = row["user_key"]
                        st.success("🎉 यशस्वीरित्या लॉगिन झाले!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा ईमेल/Username किंवा पासवर्ड!")

    with otp_tab:
        st.markdown("#### 📧 Email OTP Verification")
        email_input = st.text_input("तुमचा ईमेल आयडी टाका:").strip()

        if not st.session_state.otp_verified:
            if st.button("📤 Send OTP to Email", type="primary"):
                if email_input and "@" in email_input:
                    generated_otp = "".join(random.choices(string.digits, k=6))
                    st.session_state.generated_otp = generated_otp
                    st.session_state.pending_email = email_input
                    send_email_message(email_input, "PATIL INFRATECH - Verification OTP", f"OTP: {generated_otp}")
                    st.success("✅ ईमेलवर 6 अंकी OTP पाठवला आहे!")

            if st.session_state.generated_otp:
                entered_otp = st.text_input("6 अंकी OTP टाका:", max_chars=6).strip()
                if st.button("🔐 Verify OTP"):
                    if entered_otp == st.session_state.generated_otp:
                        st.session_state.otp_verified = True
                        st.success("✅ OTP व्हेरिफाय झाला!")
                        st.rerun()

    # ==========================================
    # 👷‍♂️ IN-APP DIRECT LABOR ATTENDANCE PORTAL
    # ==========================================
    with labor_portal_tab:
        st.markdown("#### 👷‍♂️ पाटील इन्फ्राटेक - मजूर थेट हजेरी पोर्टल")
        st.caption("💡 इंजिनिअरने दिलेला टोकन कोड (उदा. IN-XXXX किंवा OUT-XXXX) खाली टाका:")

        token_input = st.text_input("Enter Attendance Token Code:", placeholder="e.g. IN-AB12CD34").strip().upper()

        if token_input:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance_tokens WHERE token = ?", (token_input,))
            tok_row = cursor.fetchone()

            if not tok_row:
                st.error("❌ हा टोकन कोड चुकीचा आहे किंवा एक्सपायर झाला आहे!")
            else:
                tok_info = dict(tok_row)
                eng_key = tok_info["user_key"]
                att_type = tok_info["type"]

                cursor.execute("SELECT * FROM site_geo_config WHERE user_key = ?", (eng_key,))
                geo_row = cursor.fetchone()

                if not geo_row:
                    st.error("⚠️ इंजिनिअरने अजून साईट जीपीएस लोकेशन सेट केले नाही!")
                else:
                    geo_info = dict(geo_row)
                    target_lat = geo_info["latitude"]
                    target_lon = geo_info["longitude"]
                    allowed_radius = geo_info["radius_meters"]

                    st.info(f"🏗️ **Site:** {geo_info['site_name']} | **Entry:** `{att_type}` | **Max Radius:** `{allowed_radius}m`")

                    cursor.execute("SELECT * FROM labor_master WHERE user_key = ?", (eng_key,))
                    labors_list = cursor.fetchall()

                    if not labors_list:
                        st.error("⚠️ मास्टर लेबर एंट्री सापडली नाही.")
                    else:
                        labor_options = {f"{l['labor_name']} ({l['mobile']})": l["mobile"] for l in labors_list}
                        selected_labor_str = st.selectbox("तुमचे नाव निवडा:", list(labor_options.keys()))
                        sel_labor_mob = labor_options[selected_labor_str]
                        sel_labor_name = selected_labor_str.split(" (")[0]

                        st.markdown("##### 📍 १. तुमचे लाईव्ह लोकेशन व्हॅरिफाय करा:")

                        # HTML5 Native High Accuracy GPS Fetcher
                        st.components.v1.html(
                            """
                            <script>
                            function getLocation() {
                                if (navigator.geolocation) {
                                    navigator.geolocation.getCurrentPosition(showPosition, showError, {
                                        enableHighAccuracy: true,
                                        timeout: 10000,
                                        maximumAge: 0
                                    });
                                } else {
                                    alert("Geolocation is not supported by this browser.");
                                }
                            }
                            function showPosition(position) {
                                const lat = position.coords.latitude;
                                const lon = position.coords.longitude;
                                const urlParams = new URLSearchParams(window.location.search);
                                urlParams.set('labor_lat', lat);
                                urlParams.set('labor_lon', lon);
                                window.parent.location.search = urlParams.toString();
                            }
                            function showError(error) {
                                alert("GPS Error: " + error.message);
                            }
                            </script>
                            <button onclick="getLocation()" style="width:100%; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color:#030712; padding:14px; font-weight:bold; border-radius:12px; border:none; cursor:pointer; font-size:16px;">
                                🎯 Capture My Live GPS Location
                            </button>
                        """,
                            height=70,
                        )

                        l_lat = st.query_params.get("labor_lat", None)
                        l_lon = st.query_params.get("labor_lon", None)

                        if l_lat and l_lon:
                            dist = calculate_haversine_distance(float(l_lat), float(l_lon), target_lat, target_lon)
                            st.write(f"📏 **साईटपासून तुमचे अंतर:** `{dist:.1f} मीटर`")

                            if dist > allowed_radius:
                                st.error(f"⚠️ तुम्ही साईटच्या {allowed_radius:.0f}m परिघाबाहेर आहात! हजेरी ब्लॉक केली आहे.")
                            else:
                                st.success("✅ लोकेशन व्हॅरिफाय झाले! आता फोटो काढा:")
                                selfie_img = st.camera_input("Take Live Selfie")

                                if selfie_img:
                                    if st.button("🚀 Mark Attendance Now", type="primary"):
                                        today_date = get_ist_time().strftime("%Y-%m-%d")
                                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                                        cursor.execute(
                                            """
                                            INSERT INTO labor_attendance_records 
                                            (user_key, labor_mobile, labor_name, date, entry_type, timestamp, distance_m, selfie_status)
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                        """,
                                            (eng_key, sel_labor_mob, sel_labor_name, today_date, att_type, now_str, dist, "Verified Selfie"),
                                        )
                                        conn.commit()
                                        st.balloons()
                                        st.success(f"🎉 {sel_labor_name}! तुमची {att_type} हजेरी सेव्ह झाली आहे.")
            conn.close()

    st.stop()

# ==========================================
# 🚀 MAIN DASHBOARD (ENGINEER LOGGED IN)
# ==========================================
current_user_name = st.session_state.app_user_name
locks_cfg = get_feature_locks()

col_u, col_lo = st.columns([3.5, 1.5])
col_u.markdown(f"<span class='gold-vip-badge'>👷 ENGINEEER: {current_user_name.upper()}</span>", unsafe_allow_html=True)

if col_lo.button("🔄 Logout"):
    st.session_state.app_user_name = None
    if "saved_user" in st.query_params:
        del st.query_params["saved_user"]
    st.session_state.selected_module = None
    st.rerun()

st.write("---")

if st.session_state.selected_module is None:
    st.markdown("### 🚀 तुम्हाला काय करायचे आहे ते निवडा:")

    main_col1, main_col2 = st.columns(2)

    with main_col1:
        st.markdown("#### 👷‍♂️ 1. Site Manager")
        st.markdown(
            """
            <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3); margin-bottom: 12px;">
                <h1 style="font-size: 32px; margin:0;">👷‍♂️</h1>
                <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Site Manager</h5>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("👷‍♂️ Open Site Manager", key="btn_open_site", use_container_width=True):
            st.session_state.selected_module = "Site Manager"
            trigger_push_state()
            st.rerun()

    with main_col2:
        st.markdown("#### 📐 2. Estimator Tools")
        st.markdown(
            """
            <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3); margin-bottom: 12px;">
                <h1 style="font-size: 32px; margin:0;">🧮</h1>
                <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Estimator Tools</h5>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("📐 Open Estimator Tools", key="btn_open_estimator", use_container_width=True):
            st.session_state.selected_module = "Estimator Tools"
            trigger_push_state()
            st.rerun()

    st.write("---")
    st.markdown("#### 🌐 3. Other Features (Labor Geo-Attendance Engine)")
    st.markdown(
        """
        <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(236, 56, 188, 0.4); margin-bottom: 12px;">
            <h1 style="font-size: 32px; margin:0;">📍</h1>
            <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:14px;">Labor Geo-Fence Attendance Engine</h5>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🌐 Open Labor Geo-Attendance System", key="btn_open_geo_att", use_container_width=True):
        st.session_state.selected_module = "Labor Geo-Attendance"
        trigger_push_state()
        st.rerun()

# ==========================================
# 🌐 MODULE: LABOR GEO-ATTENDANCE SYSTEM
# ==========================================
elif st.session_state.selected_module == "Labor Geo-Attendance":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_geo_main"):
        st.session_state.selected_module = None
        st.rerun()

    st.write("---")
    st.subheader("📍 Labor Geo-Fence & Token Control Center")

    geo_tab1, geo_tab2, geo_tab3, geo_tab4 = st.tabs([
        "१. Register Labor Master",
        "२. Set Site GPS Geo-Fence",
        "३. Dynamic Token Generator",
        "४. Tamper-Proof Attendance Logs",
    ])

    with geo_tab1:
        st.markdown("#### 👥 कायमस्वरूपी कामगारांची नावे (Labor Master Entry)")

        with st.form("add_labor_form"):
            l_name = st.text_input("कामगाराचे पूर्ण नाव:").strip()
            l_mob = st.text_input("मोबाईल नंबर (10 Digits):", max_chars=10).strip()
            sub_l = st.form_submit_button("➕ Register Labor", type="primary")

            if sub_l:
                if l_name and len(l_mob) == 10 and l_mob.isdigit():
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO labor_master (user_key, labor_name, mobile, created_at) VALUES (?, ?, ?, ?)",
                            (current_user_name, l_name, l_mob, get_ist_time().strftime("%Y-%m-%d %H:%M:%S")),
                        )
                        conn.commit()
                        conn.close()
                        st.success(f"✅ मजूर '{l_name}' सेव्ह झाला!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ हा मोबाईल नंबर आधीच रजिस्टर आहे!")

    with geo_tab2:
        st.markdown("#### 📍 साईट जीपीएस लोकेशन आणि Geo-Fence सेटिंग")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM site_geo_config WHERE user_key = ?", (current_user_name,))
        curr_geo = cursor.fetchone()
        conn.close()

        curr_geo_dict = dict(curr_geo) if curr_geo else {}

        site_name_val = st.text_input("साईटीचे नाव:", value=curr_geo_dict.get("site_name", "Main Site"))
        radius_val = st.number_input("परिघ (Radius in Meters):", min_value=10.0, value=float(curr_geo_dict.get("radius_meters", 100.0)))

        # Fixed Engineer GPS Fetcher
        st.components.v1.html(
            """
            <script>
            function getEngineerLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showEngPosition, showEngError, {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    });
                } else {
                    alert("Geolocation is not supported.");
                }
            }
            function showEngPosition(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('eng_lat', lat);
                urlParams.set('eng_lon', lon);
                window.parent.location.search = urlParams.toString();
            }
            function showEngError(error) {
                alert("GPS Error: " + error.message);
            }
            </script>
            <button onclick="getEngineerLocation()" style="width:100%; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color:#030712; padding:14px; font-weight:bold; border-radius:12px; border:none; cursor:pointer; font-size:16px;">
                🎯 Capture Current Site GPS Location
            </button>
        """,
            height=70,
        )

        eng_lat = st.query_params.get("eng_lat", curr_geo_dict.get("latitude", 0.0))
        eng_lon = st.query_params.get("eng_lon", curr_geo_dict.get("longitude", 0.0))

        st.write(f"📍 **Captured Location:** Latitude: `{eng_lat}` | Longitude: `{eng_lon}`")

        if st.button("💾 Save Site Geo-Fence Settings", type="primary"):
            if float(eng_lat) != 0.0 and float(eng_lon) != 0.0:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    REPLACE INTO site_geo_config (user_key, site_name, latitude, longitude, radius_meters, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (current_user_name, site_name_val, float(eng_lat), float(eng_lon), radius_val, get_ist_time().strftime("%Y-%m-%d %H:%M:%S")),
                )
                conn.commit()
                conn.close()
                st.success("✅ साईटचे जीपीएस लोकेशन सेव्ह झाले!")
            else:
                st.error("❌ कृपया वरील बटणावर क्लिक करून लोकेशन मिळवा!")

    with geo_tab3:
        st.markdown("#### 🔗 Dynamic Token Generator (IN / OUT Tokens)")

        if st.button("🚀 Generate Today's Tokens", type="primary"):
            today_date_str = get_ist_time().strftime("%Y-%m-%d")
            in_token = "IN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            out_token = "OUT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

            conn = get_db_connection()
            cursor = conn.cursor()
            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("INSERT INTO attendance_tokens (token, user_key, type, date, created_at) VALUES (?, ?, 'IN', ?, ?)", (in_token, current_user_name, today_date_str, now_str))
            cursor.execute("INSERT INTO attendance_tokens (token, user_key, type, date, created_at) VALUES (?, ?, 'OUT', ?, ?)", (out_token, current_user_name, today_date_str, now_str))
            conn.commit()
            conn.close()
            st.success("🎉 आजचे टोकन्स तयार झाले!")

        conn = get_db_connection()
        cursor = conn.cursor()
        today_date_str = get_ist_time().strftime("%Y-%m-%d")
        cursor.execute("SELECT * FROM attendance_tokens WHERE user_key = ? AND date = ? ORDER BY rowid DESC LIMIT 2", (current_user_name, today_date_str))
        toks = cursor.fetchall()
        conn.close()

        if toks:
            for t in toks:
                st.markdown(f"##### 🟢 Today's {t['type']} Token Code: `{t['token']}`")
                wa_msg = f"🏗️ *PATIL INFRATECH ATTENDANCE CODE ({t['type']})*\n🔑 Code: *{t['token']}*\nॲप उघडून 'Labor Live Attendance Portal' मध्ये हा कोड टाका."
                enc_msg = urllib.parse.quote(wa_msg)
                st.markdown(f"<a href='https://wa.me/?text={enc_msg}' target='_blank'><button style='background:#25D366; color:white; border:none; padding:8px 16px; border-radius:10px; font-weight:bold;'>📱 Share Code on WhatsApp</button></a>", unsafe_allow_html=True)

    with geo_tab4:
        st.markdown("#### 🔒 Live Attendance Logs (Tamper-Proof)")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM labor_attendance_records WHERE user_key = ? ORDER BY id DESC", (current_user_name,))
        logs = cursor.fetchall()
        conn.close()

        if logs:
            log_df = pd.DataFrame([dict(r) for r in logs])
            st.dataframe(log_df[["date", "labor_name", "labor_mobile", "entry_type", "timestamp", "distance_m", "selfie_status"]], use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ आज अजून एकही हजेरी लागलेली नाही.")
