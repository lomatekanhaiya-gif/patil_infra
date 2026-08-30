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
    initial_sidebar_state="expanded",  # Gemini सारखा sidebar दिसावा म्हणून
)

# ==========================================
# 📌 विभाग ३: ब्राउझर लोकल स्टोरेज आणि मोबाईल बॅक बटन हँडलर
# ==========================================
st.markdown(
    """
    <script>
    // १. मोबाईलचा बॅक बटन दाबताच ट्रिगर होणारा इव्हेंट
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

    // २. स्लीप मोडनंतर किंवा स्क्रीन रिफ्रेश झाल्यावर LocalStorage मधून लॉगिन पूर्ववत करणे
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
    """जेव्हा युझर नवीन सब-मॉड्यूलवर क्लिक करेल तेव्हा ब्राउझर हिस्ट्रीमध्ये पुश करण्यासाठी हूक"""
    st.markdown(
        "<script>window.history.pushState({inSubModule: true}, '');</script>",
        unsafe_allow_html=True,
    )

# ==========================================
# 📌 विभाग ४: युटिलिटी आणि सपोर्ट फंक्शन्स (वेळ, ईमेल, पासवर्ड, SMTP Mailer & Weather)
# ==========================================
def get_ist_time():
    """भारतीय प्रमाणवेळ (IST - Indian Standard Time) मिळवण्याचे फंक्शन"""
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    return ist_now


def generate_random_code():
    """प्रिमियम ॲक्टिव्हेशन कोड जनरेट करणे"""
    return "PATIL-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )


def send_email_message(receiver_email, subject, body_text):
    """ईमेल OTP आणि तपशील पाठवण्याचे फंक्शन"""
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


def send_live_otp_email(to_email, otp_code, purpose="Verification"):
    """NeevPay साठी थेट ईमेलवर HTML फॉरमॅटमध्ये OTP पाठवणारे फंक्शन"""
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
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #10b981; border-radius: 10px; max-width: 500px;">
        <h2 style="color: #064e3b; margin-top:0;">PATIL INFRATECH - NEEVPAY</h2>
        <p>प्रिय क्लायंट / घरमालक,</p>
        <p>तुमच्या साईटच्या <b>{purpose}</b> साठी खालील OTP तयार करण्यात आला आहे:</p>
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-size: 28px; font-weight: 900; letter-spacing: 5px; color: #10b981; background: #f0fdf4; padding: 10px 20px; border-radius: 8px; border: 1px dashed #10b981;">
                {otp_code}
            </span>
        </div>
        <p style="color: #ef4444; font-size: 13px;">⚠️ हा OTP अत्यंत गोपनीय आहे. इंजिनिअरशी चर्चा करून संमती असल्यासच हा OTP शेअर करा.</p>
        <hr style="border: 0.5px solid #e2e8f0;">
        <small style="color: #64748b;">Patil Infratech • Automated Security System</small>
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
    """पासवर्ड सुरक्षितता तपासणी"""
    if len(password) < 8:
        return False, "पासवर्ड कमीत कमी ८ अक्षरांचा असावा."
    if not re.search(r"\d", password):
        return False, "पासवर्डमध्ये कमीत कमी एक नंबर (0-9) असावा."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "पासवर्डमध्ये कमीत कमी एक विशेष चिन्ह (!@#$%^&*) असावे."
    return True, "Strong"


def get_site_weather_forecast(city_name="Pune"):
    """ओपन-मेटिओ API द्वारे शहराचा रिअल-टाइम वेदर आणि पावसाचा अंदाज (%) मिळवणे"""
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
# 📌 विभाग ५: SQLITE डेटाबेस मॅनेजमेंट आणि मॉडेल्स
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

    # ८. साहित्य इन्व्हेंटरी टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_key TEXT,
            date TEXT,
            material_name TEXT,
            transaction_type TEXT,
            quantity INTEGER,
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

    # डीफॉल्ट फिचर लॉक्स
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

    # डीफॉल्ट मार्केट दर
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
# 📌 विभाग ७: सेशन स्टेट्स आणि प्रिमियम ऑथेंटिकेशन
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
    ("admin_dashboard_tab", "rates"),
    ("current_comment", "काही नाही"),
    ("selected_module", None),
    ("selected_site_sub_module", None),
    ("selected_estimator_sub_module", None),
    ("admin_view", "main"),
    ("admin_selected_user", None),
    ("current_site_name", "पाटील रेसिडेन्सी - साईट १"),
    ("all_sites_data", {"Default Site": {"milestones": [], "created_at": "26-08-2026"}}),
    ("site_location_city", "Pune"),
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
    """प्रिमियम वैधता आणि उरलेला कालावधी तपासणे"""
    if not username:
        return False, "Free"
    if username.lower() == "kanha" or username == "9999999999":
        return True, "Master Lifetime VIP"

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
# 📌 विभाग ८: BRANDED CONSTRUCTION THEME CSS
# ==========================================
st.markdown(
    """
    <style>
    #MainMenu { visibility: hidden; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; display: none !important; }
    footer { visibility: hidden; display: none !important; }
    .stAppHeader { display: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; }
    button[title="Increment"], button[title="Decrement"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 50%, #020617 100%) !important;
        color: #f8fafc !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }

    .brand-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #334155 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-top: 4px solid #f59e0b;
        padding: 24px 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 0 20px rgba(245, 158, 11, 0.15);
        margin-bottom: 24px;
    }

    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-testid="stNumberInputContainer"],
    div[data-testid="stTextInput"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
    }

    input, select, textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    input:focus, textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.3) !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5) !important;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
    }

    div.stButton > button {
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }

    .module-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px 16px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .module-card:hover {
        border-color: #f59e0b;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
    }

    .gold-vip-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        color: #000000 !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 13px;
        display: inline-block;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .free-user-badge {
        background: #1e293b;
        color: #38bdf8 !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        border: 1px solid #0284c7;
        display: inline-block;
    }

    .galaxy-loader {
        margin: 20px auto;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid transparent;
        border-top-color: #f59e0b;
        border-bottom-color: #00f2fe;
        animation: spin-galaxy 1.5s linear infinite;
        box-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
    }
    @keyframes spin-galaxy {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
        100% { transform: rotate(360deg) scale(1); }
    }

    /* AutoCAD Portal & Workspace Ribbon Custom Elements */
    .autocad-dwg-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }
    .autocad-dwg-card:hover {
        border-color: #38bdf8;
        background: rgba(30, 41, 59, 0.95);
        transform: translateX(4px);
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
            <a href="https://wa.me/?text={encoded_msg}" target="_blank">
                <button style="width: 100%; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);">
                    📱 Share Full Report on WhatsApp {"(🆓 Free Access)" if wa_lock_setting == "Free" else "(👑 VIP Premium Active)"}
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
    else:
        safe_uid = f"{key_prefix}_{abs(hash(encoded_msg)) % 100000}"

        with st.expander("🔒 WhatsApp Report Sharing - Unlock Premium"):
            st.warning("⚠️ व्हॉट्सॲपवर पूर्ण रिपोर्ट शेअर करण्याचे फीचर प्रिमियम युझर्ससाठी आहे.")
            st.caption("💡 अनलॉक करण्यासाठी Admin कडून आलेला प्रिमियम कोड खाली टाका:")

            p_code = st.text_input(
                "Enter Activation Code:", key=f"{safe_uid}_code_input"
            ).strip()

            w_col1, w_col2 = st.columns(2)
            with w_col1:
                if st.button("🔓 Unlock WhatsApp Share Now", key=f"{safe_uid}_unlock_btn"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT * FROM premium_codes WHERE code = ?", (p_code,)
                    )
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

                            cursor.execute(
                                "UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?",
                                (current_user_name, now_str, p_code),
                            )

                            disp_name = current_user_name if current_user_name else ""
                            welcome_msg = f"{disp_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"

                            cursor.execute(
                                """
                                UPDATE users 
                                SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?, admin_message = ?, unread_notification = 0
                                WHERE user_key = ?
                                """,
                                (
                                    exp_str,
                                    "Kanhaiya (Founder of Patil Infratech)",
                                    welcome_msg,
                                    current_user_name,
                                ),
                            )

                            conn.commit()
                            conn.close()
                            st.rerun()
                    else:
                        conn.close()
                        st.error("❌ चुकीचा प्रिमियम कोड! कृपया अचूक कोड टाका.")

            with w_col2:
                if st.button("📩 Request Code from Admin", key=f"{safe_uid}_req_btn"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET requested_code = 1 WHERE user_key = ?",
                        (current_user_name,),
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ ॲडमीनला कोडसाठी रिक्वेस्ट पाठवली आहे!")

# ==========================================
# 📌 विभाग १०: वेलकम स्क्रीन ॲनिमेशन (3D Cosmic Loader & Sponsor Ads)
# ==========================================
welcome_placeholder = st.empty()

if "welcome_completed" not in st.session_state:
    st.session_state.welcome_completed = False

if not st.session_state.welcome_completed:
    with welcome_placeholder.container():
        st.markdown("<br><div class='galaxy-loader'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="brand-header">
                <div style="font-size: 38px; margin-bottom: 4px;">🏗️</div>
                <h1 style='color: #ffffff; margin:0; font-size: 30px; font-weight: 900; letter-spacing: 1px;'>PATIL INFRATECH</h1>
                <p style='color: #f59e0b; margin:6px 0 0 0; font-size: 15px; font-weight: 700; text-transform: uppercase;'>
                    Civil Engineering • Quantity Surveying • Site Management
                </p>
                <div style="margin-top: 10px; display: inline-block; background: rgba(0,0,0,0.3); padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
                    <small style='color: #94a3b8; font-size: 12px;'>Concept & Logic by: <b style="color:#f8fafc;">Kanhaiya (Founder)</b></small>
                </div>
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
                <div style="background: #0f172a; border: 1px solid #f59e0b; padding: 10px 14px; border-radius: 12px; text-align: center; margin: 15px auto; max-width: 300px; box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);">
                    <span style="font-size: 10px; color: #f59e0b; font-weight: bold;">⭐ SPONSOR</span><br>
                    <b style="color: #ffffff; font-size: 14px;">{ad_dict.get('title')}</b>
                    <p style="color: #94a3b8; font-size: 11px; margin: 3px 0;">{ad_dict.get('desc')}</p>
                    {"<img src='" + ad_dict.get('media_url') + "' style='max-height:50px; border-radius:6px; margin-top:3px;'/>" if ad_dict.get('media_type') == 'Photo (PNG/JPG)' and ad_dict.get('media_url') else ""}
                    <br><a href="{ad_dict.get('link')}" target="_blank" style="color: #f59e0b; font-weight: bold; text-decoration: underline; font-size: 12px;">👉 Visit Link</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        progress_bar = st.progress(0)
        status_text = st.empty()

        construction_stages = [
            "🧱 पाया खोदण्याचे काम सुरू आहे...",
            "🏗️ खांब आणि कॉलम उभे राहत आहेत...",
            "🧱 विटांचे बांधकाम (Brickwork) प्रगतीपथावर आहे...",
            "🏠 छताचे (Slab) काम पूर्ण होत आहे...",
            "✨ फिनिशिंग आणि रंगकाम पूर्ण झाले! घर तयार आहे! 🎉",
        ]

        for i in range(5):
            status_text.markdown(
                f"<p style='text-align: center; font-size: 18px; font-weight: bold; color: #f8fafc;'>{construction_stages[i]}</p>",
                unsafe_allow_html=True,
            )
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.3)

    welcome_placeholder.empty()
    st.session_state.welcome_completed = True

# मुख्य ॲप हेडर बॅनर
st.markdown(
    """
    <div class="brand-header">
        <div style="font-size: 38px; margin-bottom: 4px;">🏗️</div>
        <h1 style='color: #ffffff; margin:0; font-size: 30px; font-weight: 900; letter-spacing: 1px;'>PATIL INFRATECH</h1>
        <p style='color: #f59e0b; margin:6px 0 0 0; font-size: 15px; font-weight: 700; text-transform: uppercase;'>
            Civil Engineering • Quantity Surveying • Site Management
        </p>
        <div style="margin-top: 10px; display: inline-block; background: rgba(0,0,0,0.3); padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
            <small style='color: #94a3b8; font-size: 12px;'>Concept & Logic by: <b style="color:#f8fafc;">Kanhaiya (Founder)</b></small>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 📌 विभाग ११: ॲडमीन पॅनल (Admin Command Center)
# ==========================================
if st.session_state.is_admin_logged:
    st.markdown(
        """
        <div class="admin-command-center">
            <h1 style='color: #ec38bc; margin:0; font-size: 28px; text-align: center;'>⚡ KANHAIYA'S EXECUTIVE COMMAND CENTER</h1>
            <p style='color: #cbd5e1; margin:5px 0 0 0; font-size: 14px; text-align: center;'>👑 Patil Infratech Master Control & Management Hub</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    elif current_tab == "locks":
        st.markdown("### ⚙️ Feature Lock Manager")
        cur_locks = get_feature_locks()

        fl_calc = st.selectbox("Civil Calculator Access:", ["Free", "Premium"], index=0 if cur_locks.get("Civil Calculator", "Free") == "Free" else 1)
        fl_ra = st.selectbox("Rate Analysis Module Access:", ["Free", "Premium"], index=0 if cur_locks.get("Rate Analysis", "Free") == "Free" else 1)
        fl_bbs = st.selectbox("BBS Calculator Access:", ["Free", "Premium"], index=0 if cur_locks.get("BBS", "Free") == "Free" else 1)
        fl_qs = st.selectbox("Quantity Surveying Access:", ["Free", "Premium"], index=0 if cur_locks.get("Quantity Surveying", "Free") == "Free" else 1)
        fl_site = st.selectbox("Site Manager Access:", ["Free", "Premium"], index=0 if cur_locks.get("Site Manager", "Free") == "Free" else 1)
        fl_neev = st.selectbox("NeevPay Payment Protection Access:", ["Free", "Premium"], index=0 if cur_locks.get("NeevPay", "Free") == "Free" else 1)
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

            status_badge = (
                f"👑 VIP MEMBER: {u_name.upper()}"
                if u_prem
                else (
                    "🚨 CODE REQUESTED!"
                    if is_req
                    else f"🆓 FREE: {u_name.upper()}"
                )
            )

            st.markdown(f"#### 👤 MANAGE USER: <span style='color:#ec38bc;'>{u_name.upper()}</span>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="admin-user-card">
                    <p style="margin:5px 0; font-size:16px;"><b>माहिती/स्टेटस:</b> <span class="gold-vip-badge">{status_badge}</span></p>
                    <p style="margin:5px 0; font-size:15px;"><b>Username/UID:</b> <code style="color:#00f2fe; font-size:15px;">{u_uid}</code> | <b>Password:</b> <code>{u_pin}</code> | <b>Email:</b> <code>{u_email}</code></p>
                    <p style="margin:8px 0 5px 0; font-size:15px;"><b>प्रिमियम मुदत (Expiry):</b> <code>{exp_date}</code></p>
                    <p style="margin:5px 0; font-size:15px;"><b>ॲक्टिव्ह कोड (Unused):</b> <code style="color:#10b981; font-size:16px;">{assigned_code if assigned_code else 'काही नाही'}</code></p>
                    <p style="margin:5px 0; font-size:14px; color:#94a3b8;"><b>युझर कमेंट:</b> {u_comm}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if assigned_code:
                st.info(f"💡 {u_name} साठी आधीच एक कोड तयार आहे: `{assigned_code}`")
            else:
                if st.button(f"🚀 Generate & Send Unique Code to {u_name}", key=f"win_gen_send_{target_user}"):
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
                cursor.execute(
                    """
                    UPDATE users 
                    SET is_premium = 1, premium_expiry = ?, requested_code = 0, seen_popup = 0, activated_by = ?
                    WHERE user_key = ?
                    """,
                    (
                        exp_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Kanhaiya (Founder of Patil Infratech)",
                        target_user,
                    ),
                )
                conn.commit()
                conn.close()
                st.success(f"✅ {u_name} साठी {time_val} {time_unit} सेव्ह केले!")
                st.rerun()

            if u_prem:
                if st.button(f"🔻 Revoke Premium: {u_name}", key=f"win_rev_{target_user}"):
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

            st.markdown("---")
            current_msg = info.get("admin_message", "Admin message...")
            new_msg = st.text_input(
                f"✍️ {u_name} साठी इनबॉक्स मेसेज बदलणे (Notification Send):",
                value=current_msg,
                key=f"win_msg_{target_user}",
            )
            if st.button(f"✉️ मेसेज सेव्ह करा व पाठवा ({u_name})", key=f"win_btn_msg_{target_user}"):
                if new_msg.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET admin_message = ?, unread_notification = 1 WHERE user_key = ?",
                        (new_msg.strip(), target_user),
                    )
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
                    ts = hist.get("timestamp", "N/A")
                    with st.expander(f"🗓️ रिपोर्ट #{idx} | तारीख व वेळ: `{ts}`"):
                        st.markdown(hist.get("report_data", "डेटा उपलब्ध नाही"))
            else:
                st.info("ℹ️ या युझरने अजून एकही रिपोर्ट जनरेट केलेला नाही.")
        else:
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

                    col_u1, col_u2 = st.columns([3.2, 1.8])
                    if u_prem:
                        col_u1.markdown(
                            f"<span class='gold-vip-badge'>👑 VIP: {u_name.upper()}</span> (User ID: <code>{u_uid}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>",
                            unsafe_allow_html=True,
                        )
                    elif is_req:
                        col_u1.markdown(
                            f"#### 👤 **{u_name}** `[🚨 CODE]` (User ID: `{u_uid}`)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>",
                            unsafe_allow_html=True,
                        )
                    else:
                        col_u1.markdown(
                            f"<span class='free-user-badge'>🆓 FREE: {u_name.upper()}</span> (User ID: <code>{u_uid}</code>)<br><small style='color: {'#10b981' if is_online else '#ef4444'}; font-weight: bold;'>Status: {status_indicator}</small>",
                            unsafe_allow_html=True,
                        )

                    if col_u2.button("👁️ View / Manage", key=f"open_user_win_{mob}"):
                        st.session_state.admin_view = "user_detail"
                        st.session_state.admin_selected_user = mob
                        trigger_push_state()
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

    elif current_tab == "broadcast":
        st.markdown("### 🔔 Broadcast Notification to All Users")
        with st.form("broadcast_form"):
            broadcast_msg = st.text_area(
                "सर्व युझर्सना पाठवायचा मेसेज (Broadcast Message):",
                placeholder="उदा. नवीन अपडेट आली आहे, चेक करा...",
            )
            submit_broadcast = st.form_submit_button("🚀 Send to All Users (Broadcast)", type="primary")

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
        "🔑 Registered User Login",
        "📧 Email OTP Register / Verification",
        "🔍 Client / Owner Live Site View (घरमालक व्ह्यू)"
    ])

    # १२.१ Registered User Login
    with login_tab:
        with st.form("direct_login_form"):
            login_email = st.text_input("ईमेल किंवा Username (Email ID / Username):").strip()
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
                        found_user = row["user_key"]
                        st.session_state.app_user_name = found_user
                        st.session_state.is_client_view = False
                        st.query_params["saved_user"] = found_user

                        st.markdown(
                            f"""
                            <script>
                                localStorage.setItem("patil_app_user", "{found_user}");
                            </script>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.success("🎉 यशस्वीरित्या लॉगिन झाले!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा ईमेल/Username किंवा पासवर्ड! कृपया तपासा.")
                else:
                    st.warning("⚠️ कृपया ईमेल/Username आणि पासवर्ड दोन्ही भरा.")

    # १२.२ Email OTP Registration & Setup
    with otp_tab:
        st.markdown("#### 📧 Email OTP Verification & Account Creation")
        email_input = st.text_input("तुमचा ईमेल आयडी टाका (Email ID):", key="otp_email_key").strip()

        if not st.session_state.otp_verified:
            if st.button("📤 Send OTP to Email", type="primary"):
                if email_input and "@" in email_input:
                    generated_otp = "".join(random.choices(string.digits, k=6))
                    st.session_state.generated_otp = generated_otp
                    st.session_state.pending_email = email_input

                    with st.spinner("📧 ईमेलवर OTP पाठवत आहे..."):
                        subject = "PATIL INFRATECH - Verification OTP"
                        body = (
                            "नमस्कार!\n\nतुमचा पाटील इन्फ्राटेक लॉगिन/रेजिस्ट्रेशन OTP हा"
                            f" आहे: {generated_otp}\nहा OTP कोणासोबतही शेअर करू"
                            " नका.\n\n- Kanhaiya (Founder of Patil Infratech)"
                        )
                        success = send_email_message(email_input, subject, body)

                        if success:
                            st.success("✅ तुमच्या ईमेलवर 6 अंकी OTP पाठवला आहे! खाली टाका.")
                        else:
                            st.error("❌ ईमेल पाठवताना एरर आली. (SMTP क्रेडेन्शियल्स तपासा)")
                else:
                    st.warning("⚠️ कृपया वैध ईमेल आयडी टाका!")

            if st.session_state.generated_otp:
                entered_otp = st.text_input("6 अंकी OTP टाका:", max_chars=6).strip()
                if st.button("🔐 Verify OTP"):
                    if entered_otp == st.session_state.generated_otp:
                        st.session_state.otp_verified = True
                        st.success("✅ OTP यशस्वीरित्या व्हेरिफाय झाला आहे!")
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा OTP! कृपया पुन्हा प्रयत्न करा.")

        if st.session_state.otp_verified and st.session_state.pending_email:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (st.session_state.pending_email,))
            row = cursor.fetchone()
            conn.close()

            if row:
                user_data = dict(row)
                found_user = user_data["user_key"]
                st.session_state.app_user_name = found_user
                st.session_state.is_client_view = False
                st.query_params["saved_user"] = found_user

                st.markdown(
                    f"""
                    <script>
                        localStorage.setItem("patil_app_user", "{found_user}");
                    </script>
                    """,
                    unsafe_allow_html=True,
                )

                st.success(f"🎉 स्वागत आहे {found_user}! लॉगिन होत आहे...")
                time.sleep(1)
                st.rerun()
            else:
                st.info("✨ नवीन युझर! कृपया खालील माहिती भरून युझरनेम आणि मजबूत पासवर्ड सेट करा:")
                with st.form("custom_reg_form"):
                    custom_username = st.text_input("तुमचे नाव किंवा युनिक Username बनावा:").strip()
                    custom_password = st.text_input(
                        "मजबूत पासवर्ड (Set Strong Password):",
                        type="password",
                        help="कमीत कमी ८ अक्षरे, १ अंक आणि १ विशेष चिन्ह (!@#$%) असणे आवश्यक आहे.",
                    ).strip()
                    confirm_password = st.text_input("पासवर्ड पुन्हा टाका (Confirm Password):", type="password").strip()

                    submit_custom_reg = st.form_submit_button("🚀 Complete Registration & Create Account", type="primary")

                    if submit_custom_reg:
                        if custom_username and custom_password and confirm_password:
                            if custom_password != confirm_password:
                                st.error("❌ पासवर्ड आणि कंफर्म पासवर्ड जुळत नाहीत!")
                            else:
                                is_strong, msg = is_strong_password(custom_password)
                                if not is_strong:
                                    st.error(f"❌ पासवर्ड कमजोर आहे: {msg}")
                                else:
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "SELECT user_key FROM users WHERE user_key = ? OR uid = ?",
                                        (custom_username, custom_username),
                                    )
                                    if cursor.fetchone():
                                        conn.close()
                                        st.error("❌ हा Username आधीच वापरला गेला आहे, कृपया दुसरा टाका!")
                                    else:
                                        welcome_msg = f"{custom_username} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                                        cursor.execute(
                                            """
                                            INSERT INTO users (
                                                user_key, id, uid, pin, mobile, email, password, comment, 
                                                admin_message, unread_notification, is_premium, premium_expiry, 
                                                requested_code, seen_popup, master_code_uses, last_active, activated_by
                                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, NULL, 0, 0, 0, ?, ?)
                                            """,
                                            (
                                                custom_username,
                                                custom_username,
                                                custom_username,
                                                custom_password,
                                                "N/A",
                                                st.session_state.pending_email,
                                                custom_password,
                                                "काही नाही",
                                                welcome_msg,
                                                now_str,
                                                "Free User",
                                            ),
                                        )
                                        conn.commit()
                                        conn.close()

                                        subject = "PATIL INFRATECH - Account Created Successfully!"
                                        body = (
                                            f"नमस्कार {custom_username}!\n\nपाटील इन्फ्राटेक मध्ये"
                                            " तुमचे अकाउंट यशस्वीरित्या तयार झाले आहे.\n\nतुमचा"
                                            f" लॉगिन तपशील:\nUsername: {custom_username}\nPassword:"
                                            f" {custom_password}\nRegistered Email:"
                                            f" {st.session_state.pending_email}\n\nतुम्ही पुढील"
                                            " वेळी ईमेल/युझरनेम आणि पासवर्ड वापरून लॉगिन करू"
                                            " शकता.\n\n- Kanhaiya (Founder of Patil Infratech)"
                                        )
                                        send_email_message(st.session_state.pending_email, subject, body)

                                        st.session_state.app_user_name = custom_username
                                        st.session_state.is_client_view = False
                                        st.query_params["saved_user"] = custom_username

                                        st.markdown(
                                            f"""
                                            <script>
                                                localStorage.setItem("patil_app_user", "{custom_username}");
                                            </script>
                                            """,
                                            unsafe_allow_html=True,
                                        )

                                        st.success("🎉 अकाउंट यशस्वीरित्या तयार झाले! डिटेल्स ईमेलवर पाठवले आहेत.")
                                        time.sleep(1)
                                        st.rerun()
                        else:
                            st.warning("⚠️ कृपया सर्व माहिती भरा!")

    # १२.३ 🔍 Client Read-Only Live Portal View (घरमालकांसाठी)
    with client_tab:
        st.markdown("#### 🔍 घरमालक / क्लायंट लाईव्ह पोर्टल (Read-Only View)")
        st.caption("घरमालक कोणत्याही पासवर्डशिवाय आपल्या साईटचे नाव निवडून थेट रिअल-टाइम प्रोग्रेस, हजेरी व बिलाचा हिशोब पाहू शकतात.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT site_name FROM site_milestone_payments UNION SELECT DISTINCT site_name FROM site_progress")
        available_sites = [r["site_name"] for r in cursor.fetchall() if r["site_name"]]
        conn.close()

        with st.form("client_read_only_form"):
            if available_sites:
                c_site_select = st.selectbox("तुमच्या साईटचे नाव निवडा:", available_sites)
            else:
                c_site_select = st.text_input("तुमच्या साईटचे नाव टाका (उदा. पाटील रेसिडेन्सी):")
            
            c_verify_contact = st.text_input("तुमचा ईमेल किंवा फोन (नोंदणीसाठी / पडताळणी):").strip()
            submit_client_view = st.form_submit_button("🔍 साईट प्रोग्रेस व बिल पाहा (View Live Status)", type="primary")

            if submit_client_view:
                if c_site_select:
                    st.session_state.is_client_view = True
                    st.session_state.client_view_site = c_site_select
                    st.session_state.client_view_contact = c_verify_contact
                    st.rerun()
                else:
                    st.warning("⚠️ कृपया साईटचे नाव टाका किंवा निवडा!")

    st.write("---")

    # १२.४ ॲडमीन लॉगिन एक्सपँडर
    with st.expander("🛡️ Admin Login Panel"):
        with st.form("admin_login_form"):
            admin_id = st.text_input("Admin ID:")
            admin_pass = st.text_input("Password:", type="password")
            submit_admin = st.form_submit_button("🔓 Login to Admin Panel", type="primary")

            secret_admin_id = (
                st.secrets.get("ADMIN_ID", "kanha_1p")
                if hasattr(st, "secrets") and "ADMIN_ID" in st.secrets
                else "kanha_1p"
            )
            secret_admin_pass = (
                st.secrets.get("ADMIN_PASS", "@Dellg15")
                if hasattr(st, "secrets") and "ADMIN_PASS" in st.secrets
                else "@Dellg15"
            )

            if submit_admin:
                if admin_id == secret_admin_id and admin_pass == secret_admin_pass:
                    st.session_state.is_admin_logged = True
                    st.rerun()
                else:
                    st.error("❌ चुकीचा Admin ID किंवा Password!")

    st.stop()


# ==========================================================
# 📌 विभाग १२.५: CLIENT LIVE READ-ONLY DASHBOARD RENDERER
# ==========================================================
if st.session_state.get("is_client_view", False):
    c_site = st.session_state.get("client_view_site", "Default Site")
    
    col_c_top, col_c_exit = st.columns([3.5, 1.5])
    with col_c_top:
        st.markdown(f"<span class='free-user-badge' style='color:#10b981; border-color:#10b981;'>👁️ CLIENT LIVE PORTAL (READ-ONLY)</span>", unsafe_allow_html=True)
    with col_c_exit:
        if st.button("🚪 पोर्टल बंद करा (Exit View)", type="primary"):
            st.session_state.is_client_view = False
            st.session_state.client_view_site = None
            st.rerun()

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); border-left: 5px solid #10b981; padding: 16px 20px; border-radius: 14px; margin: 15px 0 20px 0; border: 1px solid #10b981;">
            <span style="color:#94a3b8; font-size:12px; font-weight:bold;">📍 चालू प्रोजेक्ट / साईट:</span><br>
            <h2 style="color:#10b981; margin: 4px 0 0 0;">🏗️ {c_site}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    # १. पेमेंट व बिल डेटा
    cursor.execute("SELECT * FROM site_milestone_payments WHERE site_name = ? ORDER BY id ASC", (c_site,))
    c_milestones = [dict(r) for r in cursor.fetchall()]

    # २. प्रोग्रेस डेटा
    cursor.execute("SELECT * FROM site_progress WHERE site_name = ? ORDER BY id DESC LIMIT 5", (c_site,))
    c_progress = [dict(r) for r in cursor.fetchall()]
    conn.close()

    c_tot_budget = sum(m["planned_amount"] for m in c_milestones)
    c_tot_paid = sum(m["amount_deposited"] for m in c_milestones)
    c_tot_pending = max(0.0, c_tot_budget - c_tot_paid)
    c_locked_count = sum(1 for m in c_milestones if m.get("is_locked") == 1)
    c_pct = (c_tot_paid / c_tot_budget * 100) if c_tot_budget > 0 else 0.0

    st.markdown("### 💰 बिलाचा व पेमेंटचा तपशील (Billing & Payment Summary)")
    cb1, cb2, cb3, cb4 = st.columns(4)
    cb1.metric("एकूण ठरलेले बिल", f"₹ {c_tot_budget:,.2f}")
    cb2.metric("तुम्ही भरलेली रक्कम", f"₹ {c_tot_paid:,.2f}")
    cb3.metric("शिल्लक बाकी रक्कम", f"₹ {c_tot_pending:,.2f}")
    cb4.metric("एकूण प्रगती (%)", f"{c_pct:.1f}% ({c_locked_count}/{len(c_milestones)} टप्पे)")

    st.write("---")
    st.markdown("#### 📋 टप्प्याटप्प्याने बिलाचा तपशील (Milestones Breakdown)")
    if c_milestones:
        m_table_rows = ""
        for idx, m in enumerate(c_milestones, 1):
            p = float(m["planned_amount"])
            d = float(m["amount_deposited"])
            bal = max(0.0, p - d)
            st_text = "✅ 100% Paid & Locked" if m.get("is_locked") == 1 else ("🟡 Partially Paid" if d > 0 else "🔴 Unpaid")
            m_table_rows += f"| {idx} | **{m['stage_name']}** | ₹ {p:,.2f} | ₹ {d:,.2f} | ₹ {bal:,.2f} | {st_text} |\n"

        st.markdown(
            f"""
| # | कामाचा टप्पा | ठरलेले बिल | जमा रक्कम | शिल्लक बाकी | सद्यस्थिती |
| :--- | :--- | :--- | :--- | :--- | :--- |
{m_table_rows}
            """
        )
    else:
        st.info("ℹ️ या साईटवर अजून बिलाचे टप्पे ठरवलेले नाहीत.")

    st.write("---")
    st.markdown("#### 📸 साईटवरील कामाची सद्यस्थिती (Latest Progress Updates)")
    if c_progress:
        for p in c_progress:
            st.markdown(f"**📅 तारीख:** `{p['date']}` | **🚧 टप्पा:** {p['stage_name']} | **प्रगती:** `{p['progress_percent']}%`")
            st.progress(int(p['progress_percent']))
            if p.get("remark"):
                st.caption(f"📝 **इंजिनिअर शेरा:** {p['remark']}")
            st.write("---")
    else:
        st.info("ℹ️ सध्या कोणताही नवीन प्रोग्रेस रिपोर्ट उपलब्ध नाही.")

    st.stop()
                    
# ==============================================================================
# 📌 विभाग १३: GEMINI-STYLE LEFT SIDEBAR (Site, Weather, Notice & Controls)
# ==============================================================================
current_user_name = st.session_state.app_user_name
is_user_premium, status_text_str = check_user_premium_status(current_user_name)

# १. हवामान डेटा (Open-Meteo API)
if "site_location_city" not in st.session_state:
    st.session_state.site_location_city = "Pune"

site_weather = get_site_weather_forecast(st.session_state.site_location_city)
w_temp = site_weather["temp"] if site_weather else "--"
w_rain = site_weather["rain_prob"] if site_weather else 0
w_city = (
    site_weather["city"] if site_weather else st.session_state.site_location_city
)

current_user_data = get_user_data(current_user_name) or {}
disp_name_inbox = current_user_name if current_user_name else ""

# ------------------------------------------------------------------------------
# 🌟 डाव्या बाजूचा GEMINI STYLE SIDEBAR
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px 0 15px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px;">
            <span style="font-size: 26px;">🏗️</span>
            <h3 style="margin: 4px 0 0 0; font-size: 18px; font-weight: 800; color: #f59e0b;">PATIL INFRATECH</h3>
            <small style="color: #94a3b8; font-size: 11px;">Site Control Panel</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # १. चालू साईट बॉक्स
    st.markdown(
        f"""
        <div style="background: #141820; border: 1px solid #2d3545; border-left: 4px solid #38bdf8; padding: 10px 12px; border-radius: 10px; margin-bottom: 8px;">
            <span style="font-size: 11px; color: #94a3b8; font-weight: 600;">📍 चालू साईट:</span><br>
            <b style="color: #ffffff; font-size: 14px;">🏗️ {st.session_state.current_site_name}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.popover("✏️ साईट नाव बदला", use_container_width=True):
        new_site_input = st.text_input(
            "नवीन साईटचे नाव टाका:",
            value=st.session_state.current_site_name,
            key="side_site_edit_input",
        )
        if st.button("💾 सेव्ह करा", key="btn_save_side_site", type="primary", use_container_width=True):
            if new_site_input.strip():
                st.session_state.current_site_name = new_site_input.strip()
                st.rerun()

    st.write("")

    # २. हवामान बॉक्स
    st.markdown(
        f"""
        <div style="background: #141820; border: 1px solid #2d3545; padding: 10px 12px; border-radius: 10px; text-align: center; margin-bottom: 8px;">
            <span style="font-size: 11px; color: #94a3b8;">🌤️ हवामान ({w_city})</span><br>
            <b style="color: #38bdf8; font-size: 15px;">{w_temp}°C</b> | <span style="color: {'#ef4444' if w_rain >= 50 else '#10b981'}; font-weight: bold; font-size: 13px;">🌧️ {w_rain}% पाऊस</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ३. शहर बदलणे
    with st.popover("📍 Set City Location", use_container_width=True):
        new_city_input = st.text_input(
            "शहर टाका (उदा. Pune):",
            value=st.session_state.site_location_city,
            key="side_city_edit_input",
        )
        if st.button("🌦️ अपडेट करा", key="btn_side_weather_update", type="primary", use_container_width=True):
            if new_city_input.strip():
                st.session_state.site_location_city = new_city_input.strip()
                st.rerun()

    # ४. लॉगआउट बटण
    if st.button("🔄 Logout", key="side_logout_btn", use_container_width=True):
        st.session_state.app_user_name = None
        st.session_state.otp_verified = False
        if "saved_user" in st.query_params:
            del st.query_params["saved_user"]
        st.session_state.current_comment = "काही नाही"
        st.session_state.selected_module = None
        st.session_state.selected_site_sub_module = None
        st.session_state.selected_estimator_sub_module = None

        st.markdown(
            """
            <script>
                localStorage.removeItem("patil_app_user");
            </script>
            """,
            unsafe_allow_html=True,
        )
        st.rerun()

    st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)

    # ५. नोटीस बॉक्स
    if current_user_data.get("unread_notification") == 1:
        admin_msg = current_user_data.get("admin_message", "")
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #10b981;">
                <h6 style="color: #34d399; margin: 0 0 4px 0;">🔔 नवीन ॲडमीन नोटीस</h6>
                <p style="color: #ffffff; font-size: 12px; margin: 0;">{admin_msg}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("✅ Mark as Read", type="primary", key="btn_read_notice_side", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET unread_notification = 0, admin_message = ? WHERE user_key = ?",
                (
                    f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳",
                    current_user_name,
                ),
            )
            conn.commit()
            conn.close()
            st.rerun()
    else:
        admin_msg = current_user_data.get(
            "admin_message",
            f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳",
        )
        with st.expander("📥 नोटीस व मेसेज इनबॉक्स"):
            st.info(f"📢 {admin_msg}")

    # ६. प्रिमियम अनलॉक बॉक्स
    if not is_user_premium:
        with st.expander("🔑 प्रिमियम अनलॉक करा"):
            input_code = st.text_input("Enter Code:", key="side_code_input").strip()
            
            if st.button("🔓 Unlock", key="btn_activate_prem_side", type="primary", use_container_width=True):
                u_info = get_user_data(current_user_name) or {}

                if input_code == "4528":
                    uses_count = u_info.get("master_code_uses", 0)
                    if uses_count >= 3:
                        st.error("❌ मर्यादा संपली आहे (Max 3).")
                    else:
                        exp_datetime = get_ist_time() + datetime.timedelta(hours=8)
                        exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")

                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            UPDATE users 
                            SET master_code_uses = ?, is_premium = 1, premium_expiry = ?, seen_popup = 0,
                                activated_by = ?, admin_message = ?, unread_notification = 0
                            WHERE user_key = ?
                            """,
                            (
                                uses_count + 1,
                                exp_str,
                                "Master Code 4528 (8 Hours VIP)",
                                f"🎉 ८ तासांचे प्रिमियम मिळाले आहे! ({uses_count + 1}/3)",
                                current_user_name,
                            ),
                        )
                        conn.commit()
                        conn.close()
                        st.success("🎉 प्रिमियम अनलॉक झाले!")
                        st.rerun()

                elif input_code == "kanha_1p":
                    exp_datetime = get_ist_time() + datetime.timedelta(days=1)
                    exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE users 
                        SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?,
                            admin_message = ?, unread_notification = 0
                        WHERE user_key = ?
                        """,
                        (
                            exp_str,
                            "Master Code",
                            f"{current_user_name} स्वागत आहे🥳",
                            current_user_name,
                        ),
                    )
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
                        exp_datetime = get_ist_time() + datetime.timedelta(days=28)
                        exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

                        cursor.execute(
                            "UPDATE premium_codes SET used = 1, used_by = ?, used_date = ? WHERE code = ?",
                            (current_user_name, now_str, input_code),
                        )
                        cursor.execute(
                            """
                            UPDATE users 
                            SET is_premium = 1, premium_expiry = ?, seen_popup = 0, activated_by = ?,
                                admin_message = ?, unread_notification = 0
                            WHERE user_key = ?
                            """,
                            (
                                exp_str,
                                "Patil Infratech",
                                f"{current_user_name} स्वागत आहे🥳",
                                current_user_name,
                            ),
                        )
                        conn.commit()
                        conn.close()
                        st.success("🎉 प्रिमियम सुरू झाले!")
                        st.rerun()
                    else:
                        conn.close()
                        st.error("❌ चुकीचा किंवा वापरलेला कोड!")

            if st.button("📩 Request Code", key="btn_req_code_side", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET requested_code = 1 WHERE user_key = ?",
                    (current_user_name,),
                )
                conn.commit()
                conn.close()
                st.success("✅ रिक्वेस्ट पाठवली!")
# ==========================================
# 📌 विभाग १४: CIVIL AI ASSISTANT (Gemini SDK & Fallback)
# ==========================================
locks_cfg = get_feature_locks()
ai_lock_setting = locks_cfg.get("Civil AI Assistant", "Premium")

if ai_lock_setting == "Free" or is_user_premium:
    with st.expander("🤖 Patil Infratech Civil AI Assistant (Ask Anything)"):
        user_ai_query = st.text_input(
            "तुमचा प्रश्न किंवा शंका इथे लिहा:",
            placeholder="उदा. What is the dry volume factor for concrete...",
            key="civil_ai_input",
        )
        if st.button("🚀 Ask Civil AI", type="primary"):
            if user_ai_query.strip():
                api_key = (
                    st.secrets.get("GEMINI_API_KEY") 
                    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets 
                    else os.getenv("GEMINI_API_KEY", "")
                )
                
                ai_response_text = ""
                
                if HAS_GENAI and api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = (
                            "You are a Senior Civil Engineer for Patil Infratech. "
                            "Provide a direct, professional, and precise engineering answer: "
                            f"{user_ai_query}"
                        )
                        response = client.models.generate_content(
                            model="gemini-1.5-flash", 
                            contents=prompt
                        )
                        if response and response.text:
                            ai_response_text = response.text
                    except Exception:
                        ai_response_text = ""
                
                # जर एआय किंवा एपीआय की उपलब्ध नसेल, तर स्मार्ट इंजिनिअरिंग उत्तर देणे
                if not ai_response_text:
                    q_lower = user_ai_query.lower()
                    if "cement bag" in q_lower or "volume" in q_lower:
                        ai_response_text = (
                            "👷‍♂️ **Patil Infratech Expert Answer:**\n"
                            "• Weight of 1 cement bag = **50 kg**\n"
                            "• Density of cement = **1440 kg/m³**\n"
                            "• Volume in m³ = **0.0347 m³**\n"
                            "• Volume in Cubic Feet (CFT) = **1.225 CFT**"
                        )
                    elif "concrete" in q_lower or "dry volume" in q_lower:
                        ai_response_text = (
                            "👷‍♂️ **Patil Infratech Expert Answer:**\n"
                            "• Wet volume of concrete is multiplied by a **Dry Volume Factor of 1.54** "
                            "to calculate the required quantities of dry materials (Cement, Sand, and Aggregate)."
                        )
                    else:
                        ai_response_text = (
                            f"👷‍♂️ **Patil Infratech Expert Engineer Analysis:** Regarding your query *'{user_ai_query}'*, "
                            "please check IS-456 standards or use our built-in Rate Analysis and BBS modules for exact calculations."
                        )

                st.markdown(
                    f"""
                    <div style="background: #111827; border-left: 5px solid #00f2fe; padding: 18px; border-radius: 14px; margin-top: 12px; box-shadow: 0 4px 20px rgba(0, 242, 254, 0.2); color: #f8fafc;">
                        <b>🎯 Civil AI Answer:</b><br><br>{ai_response_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("⚠️ कृपया आधी तुमचा प्रश्न किंवा शंका इथे लिहा!")
else:
    st.info("🔒 Civil AI Assistant हे प्रिमियम फिचर आहे.")

# ==========================================
# 📌 विभाग १५: मुख्य मॉड्यूल निवड कार्ड्स (Site Manager vs Estimator Tools vs NeevPay)
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("<h3 style='text-align:center; margin-bottom:20px;'>🚀 कृपया मॉड्यूल निवडा</h3>", unsafe_allow_html=True)

    calc_lock = locks_cfg.get("Civil Calculator", "Free")
    site_lock = locks_cfg.get("Site Manager", "Free")
    neev_lock = locks_cfg.get("NeevPay", "Free")

    main_col1, main_col2, main_col3 = st.columns(3)

    # १. साईट मॅनेजर कार्ड
    with main_col1:
        site_badge = "🆓 Free Access" if site_lock == "Free" else "👑 VIP Premium"
        st.markdown(
            f"""
            <div class="module-card">
                <div style="font-size: 40px; margin-bottom: 8px;">👷‍♂️</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 20px;">Site Manager</h3>
                <p style="color: #94a3b8; font-size: 12px; margin: 6px 0 12px 0;">हजेरी, मजुरी, साहित्य ट्रॅकर व दैनिक प्रोग्रेस रिपोर्ट</p>
                <span style="font-size: 11px; font-weight: bold; color: {'#38bdf8' if site_lock == 'Free' else '#f59e0b'}; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 12px;">[{site_badge}]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("👷‍♂️ Open Site Manager", key="btn_open_site", use_container_width=True, type="primary"):
            if site_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
            else:
                st.session_state.selected_module = "Site Manager"
                st.session_state.selected_site_sub_module = None
                trigger_push_state()
                st.rerun()

    # २. एस्टिमेटर टूल्स कार्ड
    with main_col2:
        st.markdown(
            """
            <div class="module-card">
                <div style="font-size: 40px; margin-bottom: 8px;">📐</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 20px;">Estimator Tools</h3>
                <p style="color: #94a3b8; font-size: 12px; margin: 6px 0 12px 0;">Rate Analysis, BBS Schedule, QS & 3-in-1 Master PDF</p>
                <span style="font-size: 11px; font-weight: bold; color: #f59e0b; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 12px;">[5 Advanced Tools]</span>
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

    # ३. NeevPay पेमेंट प्रोटेक्शन कार्ड
    with main_col3:
        neev_badge = "🆓 Free Access" if neev_lock == "Free" else "👑 VIP Premium"
        st.markdown(
            f"""
            <div class="module-card" style="border: 1px solid #10b981; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.25);">
                <div style="font-size: 40px; margin-bottom: 8px;">🤝</div>
                <h3 style="margin: 0; color: #10b981; font-weight: 800; font-size: 20px;">NeevPay Escrow</h3>
                <p style="color: #94a3b8; font-size: 12px; margin: 6px 0 12px 0;">टप्प्याटप्प्याने पेमेंट, एस्क्रो वॉलेट व डिजिटल संमती</p>
                <span style="font-size: 11px; font-weight: bold; color: {'#10b981' if neev_lock == 'Free' else '#f59e0b'}; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 12px;">[{neev_badge}]</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("🤝 Open NeevPay Escrow", key="btn_open_neevpay", use_container_width=True, type="primary"):
            if neev_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
            else:
                st.session_state.selected_module = "NeevPay"
                trigger_push_state()
                st.rerun()

# ==========================================
# 📌 विभाग १६: ESTIMATOR TOOLS मुख्य मॉड्यूल (Sub-modules)
# ==========================================
elif st.session_state.selected_module == "Estimator Tools":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_estimator"):
        st.session_state.selected_module = None
        st.session_state.selected_estimator_sub_module = None
        st.rerun()

    st.write("---")
    st.subheader("📐 Estimator Tools Dashboard")

    calc_lock = locks_cfg.get("Civil Calculator", "Free")
    ra_lock = locks_cfg.get("Rate Analysis", "Free")
    bbs_lock = locks_cfg.get("BBS", "Free")
    qs_lock = locks_cfg.get("Quantity Surveying", "Free")

    # १६.० मास्टर ३-इन-१ कंबाइन्ड PDF व Excel रिपोर्ट फंक्शन
    def render_combined_master_report(user_key, site_name):
        st.subheader(f"📑 Master Project Estimate: {site_name}")
        st.caption("💡 मागील २ दिवसांमधील Rate Analysis, BBS आणि Quantity Survey चा एकत्रित IS-Code फॉरमॅट ३-पेज रिपोर्ट.")

        conn = get_db_connection()
        cursor = conn.cursor()

        two_days_ago = (get_ist_time() - datetime.timedelta(days=2)).strftime("%Y-%m-%d 00:00:00")
        cursor.execute(
            """
            SELECT timestamp, user_note, report_data FROM history 
            WHERE user_key = ? AND (site_name = ? OR site_name IS NULL) AND timestamp >= ?
            ORDER BY id ASC
            """,
            (user_key, site_name, two_days_ago),
        )

        records = cursor.fetchall()
        conn.close()

        if not records:
            st.warning(f"⚠️ '{site_name}' साठी मागील २ दिवसांत कोणतेही कॅल्क्युलेशन सेव्ह केलेले नाही. कृपया आधी टूल्स वापरून रिपोर्ट तयार करा.")
            return

        def markdown_to_html_table(md_text):
            lines = [line.strip() for line in md_text.strip().split("\n") if line.strip().startswith("|")]
            if not lines:
                return f"<div style='padding:8px; background:rgba(248, 250, 252, 0.85);'>{md_text}</div>"
            
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
            <title>PATIL INFRATECH - {site_name} Master Report</title>
            <style>
                @page {{ size: A4 portrait; margin: 8mm; }}
                @media print {{
                    body {{ background: #ffffff !important; color: #000000 !important; }}
                    .no-print {{ display: none !important; }}
                    .page-break {{ page-break-before: always !important; break-before: page !important; }}
                }}
                body {{ background-color: #e2e8f0; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 10px; color: #0f172a; }}
                .a4-page {{ position: relative; background: #ffffff; width: 100%; max-width: 780px; margin: 0 auto 20px auto; padding: 25px 30px; border-radius: 6px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 1.5px solid #0f172a; box-sizing: border-box; min-height: 1020px; overflow: hidden; }}
                .watermark {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-28deg); font-size: 22px; font-weight: 900; color: rgba(15, 23, 42, 0.09); text-transform: uppercase; letter-spacing: 2.5px; text-align: center; width: 78%; max-width: 500px; line-height: 1.5; pointer-events: none; user-select: none; border: 3px dashed rgba(15, 23, 42, 0.09); padding: 15px 25px; border-radius: 12px; z-index: 999; }}
                .content-box {{ position: relative; z-index: 2; }}
                .header-title {{ text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 6px; margin-bottom: 12px; }}
                .header-title h1 {{ margin: 0; font-size: 22px; color: #0f172a; font-weight: 900; letter-spacing: 0.5px; }}
                .header-title p {{ margin: 2px 0; font-size: 11px; font-weight: bold; color: #475569; }}
                table.info-table {{ width: 100%; margin-bottom: 12px; font-size: 12px; border-collapse: collapse; }}
                table.info-table td {{ padding: 3px 0; }}
                .section-header {{ background: #0f172a; color: #ffffff; padding: 6px 12px; font-size: 12px; font-weight: bold; border-radius: 4px; margin: 12px 0 8px 0; }}
                table.custom-data-table {{ width: 100%; border-collapse: collapse; margin: 8px 0 15px 0; font-size: 11px; }}
                table.custom-data-table th, table.custom-data-table td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
                table.custom-data-table th {{ background-color: rgba(241, 245, 249, 0.85); font-weight: bold; color: #0f172a; }}
                table.custom-data-table tr:nth-child(even) {{ background-color: rgba(248, 250, 252, 0.6); }}
                .signature-box {{ margin-top: 35px; width: 100%; font-size: 12px; }}
                .footer-stamp {{ text-align: center; margin-top: 20px; font-size: 10px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 5px; }}
            </style>
        </head>
        <body>
        """

        for idx, r in enumerate(records, 1):
            page_break_class = "page-break" if idx > 1 else ""
            sec_title = "Rate Analysis" if idx == 1 else ("Bar Bending Schedule (BBS)" if idx == 2 else "Quantity Survey")
            table_content_html = markdown_to_html_table(r['report_data'])

            full_html_doc += f"""
            <div class="a4-page {page_break_class}">
                <div class="watermark">KANHAIYA<br>FOUNDER OF PATIL INFRATECH</div>
                <div class="content-box">
                    <div class="header-title">
                        <h1>PATIL INFRATECH</h1>
                        <p>CIVIL ENGINEERS • CONSULTANTS • QUANTITY SURVEYORS</p>
                        <small style="color: #64748b;">(Compliant with IS 1200 & IS 2502 Standards)</small>
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
                    </table>
                    <hr style="border: 0.5px solid #cbd5e1; margin-bottom: 8px;">

                    <div class="section-header">
                        विभाग #{idx}: {sec_title} (नोंद वेळ: {r['timestamp']})
                    </div>

                    {table_content_html}

                    <table class="signature-box">
                        <tr>
                            <td style="width: 50%;">
                                <br><br>
                                __________________________<br>
                                <b>Site Engineer Signature</b>
                            </td>
                            <td style="width: 50%; text-align: right;">
                                <br><br>
                                __________________________<br>
                                <b>Authorized Checker</b>
                            </td>
                        </tr>
                    </table>

                    <div class="footer-stamp">
                        Certified & Generated by: <b>Kanhaiya (Founder of Patil Infratech)</b>
                    </div>
                </div>
            </div>
            """

        full_html_doc += """
        </body>
        </html>
        """

        st.components.v1.html(full_html_doc, height=520, scrolling=True)

        excel_data_list = []
        for r in records:
            excel_data_list.append({
                "Site Name": site_name,
                "User": user_key,
                "Timestamp": r["timestamp"],
                "Report Details": r["report_data"].replace("|", " ").strip()
            })
        excel_df = pd.DataFrame(excel_data_list)
        csv_bytes = excel_df.to_csv(index=False).encode('utf-8-sig')

        st.write("---")
        c1, c2, c3 = st.columns(3)

        with c1:
            st.download_button(
                label="📥 Download Master Report",
                data=full_html_doc,
                file_name=f"Patil_Infratech_{site_name.replace(' ', '_')}_Report.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )

        with c2:
            st.download_button(
                label="📊 Export Excel Data (.csv)",
                data=csv_bytes,
                file_name=f"Patil_Infratech_{site_name.replace(' ', '_')}_Estimate.csv",
                mime="text/csv",
                use_container_width=True
            )

        with c3:
            st.markdown(
                """
                <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 10px 14px; border-radius: 8px; font-weight: bold; cursor: pointer; height: 38px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                    🖨️ Instant Print (A4)
                </button>
                """,
                unsafe_allow_html=True,
            )

        wa_text = (
            f"🏗️ *PATIL INFRATECH - MASTER ESTIMATE REPORT*\n📍 *Site:* {site_name}\n"
            f"👤 *Engineer:* {user_key}\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
            f"✅ 3-in-1 Estimation Report Generated.\n_Certified by: Kanhaiya (Founder)_"
        )
        st.write(" ")
        render_whatsapp_feature(urllib.parse.quote(wa_text), "master_pdf_wa")

    if st.session_state.selected_estimator_sub_module is None:
        st.markdown("##### 🔽 खालीलपैकी एक Estimator टूल निवडा:")

        e_col1, e_col2 = st.columns(2)
        with e_col1:
            calc_badge = "🆓 Free" if calc_lock == "Free" else "👑 Premium"
            st.markdown(
                f"""
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">🧮</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Civil Calculator</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[{calc_badge}]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🧮 Calculator", key="btn_est_calc", use_container_width=True):
                if calc_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Calculator"
                    trigger_push_state()
                    st.rerun()

        with e_col2:
            ra_badge = "🆓 Free" if ra_lock == "Free" else "👑 Premium"
            st.markdown(
                f"""
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">📊</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Rate Analysis</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[{ra_badge}]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("📊 Rate Analysis", key="btn_est_ra", use_container_width=True):
                if ra_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Rate Analysis"
                    trigger_push_state()
                    st.rerun()

        st.write(" ")
        e_col3, e_col4 = st.columns(2)
        with e_col3:
            bbs_badge = "🆓 Free" if bbs_lock == "Free" else "👑 Premium"
            st.markdown(
                f"""
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">🏗️</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">BBS Calculator</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[{bbs_badge}]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🏗️ Open BBS", key="btn_est_bbs", use_container_width=True):
                if bbs_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "BBS"
                    trigger_push_state()
                    st.rerun()

        with e_col4:
            qs_badge = "🆓 Free" if qs_lock == "Free" else "👑 Premium"
            st.markdown(
                f"""
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">📈</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Quantity Surveying</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[{qs_badge}]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("📈 Quantity Survey", key="btn_est_qs", use_container_width=True):
                if qs_lock == "Premium" and not is_user_premium:
                    st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
                else:
                    st.session_state.selected_estimator_sub_module = "Quantity Surveying"
                    trigger_push_state()
                    st.rerun()

        st.write(" ")
        st.markdown(
            """
            <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid #f59e0b;">
                <h1 style="font-size: 32px; margin:0;">📑</h1>
                <h5 style="margin: 8px 0 2px 0; color: #f59e0b; font-weight:800; font-size:14px;">3-in-1 Master Estimate PDF</h5>
                <p style="font-size: 10px; color: #cbd5e1; margin:0;">[Rate Analysis + BBS + QS कंबाइन्ड रिपोर्ट]</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(" ")
        if st.button("📑 Open 3-in-1 Master PDF Generator", key="btn_est_master_pdf", use_container_width=True, type="primary"):
            st.session_state.selected_estimator_sub_module = "Master PDF"
            trigger_push_state()
            st.rerun()

    else:
        if st.button("⬅️ Back to Estimator Menu", key="btn_back_estimator_menu"):
            st.session_state.selected_estimator_sub_module = None
            st.rerun()

        st.write("---")
        est_sub_mod = st.session_state.selected_estimator_sub_module

        # १६.० Master 3-in-1 Combined Estimate PDF
        if est_sub_mod == "Master PDF":
            render_combined_master_report(current_user_name, st.session_state.current_site_name)

        # १६.१ Civil Calculator & Smart Unit Converter
        elif est_sub_mod == "Calculator":
            st.subheader("🧮 Civil Smart Unit Converter")
            st.caption("💡 एकाच बॉक्समध्ये मूल्य भरा आणि सर्व युनिट्समधील अचूक हिशोब एकाच झटक्यात मिळवा!")

            conv_category = st.selectbox("कनव्हर्शन प्रकार निवडा:", [
                "📦 Volume / Brass Converter (घनफळ आणि ब्रास)",
                "📏 Length Converter (लांबी मोजमाप)",
                "📐 Area Converter (क्षेत्रफळ मोजमाप)",
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
                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 20px; border-radius: 18px; border-left: 5px solid #00f2fe; box-shadow: 0 6px 20px rgba(0,242,254,0.15);">
                            <p style="margin: 6px 0; font-size: 16px;"><b>📦 एकूण ब्रास (Brass):</b> <span style="color:#f59e0b; font-size:19px; font-weight:bold;">{brass:.4f} Brass</span></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>📐 घन फूट (Cubic Feet / CFT):</b> <code>{cft:.2f} CFT</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>📏 घन मीटर (Cubic Meter / m³):</b> <code>{m3:.4f} m³</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>💧 लिटर (Liters):</b> <code>{liters:.2f} Ltrs</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

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
                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 20px; border-radius: 18px; border-left: 5px solid #00f2fe; box-shadow: 0 6px 20px rgba(0,242,254,0.15);">
                            <p style="margin: 6px 0; font-size: 15px;"><b>📏 मीटर (Meters):</b> <span style="color:#f59e0b; font-weight:bold;">{meters:.4f} m</span></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>🦶 फूट (Feet):</b> <code>{feet:.4f} ft</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>📐 इंच (Inches):</b> <code>{inches:.2f} inches</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>🔍 मिलिमीटर (mm):</b> <code>{mm:.2f} mm</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>📍 सेंटीमीटर (cm):</b> <code>{cm:.2f} cm</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

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
                    st.markdown(
                        f"""
                        <div style="background: #111827; padding: 20px; border-radius: 18px; border-left: 5px solid #00f2fe; box-shadow: 0 6px 20px rgba(0,242,254,0.15);">
                            <p style="margin: 6px 0; font-size: 15px;"><b>📐 स्क्वेअर फूट (Sq. Ft.):</b> <span style="color:#f59e0b; font-weight:bold;">{sqft:.2f} sq.ft.</span></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>📏 स्क्वेअर मीटर (m²):</b> <code>{sqm:.2f} m²</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>🌾 गुंठा (Guntha):</b> <code>{guntha:.4f} Guntha</code></p>
                            <p style="margin: 6px 0; font-size: 15px;"><b>🌳 हेक्टर/एकर (Acre):</b> <code>{acre:.4f} Acre</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # १६.२ Rate Analysis Module (Concrete, Brickwork, Plaster)
        elif est_sub_mod == "Rate Analysis":
            master_rates = get_market_rates()
            st.markdown(
                f"<div style='background: #111827; padding: 14px; border-radius: 16px; text-align: center; font-size: 13px; font-weight: bold; color: #f8fafc; margin-bottom: 18px; border-left: 5px solid #00f2fe; border: 1px solid rgba(0,242,254,0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>📢 आजचे मार्केट दर 🏷️ cement: ₹{master_rates.get('cement', 400.0)}/bag | sand: ₹{master_rates.get('sand', 2500.0)}/m³ | aggregate: ₹{master_rates.get('aggregate', 2200.0)}/m³ | steel: ₹{master_rates.get('steel', 60.0)}/Kg | brick: ₹{master_rates.get('bricks', 8.0)}/nos</div>",
                unsafe_allow_html=True,
            )

            main_choice = st.radio("**काय काम करायचे ते निवडा :**", [
                "Concrete Work (काँक्रीट काम)",
                "Brickwork (वीटकाम)",
                "Plaster Work (प्लास्टर काम)",
            ])

            if "Concrete Work" in main_choice:
                st.subheader("🧱 Concrete Work Estimation")
                col1, col2 = st.columns(2)
                with col1:
                    grade = st.selectbox("काँक्रीट ग्रेड निवडा:", ["M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"])
                with col2:
                    component = st.selectbox("आरसीसी घटक (Component) निवडा:", ["Footing (0.8% Steel)", "Slab (1.0% Steel)", "Beam (2.0% Steel)", "Column (2.5% Steel)", "Plain Concrete (0% Steel)"])

                if "M10" in grade:
                    cement_ratio, sand_ratio, aggregate_ratio = 1, 3, 6
                elif "M15" in grade:
                    cement_ratio, sand_ratio, aggregate_ratio = 1, 2, 4
                elif "M20" in grade:
                    cement_ratio, sand_ratio, aggregate_ratio = 1, 1.5, 3
                else:
                    cement_ratio, sand_ratio, aggregate_ratio = 1, 1, 2

                if "Footing" in component:
                    steel_percentage = 0.8
                elif "Slab" in component:
                    steel_percentage = 1.0
                elif "Beam" in component:
                    steel_percentage = 2.0
                elif "Column" in component:
                    steel_percentage = 2.5
                else:
                    steel_percentage = 0.0

                st.markdown("#### [A] साहित्याची माहिती आणि दर")
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
                    st.markdown("### 📊 RATE ANALYSIS SHEET - CONCRETE WORK")
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

                    msg_text = f"🏗️ *PATIL INFRATECH - RATE ANALYSIS REPORT*\n👤 *Prepared For:* {current_user_name}\n🧱 *Work:* Concrete Work ({component.split(' ')[0]})\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n📋 *DETAILS:*\n• Cement: {c_bags} Bags @ ₹{cement_rate} = ₹{total_cement_cost:.2f}\n• Sand: {s_m3:.2f} m³ @ ₹{sand_rate} = ₹{total_sand_cost:.2f}\n• Aggregate: {a_m3:.2f} m³ @ ₹{aggregate_rate} = ₹{total_aggregate_cost:.2f}\n"
                    if steel_percentage > 0:
                        msg_text += f"• Steel: {steel_qty:.2f} Kg @ ₹{steel_rate} = ₹{total_steel_cost:.2f}\n"
                    msg_text += f"• Labour Total: ₹{lab_cost:.2f}\n--------------------------------\n💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n--------------------------------\n_Generated by Patil Infratech_"

                    encoded_msg = urllib.parse.quote(msg_text)

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        render_whatsapp_feature(encoded_msg, "ra_conc")
                    with btn_col2:
                        st.markdown(
                            """
                            <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                                📄 Print / Download A3 Size PDF
                            </button>
                            """,
                            unsafe_allow_html=True,
                        )

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, now_str, st.session_state.current_comment, report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

            elif "Brickwork" in main_choice:
                st.subheader("🧱 Brickwork Estimation")
                mortar_choice = st.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio) निवडा:", ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])

                if "1:3" in mortar_choice:
                    c_part, s_part = 1, 3
                elif "1:4" in mortar_choice:
                    c_part, s_part = 1, 4
                elif "1:5" in mortar_choice:
                    c_part, s_part = 1, 5
                else:
                    c_part, s_part = 1, 6

                st.markdown("#### [A] साहित्याची माहिती आणि दर")
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
                    st.markdown("### 📊 RATE ANALYSIS SHEET - BRICKWORK")
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

                    msg_text = f"🏗️ *PATIL INFRATECH - BRICKWORK REPORT*\n👤 *Prepared For:* {current_user_name}\n🧱 *Ratio:* {mortar_choice.split(' ')[0]} | *Vol:* {volume} m³\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n📋 *DETAILS:*\n• Bricks: {total_bricks} Nos = ₹{total_brick_cost:.2f}\n• Cement: {cement_bags} Bags = ₹{total_cement_cost:.2f}\n• Sand: {sand_m3:.2f} m³ = ₹{total_sand_cost:.2f}\n• Labour: ₹{lab_cost:.2f}\n--------------------------------\n💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n--------------------------------\n_Generated by Patil Infratech_"
                    encoded_msg = urllib.parse.quote(msg_text)

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        render_whatsapp_feature(encoded_msg, "ra_bw")
                    with btn_col2:
                        st.markdown(
                            """
                            <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                                📄 Print / Download A3 Size PDF
                            </button>
                            """,
                            unsafe_allow_html=True,
                        )

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, now_str, st.session_state.current_comment, report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

            else:  # Plaster Work
                st.subheader("🎨 Plaster Work Estimation")

                thickness_mm = st.number_input("प्लास्टरची जाडी (Thickness in mm):", min_value=5.0, max_value=50.0, value=12.0, step=1.0, key="pl_thick")
                plaster_mortar = st.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio):", ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])

                if "1:3" in plaster_mortar:
                    p_c_part, p_s_part = 1, 3
                elif "1:4" in plaster_mortar:
                    p_c_part, p_s_part = 1, 4
                elif "1:5" in plaster_mortar:
                    p_c_part, p_s_part = 1, 5
                else:
                    p_c_part, p_s_part = 1, 6

                st.markdown("#### [A] साहित्याची माहिती आणि दर")
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    plaster_area = st.number_input("प्लास्टरचे एकूण क्षेत्रफळ (Area in m²):", min_value=0.0, value=10.0, key="pl_area")
                    cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=float(master_rates.get("cement", 400.0)), key="pl_cem_r")
                    use_waterproofing = st.checkbox("💧 वॉटरप्रूफिंग कंपाउंड ॲड करा (Waterproofing Compound)", value=False)
                with p_col2:
                    sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=float(master_rates.get("sand", 2500.0)), key="pl_snd_r")
                    wp_rate = st.number_input("वाटरप्रूफिंग दर (प्रति किलोग्रॅम/लिटर ₹):", min_value=0.0, value=150.0, key="pl_wp_r") if use_waterproofing else 0.0

                st.markdown("#### [B] लेबर खर्च")
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
                    st.markdown("### 📊 RATE ANALYSIS SHEET - PLASTER WORK")
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

                    msg_text = f"🏗️ *PATIL INFRATECH - PLASTER REPORT*\n👤 *Prepared For:* {current_user_name}\n🎨 *Thickness:* {thickness_mm}mm | *Area:* {plaster_area} m²\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n📋 *DETAILS:*\n• Cement: {cement_bags} Bags = ₹{total_cement_cost:.2f}\n• Sand: {sand_m3:.2f} m³ = ₹{total_sand_cost:.2f}\n"
                    if use_waterproofing:
                        msg_text += f"• Waterproofing: {wp_qty_kg:.2f} Kg = ₹{total_wp_cost:.2f}\n"
                    msg_text += f"• Labour: ₹{lab_cost:.2f}\n--------------------------------\n💰 *GRAND TOTAL:* ₹{grand_total:.2f}/-\n--------------------------------\n_Generated by Patil Infratech_"

                    encoded_msg = urllib.parse.quote(msg_text)

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        render_whatsapp_feature(encoded_msg, "ra_pl")
                    with btn_col2:
                        st.markdown(
                            """
                            <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                                📄 Print / Download A3 Size PDF
                            </button>
                            """,
                            unsafe_allow_html=True,
                        )

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, now_str, st.session_state.current_comment, report_table, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

        # १६.३ Bar Bending Schedule (BBS Calculator)
        elif est_sub_mod == "BBS":
            st.subheader("🏗️ Bar Bending Schedule (BBS Calculator)")
            default_covers = {"Footing": 50, "Column": 40, "Beam": 25, "Slab": 20}

            def update_cover_from_component():
                selected_comp = st.session_state.get("bbs_rcc_component", "Footing")
                st.session_state["bbs_cover"] = default_covers.get(selected_comp, 25)

            if "bbs_cover" not in st.session_state:
                st.session_state["bbs_cover"] = 50

            rcc_comp = st.selectbox(
                "घटक (RCC Component) निवडा:",
                ["Footing", "Column", "Beam", "Slab"],
                key="bbs_rcc_component",
                on_change=update_cover_from_component,
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
            cover = st.number_input("Clear Cover (mm):", min_value=10, max_value=100, step=5, key="bbs_cover")
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
                    m_unit_wt = (f_main_dia**2) / 162.0
                    m_tot_wt = m_tot_len * m_unit_wt
                    calc_list.append({
                        "Desc": "Main Bars (Longitudinal)", "Nos": m_nos, "Dia": f_main_dia,
                        "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt,
                    })

                    d_leg = 200.0
                    d_cut_m = (b_net + (2 * d_leg) - (4 * f_dist_dia)) / 1000.0
                    d_nos = (math.ceil(length_mm / f_dist_spacing) + 1) * num_members
                    d_tot_len = d_cut_m * d_nos
                    d_unit_wt = (f_dist_dia**2) / 162.0
                    d_tot_wt = d_tot_len * d_unit_wt
                    calc_list.append({
                        "Desc": "Distribution Bars (Transverse)", "Nos": d_nos, "Dia": f_dist_dia,
                        "Len": d_cut_m, "TotLen": d_tot_len, "Wt": d_unit_wt, "TotWt": d_tot_wt,
                    })

                elif rcc_comp == "Column":
                    m_ld = 300.0
                    m_cut_m = (height_mm + m_ld) / 1000.0
                    m_nos = col_main_nos * num_members
                    m_tot_len = m_cut_m * m_nos
                    m_unit_wt = (col_main_dia**2) / 162.0
                    m_tot_wt = m_tot_len * m_unit_wt
                    calc_list.append({
                        "Desc": "Main Vertical Bars", "Nos": m_nos, "Dia": col_main_dia,
                        "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt,
                    })

                    hook_len = 10 * col_st_dia if "135°" in col_hook_angle else 6 * col_st_dia
                    st_cut_m = ((2 * (b_net + h_net)) + (2 * hook_len) - (3 * 2 * col_st_dia)) / 1000.0
                    st_nos = (math.ceil(height_mm / col_st_spacing) + 1) * num_members
                    st_tot_len = st_cut_m * st_nos
                    st_unit_wt = (col_st_dia**2) / 162.0
                    st_tot_wt = st_tot_len * st_unit_wt
                    calc_list.append({
                        "Desc": "Stirrups / Ties (Rings)", "Nos": st_nos, "Dia": col_st_dia,
                        "Len": st_cut_m, "TotLen": st_tot_len, "Wt": st_unit_wt, "TotWt": st_tot_wt,
                    })

                elif rcc_comp == "Beam":
                    t_ld = max(300.0, 30 * bm_top_dia)
                    t_cut_m = (l_net + (2 * t_ld) - (4 * bm_top_dia)) / 1000.0
                    t_nos = bm_top_nos * num_members
                    t_tot_len = t_cut_m * t_nos
                    t_unit_wt = (bm_top_dia**2) / 162.0
                    t_tot_wt = t_tot_len * t_unit_wt
                    calc_list.append({
                        "Desc": "Top Main Bars", "Nos": t_nos, "Dia": bm_top_dia,
                        "Len": t_cut_m, "TotLen": t_tot_len, "Wt": t_unit_wt, "TotWt": t_tot_wt,
                    })

                    b_ld = max(300.0, 30 * bm_bot_dia)
                    b_cut_m = (l_net + (2 * b_ld) - (4 * bm_bot_dia)) / 1000.0
                    b_nos = bm_bot_nos * num_members
                    b_tot_len = b_cut_m * b_nos
                    b_unit_wt = (bm_bot_dia**2) / 162.0
                    b_tot_wt = b_tot_len * b_unit_wt
                    calc_list.append({
                        "Desc": "Bottom Main Bars", "Nos": b_nos, "Dia": bm_bot_dia,
                        "Len": b_cut_m, "TotLen": b_tot_len, "Wt": b_unit_wt, "TotWt": b_tot_wt,
                    })

                    st_cut_m = ((2 * (b_net + h_net)) + (2 * 10 * bm_st_dia) - (3 * 2 * bm_st_dia)) / 1000.0
                    st_nos = (math.ceil(length_mm / bm_st_spacing) + 1) * num_members
                    st_tot_len = st_cut_m * st_nos
                    st_unit_wt = (bm_st_dia**2) / 162.0
                    st_tot_wt = st_tot_len * st_unit_wt
                    calc_list.append({
                        "Desc": "Stirrups / Rings", "Nos": st_nos, "Dia": bm_st_dia,
                        "Len": st_cut_m, "TotLen": st_tot_len, "Wt": st_unit_wt, "TotWt": st_tot_wt,
                    })

                else:  # Slab
                    m_hook = 10 * sl_main_dia
                    m_cut_m = (l_net + (2 * m_hook)) / 1000.0
                    m_nos = (math.ceil(width_mm / sl_main_spacing) + 1) * num_members
                    m_tot_len = m_cut_m * m_nos
                    m_unit_wt = (sl_main_dia**2) / 162.0
                    m_tot_wt = m_tot_len * m_unit_wt
                    calc_list.append({
                        "Desc": "Main Bars", "Nos": m_nos, "Dia": sl_main_dia,
                        "Len": m_cut_m, "TotLen": m_tot_len, "Wt": m_unit_wt, "TotWt": m_tot_wt,
                    })

                    d_hook = 10 * sl_dist_dia
                    d_cut_m = (b_net + (2 * d_hook)) / 1000.0
                    d_nos = (math.ceil(length_mm / sl_dist_spacing) + 1) * num_members
                    d_tot_len = d_cut_m * d_nos
                    d_unit_wt = (sl_dist_dia**2) / 162.0
                    d_tot_wt = d_tot_len * d_unit_wt
                    calc_list.append({
                        "Desc": "Distribution Bars", "Nos": d_nos, "Dia": sl_dist_dia,
                        "Len": d_cut_m, "TotLen": d_tot_len, "Wt": d_unit_wt, "TotWt": d_tot_wt,
                    })

                total_weight_kg = sum(item["TotWt"] for item in calc_list)
                total_cost = total_weight_kg * steel_rate_kg

                st.success("🎉 BBS रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
                st.markdown("### 🏗️ BAR BENDING SCHEDULE (BBS) REPORT")
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

                msg_text = f"🏗️ *PATIL INFRATECH - BAR BENDING SCHEDULE (BBS)*\n👤 *Prepared For:* {current_user_name}\n📐 *Component:* {rcc_comp}\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n📐 *Size:* {length_m:.2f}m x {width_m:.2f}m x {height_m:.2f}m\n\n📊 *DETAILED BAR SCHEDULE:*\n--------------------------------\n"
                for idx, item in enumerate(calc_list, 1):
                    msg_text += f"*{idx}. {item['Desc']}*\n  • Nos: {item['Nos']} | Dia: {item['Dia']}mm\n  • Cutting Len: {item['Len']:.3f} m\n  • Total Len: {item['TotLen']:.2f} m\n  • Total Weight: {item['TotWt']:.2f} Kg\n\n"
                msg_text += f"--------------------------------\n⚖️ *TOTAL STEEL WEIGHT:* {total_weight_kg:.2f} Kg ({total_weight_kg/1000:.3f} MT)\n💵 *Steel Rate:* ₹ {steel_rate_kg:.2f} / Kg\n💰 *ESTIMATED COST:* ₹ {total_cost:.2f}/-\n--------------------------------\n_Generated by Patil Infratech_"

                encoded_msg = urllib.parse.quote(msg_text)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    render_whatsapp_feature(encoded_msg, "bbs_main")
                with btn_col2:
                    st.markdown(
                        """
                        <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                            📄 Print / Save A3 Size PDF
                        </button>
                        """,
                        unsafe_allow_html=True,
                    )

                if current_user_name:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                        (current_user_name, now_str, st.session_state.current_comment, report_table, st.session_state.current_site_name),
                    )
                    conn.commit()
                    conn.close()

        # १६.४ Quantity Surveying & Abstract Sheet Master
        elif est_sub_mod == "Quantity Surveying":
            st.subheader("📈 Quantity Surveying & Abstract Sheet Master")
            st.caption("💡 नोटबुकच्या मोजमाप पद्धतीनुसार खालील टेबलमध्ये Description, Nos, Length, Width, Height भरा. हिशोब तयार करा!")

            with st.expander("📷 2D Plan / Blueprint / Camera Reference"):
                plan_option = st.radio("ब्लूप्रिंट इनपुट पद्धत निवडा:", ["Upload 2D Plan Image", "Capture via Camera (Live)"], horizontal=True)
                if "Upload" in plan_option:
                    uploaded_plan = st.file_uploader("Upload Blueprint (PNG/JPG):", type=["png", "jpg", "jpeg"])
                    if uploaded_plan:
                        st.image(uploaded_plan, caption="Uploaded 2D Floor Plan", use_column_width=True)
                else:
                    cam_pic = st.camera_input("📸 Capture 2D Plan from Camera")
                    if cam_pic:
                        st.image(cam_pic, caption="Captured Blueprint Reference", use_column_width=True)

            st.markdown("### 🏢 Construction Stages Measurement Sheet (Excavation to Finishing)")
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

                st.markdown(f"#### 🔹 {stg_name}")
                c_desc, c_nos, c_l, c_w, c_h = st.columns([2.5, 1, 1, 1, 1])
                with c_desc:
                    desc_val = st.text_input(f"Description #{idx}", value=stg_name, key=f"qs_desc_{idx}")
                with c_nos:
                    nos_val = st.number_input(f"Nos #{idx}", min_value=0, value=0, step=1, key=f"qs_nos_{idx}")
                with c_l:
                    l_val = st.number_input(f"Length #{idx}", min_value=0.0, value=0.0, step=0.1, key=f"qs_l_{idx}")
                with c_w:
                    w_val = st.number_input(f"Width #{idx}", min_value=0.0, value=0.0, step=0.1, key=f"qs_w_{idx}")
                with c_h:
                    if is_area_unit:
                        h_val = 1.0
                        st.caption("📏 (Area m²)")
                    else:
                        h_val = st.number_input(f"Height #{idx}", min_value=0.0, value=0.0, step=0.05, key=f"qs_h_{idx}")

                # Deductions Input Blocks
                bw_ded_vol = 0.0
                if is_brickwork:
                    st.markdown("##### 🚪 Brickwork Deductions (Doors / Windows in m³)")
                    ded_key_bw = f"bw_ded_count_{idx}"
                    if ded_key_bw not in st.session_state:
                        st.session_state[ded_key_bw] = 1

                    if st.button(f"➕ Add Brickwork Deduction Item #{idx}", key=f"btn_bw_ded_{idx}"):
                        st.session_state[ded_key_bw] += 1
                        st.rerun()

                    for d_i in range(st.session_state[ded_key_bw]):
                        dc1, dc2, dc3, dc4, dc5 = st.columns(5)
                        with dc1:
                            dt = st.selectbox("Type", ["Door", "Window"], key=f"bw_dt_{idx}_{d_i}")
                        with dc2:
                            dl = st.number_input("L (m)", min_value=0.0, value=0.0, step=0.1, key=f"bw_dl_{idx}_{d_i}")
                        with dc3:
                            db = st.number_input("Thickness", min_value=0.0, value=0.23, step=0.05, key=f"bw_db_{idx}_{d_i}")
                        with dc4:
                            dh = st.number_input("H (m)", min_value=0.0, value=0.0, step=0.1, key=f"bw_dh_{idx}_{d_i}")
                        with dc5:
                            dn = st.number_input("Nos", min_value=0, value=0, step=1, key=f"bw_dn_{idx}_{d_i}")

                        if dl > 0 and db > 0 and dh > 0 and dn > 0:
                            bw_ded_vol += dl * db * dh * dn

                    if bw_ded_vol > 0:
                        st.markdown(f"**🔴 Total Brickwork Deduction: `{bw_ded_vol:.3f} m³`**")

                pl_ded_area = 0.0
                if is_plaster:
                    st.markdown("##### 🚪 Plaster Deductions (Doors / Windows in m²)")
                    ded_key_pl = f"pl_ded_count_{idx}"
                    if ded_key_pl not in st.session_state:
                        st.session_state[ded_key_pl] = 1

                    if st.button(f"➕ Add Plaster Deduction Item #{idx}", key=f"btn_pl_ded_{idx}"):
                        st.session_state[ded_key_pl] += 1
                        st.rerun()

                    for d_i in range(st.session_state[ded_key_pl]):
                        dc1, dc2, dc3, dc4 = st.columns(4)
                        with dc1:
                            dt = st.selectbox("Type", ["Door", "Window"], key=f"pl_dt_{idx}_{d_i}")
                        with dc2:
                            dl = st.number_input("Length (m)", min_value=0.0, value=0.0, step=0.1, key=f"pl_dl_{idx}_{d_i}")
                        with dc3:
                            dh = st.number_input("Height (m)", min_value=0.0, value=0.0, step=0.1, key=f"pl_dh_{idx}_{d_i}")
                        with dc4:
                            dn = st.number_input("Nos", min_value=0, value=0, step=1, key=f"pl_dn_{idx}_{d_i}")

                        if dl > 0 and dh > 0 and dn > 0:
                            pl_ded_area += dl * dh * dn * 2

                    if pl_ded_area > 0:
                        st.markdown(f"**🔴 Total Plaster Deduction: `{pl_ded_area:.3f} m²`**")

                # Main Calculation & Net Deduction Logic
                if nos_val > 0 and l_val > 0 and w_val > 0 and (is_area_unit or h_val > 0):
                    if is_area_unit:
                        single_qty = l_val * w_val
                        total_qty = single_qty * nos_val
                        unit_label = "m²"
                    else:
                        single_qty = l_val * w_val * h_val
                        total_qty = single_qty * nos_val
                        unit_label = "m³"

                    if is_brickwork:
                        net_total_qty = max(0.0, total_qty - bw_ded_vol)
                    elif is_plaster:
                        net_total_qty = max(0.0, total_qty - pl_ded_area)
                    else:
                        net_total_qty = total_qty

                    st.markdown(f"**📐 Gross Qty: `{total_qty:.3f} {unit_label}` | Net Qty (वजावट करून): <span style='color:#10b981;'>`{net_total_qty:.3f} {unit_label}`</span>**", unsafe_allow_html=True)

                    mat_summary = "मटेरियल लागू नाही"
                    if "P.C.C." in stg_name:
                        dry_vol = net_total_qty * 1.54
                        c_bags = math.ceil((1 / 13) * dry_vol * 28.8)
                        sand_m3 = (4 / 13) * dry_vol
                        agg_m3 = (8 / 13) * dry_vol
                        mat_summary = f"Cement: {c_bags} Bags, Sand: {sand_m3:.2f} m³, Aggregate: {agg_m3:.2f} m³"
                        st.info(f"• **Cement:** {c_bags} Bags | **Sand:** {sand_m3:.2f} m³ | **Aggregate:** {agg_m3:.2f} m³")

                    elif "RCC" in stg_name or "Column" in stg_name or "Slab" in stg_name or "Footing" in stg_name:
                        dry_vol = net_total_qty * 1.54
                        c_bags = math.ceil((1 / 5.5) * dry_vol * 28.8)
                        sand_m3 = (1.5 / 5.5) * dry_vol
                        agg_m3 = (3 / 5.5) * dry_vol
                        steel_kg = net_total_qty * 80.0
                        mat_summary = f"Cement: {c_bags} Bags, Sand: {sand_m3:.2f} m³, Aggregate: {agg_m3:.2f} m³, Steel: {steel_kg:.1f} Kg"
                        st.info(f"• **Cement:** {c_bags} Bags | **Sand:** {sand_m3:.2f} m³ | **Aggregate:** {agg_m3:.2f} m³ | **Steel:** {steel_kg:.1f} Kg")

                    elif "Brickwork" in stg_name:
                        bricks = math.ceil(net_total_qty * 500)
                        mortar_vol = net_total_qty * 0.30
                        c_bags = math.ceil((1 / 5) * mortar_vol * 28.8)
                        sand_m3 = (4 / 5) * mortar_vol
                        mat_summary = f"Bricks: {bricks} Nos, Cement: {c_bags} Bags, Sand: {sand_m3:.2f} m³"
                        st.info(f"• **Bricks:** {bricks} Nos | **Cement:** {c_bags} Bags | **Sand:** {sand_m3:.2f} m³")

                    elif "Plaster" in stg_name:
                        thickness = 0.012
                        wet_vol = net_total_qty * thickness
                        dry_vol = wet_vol * 1.33
                        c_bags = math.ceil((1 / 5) * dry_vol * 28.8)
                        sand_m3 = (4 / 5) * dry_vol
                        mat_summary = f"Cement: {c_bags} Bags, Sand: {sand_m3:.2f} m³"
                        st.info(f"• **Cement (12mm):** {c_bags} Bags | **Sand:** {sand_m3:.2f} m³")

                    stage_results.append({
                        "Stage": desc_val,
                        "Dimensions": f"{l_val} x {w_val} x {h_val if not is_area_unit else 1.0}",
                        "Nos": nos_val,
                        "SingleQty": single_qty,
                        "TotalQty": f"{net_total_qty:.3f} {unit_label}",
                        "Material": mat_summary,
                    })

                st.write("---")

            st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
            user_note = st.text_area("Abstract Sheet संदर्भात विशेष नोंद:", placeholder="उदा. Ground floor estimation...", key="qs_note")
            if st.button("💬 कमेंट सबमिट करा", key="qs_comm_btn"):
                if user_note.strip():
                    st.session_state.current_comment = user_note.strip()
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET comment = ? WHERE user_key = ?", (user_note.strip(), current_user_name))
                    conn.commit()
                    conn.close()
                    st.success("✅ कमेंट सेव्ह झाली!")

            if st.button("📈 GENERATE ABSTRACT SHEET & MATERIAL REPORT", type="primary", key="qs_gen_btn"):
                if not stage_results:
                    st.warning("⚠️ कृपया कमीत कमी एका स्टेजसाठी Nos, Length, Width आणि Height च्या व्हॅल्यू भरा!")
                else:
                    st.success("🎉 Abstract Sheet & Material Report यशस्वीरित्या तयार झाला आहे!")
                    st.markdown("### 📊 ABSTRACT SHEET & MATERIAL REPORT")
                    st.info(f"👤 **Prepared For:** {current_user_name}")

                    table_rows = ""
                    whatsapp_text_items = ""

                    for r in stage_results:
                        table_rows += f"| {r['Stage']} | {r['Nos']} | {r['Dimensions']} | {r['TotalQty']} | {r['Material']} |\n"
                        whatsapp_text_items += f"• *{r['Stage']}*\n  - Nos: {r['Nos']} | Size: {r['Dimensions']}\n  - Total Net Qty: {r['TotalQty']}\n  - Material: {r['Material']}\n\n"

                    final_report_html = f"""
<div class="print-container">
<h2>📊 PATIL INFRATECH - ABSTRACT SHEET & QUANTITY SURVEY</h2>
<p><strong>Prepared For:</strong> {current_user_name} | <strong>Date:</strong> {get_ist_time().strftime('%d-%m-%Y')}</p>

| Description | Nos | Length x Width x Height | Net Quantity | Material Required |
| :--- | :--- | :--- | :--- | :--- |
{table_rows}

---
### 📌 SUMMARY
* **Status:** Report Generated Successfully (Deductions Applied)
</div>
"""
                    st.markdown(final_report_html, unsafe_allow_html=True)

                    msg_text = f"📊 *PATIL INFRATECH - ABSTRACT SHEET*\n👤 *Prepared For:* {current_user_name}\n📅 *Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n📋 *MEASUREMENT DETAILS (NET QUANTITIES):*\n{whatsapp_text_items}_Generated by Patil Infratech_"
                    encoded_msg = urllib.parse.quote(msg_text)

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        render_whatsapp_feature(encoded_msg, "qs_main")
                    with btn_col2:
                        st.markdown(
                            """
                            <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                                📄 Print / Save A3 Size PDF
                            </button>
                            """,
                            unsafe_allow_html=True,
                        )

                    if current_user_name:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO history (user_key, timestamp, user_note, report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                            (current_user_name, now_str, st.session_state.current_comment, final_report_html, st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()

# ==========================================
# 📌 विभाग १७: SITE MANAGER मुख्य मॉड्यूल (Sub-modules)
# ==========================================
elif st.session_state.selected_module == "Site Manager":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_site"):
        st.session_state.selected_module = None
        st.session_state.selected_site_sub_module = None
        st.rerun()

    st.write("---")
    st.subheader("👷‍♂️ Construction Site Manager Dashboard")

    if st.session_state.selected_site_sub_module is None:
        st.markdown("##### 🔽 खालीलपैकी एक साईट मॅनेजर टूल निवडा:")

        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">👷</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Attendance & Wages</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[हजेरी व मजुरी]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("👷 Attendance", key="btn_site_att", use_container_width=True):
                st.session_state.selected_site_sub_module = "Attendance"
                trigger_push_state()
                st.rerun()

        with s_col2:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">📦</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Material Inventory</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[साहित्य ट्रॅकर]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("📦 Material Stock", key="btn_site_inv", use_container_width=True):
                st.session_state.selected_site_sub_module = "Inventory"
                trigger_push_state()
                st.rerun()

        with s_col3:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">📸</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Progress Report</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[प्रोग्रेस रिपोर्ट]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("📸 Progress Report", key="btn_site_prog", use_container_width=True):
                st.session_state.selected_site_sub_module = "Progress"
                trigger_push_state()
                st.rerun()

        st.write(" ")
        s_col4, s_col5, s_col6 = st.columns(3)
        with s_col4:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">🏗️</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Pre-Concreting Checklist</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[स्लॅब चेकलिस्ट]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🏗️ Pre-Concreting Checklist", key="btn_site_chk", use_container_width=True):
                st.session_state.selected_site_sub_module = "Checklist"
                trigger_push_state()
                st.rerun()

        with s_col5:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.3);">
                    <h1 style="font-size: 32px; margin:0;">📊</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f8fafc; font-weight:700; font-size:13px;">Weekly Dashboard</h5>
                    <p style="font-size: 9px; color: #38bdf8; margin:0;">[मागील ७ दिवसांचा रिपोर्ट]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("📊 Weekly Dashboard", key="btn_site_week", use_container_width=True):
                st.session_state.selected_site_sub_module = "Weekly"
                trigger_push_state()
                st.rerun()

        with s_col6:
            st.markdown(
                """
                <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid rgba(245, 158, 11, 0.4);">
                    <h1 style="font-size: 32px; margin:0;">⏳</h1>
                    <h5 style="margin: 8px 0 2px 0; color: #f59e0b; font-weight:700; font-size:13px;">Project Timeline & Delay</h5>
                    <p style="font-size: 9px; color: #94a3b8; margin:0;">[फिनिशिंग दिवस व डिले ट्रॅकर]</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("⏳ Timeline Tracker", key="btn_site_delay", use_container_width=True):
                st.session_state.selected_site_sub_module = "Timeline"
                trigger_push_state()
                st.rerun()

    else:
        if st.button("⬅️ Back to Site Manager Menu", key="btn_back_site_menu"):
            st.session_state.selected_site_sub_module = None
            st.rerun()

        st.write("---")
        sub_mod = st.session_state.selected_site_sub_module

        # १७.१ Attendance & Wages Tracker
        if sub_mod == "Attendance":
            st.markdown("#### 👷 डेली हजेरी आणि मजुरी कॅल्क्युलेटर")
            att_date = st.date_input("तारीख निवडा (Select Date):", datetime.date.today(), key="site_att_date")

            st.markdown("##### 👥 कामगारांची माहिती भरा:")
            w_cols = st.columns([1.5, 1, 1, 1])
            with w_cols[0]:
                st.markdown("**कामगार प्रकार**")
            with w_cols[1]:
                st.markdown("**संख्या (Nos)**")
            with w_cols[2]:
                st.markdown("**रोजंदारी (Rate ₹)**")
            with w_cols[3]:
                st.markdown("**एकूण (Total ₹)**")

            w_data = {}
            total_labor_cost = 0.0

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

            for w_id, w_name, def_q, def_r in labor_types:
                r_cols = st.columns([1.5, 1, 1, 1])
                with r_cols[0]:
                    st.markdown(f"<p style='margin-top:8px;'>{w_name}</p>", unsafe_allow_html=True)
                with r_cols[1]:
                    q = st.number_input(f"Qty {w_id}", min_value=0, value=def_q, step=1, key=f"q_{w_id}", label_visibility="collapsed")
                with r_cols[2]:
                    r = st.number_input(f"Rate {w_id}", min_value=0.0, value=def_r, step=50.0, key=f"r_{w_id}", label_visibility="collapsed")
                with r_cols[3]:
                    t = q * r
                    st.markdown(f"<p style='margin-top:8px; font-weight:bold;'>₹ {t:.2f}</p>", unsafe_allow_html=True)
                    total_labor_cost += t

                w_data[w_id] = {"qty": q, "rate": r}

            st.markdown(
                f"""
                <div style="background: #111827; padding: 18px; border-radius: 16px; border-left: 5px solid #10b981; margin-top: 12px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);">
                    <h4 style="margin:0; color:#10b981;">💰 Today's Total Labor Cost: ₹ {total_labor_cost:.2f}/-</h4>
                    <p style="margin:5px 0 0 0; font-size:13px; color:#cbd5e1;">(सर्व कामगारांची एकूण मजुरी)</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("💾 Save Attendance to SQLite Database", type="primary", key="save_att_btn"):
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
                        w_data["supervisor"]["qty"],
                        w_data["supervisor"]["rate"],
                        w_data["mason"]["qty"],
                        w_data["mason"]["rate"],
                        w_data["labor"]["qty"],
                        w_data["labor"]["rate"],
                        w_data["fitter"]["qty"],
                        w_data["fitter"]["rate"],
                        w_data["carpenter"]["qty"],
                        w_data["carpenter"]["rate"],
                        w_data["plumber"]["qty"],
                        w_data["plumber"]["rate"],
                        w_data["electrician"]["qty"],
                        w_data["electrician"]["rate"],
                        w_data["painter"]["qty"],
                        w_data["painter"]["rate"],
                        total_labor_cost,
                        st.session_state.current_site_name,
                    ),
                )
                conn.commit()
                conn.close()
                st.success("✅ आजची हजेरी आणि मजुरी बिल डेटाबेसमध्ये सेव्ह झाले!")

        # १७.२ Material Stock & Inventory Tracker
        elif sub_mod == "Inventory":
            st.markdown("#### 📦 साहित्य ट्रॅकर (Material Inventory & Stock Tracker)")

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT material_name, transaction_type, quantity FROM site_inventory WHERE user_key = ?",
                (current_user_name,),
            )
            inv_rows = cursor.fetchall()
            conn.close()

            stock_dict = {}
            for row in inv_rows:
                mat = row["material_name"]
                ttype = row["transaction_type"]
                qty = row["quantity"]

                if mat not in stock_dict:
                    stock_dict[mat] = 0
                if ttype == "Material IN (+)":
                    stock_dict[mat] += qty
                else:
                    stock_dict[mat] -= qty

            st.markdown("##### 📊 Live Cement & Material Stock Balance:")
            if stock_dict:
                for item, count in stock_dict.items():
                    if count <= 10:
                        st.markdown(
                            f"""
                            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; padding: 12px 16px; border-radius: 12px; margin-bottom: 8px;">
                                <span style="color: #ef4444; font-weight: bold; font-size: 16px;">⚠️ Warning: {item} Stock Low! Re-order Soon</span><br>
                                <span style="color: #ffffff; font-size: 14px;">Current Stock: <b>{count} Bags/Units</b></span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="background: #111827; border: 1px solid #00f2fe; padding: 10px 16px; border-radius: 12px; margin-bottom: 8px;">
                                <span style="color: #38bdf8; font-weight: bold;">Current {item} Stock:</span> <code style="font-size:16px; color:#10b981;">{count} Bags/Units</code>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.info("ℹ️ सध्या स्टॉकमध्ये कोणतीही एंट्री उपलब्ध नाही. खालील इन-आऊट फॉर्म भरा.")

            st.write("---")
            st.markdown("##### ➕/➖ Material IN-OUT Entry:")
            mat_name = st.selectbox("साहित्य निवडा (Material):", ["Cement Bags", "Steel (Kg)", "Sand (CFT)", "Bricks (Nos)"], key="inv_mat_type")
            trans_type = st.radio("इनपुट/आऊटपुट निवडा:", ["Material IN (+)", "Material OUT (-)"], horizontal=True, key="inv_trans_type")
            entry_qty = st.number_input("बोरी / नग संख्या (Quantity):", min_value=1, value=100, step=1, key="inv_qty_val")

            if st.button("📥 Save Stock Entry", type="primary", key="save_inv_btn"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_inventory (user_key, date, material_name, transaction_type, quantity, unit, site_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_user_name,
                        str(datetime.date.today()),
                        mat_name,
                        trans_type,
                        entry_qty,
                        "Bags/Units",
                        st.session_state.current_site_name,
                    ),
                )
                conn.commit()
                conn.close()
                st.success("✅ स्टॉक एंट्री सेव्ह झाली!")
                st.rerun()

        # १७.३ Daily Progress Report & Photos
        elif sub_mod == "Progress":
            st.markdown("#### 📸 साईट प्रोग्रेस रिपोर्ट (Daily Progress & Photo Upload)")

            work_stage = st.text_input("कामाचा टप्पा (Stage Name):", value="Plinth Level Completed", key="prog_stage_input")
            work_percent = st.slider("Work % Slider (कामाची टक्केवारी):", 0, 100, 40, key="prog_percent_slider")
            site_photo = st.file_uploader("मोबाईल किंवा कॅमेऱ्याने फोटो अपलोड करा:", type=["png", "jpg", "jpeg"], key="prog_photo_upload")
            site_remark = st.text_area("कामाचा रिमार्क / शेरा:", placeholder="उदा. साईटवर प्लिंथ लेव्हल कास्टिंगचे काम पूर्ण झाले आहे...", key="prog_remark_input")

            if site_photo:
                st.image(site_photo, caption="Uploaded Site Work Photo", use_column_width=True)

            if st.button("📊 Generate Instant PDF Report & WhatsApp Summary", type="primary", key="save_prog_btn"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_progress (user_key, date, stage_name, progress_percent, remark, site_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_user_name,
                        str(datetime.date.today()),
                        work_stage,
                        work_percent,
                        site_remark,
                        st.session_state.current_site_name,
                    ),
                )
                conn.commit()
                conn.close()

                report_summary = (
                    f"🏗️ *PATIL INFRATECH - DAILY SITE PROGRESS REPORT*\n👤 *Site Engineer:* {current_user_name}\n"
                    f"📍 *Site:* {st.session_state.current_site_name}\n📅 *Date:* {datetime.date.today()}\n"
                    f"🚧 *Stage:* {work_stage}\n📈 *Work Completed:* {work_percent}%\n"
                    f"📝 *Remark:* {site_remark}\n--------------------------------\n_Daily Progress Report Generated_"
                )

                st.success("🎉 Daily Progress Report यशस्वीरित्या जनरेट झाला आहे!")
                st.code(report_summary)

                encoded_prog_msg = urllib.parse.quote(report_summary)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    try:
                        render_whatsapp_feature(encoded_prog_msg, "site_prog_wa")
                    except Exception:
                        st.markdown(f"[Send WhatsApp](https://wa.me/?text={encoded_prog_msg})")
                with btn_col2:
                    st.markdown(
                        """
                        <button onclick="window.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                            📄 Download Instant PDF Report
                        </button>
                        """,
                        unsafe_allow_html=True,
                    )

        # १७.४ Pre-Concreting Digital Checklist
        elif sub_mod == "Checklist":
            st.markdown("#### 🏗️ Pre-Concreting Checklist (स्लॅब भरण्यापूर्वीची डिजिटल चेकलिस्ट)")
            st.caption("💡 काँक्रीटिंग किंवा स्लॅब भरण्यापूर्वी साईट इंजिनिअरने खालील सर्व बाबी तपासून टिक-मार्क करणे आवश्यक आहे.")

            default_chk_items = [
                "Cover Blocks (कव्हर ब्लॉक्स) लावलेले आहेत का?",
                "Shuttering (शटरिंग) चा लेव्हल व सपोर्ट ओके आहे का?",
                "Electrical Conduit Pipes व जंक्शन बॉक्सेस टाकले आहेत का?",
                "Curing (क्युरिंग) साठी पाण्याची योग्य सोय आहे का?",
                "सरयांचे अंतर (Reinforcement Spacing) व लॅपिंग ओके आहे का?",
                "शटरिंग ऑइल (Shuttering Oil) लावून कचरा साफ केला आहे का?",
                "कँक्रीट व्हायब्रेटर (Vibrator) चालू स्थितीत तयार आहे का?",
            ]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, item_text, is_checked FROM pre_concreting_checklist WHERE user_key = ?",
                (current_user_name,),
            )
            db_items = cursor.fetchall()

            if not db_items:
                now_time_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
                for text in default_chk_items:
                    cursor.execute(
                        "INSERT INTO pre_concreting_checklist (user_key, item_text, is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
                        (current_user_name, text, now_time_str, st.session_state.current_site_name),
                    )
                conn.commit()
                cursor.execute(
                    "SELECT id, item_text, is_checked FROM pre_concreting_checklist WHERE user_key = ?",
                    (current_user_name,),
                )
                db_items = cursor.fetchall()
            conn.close()

            total_items = len(db_items)
            checked_items = sum(1 for item in db_items if item["is_checked"] == 1)
            progress_percentage = int((checked_items / total_items) * 100) if total_items > 0 else 0

            st.markdown(
                f"""
                <div style="background: #111827; border: 1px solid rgba(0, 242, 254, 0.4); padding: 18px; border-radius: 16px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 15px; margin-bottom: 8px;">
                        <span>पूर्णता: <span style="color:#00f2fe;">{progress_percentage}%</span></span>
                        <span>{checked_items}/{total_items} चेक केले</span>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(progress_percentage)

            if progress_percentage == 100 and total_items > 0:
                st.markdown(
                    """
                    <div style="background: #166534; color: #dcfce7; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 15px; margin-top: 10px;">
                        ✅ काँक्रीटिंग सुरू करण्यास पूर्ण परवानगी आहे! (All Checks Passed)
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style="background: #991b1b; color: #fee2e2; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 15px; margin-top: 10px;">
                        🛑 काँक्रीटिंग सुरू करू नका (अजून काही पॉईंट्स बाकी आहेत)
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.expander("➕ नवीन चेकलिस्ट पॉईंट जोडा"):
                new_chk_text = st.text_input("नवीन तपासणी पॉईंट टाका:", placeholder="उदा. जनरेटर बॅकअपची सोय आहे का?...", key="new_chk_input")
                if st.button("प्लस (+)", key="btn_add_chk_item"):
                    if new_chk_text.strip():
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO pre_concreting_checklist (user_key, item_text, is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
                            (current_user_name, new_chk_text.strip(), get_ist_time().strftime("%Y-%m-%d %H:%M:%S"), st.session_state.current_site_name),
                        )
                        conn.commit()
                        conn.close()
                        st.success("✅ नवीन पॉईंट चेकलिस्टमध्ये जोडला गेला!")
                        st.rerun()

            st.markdown("##### 📝 चेकलिस्ट आयटम्स (टिक-मार्क करा):")
            for item in db_items:
                item_id = item["id"]
                item_text = item["item_text"]
                is_chk = bool(item["is_checked"])

                col_chk, col_del = st.columns([4.5, 0.5])
                with col_chk:
                    new_state = st.checkbox(item_text, value=is_chk, key=f"chk_box_{item_id}")
                    if new_state != is_chk:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE pre_concreting_checklist SET is_checked = ? WHERE id = ?",
                            (1 if new_state else 0, item_id),
                        )
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

            st.write("---")
            if st.button("🔄 चेकलिस्ट रिसेट करा (पुन्हा नवीन स्लॅबसाठी तपासणी करा)"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE pre_concreting_checklist SET is_checked = 0 WHERE user_key = ?",
                    (current_user_name,),
                )
                conn.commit()
                conn.close()
                st.success("✅ सर्व टिक-मार्क्स रिसेट झाले आहेत!")
                st.rerun()

        # १७.५ Weekly Site Dashboard & Logs
        elif sub_mod == "Weekly":
            st.markdown("#### 📊 मागील ७ दिवसांचा साइट रिपोर्ट (Weekly Site Dashboard)")
            st.caption("💡 मागील ७ दिवसांमधील तुमची हजेरी (Attendance), मटेरियल खर्च आणि कामाची प्रगती. तुम्ही चुकीची एंट्री येथून डिलीट करू शकता.")

            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            str_today = str(today)
            str_week_ago = str(week_ago)

            conn = get_db_connection()

            # १. Attendance Logs
            att_df = pd.read_sql_query(
                f"SELECT rowid as id, date as Date, total_cost as Daily_Wage_Cost FROM site_attendance WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
                conn,
            )

            # २. Inventory Logs
            inv_df = pd.read_sql_query(
                f"SELECT rowid as id, date as Date, material_name as Material, transaction_type as Status, quantity as Qty FROM site_inventory WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
                conn,
            )

            # ३. Progress Logs
            prog_df = pd.read_sql_query(
                f"SELECT rowid as id, date as Date, stage_name as Work_Stage, progress_percent as Completed_Percent FROM site_progress WHERE user_key = '{current_user_name}' AND date BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
                conn,
            )

            conn.close()

            with st.expander("👷 मागील ७ दिवसांची हजेरी आणि मजुरी खर्च (Wages)", expanded=True):
                if not att_df.empty:
                    total_week_wage = att_df["Daily_Wage_Cost"].sum()
                    st.markdown(f"**💰 एकूण ७ दिवसांचा मजुरी खर्च:** <span style='color:#10b981; font-size:18px;'>₹ {total_week_wage:,.2f}</span>", unsafe_allow_html=True)
                    st.dataframe(att_df.drop(columns=["id"]), use_container_width=True, hide_index=True)

                    st.markdown("---")
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        att_del_opt = st.selectbox(
                            "❌ डिलीट करण्यासाठी रेकॉर्ड निवडा:",
                            att_df.to_dict("records"),
                            format_func=lambda x: f"तारीख: {x['Date']} | रक्कम: ₹ {x['Daily_Wage_Cost']}",
                            key="sel_del_att",
                        )
                    with c2:
                        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete Record", key="btn_del_att", use_container_width=True):
                            conn = get_db_connection()
                            conn.execute("DELETE FROM site_attendance WHERE rowid=?", (att_del_opt["id"],))
                            conn.commit()
                            conn.close()
                            st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
                            st.rerun()
                else:
                    st.info("ℹ️ मागील ७ दिवसात कोणतीही हजेरी नोंदवली नाही.")

            with st.expander("📦 मागील ७ दिवसांचा मटेरियल ट्रॅकर (Material IN/OUT)"):
                if not inv_df.empty:
                    st.dataframe(inv_df.drop(columns=["id"]), use_container_width=True, hide_index=True)

                    st.markdown("---")
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        inv_del_opt = st.selectbox(
                            "❌ डिलीट करण्यासाठी रेकॉर्ड निवडा:",
                            inv_df.to_dict("records"),
                            format_func=lambda x: f"{x['Date']} | {x['Material']} | {x['Status']} ({x['Qty']})",
                            key="sel_del_inv",
                        )
                    with c2:
                        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete Record", key="btn_del_inv", use_container_width=True):
                            conn = get_db_connection()
                            conn.execute("DELETE FROM site_inventory WHERE rowid=?", (inv_del_opt["id"],))
                            conn.commit()
                            conn.close()
                            st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
                            st.rerun()
                else:
                    st.info("ℹ️ मागील ७ दिवसात कोणतेही मटेरियल IN/OUT नोंदवले नाही.")

            with st.expander("📸 मागील ७ दिवसांची कामाची प्रगती (Progress)"):
                if not prog_df.empty:
                    for _, row in prog_df.iterrows():
                        st.markdown(f"**📅 Date:** `{row['Date']}` | **🚧 Work:** {row['Work_Stage']} | **📈 Progress:** `{row['Completed_Percent']}%`")
                        st.progress(int(row["Completed_Percent"]))

                    st.markdown("---")
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        prog_del_opt = st.selectbox(
                            "❌ डिलीट करण्यासाठी रेकॉर्ड निवडा:",
                            prog_df.to_dict("records"),
                            format_func=lambda x: f"{x['Date']} | {x['Work_Stage']}",
                            key="sel_del_prog",
                        )
                    with c2:
                        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete Record", key="btn_del_prog", use_container_width=True):
                            conn = get_db_connection()
                            conn.execute("DELETE FROM site_progress WHERE rowid=?", (prog_del_opt["id"],))
                            conn.commit()
                            conn.close()
                            st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
                            st.rerun()
                else:
                    st.info("ℹ️ मागील ७ दिवसात कामाचा कोणताही प्रोग्रेस रिपोर्ट नोंदवला नाही.")

        # १७.६ Project Timeline, Delay Analysis & Finish Date Tracker
        elif sub_mod == "Timeline":
            st.markdown("#### ⏳ प्रोजेक्ट टाईमलाईन व डिले ट्रॅकर (Finish Date Calculator)")
            st.caption(f"📍 सध्याची साईट: **{st.session_state.current_site_name}** | एखाद्या टप्प्याला उशीर झाल्यास प्रोजेक्ट कधी पूर्ण होईल याचा थेट हिशोब.")

            load_default_tasks_if_empty(current_user_name, st.session_state.current_site_name)

            col_p1, _ = st.columns([2, 2])
            with col_p1:
                proj_start_date = st.date_input(
                    "प्रोजेक्ट सुरू झालेली तारीख (Start Date):",
                    datetime.date.today(),
                    key="proj_start_dt",
                )

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
            with m1:
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #334155; padding: 14px; border-radius: 12px; text-align: center;">
                        <span style="color:#94a3b8; font-size:12px;">मूळ अंदाजित दिवस</span>
                        <h3 style="margin: 4px 0; color:#38bdf8;">{total_planned_days} दिवस</h3>
                        <small style="color:#64748b;">({original_finish_date.strftime('%d-%m-%Y')})</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with m2:
                delay_color = "#ef4444" if total_critical_delay > 0 else "#10b981"
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid {delay_color}; padding: 14px; border-radius: 12px; text-align: center;">
                        <span style="color:#94a3b8; font-size:12px;">झालेला एकूण उशीर (Delay)</span>
                        <h3 style="margin: 4px 0; color:{delay_color};">+{total_critical_delay} दिवस</h3>
                        <small style="color:#64748b;">(Critical Path)</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with m3:
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #f59e0b; padding: 14px; border-radius: 12px; text-align: center;">
                        <span style="color:#94a3b8; font-size:12px;">नवीन अंदाजित दिवस</span>
                        <h3 style="margin: 4px 0; color:#f59e0b;">{total_projected_days} दिवस</h3>
                        <small style="color:#64748b;">(एकूण कालावधी)</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with m4:
                st.markdown(
                    f"""
                    <div style="background: #111827; border: 1px solid #10b981; padding: 14px; border-radius: 12px; text-align: center;">
                        <span style="color:#94a3b8; font-size:12px;">ताबा / फायनल समाप्ती तारीख</span>
                        <h3 style="margin: 4px 0; color:#10b981; font-size: 18px;">{new_projected_finish_date.strftime('%d %b %Y')}</h3>
                        <small style="color:#64748b;">(Projected Handover)</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.write("---")
            st.markdown("##### 📋 कामांचे टप्पे आणि उशीर व्यवस्थापन (Update Progress & Delays):")

            header_c = st.columns([0.6, 2.8, 1.2, 1.2, 1.4, 1.0])
            header_c[0].markdown("**क्र.**")
            header_c[1].markdown("**कामाचा टप्पा (Task)**")
            header_c[2].markdown("**नियोजित दिवस**")
            header_c[3].markdown("**उशीर (Delay)**")
            header_c[4].markdown("**स्टेटस**")
            header_c[5].markdown("**Critical?**")

            updated_tasks = []
            for t in tasks:
                tc = st.columns([0.6, 2.8, 1.2, 1.2, 1.4, 1.0])
                t_id = t["id"]
                tc[0].markdown(f"<p style='margin-top:8px;'>{t['stage_order']}</p>", unsafe_allow_html=True)
                tc[1].markdown(f"<p style='margin-top:8px; font-weight:600;'>{t['task_name']}</p>", unsafe_allow_html=True)

                new_plan = tc[2].number_input(
                    f"Plan_{t_id}",
                    min_value=1,
                    value=t["planned_duration"],
                    step=1,
                    key=f"plan_dur_{t_id}",
                    label_visibility="collapsed",
                )
                new_delay = tc[3].number_input(
                    f"Delay_{t_id}",
                    min_value=0,
                    value=t["delay_days"],
                    step=1,
                    key=f"delay_dur_{t_id}",
                    label_visibility="collapsed",
                )
                new_status = tc[4].selectbox(
                    f"Status_{t_id}",
                    ["Pending", "In Progress", "Completed"],
                    index=["Pending", "In Progress", "Completed"].index(t["status"]),
                    key=f"status_{t_id}",
                    label_visibility="collapsed",
                )
                is_crit = tc[5].checkbox(
                    "",
                    value=bool(t["is_critical"]),
                    key=f"crit_{t_id}",
                    help="हे काम उशिरा झाल्यास थेट पूर्ण प्रोजेक्ट पुढे ढकलला जाईल का?",
                )

                updated_tasks.append(
                    (new_plan, new_delay, new_status, 1 if is_crit else 0, t_id)
                )

            st.write(" ")
            if st.button("💾 बदल सेव्ह करा आणि नवीन तारीख कॅल्क्युलेट करा", type="primary", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                for p, d, s, c, tid in updated_tasks:
                    cursor.execute(
                        """
                        UPDATE project_tasks 
                        SET planned_duration = ?, delay_days = ?, status = ?, is_critical = ?
                        WHERE id = ?
                        """,
                        (p, d, s, c, tid),
                    )
                conn.commit()
                conn.close()
                st.success("✅ प्रोजेक्ट टाईमलाईन अपडेट झाली!")
                st.rerun()

            st.write("---")
            wa_timeline_text = (
                "🏗️ *PATIL INFRATECH - PROJECT TIMELINE REPORT*\n"
                f"📍 *Site:* {st.session_state.current_site_name}\n"
                f"📅 *Start Date:* {proj_start_date.strftime('%d-%m-%Y')}\n"
                f"⏱️ *Planned Duration:* {total_planned_days} Days\n"
                f"🚨 *Total Delay:* +{total_critical_delay} Days\n"
                f"🎯 *Projected Handover Date:* {new_projected_finish_date.strftime('%d-%m-%Y')}\n"
                "--------------------------------\n_Generated by Patil Infratech_"
            )

            render_whatsapp_feature(
                urllib.parse.quote(wa_timeline_text), "site_timeline_wa"
            )
# ==========================================
# विभाग १८: NEEVPAY / SITESETU मुख्य मॉड्यूल (Milestone Escrow & Payment Protection)
# ==========================================
elif st.session_state.selected_module == "NeevPay":
    if st.button("मुख्य मेनूवर जा (Back to Main)", key="btn_back_neevpay"):
        st.session_state.selected_module = None
        st.rerun()

    st.write("---")
    neevpay_banner = (
        "<div style='background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); "
        "padding: 18px; border-radius: 16px; border: 1px solid #10b981; margin-bottom: 20px;'>"
        "<h2 style='margin: 0; color: #10b981; font-weight: 900;'>NEEVPAY / SITESETU - SMART PAYMENT ESCROW & BILLING</h2>"
        "<p style='margin: 5px 0 0 0; color: #cbd5e1; font-size: 14px;'>"
        "इंजिनिअर व घरमालक यांच्यातील कामावर आधारित पारदर्शक बिलिंग, संमती-आधारित पेमेंट लॉक व अधिकृत Master Invoice व्यवस्था."
        "</p></div>"
    )
    st.markdown(neevpay_banner, unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    # क्लायंटचा नोंदणीकृत ईमेल आणणे
    cursor.execute(
        "SELECT client_email FROM site_client_profiles WHERE user_key = ? AND site_name = ?",
        (current_user_name, st.session_state.current_site_name),
    )
    client_row = cursor.fetchone()
    client_email = client_row["client_email"] if client_row else ""

    # डेटाबेसमधून चालू साईटचे सर्व टप्पे आणणे
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

    # ==========================================================
    # १. क्लायंट ईमेल नोंदणी व व्यवस्थापन
    # ==========================================================
    with st.container():
        if not client_email:
            st.warning("NeevPay इनव्हॉइस व सुरक्षिततेसाठी घरमालकाचा (Client) Email ID सेव्ह करा.")

            c_mail_in = st.text_input(
                "घरमालकाचा ईमेल पत्ता (Client Email ID):",
                placeholder="client@gmail.com",
                key="reg_client_mail",
            )

            if st.button("ईमेल सेव्ह करा", key="btn_save_init_email", type="primary"):
                if c_mail_in.strip() and "@" in c_mail_in:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT OR REPLACE INTO site_client_profiles (user_key, site_name, client_email) VALUES (?, ?, ?)",
                        (
                            current_user_name,
                            st.session_state.current_site_name,
                            c_mail_in.strip().lower(),
                        ),
                    )
                    conn.commit()
                    conn.close()
                    st.success("घरमालकाचा ईमेल यशस्वीरित्या सेव्ह झाला!")
                    st.rerun()
                else:
                    st.error("कृपया योग्य ईमेल पत्ता टाका.")
        else:
            c_info_col1, c_info_col2 = st.columns([3, 1])
            with c_info_col1:
                st.info(f"रजिस्टर असलेला अधिकृत Email: `{client_email}` (या ईमेलवर इनव्हॉइस पाठवले जाईल)")
            with c_info_col2:
                with st.popover("ईमेल बदला"):
                    new_mail_edit = st.text_input("नवीन ईमेल टाका:", value=client_email, key="edit_c_mail")
                    if st.button("अपडेट करा", key="btn_update_c_mail", type="primary"):
                        if new_mail_edit.strip() and "@" in new_mail_edit:
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE site_client_profiles SET client_email = ? WHERE user_key = ? AND site_name = ?",
                                (new_mail_edit.strip().lower(), current_user_name, st.session_state.current_site_name),
                            )
                            conn.commit()
                            conn.close()
                            st.success("ईमेल अपडेट झाला!")
                            st.rerun()

    st.write("---")

    # बजेट आणि समरी हिशोब
    total_budget = sum(m["planned_amount"] for m in milestones)
    total_received = sum(m["amount_deposited"] for m in milestones)
    total_pending = max(0.0, total_budget - total_received)
    locked_stages = sum(1 for m in milestones if m.get("is_locked") == 1)
    overall_site_pct = (total_received / total_budget * 100) if total_budget > 0 else 0.0

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #334155; padding: 14px; border-radius: 12px; text-align: center;">
                <span style="color:#94a3b8; font-size:12px;">एकूण ठरलेले बजेट / बिल</span>
                <h4 style="margin: 4px 0; color:#38bdf8;">Rs. {total_budget:,.2f}</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #10b981; padding: 14px; border-radius: 12px; text-align: center;">
                <span style="color:#94a3b8; font-size:12px;">क्लायंटने दिलेली रक्कम</span>
                <h4 style="margin: 4px 0; color:#10b981;">Rs. {total_received:,.2f}</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e3:
        p_color = "#ef4444" if total_pending > 0 else "#10b981"
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid {p_color}; padding: 14px; border-radius: 12px; text-align: center;">
                <span style="color:#94a3b8; font-size:12px;">उर्वरित बाकी रक्कम (Balance)</span>
                <h4 style="margin: 4px 0; color:{p_color};">Rs. {total_pending:,.2f}</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e4:
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #00f2fe; padding: 14px; border-radius: 12px; text-align: center;">
                <span style="color:#94a3b8; font-size:12px;">पूर्ण टप्पे व प्रगती</span>
                <h4 style="margin: 4px 0; color:#00f2fe;">{locked_stages}/{len(milestones)} ({overall_site_pct:.1f}%)</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("---")

    # ==========================================================
    # २. इंजिनिअर पॅनल: नवीन कामाचा टप्पा आणि बिल स्वतः तयार करा
    # ==========================================================
    with st.expander("कामाचे नवीन बिल / टप्पा तयार करा", expanded=(len(milestones) == 0)):
        st.caption("इंजिनिअर कामाचा प्रकार निवडून किंवा स्वतः लिहून त्याचे ठरलेले बिल निश्चित करू शकतो.")

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

        selected_work_type = st.selectbox("कामाचा प्रकार निवडा (Select Work Stage):", work_presets, key="sel_work_preset")

        if selected_work_type == "इतर सानुकूल काम (Custom Work Name...)":
            custom_stage_name = st.text_input("कामाचे नाव टाका (Custom Work Name):", placeholder="उदा. वॉटरप्रूफिंग व टेरेस काम...", key="custom_stg_input")
            final_stage_name = custom_stage_name.strip()
        else:
            final_stage_name = selected_work_type

        init_stage_amt = st.number_input(
            "या कामाचे ठरलेले बिल (Rs.) [किमान Rs. 1]:",
            min_value=1.0,
            value=50000.0,
            step=1000.0,
            key="new_stage_init_amt"
        )

        if st.button("कामाचे बिल निश्चित करा व सेव्ह करा", key="btn_create_custom_milestone", type="primary"):
            if final_stage_name:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO site_milestone_payments 
                    (user_key, site_name, stage_name, planned_amount, amount_deposited, status, engineer_approved, client_approved, is_locked, remark)
                    VALUES (?, ?, ?, ?, 0.0, 'Bill Fixed (Unpaid)', 0, 0, 0, 'काही नाही')
                    """,
                    (
                        current_user_name,
                        st.session_state.current_site_name,
                        final_stage_name,
                        float(init_stage_amt),
                    ),
                )
                conn.commit()
                conn.close()
                st.success(f"'{final_stage_name}' चे Rs. {init_stage_amt:,.2f} चे बिल निश्चित झाले!")
                st.rerun()
            else:
                st.warning("कृपया कामाचे नाव टाका!")

    # ==========================================================
    # ३. NEEVPAY MASTER BILL / ESCROW STATEMENT PDF & DIRECT EMAIL
    # ==========================================================
    if milestones:
        with st.expander("NeevPay Master Escrow Statement & Invoicing (PDF / Print / Email)", expanded=False):
            st.caption("क्लायंट व इंजिनिअरसाठी अधिकृत डिजिटल A4 Master Statement, PDF इनव्हॉइस आणि थेट ईमेल सुविधा.")

            table_rows_html = ""
            for idx, m_item in enumerate(milestones, 1):
                p_val = float(m_item["planned_amount"])
                d_val = float(m_item["amount_deposited"])
                bal_val = max(0.0, p_val - d_val)
                stage_pct = (d_val / p_val * 100) if p_val > 0 else 0.0

                if m_item.get("is_locked") == 1:
                    st_badge = "<span style='color: #10b981; font-weight:bold;'>FULLY PAID (100%)</span>"
                elif d_val >= p_val and p_val > 0:
                    st_badge = "<span style='color: #0284c7; font-weight:bold;'>READY TO LOCK</span>"
                elif d_val > 0:
                    st_badge = f"<span style='color: #d97706; font-weight:bold;'>PARTIAL ({stage_pct:.1f}%)</span>"
                elif p_val > 0:
                    st_badge = "<span style='color: #ef4444; font-weight:bold;'>UNPAID</span>"
                else:
                    st_badge = "<span style='color: #64748b;'>BILL PENDING</span>"

                table_rows_html += f"""
                <tr>
                    <td style="text-align:center; font-weight:bold;">{idx}</td>
                    <td><b>{m_item['stage_name']}</b></td>
                    <td style="text-align:right;">Rs. {p_val:,.2f}</td>
                    <td style="text-align:right; color:#10b981; font-weight:bold;">Rs. {d_val:,.2f}</td>
                    <td style="text-align:right; color:#ef4444; font-weight:bold;">Rs. {bal_val:,.2f}</td>
                    <td style="text-align:center;">{st_badge}</td>
                    <td style="text-align:center; font-size:10px;">{m_item.get('completion_date') or '-'}</td>
                </tr>
                """

            neevpay_html_doc = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>NEEVPAY MASTER ESCROW STATEMENT - {st.session_state.current_site_name}</title>
                <style>
                    @page {{ size: A4 portrait; margin: 8mm; }}
                    @media print {{
                        body {{ background: #ffffff !important; color: #000000 !important; }}
                        .no-print {{ display: none !important; }}
                    }}
                    body {{ background-color: #e2e8f0; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 10px; color: #0f172a; }}
                    .a4-page {{ position: relative; background: #ffffff; width: 100%; max-width: 780px; margin: 0 auto 20px auto; padding: 25px 30px; border-radius: 6px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 1.5px solid #0f172a; box-sizing: border-box; min-height: 1020px; overflow: hidden; }}
                    .watermark {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-28deg); font-size: 22px; font-weight: 900; color: rgba(15, 23, 42, 0.08); text-transform: uppercase; letter-spacing: 2.5px; text-align: center; width: 78%; max-width: 500px; line-height: 1.5; pointer-events: none; user-select: none; border: 3px dashed rgba(15, 23, 42, 0.08); padding: 15px 25px; border-radius: 12px; z-index: 999; }}
                    .content-box {{ position: relative; z-index: 2; }}
                    .header-title {{ text-align: center; border-bottom: 2px solid #064e3b; padding-bottom: 6px; margin-bottom: 12px; }}
                    .header-title h1 {{ margin: 0; font-size: 22px; color: #064e3b; font-weight: 900; letter-spacing: 0.5px; }}
                    .header-title p {{ margin: 2px 0; font-size: 11px; font-weight: bold; color: #10b981; }}
                    table.info-table {{ width: 100%; margin-bottom: 12px; font-size: 12px; border-collapse: collapse; }}
                    table.info-table td {{ padding: 3px 0; }}
                    .section-header {{ background: #064e3b; color: #ffffff; padding: 6px 12px; font-size: 12px; font-weight: bold; border-radius: 4px; margin: 12px 0 8px 0; }}
                    table.custom-data-table {{ width: 100%; border-collapse: collapse; margin: 8px 0 15px 0; font-size: 11px; }}
                    table.custom-data-table th, table.custom-data-table td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
                    table.custom-data-table th {{ background-color: rgba(241, 245, 249, 0.95); font-weight: bold; color: #0f172a; }}
                    table.custom-data-table tr:nth-child(even) {{ background-color: rgba(248, 250, 252, 0.6); }}
                    .summary-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 15px; font-size: 12px; }}
                    .signature-box {{ margin-top: 40px; width: 100%; font-size: 12px; }}
                    .footer-stamp {{ text-align: center; margin-top: 25px; font-size: 10px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 5px; }}
                </style>
            </head>
            <body>
                <div class="a4-page">
                    <div class="watermark">NEEVPAY ESCROW<br>PATIL INFRATECH VERIFIED</div>
                    <div class="content-box">
                        <div class="header-title">
                            <h1>PATIL INFRATECH - NEEVPAY ESCROW</h1>
                            <p>SMART MILESTONE PAYMENT PROTECTION & MASTER INVOICE</p>
                            <small style="color: #64748b;">(Digital Milestone Escrow & Verification Protocol)</small>
                        </div>

                        <table class="info-table">
                            <tr>
                                <td><b>Project / Site:</b> <span style="color:#064e3b; font-weight:bold;">{st.session_state.current_site_name}</span></td>
                                <td style="text-align: right;"><b>Statement Date:</b> {get_ist_time().strftime('%d-%m-%Y')}</td>
                            </tr>
                            <tr>
                                <td><b>Engineer:</b> {current_user_name}</td>
                                <td style="text-align: right;"><b>Client Email:</b> {client_email or 'Not Registered'}</td>
                            </tr>
                        </table>
                        <hr style="border: 0.5px solid #cbd5e1; margin-bottom: 8px;">

                        <div class="section-header">
                            MILESTONE-WISE PAYMENT & COMPLETION STATEMENT
                        </div>

                        <table class="custom-data-table">
                            <thead>
                                <tr>
                                    <th style="text-align:center; width:30px;">#</th>
                                    <th>कामाचा टप्पा (Milestone Stage)</th>
                                    <th style="text-align:right;">ठरलेले बिल</th>
                                    <th style="text-align:right;">जमा रक्कम</th>
                                    <th style="text-align:right;">उर्वरित बाकी</th>
                                    <th style="text-align:center;">सद्यस्थिती</th>
                                    <th style="text-align:center;">लॉक दिनांक</th>
                                </tr>
                            </thead>
                            <tbody>
                                {table_rows_html}
                            </tbody>
                        </table>

                        <div class="summary-box">
                            <table style="width:100%; font-size:12px;">
                                <tr>
                                    <td><b>एकूण ठरलेले बजेट:</b> <span style="color:#0284c7; font-weight:bold;">Rs. {total_budget:,.2f}</span></td>
                                    <td><b>क्लायंटकडून प्राप्त:</b> <span style="color:#10b981; font-weight:bold;">Rs. {total_received:,.2f}</span></td>
                                    <td><b>शिल्लक बाकी:</b> <span style="color:#ef4444; font-weight:bold;">Rs. {total_pending:,.2f}</span></td>
                                    <td><b>प्रगती:</b> <span style="color:#00f2fe; font-weight:bold;">{overall_site_pct:.1f}% ({locked_stages}/{len(milestones)} टप्पे)</span></td>
                                </tr>
                            </table>
                        </div>

                        <table class="signature-box">
                            <tr>
                                <td style="width: 50%;">
                                    <br><br>
                                    __________________________<br>
                                    <b>Site Engineer Signature</b><br>
                                    <small style="color:#64748b;">Patil Infratech Authorized</small>
                                </td>
                                <td style="width: 50%; text-align: right;">
                                    <br><br>
                                    __________________________<br>
                                    <b>Client (Owner) Signature</b><br>
                                    <small style="color:#64748b;">Verified Approver</small>
                                </td>
                            </tr>
                        </table>

                        <div class="footer-stamp">
                            System Verified & Secured by: <b>Patil Infratech NeevPay Protocol</b> • Generated on {get_ist_time().strftime('%d-%m-%Y %H:%M:%S')}
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            st.components.v1.html(neevpay_html_doc, height=520, scrolling=True)

            st.write("---")
            np_c1, np_c2, np_c3, np_c4 = st.columns(4)

            with np_c1:
                st.download_button(
                    label="Download Master HTML",
                    data=neevpay_html_doc,
                    file_name=f"NeevPay_Master_Invoice_{st.session_state.current_site_name.replace(' ', '_')}.html",
                    mime="text/html",
                    type="primary",
                    use_container_width=True,
                )

            with np_c2:
                neev_export_data = []
                for m_item in milestones:
                    neev_export_data.append({
                        "Site": st.session_state.current_site_name,
                        "Client Email": client_email,
                        "Stage": m_item["stage_name"],
                        "Planned Bill (Rs)": m_item["planned_amount"],
                        "Deposited (Rs)": m_item["amount_deposited"],
                        "Balance (Rs)": max(0.0, m_item["planned_amount"] - m_item["amount_deposited"]),
                        "Progress %": f"{(m_item['amount_deposited']/m_item['planned_amount']*100):.1f}%" if m_item["planned_amount"] > 0 else "0%",
                        "Status": m_item["status"],
                        "Locked": "Yes" if m_item.get("is_locked") == 1 else "No",
                        "Completion Date": m_item.get("completion_date") or "-"
                    })
                neev_csv = pd.DataFrame(neev_export_data).to_csv(index=False).encode('utf-8-sig')

                st.download_button(
                    label="Export CSV Data",
                    data=neev_csv,
                    file_name=f"NeevPay_Escrow_{st.session_state.current_site_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with np_c3:
                st.markdown(
                    """
                    <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 10px 14px; border-radius: 8px; font-weight: bold; cursor: pointer; height: 38px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                        Instant Print (A4)
                    </button>
                    """,
                    unsafe_allow_html=True,
                )

            with np_c4:
                # इंजिनिअर स्वतः क्लिक करून क्लायंटला अधिकृत ईमेल पाठवेल
                if st.button("Email Invoice to Client", key="btn_send_client_invoice_mail", use_container_width=True):
                    if client_email:
                        mail_subj = f"Official Escrow Statement: {st.session_state.current_site_name}"
                        mail_body = f"""
नमस्कार,

तुमच्या '{st.session_state.current_site_name}' या साईटचे अद्ययावत NeevPay Escrow पेमेंट स्टेटमेंट खालीलप्रमाणे आहे:

एकूण ठरलेले बजेट: Rs. {total_budget:,.2f}
आतापर्यंत प्राप्त रक्कम: Rs. {total_received:,.2f}
शिल्लक उर्वरित बाकी: Rs. {total_pending:,.2f}
एकूण साईट प्रगती: {overall_site_pct:.1f}% ({locked_stages}/{len(milestones)} टप्पे पूर्ण)
साईट इंजिनिअर: {current_user_name}
दिनांक: {get_ist_time().strftime('%d-%m-%Y')}

अधिक माहितीसाठी साईट इंजिनिअरशी संपर्क साधावा.

- Patil Infratech Team
                        """
                        ok_mail = send_email_message(client_email, mail_subj, mail_body)
                        if ok_mail:
                            st.success(f"अधिकृत इनव्हॉइस '{client_email}' वर पाठवले!")
                        else:
                            st.error("ईमेल पाठवण्यात त्रुटी आली. कृपया क्रेडेन्शियल्स तपासा.")
                    else:
                        st.warning("कृपया आधी क्लायंटचा ईमेल आयडी सेव्ह करा.")

            np_wa_text = (
                f"*PATIL INFRATECH - NEEVPAY MASTER ESCROW STATEMENT*\n"
                f"*Site:* {st.session_state.current_site_name}\n"
                f"*Engineer:* {current_user_name}\n"
                f"*Client Email:* {client_email or 'N/A'}\n"
                f"*Date:* {get_ist_time().strftime('%d-%m-%Y')}\n\n"
                f"*Total Planned Bill:* Rs. {total_budget:,.2f}\n"
                f"*Total Deposited:* Rs. {total_received:,.2f}\n"
                f"*Pending Balance:* Rs. {total_pending:,.2f}\n"
                f"*Overall Progress:* {overall_site_pct:.1f}% ({locked_stages}/{len(milestones)} टप्पे पूर्ण)\n\n"
                f"_Smart Escrow Master Statement Generated._"
            )
            st.write(" ")
            render_whatsapp_feature(urllib.parse.quote(np_wa_text), "neevpay_master_wa")

    st.write("---")

    # ==========================================================
    # ४. तयार केलेले टप्पे, पेमेंट व डिजिटल पडताळणी यादी
    # ==========================================================
    if not milestones:
        st.info("या साईटवर अजून कोणतेही कामाचे बिल तयार केलेले नाही. कृपया वरील बॉक्समधून कामाचा टप्पा जोडा.")
    else:
        st.markdown("##### कामाचे टप्पे, ठरलेले बिल, पेमेंट व डिजिटल पडताळणी:")

        for m in milestones:
            m_id = m["id"]
            st_name = m["stage_name"]
            p_amt = float(m["planned_amount"])
            d_amt = float(m["amount_deposited"])
            status = m["status"]
            eng_app = bool(m["engineer_approved"])
            cli_app = bool(m["client_approved"])
            is_locked = bool(m.get("is_locked", 0))
            rem_balance = max(0.0, p_amt - d_amt)
            curr_stage_pct = (d_amt / p_amt * 100) if p_amt > 0 else 0.0

            # स्टेटस बॅज
            if is_locked:
                lock_badge = "LOCKED (पूर्ण पेड व पडताळणी पूर्ण)"
            elif p_amt == 0:
                lock_badge = "BILL NOT SET"
            elif d_amt >= p_amt and p_amt > 0:
                lock_badge = "READY TO LOCK (100% Paid)"
            elif d_amt > 0:
                lock_badge = f"PARTIAL ({curr_stage_pct:.1f}%)"
            else:
                lock_badge = "UNPAID"

            with st.expander(
                f"{st_name} | {lock_badge} | ठरलेले बिल: Rs. {p_amt:,.2f} (जमा: Rs. {d_amt:,.2f})",
                expanded=not is_locked,
            ):
                if is_locked:
                    st.success(
                        f"हा टप्पा १००% पूर्ण भरला असून सुरक्षितपणे लॉक केला आहे.\n\n"
                        f"• पूर्ण झाल्याची तारीख: `{m.get('completion_date', 'N/A')}`\n"
                        f"• एकूण भरलेली रक्कम: Rs. {d_amt:,.2f} (100% Complete)\n"
                        f"• शेरा: यात आता कोणतेही बदल करता येणार नाहीत."
                    )
                else:
                    col_b1, col_b2 = st.columns([2.5, 2.5])

                    with col_b1:
                        st.markdown("###### टप्प्याचे बिल तपशील (Fixed):")
                        st.markdown(
                            f"**कामाचे ठरलेले बिल:** <span style='color:#38bdf8; font-weight:bold; font-size:16px;'>Rs. {p_amt:,.2f}</span>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"**आतापर्यंत मिळालेली रक्कम:** <span style='color:#10b981; font-weight:bold; font-size:16px;'>Rs. {d_amt:,.2f} ({curr_stage_pct:.1f}%)</span>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"**उर्वरित बाकी (Balance):** <span style='color:#ef4444; font-weight:bold; font-size:16px;'>Rs. {rem_balance:,.2f}</span>",
                            unsafe_allow_html=True,
                        )

                        # बिल बदलण्यासाठी थेट संमती पर्याय
                        with st.expander("ठरलेले बिल बदलायचे आहे का?"):
                            new_change_amt = st.number_input(
                                "नवीन सुधारीत बिल रक्कम (Rs.):",
                                min_value=max(1.0, float(d_amt)),
                                value=float(p_amt),
                                step=1000.0,
                                key=f"new_change_amt_{m_id}",
                            )

                            if st.button("नवीन बिल अपडेट करा", key=f"btn_update_bill_{m_id}", type="primary"):
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute(
                                    "UPDATE site_milestone_payments SET planned_amount = ? WHERE id = ?",
                                    (new_change_amt, m_id),
                                )
                                conn.commit()
                                conn.close()
                                st.success("नवीन बिल अपडेट झाले!")
                                st.rerun()

                        # ==========================================================
                        # पेमेंट जमा करण्याची नोंद
                        # ==========================================================
                        if p_amt > 0.0 and rem_balance > 0:
                            st.write("---")
                            if eng_app and cli_app:
                                st.caption("क्लायंटने दिलेले पैसे इथे भरा:")
                                add_pay = st.number_input(
                                    f"पैसे ॲड करा (जास्तीत जास्त Rs. {rem_balance:,.2f}):",
                                    min_value=0.0,
                                    max_value=float(rem_balance),
                                    value=float(rem_balance),
                                    step=100.0,
                                    key=f"pay_in_{m_id}",
                                )
                                if st.button("पैसे जमा नोंदवा", key=f"btn_pay_{m_id}", type="primary"):
                                    if add_pay > 0:
                                        new_total_dep = d_amt + add_pay
                                        new_st = (
                                            "Payment Completed"
                                            if new_total_dep >= p_amt
                                            else "Partially Paid"
                                        )
                                        conn = get_db_connection()
                                        cursor = conn.cursor()
                                        cursor.execute(
                                            "UPDATE site_milestone_payments SET amount_deposited = ?, status = ? WHERE id = ?",
                                            (new_total_dep, new_st, m_id),
                                        )
                                        conn.commit()
                                        conn.close()
                                        st.success(f"Rs. {add_pay:,.2f} ची पेमेंट नोंद यशस्वी झाली!")
                                        st.rerun()
                            else:
                                st.info("पेमेंट नोंदणीसाठी: उजव्या बाजूला इंजिनिअर व क्लायंट या दोघांचे पडताळणी स्टेटस पूर्ण करून सेव्ह करा.")

                    # डिजिटल पडताळणी व टप्पा लॉक करणे
                    with col_b2:
                        st.markdown("###### काम व पेमेंट पडताळणी (Approval)")

                        eng_check = st.checkbox(
                            "इंजिनिअर: काम समाधानकारक पूर्ण झाले आहे",
                            value=eng_app,
                            key=f"chk_eng_{m_id}",
                        )
                        cli_check = st.checkbox(
                            "क्लायंट: काम व पेमेंट तपासले असून सहमत आहे",
                            value=cli_app,
                            key=f"chk_cli_{m_id}",
                        )

                        # पडताळणी स्टेटस अपडेट करणे
                        if eng_check != eng_app or cli_check != cli_app:
                            if st.button("पडताळणी स्टेटस सेव्ह करा", key=f"btn_save_app_{m_id}"):
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute(
                                    "UPDATE site_milestone_payments SET engineer_approved = ?, client_approved = ? WHERE id = ?",
                                    (int(eng_check), int(cli_check), m_id),
                                )
                                conn.commit()
                                conn.close()
                                st.success("पडताळणी अपडेट झाली!")
                                st.rerun()

                        # फायनल लॉक करणे (ईमेल पाठवण्याशिवाय - साधे व जलद)
                        if p_amt > 0 and d_amt >= p_amt:
                            if eng_check and cli_check:
                                st.write("---")
                                st.info("१००% पेमेंट पूर्ण झाले असून दोन्ही पडताळणी पूर्ण आहेत.")
                                if st.button(
                                    "हा टप्पा अंतिम लॉक करा (Lock Milestone)",
                                    key=f"btn_lock_{m_id}",
                                    type="primary",
                                ):
                                    today_str = get_ist_time().strftime("%d-%m-%Y %H:%M")
                                    conn = get_db_connection()
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        """
                                        UPDATE site_milestone_payments 
                                        SET is_locked = 1, status = 'Fully Completed & Locked', completion_date = ? 
                                        WHERE id = ?
                                        """,
                                        (today_str, m_id),
                                    )
                                    conn.commit()
                                    conn.close()
                                    st.success(f"'{st_name}' यशस्वीरित्या लॉक झाला!")
                                    st.rerun()
                            else:
                                st.warning("टप्पा लॉक करण्यासाठी वरील दोन्ही पडताळणी चेकबॉक्स टिक असणे गरजेचे आहे.")
                        else:
                            st.caption("१००% पेमेंट जमा झाल्यावरच हा टप्पा फायनल लॉक करता येईल.")

                        # टप्पा डिलीट करण्याचा पर्याय (फक्त जमा रक्कम नसतानाच उपलब्ध)
                        st.write("---")
                        if d_amt > 0:
                            st.caption(f"या टप्प्यावर Rs. {d_amt:,.2f} जमा असल्याने सुरक्षिततेसाठी हा टप्पा डिलीट करता येणार नाही.")
                        else:
                            if st.button("हा टप्पा डिलीट करा", key=f"btn_del_stage_{m_id}"):
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM site_milestone_payments WHERE id = ?", (m_id,))
                                conn.commit()
                                conn.close()
                                st.warning(f"'{st_name}' टप्पा डिलीट केला!")
                                st.rerun()
