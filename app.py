# ==============================================================================
# 📦 PATIL INFRATECH - CIVIL ENGINEERING SUITE & SITE MANAGEMENT SYSTEM
# ==============================================================================
# Concept & Logic: Kanhaiya (Founder of Patil Infratech)
# Architecture: Streamlit Web UI + SQLite3 + Gemini GenAI SDK
# ==============================================================================
#
# 📑 अनुक्रमणिका व विभाग नकाशा (TABLE OF CONTENTS / INDEX):
# ------------------------------------------------------------------------------
# 📌 विभाग १  : आवश्यक लायब्ररी आणि पॅकेजेस इम्पोर्ट
# 📌 विभाग २  : STREAMLIT पेज कॉन्फिगरेशन (Must be first Streamlit command)
# 📌 विभाग ३  : ब्राउझर लोकल स्टोरेज आणि मोबाईल बॅक बटन हँडलर
# 📌 विभाग ४  : युटिलिटी आणि सपोर्ट फंक्शन्स (वेळ, ईमेल OTP, पासवर्ड सुरक्षा, SMTP Mailer)
# 📌 विभाग ५  : SQLITE डेटाबेस मॅनेजमेंट आणि मॉडेल्स (Tables Creation & Init DB)
# 📌 विभाग ६  : डेटाबेस क्वेरी आणि हेल्पर फंक्शन्स (Default Tasks & Rates)
# 📌 विभाग ७  : सेशन स्टेट्स आणि प्रिमियम ऑथेंटिकेशन व्यवस्था
# 📌 विभाग ८  : BRANDED CONSTRUCTION THEME CSS
# 📌 विभाग ९  : WHATSAPP रिपोर्ट शेअरिंग कंपोनंट (Safe Dynamic Key Protection)
# 📌 विभाग १० : वेलकम स्क्रीन ॲनिमेशन (3D Cosmic Loader & Sponsor Ads)
# 📌 विभाग ११ : ॲडमीन पॅनल (Admin Command Center)
# 📌 विभाग १२ : युझर ऑथेंटिकेशन (Login, Register & Email OTP)
# 📌 विभाग १३ : मुख्य युझर डॅशबोर्ड (Top Header, Ads, Notifications & Site Switcher)
# 📌 विभाग १४ : CIVIL AI ASSISTANT (Gemini SDK & Expert Knowledge Fallback)
# 📌 विभाग १५ : मुख्य मॉड्यूल निवड कार्ड्स (Site Manager vs Estimator Tools vs NeevPay)
# 📌 विभाग १६ : ESTIMATOR TOOLS मुख्य मॉड्यूल (Sub-modules)
# 📌 विभाग १७ : SITE MANAGER मुख्य मॉड्यूल (Sub-modules)
# 📌 विभाग १८ : NEEVPAY / SITESETU मुख्य मॉड्यूल (Milestone Escrow & Payment Protection)
# ==============================================================================

# ==============================================================================
# 📦 PATIL INFRATECH - CIVIL ENGINEERING SUITE & SITE MANAGEMENT SYSTEM
# ==============================================================================
# Architecture: Streamlit Modern UI + SQLite3 + Gemini GenAI SDK
# ==============================================================================

# ==========================================
# 📌 विभाग १: आवश्यक लायब्ररी आणि पॅकेजेस इम्पोर्ट
# ==========================================
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
import os
import random
import re
import smtplib
import sqlite3
import string
import time
import urllib.parse
import pandas as pd
import requests
import streamlit as st

# Official Google GenAI SDK Import
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# ==========================================
# 📌 विभाग २: STREAMLIT पेज कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="PATIL INFRATECH | Civil Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# मॉडर्न, सुटसुटीत आणि क्लीन CSS थीम (Zero Fluff, Mobile Responsive)
st.markdown(
    """
    <style>
    /* १. अनावश्यक डीफॉल्ट Streamlit घटक लपवणे */
    #MainMenu, header[data-testid="stHeader"], footer, .stAppHeader, 
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    button[title="Increment"], button[title="Decrement"],
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* २. आधुनिक बॅकग्राउंड व फॉन्ट */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* ३. सुटसुटीत इनपुट बॉक्सेस */
    div[data-baseweb="input"], div[data-baseweb="base-input"],
    div[data-testid="stNumberInputContainer"], div[data-testid="stTextInput"] {
        background-color: #111827 !important;
        border-radius: 8px !important;
    }

    input, select, textarea {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    input:focus, textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 1px #f59e0b !important;
    }

    /* ४. मॉडर्न फ्लॅट बटन्स */
    div.stButton > button {
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
        transform: translateY(-1px);
    }
    div.stButton > button[kind="primary"] {
        background: #f59e0b !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #d97706 !important;
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 📌 विभाग ३: ब्राउझर लोकल स्टोरेज आणि मोबाईल बॅक बटन हँडलर
# ==========================================
st.markdown(
    """
    <script>
    // मोबाईलचा बॅक बटन दाबताच ट्रिगर होणारा इव्हेंट
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

    // लोकल स्टोरेजमधून ऑटो लॉगिन डेटा रिकव्हर करणे
    const savedUser = localStorage.getItem("patil_app_user");
    const urlParams = new URLSearchParams(window.location.search);
    if (savedUser && !urlParams.has("saved_user")) {
        urlParams.set("saved_user", savedUser);
        window.location.search = urlParams.toString();
    }
    </script>
    """,
    unsafe_allow_html=True,
)

def trigger_push_state():
    """सब-मॉड्यूल नेव्हिगेशनसाठी ब्राउझर हिस्ट्रीमध्ये पुश स्टेट करणे"""
    st.markdown(
        "<script>window.history.pushState({inSubModule: true}, '');</script>",
        unsafe_allow_html=True,
    )

# ==========================================
# 📌 विभाग ४: युटिलिटी आणि सपोर्ट फंक्शन्स
# ==========================================
def get_ist_time():
    """भारतीय प्रमाणवेळ (IST) मिळवणे"""
    utc_now = datetime.datetime.utcnow()
    return utc_now + datetime.timedelta(hours=5, minutes=30)

def generate_random_code():
    """प्रिमियम कोड जनरेटर"""
    return "PATIL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

def send_email_message(receiver_email, subject, body_text):
    """ईमेल पाठवण्याचे मुख्य फंक्शन"""
    sender_email = (
        st.secrets.get("EMAIL_USER", "your_email@gmail.com")
        if hasattr(st, "secrets") and "EMAIL_USER" in st.secrets
        else "your_email@gmail.com"
    )
    sender_password = (
        st.secrets.get("EMAIL_PASS", "your_gmail_app_password")
        if hasattr(st, "secrets") and "EMAIL_PASS" in st.secrets
        else "your_gmail_app_password"
    )

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(body_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception:
        return False

def send_live_otp_email(to_email, otp_code, purpose="Verification"):
    """NeevPay साठी स्वच्छ व आधुनिक HTML फॉरमॅटमध्ये OTP पाठवणे"""
    sender_email = (
        st.secrets.get("EMAIL_USER", "your_email@gmail.com")
        if hasattr(st, "secrets") and "EMAIL_USER" in st.secrets
        else "your_email@gmail.com"
    )
    sender_password = (
        st.secrets.get("EMAIL_PASS", "your_gmail_app_password")
        if hasattr(st, "secrets") and "EMAIL_PASS" in st.secrets
        else "your_gmail_app_password"
    )

    msg = MIMEMultipart()
    msg['From'] = f"Patil Infratech NeevPay <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = f"🔐 NeevPay Security OTP: {otp_code}"

    html_content = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; border: 1px solid #10b981; border-radius: 12px; max-width: 480px; margin: auto; background-color: #ffffff; color: #0f172a;">
        <h2 style="color: #064e3b; margin-top:0; font-size: 20px;">PATIL INFRATECH • NEEVPAY</h2>
        <p style="font-size: 14px; color: #334155;">प्रिय क्लायंट / घरमालक,</p>
        <p style="font-size: 14px; color: #334155;">तुमच्या साईटच्या <b>{purpose}</b> साठी खालील OTP तयार करण्यात आला आहे:</p>
        <div style="text-align: center; margin: 24px 0;">
            <span style="font-size: 30px; font-weight: 800; letter-spacing: 6px; color: #065f46; background: #ecfdf5; padding: 12px 24px; border-radius: 8px; border: 1px dashed #10b981; display: inline-block;">
                {otp_code}
            </span>
        </div>
        <p style="color: #dc2626; font-size: 12px; margin-bottom: 0;">⚠️ हा OTP अत्यंत गोपनीय आहे. इंजिनिअरशी चर्चा करून संमती असल्यासच शेअर करा.</p>
    </div>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, "Email Sent"
    except Exception as e:
        return False, str(e)

def is_strong_password(password):
    """पासवर्ड तपासणी"""
    if len(password) < 8:
        return False, "पासवर्ड कमीत कमी ८ अक्षरांचा असावा."
    if not re.search(r"\d", password):
        return False, "पासवर्डमध्ये कमीत कमी एक नंबर (0-9) असावा."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "पासवर्डमध्ये कमीत कमी एक विशेष चिन्ह (!@#$%^&*) असावे."
    return True, "Strong"

def get_site_weather_forecast(city_name="Pune"):
    """ओपन-मेटिओ API द्वारे रिअल-टाइम हवामान अंदाज मिळवणे"""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_name)}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=5).json()
        if not geo_res.get("results"):
            return None
        
        loc = geo_res["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        resolved_name = loc.get("name", city_name)
        admin1 = loc.get("admin1", "")

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            "&hourly=precipitation_probability&forecast_days=1&timezone=auto"
        )
        w_res = requests.get(weather_url, timeout=5).json()
        curr = w_res.get("current", {})
        hourly = w_res.get("hourly", {})
        
        rain_probs = hourly.get("precipitation_probability", [0])
        curr_hour = datetime.datetime.now().hour
        rain_prob = rain_probs[curr_hour] if curr_hour < len(rain_probs) else rain_probs[0]
        max_rain_today = max(rain_probs) if rain_probs else rain_prob

        return {
            "city": f"{resolved_name}, {admin1}" if admin1 else resolved_name,
            "temp": curr.get("temperature_2m", "--"),
            "humidity": curr.get("relative_humidity_2m", "--"),
            "wind": curr.get("wind_speed_10m", "--"),
            "rain_prob": rain_prob,
            "max_rain_today": max_rain_today
        }
    except Exception:
        return None

# ==========================================
# 📌 विभाग ५: SQLITE डेटाबेस व्यवस्थापन आणि मॉडेल्स
# ==========================================
DB_FILE = "patil_infratech.db"

def get_db_connection():
    """डेटाबेस कनेक्शन हेल्पर"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """सर्व डेटाबेस टेबल्स तयार करणे आणि सुरक्षित अपग्रेड करणे"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # १. युझर्स टेबल
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

    # २. हिस्ट्री टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            timestamp TEXT,
            user_note TEXT,
            report_data TEXT,
            site_name TEXT DEFAULT 'Default Site',
            FOREIGN KEY (user_key) REFERENCES users (user_key)
        )
    """)

    # ३. प्रिमियम कोड्स टेबल
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

    # ४. फिचर लॉक्स टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feature_locks (
            feature_name TEXT PRIMARY KEY,
            access_level TEXT
        )
    """)

    # ५. मास्टर मार्केट दर टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_rates (
            material TEXT PRIMARY KEY,
            rate REAL
        )
    """)

    # ६. जाहिरात व स्पॉन्सर टेबल
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

    # ७. साईट हजेरी व मजुरी टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            supervisor INTEGER DEFAULT 0,
            supervisor_rate REAL DEFAULT 0.0,
            masons INTEGER DEFAULT 0,
            mason_rate REAL DEFAULT 0.0,
            labors INTEGER DEFAULT 0,
            labor_rate REAL DEFAULT 0.0,
            fitters INTEGER DEFAULT 0,
            fitter_rate REAL DEFAULT 0.0,
            carpenter INTEGER DEFAULT 0,
            carpenter_rate REAL DEFAULT 0.0,
            plumber INTEGER DEFAULT 0,
            plumber_rate REAL DEFAULT 0.0,
            electrician INTEGER DEFAULT 0,
            electrician_rate REAL DEFAULT 0.0,
            painter INTEGER DEFAULT 0,
            painter_rate REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

    # ८. साहित्य इन्व्हेंटरी टेबल (Quantity REAL सह)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            material_name TEXT,
            transaction_type TEXT,
            quantity REAL,
            unit TEXT,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

    # ८.१ मटेरियल ऑर्डर / इंडेंट टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_material_requisitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            work_type TEXT,
            work_volume REAL,
            material_name TEXT,
            required_qty REAL,
            stock_qty REAL,
            order_qty REAL,
            unit TEXT,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

    # ९. प्रोग्रेस रिपोर्ट टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            stage_name TEXT,
            progress_percent INTEGER,
            remark TEXT,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

    # १०. प्री-काँक्रीटिंग चेकलिस्ट टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pre_concreting_checklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            item_text TEXT,
            is_checked INTEGER DEFAULT 0,
            created_at TEXT,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

    # ११. प्रोजेक्ट टाईमलाईन आणि टास्क मॅनेजमेंट टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            site_name TEXT DEFAULT 'Default Site',
            stage_order INTEGER,
            task_name TEXT,
            planned_duration INTEGER,
            delay_days INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending',
            is_critical INTEGER DEFAULT 1
        )
    """)

    # १२. पेमेंट प्रोटेक्शन आणि टप्पे टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_milestone_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            site_name TEXT DEFAULT 'Default Site',
            stage_name TEXT,
            planned_amount REAL DEFAULT 0.0,
            amount_deposited REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Pending Deposit',
            engineer_approved INTEGER DEFAULT 0,
            client_approved INTEGER DEFAULT 0,
            is_locked INTEGER DEFAULT 0,
            completion_date TEXT,
            remark TEXT
        )
    """)

    # १३. क्लायंट प्रोफाईल व ईमेल टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_client_profiles (
            user_key TEXT,
            site_name TEXT,
            client_email TEXT,
            PRIMARY KEY (user_key, site_name)
        )
    """)

    # १४. साईट मास्टर आणि कोड्स टेबल (नवीन)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            site_code TEXT,
            site_name TEXT,
            created_at TEXT,
            UNIQUE(user_key, site_code)
        )
    """)

    # मास्टर ॲडमीन डिफॉल्ट एंट्री
    cursor.execute("SELECT * FROM users WHERE user_key = ?", ("9999999999",))
    if not cursor.fetchone():
        cursor.execute(
            """
            INSERT INTO users (
                user_key, id, uid, pin, mobile, email, password, comment, admin_message, 
                unread_notification, is_premium, premium_expiry, requested_code, seen_popup, 
                master_code_uses, last_active, activated_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    # डिफॉल्ट फिचर लॉक्स
    default_locks = {
        "Civil Calculator": "Free",
        "Rate Analysis": "Free",
        "BBS": "Free",
        "Quantity Surveying": "Free",
        "Site Manager": "Free",
        "NeevPay": "Free",
        "WhatsApp Share": "Premium",
        "Civil AI Assistant": "Premium",
    }
    for f_name, f_lvl in default_locks.items():
        cursor.execute(
            "INSERT OR IGNORE INTO feature_locks (feature_name, access_level) VALUES (?, ?)",
            (f_name, f_lvl),
        )

    # डिफॉल्ट मार्केट दर
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

# ==========================================
# 📌 विभाग ६: डेटाबेस क्वेरी आणि हेल्पर फंक्शन्स
# ==========================================
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


DEFAULT_CONSTRUCTION_STAGES = [
    (1, "पाया खोदाई (Site Clearing & Excavation)", 10, 1),
    (2, "पीसीसी व पाया काँक्रीट (PCC & Footing Casting)", 12, 1),
    (3, "प्लिंथ बीम व भराव (Plinth Beam & Backfilling)", 15, 1),
    (4, "आरसीसी कॉलम्स (Ground Floor Columns)", 10, 1),
    (5, "पहिला मजला स्लॅब कास्टिंग (Slab Casting)", 14, 1),
    (6, "विटांचे बांधकाम (Brickwork)", 20, 1),
    (7, "प्लंबिंग व इलेक्ट्रिकल कन्सिल्ड (Conduit/Piping)", 12, 0),
    (8, "आतील व बाहेरील प्लास्टर (Internal & External Plaster)", 18, 1),
    (9, "फ्लोरिंग व टाईल्स (Flooring & Tiling)", 15, 0),
    (10, "रंगकाम व फिनिशिंग (Painting & Final Handover)", 10, 1),
]


def load_default_tasks_if_empty(user_key, site_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as cnt FROM project_tasks WHERE user_key = ? AND site_name = ?",
        (user_key, site_name),
    )
    count = cursor.fetchone()["cnt"]
    if count == 0:
        for order, name, dur, crit in DEFAULT_CONSTRUCTION_STAGES:
            cursor.execute(
                """
                INSERT INTO project_tasks (user_key, site_name, stage_order, task_name, planned_duration, delay_days, status, is_critical)
                VALUES (?, ?, ?, ?, ?, 0, 'Pending', ?)
                """,
                (user_key, site_name, order, name, dur, crit),
            )
        conn.commit()
    conn.close()


# ==========================================
# 📌 विभाग ७: सेशन स्टेट्स आणि प्रिमियम ऑथेंटिकेशन (Admin Master Bypass)
# ==========================================
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
        st.session_state.otp_verified = True

for key, default in [
    ("pending_email", None),
    ("generated_otp", None),
    ("otp_verified", False),
    ("is_admin_logged", False),
    ("admin_impersonating", False),  # 🌟 Admin user bypass tracking
    ("admin_dashboard_tab", "rates"),
    ("current_comment", "काही नाही"),
    ("selected_module", None),
    ("selected_site_sub_module", None),
    ("selected_estimator_sub_module", None),
    ("admin_view", "main"),
    ("admin_selected_user", None),
    ("current_site_name", "Main Project Site"),
    ("all_sites_data", {"Default Site": {"milestones": [], "created_at": "26-08-2026"}}),
    ("autocad_site_opened", False),
    ("is_client_view", False),
    ("client_view_site", None),
    ("client_view_contact", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

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
    """प्रिमियम वैधता तपासणे - ॲडमीन/फाउंडरसाठी सर्व काही १००% मोफत व कायम अनलॉक राहील"""
    # 🌟 १. फाउंडर व ॲडमीन मास्टर बायपास (सगळे फीचर्स डायरेक्ट मोफत मिळतील):
    if st.session_state.get("is_admin_logged", False) or st.session_state.get("admin_impersonating", False):
        return True, "Founder Master VIP (All Features Free)"

    if not username:
        return False, "Free"
    
    # 🌟 २. मास्टर ॲडमीन की तपासणी:
    if str(username).lower() in ["admin", "9999999999"]:
        return True, "Master Lifetime VIP"

    # ३. सामान्य युझर प्रिमियम तपासणी:
    u_info = get_user_data(username)
    if u_info and u_info.get("is_premium") == 1:
        exp_date_str = u_info.get("premium_expiry")
        if exp_date_str:
            try:
                exp_datetime = datetime.datetime.strptime(
                    exp_date_str, "%Y-%m-%d %H:%M:%S"
                )
                now_datetime = get_ist_time()

                if now_datetime > exp_datetime:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE user_key = ?",
                        (username,),
                    )
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

# ==========================================
# 📌 विभाग ८: BRANDED CONSTRUCTION THEME CSS (Compact & Dedicated Inbox Support)
# ==========================================
st.markdown(
    """
    <style>
    /* १. अनावश्यक डीफॉल्ट स्क्रोल आणि स्ट्रीमलिट हेडर बंद करणे */
    #MainMenu, header[data-testid="stHeader"], footer, .stAppHeader, 
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    button[title="Increment"], button[title="Decrement"],
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* २. सुटसुटीत आणि डोळ्यांना हलकी डार्क थीम */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #090d16 !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* ३. कॉम्पॅक्ट ब्रँडेड हेडर (कमी जागा घेणारा, स्लीक डिझाईन) */
    .brand-header {
        background: #111827;
        border: 1px solid #1f2937;
        border-left: 4px solid #f59e0b;
        padding: 8px 14px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .brand-logo-icon {
        font-size: 22px;
        line-height: 1;
    }
    .brand-title-text h1 {
        margin: 0 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        color: #ffffff !important;
        display: inline-block;
    }
    .brand-title-text p {
        margin: 0 0 0 8px !important;
        font-size: 11px !important;
        color: #94a3b8 !important;
        font-weight: 500;
        display: inline-block;
    }
    .brand-founder-tag {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.2);
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }

    /* ४. इनबॉक्स व ॲडमीन मेसेज अलर्ट कार्ड */
    .inbox-alert-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(17, 24, 39, 0.95) 100%);
        border: 1px solid #10b981;
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* ५. इनपुट्स, सिलेक्ट व टेक्स्टएरिया */
    div[data-baseweb="input"], div[data-baseweb="base-input"],
    div[data-testid="stNumberInputContainer"], div[data-testid="stTextInput"] {
        background-color: #111827 !important;
        border-radius: 8px !important;
    }
    input, select, textarea {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    input:focus, textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 1px #f59e0b !important;
    }

    /* ६. आधुनिक कॉम्पॅक्ट बटन्स */
    div.stButton > button {
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }
    div.stButton > button[kind="primary"] {
        background: #f59e0b !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #d97706 !important;
        color: #000000 !important;
    }

    /* ७. मॉड्युल कार्ड्स */
    .module-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 14px 10px;
        text-align: center;
        transition: border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .module-card:hover {
        border-color: #f59e0b;
    }

    /* ८. स्टेटस बॅजेस */
    .gold-vip-badge {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b !important;
        border: 1px solid #f59e0b;
        padding: 2px 10px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 11px;
        display: inline-block;
    }
    .free-user-badge {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8 !important;
        border: 1px solid #0284c7;
        padding: 2px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 11px;
        display: inline-block;
    }

    /* ९. लाइटवेट ॲनिमेशन स्पिनर */
    .clean-loader {
        width: 36px;
        height: 36px;
        border: 3px solid rgba(245, 158, 11, 0.2);
        border-top-color: #f59e0b;
        border-radius: 50%;
        animation: clean-spin 0.8s linear infinite;
        margin: 15px auto;
    }
    @keyframes clean-spin {
        to { transform: rotate(360deg); }
    }

    /* १०. स्पॉन्सर ॲड कार्ड */
    .sponsor-mini-card {
        background: #111827;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 8px 12px;
        border-radius: 8px;
        text-align: center;
        margin: 8px auto;
        max-width: 320px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 📌 विभाग ९: WHATSAPP रिपोर्ट शेअरिंग कंपोनंट
# ==========================================
def render_whatsapp_feature(encoded_msg, key_prefix):
    is_prem, _ = check_user_premium_status(current_user_name)
    locks_cfg = get_feature_locks()
    wa_lock_setting = locks_cfg.get("WhatsApp Share", "Premium")

    if wa_lock_setting == "Free" or is_prem:
        st.markdown(
            f"""
            <a href="https://wa.me/?text={encoded_msg}" target="_blank" style="text-decoration:none;">
                <button style="width: 100%; background: #16a34a; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; gap: 8px;">
                    <span>📱</span> Share on WhatsApp {"(Free)" if wa_lock_setting == "Free" else "(👑 VIP Active)"}
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
    else:
        safe_uid = f"{key_prefix}_{abs(hash(encoded_msg)) % 100000}"

        with st.expander("🔒 WhatsApp Report Sharing - Unlock Premium"):
            st.caption("💡 व्हॉट्सॲपवर पूर्ण रिपोर्ट शेअर करण्यासाठी खाली ॲक्टिव्हेशन कोड टाका:")

            p_code = st.text_input(
                "Enter Activation Code:", key=f"{safe_uid}_code_input"
            ).strip()

            w_col1, w_col2 = st.columns(2)
            with w_col1:
                if st.button("🔓 Unlock Share", key=f"{safe_uid}_unlock_btn", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT * FROM premium_codes WHERE code = ?", (p_code,)
                    )
                    row = cursor.fetchone()

                    if row:
                        c_info = dict(row)
                        if c_info.get("used") == 1:
                            st.error("❌ हा कोड आधीच वापरला गेला आहे!")
                            conn.close()
                        else:
                            exp_datetime = get_ist_time() + datetime.timedelta(days=28)
                            exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                            cursor.execute(
                                "UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?",
                                (current_user_name, now_str, p_code),
                            )

                            disp_name = current_user_name if current_user_name else ""
                            welcome_msg = f"{disp_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये हार्दिक स्वागत आहे🥳"

                            cursor.execute(
                                """
                                UPDATE users 
                                SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?, admin_message = ?, unread_notification = 0
                                WHERE user_key = ?
                                """,
                                (
                                    exp_str,
                                    "Kanhaiya (Founder)",
                                    welcome_msg,
                                    current_user_name,
                                ),
                            )

                            conn.commit()
                            conn.close()
                            st.rerun()
                    else:
                        conn.close()
                        st.error("❌ चुकीचा प्रिमियम कोड!")

            with w_col2:
                if st.button("📩 Request Code", key=f"{safe_uid}_req_btn", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET requested_code = 1 WHERE user_key = ?",
                        (current_user_name,),
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ ॲडमीनला रिक्वेस्ट पाठवली!")


# ==========================================
# 📌 विभाग १०: वेलकम स्क्रीन ॲनिमेशन (Fast & Responsive)
# ==========================================
welcome_placeholder = st.empty()

if "welcome_completed" not in st.session_state:
    st.session_state.welcome_completed = False

if not st.session_state.welcome_completed:
    with welcome_placeholder.container():
        st.markdown("<div class='clean-loader'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 15px;">
                <h2 style='color: #ffffff; margin: 0; font-size: 22px; font-weight: 800;'>PATIL INFRATECH</h2>
                <p style='color: #f59e0b; margin: 4px 0; font-size: 13px; font-weight: 600;'>Civil Engineering • Site Management</p>
                <small style='color: #64748b;'>Concept & Logic by: <b>Kanhaiya (Founder)</b></small>
            </div>
            """,
            unsafe_allow_html=True,
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ads WHERE active = 1 AND position = 'Loading Page (Title Sponsor)'"
        )
        ads_rows = cursor.fetchall()
        conn.close()

        for ad in ads_rows:
            ad_dict = dict(ad)
            st.markdown(
                f"""
                <div class="sponsor-mini-card">
                    <span style="font-size: 10px; color: #f59e0b; font-weight: bold;">⭐ SPONSOR</span><br>
                    <b style="color: #ffffff; font-size: 13px;">{ad_dict.get('title')}</b>
                    <p style="color: #94a3b8; font-size: 11px; margin: 2px 0;">{ad_dict.get('desc')}</p>
                    <a href="{ad_dict.get('link')}" target="_blank" style="color: #38bdf8; font-size: 11px; font-weight: 600;">👉 भेट द्या</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        progress_bar = st.progress(0)
        status_text = st.empty()

        construction_stages = [
            "🧱 पाया खोदण्याचे काम...",
            "🏗️ कॉलम उभे राहत आहेत...",
            "🧱 विटांचे बांधकाम...",
            "🏠 स्लॅब कास्टिंग...",
            "✨ फिनिशिंग पूर्ण! 🎉",
        ]

        # मोबाईलवर जलद लोड होण्यासाठी ऑप्टिमाइझ स्लीप (०.१ सेकंद)
        for i in range(5):
            status_text.markdown(
                f"<p style='text-align: center; font-size: 14px; font-weight: 600; color: #94a3b8; margin: 5px 0;'>{construction_stages[i]}</p>",
                unsafe_allow_html=True,
            )
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.12)

    welcome_placeholder.empty()
    st.session_state.welcome_completed = True

# मुख्य ॲप हेडर बॅनर (क्लीन, मॉडर्न, फ्लेक्सिबल)
st.markdown(
    """
    <div class="brand-header">
        <div class="brand-title-wrap">
            <div class="brand-logo-icon">🏗️</div>
            <div class="brand-title-text">
                <h1>PATIL INFRATECH</h1>
                <p>Civil Engineering • Quantity Surveying • Site Management</p>
            </div>
        </div>
        <div class="brand-founder-tag">
            Founder: Kanhaiya
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# ==============================================================================
# 📌 विभाग ११: ॲडमीन पॅनल (Admin Command Center with Founder Direct Access)
# ==============================================================================
if st.session_state.is_admin_logged:
    # १. ग्रँड कॉर्पोरेट वेलकम हेडर
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #31104b 100%); border: 1px solid #4338ca; border-left: 6px solid #8b5cf6; padding: 20px 24px; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <span style="background:rgba(139,92,246,0.2); color:#c4b5fd; border:1px solid #8b5cf6; padding:3px 12px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Founder & Executive Console</span>
                    <h2 style="color:#ffffff; margin:6px 0 2px 0; font-size:24px; font-weight:900;">⚡ PATIL INFRATECH EXECUTIVE COMMAND CENTER</h2>
                    <p style="color:#94a3b8; margin:0; font-size:13px;">Master Control Hub • Full System Authority & Unlimited Access</p>
                </div>
                <div style="text-align:right;">
                    <span style="color:#10b981; font-weight:bold; font-size:13px;">🟢 Founder Rights: ACTIVE</span><br>
                    <small style="color:#64748b;">All Premium Gates Bypassed</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 🚀 फाउंडर डायरेक्ट ॲप एंट्री व लॉगआउट बार
    col_entry, col_logout, _ = st.columns([2.5, 1.5, 2])
    with col_entry:
        if st.button("🚀 Enter Main App as Founder (All Unlocked)", type="primary", use_container_width=True):
            st.session_state.app_user_name = "9999999999"  # Master Admin key
            st.session_state.is_admin_logged = False
            st.session_state.admin_impersonating = True
            st.session_state.selected_module = None
            st.rerun()

    with col_logout:
        if st.button("🔒 Admin Logout", use_container_width=True):
            st.session_state.is_admin_logged = False
            st.session_state.admin_impersonating = False
            st.rerun()

    st.write("---")

    # २. कॉर्पोरेट ऑफिस स्टाईल टॅब्स
    adm_tab_rates, adm_tab_locks, adm_tab_users, adm_tab_ads, adm_tab_bcast = st.tabs([
        "📈 Master Rates", "⚙️ Feature Locks", "👥 User Database", "📢 Ads & Sponsors", "🔔 Broadcast"
    ])

    # --- टॅब १: मास्टर दर ---
    with adm_tab_rates:
        st.markdown(
            """
            <div style="background:#111827; border-left:4px solid #38bdf8; padding:10px 16px; border-radius:8px; margin-bottom:16px;">
                <b style="color:#38bdf8; font-size:15px;">📈 Update Master Market Rates</b>
                <p style="color:#94a3b8; font-size:12px; margin:2px 0 0 0;">येथे बदललेले दर संपूर्ण ॲपमधील सर्व कॅल्क्युलेटरमध्ये लागू होतील.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        m_rates = get_market_rates()

        c_r1, c_r2 = st.columns(2)
        with c_r1:
            adm_cem = st.number_input("Cement (per bag ₹):", min_value=0.0, value=float(m_rates.get("cement", 400.0)), step=1.0)
            adm_snd = st.number_input("Sand (per m³ ₹):", min_value=0.0, value=float(m_rates.get("sand", 2500.0)), step=1.0)
            adm_brk = st.number_input("Brick (per nos ₹):", min_value=0.0, value=float(m_rates.get("bricks", 8.0)), step=0.1)
        with c_r2:
            adm_agg = st.number_input("Aggregate (per m³ ₹):", min_value=0.0, value=float(m_rates.get("aggregate", 2200.0)), step=1.0)
            adm_ste = st.number_input("Steel Rate (per kg ₹):", min_value=0.0, value=float(m_rates.get("steel", 60.0)), step=1.0)

        if st.button("💾 Save Master Market Rates", type="primary", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            updated_rates = {
                "cement": adm_cem,
                "sand": adm_snd,
                "bricks": adm_brk,
                "aggregate": adm_agg,
                "steel": adm_ste,
            }
            for mat, rat in updated_rates.items():
                cursor.execute(
                    "REPLACE INTO market_rates (material, rate) VALUES (?, ?)",
                    (mat, rat),
                )
            conn.commit()
            conn.close()
            st.success("✅ आजचे मास्टर मार्केट दर डेटाबेसमध्ये यशस्वीरित्या अपडेट झाले!")

    # --- टॅब २: फिचर लॉक्स ---
    with adm_tab_locks:
        st.markdown(
            """
            <div style="background:#111827; border-left:4px solid #f59e0b; padding:10px 16px; border-radius:8px; margin-bottom:16px;">
                <b style="color:#f59e0b; font-size:15px;">⚙️ Feature Lock Manager</b>
                <p style="color:#94a3b8; font-size:12px; margin:2px 0 0 0;">कोणते फिचर फ्री ठेवायचे आणि कोणते VIP प्रिमियम ठेवायचे ते येथून ठरवा.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        cur_locks = get_feature_locks()

        l_c1, l_c2 = st.columns(2)
        with l_c1:
            fl_calc = st.selectbox("Civil Calculator:", ["Free", "Premium"], index=0 if cur_locks.get("Civil Calculator", "Free") == "Free" else 1)
            fl_ra = st.selectbox("Rate Analysis Module:", ["Free", "Premium"], index=0 if cur_locks.get("Rate Analysis", "Free") == "Free" else 1)
            fl_bbs = st.selectbox("BBS Calculator:", ["Free", "Premium"], index=0 if cur_locks.get("BBS", "Free") == "Free" else 1)
            fl_qs = st.selectbox("Quantity Surveying:", ["Free", "Premium"], index=0 if cur_locks.get("Quantity Surveying", "Free") == "Free" else 1)
        with l_c2:
            fl_site = st.selectbox("Site Manager:", ["Free", "Premium"], index=0 if cur_locks.get("Site Manager", "Free") == "Free" else 1)
            fl_neev = st.selectbox("NeevPay Payment Protection:", ["Free", "Premium"], index=0 if cur_locks.get("NeevPay", "Free") == "Free" else 1)
            fl_wa = st.selectbox("WhatsApp Full Report Share:", ["Free", "Premium"], index=0 if cur_locks.get("WhatsApp Share", "Free") == "Free" else 1)
            fl_ai = st.selectbox("Civil AI Assistant:", ["Free", "Premium"], index=0 if cur_locks.get("Civil AI Assistant", "Premium") == "Free" else 1)

        if st.button("💾 Save Feature Lock Settings", type="primary", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            new_locks = {
                "Civil Calculator": fl_calc,
                "Rate Analysis": fl_ra,
                "BBS": fl_bbs,
                "Quantity Surveying": fl_qs,
                "Site Manager": fl_site,
                "NeevPay": fl_neev,
                "WhatsApp Share": fl_wa,
                "Civil AI Assistant": fl_ai,
            }
            for f_name, f_lvl in new_locks.items():
                cursor.execute(
                    "REPLACE INTO feature_locks (feature_name, access_level) VALUES (?, ?)",
                    (f_name, f_lvl),
                )
            conn.commit()
            conn.close()
            st.success("✅ फिचर सेटिंग्स यशस्वीरित्या बदलल्या!")

    # --- टॅब ३: युझर डेटाबेस ---
    with adm_tab_users:
        if st.session_state.admin_view == "user_detail" and st.session_state.admin_selected_user is not None:
            target_user = st.session_state.admin_selected_user
            if st.button("⬅️ सर्व युझर्स यादीवर परत जा", use_container_width=True):
                st.session_state.admin_view = "main"
                st.session_state.admin_selected_user = None
                st.rerun()

            info = get_user_data(target_user) or {}
            u_name = info.get("id", target_user)
            u_uid = info.get("uid", "N/A")
            u_email = info.get("email", "N/A")
            u_pin = info.get("pin", "N/A")
            u_comm = info.get("comment", "काही नाही")
            u_prem = bool(info.get("is_premium", 0))
            exp_date = info.get("premium_expiry", "N/A")
            is_req = bool(info.get("requested_code", 0))

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM history WHERE user_key = ? ORDER BY id DESC",
                (target_user,),
            )
            u_hist = [dict(r) for r in cursor.fetchall()]

            cursor.execute(
                "SELECT code FROM premium_codes WHERE assigned_to = ? AND used = 0",
                (u_name,),
            )
            c_row = cursor.fetchone()
            conn.close()
            assigned_code = c_row["code"] if c_row else None

            # स्टेटस बॅज
            status_badge = (
                f"👑 VIP MEMBER: {u_name.upper()}" if u_prem else ("🚨 CODE REQUESTED!" if is_req else f"🆓 FREE: {u_name.upper()}")
            )
            card_border_color = "#f59e0b" if u_prem else ("#ef4444" if is_req else "#38bdf8")

            st.markdown(
                f"""
                <div style="background:#111827; border:1px solid #1f2937; border-left:5px solid {card_border_color}; padding:16px; border-radius:12px; margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                        <h3 style="margin:0; color:#ffffff;">👤 {u_name.upper()}</h3>
                        <span class="gold-vip-badge">{status_badge}</span>
                    </div>
                    <p style="margin:8px 0 0 0; font-size:14px; color:#cbd5e1;">
                        <b>Username/UID:</b> <code style="color:#38bdf8;">{u_uid}</code> | <b>Password:</b> <code>{u_pin}</code> | <b>Email:</b> <code>{u_email}</code>
                    </p>
                    <p style="margin:4px 0 0 0; font-size:14px; color:#cbd5e1;">
                        <b>प्रिमियम मुदत (Expiry):</b> <code style="color:#f59e0b;">{exp_date}</code> | <b>ॲक्टिव्ह कोड:</b> <code style="color:#10b981;">{assigned_code if assigned_code else 'काही नाही'}</code>
                    </p>
                    <p style="margin:4px 0 0 0; font-size:13px; color:#94a3b8;"><b>युझर कमेंट:</b> {u_comm}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 🌟 थेट या युझरच्या प्रोफाइलमध्ये शिरण्याचे मास्टर बटण
            if st.button(f"🎭 Login as {u_name} (Full Free Access Bypass)", type="primary", use_container_width=True):
                st.session_state.app_user_name = target_user
                st.session_state.is_admin_logged = False
                st.session_state.admin_impersonating = True
                st.session_state.selected_module = None
                st.rerun()

            st.write("---")

            if assigned_code:
                st.info(f"💡 {u_name} साठी आधीच एक कोड तयार आहे: `{assigned_code}`")
            else:
                if st.button(f"🚀 Generate & Send Unique Code to {u_name}", key=f"win_gen_send_{target_user}", use_container_width=True):
                    new_c = generate_random_code()
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO premium_codes (code, assigned_to, used, created_at) VALUES (?, ?, 0, ?)",
                        (new_c, u_name, now_str),
                    )
                    msg = f"तुमचा प्रिमियम कोड: {new_c} (ॲपमध्ये टाकून प्रिमियम अनलॉक करा)"
                    cursor.execute(
                        "UPDATE users SET admin_message = ?, requested_code = 0 WHERE user_key = ?",
                        (msg, target_user),
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"🎉 {u_name} ला ऑटोमॅटिकली कोड पाठवला: `{new_c}`")
                    st.rerun()

            st.write("---")
            st.markdown("###### ⏱️ प्रिमियम वेळ सेट करा / वाढवा (Custom Expiry):")
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                time_val = st.number_input("संख्या (Value):", min_value=1, value=28, key=f"win_t_val_{target_user}")
            with t_col2:
                time_unit = st.selectbox("युनिट (Unit):", ["Minutes", "Hours", "Days"], index=2, key=f"win_t_unit_{target_user}")

            if st.button(f"⚡ Set Premium Time ({time_val} {time_unit})", key=f"win_btn_custom_{target_user}", use_container_width=True):
                now = get_ist_time()
                if time_unit == "Minutes":
                    exp_time = now + datetime.timedelta(minutes=time_val)
                elif time_unit == "Hours":
                    exp_time = now + datetime.timedelta(hours=time_val)
                else:
                    exp_time = now + datetime.timedelta(days=time_val)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE users 
                    SET is_premium = 1, premium_expiry = ?, requested_code = 0, seen_popup = 0, activated_by = ?
                    WHERE user_key = ?
                    """,
                    (
                        exp_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Master Admin",
                        target_user,
                    ),
                )
                conn.commit()
                conn.close()
                st.success(f"✅ {u_name} साठी {time_val} {time_unit} सेव्ह केले!")
                st.rerun()

            if u_prem:
                if st.button(f"🔻 Revoke Premium: {u_name}", key=f"win_rev_{target_user}", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE user_key = ?",
                        (target_user,),
                    )
                    conn.commit()
                    conn.close()
                    st.warning(f"❌ {u_name} चे प्रिमियम काढले आहे.")
                    st.rerun()

            st.write("---")
            current_msg = info.get("admin_message", "Admin message...")
            new_msg = st.text_input(
                f"✍️ {u_name} साठी इनबॉक्स मेसेज बदलणे (Notification Send):",
                value=current_msg,
                key=f"win_msg_{target_user}",
            )
            if st.button(f"✉️ मेसेज सेव्ह करा व पाठवा ({u_name})", key=f"win_btn_msg_{target_user}", use_container_width=True):
                if new_msg.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET admin_message = ?, unread_notification = 1 WHERE user_key = ?",
                        (new_msg.strip(), target_user),
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"✅ '{u_name}' च्या इनबॉक्समध्ये नवीन मेसेज पाठवला!")
                    st.rerun()

            if st.button(f"🗑️ Delete User: {u_name}", key=f"win_del_{target_user}", use_container_width=True):
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

            st.write("---")
            st.markdown(f"###### 📜 {u_name} चे जनरेट केलेले एस्टिमेशन रिपोर्ट्स ({len(u_hist)})")
            if u_hist:
                for idx, hist in enumerate(u_hist, 1):
                    ts = hist.get("timestamp", "N/A")
                    with st.expander(f"🗓️ रिपोर्ट #{idx} | तारीख व वेळ: `{ts}`"):
                        st.markdown(hist.get("report_data", "डेटा उपलब्ध नाही"))
            else:
                st.info("ℹ️ या युझरने अजून एकही रिपोर्ट जनरेट केलेला नाही.")

        else:
            st.markdown(
                """
                <div style="background:#111827; border-left:4px solid #10b981; padding:10px 16px; border-radius:8px; margin-bottom:16px;">
                    <b style="color:#10b981; font-size:15px;">👥 User Database Master List</b>
                    <p style="color:#94a3b8; font-size:12px; margin:2px 0 0 0;">सर्व नोंदणीकृत युझर्स, त्यांचे स्टेटस व प्रिमियम कंट्रोल.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE user_key != '9999999999' ORDER BY id ASC"
            )
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
                            last_active_dt = datetime.datetime.strptime(
                                last_active_str, "%Y-%m-%d %H:%M:%S"
                            )
                            diff_seconds = (now_time - last_active_dt).total_seconds()
                            if diff_seconds <= 120:
                                is_online = True
                        except Exception:
                            pass

                    status_indicator = (
                        "🟢 Active (Online)" if is_online else "🔴 Inactive (Offline)"
                    )
                    status_color = "#10b981" if is_online else "#ef4444"

                    u_card_col1, u_card_col2 = st.columns([3.6, 1.4])
                    with u_card_col1:
                        if u_prem:
                            badge_markup = f"<span class='gold-vip-badge'>👑 VIP: {u_name.upper()}</span>"
                        elif is_req:
                            badge_markup = f"<span style='background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid #ef4444; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:12px;'>🚨 CODE REQ: {u_name}</span>"
                        else:
                            badge_markup = f"<span class='free-user-badge'>🆓 FREE: {u_name.upper()}</span>"

                        st.markdown(
                            f"""
                            <div style="background:#111827; border:1px solid #1f2937; padding:12px 16px; border-radius:10px; margin-bottom:6px;">
                                {badge_markup} <code style="margin-left:8px; font-size:12px;">UID: {u_uid}</code>
                                <div style="margin-top:4px;">
                                    <small style="color:{status_color}; font-weight:bold;">{status_indicator}</small>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with u_card_col2:
                        st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
                        if st.button("👁️ Manage / Login", key=f"open_user_win_{mob}", use_container_width=True):
                            st.session_state.admin_view = "user_detail"
                            st.session_state.admin_selected_user = mob
                            trigger_push_state()
                            st.rerun()
            else:
                st.info("ℹ️ डेटाबेसमध्ये सध्या कोणताही सामान्य युझर नाही.")

    # --- टॅब ४: जाहिरात व स्पॉन्सर ---
    with adm_tab_ads:
        st.markdown(
            """
            <div style="background:#111827; border-left:4px solid #a855f7; padding:10px 16px; border-radius:8px; margin-bottom:16px;">
                <b style="color:#a855f7; font-size:15px;">📢 Ad & Sponsor Manager</b>
                <p style="color:#94a3b8; font-size:12px; margin:2px 0 0 0;">अॅपमध्ये दिसणाऱ्या स्पॉन्सर जाहिरातींचे नियंत्रण.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form("add_ad_form"):
            ad_title = st.text_input("Sponsor / Ad Title:")
            ad_desc = st.text_area("Offer / Description:")
            ad_link = st.text_input("Target Link (URL or WhatsApp link):")
            media_type = st.selectbox("Media Type:", ["Photo (PNG/JPG)", "Video Ad"])
            media_url = st.text_input("Media Direct URL (Image/Video Link):")
            position = st.selectbox("Display Position:", ["Loading Page (Title Sponsor)", "Main App Header (Top Banner)"])
            is_active = st.checkbox("Make Active / Live", value=True)

            submit_ad = st.form_submit_button("🚀 Publish Ad Sponsor", type="primary", use_container_width=True)
            if submit_ad:
                if ad_title.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        """
                        INSERT INTO ads (title, desc, link, media_type, media_url, position, active, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            ad_title.strip(),
                            ad_desc.strip(),
                            ad_link.strip(),
                            media_type,
                            media_url.strip(),
                            position,
                            1 if is_active else 0,
                            now_str,
                        ),
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ स्पॉन्सर ॲड यशस्वीरित्या पब्लिश झाली!")
                    st.rerun()
                else:
                    st.warning("⚠️ कृपया ॲडचे नाव टाका!")

        st.write("---")
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
                if st.button(f"🗑️ Delete Ad #{ad_id}", key=f"del_ad_{ad_id}", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
                    conn.commit()
                    conn.close()
                    st.success("🗑️ ॲड डिलीट केली!")
                    st.rerun()
        else:
            st.info("ℹ️ सध्या कोणतीही ॲड किंवा स्पॉन्सरशिप उपलब्ध नाही.")

    # --- टॅब ५: ब्रॉडकास्ट मेसेज ---
    with adm_tab_bcast:
        st.markdown(
            """
            <div style="background:#111827; border-left:4px solid #ef4444; padding:10px 16px; border-radius:8px; margin-bottom:16px;">
                <b style="color:#ef4444; font-size:15px;">🔔 Broadcast Notification to All Users</b>
                <p style="color:#94a3b8; font-size:12px; margin:2px 0 0 0;">सर्व ॲप युझर्सच्या इनबॉक्समध्ये एकाच वेळी अलर्ट पाठवा.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form("broadcast_form"):
            broadcast_msg = st.text_area(
                "सर्व युझर्सना पाठवायचा मेसेज (Broadcast Message):",
                placeholder="उदा. नवीन अपडेट आली आहे, चेक करा...",
            )
            submit_broadcast = st.form_submit_button("🚀 Send to All Users (Broadcast)", type="primary", use_container_width=True)

            if submit_broadcast:
                if broadcast_msg.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE users 
                        SET admin_message = ?, unread_notification = 1 
                        WHERE user_key != '9999999999'
                        """,
                        (broadcast_msg.strip(),),
                    )
                    conn.commit()
                    conn.close()
                    st.success("🎉 ब्रॉडकास्ट मेसेज सर्व युझर्सना यशस्वीरित्या पाठवला गेला आहे!")
                else:
                    st.warning("⚠️ कृपया पाठवण्यासाठी काहीतरी मेसेज लिहा!")

    st.stop()
# ==========================================
# 📌 विभाग १२: युझर ऑथेंटिकेशन (Login, Register, OTP & Client View)
# ==========================================
if st.session_state.app_user_name is None and not st.session_state.get("is_client_view", False):
    st.markdown("### 🏗️ PATIL INFRATECH - SECURE ACCESS")

    login_tab, otp_tab, client_tab = st.tabs([
        "🔑 Registered Login",
        "📧 Email Register / OTP",
        "🔍 Client / Owner Live View"
    ])

    # १२.१ Registered Login
    with login_tab:
        with st.form("direct_login_form"):
            login_email = st.text_input("ईमेल किंवा Username:").strip()
            login_pass = st.text_input("पासवर्ड:", type="password").strip()
            if st.form_submit_button("🚀 Login Now", type="primary", use_container_width=True):
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
                        found_user = row["user_key"]
                        st.session_state.app_user_name = found_user
                        st.session_state.is_client_view = False
                        st.query_params["saved_user"] = found_user
                        st.markdown(f"<script>localStorage.setItem('patil_app_user', '{found_user}');</script>", unsafe_allow_html=True)
                        st.success("🎉 यशस्वीरित्या लॉगिन झाले!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा आयडी किंवा पासवर्ड!")
                else:
                    st.warning("⚠️ सर्व माहिती भरा.")

    # १२.२ Email Registration & OTP
    with otp_tab:
        st.markdown("##### 📧 Email Verification & Setup")
        email_input = st.text_input("ईमेल आयडी टाका:", key="otp_email_key").strip()

        if not st.session_state.otp_verified:
            if st.button("📤 Send OTP to Email", type="primary", use_container_width=True):
                if email_input and "@" in email_input:
                    generated_otp = "".join(random.choices(string.digits, k=6))
                    st.session_state.generated_otp = generated_otp
                    st.session_state.pending_email = email_input

                    with st.spinner("📧 OTP पाठवत आहे..."):
                        subject = "PATIL INFRATECH - Verification OTP"
                        body = f"तुमचा पाटील इन्फ्राटेक लॉगिन OTP: {generated_otp}\n\n- Patil Infratech Team"
                        if send_email_message(email_input, subject, body):
                            st.success("✅ ईमेलवर OTP पाठवला आहे!")
                        else:
                            st.error("❌ ईमेल पाठवताना एरर आली.")
                else:
                    st.warning("⚠️ कृपया अचूक ईमेल टाका!")

            if st.session_state.generated_otp:
                entered_otp = st.text_input("६ अंकी OTP टाका:", max_chars=6).strip()
                if st.button("🔐 Verify OTP", use_container_width=True):
                    if entered_otp == st.session_state.generated_otp:
                        st.session_state.otp_verified = True
                        st.success("✅ OTP व्हेरिफाय झाला!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा OTP!")

        if st.session_state.otp_verified and st.session_state.pending_email:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (st.session_state.pending_email,))
            row = cursor.fetchone()
            conn.close()

            if row:
                found_user = dict(row)["user_key"]
                st.session_state.app_user_name = found_user
                st.session_state.is_client_view = False
                st.query_params["saved_user"] = found_user
                st.markdown(f"<script>localStorage.setItem('patil_app_user', '{found_user}');</script>", unsafe_allow_html=True)
                st.success(f"🎉 स्वागत आहे {found_user}!")
                st.rerun()
            else:
                with st.form("custom_reg_form"):
                    custom_username = st.text_input("युझरनेम बनवा:").strip()
                    custom_password = st.text_input("मजबूत पासवर्ड:", type="password").strip()
                    confirm_password = st.text_input("पासवर्ड पुन्हा टाका:", type="password").strip()

                    if st.form_submit_button("🚀 Complete Registration", type="primary", use_container_width=True):
                        if custom_username and custom_password and confirm_password:
                            if custom_password != confirm_password:
                                st.error("❌ पासवर्ड जुळत नाहीत!")
                            else:
                                is_strong, msg = is_strong_password(custom_password)
                                if not is_strong:
                                    st.error(f"❌ {msg}")
                                else:
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT user_key FROM users WHERE user_key = ? OR uid = ?", (custom_username, custom_username))
                                    if cursor.fetchone():
                                        conn.close()
                                        st.error("❌ हा Username आधीच अस्तित्वात आहे!")
                                    else:
                                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                                        cursor.execute(
                                            """
                                            INSERT INTO users (
                                                user_key, id, uid, pin, mobile, email, password, comment, 
                                                admin_message, unread_notification, is_premium, premium_expiry, 
                                                requested_code, seen_popup, master_code_uses, last_active, activated_by
                                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, NULL, 0, 0, 0, ?, ?)
                                            """,
                                            (custom_username, custom_username, custom_username, custom_password, "N/A", st.session_state.pending_email, custom_password, "काही नाही", f"स्वागत आहे {custom_username}!", now_str, "Free User"),
                                        )
                                        conn.commit()
                                        conn.close()

                                        st.session_state.app_user_name = custom_username
                                        st.session_state.is_client_view = False
                                        st.query_params["saved_user"] = custom_username
                                        st.markdown(f"<script>localStorage.setItem('patil_app_user', '{custom_username}');</script>", unsafe_allow_html=True)
                                        st.success("🎉 अकाउंट तयार झाले!")
                                        st.rerun()

    # १२.३ 🔍 Client Read-Only Live Portal (Using Site Code)
    with client_tab:
        st.markdown("##### 🔍 Client / Owner Live Site Portal")
        st.caption("घरमालक इंजिनिअरने दिलेला युनिक साईट कोड टाकून थेट कामाची सद्यस्थिती पाहू शकतात.")

        with st.form("client_code_access_form"):
            input_client_code = st.text_input(
                "Enter Site Access Code (साईट कोड टाका):", 
                placeholder="उदा. S1, P1, L2", 
                help="इंजिनिअरने तुमच्या साईटसाठी दिलेला कोड टाका."
            ).strip().upper()

            submit_client_view = st.form_submit_button("🔍 साईट प्रोग्रेस व बिल पाहा (View Live Status)", type="primary", use_container_width=True)

            if submit_client_view:
                if input_client_code:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT site_name, user_key FROM user_sites WHERE site_code = ?",
                        (input_client_code,)
                    )
                    found_site_row = cursor.fetchone()
                    conn.close()

                    if found_site_row:
                        st.session_state.is_client_view = True
                        st.session_state.client_view_site = found_site_row["site_name"]
                        st.session_state.client_view_code = input_client_code
                        st.session_state.client_view_engineer = found_site_row["user_key"]
                        st.rerun()
                    else:
                        st.error(f"❌ '{input_client_code}' या कोडची कोणतीही साईट सापडली नाही! अचूक कोड टाका.")
                else:
                    st.warning("⚠️ कृपया साईट कोड टाका!")

    st.write("---")
    with st.expander("🛡️ Admin Login"):
        with st.form("admin_login_form"):
            admin_id = st.text_input("Admin ID:")
            admin_pass = st.text_input("Password:", type="password")
            if st.form_submit_button("🔓 Admin Login", type="primary", use_container_width=True):
                secret_id = st.secrets.get("ADMIN_ID", "kanha_1p") if hasattr(st, "secrets") and "ADMIN_ID" in st.secrets else "kanha_1p"
                secret_pass = st.secrets.get("ADMIN_PASS", "@Dellg15") if hasattr(st, "secrets") and "ADMIN_PASS" in st.secrets else "@Dellg15"
                if admin_id == secret_id and admin_pass == secret_pass:
                    st.session_state.is_admin_logged = True
                    st.rerun()
                else:
                    st.error("❌ चुकीचे क्रेडेन्शियल्स!")

    st.stop()


# ==========================================================
# 📌 विभाग १२.५: CLIENT LIVE READ-ONLY DASHBOARD RENDERER
# ==========================================================
if st.session_state.get("is_client_view", False):
    c_site = st.session_state.get("client_view_site", "Default Site")
    c_code = st.session_state.get("client_view_code", "S1")
    c_eng = st.session_state.get("client_view_engineer", "Site Engineer")

    col_c_top, col_c_exit = st.columns([3.5, 1.5])
    with col_c_top:
        st.markdown(
            f"""
            <div style="background:#111827; border:1px solid #1f2937; border-left:4px solid #10b981; padding:10px 14px; border-radius:8px;">
                <span style="color:#94a3b8; font-size:11px; text-transform:uppercase;">CLIENT LIVE PORTAL (READ-ONLY)</span><br>
                <b style="color:#ffffff; font-size:16px;">🏗️ [{c_code}] {c_site}</b>
                <span style="color:#94a3b8; font-size:12px; margin-left:8px;">(Site Engineer: {c_eng})</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_c_exit:
        if st.button("🚪 पोर्टल बंद करा (Exit View)", type="primary", use_container_width=True):
            st.session_state.is_client_view = False
            st.session_state.client_view_site = None
            st.session_state.client_view_code = None
            st.rerun()

    st.write("---")

    conn = get_db_connection()
    cursor = conn.cursor()

    # पेमेंट डेटा
    cursor.execute("SELECT * FROM site_milestone_payments WHERE site_name = ? ORDER BY id ASC", (c_site,))
    c_milestones = [dict(r) for r in cursor.fetchall()]

    # प्रोग्रेस डेटा
    cursor.execute("SELECT * FROM site_progress WHERE site_name = ? ORDER BY id DESC LIMIT 5", (c_site,))
    c_progress = [dict(r) for r in cursor.fetchall()]

    # मटेरियल इन्व्हेंटरी
    cursor.execute("SELECT material_name, transaction_type, quantity, unit FROM site_inventory WHERE site_name = ?", (c_site,))
    inv_rows = cursor.fetchall()
    conn.close()

    c_tot_budget = sum(m["planned_amount"] for m in c_milestones)
    c_tot_paid = sum(m["amount_deposited"] for m in c_milestones)
    c_tot_pending = max(0.0, c_tot_budget - c_tot_paid)
    c_locked_count = sum(1 for m in c_milestones if m.get("is_locked") == 1)
    c_pct = (c_tot_paid / c_tot_budget * 100) if c_tot_budget > 0 else 0.0

    st.markdown("##### 💰 बिलाचा व पेमेंटचा तपशील (Billing & Payment Summary)")
    cb1, cb2, cb3, cb4 = st.columns(4)
    cb1.metric("एकूण ठरलेले बिल", f"₹ {c_tot_budget:,.2f}")
    cb2.metric("तुम्ही दिलेली रक्कम", f"₹ {c_tot_paid:,.2f}")
    cb3.metric("शिल्लक बाकी", f"₹ {c_tot_pending:,.2f}")
    cb4.metric("एकूण प्रगती (%)", f"{c_pct:.1f}% ({c_locked_count}/{len(c_milestones)} टप्पे)")

    c_tab1, c_tab2, c_tab3 = st.tabs(["📋 टप्प्याटप्प्याने बिल (Milestones)", "📸 कामाची प्रगती (Progress)", "📦 साहित्याचा हिशोब (Stock)"])

    with c_tab1:
        if c_milestones:
            m_table_rows = ""
            for idx, m in enumerate(c_milestones, 1):
                p = float(m["planned_amount"])
                d = float(m["amount_deposited"])
                bal = max(0.0, p - d)
                st_text = "✅ 100% Paid" if m.get("is_locked") == 1 else ("🟡 Partially Paid" if d > 0 else "🔴 Unpaid")
                m_table_rows += f"| {idx} | **{m['stage_name']}** | ₹ {p:,.2f} | ₹ {d:,.2f} | ₹ {bal:,.2f} | {st_text} |\n"

            st.markdown(
                f"""
| # | कामाचा टप्पा | ठरलेले बिल | जमा रक्कम | शिल्लक बाकी | स्थिती |
| :--- | :--- | :--- | :--- | :--- | :--- |
{m_table_rows}
                """
            )
        else:
            st.info("ℹ️ या साईटवर अजून बिलाचे टप्पे ठरवलेले नाहीत.")

    with c_tab2:
        if c_progress:
            for p in c_progress:
                st.markdown(f"**📅 तारीख:** `{p['date']}` | **🚧 टप्पा:** {p['stage_name']} | **प्रगती:** `{p['progress_percent']}%`")
                st.progress(int(p['progress_percent']))
                if p.get("remark"):
                    st.caption(f"📝 **इंजिनिअर शेरा:** {p['remark']}")
                st.write("---")
        else:
            st.info("ℹ️ सध्या कोणताही नवीन प्रोग्रेस रिपोर्ट उपलब्ध नाही.")

    with c_tab3:
        c_stock = {}
        for row in inv_rows:
            mat = row["material_name"]
            ttype = row["transaction_type"]
            qty = float(row["quantity"])
            unit = row["unit"] or "Units"

            key_label = f"{mat} ({unit})"
            if key_label not in c_stock:
                c_stock[key_label] = 0.0
            if "IN" in ttype:
                c_stock[key_label] += qty
            else:
                c_stock[key_label] -= qty

        if c_stock:
            st.markdown("###### 📊 साईटवर सद्यस्थितीत शिल्लक असलेले साहित्य:")
            s_rows = ""
            for s_name, s_count in c_stock.items():
                s_rows += f"| {s_name} | **{s_count:.2f}** |\n"

            st.markdown(
                f"""
| साहित्याचे नाव | शिल्लक प्रमाण |
| :--- | :--- |
{s_rows}
                """
            )
        else:
            st.info("ℹ️ या साईटवर साहित्याची नोंद उपलब्ध नाही.")

    st.stop()


# ==============================================================================
# 📌 विभाग १३: मुख्य युझर डॅशबोर्ड (Compact Header, Site Code Manager & Dedicated Inbox)
# ==============================================================================
# 🌟 फाउंडर मोड फ्लोटिंग बॅनर (ॲडमीनला परत पॅनलवर जाण्यासाठी)
if st.session_state.get("admin_impersonating", False) or st.session_state.get("is_admin_logged", False):
    ret_c1, ret_c2 = st.columns([4, 1.5])
    with ret_c1:
        st.markdown(
            """
            <div style="background:rgba(139,92,246,0.15); border:1px solid #8b5cf6; padding:8px 14px; border-radius:8px;">
                <b style="color:#c4b5fd;">👑 FOUNDER MODE ACTIVE:</b> <span style="color:#ffffff;">All VIP Features Unlocked (Full Free Access)</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with ret_c2:
        if st.button("🛡️ Return to Admin Panel", type="primary", use_container_width=True):
            st.session_state.is_admin_logged = True
            st.session_state.admin_impersonating = False
            st.rerun()
    st.write(" ")

current_user_name = st.session_state.app_user_name
is_user_premium, status_text_str = check_user_premium_status(current_user_name)
current_user_data = get_user_data(current_user_name) or {}

# --- डेटाबेसमधून युझरच्या साईट्स लोड करणे ---
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "SELECT site_code, site_name FROM user_sites WHERE user_key = ? ORDER BY id ASC",
    (current_user_name,),
)
user_sites_db = cursor.fetchall()

# जर युझरची एकही साईट नसेल तर डीफॉल्ट सामान्य साईट सेव्ह करणे
if not user_sites_db:
    default_c = "S1"
    default_n = "Main Project Site"
    now_d = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT OR IGNORE INTO user_sites (user_key, site_code, site_name, created_at) VALUES (?, ?, ?, ?)",
        (current_user_name, default_c, default_n, now_d),
    )
    conn.commit()
    cursor.execute(
        "SELECT site_code, site_name FROM user_sites WHERE user_key = ? ORDER BY id ASC",
        (current_user_name,),
    )
    user_sites_db = cursor.fetchall()
conn.close()

sites_list = [dict(r) for r in user_sites_db] if user_sites_db else [{"site_code": "S1", "site_name": "Main Project Site"}]
available_codes = [s["site_code"] for s in sites_list]

# 🛡️ सुरक्षित कोड तपासणी (ValueError टाळण्यासाठी)
if "active_site_code" not in st.session_state or st.session_state.active_site_code not in available_codes:
    st.session_state.active_site_code = available_codes[0]

# चालू साईटचे नाव मिळवणे
active_site_obj = next((s for s in sites_list if s["site_code"] == st.session_state.active_site_code), sites_list[0])
st.session_state.current_site_name = active_site_obj["site_name"]
active_code_display = active_site_obj["site_code"]

# --- १. अल्ट्रा-कॉम्पॅक्ट स्लीक हेडर ---
st.markdown(
    """
    <div class="brand-header-compact">
        <div class="brand-title-compact">
            <span style="font-size: 20px;">🏗️</span>
            <h2>PATIL INFRATECH</h2>
            <span class="brand-subtext">| Civil Suite & Site Manager</span>
        </div>
        <div>
            <span style="background:rgba(245,158,11,0.12); color:#f59e0b; border:1px solid rgba(245,158,11,0.25); padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700;">
                Console Active
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- २. स्पॉन्सर जाहिरात (असल्यास) ---
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM ads WHERE active = 1 AND position = 'Main App Header (Top Banner)'")
ads_list = [dict(r) for r in cursor.fetchall()]
conn.close()

for ad in ads_list:
    st.markdown(
        f"""
        <div style="background:#111827; border:1px solid #1f2937; padding:6px 12px; border-radius:8px; text-align:center; margin-bottom:10px; font-size:12px;">
            <span style="color:#f59e0b; font-weight:bold;">📢 SPONSOR:</span> 
            <b style="color:#fff; margin-left:4px;">{ad.get('title')}</b> — <span style="color:#94a3b8;">{ad.get('desc')}</span>
            <a href="{ad.get('link')}" target="_blank" style="color:#38bdf8; margin-left:6px; font-weight:600; text-decoration:none;">[भेट द्या]</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- ३. टॉप ॲक्शन बार ---
bar_c1, bar_c2, bar_c3 = st.columns([3.8, 1.8, 1.2])

with bar_c1:
    st.markdown(
        f"""
        <div style="background:#111827; border:1px solid #1f2937; border-left:4px solid #38bdf8; padding:8px 14px; border-radius:8px;">
            <span style="font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase;">Current Active Project:</span><br>
            <b style="color:#ffffff; font-size:15px;"><span style="color:#f59e0b; font-weight:800;">[{active_code_display}]</span> {st.session_state.current_site_name}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bar_c2:
    with st.popover("📂 View All Sites"):
        st.markdown("##### 🏢 Your Projects / Sites")
        st.caption("Select a site to switch, or add a new site in Roman/English script.")

        # १. साईट निवडणे (Safe Index Logic)
        site_options = {f"[{s['site_code']}] {s['site_name']}": s["site_code"] for s in sites_list}
        site_keys_list = list(site_options.keys())

        # सुरक्षित इंडेक्स कॅल्क्युलेशन
        current_selection_idx = 0
        for idx, s in enumerate(sites_list):
            if s["site_code"] == st.session_state.active_site_code:
                current_selection_idx = idx
                break

        selected_display = st.selectbox(
            "Switch Active Site:",
            site_keys_list,
            index=current_selection_idx,
            key="sel_switch_site_box"
        )
        if st.button("🔄 Switch Site", key="btn_switch_site_action", type="primary", use_container_width=True):
            st.session_state.active_site_code = site_options[selected_display]
            st.rerun()

        st.write("---")
        # २. नवीन साईट ॲड करणे
        st.markdown("###### ➕ Add New Project Site")
        new_s_name = st.text_input("Site Name (English/Roman only):", placeholder="Enter Site Name", key="new_s_name_in").strip()
        new_s_code = st.text_input("Site Code (English only):", placeholder="Enter Code (e.g. S1)", key="new_s_code_in").strip().upper()

        if st.button("💾 Save New Site", key="btn_save_new_site_code", use_container_width=True):
            is_valid_name = bool(re.match(r"^[A-Za-z0-9\s\-]+$", new_s_name))
            is_valid_code = bool(re.match(r"^[A-Za-z0-9\-]+$", new_s_code))

            if not new_s_name or not new_s_code:
                st.warning("⚠️ Please fill both Site Name and Site Code.")
            elif not is_valid_name or not is_valid_code:
                st.error("❌ Devanagari not allowed! Please use only English/Roman characters (A-Z, 0-9).")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT site_code FROM user_sites WHERE user_key = ? AND site_code = ?",
                    (current_user_name, new_s_code),
                )
                if cursor.fetchone():
                    conn.close()
                    st.error(f"❌ Code '{new_s_code}' is already used. Choose another code.")
                else:
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        "INSERT INTO user_sites (user_key, site_code, site_name, created_at) VALUES (?, ?, ?, ?)",
                        (current_user_name, new_s_code, new_s_name, now_str),
                    )
                    conn.commit()
                    conn.close()
                    st.session_state.active_site_code = new_s_code
                    st.success(f"✅ Site [{new_s_code}] {new_s_name} created successfully!")
                    st.rerun()

with bar_c3:
    if st.button("🚪 Logout", key="top_logout_btn", use_container_width=True):
        st.session_state.app_user_name = None
        st.session_state.otp_verified = False
        st.session_state.admin_impersonating = False
        if "saved_user" in st.query_params:
            del st.query_params["saved_user"]
        st.session_state.selected_module = None
        st.markdown("<script>localStorage.removeItem('patil_app_user');</script>", unsafe_allow_html=True)
        st.rerun()

# --- ४. युझरचा अधिकृत इनबॉक्स व मेसेज सेंटर ---
has_unread = current_user_data.get("unread_notification", 0) == 1
admin_message_content = current_user_data.get("admin_message", "")

if has_unread:
    st.markdown(
        f"""
        <div class="inbox-alert-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#10b981; font-size:14px;">🔔 नवीन ॲडमीन संदेश / कोड आला आहे!</b>
                <span style="background:#ef4444; color:#fff; font-size:10px; font-weight:bold; padding:2px 8px; border-radius:10px;">NEW</span>
            </div>
            <p style="color:#ffffff; font-size:14px; margin:8px 0 6px 0; line-height:1.4;">
                {admin_message_content}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("✅ मेसेज वाचला आहे (Mark as Read)", type="primary", key="btn_read_notice", use_container_width=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET unread_notification = 0 WHERE user_key = ?", (current_user_name,))
        conn.commit()
        conn.close()
        st.rerun()
else:
    inbox_label = f"📥 इनबॉक्स व ॲडमीन संदेश ({current_user_name})"
    with st.expander(inbox_label, expanded=False):
        if admin_message_content:
            st.markdown(f"**शेवटचा मेसेज:**\n\n> {admin_message_content}")
        else:
            st.info("ℹ️ इनबॉक्समध्ये सध्या कोणताही नवीन संदेश नाही.")

# --- ५. प्रिमियम कोड अनलॉक व ॲक्टिव्हेशन (Free Users Only) ---
if not is_user_premium:
    with st.expander("🔑 प्रिमियम कोड अनलॉक करा (Enter Code)"):
        input_code = st.text_input("Activation Code:", placeholder="Code टाका", key="home_code_input").strip()
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔓 Activate Premium", key="btn_activate_prem_main", type="primary", use_container_width=True):
                u_info = get_user_data(current_user_name) or {}
                if input_code == "4528":
                    uses_count = u_info.get("master_code_uses", 0)
                    if uses_count >= 3:
                        st.error("❌ या कोडची मर्यादा संपली आहे!")
                    else:
                        exp_str = (get_ist_time() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET master_code_uses = ?, is_premium = 1, premium_expiry = ? WHERE user_key = ?", (uses_count + 1, exp_str, current_user_name))
                        conn.commit()
                        conn.close()
                        st.success("🎉 ८ तासांचे प्रिमियम अनलॉक झाले!")
                        st.rerun()
                elif input_code in ["admin_master", "vip_access"]:
                    exp_str = (get_ist_time() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET is_premium = 1, premium_expiry = ? WHERE user_key = ?", (exp_str, current_user_name))
                    conn.commit()
                    conn.close()
                    st.success("🎉 प्रिमियम सुरू झाले!")
                    st.rerun()
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM premium_codes WHERE code = ?", (input_code,))
                    c_row = cursor.fetchone()
                    if c_row and dict(c_row).get("used") == 0:
                        exp_str = (get_ist_time() + datetime.timedelta(days=28)).strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute("UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?", (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), input_code))
                        cursor.execute("UPDATE users SET is_premium = 1, premium_expiry = ? WHERE user_key = ?", (exp_str, current_user_name))
                        conn.commit()
                        conn.close()
                        st.success("🎉 प्रिमियम अनलॉक झाले!")
                        st.rerun()
                    else:
                        conn.close()
                        st.error("❌ अमान्य कोड!")
        with c_btn2:
            if st.button("📩 Request Code from Admin", key="btn_req_code_main", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET requested_code = 1 WHERE user_key = ?", (current_user_name,))
                conn.commit()
                conn.close()
                st.success("✅ ॲडमीनला कोडसाठी रिक्वेस्ट पाठवली!")

st.write("---")
# ==========================================
# 📌 विभाग १४: CIVIL AI ASSISTANT (Gemini SDK & Fallback)
# ==========================================
locks_cfg = get_feature_locks()
ai_lock_setting = locks_cfg.get("Civil AI Assistant", "Premium")

if ai_lock_setting == "Free" or is_user_premium:
    with st.expander("🤖 Patil Infratech Civil AI Assistant (Ask Anything)"):
        user_ai_query = st.text_input("प्रश्न किंवा शंका इथे लिहा:", placeholder="उदा. What is the dry volume factor for concrete...", key="civil_ai_input")
        if st.button("🚀 Ask Civil AI", type="primary", use_container_width=True):
            if user_ai_query.strip():
                api_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY", "")
                ai_response_text = ""
                if HAS_GENAI and api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = f"You are a Senior Civil Engineer for Patil Infratech. Provide a direct, professional, and precise engineering answer: {user_ai_query}"
                        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                        if response and response.text:
                            ai_response_text = response.text
                    except Exception:
                        ai_response_text = ""

                if not ai_response_text:
                    q_lower = user_ai_query.lower()
                    if "cement bag" in q_lower or "volume" in q_lower:
                        ai_response_text = "👷‍♂️ **Expert Answer:**\n• Weight: **50 kg**\n• Density: **1440 kg/m³**\n• Volume: **0.0347 m³ (1.225 CFT)**"
                    elif "concrete" in q_lower or "dry volume" in q_lower:
                        ai_response_text = "👷‍♂️ **Expert Answer:**\n• Concrete dry volume factor is **1.54**."
                    else:
                        ai_response_text = f"👷‍♂️ **Analysis:** Please check IS-456 standards or use our built-in modules for *'{user_ai_query}'*."

                st.markdown(
                    f"""
                    <div style="background:#111827; border-left:4px solid #38bdf8; padding:14px; border-radius:8px; margin-top:10px;">
                        <b>🎯 Answer:</b><br><br>{ai_response_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("⚠️ कृपया आधी प्रश्न लिहा!")
else:
    st.info("🔒 Civil AI Assistant हे प्रिमियम फिचर आहे.")


# ==========================================
# 📌 विभाग १५: मुख्य मॉड्यूल निवड कार्ड्स (Responsive Dashboard Grid)
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("<h4 style='text-align:center; margin-bottom:16px;'>🚀 कृपया मॉड्यूल निवडा</h4>", unsafe_allow_html=True)

    calc_lock = locks_cfg.get("Civil Calculator", "Free")
    site_lock = locks_cfg.get("Site Manager", "Free")
    neev_lock = locks_cfg.get("NeevPay", "Free")

    # डेस्कटॉपवर ४ कॉलम्स आणि मोबाईलवर २x२ आपोआप ॲडजस्ट होणारे कॉलम्स
    main_col1, main_col2 = st.columns(2)
    main_col3, main_col4 = st.columns(2)

    # १. साईट मॅनेजर
    with main_col1:
        st.markdown(
            f"""
            <div class="module-card">
                <div style="font-size: 34px; margin-bottom: 6px;">👷‍♂️</div>
                <h4 style="margin: 0; color: #ffffff; font-weight: 700;">Site Manager</h4>
                <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 10px 0;">हजेरी, मजुरी, इन्व्हेंटरी व दैनिक प्रोग्रेस</p>
                <span class="{'free-user-badge' if site_lock == 'Free' else 'gold-vip-badge'}">[{'Free' if site_lock == 'Free' else 'VIP'}]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("👷‍♂️ Open Site Manager", key="btn_open_site", use_container_width=True, type="primary"):
            if site_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे प्रिमियम फीचर आहे!")
            else:
                st.session_state.selected_module = "Site Manager"
                st.session_state.selected_site_sub_module = None
                trigger_push_state()
                st.rerun()

    # २. एस्टिमेटर टूल्स
    with main_col2:
        st.markdown(
            """
            <div class="module-card">
                <div style="font-size: 34px; margin-bottom: 6px;">📐</div>
                <h4 style="margin: 0; color: #ffffff; font-weight: 700;">Estimator Tools</h4>
                <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 10px 0;">Rate Analysis, BBS Schedule, QS & 3-in-1 PDF</p>
                <span class="gold-vip-badge">[5 Advanced Tools]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("📐 Open Estimator Tools", key="btn_open_estimator", use_container_width=True, type="primary"):
            st.session_state.selected_module = "Estimator Tools"
            st.session_state.selected_estimator_sub_module = None
            trigger_push_state()
            st.rerun()

    st.write(" ")

    # ३. NeevPay
    with main_col3:
        st.markdown(
            f"""
            <div class="module-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <div style="font-size: 34px; margin-bottom: 6px;">🤝</div>
                <h4 style="margin: 0; color: #10b981; font-weight: 700;">NeevPay Escrow</h4>
                <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 10px 0;">टप्प्याटप्प्याने पेमेंट, एस्क्रो व डिजिटल संमती</p>
                <span class="{'free-user-badge' if neev_lock == 'Free' else 'gold-vip-badge'}">[{'Free' if neev_lock == 'Free' else 'VIP'}]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("🤝 Open NeevPay", key="btn_open_neevpay", use_container_width=True, type="primary"):
            if neev_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे प्रिमियम फीचर आहे!")
            else:
                st.session_state.selected_module = "NeevPay"
                trigger_push_state()
                st.rerun()

    # ४. हाउस एस्टिमेटर
    with main_col4:
        st.markdown(
            """
            <div class="module-card" style="border-color: rgba(56, 189, 248, 0.4);">
                <div style="font-size: 34px; margin-bottom: 6px;">🏠</div>
                <h4 style="margin: 0; color: #38bdf8; font-weight: 700;">House Estimator</h4>
                <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 10px 0;">घराचे बजेट, सिमेंट-स्टील थंब रूल कोटेशन</p>
                <span class="free-user-badge">[Quick Engine]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("🏠 Open House Estimator", key="btn_open_house_est", use_container_width=True, type="primary"):
            st.session_state.selected_module = "House Estimator"
            trigger_push_state()
            st.rerun()

# ==========================================
# 📌 विभाग १६: ESTIMATOR TOOLS मुख्य मॉड्यूल (Corporate & 100% IS-Code Compliant)
# ==========================================
elif st.session_state.selected_module == "Estimator Tools":
    col_back, _ = st.columns([1.5, 3.5])
    with col_back:
        if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_estimator", use_container_width=True):
            st.session_state.selected_module = None
            st.session_state.selected_estimator_sub_module = None
            st.rerun()

    st.write("---")

    calc_lock = locks_cfg.get("Civil Calculator", "Free")
    ra_lock = locks_cfg.get("Rate Analysis", "Free")
    bbs_lock = locks_cfg.get("BBS", "Free")
    qs_lock = locks_cfg.get("Quantity Surveying", "Free")

    # ==========================================================================
    # १६.० मास्टर ३-इन-१ कंबाइन्ड एक्झिक्युटिव्ह PDF / HTML रिपोर्ट
    # ==========================================================================
    def render_combined_master_report(user_key, site_name):
        st.markdown(f"#### 📑 Executive Master Estimate: `{site_name}`")
        st.caption("💡 मागील ७ दिवसांमधील Rate Analysis, BBS आणि Quantity Survey चा सर्वसमावेशक IS-Code फॉरमॅट ३-इन-१ रिपोर्ट.")

        conn = get_db_connection()
        cursor = conn.cursor()
        seven_days_ago = (get_ist_time() - datetime.timedelta(days=7)).strftime("%Y-%m-%d 00:00:00")
        cursor.execute(
            """
            SELECT timestamp, user_note, report_data FROM history 
            WHERE user_key = ? AND (site_name = ? OR site_name IS NULL) AND timestamp >= ?
            ORDER BY id ASC
            """,
            (user_key, site_name, seven_days_ago),
        )
        records = cursor.fetchall()
        conn.close()

        if not records:
            st.warning(f"⚠️ '{site_name}' साठी मागील ७ दिवसांत कोणतेही कॅल्क्युलेशन सेव्ह केलेले नाही. आधी खालील टूल्स वापरून हिशोब तयार करा.")
            return

        def markdown_to_html_table(md_text):
            lines = [line.strip() for line in md_text.strip().split("\n") if line.strip().startswith("|")]
            if not lines:
                return f"<div style='padding:8px; background:#f8fafc; font-size:12px;'>{md_text}</div>"
            
            html_table = "<table class='custom-data-table'>"
            for i, line in enumerate(lines):
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if i == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cells):
                    continue
                if i == 0:
                    html_table += "<thead><tr>"
                    for c in cells:
                        html_table += f"<th>{c}</th>"
                    html_table += "</tr></thead><tbody>"
                else:
                    html_table += "<tr>"
                    for c in cells:
                        bold_formatted = c.replace("**", "<b>").replace("**", "</b>")
                        html_table += f"<td>{bold_formatted}</td>"
                    html_table += "</tr>"
            html_table += "</tbody></table>"
            return html_table

        full_html_doc = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>PATIL INFRATECH - {site_name} Master Estimate</title>
            <style>
                @page {{ size: A4 portrait; margin: 10mm; }}
                @media print {{
                    body {{ background: #ffffff !important; color: #000000 !important; }}
                    .no-print {{ display: none !important; }}
                    .page-break {{ page-break-before: always !important; break-before: page !important; }}
                }}
                body {{ background-color: #f1f5f9; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 10px; color: #0f172a; }}
                .a4-page {{ position: relative; background: #ffffff; width: 100%; max-width: 800px; margin: 0 auto 25px auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1.5px solid #0f172a; box-sizing: border-box; min-height: 1050px; overflow: hidden; }}
                .watermark {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg); font-size: 24px; font-weight: 900; color: rgba(15, 23, 42, 0.06); text-transform: uppercase; letter-spacing: 3px; text-align: center; width: 85%; pointer-events: none; border: 4px dashed rgba(15, 23, 42, 0.06); padding: 25px; border-radius: 12px; z-index: 1; }}
                .content-box {{ position: relative; z-index: 2; }}
                .header-title {{ text-align: center; border-bottom: 2.5px solid #0f172a; padding-bottom: 8px; margin-bottom: 14px; }}
                .header-title h1 {{ margin: 0; font-size: 24px; color: #0f172a; font-weight: 900; }}
                .header-title p {{ margin: 3px 0; font-size: 11px; font-weight: 700; color: #475569; }}
                table.info-table {{ width: 100%; margin-bottom: 12px; font-size: 12px; border-collapse: collapse; }}
                table.info-table td {{ padding: 3px 0; }}
                .section-header {{ background: #0f172a; color: #ffffff; padding: 7px 14px; font-size: 13px; font-weight: bold; border-radius: 4px; margin: 14px 0 10px 0; }}
                table.custom-data-table {{ width: 100%; border-collapse: collapse; margin: 8px 0 16px 0; font-size: 11px; }}
                table.custom-data-table th, table.custom-data-table td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
                table.custom-data-table th {{ background-color: #f8fafc; font-weight: bold; color: #0f172a; }}
                table.custom-data-table tr:nth-child(even) {{ background-color: #fcfdfe; }}
                .signature-box {{ margin-top: 50px; width: 100%; font-size: 12px; }}
                .footer-stamp {{ text-align: center; margin-top: 30px; font-size: 10px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 6px; }}
            </style>
        </head>
        <body>
        """

        for idx, r in enumerate(records, 1):
            page_break_class = "page-break" if idx > 1 else ""
            table_content_html = markdown_to_html_table(r['report_data'])

            full_html_doc += f"""
            <div class="a4-page {page_break_class}">
                <div class="watermark">PATIL INFRATECH • OFFICIAL MASTER ESTIMATE</div>
                <div class="content-box">
                    <div class="header-title">
                        <h1>PATIL INFRATECH</h1>
                        <p>CIVIL ENGINEERS • ARCHITECTURAL CONSULTANTS • QUANTITY SURVEYORS</p>
                        <small style="color: #64748b;">(Certified Compliant with IS 1200, IS 456, IS 2502 & IS 1077 Standards)</small>
                    </div>

                    <table class="info-table">
                        <tr>
                            <td><b>📍 Project / Site:</b> <span style="color:#d97706; font-weight:bold;">{site_name}</span></td>
                            <td style="text-align: right;"><b>📅 Report Date:</b> {get_ist_time().strftime('%d-%m-%Y')}</td>
                        </tr>
                        <tr>
                            <td><b>👤 Site Engineer:</b> {user_key}</td>
                            <td style="text-align: right;"><b>📄 Page:</b> {idx} of {len(records)}</td>
                        </tr>
                        <tr>
                            <td colspan="2"><b>📝 Activity / Note:</b> {r['user_note']}</td>
                        </tr>
                    </table>
                    <hr style="border: 0.5px solid #cbd5e1; margin-bottom: 8px;">

                    <div class="section-header">
                        विभाग #{idx}: {r['user_note']} (नोंद वेळ: {r['timestamp']})
                    </div>

                    {table_content_html}

                    <table class="signature-box">
                        <tr>
                            <td style="width: 50%;">
                                <br><br>
                                __________________________<br>
                                <b>Site Engineer Signature</b><br>
                                <small style="color:#64748b;">Patil Infratech Site Office</small>
                            </td>
                            <td style="width: 50%; text-align: right;">
                                <br><br>
                                __________________________<br>
                                <b>Project Manager / Checker</b><br>
                                <small style="color:#64748b;">Quality & Audit Control</small>
                            </td>
                        </tr>
                    </table>

                    <div class="footer-stamp">
                        System Verified & Generated by: <b>Patil Infratech Corporate Engine</b> • Date: {get_ist_time().strftime('%d-%m-%Y %H:%M:%S')}
                    </div>
                </div>
            </div>
            """

        full_html_doc += """
        </body>
        </html>
        """

        st.components.v1.html(full_html_doc, height=540, scrolling=True)

        excel_data_list = []
        for r in records:
            excel_data_list.append({
                "Site Name": site_name,
                "Engineer": user_key,
                "Timestamp": r["timestamp"],
                "Note": r["user_note"],
                "Raw Data": r["report_data"].replace("|", " ").strip()
            })
        excel_df = pd.DataFrame(excel_data_list)
        csv_bytes = excel_df.to_csv(index=False).encode('utf-8-sig')

        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                label="📥 Download Master HTML/PDF",
                data=full_html_doc,
                file_name=f"Patil_Infratech_{site_name.replace(' ', '_')}_Master_Report.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
        with c2:
            st.download_button(
                label="📊 Export Full CSV Data",
                data=csv_bytes,
                file_name=f"Patil_Infratech_{site_name.replace(' ', '_')}_Data.csv",
                mime="text/csv",
                use_container_width=True
            )
        with c3:
            st.markdown(
                """
                <button onclick="window.parent.print()" style="width: 100%; background: #0284c7; color: white; border: none; padding: 9px 14px; border-radius: 8px; font-weight: 700; cursor: pointer; height: 38px;">
                    🖨️ Instant Print (A4)
                </button>
                """,
                unsafe_allow_html=True,
            )

        wa_text = (
            f"🏗️ *PATIL INFRATECH - EXECUTIVE ESTIMATE REPORT*\n"
            f"📍 *Site:* {site_name}\n👤 *Engineer:* {user_key}\n"
            f"📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
            f"✅ Complete 3-in-1 Report generated as per IS-Codes.\n"
            f"_Patil Infratech Authorized Console_"
        )
        st.write(" ")
        render_whatsapp_feature(urllib.parse.quote(wa_text), "master_pdf_wa")

    # ==========================================================================
    # सब-मॉड्यूल ग्रिड नेव्हिगेशन
    # ==========================================================================
    if st.session_state.selected_estimator_sub_module is None:
        st.markdown("<h4 style='margin-bottom:14px;'>📐 Estimator Tools Dashboard</h4>", unsafe_allow_html=True)

        e_col1, e_col2 = st.columns(2)
        with e_col1:
            st.markdown(
                f"""
                <div class="module-card">
                    <div style="font-size: 32px; margin-bottom: 4px;">🧮</div>
                    <b style="color: #f8fafc; font-size: 14px;">Civil Calculator</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">Brass, CFT, m³, गुंठा व एरिया कनव्हर्टर</p>
                    <span class="{'free-user-badge' if calc_lock == 'Free' else 'gold-vip-badge'}" style="margin-top:6px;">[{calc_lock}]</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Calculator", key="btn_est_calc", use_container_width=True):
                if calc_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे प्रिमियम फीचर आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Calculator"
                    trigger_push_state()
                    st.rerun()

        with e_col2:
            st.markdown(
                f"""
                <div class="module-card">
                    <div style="font-size: 32px; margin-bottom: 4px;">📊</div>
                    <b style="color: #f8fafc; font-size: 14px;">Rate Analysis</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">IS 456 काँक्रीट, विटांचे बांधकाम व प्लास्टर दर</p>
                    <span class="{'free-user-badge' if ra_lock == 'Free' else 'gold-vip-badge'}" style="margin-top:6px;">[{ra_lock}]</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Rate Analysis", key="btn_est_ra", use_container_width=True):
                if ra_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे प्रिमियम फीचर आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Rate Analysis"
                    trigger_push_state()
                    st.rerun()

        st.write(" ")
        e_col3, e_col4 = st.columns(2)
        with e_col3:
            st.markdown(
                f"""
                <div class="module-card">
                    <div style="font-size: 32px; margin-bottom: 4px;">🏗️</div>
                    <b style="color: #f8fafc; font-size: 14px;">BBS Calculator</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">Footing, Column, Beam व Slab स्टील शेड्युल</p>
                    <span class="{'free-user-badge' if bbs_lock == 'Free' else 'gold-vip-badge'}" style="margin-top:6px;">[{bbs_lock}]</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open BBS", key="btn_est_bbs", use_container_width=True):
                if bbs_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे प्रिमियम फीचर आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "BBS"
                    trigger_push_state()
                    st.rerun()

        with e_col4:
            st.markdown(
                f"""
                <div class="module-card">
                    <div style="font-size: 32px; margin-bottom: 4px;">📈</div>
                    <b style="color: #f8fafc; font-size: 14px;">Quantity Surveying</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">मोजमाप पुस्तिका, Deductions व ॲब्स्ट्रॅक्ट शीट</p>
                    <span class="{'free-user-badge' if qs_lock == 'Free' else 'gold-vip-badge'}" style="margin-top:6px;">[{qs_lock}]</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Quantity Survey", key="btn_est_qs", use_container_width=True):
                if qs_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे प्रिमियम फीचर आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Quantity Surveying"
                    trigger_push_state()
                    st.rerun()

        st.write(" ")
        st.markdown(
            """
            <div class="module-card" style="border-color: rgba(245, 158, 11, 0.4);">
                <div style="font-size: 32px; margin-bottom: 4px;">📑</div>
                <b style="color: #f59e0b; font-size: 15px;">3-in-1 Executive Master PDF</b>
                <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">Rate Analysis + BBS + QS कंबाइन्ड व्हॅलिडेटेड रिपोर्ट</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("📑 Generate Master PDF Report", key="btn_est_master_pdf", use_container_width=True, type="primary"):
            st.session_state.selected_estimator_sub_module = "Master PDF"
            trigger_push_state()
            st.rerun()

    else:
        col_b_menu, _ = st.columns([1.5, 3.5])
        with col_b_menu:
            if st.button("⬅️ Estimator Menu वर जा", key="btn_back_estimator_menu", use_container_width=True):
                st.session_state.selected_estimator_sub_module = None
                st.rerun()

        st.write("---")
        est_sub_mod = st.session_state.selected_estimator_sub_module

        # १६.० Master 3-in-1 Combined Estimate PDF
        if est_sub_mod == "Master PDF":
            render_combined_master_report(current_user_name, st.session_state.current_site_name)

        # ======================================================================
        # १६.१ Civil Calculator & Smart Unit Converter
        # ======================================================================
        elif est_sub_mod == "Calculator":
            st.markdown("#### 🧮 Civil Smart Unit Converter")
            st.caption("💡 एकाच बॉक्समध्ये मूल्य भरा आणि सर्व युनिट्समधील अचूक हिशोब एकाच झटक्यात मिळवा!")

            conv_category = st.selectbox("कनव्हर्शन प्रकार निवडा:", [
                "📦 Volume / Brass Converter (घनफळ आणि ब्रास)",
                "📏 Length Converter (लांबी मोजमाप)",
                "📐 Area Converter (क्षेत्रफळ मोजमाप)",
            ])

            if "Volume / Brass" in conv_category:
                v_c1, v_c2 = st.columns(2)
                with v_c1:
                    val = st.number_input("मूल्य भरा (Value):", min_value=0.0, value=1.0, step=0.1, key="v_val")
                with v_c2:
                    unit_from = st.selectbox("मूळ युनिट:", ["Cubic Meter (m³)", "Cubic Feet (CFT)", "Brass"])

                if st.button("⚡ Convert Now", type="primary", key="btn_conv_vol", use_container_width=True):
                    if "Cubic Meter" in unit_from:
                        m3 = val
                    elif "Cubic Feet" in unit_from:
                        m3 = val / 35.3147
                    else:
                        m3 = val * 2.83168

                    brass = m3 / 2.83168
                    cft = m3 * 35.3147
                    liters = m3 * 1000.0

                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 16px; border-radius: 10px; border-left: 4px solid #38bdf8; margin-top: 10px;">
                            <p style="margin: 4px 0;"><b>📦 ब्रास (Brass):</b> <span style="color:#f59e0b; font-weight:bold; font-size:16px;">{brass:.4f} Brass</span></p>
                            <p style="margin: 4px 0;"><b>📐 घन फूट (CFT):</b> <code>{cft:.2f} CFT</code></p>
                            <p style="margin: 4px 0;"><b>📏 घन मीटर (m³):</b> <code>{m3:.4f} m³</code></p>
                            <p style="margin: 4px 0;"><b>💧 लिटर:</b> <code>{liters:.2f} Ltrs</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            elif "Length Converter" in conv_category:
                l_c1, l_c2 = st.columns(2)
                with l_c1:
                    val = st.number_input("लांबी भरा:", min_value=0.0, value=1.0, step=0.1, key="l_val")
                with l_c2:
                    unit_from = st.selectbox("मूळ युनिट:", ["Meters", "Feet", "Inches", "Millimeters (mm)", "Centimeters (cm)"])

                if st.button("⚡ Convert Now", type="primary", key="btn_conv_len", use_container_width=True):
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

                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 16px; border-radius: 10px; border-left: 4px solid #38bdf8; margin-top: 10px;">
                            <p style="margin: 4px 0;"><b>📏 मीटर:</b> <span style="color:#f59e0b; font-weight:bold;">{meters:.4f} m</span></p>
                            <p style="margin: 4px 0;"><b>🦶 फूट:</b> <code>{feet:.4f} ft</code> | <b>इंच:</b> <code>{inches:.2f} in</code></p>
                            <p style="margin: 4px 0;"><b>मिलिमीटर:</b> <code>{mm:.2f} mm</code> | <b>सेंटीमीटर:</b> <code>{cm:.2f} cm</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:
                a_c1, a_c2 = st.columns(2)
                with a_c1:
                    val = st.number_input("क्षेत्रफळ भरा:", min_value=0.0, value=100.0, step=10.0, key="a_val")
                with a_c2:
                    unit_from = st.selectbox("मूळ युनिट:", ["Sq. Meters (m²)", "Sq. Feet (Sq. Ft.)", "Guntha", "Acre"])

                if st.button("⚡ Convert Now", type="primary", key="btn_conv_area", use_container_width=True):
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

                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 16px; border-radius: 10px; border-left: 4px solid #38bdf8; margin-top: 10px;">
                            <p style="margin: 4px 0;"><b>📐 स्क्वेअर फूट:</b> <span style="color:#f59e0b; font-weight:bold;">{sqft:.2f} sq.ft.</span></p>
                            <p style="margin: 4px 0;"><b>📏 स्क्वेअर मीटर:</b> <code>{sqm:.2f} m²</code></p>
                            <p style="margin: 4px 0;"><b>🌾 गुंठा:</b> <code>{guntha:.4f} Guntha</code> | <b>एकर:</b> <code>{acre:.4f} Acre</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # ======================================================================
        # १६.२ Rate Analysis Module (100% IS Code & CPWD Standard)
        # ======================================================================
        elif est_sub_mod == "Rate Analysis":
            master_rates = get_market_rates()
            st.markdown(
                f"""
                <div style="background:#111827; border:1px solid #1f2937; border-left:4px solid #f59e0b; padding:10px 14px; border-radius:8px; margin-bottom:14px; font-size:12px;">
                    📢 <b>चालू मार्केट दर:</b> Cement: ₹{master_rates.get('cement', 400.0):.2f}/bag | Sand: ₹{master_rates.get('sand', 2500.0):.2f}/m³ | Agg: ₹{master_rates.get('aggregate', 2200.0):.2f}/m³ | Steel: ₹{master_rates.get('steel', 60.0):.2f}/Kg | Brick: ₹{master_rates.get('bricks', 8.0):.2f}/nos
                </div>
                """,
                unsafe_allow_html=True,
            )

            main_choice = st.radio("कामाचा प्रकार निवडा:", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)", "Plaster Work (प्लास्टर काम)"], horizontal=True)

            # [१] Concrete Work (IS 456)
            if "Concrete Work" in main_choice:
                st.markdown("##### 🧱 Concrete Work Rate Analysis (IS 456)")
                col1, col2 = st.columns(2)
                with col1:
                    grade = st.selectbox("काँक्रीट ग्रेड निवडा:", ["M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"], index=2)
                with col2:
                    component = st.selectbox("आरसीसी घटक निवडा:", ["Footing (0.8% Steel)", "Slab (1.0% Steel)", "Beam (2.0% Steel)", "Column (2.5% Steel)", "Plain Concrete (0% Steel)"], index=1)

                c_r, s_r, a_r = (1.0, 3.0, 6.0) if "M10" in grade else ((1.0, 2.0, 4.0) if "M15" in grade else ((1.0, 1.5, 3.0) if "M20" in grade else (1.0, 1.0, 2.0)))
                steel_pct = 0.8 if "Footing" in component else (1.0 if "Slab" in component else (2.0 if "Beam" in component else (2.5 if "Column" in component else 0.0)))

                st.markdown("###### [A] साहित्याचे मोजमाप व दर")
                v_col1, v_col2 = st.columns(2)
                with v_col1:
                    volume = st.number_input("काँक्रीट घनफळ (Volume in m³):", min_value=0.1, value=1.0, step=0.5, key="cc_vol")
                    cement_rate = st.number_input("सिमेंट दर (₹/bag):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="cc_cem_r")
                    sand_rate = st.number_input("वाळू दर प्रति m³ (₹/m³):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="cc_snd_r")
                with v_col2:
                    aggregate_rate = st.number_input("खडी दर प्रति m³ (₹/m³):", min_value=0.0, value=float(master_rates.get("aggregate", 2200.0)), key="cc_agg_r")
                    steel_rate = st.number_input("स्टील दर (₹/Kg):", min_value=0.0, value=float(master_rates.get("steel", 60.0)), key="cc_stl_r") if steel_pct > 0 else 0.0

                st.markdown("###### [B] मजुरी व लेबर खर्च (नसल्यास ० ठेवा)")
                l_col1, l_col2, l_col3 = st.columns(3)
                with l_col1:
                    mason_qty = st.number_input("मेसन (Days):", min_value=0.0, value=0.5, step=0.5, key="cc_msn_q")
                    mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=750.0, key="cc_msn_r")
                with l_col2:
                    mazdoor_qty = st.number_input("मजदूर (Days):", min_value=0.0, value=2.0, step=0.5, key="cc_mzd_q")
                    mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=500.0, key="cc_mzd_r")
                with l_col3:
                    bb_qty = st.number_input("बार बेंडर (Days):", min_value=0.0, value=0.5 if steel_pct > 0 else 0.0, step=0.5, key="cc_bb_q")
                    bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=700.0, key="cc_bb_r")

                st.markdown("###### [C] अवांतर खर्च व नफा")
                o_col1, o_col2 = st.columns(2)
                with o_col1:
                    scaffolding_cost = st.number_input("सेंटरिंग / शटरिंग खर्च (₹):", min_value=0.0, value=350.0 if "Plain" not in component else 0.0, step=50.0, key="cc_scaf")
                    contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=100.0, step=25.0, key="cc_cont")
                with o_col2:
                    water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=1.0, step=0.5, key="cc_wat_p")
                    profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0, step=1.0, key="cc_prof_p")

                user_note = st.text_input("या एस्टिमेशनची नोट (Note):", placeholder="उदा. Ground floor slab casting...", key="cc_note")

                if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="cc_report_btn", use_container_width=True):
                    dry_volume = volume * 1.54
                    total_parts = c_r + s_r + a_r
                    c_bags = math.ceil(((c_r / total_parts) * dry_volume) * 28.8)
                    s_m3 = (s_r / total_parts) * dry_volume
                    a_m3 = (a_r / total_parts) * dry_volume
                    s_brass = s_m3 / 2.83168
                    a_brass = a_m3 / 2.83168
                    steel_qty = volume * (steel_pct / 100.0) * 7850.0

                    c_cost = c_bags * cement_rate
                    s_cost = s_m3 * sand_rate
                    a_cost = a_m3 * aggregate_rate
                    stl_cost = steel_qty * steel_rate
                    mat_cost = c_cost + s_cost + a_cost + stl_cost

                    lab_cost = (mason_qty * mason_rate) + (mazdoor_qty * mazdoor_rate) + (bb_qty * bb_rate)
                    extra_cost = scaffolding_cost + contingency_cost
                    base_total = mat_cost + lab_cost + extra_cost
                    w_amt = base_total * (water_pct / 100.0)
                    p_amt = base_total * (profit_pct / 100.0)
                    grand_total = base_total + w_amt + p_amt

                    st.success(f"🎉 एकूण काँक्रीट दर: ₹ {grand_total:,.2f}/- ({volume} m³ साठी)")

                    steel_row = f"| Steel Reinforcement | {steel_qty:.2f} | Kg | {steel_rate:.2f} | {stl_cost:.2f} |\n" if steel_pct > 0 else ""

                    report_table = f"""
| तपशील (Item) | प्रमाण (Quantity) | एकक (Unit) | दर (Rate ₹) | एकूण रक्कम (Amount ₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] साहित्याचा खर्च (Material)** | | | | |
| Cement (IS PPC/OPC) | {c_bags} | Bags | {cement_rate:.2f} | {c_cost:.2f} |
| Sand (वाळू) | {s_m3:.2f} ({s_brass:.2f} Brass) | m³ | {sand_rate:.2f} | {s_cost:.2f} |
| Aggregate (खडी) | {a_m3:.2f} ({a_brass:.2f} Brass) | m³ | {aggregate_rate:.2f} | {a_cost:.2f} |
{steel_row}| **[B] मजुरी व लेबर (Labour)** | | | | |
| Mason (गवंडी) | {mason_qty} | Days | {mason_rate:.2f} | {mason_qty*mason_rate:.2f} |
| Mazdoor (मजदूर) | {mazdoor_qty} | Days | {mazdoor_rate:.2f} | {mazdoor_qty*mazdoor_rate:.2f} |
| Bar Bender (फिटर) | {bb_qty} | Days | {bb_rate:.2f} | {bb_qty*bb_rate:.2f} |
| **[C] अवांतर खर्च (Overheads)** | | | | |
| Shuttering / Scaffolding | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies (आकस्मिक) | - | L.S. | - | {contingency_cost:.2f} |
| **एकूण पायाभूत खर्च (Subtotal A+B+C)** | | | | **₹ {base_total:.2f}** |
| Water Charges ({water_pct}%) | - | - | - | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | - | - | - | {p_amt:.2f} |
| **फायनल ग्रँड टोटल (Grand Total)** | | | | **₹ {grand_total:,.2f}/-** |
"""
                    st.markdown(report_table)

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), f"Concrete {grade.split(' ')[0]} - {user_note}", report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

                    msg_text = f"🏗️ *PATIL INFRATECH - CONCRETE RATE ANALYSIS*\n👤 *User:* {current_user_name}\n📍 *Site:* {st.session_state.current_site_name}\n🧱 *Grade:* {grade.split(' ')[0]} | *Vol:* {volume} m³\n• Cement: {c_bags} Bags\n• Sand: {s_m3:.2f} m³ ({s_brass:.2f} Brass)\n• Aggregate: {a_m3:.2f} m³ ({a_brass:.2f} Brass)\n💰 *GRAND TOTAL:* ₹{grand_total:,.2f}/-"
                    render_whatsapp_feature(urllib.parse.quote(msg_text), "ra_conc")

            # [२] Brickwork Estimation (IS 2212)
            elif "Brickwork" in main_choice:
                st.markdown("##### 🧱 Brickwork Rate Analysis (IS 2212)")
                mortar_choice = st.selectbox("मॉर्टर मिक्स गुणोत्तर निवडा:", ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"], index=3)
                c_part = 1.0
                s_part = float(mortar_choice.split(":")[1].split(" ")[0])

                st.markdown("###### [A] साहित्याचे मोजमाप व दर")
                bm_col1, bm_col2 = st.columns(2)
                with bm_col1:
                    volume = st.number_input("वीटकामाचे घनफळ (Volume in m³):", min_value=0.1, value=1.0, step=0.5, key="bw_vol")
                    brick_rate = st.number_input("विटांचा दर प्रति हजार नग (₹/1000 Bricks):", min_value=0.0, value=8000.0, step=100.0, key="bw_br")
                with bm_col2:
                    cement_rate = st.number_input("सिमेंट दर (₹/bag):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="bw_cr")
                    sand_rate = st.number_input("वाळू दर प्रति m³ (₹/m³):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="bw_sr")

                st.markdown("###### [B] मजुरी व लेबर खर्च")
                bl_col1, bl_col2 = st.columns(2)
                with bl_col1:
                    mason_qty = st.number_input("मेसन (Days):", min_value=0.0, value=0.7, step=0.1, key="bw_mq")
                    mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=750.0, key="bw_mr")
                with bl_col2:
                    mazdoor_qty = st.number_input("मजदूर (Days):", min_value=0.0, value=1.2, step=0.1, key="bw_mzq")
                    mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=500.0, key="bw_mzr")

                st.markdown("###### [C] अवांतर खर्च व नफा")
                bo_col1, bo_col2 = st.columns(2)
                with bo_col1:
                    scaffolding_cost = st.number_input("पाळत / स्कॅफोल्डिंग खर्च (₹):", min_value=0.0, value=100.0, step=25.0, key="bw_sc")
                    contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=50.0, step=25.0, key="bw_cc")
                with bo_col2:
                    water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=1.0, step=0.5, key="bw_wp")
                    profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0, step=1.0, key="bw_pp")

                user_note = st.text_input("या वीटकामाची नोट (Note):", placeholder="उदा. 9 inch external wall...", key="bw_note")

                if st.button("📊 GENERATE BRICKWORK REPORT", type="primary", key="bw_report_btn", use_container_width=True):
                    total_bricks = math.ceil(volume * 500)
                    dry_mortar_vol = volume * 0.30
                    tot_mortar_parts = c_part + s_part
                    cement_vol = (c_part / tot_mortar_parts) * dry_mortar_vol
                    sand_m3 = (s_part / tot_mortar_parts) * dry_mortar_vol
                    sand_brass = sand_m3 / 2.83168
                    cement_bags = math.ceil(cement_vol * 28.8)

                    b_cost = (total_bricks / 1000.0) * brick_rate
                    c_cost = cement_bags * cement_rate
                    s_cost = sand_m3 * sand_rate
                    mat_cost = b_cost + c_cost + s_cost

                    lab_cost = (mason_qty * mason_rate) + (mazdoor_qty * mazdoor_rate)
                    extra_cost = scaffolding_cost + contingency_cost
                    base_total = mat_cost + lab_cost + extra_cost
                    w_amt = base_total * (water_pct / 100.0)
                    p_amt = base_total * (profit_pct / 100.0)
                    grand_total = base_total + w_amt + p_amt

                    st.success(f"🎉 एकूण वीटकाम खर्च: ₹ {grand_total:,.2f}/- ({volume} m³ साठी)")

                    report_table = f"""
| तपशील (Item) | प्रमाण (Quantity) | एकक (Unit) | दर (Rate ₹) | एकूण रक्कम (Amount ₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] साहित्याचा खर्च (Material)** | | | | |
| Bricks (लाल विटा) | {total_bricks} | Nos | {(brick_rate/1000.0):.2f}/नग | {b_cost:.2f} |
| Cement (IS PPC) | {cement_bags} | Bags | {cement_rate:.2f} | {c_cost:.2f} |
| Sand (वाळू) | {sand_m3:.2f} ({sand_brass:.2f} Brass) | m³ | {sand_rate:.2f} | {s_cost:.2f} |
| **[B] मजुरी व लेबर (Labour)** | | | | |
| Mason (गवंडी) | {mason_qty} | Days | {mason_rate:.2f} | {mason_qty*mason_rate:.2f} |
| Mazdoor (मजदूर) | {mazdoor_qty} | Days | {mazdoor_rate:.2f} | {mazdoor_qty*mazdoor_rate:.2f} |
| **[C] अवांतर खर्च (Overheads)** | | | | |
| Scaffolding / पाळत | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies | - | L.S. | - | {contingency_cost:.2f} |
| **एकूण पायाभूत खर्च (Subtotal A+B+C)** | | | | **₹ {base_total:.2f}** |
| Water Charges ({water_pct}%) | - | - | - | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | - | - | - | {p_amt:.2f} |
| **फायनल ग्रँड टोटल (Grand Total)** | | | | **₹ {grand_total:,.2f}/-** |
"""
                    st.markdown(report_table)

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), f"Brickwork {mortar_choice.split(' ')[0]} - {user_note}", report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

                    msg_text = f"🏗️ *PATIL INFRATECH - BRICKWORK RATE ANALYSIS*\n👤 *User:* {current_user_name}\n📍 *Site:* {st.session_state.current_site_name}\n🧱 *Ratio:* {mortar_choice.split(' ')[0]} | *Vol:* {volume} m³\n• Bricks: {total_bricks} Nos\n• Cement: {cement_bags} Bags\n• Sand: {sand_m3:.2f} m³ ({sand_brass:.2f} Brass)\n💰 *GRAND TOTAL:* ₹{grand_total:,.2f}/-"
                    render_whatsapp_feature(urllib.parse.quote(msg_text), "ra_bw")

            # [३] Plaster Work Estimation (IS 1661)
            else:
                st.markdown("##### 🎨 Plaster Work Rate Analysis (IS 1661)")
                thickness_mm = st.number_input("प्लास्टरची जाडी (Thickness in mm):", min_value=6.0, max_value=25.0, value=12.0, step=1.0, key="pl_thick")
                plaster_mortar = st.selectbox("मॉर्टर मिक्स गुणोत्तर निवडा:", ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"], index=1)
                p_c_part = 1.0
                p_s_part = float(plaster_mortar.split(":")[1].split(" ")[0])

                st.markdown("###### [A] साहित्याचे मोजमाप व दर")
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    plaster_area = st.number_input("प्लास्टर क्षेत्रफळ (Area in m²):", min_value=1.0, value=100.0, step=10.0, key="pl_area")
                    cement_rate = st.number_input("सिमेंट दर (₹/bag):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="pl_cem_r")
                    use_wp = st.checkbox("💧 वॉटरप्रूफिंग कंपाउंड जोडा (1 Kg per Bag)", value=False)
                with p_col2:
                    sand_rate = st.number_input("वाळू दर प्रति m³ (₹/m³):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="pl_snd_r")
                    wp_rate = st.number_input("वॉटरप्रूफिंग दर (₹/Kg):", min_value=0.0, value=140.0, step=10.0, key="pl_wp_r") if use_wp else 0.0

                st.markdown("###### [B] मजुरी व लेबर खर्च")
                pl_l1, pl_l2 = st.columns(2)
                with pl_l1:
                    pl_mason_qty = st.number_input("मेसन (Days):", min_value=0.0, value=2.0, step=0.5, key="pl_mq")
                    pl_mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=750.0, key="pl_mr")
                with pl_l2:
                    pl_mazdoor_qty = st.number_input("मजदूर (Days):", min_value=0.0, value=3.0, step=0.5, key="pl_mzq")
                    pl_mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=500.0, key="pl_mzr")

                st.markdown("###### [C] अवांतर खर्च व नफा")
                po_c1, po_c2 = st.columns(2)
                with po_c1:
                    scaffolding_cost = st.number_input("पाळत / घोडी खर्च (₹):", min_value=0.0, value=200.0, step=50.0, key="pl_sc")
                    contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=100.0, step=25.0, key="pl_cc")
                with po_c2:
                    water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=1.0, step=0.5, key="pl_wp")
                    profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0, step=1.0, key="pl_pp")

                user_note = st.text_input("प्लास्टर कामाची नोट (Note):", placeholder="उदा. External double coat plaster...", key="pl_note")

                if st.button("📊 GENERATE PLASTER REPORT", type="primary", key="pl_report_btn", use_container_width=True):
                    wet_vol = plaster_area * (thickness_mm / 1000.0)
                    dry_vol = wet_vol * 1.33
                    tot_mortar_parts = p_c_part + p_s_part
                    cement_vol = (p_c_part / tot_mortar_parts) * dry_vol
                    sand_m3 = (p_s_part / tot_mortar_parts) * dry_vol
                    sand_brass = sand_m3 / 2.83168
                    cement_bags = math.ceil(cement_vol * 28.8)

                    c_cost = cement_bags * cement_rate
                    s_cost = sand_m3 * sand_rate
                    wp_cost = (cement_bags * 1.0 * wp_rate) if use_wp else 0.0
                    mat_cost = c_cost + s_cost + wp_cost

                    lab_cost = (pl_mason_qty * pl_mason_rate) + (pl_mazdoor_qty * pl_mazdoor_rate)
                    extra_cost = scaffolding_cost + contingency_cost
                    base_total = mat_cost + lab_cost + extra_cost
                    w_amt = base_total * (water_pct / 100.0)
                    p_amt = base_total * (profit_pct / 100.0)
                    grand_total = base_total + w_amt + p_amt

                    st.success(f"🎉 एकूण प्लास्टर खर्च: ₹ {grand_total:,.2f}/- ({plaster_area} m² साठी)")

                    wp_row = f"| Waterproofing Compound | {cement_bags} | Kg | {wp_rate:.2f} | {wp_cost:.2f} |\n" if use_wp else ""

                    report_table = f"""
| तपशील (Item) | प्रमाण (Quantity) | एकक (Unit) | दर (Rate ₹) | एकूण रक्कम (Amount ₹) |
| :--- | :--- | :--- | :--- | :--- |
| **[A] साहित्याचा खर्च (Material)** | | | | |
| Cement (IS PPC) | {cement_bags} | Bags | {cement_rate:.2f} | {c_cost:.2f} |
| Sand (वाळू) | {sand_m3:.2f} ({sand_brass:.2f} Brass) | m³ | {sand_rate:.2f} | {s_cost:.2f} |
{wp_row}| **[B] मजुरी व लेबर (Labour)** | | | | |
| Mason (गवंडी) | {pl_mason_qty} | Days | {pl_mason_rate:.2f} | {pl_mason_qty*pl_mason_rate:.2f} |
| Mazdoor (मजदूर) | {pl_mazdoor_qty} | Days | {pl_mazdoor_rate:.2f} | {pl_mazdoor_qty*pl_mazdoor_rate:.2f} |
| **[C] अवांतर खर्च (Overheads)** | | | | |
| Scaffolding / पाळत | - | L.S. | - | {scaffolding_cost:.2f} |
| Contingencies | - | L.S. | - | {contingency_cost:.2f} |
| **एकूण पायाभूत खर्च (Subtotal A+B+C)** | | | | **₹ {base_total:.2f}** |
| Water Charges ({water_pct}%) | - | - | - | {w_amt:.2f} |
| Contractor Profit ({profit_pct}%) | - | - | - | {p_amt:.2f} |
| **फायनल ग्रँड टोटल (Grand Total)** | | | | **₹ {grand_total:,.2f}/-** |
"""
                    st.markdown(report_table)

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), f"Plaster {thickness_mm}mm - {user_note}", report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

                    msg_text = f"🏗️ *PATIL INFRATECH - PLASTER RATE ANALYSIS*\n👤 *User:* {current_user_name}\n📍 *Site:* {st.session_state.current_site_name}\n🎨 *Thick:* {thickness_mm}mm | *Area:* {plaster_area} m²\n• Cement: {cement_bags} Bags\n• Sand: {sand_m3:.2f} m³ ({sand_brass:.2f} Brass)\n💰 *GRAND TOTAL:* ₹{grand_total:,.2f}/-"
                    render_whatsapp_feature(urllib.parse.quote(msg_text), "ra_pl")

        # ======================================================================
        # १६.३ Bar Bending Schedule (IS 2502 & IS 1786)
        # ======================================================================
        elif est_sub_mod == "BBS":
            st.markdown("#### 🏗️ Bar Bending Schedule (BBS Calculator - IS 2502)")
            default_covers = {"Footing": 50, "Column": 40, "Beam": 25, "Slab": 20}

            def update_cover_from_component():
                selected_comp = st.session_state.get("bbs_rcc_component", "Footing")
                st.session_state["bbs_cover"] = default_covers.get(selected_comp, 25)

            if "bbs_cover" not in st.session_state:
                st.session_state["bbs_cover"] = 50

            rcc_comp = st.selectbox(
                "घटक निवडा:",
                ["Footing", "Column", "Beam", "Slab"],
                key="bbs_rcc_component",
                on_change=update_cover_from_component,
            )

            dim_col1, dim_col2, dim_col3 = st.columns(3)
            with dim_col1:
                length_m = st.number_input("लांबी L (m):", min_value=0.1, value=3.0, step=0.1, key="bbs_l")
            with dim_col2:
                width_m = st.number_input("रुंदी B (m):", min_value=0.1, value=0.3, step=0.05, key="bbs_b")
            with dim_col3:
                height_m = st.number_input("उंची H (m):", min_value=0.1, value=0.45, step=0.05, key="bbs_h")

            c_c1, c_c2 = st.columns(2)
            with c_c1:
                cover = st.number_input("Clear Cover (mm):", min_value=10, max_value=100, step=5, key="bbs_cover")
            with c_c2:
                num_members = st.number_input("घटक संख्या (Nos):", min_value=1, value=1, step=1, key="bbs_mem")

            dia_list = [8, 10, 12, 16, 20, 25, 32]

            if rcc_comp == "Footing":
                f1, f2 = st.columns(2)
                with f1:
                    f_main_dia = st.selectbox("Main Bar DIA (mm):", dia_list, index=2, key="f_m_dia")
                    f_main_spacing = st.number_input("Main Spacing (mm):", min_value=50, value=150, step=10, key="f_m_sp")
                with f2:
                    f_dist_dia = st.selectbox("Distribution DIA (mm):", dia_list, index=1, key="f_d_dia")
                    f_dist_spacing = st.number_input("Dist Spacing (mm):", min_value=50, value=150, step=10, key="f_d_sp")

            elif rcc_comp == "Column":
                c1, c2, c3 = st.columns(3)
                with c1:
                    col_main_dia = st.selectbox("Main DIA (mm):", dia_list, index=3, key="col_m_dia")
                    col_main_nos = st.number_input("Main Bars (Nos):", min_value=4, value=4, step=2, key="col_m_nos")
                with c2:
                    col_st_dia = st.selectbox("Ring DIA (mm):", dia_list, index=0, key="col_s_dia")
                    col_st_spacing = st.number_input("Ring Spacing (mm):", min_value=50, value=150, step=10, key="col_s_sp")
                with c3:
                    col_hook_angle = st.selectbox("Hook Angle:", ["135° (Hook = 10d)", "90° (Hook = 6d)"], key="col_h_ang")

            elif rcc_comp == "Beam":
                b1, b2, b3 = st.columns(3)
                with b1:
                    bm_top_dia = st.selectbox("Top DIA (mm):", dia_list, index=2, key="bm_t_dia")
                    bm_top_nos = st.number_input("Top Bars:", min_value=2, value=2, step=1, key="bm_t_nos")
                with b2:
                    bm_bot_dia = st.selectbox("Bot DIA (mm):", dia_list, index=3, key="bm_b_dia")
                    bm_bot_nos = st.number_input("Bot Bars:", min_value=2, value=2, step=1, key="bm_b_nos")
                with b3:
                    bm_st_dia = st.selectbox("Ring DIA (mm):", dia_list, index=0, key="bm_s_dia")
                    bm_st_spacing = st.number_input("Ring Spacing:", min_value=50, value=150, step=10, key="bm_s_sp")

            else:  # Slab
                s1, s2 = st.columns(2)
                with s1:
                    sl_main_dia = st.selectbox("Main DIA (mm):", dia_list, index=1, key="sl_m_dia")
                    sl_main_spacing = st.number_input("Main Spacing (mm):", min_value=50, value=150, step=10, key="sl_m_sp")
                with s2:
                    sl_dist_dia = st.selectbox("Dist DIA (mm):", dia_list, index=0, key="sl_d_dia")
                    sl_dist_spacing = st.number_input("Dist Spacing (mm):", min_value=50, value=150, step=10, key="sl_d_spacing")

            master_rates = get_market_rates()
            steel_rate_kg = st.number_input("आजचा स्टील दर (₹/Kg):", min_value=0.0, value=float(master_rates.get("steel", 60.0)), key="bbs_rate")

            if st.button("🧮 CALCULATE BBS REPORT", type="primary", key="bbs_calc_btn", use_container_width=True):
                length_mm = length_m * 1000.0
                width_mm = width_m * 1000.0
                height_mm = height_m * 1000.0
                l_net = length_mm - (2 * cover)
                b_net = width_mm - (2 * cover)
                h_net = height_mm - (2 * cover)

                calc_list = []

                if rcc_comp == "Footing":
                    m_cut_m = (l_net + 400.0 - (4 * f_main_dia)) / 1000.0
                    m_nos = (math.ceil(width_mm / f_main_spacing) + 1) * num_members
                    m_tot_len = m_cut_m * m_nos
                    m_tot_wt = m_tot_len * ((f_main_dia**2) / 162.0)
                    calc_list.append({"Desc": "Main Bars", "Nos": m_nos, "Dia": f_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "TotWt": m_tot_wt})

                    d_cut_m = (b_net + 400.0 - (4 * f_dist_dia)) / 1000.0
                    d_nos = (math.ceil(length_mm / f_dist_spacing) + 1) * num_members
                    d_tot_len = d_cut_m * d_nos
                    d_tot_wt = d_tot_len * ((f_dist_dia**2) / 162.0)
                    calc_list.append({"Desc": "Distribution Bars", "Nos": d_nos, "Dia": f_dist_dia, "Len": d_cut_m, "TotLen": d_tot_len, "TotWt": d_tot_wt})

                elif rcc_comp == "Column":
                    m_cut_m = (height_mm + 300.0) / 1000.0
                    m_nos = col_main_nos * num_members
                    m_tot_len = m_cut_m * m_nos
                    m_tot_wt = m_tot_len * ((col_main_dia**2) / 162.0)
                    calc_list.append({"Desc": "Main Vertical", "Nos": m_nos, "Dia": col_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "TotWt": m_tot_wt})

                    hook_len = 10 * col_st_dia if "135°" in col_hook_angle else 6 * col_st_dia
                    st_cut_m = ((2 * (b_net + h_net)) + (2 * hook_len) - (6 * col_st_dia)) / 1000.0
                    st_nos = (math.ceil(height_mm / col_st_spacing) + 1) * num_members
                    st_tot_len = st_cut_m * st_nos
                    st_tot_wt = st_tot_len * ((col_st_dia**2) / 162.0)
                    calc_list.append({"Desc": "Stirrups / Ties", "Nos": st_nos, "Dia": col_st_dia, "Len": st_cut_m, "TotLen": st_tot_len, "TotWt": st_tot_wt})

                elif rcc_comp == "Beam":
                    t_ld = max(300.0, 30 * bm_top_dia)
                    t_cut_m = (l_net + (2 * t_ld) - (4 * bm_top_dia)) / 1000.0
                    t_nos = bm_top_nos * num_members
                    t_tot_len = t_cut_m * t_nos
                    t_tot_wt = t_tot_len * ((bm_top_dia**2) / 162.0)
                    calc_list.append({"Desc": "Top Bars", "Nos": t_nos, "Dia": bm_top_dia, "Len": t_cut_m, "TotLen": t_tot_len, "TotWt": t_tot_wt})

                    b_ld = max(300.0, 30 * bm_bot_dia)
                    b_cut_m = (l_net + (2 * b_ld) - (4 * bm_bot_dia)) / 1000.0
                    b_nos = bm_bot_nos * num_members
                    b_tot_len = b_cut_m * b_nos
                    b_tot_wt = b_tot_len * ((bm_bot_dia**2) / 162.0)
                    calc_list.append({"Desc": "Bottom Bars", "Nos": b_nos, "Dia": bm_bot_dia, "Len": b_cut_m, "TotLen": b_tot_len, "TotWt": b_tot_wt})

                    st_cut_m = ((2 * (b_net + h_net)) + (20 * bm_st_dia) - (6 * bm_st_dia)) / 1000.0
                    st_nos = (math.ceil(length_mm / bm_st_spacing) + 1) * num_members
                    st_tot_len = st_cut_m * st_nos
                    st_tot_wt = st_tot_len * ((bm_st_dia**2) / 162.0)
                    calc_list.append({"Desc": "Stirrups", "Nos": st_nos, "Dia": bm_st_dia, "Len": st_cut_m, "TotLen": st_tot_len, "TotWt": st_tot_wt})

                else:  # Slab
                    m_cut_m = (l_net + (20 * sl_main_dia)) / 1000.0
                    m_nos = (math.ceil(width_mm / sl_main_spacing) + 1) * num_members
                    m_tot_len = m_cut_m * m_nos
                    m_tot_wt = m_tot_len * ((sl_main_dia**2) / 162.0)
                    calc_list.append({"Desc": "Main Bars", "Nos": m_nos, "Dia": sl_main_dia, "Len": m_cut_m, "TotLen": m_tot_len, "TotWt": m_tot_wt})

                    d_cut_m = (b_net + (20 * sl_dist_dia)) / 1000.0
                    d_nos = (math.ceil(length_mm / sl_dist_spacing) + 1) * num_members
                    d_tot_len = d_cut_m * d_nos
                    d_tot_wt = d_tot_len * ((sl_dist_dia**2) / 162.0)
                    calc_list.append({"Desc": "Distribution Bars", "Nos": d_nos, "Dia": sl_dist_dia, "Len": d_cut_m, "TotLen": d_tot_len, "TotWt": d_tot_wt})

                total_weight_kg = sum(item["TotWt"] for item in calc_list)
                total_cost = total_weight_kg * steel_rate_kg

                st.success(f"🎉 एकूण स्टील वजन: {total_weight_kg:.2f} Kg | खर्च: ₹ {total_cost:,.2f}/-")

                table_rows = ""
                for item in calc_list:
                    table_rows += f"| {item['Desc']} | {item['Nos']} | {item['Dia']} mm | {item['Len']:.3f} m | {item['TotLen']:.2f} m | {item['TotWt']:.2f} Kg |\n"

                report_table = f"""
| Description | Nos | Dia | Cutting Len | Total Len | Total Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
{table_rows}
| **TOTAL** | | | | | **{total_weight_kg:.2f} Kg (₹ {total_cost:,.2f})** |
"""
                st.markdown(report_table)

                if current_user_name:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                        (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), f"BBS {rcc_comp}", report_table, st.session_state.current_site_name),
                    )
                    conn.commit()
                    conn.close()

                msg_text = f"🏗️ *PATIL INFRATECH - BBS REPORT*\n👤 *User:* {current_user_name}\n📐 *Component:* {rcc_comp}\n⚖️ *Weight:* {total_weight_kg:.2f} Kg\n💰 *Cost:* ₹{total_cost:,.2f}/-"
                render_whatsapp_feature(urllib.parse.quote(msg_text), "bbs_main")

        # ======================================================================
        # १६.४ Quantity Surveying & Abstract Sheet Master (IS 1200)
        # ======================================================================
        elif est_sub_mod == "Quantity Surveying":
            st.markdown("#### 📈 Quantity Surveying & Abstract Sheet Master (IS 1200)")
            st.caption("💡 आयटमचे परिमाण, नग व वजावट (Deduction) भरून नेट प्रमाण व मटेरियल आवश्यकता मिळवा.")

            stages = [
                "Earthwork in Excavation", "P.C.C. Bedding", "Foundation / Footing RCC Work",
                "Plinth Beam & Masonry Work", "Superstructure Brickwork", "RCC Columns & Beams",
                "Slab Casting", "Flooring / Tiling Work", "Plaster Work",
            ]

            stage_results = []
            for idx, stg_name in enumerate(stages):
                is_area_unit = "Flooring" in stg_name or "Plaster" in stg_name
                is_brickwork = "Brickwork" in stg_name
                is_plaster = "Plaster" in stg_name

                with st.expander(f"🔹 {stg_name}", expanded=False):
                    c_desc, c_nos = st.columns([3, 1])
                    with c_desc:
                        desc_val = st.text_input(f"विवरण #{idx}", value=stg_name, key=f"qs_desc_{idx}")
                    with c_nos:
                        nos_val = st.number_input(f"नग (Nos) #{idx}", min_value=0, value=0, step=1, key=f"qs_nos_{idx}")

                    c_l, c_w, c_h = st.columns(3)
                    with c_l:
                        l_val = st.number_input(f"लांबी (L) #{idx}", min_value=0.0, value=0.0, step=0.1, key=f"qs_l_{idx}")
                    with c_w:
                        w_val = st.number_input(f"रुंदी (W) #{idx}", min_value=0.0, value=0.0, step=0.1, key=f"qs_w_{idx}")
                    with c_h:
                        h_val = 1.0 if is_area_unit else st.number_input(f"उंची (H) #{idx}", min_value=0.0, value=0.0, step=0.05, key=f"qs_h_{idx}")

                    bw_ded_vol = 0.0
                    if is_brickwork:
                        st.caption("🚪 वजावट (Doors/Windows Deduction in m³):")
                        d1, d2, d3 = st.columns(3)
                        with d1:
                            dl = st.number_input("Deduction L (m):", min_value=0.0, value=0.0, key=f"bw_dl_{idx}")
                        with d2:
                            dh = st.number_input("Deduction H (m):", min_value=0.0, value=0.0, key=f"bw_dh_{idx}")
                        with d3:
                            dn = st.number_input("Deduction Nos:", min_value=0, value=0, key=f"bw_dn_{idx}")
                        bw_ded_vol = dl * 0.23 * dh * dn

                    pl_ded_area = 0.0
                    if is_plaster:
                        st.caption("🚪 प्लास्टर वजावट (Deduction in m²):")
                        p1, p2, p3 = st.columns(3)
                        with p1:
                            pdl = st.number_input("Ded L (m):", min_value=0.0, value=0.0, key=f"pl_dl_{idx}")
                        with p2:
                            pdh = st.number_input("Ded H (m):", min_value=0.0, value=0.0, key=f"pl_dh_{idx}")
                        with p3:
                            pdn = st.number_input("Ded Nos:", min_value=0, value=0, key=f"pl_dn_{idx}")
                        pl_ded_area = pdl * pdh * pdn * 2.0

                    if nos_val > 0 and l_val > 0 and w_val > 0 and (is_area_unit or h_val > 0):
                        unit_label = "m²" if is_area_unit else "m³"
                        gross_qty = l_val * w_val * (1.0 if is_area_unit else h_val) * nos_val
                        net_total_qty = max(0.0, gross_qty - (bw_ded_vol if is_brickwork else (pl_ded_area if is_plaster else 0.0)))

                        st.info(f"Net Qty: **{net_total_qty:.3f} {unit_label}**")

                        stage_results.append({
                            "Stage": desc_val,
                            "Dimensions": f"{l_val} x {w_val} x {h_val if not is_area_unit else '-'}",
                            "Nos": nos_val,
                            "TotalQty": f"{net_total_qty:.3f} {unit_label}",
                        })

            if st.button("📈 GENERATE ABSTRACT REPORT", type="primary", key="qs_gen_btn", use_container_width=True):
                if not stage_results:
                    st.warning("⚠️ कृपया कमीत कमी एका स्टेजचे मोजमाप भरा!")
                else:
                    st.success("🎉 Abstract Sheet तयार झाली!")
                    table_rows = ""
                    for r in stage_results:
                        table_rows += f"| {r['Stage']} | {r['Nos']} | {r['Dimensions']} | {r['TotalQty']} |\n"

                    report_table = f"""
| Stage | Nos | Dimensions | Net Quantity |
| :--- | :--- | :--- | :--- |
{table_rows}
"""
                    st.markdown(report_table)

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), "Abstract Sheet", report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

                    msg_text = f"📊 *PATIL INFRATECH - QUANTITY SURVEY*\n👤 *User:* {current_user_name}\n📍 *Site:* {st.session_state.current_site_name}\nAbstract Report Generated Successfully."
                    render_whatsapp_feature(urllib.parse.quote(msg_text), "qs_main")
# ==========================================
# 📌 विभाग १७: SITE MANAGER मुख्य मॉड्यूल (Sub-modules)
# ==========================================
elif st.session_state.selected_module == "Site Manager":
    col_back, _ = st.columns([1.5, 3.5])
    with col_back:
        if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_site", use_container_width=True):
            st.session_state.selected_module = None
            st.session_state.selected_site_sub_module = None
            st.rerun()

    st.write("---")

    # --- सब-मॉड्यूल निवड मेनू (Responsive Grid for Mobile & Laptop) ---
    if st.session_state.selected_site_sub_module is None:
        st.markdown("<h4 style='margin-bottom:14px;'>👷 Construction Site Manager Dashboard</h4>", unsafe_allow_html=True)

        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown(
                """
                <div class="module-card">
                    <div style="font-size: 30px; margin-bottom: 4px;">👷</div>
                    <b style="color: #f8fafc; font-size: 14px;">Attendance & Wages</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">दैनिक हजेरी व मजुरी बिल</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Attendance", key="btn_site_att", use_container_width=True):
                st.session_state.selected_site_sub_module = "Attendance"
                trigger_push_state()
                st.rerun()

        with s_col2:
            st.markdown(
                """
                <div class="module-card">
                    <div style="font-size: 30px; margin-bottom: 4px;">📦</div>
                    <b style="color: #f8fafc; font-size: 14px;">Material Stock & Indent</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">शिल्लक माल व आजची ऑर्डर</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Material Stock", key="btn_site_inv", use_container_width=True):
                st.session_state.selected_site_sub_module = "Inventory"
                trigger_push_state()
                st.rerun()

        st.write(" ")
        s_col3, s_col4 = st.columns(2)
        with s_col3:
            st.markdown(
                """
                <div class="module-card">
                    <div style="font-size: 30px; margin-bottom: 4px;">📸</div>
                    <b style="color: #f8fafc; font-size: 14px;">Progress Report</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">दैनिक प्रगती व फोटो अपलोड</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Progress Report", key="btn_site_prog", use_container_width=True):
                st.session_state.selected_site_sub_module = "Progress"
                trigger_push_state()
                st.rerun()

        with s_col4:
            st.markdown(
                """
                <div class="module-card">
                    <div style="font-size: 30px; margin-bottom: 4px;">🏗️</div>
                    <b style="color: #f8fafc; font-size: 14px;">Pre-Concreting Checklist</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">स्लॅब भरण्यापूर्वी डिजिटल तपासणी</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Checklist", key="btn_site_chk", use_container_width=True):
                st.session_state.selected_site_sub_module = "Checklist"
                trigger_push_state()
                st.rerun()

        st.write(" ")
        s_col5, s_col6 = st.columns(2)
        with s_col5:
            st.markdown(
                """
                <div class="module-card">
                    <div style="font-size: 30px; margin-bottom: 4px;">📊</div>
                    <b style="color: #f8fafc; font-size: 14px;">Weekly Dashboard</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">मागील ७ दिवसांचे संपूर्ण लॉग्स</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Weekly Logs", key="btn_site_week", use_container_width=True):
                st.session_state.selected_site_sub_module = "Weekly"
                trigger_push_state()
                st.rerun()

        with s_col6:
            st.markdown(
                """
                <div class="module-card" style="border-color: rgba(245, 158, 11, 0.4);">
                    <div style="font-size: 30px; margin-bottom: 4px;">⏳</div>
                    <b style="color: #f59e0b; font-size: 14px;">Timeline & Delay Tracker</b>
                    <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">प्रोजेक्ट समाप्ती तारीख हिशोब</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(" ")
            if st.button("Open Timeline Tracker", key="btn_site_delay", use_container_width=True, type="primary"):
                st.session_state.selected_site_sub_module = "Timeline"
                trigger_push_state()
                st.rerun()

    else:
        col_b_menu, _ = st.columns([1.5, 3.5])
        with col_b_menu:
            if st.button("⬅️ Site Manager मेनूवर जा", key="btn_back_site_menu", use_container_width=True):
                st.session_state.selected_site_sub_module = None
                st.rerun()

        st.write("---")
        sub_mod = st.session_state.selected_site_sub_module

        # १७.१ Attendance & Wages Tracker (Responsive Layout)
        if sub_mod == "Attendance":
            st.markdown("#### 👷 डेली हजेरी आणि मजुरी कॅल्क्युलेटर")
            att_date = st.date_input("तारीख निवडा:", datetime.date.today(), key="site_att_date")

            st.markdown("##### 👥 कामगारांची संख्या व रोजंदारी भरा:")
            
            labor_types = [
                ("supervisor", "मुकादम (Supervisor)", 0, 800.0),
                ("mason", "गवंडी (Mason)", 4, 800.0),
                ("labor", "मजूर (Labor/Helper)", 6, 500.0),
                ("fitter", "फिटर/बार बेंडर (Fitter)", 2, 750.0),
                ("carpenter", "सुतार/सेंटरिंग (Carpenter)", 0, 800.0),
                ("plumber", "प्लंबर (Plumber)", 0, 700.0),
                ("electrician", "इलेक्ट्रिशियन (Electrician)", 0, 700.0),
                ("painter", "पेंटर (Painter)", 0, 600.0),
            ]

            w_data = {}
            total_labor_cost = 0.0

            for w_id, w_name, def_q, def_r in labor_types:
                with st.expander(f"🔹 {w_name}", expanded=(def_q > 0)):
                    c_q, c_r, c_t = st.columns([2, 2, 2])
                    with c_q:
                        q = st.number_input("संख्या (Nos):", min_value=0, value=def_q, step=1, key=f"q_{w_id}")
                    with c_r:
                        r = st.number_input("रोजंदारी दर (₹):", min_value=0.0, value=def_r, step=50.0, key=f"r_{w_id}")
                    with c_t:
                        t = q * r
                        st.markdown(f"<p style='margin-top:28px; font-weight:bold; color:#10b981;'>रक्कम: ₹ {t:,.2f}</p>", unsafe_allow_html=True)
                        total_labor_cost += t

                w_data[w_id] = {"qty": q, "rate": r}

            st.markdown(
                f"""
                <div style="background: #111827; padding: 14px 18px; border-radius: 10px; border-left: 4px solid #10b981; margin: 12px 0;">
                    <h4 style="margin:0; color:#10b981;">💰 आजची एकूण मजुरी: ₹ {total_labor_cost:,.2f}/-</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("💾 हजेरी डेटाबेसमध्ये सेव्ह करा", type="primary", key="save_att_btn", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_attendance (
                        user_key, date,
                        supervisor, supervisor_rate,
                        masons, mason_rate,
                        labors, labor_rate,
                        fitters, fitter_rate,
                        carpenter, carpenter_rate,
                        plumber, plumber_rate,
                        electrician, electrician_rate,
                        painter, painter_rate,
                        total_cost, site_name
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_user_name,
                        str(att_date),
                        w_data["supervisor"]["qty"], w_data["supervisor"]["rate"],
                        w_data["mason"]["qty"], w_data["mason"]["rate"],
                        w_data["labor"]["qty"], w_data["labor"]["rate"],
                        w_data["fitter"]["qty"], w_data["fitter"]["rate"],
                        w_data["carpenter"]["qty"], w_data["carpenter"]["rate"],
                        w_data["plumber"]["qty"], w_data["plumber"]["rate"],
                        w_data["electrician"]["qty"], w_data["electrician"]["rate"],
                        w_data["painter"]["qty"], w_data["painter"]["rate"],
                        total_labor_cost,
                        st.session_state.current_site_name,
                    ),
                )
                conn.commit()
                conn.close()
                st.success("✅ आजची हजेरी आणि मजुरी बिल सेव्ह झाले!")

  # ==============================================================================
        # १७.२ Fully Automated Material Taking, Stock Auto-Deduct & Stage Lock System
        # ==============================================================================
        elif sub_mod == "Inventory":
            st.markdown("#### 📦 Smart Material ERP: Automated Taking, Stock & Stage Lock")
            st.caption(f"📍 Project: **[{st.session_state.active_site_code}] {st.session_state.current_site_name}** | Automated Workflow.")

            # --- १. Live Stock Balance Calculate Karne ---
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT material_name, transaction_type, quantity 
                FROM site_inventory 
                WHERE site_name = ?
                """,
                (st.session_state.current_site_name,),
            )
            inv_rows = cursor.fetchall()

            current_stock = {
                "Cement": 0.0,
                "Sand": 0.0,
                "Aggregate": 0.0,
                "Steel": 0.0,
                "Bricks": 0.0
            }

            for row in inv_rows:
                mat = str(row["material_name"]).strip()
                ttype = str(row["transaction_type"])
                qty = float(row["quantity"])
                matched_key = next((k for k in current_stock if k.lower() in mat.lower()), None)
                if matched_key:
                    if "IN" in ttype:
                        current_stock[matched_key] += qty
                    else:
                        current_stock[matched_key] -= qty

            # Database madhun master volumes ghene
            cursor.execute("SELECT * FROM site_master_volumes WHERE site_name = ?", (st.session_state.current_site_name,))
            mv_row = cursor.fetchone()
            conn.close()

            if not mv_row:
                vol_pcc, vol_footing, vol_plinth = 2.0, 5.0, 3.0
                vol_col, vol_brick, vol_slab = 2.5, 15.0, 10.0
            else:
                vol_pcc = float(mv_row["pcc_vol"])
                vol_footing = float(mv_row["footing_vol"])
                vol_plinth = float(mv_row["plinth_vol"])
                vol_col = float(mv_row["column_vol"])
                vol_brick = float(mv_row["brickwork_vol"])
                vol_slab = float(mv_row["slab_vol"])

            # --- २. Screen var Slim Live Stock Indicators ---
            st.markdown("##### 📊 Live Stock on Site (Shillak Mal):")
            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            sc1.metric("Cement", f"{current_stock['Cement']:.1f} Bags")
            sc2.metric("Sand", f"{current_stock['Sand']:.2f} Brass")
            sc3.metric("Aggregate", f"{current_stock['Aggregate']:.2f} Brass")
            sc4.metric("Steel", f"{current_stock['Steel']:.1f} Kg")
            sc5.metric("Bricks", f"{current_stock['Bricks']:.0f} Nos")

            st.write("---")

            # --- ३. One-Time Master Project Volumes Box (Kadhihi edit karnyachi soy) ---
            with st.expander("⚙️ Setup / Update Master Project Volumes (PCC pasun Slab paryant)", expanded=False):
                st.caption("Ithe ekdach purna building che volumes bharun save kara. System automatic sagle material plan karel.")
                mv_c1, mv_c2, mv_c3 = st.columns(3)
                with mv_c1:
                    new_vpcc = st.number_input("1. PCC Bedding (m³):", min_value=0.1, value=vol_pcc, step=0.5, key="mv_pcc")
                    new_vfooting = st.number_input("2. Footing Casting (m³):", min_value=0.1, value=vol_footing, step=0.5, key="mv_footing")
                with mv_c2:
                    new_vplinth = st.number_input("3. Plinth Beams (m³):", min_value=0.1, value=vol_plinth, step=0.5, key="mv_plinth")
                    new_vcol = st.number_input("4. Columns Casting (m³):", min_value=0.1, value=vol_col, step=0.5, key="mv_col")
                with mv_c3:
                    new_vbrick = st.number_input("5. Brickwork 9-inch (m³):", min_value=0.1, value=vol_brick, step=1.0, key="mv_brick")
                    new_vslab = st.number_input("6. Roof Slab & Beams (m³):", min_value=0.1, value=vol_slab, step=1.0, key="mv_slab")

                if st.button("💾 Save Project Volumes", type="primary", use_container_width=True):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    now_ts = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO site_master_volumes 
                        (site_name, pcc_vol, footing_vol, plinth_vol, column_vol, brickwork_vol, slab_vol, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (st.session_state.current_site_name, new_vpcc, new_vfooting, new_vplinth, new_vcol, new_vbrick, new_vslab, now_ts)
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ Master Project Volumes यशस्वीरीत्या सेव्ह झाले!")
                    st.rerun()

            # --- ४. Material IN (+) Supervisor Stock Form ---
            with st.expander("📥 Add Incoming Material to Stock (Navin Mal Aalyas Entry)", expanded=False):
                in_c1, in_c2, in_c3 = st.columns([2, 1.5, 1.5])
                with in_c1:
                    sup_mat = st.selectbox("Material:", ["Cement (Bags)", "Sand (Brass)", "Aggregate (Brass)", "Steel (Kg)", "Bricks (Nos)"], key="sup_m_sel")
                with in_c2:
                    sup_qty = st.number_input("Quantity:", min_value=0.1, value=50.0, step=1.0, key="sup_q_val")
                with in_c3:
                    sup_ch = st.text_input("Challan / Bill No:", placeholder="e.g. CH-201", key="sup_ch_no")

                if st.button("➕ Stock Madhe Jama Kara", type="primary", use_container_width=True):
                    c_m = sup_mat.split(" ")[0]
                    c_u = sup_mat.split("(")[-1].replace(")", "")
                    now_ts = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO site_inventory (user_key, date, material_name, transaction_type, quantity, unit, site_name)
                        VALUES (?, ?, ?, 'Material IN (+)', ?, ?, ?)
                        """,
                        (current_user_name, now_ts, c_m, sup_qty, c_u, st.session_state.current_site_name)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"✅ {sup_qty} {c_u} {c_m} successfully stock madhe add zale!")
                    st.rerun()

            st.write("---")

            # --- ५. Current Active Stage Execution Engine (IS Code Formulas) ---
            st.markdown("##### 🚧 Current Stage Execution & Auto-Deduct:")

            stage_names = [
                "Stage 1: PCC Bedding Work (1:4:8)",
                "Stage 2: Footing RCC Casting (M20)",
                "Stage 3: Plinth Beam Casting (M20)",
                "Stage 4: Columns Casting (M20)",
                "Stage 5: Brickwork 9-inch (1:6)",
                "Stage 6: Slab & Beam Casting (M20)"
            ]

            active_stage = st.selectbox("Execute Karaycha Tappa (Select Stage):", stage_names, key="active_stg_sel")

            # Assigned volumes selection
            if "PCC" in active_stage:
                target_vol = vol_pcc
                vol_unit = "m³"
                dry_v = target_vol * 1.54 * 1.03  # 3% wastage
                stage_req = {
                    "Cement": (math.ceil((1.0 / 13.0) * dry_v * 28.8), "Bags"),
                    "Sand": (round((((4.0 / 13.0) * dry_v) / 2.8317), 2), "Brass"),
                    "Aggregate": (round((((8.0 / 13.0) * dry_v) / 2.8317), 2), "Brass")
                }
            elif "Footing" in active_stage:
                target_vol = vol_footing
                vol_unit = "m³"
                dry_v = target_vol * 1.54 * 1.03
                stage_req = {
                    "Cement": (math.ceil((1.0 / 5.5) * dry_v * 28.8), "Bags"),
                    "Sand": (round((((1.5 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Aggregate": (round((((3.0 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Steel": (round(target_vol * 85.0 * 1.03, 1), "Kg")
                }
            elif "Plinth" in active_stage:
                target_vol = vol_plinth
                vol_unit = "m³"
                dry_v = target_vol * 1.54 * 1.03
                stage_req = {
                    "Cement": (math.ceil((1.0 / 5.5) * dry_v * 28.8), "Bags"),
                    "Sand": (round((((1.5 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Aggregate": (round((((3.0 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Steel": (round(target_vol * 125.0 * 1.03, 1), "Kg")
                }
            elif "Columns" in active_stage:
                target_vol = vol_col
                vol_unit = "m³"
                dry_v = target_vol * 1.54 * 1.03
                stage_req = {
                    "Cement": (math.ceil((1.0 / 5.5) * dry_v * 28.8), "Bags"),
                    "Sand": (round((((1.5 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Aggregate": (round((((3.0 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Steel": (round(target_vol * 160.0 * 1.03, 1), "Kg")
                }
            elif "Brickwork" in active_stage:
                target_vol = vol_brick
                vol_unit = "m³"
                dry_m = target_vol * 0.30 * 1.03
                stage_req = {
                    "Bricks": (math.ceil(target_vol * 500.0 * 1.03), "Nos"),
                    "Cement": (math.ceil((1.0 / 7.0) * dry_m * 28.8), "Bags"),
                    "Sand": (round((((6.0 / 7.0) * dry_m) / 2.8317), 2), "Brass")
                }
            else:  # Slab
                target_vol = vol_slab
                vol_unit = "m³"
                dry_v = target_vol * 1.54 * 1.03
                stage_req = {
                    "Cement": (math.ceil((1.0 / 5.5) * dry_v * 28.8), "Bags"),
                    "Sand": (round((((1.5 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Aggregate": (round((((3.0 / 5.5) * dry_v) / 2.8317), 2), "Brass"),
                    "Steel": (round(target_vol * 95.0 * 1.03, 1), "Kg")
                }

            st.info(f"📋 **Stage Info:** `{active_stage}` | **Setup Volume:** `{target_vol} {vol_unit}`")

            # --- ६. Clean Markdown Table (No HTML rendering error) ---
            req_rows_md = ""
            shortage_list = []
            has_stage_shortage = False
            wa_indent_lines = []

            for m_key, (req_val, u_lbl) in stage_req.items():
                cur_val = current_stock.get(m_key, 0.0)
                diff = req_val - cur_val
                needed = math.ceil(diff) if u_lbl in ["Bags", "Nos"] else round(max(0.0, diff), 2)

                if needed > 0:
                    has_stage_shortage = True
                    shortage_list.append(f"{m_key}: {needed} {u_lbl}")
                    st_badge = f"🔴 Shortage ({needed} {u_lbl})"
                    wa_indent_lines.append(f"• *{m_key}:* {needed} {u_lbl}")
                else:
                    st_badge = f"🟢 Available (+{abs(round(cur_val - req_val, 2))} {u_lbl})"

                req_rows_md += f"| **{m_key}** | {req_val} {u_lbl} | {cur_val:.2f} {u_lbl} | **{needed} {u_lbl}** | {st_badge} |\n"

            st.markdown(
                f"""
| Material Name | Required (Lagnare) | Available Stock | Need to Order (Kami Mal) | Status |
| :--- | :--- | :--- | :--- | :--- |
{req_rows_md}
                """
            )

            # --- ७. Stage Lock vs Execution Button ---
            st.write(" ")
            if has_stage_shortage:
                st.error(
                    f"""
                    🛑 **STAGE LOCKED: अपुरा साहित्य साठा!**  
                    `{active_stage}` सुरू करण्यासाठी आवश्यक माल साईटवर शिल्लक नाही.  
                    जोपर्यंत खालील माल **'Material IN (+)'** द्वारे स्टॉकमध्ये भरला जात नाही, तोपर्यंत काम पुढे सुरू करता येणार नाही!  
                    **Missing:** `{', '.join(shortage_list)}`
                    """
                )

                # Instant WhatsApp Material Order
                wa_msg = (
                    f"🚨 *URGENT MATERIAL INDENT - PATIL INFRATECH*\n"
                    f"📍 *Site:* {st.session_state.current_site_name} [{st.session_state.active_site_code}]\n"
                    f"👷 *Engineer:* {current_user_name}\n"
                    f"🚧 *Blocked Work:* {active_stage} ({target_vol} {vol_unit})\n"
                    f"--------------------------------\n"
                    f"🚚 *Lagnara Navin Mal:*\n"
                )
                wa_msg += "\n".join(wa_indent_lines)
                wa_msg += "\n--------------------------------\n_Site kam band ahe, krupaya tatkal dispatch kara._"
                render_whatsapp_feature(urllib.parse.quote(wa_msg), "stage_shortage_wa")

            else:
                st.success(f"✅ **STAGE READY:** '{active_stage}' साठी सर्व माल स्टॉकमध्ये उपलब्ध आहे!")

                if st.button(f"🚀 Execute Work & Deduct Materials ({active_stage})", type="primary", use_container_width=True):
                    now_ts = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    # Material Stock Madhun OUT (-) Karne
                    for m_key, (req_val, u_lbl) in stage_req.items():
                        cursor.execute(
                            """
                            INSERT INTO site_inventory (user_key, date, material_name, transaction_type, quantity, unit, site_name)
                            VALUES (?, ?, ?, 'Material OUT (-)', ?, ?, ?)
                            """,
                            (current_user_name, now_ts, m_key, req_val, u_lbl, st.session_state.current_site_name)
                        )

                    # Progress report madhe stage completion entry
                    cursor.execute(
                        """
                        INSERT INTO site_progress (user_key, date, stage_name, progress_percent, remark, site_name)
                        VALUES (?, ?, ?, 100, ?, ?)
                        """,
                        (current_user_name, now_ts[:10], active_stage, f"{target_vol} {vol_unit} work completed. Stock deducted.", st.session_state.current_site_name)
                    )

                    conn.commit()
                    conn.close()

                    st.balloons()
                    st.success(f"🎉 '{active_stage}' चे साहित्य स्टॉकमधून वजा झाले! उरलेला माल पुढील कामासाठी सुरक्षित शिल्लक आहे.")
                    time.sleep(1.2)
                    st.rerun()

            # --- ८. Compact Recent Logs History ---
            st.write("---")
            with st.expander("📜 Recent Stock Transactions Log (Audit)", expanded=False):
                conn = get_db_connection()
                recent_logs = conn.execute(
                    "SELECT date, material_name, transaction_type, quantity, unit FROM site_inventory WHERE site_name = ? ORDER BY id DESC LIMIT 8",
                    (st.session_state.current_site_name,)
                ).fetchall()
                conn.close()

                if recent_logs:
                    log_md = ""
                    for r in recent_logs:
                        col_icon = "🟢" if "IN" in r["transaction_type"] else "🔴"
                        log_md += f"| {r['date']} | **{r['material_name']}** | {col_icon} {r['transaction_type']} | {r['quantity']} {r['unit']} |\n"

                    st.markdown(
                        f"""
| Date & Time | Material | Type | Quantity |
| :--- | :--- | :--- | :--- |
{log_md}
                        """
                    )
                else:
                    st.info("ℹ️ या साईटवर अजून कोणत्याही साठ्याची नोंद झालेली नाही.")
        # १७.३ Daily Progress Report & Photos
        elif sub_mod == "Progress":
            st.markdown("#### 📸 दैनिक प्रोग्रेस रिपोर्ट व फोटो")

            work_stage = st.text_input("कामाचा टप्पा:", value="Plinth Level Completed", key="prog_stage_input")
            work_percent = st.slider("टक्केवारी (%):", 0, 100, 40, key="prog_percent_slider")
            site_photo = st.file_uploader("फोटो अपलोड करा:", type=["png", "jpg", "jpeg"], key="prog_photo_upload")
            site_remark = st.text_area("रिमार्क / शेरा:", placeholder="उदा. साईटवर काम वेळेत पूर्ण झाले...", key="prog_remark_input")

            if site_photo:
                st.image(site_photo, caption="Uploaded Site Photo", use_column_width=True)

            if st.button("📊 प्रोग्रेस रिपोर्ट सेव्ह करा", type="primary", key="save_prog_btn", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_progress (user_key, date, stage_name, progress_percent, remark, site_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (current_user_name, str(datetime.date.today()), work_stage, work_percent, site_remark, st.session_state.current_site_name),
                )
                conn.commit()
                conn.close()

                report_summary = (
                    f"🏗️ *PATIL INFRATECH - PROGRESS REPORT*\n"
                    f"📍 *Site:* {st.session_state.current_site_name}\n📅 *Date:* {datetime.date.today()}\n"
                    f"🚧 *Stage:* {work_stage} ({work_percent}%)\n📝 *Remark:* {site_remark}\n"
                )
                st.success("🎉 Daily Progress Report सेव्ह झाला!")
                render_whatsapp_feature(urllib.parse.quote(report_summary), "site_prog_wa")

        # १७.४ Pre-Concreting Digital Checklist
        elif sub_mod == "Checklist":
            st.markdown("#### 🏗️ Pre-Concreting Digital Checklist")
            st.caption("💡 काँक्रीटिंग किंवा स्लॅब भरण्यापूर्वी सर्व बाबी तपासून टिक-मार्क करा.")

            default_chk_items = [
                "Cover Blocks (कव्हर ब्लॉक्स) लावलेले आहेत का?",
                "Shuttering (शटरिंग) चा लेव्हल व सपोर्ट ओके आहे का?",
                "Electrical Conduit Pipes व जंक्शन बॉक्सेस टाकले आहेत का?",
                "Curing (क्युरिंग) साठी पाण्याची सोय आहे का?",
                "सरयांचे अंतर (Reinforcement Spacing) व लॅपिंग ओके आहे का?",
                "शटरिंग ऑइल (Shuttering Oil) लावून कचरा साफ केला आहे का?",
                "काँक्रीट व्हायब्रेटर चालू स्थितीत तयार आहे का?",
            ]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, item_text, is_checked FROM pre_concreting_checklist WHERE user_key = ?", (current_user_name,))
            db_items = cursor.fetchall()

            if not db_items:
                now_time_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                for text in default_chk_items:
                    cursor.execute(
                        "INSERT INTO pre_concreting_checklist (user_key, item_text, is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
                        (current_user_name, text, now_time_str, st.session_state.current_site_name),
                    )
                conn.commit()
                cursor.execute("SELECT id, item_text, is_checked FROM pre_concreting_checklist WHERE user_key = ?", (current_user_name,))
                db_items = cursor.fetchall()
            conn.close()

            total_items = len(db_items)
            checked_items = sum(1 for item in db_items if item["is_checked"] == 1)
            progress_percentage = int((checked_items / total_items) * 100) if total_items > 0 else 0

            st.progress(progress_percentage)
            st.markdown(f"**पूर्णता: {progress_percentage}% ({checked_items}/{total_items} चेक केले)**")

            if progress_percentage == 100 and total_items > 0:
                st.success("✅ काँक्रीटिंग सुरू करण्यास पूर्ण परवानगी आहे! (All Checks Passed)")
            else:
                st.warning("🛑 काँक्रीटिंग सुरू करू नका (अजून काही पॉईंट्स बाकी आहेत)")

            with st.expander("➕ नवीन चेकलिस्ट पॉईंट जोडा"):
                new_chk_text = st.text_input("पॉईंट नाव:", placeholder="उदा. जनरेटर बॅकअप तयार आहे का?...", key="new_chk_input")
                if st.button("जोडा (+)", key="btn_add_chk_item", use_container_width=True):
                    if new_chk_text.strip():
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO pre_concreting_checklist (user_key, item_text, is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
                            (current_user_name, new_chk_text.strip(), get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()
                        st.rerun()

            st.write("---")
            for item in db_items:
                item_id, item_text, is_chk = item["id"], item["item_text"], bool(item["is_checked"])
                col_chk, col_del = st.columns([4.5, 0.5])
                with col_chk:
                    new_state = st.checkbox(item_text, value=is_chk, key=f"chk_box_{item_id}")
                    if new_state != is_chk:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE pre_concreting_checklist SET is_checked = ? WHERE id = ?", (1 if new_state else 0, item_id))
                        conn.commit()
                        conn.close()
                        st.rerun()
                with col_del:
                    if st.button("❌", key=f"btn_del_chk_{item_id}"):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM pre_concreting_checklist WHERE id = ?", (item_id,))
                        conn.commit()
                        conn.close()
                        st.rerun()

            if st.button("🔄 चेकलिस्ट रिसेट करा", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE pre_concreting_checklist SET is_checked = 0 WHERE user_key = ?", (current_user_name,))
                conn.commit()
                conn.close()
                st.success("✅ चेकलिस्ट रिसेट झाली!")
                st.rerun()

        # १७.५ Weekly Site Dashboard & Logs
        elif sub_mod == "Weekly":
            st.markdown("#### 📊 मागील ७ दिवसांचा साइट रिपोर्ट")
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            str_today, str_week_ago = str(today), str(week_ago)

            conn = get_db_connection()
            att_df = pd.read_sql_query(f"SELECT rowid as id, date as Date, total_cost as Daily_Wage FROM site_attendance WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC", conn)
            inv_df = pd.read_sql_query(f"SELECT rowid as id, date as Date, material_name as Material, transaction_type as Status, quantity as Qty FROM site_inventory WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC", conn)
            prog_df = pd.read_sql_query(f"SELECT rowid as id, date as Date, stage_name as Work_Stage, progress_percent as Completed_Percent FROM site_progress WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC", conn)
            conn.close()

            with st.expander("👷 मजुरी खर्च (Wages)", expanded=True):
                if not att_df.empty:
                    st.markdown(f"**💰 एकूण मजुरी खर्च:** <span style='color:#10b981; font-weight:bold;'>₹ {att_df['Daily_Wage'].sum():,.2f}</span>", unsafe_allow_html=True)
                    st.dataframe(att_df.drop(columns=["id"]), use_container_width=True, hide_index=True)
                    
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        att_del_opt = st.selectbox("डिलीट करण्यासाठी रेकॉर्ड निवडा:", att_df.to_dict("records"), format_func=lambda x: f"तारीख: {x['Date']} | रक्कम: ₹ {x['Daily_Wage']}", key="sel_del_att")
                    with c2:
                        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete", key="btn_del_att", use_container_width=True):
                            conn = get_db_connection()
                            conn.execute("DELETE FROM site_attendance WHERE rowid=?", (att_del_opt["id"],))
                            conn.commit()
                            conn.close()
                            st.success("✅ रेकॉर्ड डिलीट झाले!")
                            st.rerun()
                else:
                    st.info("ℹ️ मागील ७ दिवसात कोणतीही हजेरी नोंदवली नाही.")

            with st.expander("📦 मटेरियल ट्रॅकर (IN/OUT)"):
                if not inv_df.empty:
                    st.dataframe(inv_df.drop(columns=["id"]), use_container_width=True, hide_index=True)
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        inv_del_opt = st.selectbox("डिलीट करण्यासाठी रेकॉर्ड निवडा:", inv_df.to_dict("records"), format_func=lambda x: f"{x['Date']} | {x['Material']} | {x['Status']} ({x['Qty']})", key="sel_del_inv")
                    with c2:
                        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete", key="btn_del_inv", use_container_width=True):
                            conn = get_db_connection()
                            conn.execute("DELETE FROM site_inventory WHERE rowid=?", (inv_del_opt["id"],))
                            conn.commit()
                            conn.close()
                            st.success("✅ रेकॉर्ड डिलीट झाले!")
                            st.rerun()
                else:
                    st.info("ℹ️ मागील ७ दिवसात कोणतेही मटेरियल नोंदवले नाही.")

            with st.expander("📸 कामाची प्रगती (Progress)"):
                if not prog_df.empty:
                    for _, row in prog_df.iterrows():
                        st.markdown(f"**📅 {row['Date']}** | **{row['Work_Stage']}** (`{row['Completed_Percent']}%`)")
                        st.progress(int(row["Completed_Percent"]))
                else:
                    st.info("ℹ️ प्रोग्रेस रिपोर्ट उपलब्ध नाही.")

        # १७.६ Project Timeline & Delay Analysis
        elif sub_mod == "Timeline":
            st.markdown("#### ⏳ प्रोजेक्ट टाईमलाईन व डिले ट्रॅकर")
            load_default_tasks_if_empty(current_user_name, st.session_state.current_site_name)

            col_p1, _ = st.columns([2, 2])
            with col_p1:
                proj_start_date = st.date_input("प्रोजेक्ट सुरू झालेली तारीख:", datetime.date.today(), key="proj_start_dt")

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, stage_order, task_name, planned_duration, delay_days, status, is_critical 
                FROM project_tasks 
                WHERE user_key = ? AND site_name = ?
                ORDER BY stage_order ASC
                """,
                (current_user_name, st.session_state.current_site_name),
            )
            tasks = [dict(r) for r in cursor.fetchall()]
            conn.close()

            total_planned_days = sum(t["planned_duration"] for t in tasks) if tasks else 0
            total_critical_delay = sum(t["delay_days"] for t in tasks if t["is_critical"] == 1) if tasks else 0
            total_projected_days = total_planned_days + total_critical_delay

            original_finish_date = proj_start_date + datetime.timedelta(days=total_planned_days)
            new_projected_finish_date = proj_start_date + datetime.timedelta(days=total_projected_days)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("नियोजित दिवस", f"{total_planned_days} दिवस", f"End: {original_finish_date.strftime('%d-%m')}")
            m2.metric("उशीर (Delay)", f"+{total_critical_delay} दिवस", delta_color="inverse")
            m3.metric("एकूण दिवस", f"{total_projected_days} दिवस")
            m4.metric("अंतिम ताबा तारीख", new_projected_finish_date.strftime('%d %b %Y'))

            st.write("---")
            st.markdown("##### 📋 कामाचे टप्पे व्यवस्थापन:")

            updated_tasks = []
            for t in tasks:
                t_id = t["id"]
                with st.expander(f"#{t['stage_order']} {t['task_name']} ({t['status']})", expanded=False):
                    tc1, tc2, tc3, tc4 = st.columns([2, 2, 2, 1])
                    with tc1:
                        new_plan = st.number_input("नियोजित दिवस:", min_value=1, value=t["planned_duration"], step=1, key=f"plan_dur_{t_id}")
                    with tc2:
                        new_delay = st.number_input("उशीर (दिवस):", min_value=0, value=t["delay_days"], step=1, key=f"delay_dur_{t_id}")
                    with tc3:
                        new_status = st.selectbox("स्थिती:", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(t["status"]), key=f"status_{t_id}")
                    with tc4:
                        is_crit = st.checkbox("Critical?", value=bool(t["is_critical"]), key=f"crit_{t_id}", help="या कामामुळे पूर्ण प्रोजेक्ट पुढे जाईल का?")

                    updated_tasks.append((new_plan, new_delay, new_status, 1 if is_crit else 0, t_id))

            if st.button("💾 बदल सेव्ह करा आणि तारीख अपडेट करा", type="primary", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                for p, d, s, c, tid in updated_tasks:
                    cursor.execute(
                        "UPDATE project_tasks SET planned_duration = ?, delay_days = ?, status = ?, is_critical = ? WHERE id = ?",
                        (p, d, s, c, tid),
                    )
                conn.commit()
                conn.close()
                st.success("✅ प्रोजेक्ट टाईमलाईन अपडेट झाली!")
                st.rerun()

            wa_timeline_text = (
                f"🏗️ *PATIL INFRATECH - TIMELINE REPORT*\n"
                f"📍 *Site:* {st.session_state.current_site_name}\n"
                f"📅 *Start Date:* {proj_start_date.strftime('%d-%m-%Y')}\n"
                f"⏱️ *Duration:* {total_planned_days} Days (+{total_critical_delay} Delay)\n"
                f"🎯 *Handover Date:* {new_projected_finish_date.strftime('%d-%m-%Y')}\n"
            )
            render_whatsapp_feature(urllib.parse.quote(wa_timeline_text), "site_timeline_wa")
# ==========================================
# 📌 विभाग १८: NEEVPAY / SITESETU मुख्य मॉड्यूल (Escrow & Two-Way Approval)
# ==========================================
elif st.session_state.selected_module == "NeevPay":
    col_back, _ = st.columns([1.5, 3.5])
    with col_back:
        if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_neevpay", use_container_width=True):
            st.session_state.selected_module = None
            st.rerun()

    st.write("---")
    st.markdown(
        """
        <div style="background: #111827; border: 1px solid #1f2937; border-left: 5px solid #10b981; padding: 14px 18px; border-radius: 10px; margin-bottom: 16px;">
            <h3 style="margin: 0; color: #10b981; font-size: 18px; font-weight: 800;">🤝 NEEVPAY / SITESETU - SMART ESCROW</h3>
            <p style="margin: 3px 0 0 0; color: #94a3b8; font-size: 12px;">
                ठरलेले बिल बदलण्यासाठी क्लायंट ईमेल OTP अनिवार्य • पेमेंट नोंदीसाठी दोघांची संमती • अधिकृत Master Invoice PDF.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT client_email FROM site_client_profiles WHERE user_key = ? AND site_name = ?",
        (current_user_name, st.session_state.current_site_name),
    )
    client_row = cursor.fetchone()
    client_email = client_row["client_email"] if client_row else ""

    cursor.execute(
        """
        SELECT * FROM site_milestone_payments 
        WHERE user_key = ? AND site_name = ? 
        ORDER BY id ASC
        """,
        (current_user_name, st.session_state.current_site_name),
    )
    milestones = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # १. क्लायंट ईमेल नोंदणी
    if not client_email:
        st.warning("⚠️ NeevPay सुरक्षेसाठी घरमालकाचा (Client) ईमेल आयडी नोंदवा:")
        c_mail_in = st.text_input("घरमालकाचा ईमेल:", placeholder="client@gmail.com", key="reg_client_mail")
        if st.button("💾 ईमेल सेव्ह करा", key="btn_save_init_email", type="primary", use_container_width=True):
            if c_mail_in.strip() and "@" in c_mail_in:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO site_client_profiles (user_key, site_name, client_email) VALUES (?, ?, ?)",
                    (current_user_name, st.session_state.current_site_name, c_mail_in.strip().lower()),
                )
                conn.commit()
                conn.close()
                st.success("✅ घरमालकाचा ईमेल सेव्ह झाला!")
                st.rerun()
            else:
                st.error("❌ अचूक ईमेल पत्ता टाका!")
    else:
        c_info_col1, c_info_col2 = st.columns([3.5, 1.5])
        with c_info_col1:
            st.info(f"📧 **नोंदणीकृत घरमालक ईमेल:** `{client_email}`")
        with c_info_col2:
            with st.popover("✏️ ईमेल बदला"):
                new_mail_edit = st.text_input("नवीन ईमेल:", value=client_email, key="edit_c_mail")
                if st.button("अपडेट करा", key="btn_update_c_mail", type="primary", use_container_width=True):
                    if new_mail_edit.strip() and "@" in new_mail_edit:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE site_client_profiles SET client_email = ? WHERE user_key = ? AND site_name = ?",
                            (new_mail_edit.strip().lower(), current_user_name, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()
                        st.success("✅ ईमेल अपडेट झाला!")
                        st.rerun()

    st.write("---")

    # बजेट समरी मेट्रिक्स
    total_budget = sum(m["planned_amount"] for m in milestones)
    total_received = sum(m["amount_deposited"] for m in milestones)
    total_pending = max(0.0, total_budget - total_received)
    locked_stages = sum(1 for m in milestones if m.get("is_locked") == 1)
    overall_site_pct = (total_received / total_budget * 100) if total_budget > 0 else 0.0

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("एकूण बजेट", f"₹ {total_budget:,.2f}")
    e2.metric("जमा रक्कम", f"₹ {total_received:,.2f}")
    e3.metric("शिल्लक बाकी", f"₹ {total_pending:,.2f}")
    e4.metric("प्रगती", f"{locked_stages}/{len(milestones)} ({overall_site_pct:.1f}%)")

    st.write("---")

    # २. कामाचा नवीन टप्पा तयार करणे
    with st.expander("➕ कामाचे नवीन बिल / टप्पा निश्चित करा", expanded=(len(milestones) == 0)):
        work_presets = [
            "पाया खोदाई व प्लिंथ काम (Excavation & Plinth Level)",
            "आरसीसी कॉलम्स कास्टिंग (RCC Columns Casting)",
            "पहिला मजला स्लॅब कास्टिंग (First Floor Slab Casting)",
            "विटांचे बांधकाम व कन्सिल्ड फिटिंग (Brickwork & Piping)",
            "आतील व बाहेरील प्लास्टर (Internal & External Plaster)",
            "टाईल्स, फ्लोरिंग व प्लंबिंग (Flooring & Plumbing)",
            "रंगकाम, दरवाजे व फिनिशिंग (Painting & Finishing)",
            "कंपाउंड वॉल व मेन गेट (Compound Wall & Gate)",
            "इतर सानुकूल काम (Custom Work Name...)"
        ]

        selected_work_type = st.selectbox("कामाचा प्रकार:", work_presets, key="sel_work_preset")
        if selected_work_type == "इतर सानुकूल काम (Custom Work Name...)":
            custom_stage_name = st.text_input("कामाचे नाव टाका:", placeholder="उदा. वॉटरप्रूफिंग काम...", key="custom_stg_input")
            final_stage_name = custom_stage_name.strip()
        else:
            final_stage_name = selected_work_type

        init_stage_amt = st.number_input(
            "या कामाचे ठरलेले बिल (₹):",
            min_value=1.0,
            value=50000.0,
            step=1000.0,
            key="new_stage_init_amt"
        )

        if st.button("🔒 कामाचे बिल निश्चित करा व सेव्ह करा", key="btn_create_custom_milestone", type="primary", use_container_width=True):
            if final_stage_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_milestone_payments 
                    (user_key, site_name, stage_name, planned_amount, amount_deposited, status, engineer_approved, client_approved, is_locked, remark)
                    VALUES (?, ?, ?, ?, 0.0, 'Bill Fixed (Unpaid)', 0, 0, 0, 'काही नाही')
                    """,
                    (current_user_name, st.session_state.current_site_name, final_stage_name, float(init_stage_amt)),
                )
                conn.commit()
                conn.close()
                st.success(f"✅ '{final_stage_name}' चे ₹ {init_stage_amt:,.2f} चे बिल निश्चित झाले!")
                st.rerun()
            else:
                st.warning("⚠️ कृपया कामाचे नाव टाका!")

    # ३. मास्टर A4 इनव्हॉइस व स्टेटमेंट
    if milestones:
        with st.expander("📑 NeevPay Master Statement & Invoicing (A4 PDF / Print / Email)", expanded=False):
            table_rows_html = ""
            for idx, m_item in enumerate(milestones, 1):
                p_val = float(m_item["planned_amount"])
                d_val = float(m_item["amount_deposited"])
                bal_val = max(0.0, p_val - d_val)
                stage_pct = (d_val / p_val * 100) if p_val > 0 else 0.0

                if m_item.get("is_locked") == 1:
                    st_badge = "<span style='color: #10b981; font-weight:bold;'>FULLY PAID</span>"
                elif d_val >= p_val and p_val > 0:
                    st_badge = "<span style='color: #0284c7; font-weight:bold;'>READY TO LOCK</span>"
                elif d_val > 0:
                    st_badge = f"<span style='color: #d97706; font-weight:bold;'>PARTIAL ({stage_pct:.1f}%)</span>"
                else:
                    st_badge = "<span style='color: #ef4444; font-weight:bold;'>UNPAID</span>"

                table_rows_html += f"""
                <tr>
                    <td style="text-align:center;">{idx}</td>
                    <td><b>{m_item['stage_name']}</b></td>
                    <td style="text-align:right;">₹ {p_val:,.2f}</td>
                    <td style="text-align:right; color:#10b981; font-weight:bold;">₹ {d_val:,.2f}</td>
                    <td style="text-align:right; color:#ef4444; font-weight:bold;">₹ {bal_val:,.2f}</td>
                    <td style="text-align:center;">{st_badge}</td>
                </tr>
                """

            neevpay_html_doc = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>NEEVPAY MASTER ESCROW - {st.session_state.current_site_name}</title>
                <style>
                    @page {{ size: A4 portrait; margin: 8mm; }}
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 15px; color: #0f172a; background: #ffffff; }}
                    .header-title {{ text-align: center; border-bottom: 2px solid #064e3b; padding-bottom: 6px; margin-bottom: 12px; }}
                    .header-title h1 {{ margin: 0; font-size: 20px; color: #064e3b; font-weight: 800; }}
                    table.info-table {{ width: 100%; font-size: 12px; margin-bottom: 10px; }}
                    table.custom-data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }}
                    table.custom-data-table th, table.custom-data-table td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
                    table.custom-data-table th {{ background-color: #f1f5f9; font-weight: bold; }}
                    .summary-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin-top: 14px; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="header-title">
                    <h1>PATIL INFRATECH - NEEVPAY ESCROW</h1>
                    <p style="margin:2px 0; color:#10b981; font-weight:bold; font-size:12px;">SMART MILESTONE PAYMENT PROTECTION & MASTER INVOICE</p>
                </div>
                <table class="info-table">
                    <tr><td><b>Site:</b> {st.session_state.current_site_name}</td><td style="text-align:right;"><b>Date:</b> {get_ist_time().strftime('%d-%m-%Y')}</td></tr>
                    <tr><td><b>Engineer:</b> {current_user_name}</td><td style="text-align:right;"><b>Client:</b> {client_email or 'N/A'}</td></tr>
                </table>
                <table class="custom-data-table">
                    <thead>
                        <tr><th style="width:25px;">#</th><th>कामाचा टप्पा</th><th>ठरलेले बिल</th><th>जमा</th><th>शिल्लक</th><th>स्थिती</th></tr>
                    </thead>
                    <tbody>{table_rows_html}</tbody>
                </table>
                <div class="summary-box">
                    <b>एकूण बजेट:</b> ₹ {total_budget:,.2f} | <b>जमा:</b> ₹ {total_received:,.2f} | <b>शिल्लक बाकी:</b> ₹ {total_pending:,.2f} | <b>प्रगती:</b> {overall_site_pct:.1f}%
                </div>
            </body>
            </html>
            """

            st.components.v1.html(neevpay_html_doc, height=360, scrolling=True)

            np_c1, np_c2, np_c3 = st.columns(3)
            with np_c1:
                st.download_button(
                    label="📥 Download HTML",
                    data=neevpay_html_doc,
                    file_name=f"NeevPay_Statement_{st.session_state.current_site_name.replace(' ', '_')}.html",
                    mime="text/html",
                    type="primary",
                    use_container_width=True,
                    key="btn_down_neevpay_html"
                )
            with np_c2:
                st.markdown(
                    """
                    <button onclick="window.parent.print()" style="width: 100%; background: #0284c7; color: white; border: none; padding: 9px; border-radius: 8px; font-weight: bold; cursor: pointer; height: 38px;">
                        🖨️ Instant Print
                    </button>
                    """,
                    unsafe_allow_html=True,
                )
            with np_c3:
                if st.button("📧 Email to Client", key="btn_send_client_invoice_mail", use_container_width=True):
                    if client_email:
                        mail_subj = f"Official Escrow Statement: {st.session_state.current_site_name}"
                        mail_body = f"नमस्कार,\n\nतुमच्या '{st.session_state.current_site_name}' साईटचे पेमेंट अपडेट:\n\nएकूण बजेट: ₹ {total_budget:,.2f}\nजमा: ₹ {total_received:,.2f}\nशिल्लक बाकी: ₹ {total_pending:,.2f}\nप्रगती: {overall_site_pct:.1f}%\n\n- Patil Infratech"
                        if send_email_message(client_email, mail_subj, mail_body):
                            st.success(f"✅ इनव्हॉइस '{client_email}' वर पाठवले!")
                        else:
                            st.error("❌ ईमेल पाठवताना त्रुटी आली.")
                    else:
                        st.warning("⚠️ आधी क्लायंटचा ईमेल सेव्ह करा.")

            np_wa_text = (
                f"*PATIL INFRATECH - NEEVPAY STATEMENT*\n"
                f"*Site:* {st.session_state.current_site_name}\n"
                f"*Planned Bill:* ₹ {total_budget:,.2f}\n"
                f"*Deposited:* ₹ {total_received:,.2f}\n"
                f"*Pending:* ₹ {total_pending:,.2f}\n"
                f"*Progress:* {overall_site_pct:.1f}%\n"
            )
            render_whatsapp_feature(urllib.parse.quote(np_wa_text), "neevpay_master_wa")

    # ४. टप्प्यांची यादी, OTP बिल बदल आणि Two-Way संमती
    st.write("---")
    if milestones:
        st.markdown("##### 📋 कामाचे टप्पे व पेमेंट संमती:")
        for m in milestones:
            m_id = m["id"]
            st_name = m["stage_name"]
            p_amt = float(m["planned_amount"])
            d_amt = float(m["amount_deposited"])
            is_locked = bool(m.get("is_locked", 0))
            rem_balance = max(0.0, p_amt - d_amt)
            curr_stage_pct = (d_amt / p_amt * 100) if p_amt > 0 else 0.0

            lock_badge = "🔒 LOCKED" if is_locked else ("🟢 100% PAID" if d_amt >= p_amt and p_amt > 0 else (f"🟡 {curr_stage_pct:.1f}%" if d_amt > 0 else "🔴 UNPAID"))

            with st.expander(f"{st_name} | {lock_badge} | ठरलेले: ₹ {p_amt:,.2f} (जमा: ₹ {d_amt:,.2f})", expanded=not is_locked):
                if is_locked:
                    st.success(f"✅ हा टप्पा १००% पूर्ण भरला असून अंतिम लॉक झाला आहे. (पूर्ण तारीख: {m.get('completion_date', 'N/A')})")
                else:
                    col_b1, col_b2 = st.columns(2)

                    # डावा कॉलम: बिल आणि OTP चेंज
                    with col_b1:
                        st.markdown(f"**कामाचे बिल:** `₹ {p_amt:,.2f}` | **जमा:** `₹ {d_amt:,.2f}`")
                        st.markdown(f"**शिल्लक बाकी:** <span style='color:#ef4444; font-weight:bold;'>₹ {rem_balance:,.2f}</span>", unsafe_allow_html=True)

                        with st.expander("🔐 ठरलेले बिल बदला (Client OTP)"):
                            new_target_bill = st.number_input("सुधारीत बिल (₹):", min_value=max(1.0, float(d_amt)), value=float(p_amt), step=1000.0, key=f"edit_bill_val_{m_id}")
                            otp_session_key = f"neevpay_bill_otp_{m_id}"

                            if st.button("📤 Client ला OTP पाठवा", key=f"btn_send_otp_{m_id}", use_container_width=True):
                                if client_email:
                                    generated_otp = "".join(random.choices(string.digits, k=6))
                                    st.session_state[otp_session_key] = generated_otp
                                    ok_otp, _ = send_live_otp_email(client_email, generated_otp, purpose=f"{st_name} बिल सुधारीत करणे")
                                    if ok_otp:
                                        st.success("✅ OTP पाठवला आहे!")
                                    else:
                                        st.error("❌ एरर आली.")
                                else:
                                    st.warning("⚠️ आधी ईमेल सेव्ह करा.")

                            entered_bill_otp = st.text_input("६ अंकी OTP:", max_chars=6, key=f"input_otp_{m_id}")
                            if st.button("🔐 OTP तपासा व बिल लॉक करा", key=f"btn_verify_bill_otp_{m_id}", type="primary", use_container_width=True):
                                correct_otp = st.session_state.get(otp_session_key)
                                if correct_otp and entered_bill_otp.strip() == correct_otp:
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE site_milestone_payments SET planned_amount = ? WHERE id = ?", (new_target_bill, m_id))
                                    conn.commit()
                                    conn.close()
                                    del st.session_state[otp_session_key]
                                    st.success("🎉 नवीन बिल सेट झाले!")
                                    st.rerun()
                                else:
                                    st.error("❌ चुकीचा OTP!")

                    # उजवा कॉलम: पेमेंट संमती
                    with col_b2:
                        if rem_balance > 0:
                            deposit_val = st.number_input(f"जमा रक्कम (Max ₹ {rem_balance:,.2f}):", min_value=1.0, max_value=float(rem_balance), value=float(rem_balance), step=500.0, key=f"deposit_amt_in_{m_id}")
                            cli_paid_check = st.checkbox(f"🙋‍♂️ **क्लायंट:** मी ₹ {deposit_val:,.0f} दिले.", key=f"chk_client_paid_{m_id}")
                            eng_rcvd_check = st.checkbox(f"👷‍♂️ **इंजिनिअर:** मला ₹ {deposit_val:,.0f} मिळाले.", key=f"chk_eng_rcvd_{m_id}")

                            if st.button("✅ संमतीसह जमा नोंदवा", key=f"btn_confirm_payment_{m_id}", type="primary", use_container_width=True):
                                if cli_paid_check and eng_rcvd_check:
                                    new_deposited = d_amt + deposit_val
                                    new_status = "Payment Completed" if new_deposited >= p_amt else "Partially Paid"
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "UPDATE site_milestone_payments SET amount_deposited = ?, status = ?, engineer_approved = 1, client_approved = 1 WHERE id = ?",
                                        (new_deposited, new_status, m_id),
                                    )
                                    conn.commit()
                                    conn.close()
                                    st.success("🎉 पेमेंट नोंद झाली!")
                                    st.rerun()
                                else:
                                    st.error("⚠️ दोघांची संमती आवश्यक आहे!")

                        if p_amt > 0 and d_amt >= p_amt:
                            if st.button("🔒 हा टप्पा अंतिम लॉक करा", key=f"btn_final_lock_{m_id}", type="primary", use_container_width=True):
                                today_str = get_ist_time().strftime("%d-%m-%Y %H:%M")
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute("UPDATE site_milestone_payments SET is_locked = 1, status = 'Fully Completed & Locked', completion_date = ? WHERE id = ?", (today_str, m_id))
                                conn.commit()
                                conn.close()
                                st.success("🔒 टप्पा कायमस्वरूपी लॉक झाला!")
                                st.rerun()

                        if d_amt == 0:
                            if st.button("🗑️ टप्पा डिलीट करा", key=f"btn_del_stage_{m_id}", use_container_width=True):
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM site_milestone_payments WHERE id = ?", (m_id,))
                                conn.commit()
                                conn.close()
                                st.rerun()


# ==========================================
# 📌 विभाग १९: HOUSE ESTIMATOR मुख्य मॉड्यूल (Quick Thumb Rule Quotation)
# ==========================================
elif st.session_state.selected_module == "House Estimator":
    col_back, _ = st.columns([1.5, 3.5])
    with col_back:
        if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_house_est", use_container_width=True):
            st.session_state.selected_module = None
            st.rerun()

    st.write("---")
    st.markdown(
        """
        <div style="background: #111827; border: 1px solid #1f2937; border-left: 5px solid #38bdf8; padding: 14px 18px; border-radius: 10px; margin-bottom: 16px;">
            <h3 style="margin: 0; color: #38bdf8; font-size: 18px; font-weight: 800;">🏠 PATIL INFRATECH - QUICK HOUSE ESTIMATOR</h3>
            <p style="margin: 3px 0 0 0; color: #94a3b8; font-size: 12px;">Ground ते G+10 मजल्यांपर्यंत घराचा/इमारतीचा प्राथमिक थंब-रूल अंदाज व ऑन-डिमांड कोटेशन.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    h_col1, h_col2 = st.columns(2)
    with h_col1:
        builtup_area = st.number_input("एका मजल्याचे क्षेत्रफळ (Sq. Ft.):", min_value=100.0, value=1000.0, step=50.0, key="he_builtup_area")
    with h_col2:
        upper_floors = st.number_input("वरच्या मजल्यांची संख्या (G + ?):", min_value=0, max_value=10, value=1, step=1, key="he_floors_num")

    total_floors_count = 1 + upper_floors
    floors_label = "Ground Floor Only" if upper_floors == 0 else f"G + {upper_floors} Floors ({total_floors_count} मजले)"
    total_calc_area = builtup_area * total_floors_count

    st.info(f"🏢 **संरचना:** {floors_label} | **एकूण बिल्ट-अप क्षेत्रफळ:** `{total_calc_area:,.0f} Sq. Ft.`")

    h_col3, h_col4 = st.columns(2)
    with h_col3:
        quality_custom_name = st.text_input("पॅकेजचे नाव:", value="Standard Quality (मध्यम दर्जा)", key="he_quality_name")
    with h_col4:
        unit_cost_sqft = st.number_input("दर प्रति चौ. फूट (₹):", min_value=500.0, value=1650.0, step=50.0, key="he_custom_sqft_rate")

    with st.expander("⚙️ स्थानिक साहित्याचे दर बदला (ऐच्छिक)"):
        cr1, cr2, cr3 = st.columns(3)
        with cr1:
            h_cem_rate = st.number_input("सिमेंट (₹/Bag):", min_value=100.0, value=400.0, step=10.0, key="he_crate_cem")
            h_sand_rate = st.number_input("वाळू (₹/Brass):", min_value=500.0, value=6500.0, step=100.0, key="he_crate_sand")
        with cr2:
            h_steel_rate = st.number_input("स्टील (₹/Kg):", min_value=30.0, value=65.0, step=1.0, key="he_crate_steel")
            h_agg_rate = st.number_input("खडी (₹/Brass):", min_value=500.0, value=3500.0, step=100.0, key="he_crate_agg")
        with cr3:
            h_brick_rate = st.number_input("विटा (₹/नग):", min_value=2.0, value=8.5, step=0.5, key="he_crate_brick")

    if st.button("📊 CALCULATE ESTIMATE", type="primary", use_container_width=True, key="btn_run_house_est"):
        st.session_state["house_est_calculated"] = True

    if st.session_state.get("house_est_calculated", False):
        total_house_cost = total_calc_area * unit_cost_sqft
        c_bags_needed = math.ceil(total_calc_area * 0.40)
        steel_kg_needed = math.ceil(total_calc_area * (4.2 if upper_floors >= 3 else 3.8))
        sand_brass_needed = round(total_calc_area * 0.018, 2)
        agg_brass_needed = round(total_calc_area * 0.0135, 2)
        bricks_needed = math.ceil(total_calc_area * 18.0)

        cost_cement = c_bags_needed * h_cem_rate
        cost_steel = steel_kg_needed * h_steel_rate
        cost_sand = sand_brass_needed * h_sand_rate
        cost_agg = agg_brass_needed * h_agg_rate
        cost_bricks = bricks_needed * h_brick_rate
        cost_labour = total_house_cost * 0.25
        cost_misc = total_house_cost * 0.10

        st.success(f"🎉 एकूण अंदाजित खर्च: ₹ {total_house_cost:,.2f}/- ({total_calc_area:,.0f} Sq.Ft. @ ₹{unit_cost_sqft:,.2f}/sq.ft)")

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("एकूण बजेट", f"₹ {total_house_cost:,.2f}")
        mc2.metric("सिमेंट", f"{c_bags_needed} Bags")
        mc3.metric("स्टील", f"{steel_kg_needed} Kg ({round(steel_kg_needed/1000, 2)} MT)")
        mc4.metric("विटा", f"{bricks_needed:,} Nos")

        st.write("---")

        house_html_doc = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>PATIL INFRATECH - House Estimate</title>
            <style>
                @page {{ size: A4 portrait; margin: 8mm; }}
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 15px; color: #0f172a; background: #ffffff; }}
                .header-title {{ text-align: center; border-bottom: 2px solid #0c4a6e; padding-bottom: 6px; margin-bottom: 12px; }}
                .header-title h1 {{ margin: 0; font-size: 20px; color: #0c4a6e; }}
                table.info-table {{ width: 100%; font-size: 12px; margin-bottom: 10px; }}
                table.custom-data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }}
                table.custom-data-table th, table.custom-data-table td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
                table.custom-data-table th {{ background-color: #f1f5f9; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header-title">
                <h1>PATIL INFRATECH</h1>
                <p style="margin:2px 0; color:#0284c7; font-weight:bold; font-size:12px;">PRELIMINARY HOUSE CONSTRUCTION ESTIMATE</p>
            </div>
            <table class="info-table">
                <tr><td><b>Site:</b> {st.session_state.current_site_name}</td><td style="text-align:right;"><b>Date:</b> {get_ist_time().strftime('%d-%m-%Y')}</td></tr>
                <tr><td><b>Structure:</b> {floors_label} ({total_calc_area:,.0f} sq.ft)</td><td style="text-align:right;"><b>Rate:</b> ₹ {unit_cost_sqft:,.2f} / sq.ft</td></tr>
            </table>
            <table class="custom-data-table">
                <thead>
                    <tr><th>#</th><th>घटक</th><th>प्रमाण</th><th>युनिट</th><th>दर</th><th>रक्कम (₹)</th></tr>
                </thead>
                <tbody>
                    <tr><td>1</td><td>सिमेंट (Cement)</td><td>{c_bags_needed}</td><td>Bags</td><td>₹ {h_cem_rate:.2f}</td><td>₹ {cost_cement:,.2f}</td></tr>
                    <tr><td>2</td><td>स्टील (TMT Steel)</td><td>{steel_kg_needed}</td><td>Kg</td><td>₹ {h_steel_rate:.2f}</td><td>₹ {cost_steel:,.2f}</td></tr>
                    <tr><td>3</td><td>वाळू (Sand)</td><td>{sand_brass_needed}</td><td>Brass</td><td>₹ {h_sand_rate:.2f}</td><td>₹ {cost_sand:,.2f}</td></tr>
                    <tr><td>4</td><td>खडी (Aggregate)</td><td>{agg_brass_needed}</td><td>Brass</td><td>₹ {h_agg_rate:.2f}</td><td>₹ {cost_agg:,.2f}</td></tr>
                    <tr><td>5</td><td>विटा (Bricks)</td><td>{bricks_needed}</td><td>Nos</td><td>₹ {h_brick_rate:.2f}</td><td>₹ {cost_bricks:,.2f}</td></tr>
                    <tr><td>6</td><td>मजुरी (Labour ~25%)</td><td>-</td><td>L.S.</td><td>-</td><td>₹ {cost_labour:,.2f}</td></tr>
                    <tr><td>7</td><td>प्लंबिंग व इतर (~10%)</td><td>-</td><td>L.S.</td><td>-</td><td>₹ {cost_misc:,.2f}</td></tr>
                </tbody>
            </table>
            <h3 style="text-align:right; margin-top:14px; color:#0c4a6e;">अंदाजित एकूण बजेट: ₹ {total_house_cost:,.2f}/-</h3>
        </body>
        </html>
        """

        with st.expander("👁️ A4 कोटेशन प्रिव्ह्यू व डाऊनलोड", expanded=False):
            st.components.v1.html(house_html_doc, height=360, scrolling=True)

            hb1, hb2 = st.columns(2)
            with hb1:
                st.download_button(
                    label="📥 Download HTML Quotation",
                    data=house_html_doc,
                    file_name=f"Patil_Infratech_Estimate_{st.session_state.current_site_name.replace(' ', '_')}.html",
                    mime="text/html",
                    type="primary",
                    use_container_width=True,
                )
            with hb2:
                st.markdown(
                    """
                    <button onclick="window.parent.print()" style="width: 100%; background: #0284c7; color: white; border: none; padding: 9px; border-radius: 8px; font-weight: bold; cursor: pointer; height: 38px;">
                        🖨️ Instant Print
                    </button>
                    """,
                    unsafe_allow_html=True,
                )

        if current_user_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                (
                    current_user_name,
                    get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                    f"House Est: {floors_label} ({total_calc_area:,.0f} sqft)",
                    f"Budget: ₹{total_house_cost:,.2f}",
                    st.session_state.current_site_name,
                ),
            )
            conn.commit()
            conn.close()

        he_wa_msg = (
            f"🏠 *PATIL INFRATECH - BUILDING ESTIMATE*\n"
            f"*Site:* {st.session_state.current_site_name}\n"
            f"*Structure:* {floors_label} ({total_calc_area:,.0f} sq.ft)\n"
            f"*Rate:* ₹{unit_cost_sqft:,.2f} / sq.ft\n"
            f"💰 *अंदाजित एकूण बजेट:* ₹ {total_house_cost:,.2f}/-\n\n"
            f"• सिमेंट: {c_bags_needed} Bags\n"
            f"• स्टील: {steel_kg_needed} kg\n"
            f"• वाळू: {sand_brass_needed} Brass\n"
            f"• खडी: {agg_brass_needed} Brass\n"
            f"• विटा: {bricks_needed} Nos\n"
        )
        render_whatsapp_feature(urllib.parse.quote(he_wa_msg), "house_single_wa_key")
