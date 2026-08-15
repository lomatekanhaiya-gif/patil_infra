# ==============================================================================
# 📦 PATIL INFRATECH - CIVIL ENGINEERING SUITE & SITE MANAGEMENT SYSTEM
# ==============================================================================
# Concept & Logic: Kanhaiya (Founder of Patil Infratech)
# Architecture: Streamlit Web UI + SQLite3 + Gemini GenAI SDK
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
# 📌 विभाग ४: युटिलिटी आणि सपोर्ट फंक्शन्स (वेळ, ईमेल, पासवर्ड)
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
  """पासवर्ड सुरक्षितता तपासणी"""
  if len(password) < 8:
    return False, "पासवर्ड कमीत कमी ८ अक्षरांचा असावा."
  if not re.search(r"\d", password):
    return False, "पासवर्डमध्ये कमीत कमी एक नंबर (0-9) असावा."
  if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    return False, "पासवर्डमध्ये कमीत कमी एक विशेष चिन्ह (!@#$%^&*) असावे."
  return True, "Strong"


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

  # १. युझर्स टेबल (Users Table)
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

  # २. हिस्ट्री टेबल (History Table)
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

  # ३. प्रिमियम कोड्स टेबल (Premium Codes Table)
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

  # ४. फिचर लॉक्स टेबल (Feature Locks Table)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS feature_locks (
            feature_name TEXT PRIMARY KEY,
            access_level TEXT
        )
    """)

  # ५. मास्टर मार्केट दर टेबल (Master Market Rates Table)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_rates (
            material TEXT PRIMARY KEY,
            rate REAL
        )
    """)

  # ६. जाहिरात व स्पॉन्सर टेबल (Ads Table)
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

  # ७. साईट हजेरी व मजुरी टेबल (Daily Attendance Table)
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
            total_cost REAL DEFAULT 0.0,
            site_name TEXT DEFAULT 'Default Site'
        )
    """)

  # सुरक्षित डेटाबेस अपग्रेड
  new_labour_cols = [
      ("supervisor", "INTEGER DEFAULT 0"),
      ("supervisor_rate", "REAL DEFAULT 0.0"),
      ("carpenter", "INTEGER DEFAULT 0"),
      ("carpenter_rate", "REAL DEFAULT 0.0"),
      ("plumber", "INTEGER DEFAULT 0"),
      ("plumber_rate", "REAL DEFAULT 0.0"),
      ("electrician", "INTEGER DEFAULT 0"),
      ("electrician_rate", "REAL DEFAULT 0.0"),
      ("painter", "INTEGER DEFAULT 0"),
      ("painter_rate", "REAL DEFAULT 0.0"),
  ]
  for col_name, col_type in new_labour_cols:
    try:
      cursor.execute(
          f"ALTER TABLE site_attendance ADD COLUMN {col_name} {col_type}"
      )
    except sqlite3.OperationalError:
      pass

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

  # मास्टर ॲडमीन डि default नोंद
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
            (
                "स्वागत आहे मास्टर कन्हैया! आपले पाटील इन्फ्राटेक मध्ये सर्व"
                " अधिकार अनलॉक्ड आहेत ⚡"
            ),
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
  }
  for f_name, f_lvl in default_locks.items():
    cursor.execute(
        "INSERT OR IGNORE INTO feature_locks (feature_name, access_level)"
        " VALUES (?, ?)",
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

  # सर्व मुख्य टेबल्समध्ये site_name सुरक्षितपणे तपासणे
  tables_to_update = [
      "history",
      "site_attendance",
      "site_inventory",
      "site_progress",
      "pre_concreting_checklist",
  ]
  for tbl in tables_to_update:
    try:
      cursor.execute(
          f"ALTER TABLE {tbl} ADD COLUMN site_name TEXT DEFAULT 'Default Site'"
      )
    except sqlite3.OperationalError:
      pass

  conn.commit()
  conn.close()


init_db()

# ==========================================
# 📌 विभाग ६: डेटाबेस क्वेरी हेल्पर फंक्शन्स
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

# आवश्यक स्टेट्स इनिशियलाईज करणे
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
    ("current_site_name", "साई रेसिडेन्सी - साईट १"),
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
              "UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE"
              " user_key = ?",
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
    with st.expander("🔒 WhatsApp Report Sharing - Unlock Premium"):
      st.warning(
          "⚠️ व्हॉट्सॲपवर पूर्ण रिपोर्ट शेअर करण्याचे फीचर प्रिमियम"
          " युझर्ससाठी आहे."
      )
      st.caption(
          "💡 अनलॉक करण्यासाठी Admin कडून आलेला प्रिमियम कोड खाली टाका:"
      )

      p_code = st.text_input(
          "Enter Activation Code:", key=f"{key_prefix}_code_input"
      ).strip()

      w_col1, w_col2 = st.columns(2)
      with w_col1:
        if st.button(
            "🔓 Unlock WhatsApp Share Now", key=f"{key_prefix}_unlock_btn"
        ):
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "SELECT * FROM premium_codes WHERE code = ?", (p_code,)
          )
          row = cursor.fetchone()

          if row:
            c_info = dict(row)
            if c_info.get("used") == 1:
              st.error(
                  "❌ हा कोड आधीच वापरला गेला आहे! तो आता व्हॅलिड नाही."
              )
              conn.close()
            else:
              exp_datetime = get_ist_time() + datetime.timedelta(days=28)
              exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
              now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

              cursor.execute(
                  "UPDATE premium_codes SET used = 1, used_by = ?, used_date ="
                  " ? WHERE code = ?",
                  (current_user_name, now_str, p_code),
              )

              disp_name = current_user_name if current_user_name else ""
              welcome_msg = (
                  f"{disp_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले"
                  " हार्दिक स्वागत आहे🥳"
              )

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
        if st.button(
            "📩 Request Code from Admin", key=f"{key_prefix}_req_btn"
        ):
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
# 📌 विभाग १०: वेलकम स्क्रीन ॲनिमेशन (3D Cosmic Loader)
# ==========================================
welcome_placeholder = st.empty()

if "welcome_completed" not in st.session_state:
  st.session_state.welcome_completed = False

if not st.session_state.welcome_completed:
  with welcome_placeholder.container():
    st.markdown(
        "<br><div class='galaxy-loader'></div>", unsafe_allow_html=True
    )
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
        "SELECT * FROM ads WHERE active = 1 AND position = 'Loading Page (Title"
        " Sponsor)'"
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
          f"<p style='text-align: center; font-size: 18px; font-weight: bold;"
          f" color: #f8fafc;'>{construction_stages[i]}</p>",
          unsafe_allow_html=True,
      )
      progress_bar.progress((i + 1) * 20)
      time.sleep(0.4)

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

    adm_cem = st.number_input(
        "Cement (per bag ₹):",
        min_value=0.0,
        value=float(m_rates.get("cement", 400.0)),
        step=1.0,
    )
    adm_snd = st.number_input(
        "Sand (per m³ ₹):",
        min_value=0.0,
        value=float(m_rates.get("sand", 2500.0)),
        step=1.0,
    )
    adm_brk = st.number_input(
        "Brick (per nos ₹):",
        min_value=0.0,
        value=float(m_rates.get("bricks", 8.0)),
        step=0.1,
    )
    adm_agg = st.number_input(
        "Aggregate (per m³ ₹):",
        min_value=0.0,
        value=float(m_rates.get("aggregate", 2200.0)),
        step=1.0,
    )
    adm_ste = st.number_input(
        "Steel Rate (per kg ₹):",
        min_value=0.0,
        value=float(m_rates.get("steel", 60.0)),
        step=1.0,
    )

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
      st.success(
          "✅ आजचे मास्टर मार्केट दर डेटाबेसमध्ये यशस्वीरित्या अपडेट"
          " झाले!"
      )

  elif current_tab == "locks":
    st.markdown("### ⚙️ Feature Lock Manager")
    cur_locks = get_feature_locks()

    fl_calc = st.selectbox(
        "Civil Calculator Access:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("Civil Calculator", "Free") == "Free" else 1,
    )
    fl_ra = st.selectbox(
        "Rate Analysis Module Access:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("Rate Analysis", "Free") == "Free" else 1,
    )
    fl_bbs = st.selectbox(
        "BBS Calculator Access:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("BBS", "Free") == "Free" else 1,
    )
    fl_qs = st.selectbox(
        "Quantity Surveying Access:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("Quantity Surveying", "Free") == "Free" else 1,
    )
    fl_site = st.selectbox(
        "Site Manager Access:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("Site Manager", "Free") == "Free" else 1,
    )
    fl_wa = st.selectbox(
        "WhatsApp Full Report Share:",
        ["Free", "Premium"],
        index=0 if cur_locks.get("WhatsApp Share", "Free") == "Free" else 1,
    )
    fl_ai = st.selectbox(
        "Civil AI Assistant Access:",
        ["Free", "Premium"],
        index=0
        if cur_locks.get("Civil AI Assistant", "Premium") == "Free"
        else 1,
    )

    if st.button("💾 Save Feature Lock Settings", type="primary"):
      conn = get_db_connection()
      cursor = conn.cursor()
      new_locks = {
          "Civil Calculator": fl_calc,
          "Rate Analysis": fl_ra,
          "BBS": fl_bbs,
          "Quantity Surveying": fl_qs,
          "Site Manager": fl_site,
          "WhatsApp Share": fl_wa,
          "Civil AI Assistant": fl_ai,
      }
      for f_name, f_lvl in new_locks.items():
        cursor.execute(
            "REPLACE INTO feature_locks (feature_name, access_level) VALUES (?,"
            " ?)",
            (f_name, f_lvl),
        )
      conn.commit()
      conn.close()
      st.success("✅ प्रिमियम/फ्री फीचर्स सेटिंग्स यशस्वीरित्या बदलल्या!")

  elif current_tab == "users":
    st.markdown("### 📋 User Database Master List")

    if (
        st.session_state.admin_view == "user_detail"
        and st.session_state.admin_selected_user is not None
    ):
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

      st.markdown(
          f"#### 👤 MANAGE USER: <span style='color:#ec38bc;'>{u_name.upper()}</span>",
          unsafe_allow_html=True,
      )
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
        if st.button(
            f"🚀 Generate & Send Unique Code to {u_name}",
            key=f"win_gen_send_{target_user}",
        ):
          new_c = generate_random_code()
          now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO premium_codes (code, assigned_to, used, created_at)"
              " VALUES (?, ?, 0, ?)",
              (new_c, u_name, now_str),
          )
          msg = (
              f"तुमचा प्रिमियम कोड: {new_c} (ॲपमध्ये टाकून प्रिमियम अनलॉक"
              " करा)"
          )
          cursor.execute(
              "UPDATE users SET admin_message = ?, requested_code = 0 WHERE"
              " user_key = ?",
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
        time_val = st.number_input(
            "संख्या (Value):",
            min_value=1,
            value=28,
            key=f"win_t_val_{target_user}",
        )
      with t_col2:
        time_unit = st.selectbox(
            "युनिट (Unit):",
            ["Minutes", "Hours", "Days"],
            index=2,
            key=f"win_t_unit_{target_user}",
        )

      if st.button(
          f"⚡ Set Premium Time ({time_val} {time_unit})",
          key=f"win_btn_custom_{target_user}",
      ):
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
        if st.button(
            f"🔻 Revoke Premium: {u_name}", key=f"win_rev_{target_user}"
        ):
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE users SET is_premium = 0, premium_expiry = NULL WHERE"
              " user_key = ?",
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
      if st.button(
          f"✉️ मेसेज सेव्ह करा व पाठवा ({u_name})",
          key=f"win_btn_msg_{target_user}",
      ):
        if new_msg.strip():
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "UPDATE users SET admin_message = ?, unread_notification = 1"
              " WHERE user_key = ?",
              (new_msg.strip(), target_user),
          )
          conn.commit()
          conn.close()
          st.success(
              f"✅ '{u_name}' च्या इनबॉक्समध्ये नवीन मेसेज पाठवला"
              " (Notification Sent)!"
          )
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
      st.markdown(
          f"##### 📜 {u_name} चे जनरेट केलेले एस्टिमेशन रिपोर्ट्स"
          f" ({len(u_hist)})"
      )
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
                f"<span class='gold-vip-badge'>👑 VIP: {u_name.upper()}</span>"
                f" (User ID: <code>{u_uid}</code>)<br><small style='color:"
                f" {'#10b981' if is_online else '#ef4444'}; font-weight:"
                f" bold;'>Status: {status_indicator}</small>",
                unsafe_allow_html=True,
            )
          elif is_req:
            col_u1.markdown(
                f"#### 👤 **{u_name}** `[🚨 CODE]` (User ID:"
                f" `{u_uid}`)<br><small style='color:"
                f" {'#10b981' if is_online else '#ef4444'}; font-weight:"
                f" bold;'>Status: {status_indicator}</small>",
                unsafe_allow_html=True,
            )
          else:
            col_u1.markdown(
                f"<span class='free-user-badge'>🆓 FREE:"
                f" {u_name.upper()}</span> (User ID: <code>{u_uid}</code>)<br><small"
                f" style='color: {'#10b981' if is_online else '#ef4444'};"
                f" font-weight: bold;'>Status: {status_indicator}</small>",
                unsafe_allow_html=True,
            )

          if col_u2.button(
              "👁️ View / Manage", key=f"open_user_win_{mob}"
          ):
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
      media_type = st.selectbox(
          "Media Type:", ["Photo (PNG/JPG)", "Video Ad"]
      )
      media_url = st.text_input("Media Direct URL (Image/Video Link):")
      position = st.selectbox("Display Position:", [
          "Loading Page (Title Sponsor)",
          "Main App Header (Top Banner)",
      ])
      is_active = st.checkbox("Make Active / Live", value=True)

      submit_ad = st.form_submit_button(
          "🚀 Publish Ad Sponsor", type="primary"
      )
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
        st.info(
            f"**#{ad_id} | {ad.get('title')}** ({ad.get('position')})\n-"
            f" *Status:* {'🟢 Active' if ad.get('active')==1 else '🔴 Inactive'}"
        )
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
      submit_broadcast = st.form_submit_button(
          "🚀 Send to All Users (Broadcast)", type="primary"
      )

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
          st.success(
              "🎉 ब्रॉडकास्ट मेसेज सर्व युझर्सना यशस्वीरित्या पाठवला गेला"
              " आहे!"
          )
        else:
          st.warning("⚠️ कृपया पाठवण्यासाठी काहीतरी मेसेज लिहा!")

  st.stop()

# ==========================================
# 📌 विभाग १२: युझर ऑथेंटिकेशन (Email / Password / OTP Login)
# ==========================================
if st.session_state.app_user_name is None:
  st.markdown("### 🏗️ PATIL INFRATECH - SECURE LOGIN")

  login_tab, otp_tab = st.tabs([
      "🔑 Registered User Login",
      "📧 Email OTP Register / Verification",
  ])

  # १. Registered User Login
  with login_tab:
    with st.form("direct_login_form"):
      login_email = st.text_input(
          "ईमेल किंवा Username (Email ID / Username):"
      ).strip()
      login_pass = st.text_input(
          "पासवर्ड (Password):", type="password"
      ).strip()
      submit_direct = st.form_submit_button("🚀 Login Now", type="primary")

      if submit_direct:
        if login_email and login_pass:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "SELECT user_key FROM users WHERE (email = ? OR uid = ? OR"
              " user_key = ?) AND pin = ?",
              (login_email, login_email, login_email, login_pass),
          )
          row = cursor.fetchone()
          conn.close()

          if row:
            found_user = row["user_key"]
            st.session_state.app_user_name = found_user
            st.query_params["saved_user"] = found_user

            st.markdown(
                f"""
                            <script>
                                localStorage.setItem("patil_app_user", "{found_user}");
                            </script>
                        """,
                unsafe_allow_html=True,
            )

            st.success(
                "🎉 यशस्वीरित्या लॉगिन झाले! (तुमचे सेशन या डिव्हाइसवर"
                " सेव्ह केले आहे)"
            )
            st.rerun()
          else:
            st.error("❌ चुकीचा ईमेल/Username किंवा पासवर्ड! कृपया तपासा.")
        else:
          st.warning("⚠️ कृपया ईमेल/Username आणि पासवर्ड दोन्ही भरा.")

  # २. Email OTP Registration & Setup
  with otp_tab:
    st.markdown("#### 📧 Email OTP Verification & Account Creation")
    email_input = st.text_input(
        "तुमचा ईमेल आयडी टाका (Email ID):", key="otp_email_key"
    ).strip()

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
              st.success(
                  "✅ तुमच्या ईमेलवर 6 अंकी OTP पाठवला आहे! खाली टाका."
              )
            else:
              st.error(
                  "❌ ईमेल पाठवताना एरर आली. (SMTP क्रेडेन्शियल्स तपासा)"
              )
        else:
          st.warning("⚠️ कृपया वैध ईमेल आयडी टाका!")

      if st.session_state.generated_otp:
        entered_otp = st.text_input(
            "6 अंकी OTP टाका:", max_chars=6
        ).strip()
        if st.button("🔐 Verify OTP"):
          if entered_otp == st.session_state.generated_otp:
            st.session_state.otp_verified = True
            st.success("✅ OTP यशस्वीरित्या व्हेरिफाय झाला आहे!")
            st.rerun()
          else:
            st.error("❌ चुकीचा OTP! कृपया पुन्हा प्रयत्न करा.")

    # जर OTP पडताळणी पूर्ण झाली असेल तर
    if st.session_state.otp_verified and st.session_state.pending_email:
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(
          "SELECT * FROM users WHERE email = ?",
          (st.session_state.pending_email,),
      )
      row = cursor.fetchone()
      conn.close()

      if row:
        user_data = dict(row)
        found_user = user_data["user_key"]
        st.session_state.app_user_name = found_user
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
        st.info(
            "✨ नवीन युझर! कृपया खालील माहिती भरून युझरनेम आणि मजबूत पासवर्ड"
            " सेट करा:"
        )
        with st.form("custom_reg_form"):
          custom_username = st.text_input(
              "तुमचे नाव किंवा युनिक Username बनावा:"
          ).strip()
          custom_password = st.text_input(
              "मजबूत पासवर्ड (Set Strong Password):",
              type="password",
              help=(
                  "कमीत कमी ८ अक्षरे, १ अंक आणि १ विशेष चिन्ह (!@#$%) असणे"
                  " आवश्यक आहे."
              ),
          ).strip()
          confirm_password = st.text_input(
              "पासवर्ड पुन्हा टाका (Confirm Password):", type="password"
          ).strip()

          submit_custom_reg = st.form_submit_button(
              "🚀 Complete Registration & Create Account", type="primary"
          )

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
                    st.error(
                        "❌ हा Username आधीच वापरला गेला आहे, कृपया दुसरा"
                        " टाका!"
                    )
                  else:
                    welcome_msg = (
                        f"{custom_username} मी कन्हैया आपले पाटील इन्फ्राटेक"
                        " मध्ये आपले हार्दिक स्वागत आहे🥳"
                    )
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

                    subject = (
                        "PATIL INFRATECH - Account Created Successfully!"
                    )
                    body = (
                        f"नमस्कार {custom_username}!\n\nपाटील इन्फ्राटेक मध्ये"
                        " तुमचे अकाउंट यशस्वीरित्या तयार झाले आहे.\n\nतुमचा"
                        f" लॉगिन तपशील:\nUsername: {custom_username}\nPassword:"
                        f" {custom_password}\nRegistered Email:"
                        f" {st.session_state.pending_email}\n\nतुम्ही पुढील"
                        " वेळी ईमेल/युझरनेम आणि पासवर्ड वापरून लॉगिन करू"
                        " शकता.\n\n- Kanhaiya (Founder of Patil Infratech)"
                    )
                    send_email_message(
                        st.session_state.pending_email, subject, body
                    )

                    st.session_state.app_user_name = custom_username
                    st.query_params["saved_user"] = custom_username

                    st.markdown(
                        f"""
                                            <script>
                                                localStorage.setItem("patil_app_user", "{custom_username}");
                                            </script>
                                        """,
                        unsafe_allow_html=True,
                    )

                    st.success(
                        "🎉 अकाउंट यशस्वीरित्या तयार झाले! डिटेल्स ईमेलवर"
                        " पाठवले आहेत."
                    )
                    time.sleep(1)
                    st.rerun()
            else:
              st.warning("⚠️ कृपया सर्व माहिती भरा!")

  st.write("---")

  # ॲडमीन लॉगिन एक्सपँडर
  with st.expander("🛡️ Admin Login Panel"):
    with st.form("admin_login_form"):
      admin_id = st.text_input("Admin ID:")
      admin_pass = st.text_input("Password:", type="password")
      submit_admin = st.form_submit_button(
          "🔓 Login to Admin Panel", type="primary"
      )

      secret_admin_id = (
          st.secrets.get("ADMIN_ID", "kanha_1p")
          if hasattr(st, "secrets")
          else "kanha_1p"
      )
      secret_admin_pass = (
          st.secrets.get("ADMIN_PASS", "@Dellg15")
          if hasattr(st, "secrets")
          else "@Dellg15"
      )

      if submit_admin:
        if admin_id == secret_admin_id and admin_pass == secret_admin_pass:
          st.session_state.is_admin_logged = True
          st.rerun()
        else:
          st.error("❌ चुकीचा Admin ID किंवा Password!")

  st.stop()

# ==========================================
# 📌 विभाग १३: मुख्य युझर डॅशबोर्ड (Top Header, Ads, Notifications)
# ==========================================
current_user_name = st.session_state.app_user_name
is_user_premium, status_text_str = check_user_premium_status(current_user_name)

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "SELECT * FROM ads WHERE active = 1 AND position = 'Main App Header (Top"
    " Banner)'"
)
ads_list = [dict(r) for r in cursor.fetchall()]
conn.close()

for ad in ads_list:
  st.markdown(
      f"""
        <div style="background: #111827; border: 1px solid rgba(0, 242, 254, 0.3); padding: 8px 12px; border-radius: 12px; text-align: center; margin-bottom: 18px;">
            <span style="font-size: 9px; color: #38bdf8; font-weight: bold;">📢 SPONSOR AD</span><br>
            <b style="color: #fff; font-size: 13px;">{ad.get('title')}</b> — <span style="color: #cbd5e1; font-size: 11px;">{ad.get('desc')}</span>
            {"<img src='" + ad.get('media_url') + "' style='max-height:50px; border-radius:6px; margin-top:3px;'/>" if ad.get('media_type') == 'Photo (PNG/JPG)' and ad.get('media_url') else ""}
            <a href="{ad.get('link')}" target="_blank" style="color: #f59e0b; font-weight: bold; text-decoration: underline; font-size: 11px; margin-left: 6px;">[Visit]</a>
        </div>
    """,
      unsafe_allow_html=True,
  )

col_u, col_lo = st.columns([3.5, 1.5])
if is_user_premium:
  col_u.markdown(
      f"<span class='gold-vip-badge'>👑 VIP MEMBER: {current_user_name.upper()}"
      f" ({status_text_str})</span>",
      unsafe_allow_html=True,
  )
else:
  col_u.markdown(
      f"<span class='free-user-badge'>🆓 FREE USER:"
      f" {current_user_name.upper()}</span>",
      unsafe_allow_html=True,
  )

# १३.१ ॲक्टिव्ह साईट सिलेक्टर बार (Active Site Switcher)
with st.container():
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-left: 5px solid #f59e0b; padding: 12px 18px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(245,158,11,0.3);">
            <span style="color:#94a3b8; font-size:11px; font-weight:bold;">📍 चालू प्रोजेक्ट / साईट:</span><br>
            <b style="color:#f59e0b; font-size:17px;">🏗️ """
      + str(st.session_state.current_site_name)
      + """</b>
        </div>
    """,
      unsafe_allow_html=True,
  )

  with st.popover("✏️ साईटचे नाव बदला"):
    new_site_input = st.text_input(
        "नवीन साईटचे नाव टाका:", value=st.session_state.current_site_name
    )
    if st.button("💾 सेव्ह करा", key="btn_save_site_name", type="primary"):
      if new_site_input.strip():
        st.session_state.current_site_name = new_site_input.strip()
        st.success("✅ साईट अपडेट झाली!")
        st.rerun()

if col_lo.button("🔄 Logout"):
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

current_user_data = get_user_data(current_user_name) or {}
disp_name_inbox = current_user_name if current_user_name else ""

if current_user_data.get("unread_notification") == 1:
  admin_msg = current_user_data.get("admin_message", "")
  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #047857 0%, #065f46 100%); padding: 18px 22px; border-radius: 18px; margin-bottom: 18px; border: 1px solid #34d399; box-shadow: 0 6px 22px rgba(52, 211, 153, 0.35);">
            <h4 style="color: #6ee7b7; margin: 0 0 6px 0;">🔔 नवीन नोटिफिकेशन</h4>
            <p style="color: #ffffff; font-size: 16px; margin: 0;">{admin_msg}</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  if st.button("✅ Mark as Read & Clear (वाचले आहे)", type="primary"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET unread_notification = 0, admin_message = ? WHERE"
        " user_key = ?",
        (
            f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले"
            " हार्दिक स्वागत आहे🥳",
            current_user_name,
        ),
    )
    conn.commit()
    conn.close()
    st.success("✅ मेसेज वाचून क्लियर केला आहे!")
    st.rerun()
else:
  admin_msg = current_user_data.get(
      "admin_message",
      f"{disp_name_inbox} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये आपले हार्दिक"
      " स्वागत आहे🥳",
  )
  st.markdown("### 📥 Admin Message / Code Inbox")
  st.info(f"📢 **Admin:** {admin_msg}")

st.write("---")

# प्रिमियम अनलॉक बॉक्स (फ्री युझर्ससाठी)
if not is_user_premium:
  with st.expander("🔑 प्रिमियम अनलॉक करा (Enter Premium Code)"):
    input_code = st.text_input(
        "Enter Code (e.g. PATIL-XXXXX):", key="home_code_input"
    ).strip()
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
      if st.button("🔓 Activate Premium", type="primary"):
        u_info = get_user_data(current_user_name) or {}

        if input_code == "4528":
          uses_count = u_info.get("master_code_uses", 0)
          if uses_count >= 3:
            st.error(
                "❌ हा मास्टर कोड तुम्ही आधीच ३ वेळा वापरला आहे! मर्यादा"
                " संपली आहे."
            )
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
                    "🎉 मास्टर कोड 4528 द्वारे तुला ८ तासांचे प्रिमियम मिळाले आहे!"
                    f" (वापर: {uses_count + 1}/3)",
                    current_user_name,
                ),
            )
            conn.commit()
            conn.close()
            st.success("🎉 मास्टर कोड द्वारे ८ तासांचे प्रिमियम अनलॉक झाले!")
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
                  f"{current_user_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये"
                  " आपले हार्दिक स्वागत आहे🥳",
                  current_user_name,
              ),
          )
          conn.commit()
          conn.close()
          st.success("🎉 मास्टर कोडद्वारे प्रिमियम यशस्वीरित्या सुरू झाले!")
          st.rerun()
        else:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "SELECT * FROM premium_codes WHERE code = ?", (input_code,)
          )
          c_row = cursor.fetchone()

          if c_row and dict(c_row).get("used") == 0:
            exp_datetime = get_ist_time() + datetime.timedelta(days=28)
            exp_str = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
            now_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "UPDATE premium_codes SET used = 1, used_by = ?, used_date = ?"
                " WHERE code = ?",
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
                    f"{current_user_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये"
                    " आपले हार्दिक स्वागत आहे🥳",
                    current_user_name,
                ),
            )
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
        cursor.execute(
            "UPDATE users SET requested_code = 1 WHERE user_key = ?",
            (current_user_name,),
        )
        conn.commit()
        conn.close()
        st.success("✅ ॲडमीनला रिक्वेस्ट पाठवली!")

# ==========================================
# 📌 विभाग १४: CIVIL AI ASSISTANT
# ==========================================
locks_cfg = get_feature_locks()
ai_lock_setting = locks_cfg.get("Civil AI Assistant", "Premium")

if ai_lock_setting == "Free" or is_user_premium:
  with st.expander("🤖 Patil Infratech Civil AI Assistant (Ask Anything)"):
    user_ai_query = st.text_input(
        "तुमचा प्रश्न किंवा शंका इथे लिहा:",
        placeholder="उदा. dry volume factor for concrete...",
        key="civil_ai_input",
    )
    if st.button("🚀 Ask Civil AI"):
      if user_ai_query.strip():
        with st.spinner(
            "🤖 Civil AI is analyzing... (कृपया ५ सेकंद वाट पाहा)"
        ):
          time.sleep(5.0)
          api_key = st.secrets.get(
              "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")
          )
          ai_response_text = ""
          if HAS_GENAI and api_key:
            try:
              client = genai.Client(api_key=api_key)
              prompt = (
                  "You are a Senior Civil Engineer for Patil Infratech. Provide"
                  " a direct, professional, final answer to the user query"
                  f" without showing calculation steps: {user_ai_query}"
              )
              response = client.models.generate_content(
                  model="gemini-2.5-flash", contents=prompt
              )
              if response and response.text:
                ai_response_text = response.text
            except Exception as e:
              ai_response_text = f"⚠️ AI Error: {e}"
          if not ai_response_text or "Error" in ai_response_text:
            ai_response_text = (
                "👷‍♂️ **Patil Infratech Expert Engineer Analysis:** Regarding"
                f' your query *"{user_ai_query}"*, please use our Rate Analysis'
                " or BBS Calculator modules."
            )

          st.markdown(
              f"""
                        <div style="background: #111827; border-left: 5px solid #00f2fe; padding: 18px; border-radius: 14px; margin-top: 12px; box-shadow: 0 4px 20px rgba(0, 242, 254, 0.2);">
                            <b>🎯 Civil AI Answer:</b><br><br>{ai_response_text}
                        </div>
                    """,
              unsafe_allow_html=True,
          )

# ==========================================
# 📌 विभाग १५: मुख्य मॉड्यूल निवडीचे डॅशबोर्ड कार्ड्स (Side-by-Side)
# ==========================================
if st.session_state.selected_module is None:
  st.markdown(
      "<h3 style='text-align:center; margin-bottom:20px;'>🚀 कृपया मॉड्यूल"
      " निवडा</h3>",
      unsafe_allow_html=True,
  )

  calc_lock = locks_cfg.get("Civil Calculator", "Free")
  site_lock = locks_cfg.get("Site Manager", "Free")

  main_col1, main_col2 = st.columns(2)

  # १. साईट मॅनेजर कार्ड
  with main_col1:
    site_badge = "🆓 Free Access" if site_lock == "Free" else "👑 VIP Premium"
    st.markdown(
        f"""
            <div class="module-card">
                <div style="font-size: 42px; margin-bottom: 8px;">👷‍♂️</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 800;">Site Manager</h3>
                <p style="color: #94a3b8; font-size: 13px; margin: 6px 0 12px 0;">हजेरी, मजुरी, साहित्य ट्रॅकर व दैनिक प्रोग्रेस रिपोर्ट</p>
                <span style="font-size: 11px; font-weight: bold; color: {'#38bdf8' if site_lock == 'Free' else '#f59e0b'}; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 12px;">[{site_badge}]</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(" ")
    if st.button(
        "👷‍♂️ Open Site Manager",
        key="btn_open_site",
        use_container_width=True,
        type="primary",
    ):
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
                <div style="font-size: 42px; margin-bottom: 8px;">📐</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 800;">Estimator Tools</h3>
                <p style="color: #94a3b8; font-size: 13px; margin: 6px 0 12px 0;">Rate Analysis, BBS Schedule, QS & Unit Converter</p>
                <span style="font-size: 11px; font-weight: bold; color: #f59e0b; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 12px;">[5 Advanced Tools]</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(" ")
    if st.button(
        "📐 Open Estimator Tools",
        key="btn_open_estimator",
        use_container_width=True,
        type="primary",
    ):
      st.session_state.selected_module = "Estimator Tools"
      st.session_state.selected_estimator_sub_module = None
      trigger_push_state()
      st.rerun()

# ==========================================
# 📌 विभाग १६: ESTIMATOR TOOLS मॉड्यूल (Sub-modules)
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

    # ✅ बरोबर ४ Spaces (Correct Indentation)
    def render_combined_master_report(user_key, site_name):
        st.subheader(f"📑 Master Project Estimate: {site_name}")
        st.caption("💡 मागील २ दिवसांमधील Rate Analysis, BBS आणि Quantity Survey चा एकत्रित IS-Code फॉरमॅट ३-पेज रिपोर्ट.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
 # ==========================================
    # १६.१ मास्टर ३-इन-१ कंबाइन्ड PDF व Excel रिपोर्ट फंक्शन (Fixed & Complete)
    # ==========================================
    def render_combined_master_report(user_key, site_name):
      st.subheader(f"📑 Master Project Estimate: {site_name}")
      st.caption(
          "💡 मागील २ दिवसांमधील Rate Analysis, BBS आणि Quantity Survey चा एकत्रित"
          " IS-Code फॉरमॅट ३-पेज रिपोर्ट."
      )

      conn = get_db_connection()
      cursor = conn.cursor()
      two_days_ago = (get_ist_time() - datetime.timedelta(days=2)).strftime(
          "%Y-%m-%d 00:00:00"
      )
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
        st.warning(
            f"⚠️ '{site_name}' साठी मागील २ दिवसांत कोणतेही कॅल्क्युलेशन सेव्ह"
            " केलेले नाही. कृपया आधी टूल्स वापरून रिपोर्ट तयार करा."
        )
        return

      # पूर्ण दिसणारा वॉटरमार्क व A4 पेज-ब्रेक स्टाईल
      full_html_doc = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>PATIL INFRATECH - {site_name} Master Estimate</title>
            <style>
                @page {{
                    size: A4 portrait;
                    margin: 10mm;
                }}
                @media print {{
                    body {{
                        background: #ffffff !important;
                        color: #000000 !important;
                    }}
                    .no-print {{
                        display: none !important;
                    }}
                    .page-break {{
                        page-break-before: always !important;
                        break-before: page !important;
                    }}
                }}
                body {{
                    background-color: #f1f5f9;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 10px;
                    color: #000000;
                }}
                .a4-page {{
                    position: relative;
                    background: #ffffff;
                    width: 100%;
                    max-width: 800px;
                    margin: 0 auto 25px auto;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    border: 1.5px solid #0f172a;
                    box-sizing: border-box;
                    min-height: 1050px;
                }}
                /* 🌊 सुस्पष्ट आणि पूर्ण दिसणारा वॉटरमार्क */
                .watermark {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(-30deg);
                    font-size: 24px;
                    font-weight: 900;
                    color: rgba(0, 0, 0, 0.08);
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    text-align: center;
                    width: 85%;
                    max-width: 600px;
                    line-height: 1.4;
                    pointer-events: none;
                    user-select: none;
                    border: 3px dashed rgba(0, 0, 0, 0.08);
                    padding: 15px 25px;
                    border-radius: 14px;
                    z-index: 1;
                }}
                .content-box {{
                    position: relative;
                    z-index: 2;
                }}
                .header-title {{
                    text-align: center;
                    border-bottom: 2.5px solid #0f172a;
                    padding-bottom: 8px;
                    margin-bottom: 15px;
                }}
                .header-title h1 {{
                    margin: 0;
                    font-size: 24px;
                    color: #0f172a;
                    font-weight: 900;
                }}
                .header-title p {{
                    margin: 3px 0;
                    font-size: 12px;
                    font-weight: bold;
                    color: #475569;
                }}
                table.info-table {{
                    width: 100%;
                    margin-bottom: 15px;
                    font-size: 12px;
                    border-collapse: collapse;
                }}
                table.info-table td {{
                    padding: 4px 0;
                }}
                .section-header {{
                    background: #0f172a;
                    color: #ffffff;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 4px;
                    margin: 15px 0 10px 0;
                }}
                pre.data-render {{
                    white-space: pre-wrap;
                    font-family: inherit;
                    background: #f8fafc;
                    padding: 12px;
                    border-radius: 6px;
                    border: 1px solid #cbd5e1;
                    font-size: 11px;
                    line-height: 1.5;
                }}
                .signature-box {{
                    margin-top: 40px;
                    width: 100%;
                    font-size: 12px;
                }}
                .footer-stamp {{
                    text-align: center;
                    margin-top: 25px;
                    font-size: 11px;
                    color: #64748b;
                    border-top: 1px solid #e2e8f0;
                    padding-top: 6px;
                }}
            </style>
        </head>
        <body>
        """

      # प्रत्येक सेव्ह केलेल्या नोंदीसाठी स्वतंत्र A4 पेज
      for idx, r in enumerate(records, 1):
        page_break_class = "page-break" if idx > 1 else ""
        sec_title = (
            "Rate Analysis"
            if idx == 1
            else (
                "Bar Bending Schedule (BBS)"
                if idx == 2
                else "Quantity Surveying"
            )
        )

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
                    <hr style="border: 0.5px solid #cbd5e1; margin-bottom: 12px;">

                    <div class="section-header">
                        विभाग #{idx}: {sec_title} (नोंद वेळ: {r['timestamp']})
                    </div>

                    <pre class="data-render">{r['report_data']}</pre>

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

      # प्रीव्ह्यू
      st.components.v1.html(full_html_doc, height=520, scrolling=True)

      # Excel / CSV एक्स्पोर्ट डेटा तयार करणे (openpyxl वर विसंबून न राहता थेट सुसंगत फॉरमॅट)
      excel_data_list = []
      for r in records:
        excel_data_list.append({
            "Site Name": site_name,
            "User": user_key,
            "Timestamp": r["timestamp"],
            "Report Data": r["report_data"].replace("|", " ").strip(),
        })
      excel_df = pd.DataFrame(excel_data_list)
      csv_bytes = excel_df.to_csv(index=False).encode("utf-8-sig")

      st.write("---")
      c1, c2, c3 = st.columns(3)

      with c1:
        # १. मास्टर HTML/PDF फाईल डाऊनलोड
        st.download_button(
            label="📥 Download Master Report",
            data=full_html_doc,
            file_name=(
                f"Patil_Infratech_{site_name.replace(' ', '_')}_Report.html"
            ),
            mime="text/html",
            type="primary",
            use_container_width=True,
        )

      with c2:
        # २. Excel सुसंगत CSV डाऊनलोड (Zero Dependency)
        st.download_button(
            label="📊 Export Excel Data (.csv)",
            data=csv_bytes,
            file_name=(
                f"Patil_Infratech_{site_name.replace(' ', '_')}_Estimate.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

      with c3:
        # ३. थेट प्रिंट / Save as PDF
        st.markdown(
            """
                <button onclick="window.parent.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 10px 14px; border-radius: 8px; font-weight: bold; cursor: pointer; height: 38px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                    🖨️ Instant Print (A4)
                </button>
            """,
            unsafe_allow_html=True,
        )

  # --- मेनू पर्याय (Icon Grid Selection) ---
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
      if st.button(
          "🧮 Calculator", key="btn_est_calc", use_container_width=True
      ):
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
      if st.button(
          "📊 Rate Analysis", key="btn_est_ra", use_container_width=True
      ):
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
      if st.button(
          "📈 Quantity Survey", key="btn_est_qs", use_container_width=True
      ):
        if qs_lock == "Premium" and not is_user_premium:
          st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे!")
        else:
          st.session_state.selected_estimator_sub_module = (
              "Quantity Surveying"
          )
          trigger_push_state()
          st.rerun()

    st.write(" ")
    st.markdown(
        """
            <div style="text-align: center; background: #111827; padding: 18px 10px; border-radius: 20px; border: 1px solid #f59e0b;">
                <h1 style="font-size: 32px; margin:0;">📑</h1>
                <h5 style="margin: 8px 0 2px 0; color: #f59e0b; font-weight:800; font-size:14px;">3-in-1 Master Estimate PDF & Excel</h5>
                <p style="font-size: 10px; color: #cbd5e1; margin:0;">[Rate Analysis + BBS + QS ३ स्वतंत्र पेजेसचा रिपोर्ट]</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(" ")
    if st.button(
        "📑 Open 3-in-1 Master Report Generator",
        key="btn_est_master_pdf",
        use_container_width=True,
        type="primary",
    ):
      st.session_state.selected_estimator_sub_module = "Master PDF"
      trigger_push_state()
      st.rerun()

  # --- टूल्स उघडल्यानंतरची रचना ---
  else:
    if st.button("⬅️ Back to Estimator Menu", key="btn_back_estimator_menu"):
      st.session_state.selected_estimator_sub_module = None
      st.rerun()

    st.write("---")
    est_sub_mod = st.session_state.selected_estimator_sub_module

    # ०. Master 3-in-1 Combined Estimate PDF
    if est_sub_mod == "Master PDF":
      render_combined_master_report(
          current_user_name, st.session_state.current_site_name
      )

    # १. Civil Calculator & Smart Unit Converter
    elif est_sub_mod == "Calculator":
      st.subheader("🧮 Civil Smart Unit Converter")
      st.caption(
          "💡 एकाच बॉक्समध्ये मूल्य भरा आणि सर्व युनिट्समधील अचूक हिशोब एकाच"
          " झटक्यात मिळवा!"
      )

      conv_category = st.selectbox("कनव्हर्शन प्रकार निवडा:", [
          "📦 Volume / Brass Converter (घनफळ आणि ब्रास)",
          "📏 Length Converter (लांबी मोजमाप)",
          "📐 Area Converter (क्षेत्रफळ मोजमाप)",
      ])

      if "Volume / Brass" in conv_category:
        st.markdown("#### 📦 Volume & Brass Converter")
        val = st.number_input(
            "मूल्य भरा (Value):",
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="v_val",
        )
        unit_from = st.selectbox("मूळ युनिट (From Unit):", [
            "Cubic Meter (m³)",
            "Cubic Feet (CFT)",
            "Brass",
        ])

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
        val = st.number_input(
            "लांबी भरा (Length Value):",
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="l_val",
        )
        unit_from = st.selectbox("मूळ युनिट (From Unit):", [
            "Meters",
            "Feet",
            "Inches",
            "Millimeters (mm)",
            "Centimeters (cm)",
        ])

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
        val = st.number_input(
            "क्षेत्रफळ भरा (Area Value):",
            min_value=0.0,
            value=100.0,
            step=10.0,
            key="a_val",
        )
        unit_from = st.selectbox("मूळ युनिट (From Unit):", [
            "Sq. Meters (m²)",
            "Sq. Feet (Sq. Ft.)",
            "Guntha",
            "Acre",
        ])

        if st.button(
            "⚡ Convert Now", type="primary", key="btn_conv_area"
        ):
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

    # २. Rate Analysis Module
    elif est_sub_mod == "Rate Analysis":
      master_rates = get_market_rates()
      st.markdown(
          "<div style='background: #111827; padding: 14px; border-radius:"
          " 16px; text-align: center; font-size: 13px; font-weight: bold;"
          " color: #f8fafc; margin-bottom: 18px; border-left: 5px solid"
          " #00f2fe; border: 1px solid rgba(0,242,254,0.2); box-shadow: 0 4px"
          " 15px rgba(0,0,0,0.5);'>📢 आजचे मार्केट दर 🏷️ cement:"
          f" ₹{master_rates.get('cement', 400.0)}/bag | sand:"
          f" ₹{master_rates.get('sand', 2500.0)}/m³ | aggregate:"
          f" ₹{master_rates.get('aggregate', 2200.0)}/m³ | steel:"
          f" ₹{master_rates.get('steel', 60.0)}/Kg | brick:"
          f" ₹{master_rates.get('bricks', 8.0)}/nos</div>",
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
          grade = st.selectbox("काँक्रीट ग्रेड निवडा:", [
              "M10 (1:3:6)",
              "M15 (1:2:4)",
              "M20 (1:1.5:3)",
              "M25 (1:1:2)",
          ])
        with col2:
          component = st.selectbox("आरसीसी घटक (Component) निवडा:", [
              "Footing (0.8% Steel)",
              "Slab (1.0% Steel)",
              "Beam (2.0% Steel)",
              "Column (2.5% Steel)",
              "Plain Concrete (0% Steel)",
          ])

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
          volume = st.number_input(
              "एकूण काँक्रीट घनफळ (Volume in m³):",
              min_value=0.0,
              value=1.0,
              key="cc_vol",
          )
          cement_rate = st.number_input(
              "सिमेंट दर प्रति बॅग (₹):",
              min_value=0.0,
              value=float(master_rates.get("cement", 400.0)),
              key="cc_cem_r",
          )
          sand_rate = st.number_input(
              "वाळूचा दर प्रति m³ (₹):",
              min_value=0.0,
              value=float(master_rates.get("sand", 2500.0)),
              key="cc_snd_r",
          )
        with v_col2:
          aggregate_rate = st.number_input(
              "खडीचा दर प्रति m³ (₹):",
              min_value=0.0,
              value=float(master_rates.get("aggregate", 2200.0)),
              key="cc_agg_r",
          )
          steel_rate = (
              st.number_input(
                  "स्टीलचा दर प्रति किलो (₹/Kg):",
                  min_value=0.0,
                  value=float(master_rates.get("steel", 60.0)),
                  key="cc_stl_r",
              )
              if steel_percentage > 0
              else 0.0
          )

        st.markdown("#### [B] लेबर खर्च")
        l_col1, l_col2, l_col3 = st.columns(3)
        with l_col1:
          mason_qty = st.number_input(
              "मेसन संख्या:", min_value=0.0, value=0.0, key="cc_msn_q"
          )
          mason_rate = st.number_input(
              "मेसन दर (₹/Day):",
              min_value=0.0,
              value=600.0,
              key="cc_msn_r",
          )
        with l_col2:
          mazdoor_qty = st.number_input(
              "मजदूर संख्या:", min_value=0.0, value=0.0, key="cc_mzd_q"
          )
          mazdoor_rate = st.number_input(
              "मजदूर दर (₹/Day):",
              min_value=0.0,
              value=400.0,
              key="cc_mzd_r",
          )
        with l_col3:
          bb_qty = st.number_input(
              "बार बेंडर संख्या:", min_value=0.0, value=0.0, key="cc_bb_q"
          )
          bb_rate = st.number_input(
              "बार बेंडर दर (₹/Day):",
              min_value=0.0,
              value=550.0,
              key="cc_bb_r",
          )

        st.markdown("#### [C] अवांतर खर्च व नफा")
        o_col1, o_col2 = st.columns(2)
        with o_col1:
          scaffolding_cost = st.number_input(
              "सेंटरिंग खर्च (₹):", min_value=0.0, value=0.0, key="cc_scaf"
          )
          contingency_cost = st.number_input(
              "आकस्मिक खर्च (₹):", min_value=0.0, value=0.0, key="cc_cont"
          )
        with o_col2:
          water_pct = st.number_input(
              "वॉटर charge (%):", min_value=0.0, value=1.0, key="cc_wat_p"
          )
          profit_pct = st.number_input(
              "कंत्राटदार नफा (%):",
              min_value=0.0,
              value=10.0,
              key="cc_prof_p",
          )

        if st.button(
            "📊 GENERATE RATE ANALYSIS REPORT",
            type="primary",
            key="cc_report_btn",
        ):
          dry_volume = volume * 1.54
          total_parts = cement_ratio + sand_ratio + aggregate_ratio
          c_bags = (
              math.ceil(
                  ((cement_ratio / total_parts) * dry_volume) * 28.8
              )
              if total_parts > 0
              else 0
          )
          s_m3 = (
              (sand_ratio / total_parts) * dry_volume
              if total_parts > 0
              else 0.0
          )
          a_m3 = (
              (aggregate_ratio / total_parts) * dry_volume
              if total_parts > 0
              else 0.0
          )
          steel_qty = (
              volume * (steel_percentage / 100) * 7850
              if steel_percentage > 0
              else 0.0
          )

          total_cement_cost = c_bags * cement_rate
          total_sand_cost = s_m3 * sand_rate
          total_aggregate_cost = a_m3 * aggregate_rate
          total_steel_cost = steel_qty * steel_rate

          mat_cost = (
              total_cement_cost
              + total_aggregate_cost
              + total_sand_cost
              + total_steel_cost
          )
          lab_cost = (
              (mason_qty * mason_rate)
              + (mazdoor_qty * mazdoor_rate)
              + (bb_qty * bb_rate)
          )
          base_total = (
              mat_cost + lab_cost + scaffolding_cost + contingency_cost
          )
          w_amt = base_total * (water_pct / 100)
          p_amt = base_total * (profit_pct / 100)
          grand_total = base_total + w_amt + p_amt

          st.success("🎉 रिपोर्ट तयार झाला आहे!")
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

          if current_user_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_key, timestamp, user_note,"
                " report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                (
                    current_user_name,
                    get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                    "Concrete Rate Analysis",
                    report_table,
                    st.session_state.current_site_name,
                ),
            )
            conn.commit()
            conn.close()

      elif "Brickwork" in main_choice:
        st.subheader("🧱 Brickwork Estimation")
        mortar_choice = st.selectbox(
            "मॉर्टर मिक्स गुणोत्तर निवडा:",
            ["1:3", "1:4", "1:5", "1:6"],
        )
        c_part, s_part = (
            (1, 3)
            if mortar_choice == "1:3"
            else ((1, 4) if mortar_choice == "1:4" else (1, 6))
        )
        volume = st.number_input(
            "वीटकामाचे घनफळ (m³):", min_value=0.1, value=1.0, key="bw_vol"
        )
        brick_rate = st.number_input(
            "विटांचा दर (प्रति १००० नग ₹):", value=8000.0, key="bw_br"
        )
        cement_rate = st.number_input(
            "सिमेंट दर प्रति बॅग (₹):", value=400.0, key="bw_cr"
        )
        sand_rate = st.number_input(
            "वाळूचा दर प्रति m³ (₹):", value=2500.0, key="bw_sr"
        )

        if st.button(
            "📊 GENERATE BRICKWORK REPORT", type="primary", key="bw_btn"
        ):
          total_bricks = math.ceil(volume * 500)
          dry_mortar_vol = volume * 0.30
          c_bags = math.ceil(
              (c_part / (c_part + s_part)) * dry_mortar_vol * 28.8
          )
          sand_m3 = (s_part / (c_part + s_part)) * dry_mortar_vol

          b_cost = (total_bricks / 1000) * brick_rate
          c_cost = c_bags * cement_rate
          s_cost = sand_m3 * sand_rate
          grand_total = (b_cost + c_cost + s_cost) * 1.15

          report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| Bricks | {total_bricks} | Nos | {(brick_rate/1000):.2f} | {b_cost:.2f} |
| Cement | {c_bags} | Bags | {cement_rate:.2f} | {c_cost:.2f} |
| Sand | {sand_m3:.2f} | m³ | {sand_rate:.2f} | {s_cost:.2f} |
| **GRAND TOTAL (Incl. Overhead & Profit)** | | | | **₹ {grand_total:.2f}/-** |
"""
          st.markdown(report_table)

          if current_user_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_key, timestamp, user_note,"
                " report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                (
                    current_user_name,
                    get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                    "Brickwork Rate Analysis",
                    report_table,
                    st.session_state.current_site_name,
                ),
            )
            conn.commit()
            conn.close()

      else:  # Plaster Work
        st.subheader("🎨 Plaster Work Estimation")
        plaster_area = st.number_input(
            "प्लास्टर क्षेत्रफळ (m²):", min_value=1.0, value=10.0, key="pl_a"
        )
        thickness_mm = st.number_input(
            "जाडी (mm):", min_value=6.0, value=12.0, key="pl_t"
        )
        cement_rate = st.number_input(
            "सिमेंट दर प्रति बॅग (₹):", value=400.0, key="pl_cr"
        )
        sand_rate = st.number_input(
            "वाळू दर प्रति m³ (₹):", value=2500.0, key="pl_sr"
        )

        if st.button("📊 GENERATE PLASTER REPORT", type="primary", key="pl_btn"):
          wet_vol = plaster_area * (thickness_mm / 1000.0)
          dry_vol = wet_vol * 1.33
          c_bags = math.ceil((1 / 5) * dry_vol * 28.8)
          sand_m3 = (4 / 5) * dry_vol
          grand_total = (
              (c_bags * cement_rate) + (sand_m3 * sand_rate)
          ) * 1.20

          report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| Cement | {c_bags} | Bags | {cement_rate:.2f} | {c_bags*cement_rate:.2f} |
| Sand | {sand_m3:.2f} | m³ | {sand_rate:.2f} | {sand_m3*sand_rate:.2f} |
| **GRAND TOTAL (With Labor & Charges)** | | | | **₹ {grand_total:.2f}/-** |
"""
          st.markdown(report_table)

          if current_user_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (user_key, timestamp, user_note,"
                " report_data, site_name) VALUES (?, ?, ?, ?, ?)",
                (
                    current_user_name,
                    get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                    "Plaster Rate Analysis",
                    report_table,
                    st.session_state.current_site_name,
                ),
            )
            conn.commit()
            conn.close()

    # ३. BBS Calculator
    elif est_sub_mod == "BBS":
      st.subheader("🏗️ Bar Bending Schedule (BBS)")
      rcc_comp = st.selectbox(
          "घटक निवडा:", ["Footing", "Column", "Beam", "Slab"]
      )
      length_m = st.number_input("लांबी (m):", value=3.0, key="bbs_l")
      bar_dia = st.selectbox(
          "स्टील बार व्यास (mm):", [8, 10, 12, 16, 20, 25], index=2
      )
      nos = st.number_input("एकूण बार संख्या (Nos):", min_value=1, value=4)
      steel_rate = st.number_input("स्टील दर (₹/Kg):", value=60.0)

      if st.button("🧮 CALCULATE BBS REPORT", type="primary", key="bbs_btn"):
        unit_wt = (bar_dia**2) / 162.0
        tot_wt = unit_wt * length_m * nos
        tot_cost = tot_wt * steel_rate

        report_table = f"""
| Component | Bar Dia | Nos | Cutting Length | Total Weight | Rate | Total Amount |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| {rcc_comp} | {bar_dia} mm | {nos} | {length_m:.2f} m | **{tot_wt:.2f} Kg** | ₹{steel_rate:.2f} | **₹{tot_cost:.2f}/-** |
"""
        st.markdown(report_table)

        if current_user_name:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO history (user_key, timestamp, user_note,"
              " report_data, site_name) VALUES (?, ?, ?, ?, ?)",
              (
                  current_user_name,
                  get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                  f"BBS - {rcc_comp}",
                  report_table,
                  st.session_state.current_site_name,
              ),
          )
          conn.commit()
          conn.close()

    # ४. Quantity Surveying
    elif est_sub_mod == "Quantity Surveying":
      st.subheader("📈 Quantity Surveying & Abstract Sheet")
      desc = st.text_input("कामाचा तपशील:", value="Earthwork in Excavation")
      nos_item = st.number_input("संख्या (Nos):", min_value=1, value=1)
      l_val = st.number_input("लांबी (m):", min_value=0.1, value=5.0)
      w_val = st.number_input("रुंदी (m):", min_value=0.1, value=4.0)
      h_val = st.number_input("उंची/खोली (m):", min_value=0.1, value=1.5)

      if st.button("📈 GENERATE QS REPORT", type="primary", key="qs_btn"):
        tot_qty = nos_item * l_val * w_val * h_val
        report_table = f"""
| Description | Nos | Dimensions (L x W x H) | Total Quantity | Unit |
| :--- | :--- | :--- | :--- | :--- |
| {desc} | {nos_item} | {l_val:.2f} x {w_val:.2f} x {h_val:.2f} m | **{tot_qty:.3f}** | m³ |
"""
        st.markdown(report_table)

        if current_user_name:
          conn = get_db_connection()
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO history (user_key, timestamp, user_note,"
              " report_data, site_name) VALUES (?, ?, ?, ?, ?)",
              (
                  current_user_name,
                  get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                  f"QS - {desc}",
                  report_table,
                  st.session_state.current_site_name,
              ),
          )
          conn.commit()
          conn.close()
# ==========================================
# 📌 विभाग १७: SITE MANAGER मॉड्यूल (Attendance, Inventory, Progress, Checklist, Weekly)
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

    # Row 1: 3 Icons
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
      if st.button(
          "👷 Attendance", key="btn_site_att", use_container_width=True
      ):
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
      if st.button(
          "📦 Material Stock", key="btn_site_inv", use_container_width=True
      ):
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
      if st.button(
          "📸 Progress Report", key="btn_site_prog", use_container_width=True
      ):
        st.session_state.selected_site_sub_module = "Progress"
        trigger_push_state()
        st.rerun()

    st.write(" ")
    # Row 2: 2 Icons
    s_col4, s_col5 = st.columns(2)
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
      if st.button(
          "🏗️ Pre-Concreting Checklist",
          key="btn_site_chk",
          use_container_width=True,
      ):
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
      if st.button(
          "📊 Weekly Dashboard", key="btn_site_week", use_container_width=True
      ):
        st.session_state.selected_site_sub_module = "Weekly"
        trigger_push_state()
        st.rerun()

  else:
    if st.button("⬅️ Back to Site Manager Menu", key="btn_back_site_menu"):
      st.session_state.selected_site_sub_module = None
      st.rerun()

    st.write("---")
    sub_mod = st.session_state.selected_site_sub_module

    # --------------------------------------------------
    # १. Attendance & Wages Tracker
    # --------------------------------------------------
    if sub_mod == "Attendance":
      st.markdown("#### 👷 डेली हजेरी आणि मजुरी कॅल्क्युलेटर")
      att_date = st.date_input(
          "तारीख निवडा (Select Date):",
          datetime.date.today(),
          key="site_att_date",
      )

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
          st.markdown(
              f"<p style='margin-top:8px;'>{w_name}</p>",
              unsafe_allow_html=True,
          )
        with r_cols[1]:
          q = st.number_input(
              f"Qty {w_id}",
              min_value=0,
              value=def_q,
              step=1,
              key=f"q_{w_id}",
              label_visibility="collapsed",
          )
        with r_cols[2]:
          r = st.number_input(
              f"Rate {w_id}",
              min_value=0.0,
              value=def_r,
              step=50.0,
              key=f"r_{w_id}",
              label_visibility="collapsed",
          )
        with r_cols[3]:
          t = q * r
          st.markdown(
              f"<p style='margin-top:8px; font-weight:bold;'>₹ {t:.2f}</p>",
              unsafe_allow_html=True,
          )
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

      if st.button(
          "💾 Save Attendance to SQLite Database",
          type="primary",
          key="save_att_btn",
      ):
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
        st.success(
            "✅ आजची हजेरी आणि मजुरी बिल डेटाबेसमध्ये सेव्ह झाले!"
        )

    # --------------------------------------------------
    # २. Material Stock & Inventory Tracker
    # --------------------------------------------------
    elif sub_mod == "Inventory":
      st.markdown(
          "#### 📦 साहित्य ट्रॅकर (Material Inventory & Stock Tracker)"
      )

      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(
          "SELECT material_name, transaction_type, quantity FROM"
          " site_inventory WHERE user_key = ?",
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
        st.info(
            "ℹ️ सध्या स्टॉकमध्ये कोणतीही एंट्री उपलब्ध नाही. खालील"
            " इन-आऊट फॉर्म भरा."
        )

      st.write("---")
      st.markdown("##### ➕/➖ Material IN-OUT Entry:")
      mat_name = st.selectbox(
          "साहित्य निवडा (Material):",
          ["Cement Bags", "Steel (Kg)", "Sand (CFT)", "Bricks (Nos)"],
          key="inv_mat_type",
      )
      trans_type = st.radio(
          "इनपुट/आऊटपुट निवडा:",
          ["Material IN (+)", "Material OUT (-)"],
          horizontal=True,
          key="inv_trans_type",
      )
      entry_qty = st.number_input(
          "बोरी / नग संख्या (Quantity):",
          min_value=1,
          value=100,
          step=1,
          key="inv_qty_val",
      )

      if st.button(
          "📥 Save Stock Entry", type="primary", key="save_inv_btn"
      ):
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

    # --------------------------------------------------
    # ३. Daily Progress Report & Photos
    # --------------------------------------------------
    elif sub_mod == "Progress":
      st.markdown(
          "#### 📸 साईट प्रोग्रेस रिपोर्ट (Daily Progress & Photo Upload)"
      )

      work_stage = st.text_input(
          "कामाचा टप्पा (Stage Name):",
          value="Plinth Level Completed",
          key="prog_stage_input",
      )
      work_percent = st.slider(
          "Work % Slider (कामाची टक्केवारी):",
          0,
          100,
          40,
          key="prog_percent_slider",
      )
      site_photo = st.file_uploader(
          "मोबाईल किंवा कॅमेऱ्याने फोटो अपलोड करा:",
          type=["png", "jpg", "jpeg"],
          key="prog_photo_upload",
      )
      site_remark = st.text_area(
          "कामाचा रिमार्क / शेरा:",
          placeholder=(
              "उदा. साईटवर प्लिंथ लेव्हल कास्टिंगचे काम पूर्ण झाले आहे..."
          ),
          key="prog_remark_input",
      )

      if site_photo:
        st.image(
            site_photo,
            caption="Uploaded Site Work Photo",
            use_column_width=True,
        )

      if st.button(
          "📊 Generate Instant PDF Report & WhatsApp Summary",
          type="primary",
          key="save_prog_btn",
      ):
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
            "🏗️ *PATIL INFRATECH - DAILY SITE PROGRESS REPORT*\n👤 *Site"
            f" Engineer:* {current_user_name}\n📍 *Site:*"
            f" {st.session_state.current_site_name}\n📅 *Date:*"
            f" {datetime.date.today()}\n🚧 *Stage:* {work_stage}\n📈 *Work"
            f" Completed:* {work_percent}%\n📝 *Remark:*"
            f" {site_remark}\n--------------------------------\n_Daily"
            " Progress Report Generated_"
        )

        st.success(
            "🎉 Daily Progress Report यशस्वीरित्या जनरेट झाला आहे!"
        )
        st.code(report_summary)

        encoded_prog_msg = urllib.parse.quote(report_summary)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
          try:
            render_whatsapp_feature(encoded_prog_msg, "site_prog_wa")
          except Exception:
            st.markdown(
                "[Send"
                f" WhatsApp](https://wa.me/?text={encoded_prog_msg})"
            )
        with btn_col2:
          st.markdown(
              """
                        <button onclick="window.print()" style="width: 100%; background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; border: none; padding: 12px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);">
                            📄 Download Instant PDF Report
                        </button>
                    """,
              unsafe_allow_html=True,
          )

    # --------------------------------------------------
    # ४. Pre-Concreting Digital Checklist
    # --------------------------------------------------
    elif sub_mod == "Checklist":
      st.markdown(
          "#### 🏗️ Pre-Concreting Checklist (स्लॅब भरण्यापूर्वीची"
          " डिजिटल चेकलिस्ट)"
      )
      st.caption(
          "💡 काँक्रीटिंग किंवा स्लॅब भरण्यापूर्वी साईट इंजिनिअरने"
          " खालील सर्व बाबी तपासून टिक-मार्क करणे आवश्यक आहे."
      )

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
          "SELECT id, item_text, is_checked FROM pre_concreting_checklist WHERE"
          " user_key = ?",
          (current_user_name,),
      )
      db_items = cursor.fetchall()

      if not db_items:
        now_time_str = get_ist_time().strftime("%Y-%m-%d %H:%M:%S")
        for text in default_chk_items:
          cursor.execute(
              "INSERT INTO pre_concreting_checklist (user_key, item_text,"
              " is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
              (
                  current_user_name,
                  text,
                  now_time_str,
                  st.session_state.current_site_name,
              ),
          )
        conn.commit()
        cursor.execute(
            "SELECT id, item_text, is_checked FROM pre_concreting_checklist"
            " WHERE user_key = ?",
            (current_user_name,),
        )
        db_items = cursor.fetchall()
      conn.close()

      total_items = len(db_items)
      checked_items = sum(
          1 for item in db_items if item["is_checked"] == 1
      )
      progress_percentage = (
          int((checked_items / total_items) * 100) if total_items > 0 else 0
      )

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
        new_chk_text = st.text_input(
            "नवीन तपासणी पॉईंट टाका:",
            placeholder="उदा. जनरेटर बॅकअपची सोय आहे का?...",
            key="new_chk_input",
        )
        if st.button("प्लस (+)", key="btn_add_chk_item"):
          if new_chk_text.strip():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pre_concreting_checklist (user_key, item_text,"
                " is_checked, created_at, site_name) VALUES (?, ?, 0, ?, ?)",
                (
                    current_user_name,
                    new_chk_text.strip(),
                    get_ist_time().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.current_site_name,
                ),
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
          new_state = st.checkbox(
              item_text, value=is_chk, key=f"chk_box_{item_id}"
          )
          if new_state != is_chk:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pre_concreting_checklist SET is_checked = ? WHERE id ="
                " ?",
                (1 if new_state else 0, item_id),
            )
            conn.commit()
            conn.close()
            st.rerun()

        with col_del:
          if st.button("❌", key=f"btn_del_chk_{item_id}"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM pre_concreting_checklist WHERE id = ?",
                (item_id,),
            )
            conn.commit()
            conn.close()
            st.rerun()

      st.write("---")
      if st.button(
          "🔄 चेकलिस्ट रिसेट करा (पुन्हा नवीन स्लॅबसाठी तपासणी करा)"
      ):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pre_concreting_checklist SET is_checked = 0 WHERE user_key"
            " = ?",
            (current_user_name,),
        )
        conn.commit()
        conn.close()
        st.success("✅ सर्व टिक-मार्क्स रिसेट झाले आहेत!")
        st.rerun()

    # --------------------------------------------------
    # ५. Weekly Site Dashboard & Logs
    # --------------------------------------------------
    elif sub_mod == "Weekly":
      st.markdown(
          "#### 📊 मागील ७ दिवसांचा साइट रिपोर्ट (Weekly Site Dashboard)"
      )
      st.caption(
          "💡 मागील ७ दिवसांमधील तुमची हजेरी (Attendance), मटेरियल खर्च आणि"
          " कामाची प्रगती. तुम्ही चुकीची एंट्री येथून डिलीट करू शकता."
      )

      today = datetime.date.today()
      week_ago = today - datetime.timedelta(days=7)
      str_today = str(today)
      str_week_ago = str(week_ago)

      conn = get_db_connection()

      # १. Attendance Logs
      att_df = pd.read_sql_query(
          "SELECT rowid as id, date as Date, total_cost as Daily_Wage_Cost FROM"
          f" site_attendance WHERE user_key = '{current_user_name}' AND date"
          f" BETWEEN '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
          conn,
      )

      # २. Inventory Logs
      inv_df = pd.read_sql_query(
          "SELECT rowid as id, date as Date, material_name as Material,"
          " transaction_type as Status, quantity as Qty FROM site_inventory"
          f" WHERE user_key = '{current_user_name}' AND date BETWEEN"
          f" '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
          conn,
      )

      # ३. Progress Logs
      prog_df = pd.read_sql_query(
          "SELECT rowid as id, date as Date, stage_name as Work_Stage,"
          " progress_percent as Completed_Percent FROM site_progress WHERE"
          f" user_key = '{current_user_name}' AND date BETWEEN"
          f" '{str_week_ago}' AND '{str_today}' ORDER BY date DESC",
          conn,
      )

      conn.close()

      # Attendance Display
      with st.expander(
          "👷 मागील ७ दिवसांची हजेरी आणि मजुरी खर्च (Wages)", expanded=True
      ):
        if not att_df.empty:
          total_week_wage = att_df["Daily_Wage_Cost"].sum()
          st.markdown(
              "**💰 एकूण ७ दिवसांचा मजुरी खर्च:** <span style='color:#10b981;"
              f" font-size:18px;'>₹ {total_week_wage:,.2f}</span>",
              unsafe_allow_html=True,
          )
          st.dataframe(
              att_df.drop(columns=["id"]),
              use_container_width=True,
              hide_index=True,
          )

          st.markdown("---")
          c1, c2 = st.columns([3, 1])
          with c1:
            att_del_opt = st.selectbox(
                "❌ डिलीट करण्यासाठी रेकॉर्ड निवडा:",
                att_df.to_dict("records"),
                format_func=lambda x: (
                    f"तारीख: {x['Date']} | रक्कम: ₹ {x['Daily_Wage_Cost']}"
                ),
                key="sel_del_att",
            )
          with c2:
            st.markdown(
                "<div style='margin-top:28px;'></div>", unsafe_allow_html=True
            )
            if st.button(
                "🗑️ Delete Record",
                key="btn_del_att",
                use_container_width=True,
            ):
              conn = get_db_connection()
              conn.execute(
                  "DELETE FROM site_attendance WHERE rowid=?",
                  (att_del_opt["id"],),
              )
              conn.commit()
              conn.close()
              st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
              st.rerun()
        else:
          st.info("ℹ️ मागील ७ दिवसात कोणतीही हजेरी नोंदवली नाही.")

      # Inventory Display
      with st.expander(
          "📦 मागील ७ दिवसांचा मटेरियल ट्रॅकर (Material IN/OUT)"
      ):
        if not inv_df.empty:
          st.dataframe(
              inv_df.drop(columns=["id"]),
              use_container_width=True,
              hide_index=True,
          )

          st.markdown("---")
          c1, c2 = st.columns([3, 1])
          with c1:
            inv_del_opt = st.selectbox(
                "❌ डिलीट करण्यासाठी रेकॉर्ड निवडा:",
                inv_df.to_dict("records"),
                format_func=lambda x: (
                    f"{x['Date']} | {x['Material']} | {x['Status']}"
                    f" ({x['Qty']})"
                ),
                key="sel_del_inv",
            )
          with c2:
            st.markdown(
                "<div style='margin-top:28px;'></div>", unsafe_allow_html=True
            )
            if st.button(
                "🗑️ Delete Record",
                key="btn_del_inv",
                use_container_width=True,
            ):
              conn = get_db_connection()
              conn.execute(
                  "DELETE FROM site_inventory WHERE rowid=?",
                  (inv_del_opt["id"],),
              )
              conn.commit()
              conn.close()
              st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
              st.rerun()
        else:
          st.info(
              "ℹ️ मागील ७ दिवसात कोणतेही मटेरियल IN/OUT नोंदवले नाही."
          )

      # Progress Display
      with st.expander("📸 मागील ७ दिवसांची कामाची प्रगती (Progress)"):
        if not prog_df.empty:
          for _, row in prog_df.iterrows():
            st.markdown(
                f"**📅 Date:** `{row['Date']}` | **🚧 Work:**"
                f" {row['Work_Stage']} | **📈 Progress:**"
                f" `{row['Completed_Percent']}%`"
            )
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
            st.markdown(
                "<div style='margin-top:28px;'></div>", unsafe_allow_html=True
            )
            if st.button(
                "🗑️ Delete Record",
                key="btn_del_prog",
                use_container_width=True,
            ):
              conn = get_db_connection()
              conn.execute(
                  "DELETE FROM site_progress WHERE rowid=?",
                  (prog_del_opt["id"],),
              )
              conn.commit()
              conn.close()
              st.success("✅ रेकॉर्ड यशस्वीरित्या डिलीट झाले!")
              st.rerun()
        else:
          st.info(
              "ℹ️ मागील ७ दिवसात कामाचा कोणताही प्रोग्रेस रिपोर्ट"
              " नोंदवला नाही."
          )
