# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import json
import os
import datetime
import pandas as pd
import time
import urllib.parse
import random
import string

# Safe Google GenAI Import
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 🚨 Streamlit नियम: set_page_config नेहमी सर्वात आधी असावे!
st.set_page_config(page_title="PATIL INFRATECH", page_icon="🏗️", layout="centered")

# ==========================================
# 📂 फाईल डेटाबेस मॅनेजमेंट
# ==========================================
DB_FILE = "users_db.json"

def load_db():
    db = {
        "9999999999": {
            "id": "kanha", 
            "password": "patiladmin123",
            "comment": "मास्टर ॲडमीन अकाउंट",
            "admin_message": "मास्टर ॲडमीन",
            "is_premium": True,
            "premium_expiry": "2099-12-31 23:59:59",
            "requested_code": False,
            "seen_popup": True,
            "history": []
        },
        "PREMIUM_CODES": {},
        "FEATURE_LOCKS": {
            "Rate Analysis": "Free",
            "BBS": "Free",
            "WhatsApp Share": "Premium",
            "Civil AI Assistant": "Premium"
        }
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                old_db = json.load(f)
                if isinstance(old_db, dict):
                    for key, val in old_db.items():
                        if key != "9999999999":
                            db[key] = val
        except:
            pass
    return db

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

user_db = load_db()

# Session State Initialization
if "app_user_name" not in st.session_state:
    st.session_state.app_user_name = None
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "admin_view" not in st.session_state:
    st.session_state.admin_view = "main"
if "admin_selected_user" not in st.session_state:
    st.session_state.admin_selected_user = None

current_user_name = st.session_state.app_user_name

# ⏳ प्रिमियम स्टेटस व अचूक एक्सपायरी तपासणी
def check_user_premium_status(username):
    if not username: return False, "Free"
    db = load_db()
    user_info = db.get(username, {})
    if isinstance(user_info, dict) and user_info.get("is_premium", False):
        exp_date_str = user_info.get("premium_expiry")
        if exp_date_str:
            try:
                exp_datetime = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d %H:%M:%S")
                now_datetime = datetime.datetime.now()
                
                if now_datetime > exp_datetime:
                    user_info["is_premium"] = False
                    user_info["premium_expiry"] = None
                    save_db(db)
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
# 🎨 ULTRA-PREMIUM ROYAL METALLIC GOLD & AESTHETIC STYLING
# ==========================================
touch_glow_color = "rgba(255, 179, 0, 0.45)" if is_curr_premium else "rgba(59, 130, 246, 0.25)"
touch_border_color = "#FFD54F" if is_curr_premium else "#3b82f6"
card_border_color = "rgba(255, 179, 0, 0.45)" if is_curr_premium else "rgba(59, 130, 246, 0.25)"
input_inner_shadow = "inset 0 0 10px rgba(255, 179, 0, 0.3)" if is_curr_premium else "inset 0 2px 4px rgba(0, 0, 0, 0.4)"

st.markdown(f"""
    <style>
    /* 🔒 Hide Streamlit Branding & Controls */
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

    .admin-user-card {{
        background: rgba(31, 41, 55, 0.85);
        border: 1px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
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
# --- १. वेलकम स्क्रीन ॲनिमेशन (Always Play) ---
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

# ==========================================
# 🛑 USER FIRST-TIME AESTHETIC VIP POPUP CHECK
# ==========================================
if current_user_name:
    u_info = user_db.get(current_user_name, {})
    if isinstance(u_info, dict) and u_info.get("is_premium", False) and not u_info.get("seen_popup", False):
        activated_by_text = u_info.get("activated_by", "Kanhaiya (Founder of Patil Infratech)")
        st.markdown(f"""
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                        background: radial-gradient(circle at center, #141b2d 0%, #070a12 100%);
                        z-index: 9999999; display: flex; flex-direction: column; 
                        justify-content: center; align-items: center; text-align: center; padding: 25px;">
                <div style="background: rgba(255, 215, 0, 0.05); backdrop-filter: blur(25px); border-radius: 30px; padding: 40px; box-shadow: 0 0 50px rgba(255, 179, 0, 0.25); max-width: 500px; width: 100%;">
                    <h1 style="font-size: 70px; margin: 0; text-shadow: 0 0 25px #FFB300;">👑</h1>
                    <h1 style="background: linear-gradient(135deg, #FFE082 0%, #FFB300 50%, #FF6F00 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 28px; font-weight: 900; margin-top: 15px; letter-spacing: 0.5px;">WELCOME VIP MEMBER<br>{current_user_name.upper()}</h1>
                    <h2 style="color: #e2e8f0; font-size: 18px; font-weight: 500; margin-top: 15px; line-height: 1.4;">YOU ARE NOW A ROYAL PREMIUM MEMBER OF PATIL INFRATECH!</h2>
                    <p style="color: #93c5fd; font-size: 15px; margin-top: 12px;">✨ Unlimited WhatsApp Sharing & Full Feature Access Unlocked! 🚀</p>
                    <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.15); margin: 20px 0;">
                    <p style="color: #FFE082; font-size: 14px; margin: 0; font-weight: 600; letter-spacing: 0.3px;">✨ Approved & Activated By: {activated_by_text}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(4.0)
        user_db[current_user_name]["seen_popup"] = True
        save_db(user_db)
        st.rerun()

# मुख्य टायटल बॅनर
st.markdown("""
    <div class="main-header">
        <h1 style='color: white; margin:0; font-size: 26px;'>🏗️ PATIL INFRATECH</h1>
        <p style='color: #e0e7ff; margin:5px 0 0 0; font-size: 14px;'>📐 Quantity Surveyor & Cost Estimator</p>
        <small style='color: #93c5fd;'>Concept & Logic by: Kanhaiya (Founder of Patil Infratech)</small>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 👤 युझर नाव प्रविष्ट करणे
# ==========================================
if st.session_state.app_user_name is None:
    st.markdown("### 👤 ॲपमध्ये प्रवेश करण्यासाठी नाव प्रविष्ट करा")
    
    u_input = st.text_input("तुमचे नाव (Your Name):", placeholder="NAME", key="entry_user_name").strip()
    
    if st.button("ॲप उघडा (Enter App) 👉", type="primary"):
        if u_input:
            st.session_state.app_user_name = u_input
            user_db = load_db()
            
            if u_input not in user_db:
                new_welcome_msg = f"Welcome {u_input}! पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                user_db[u_input] = {
                    "id": u_input,
                    "comment": "काही नाही",
                    "admin_message": new_welcome_msg,
                    "is_premium": False,
                    "premium_expiry": None,
                    "requested_code": False,
                    "seen_popup": False,
                    "history": []
                }
                save_db(user_db)
            st.rerun()
        else:
            st.warning("⚠️ कृपया ॲप वापरण्यासाठी आधी तुमचे नाव टाका!")

    st.write("---")
    # 🛡️ सुरक्षित ॲडमीन पॅनल
    with st.expander("🛡️ Admin Database Panel (Only Kanhaiya)"):
        admin_id = st.text_input("Admin ID:", key="adm_id")
        admin_pass = st.text_input("Password:", type="password", key="adm_pass")
        
        secret_admin_id = st.secrets.get("ADMIN_ID", "kanha_1p") if hasattr(st, "secrets") else "kanha_1p"
        secret_admin_pass = st.secrets.get("ADMIN_PASS", "@Dellg15") if hasattr(st, "secrets") else "@Dellg15"

        if admin_id == secret_admin_id and admin_pass == secret_admin_pass:
            st.success("🔓 डेटाबेस अनलॉक झाला!")
            user_db = load_db()

            if st.session_state.admin_view == "rates":
                if st.button("⬅️ Back to Admin Main Menu", key="btn_back_from_rates"):
                    st.session_state.admin_view = "main"
                    st.rerun()

                st.write("---")
                st.markdown("### 📈 Update Master Market Rates (Today's Live Rates)")
                m_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
                
                adm_cem = st.number_input("Cement (per bag ₹):", min_value=0.0, value=float(m_rates.get("cement", 400.0)), step=1.0, key="adm_cem_inp_fixed")
                adm_snd = st.number_input("Sand (per m³ ₹):", min_value=0.0, value=float(m_rates.get("sand", 2500.0)), step=1.0, key="adm_snd_inp_fixed")
                adm_brk = st.number_input("Brick (per nos ₹):", min_value=0.0, value=float(m_rates.get("bricks", 8.0)), step=0.1, key="adm_brk_inp_fixed")
                adm_agg = st.number_input("Aggregate (per m³ ₹):", min_value=0.0, value=float(m_rates.get("aggregate", 2200.0)), step=1.0, key="adm_agg_inp_fixed")
                adm_ste = st.number_input("Steel Rate (per kg ₹):", min_value=0.0, value=float(m_rates.get("steel", 60.0)), step=1.0, key="adm_ste_inp_fixed")
                
                if st.button("💾 Save Master Market Rates", key="save_master_rates_fixed", type="primary"):
                    user_db["MASTER_MARKET_RATES"] = {
                        "cement": adm_cem, "sand": adm_snd, "bricks": adm_brk, "aggregate": adm_agg, "steel": adm_ste
                    }
                    save_db(user_db)
                    st.success("✅ आजचे मास्टर मार्केट दर डेटाबेसमध्ये यशस्वीरित्या अपडेट झाले!")

            elif st.session_state.admin_view == "locks":
                if st.button("⬅️ Back to Admin Main Menu", key="btn_back_from_locks"):
                    st.session_state.admin_view = "main"
                    st.rerun()

                st.write("---")
                st.markdown("### ⚙️ Feature Lock Manager (Free / Premium Selection)")
                st.caption("💡 इथून तू कोणतेही फीचर फ्री किंवा प्रिमियम करू शकतोस:")

                cur_locks = user_db.get("FEATURE_LOCKS", {"Rate Analysis": "Free", "BBS": "Free", "WhatsApp Share": "Premium", "Civil AI Assistant": "Premium"})

                fl_ra = st.selectbox("1. Rate Analysis Module Access:", ["Free", "Premium"], index=0 if cur_locks.get("Rate Analysis") == "Free" else 1, key="fl_ra_choice")
                fl_bbs = st.selectbox("2. BBS Calculator Access:", ["Free", "Premium"], index=0 if cur_locks.get("BBS") == "Free" else 1, key="fl_bbs_choice")
                fl_wa = st.selectbox("3. WhatsApp Full Report Share:", ["Free", "Premium"], index=0 if cur_locks.get("WhatsApp Share") == "Free" else 1, key="fl_wa_choice")
                fl_ai = st.selectbox("4. Civil AI Assistant Access:", ["Free", "Premium"], index=0 if cur_locks.get("Civil AI Assistant") == "Free" else 1, key="fl_ai_choice")

                if st.button("💾 Save Feature Lock Settings", key="save_locks_btn", type="primary"):
                    user_db["FEATURE_LOCKS"] = {
                        "Rate Analysis": fl_ra,
                        "BBS": fl_bbs,
                        "WhatsApp Share": fl_wa,
                        "Civil AI Assistant": fl_ai
                    }
                    save_db(user_db)
                    st.success("✅ प्रिमियम/फ्री फीचर्स सेटिंग्स यशस्वीरित्या अपडेट झाल्या!")

            elif st.session_state.admin_view == "user_detail" and st.session_state.admin_selected_user is not None:
                target_user = st.session_state.admin_selected_user
                
                if st.button("⬅️ Back to All Users List", key="btn_back_admin_list"):
                    st.session_state.admin_view = "main"
                    st.session_state.admin_selected_user = None
                    st.rerun()

                st.write("---")
                info = user_db.get(target_user, {})
                u_name = info.get("id", target_user)
                u_comm = info.get("comment", "काही नाही")
                u_prem = info.get("is_premium", False)
                exp_date = info.get("premium_expiry", "N/A")
                is_req = info.get("requested_code", False)
                u_hist = info.get("history", [])

                assigned_code = None
                if "PREMIUM_CODES" in user_db:
                    for c_code, c_data in user_db["PREMIUM_CODES"].items():
                        if c_data.get("assigned_to") == u_name and not c_data.get("used", False):
                            assigned_code = c_code
                            break

                status_badge = f"👑 VIP MEMBER: {u_name.upper()}" if u_prem else ("🚨 CODE REQUESTED!" if is_req else f"🆓 FREE: {u_name.upper()}")

                st.markdown(f"### 👤 MANAGE USER: <span style='color:#60a5fa;'>{u_name.upper()}</span>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="admin-user-card">
                        <p style="margin:5px 0; font-size:16px;"><b>माहिती/स्टेटस:</b> <span class="gold-vip-badge">{status_badge}</span></p>
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
                        if "PREMIUM_CODES" not in user_db: user_db["PREMIUM_CODES"] = {}
                        user_db["PREMIUM_CODES"][new_c] = {
                            "assigned_to": u_name,
                            "used": False,
                            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        user_db[target_user]["admin_message"] = f"तुमचा प्रिमियम कोड: {new_c} (ॲपमध्ये टाकून प्रिमियम अनलॉक करा)"
                        user_db[target_user]["requested_code"] = False
                        save_db(user_db)
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
                    now = datetime.datetime.now()
                    if time_unit == "Minutes":
                        exp_time = now + datetime.timedelta(minutes=time_val)
                    elif time_unit == "Hours":
                        exp_time = now + datetime.timedelta(hours=time_val)
                    else:
                        exp_time = now + datetime.timedelta(days=time_val)

                    user_db[target_user]["is_premium"] = True
                    user_db[target_user]["premium_expiry"] = exp_time.strftime("%Y-%m-%d %H:%M:%S")
                    user_db[target_user]["requested_code"] = False
                    user_db[target_user]["seen_popup"] = False
                    user_db[target_user]["activated_by"] = "Kanhaiya (Founder of Patil Infratech)"
                    save_db(user_db)
                    st.success(f"✅ {u_name} साठी {time_val} {time_unit} सेव्ह केले!")
                    st.rerun()

                if u_prem:
                    if st.button(f"🔻 Revoke Premium: {u_name}", key=f"win_rev_{target_user}"):
                        user_db[target_user]["is_premium"] = False
                        user_db[target_user]["premium_expiry"] = None
                        save_db(user_db)
                        st.warning(f"❌ {u_name} चे प्रिमियम काढले आहे.")
                        st.rerun()

                st.markdown("---")
                current_msg = info.get("admin_message", "Admin message...")
                new_msg = st.text_input(f"✍️ {u_name} साठी इनबॉक्स मेसेज बदलणे:", value=current_msg, key=f"win_msg_{target_user}")
                if st.button(f"✉️ मेसेज सेव्ह करा ({u_name})", key=f"win_btn_msg_{target_user}"):
                    if new_msg.strip():
                        user_db[target_user]["admin_message"] = new_msg.strip()
                        save_db(user_db)
                        st.success(f"✅ '{u_name}' चा इनबॉक्स मेसेज अपडेट झाला!")
                        st.rerun()

                if st.button(f"🗑️ Delete User: {u_name}", key=f"win_del_{target_user}"):
                    del user_db[target_user]
                    save_db(user_db)
                    st.session_state.admin_view = "main"
                    st.session_state.admin_selected_user = None
                    st.error(f"❌ युझर '{u_name}' डिलीट केला आहे!")
                    st.rerun()
                
                st.markdown("---")
                st.markdown(f"##### 📜 {u_name} चे जनरेट केलेले एस्टिमेशन रिपोर्ट्स ({len(u_hist)})")
                if u_hist:
                    for idx, hist in enumerate(u_hist, 1):
                        if isinstance(hist, dict):
                            ts = hist.get('timestamp', 'N/A')
                            with st.expander(f"🗓️ रिपोर्ट #{idx} | तारीख व वेळ: `{ts}`"):
                                st.markdown(hist.get("report_data", "डेटा उपलब्ध नाही"))
                else:
                    st.info("ℹ️ या युझरने अजून एकही रिपोर्ट जनरेट केलेला नाही.")

            else:
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    if st.button("📈 Update Master Market Rates", key="btn_open_rates", use_container_width=True):
                        st.session_state.admin_view = "rates"
                        st.rerun()
                with col_m2:
                    if st.button("⚙️ Feature Lock Manager", key="btn_open_locks", use_container_width=True):
                        st.session_state.admin_view = "locks"
                        st.rerun()

                st.markdown("---")
                st.markdown("### 📋 युझर डेटाबेस MASTER LIST (Sorted A-Z)")
                
                all_users_keys = [k for k in user_db.keys() if k not in ["9999999999", "MASTER_MARKET_RATES", "PREMIUM_CODES", "FEATURE_LOCKS"]]
                sorted_user_keys = sorted(all_users_keys, key=lambda x: str(user_db[x].get("id", x)).lower())

                if sorted_user_keys:
                    for mob in sorted_user_keys:
                        info = user_db[mob]
                        if not isinstance(info, dict): continue
                            
                        u_name = info.get("id", mob)
                        u_prem = info.get("is_premium", False)
                        is_req = info.get("requested_code", False)

                        col_u1, col_u2 = st.columns([3, 2])
                        if u_prem:
                            col_u1.markdown(f"<span class='gold-vip-badge'>👑 VIP MEMBER: {u_name.upper()}</span>", unsafe_allow_html=True)
                        elif is_req:
                            col_u1.markdown(f"#### 👤 **{u_name}** `[🚨 CODE REQUESTED!]`", unsafe_allow_html=True)
                        else:
                            col_u1.markdown(f"<span class='free-user-badge'>🆓 FREE: {u_name.upper()}</span>", unsafe_allow_html=True)

                        if col_u2.button(f"👁️ View / Manage {u_name}", key=f"open_user_win_{mob}"):
                            st.session_state.admin_view = "user_detail"
                            st.session_state.admin_selected_user = mob
                            st.rerun()
                        st.write("---")
                else:
                    st.info("ℹ️ डेटाबेसमध्ये सध्या कोणताही सामान्य युझर नाही.")

        elif admin_id or admin_pass:
            st.error("❌ चुकीचा Admin ID किंवा Password!")
            
    st.stop()

# सध्याचा ॲक्टिव्ह युझर
current_user_name = st.session_state.app_user_name
user_db = load_db()

# युझर हेडर व प्रिमियम व्हॅलिडिटी तपासणी
is_user_premium, status_text_str = check_user_premium_status(current_user_name)

col_u, col_lo = st.columns([3.5, 1.5])
if is_user_premium:
    col_u.markdown(f"<span class='gold-vip-badge'>👑 VIP MEMBER: {current_user_name.upper()} ({status_text_str})</span>", unsafe_allow_html=True)
else:
    col_u.markdown(f"<span class='free-user-badge'>🆓 FREE USER: {current_user_name.upper()}</span>", unsafe_allow_html=True)

if col_lo.button("🔄 नाव बदला"):
    st.session_state.app_user_name = None
    st.session_state.current_comment = "काही नाही"
    st.session_state.selected_module = None
    st.rerun()

# 🔄 इनबॉक्स मेसेज नेहमी लेटेस्ट डेटाबेसमधून लोड करणे
current_user_data = user_db.get(current_user_name, {})
admin_msg = current_user_data.get("admin_message", None)
if admin_msg:
    st.markdown("### 📥 Admin Message / Code Inbox")
    st.info(f"📢 **Admin:** {admin_msg}")
    st.write("---")

# ==========================================
# 🔑 १. युझरसाठी प्रिमियम कोड रिक्वेस्ट व इनपुट (FREE USER ONLY)
# ==========================================
if not is_user_premium:
    with st.expander("🔑 प्रिमियम अनलॉक करा (Enter Premium Code)"):
        st.markdown("##### 🎁 तुम्हाला मिळालेला प्रिमियम कोड इथे प्रविष्ट करा:")
        input_code = st.text_input("Enter Code (e.g. PATIL-XXXXX):", key="home_code_input").strip()
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔓 Activate Premium Now", key="home_activate_btn", type="primary"):
                codes_db = user_db.get("PREMIUM_CODES", {})
                if input_code in codes_db:
                    c_info = codes_db[input_code]
                    if c_info.get("used", False):
                        st.error("❌ हा कोड आधीच वापरला गेला आहे! तो आता व्हॅलिड नाही.")
                    else:
                        user_db["PREMIUM_CODES"][input_code]["used"] = True
                        user_db["PREMIUM_CODES"][input_code]["used_by"] = current_user_name
                        user_db["PREMIUM_CODES"][input_code]["used_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        exp_datetime = datetime.datetime.now() + datetime.timedelta(days=28)
                        user_db[current_user_name]["is_premium"] = True
                        user_db[current_user_name]["premium_expiry"] = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        user_db[current_user_name]["seen_popup"] = False
                        user_db[current_user_name]["activated_by"] = "Kanhaiya (Founder of Patil Infratech)"

                        user_db[current_user_name]["admin_message"] = f"Welcome {current_user_name}! पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                        save_db(user_db)
                        st.rerun()
                else:
                    st.error("❌ चुकीचा कोड! कृपया Admin कडून आलेला अचूक कोड टाका.")

        with c_btn2:
            if st.button("📩 Request Code from Admin", key="req_code_btn"):
                user_db[current_user_name]["requested_code"] = True
                save_db(user_db)
                st.success("✅ Admin ला कोडसाठी रिक्वेस्ट पाठवली आहे! लवकरच इनबॉक्समध्ये कोड दिसेल.")

# ==========================================
# 🔐 ॲप व्हॉट्सॲप फीचर अनलॉक/प्रीमियम फंक्शन
# ==========================================
def render_whatsapp_feature(encoded_msg, key_prefix):
    user_db = load_db()
    is_prem, status_str = check_user_premium_status(current_user_name)
    locks_cfg = user_db.get("FEATURE_LOCKS", {})
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
                    codes_db = user_db.get("PREMIUM_CODES", {})
                    if p_code in codes_db:
                        c_info = codes_db[p_code]
                        if c_info.get("used", False):
                            st.error("❌ हा कोड आधीच वापरला गेला आहे! तो आता व्हॅलिड नाही.")
                        else:
                            user_db["PREMIUM_CODES"][p_code]["used"] = True
                            user_db["PREMIUM_CODES"][p_code]["used_by"] = current_user_name
                            user_db["PREMIUM_CODES"][p_code]["used_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            exp_datetime = datetime.datetime.now() + datetime.timedelta(days=28)
                            user_db[current_user_name]["is_premium"] = True
                            user_db[current_user_name]["premium_expiry"] = exp_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            user_db[current_user_name]["seen_popup"] = False
                            user_db[current_user_name]["activated_by"] = "Kanhaiya (Founder of Patil Infratech)"
                            
                            user_db[current_user_name]["admin_message"] = f"Welcome {current_user_name}! पाटील इन्फ्राटेक मध्ये आपले हार्दिक स्वागत आहे🥳"
                            save_db(user_db)
                            st.rerun()
                    else:
                        st.error("❌ चुकीचा प्रिमियम कोड! कृपया अचूक कोड टाका.")

            with w_col2:
                if st.button("📩 Request Code from Admin", key=f"{key_prefix}_req_btn"):
                    user_db[current_user_name]["requested_code"] = True
                    save_db(user_db)
                    st.success("✅ ॲडमीनला कोडसाठी रिक्वेस्ट पाठवली आहे!")

# ==========================================
# 🤖 CIVIL AI ASSISTANT (Live Gemini AI + 5 Sec Thinking Time)
# ==========================================
st.markdown("---")
st.markdown("### 🤖 Patil Infratech Civil AI Assistant")

locks_cfg = user_db.get("FEATURE_LOCKS", {})
ai_lock_setting = locks_cfg.get("Civil AI Assistant", "Premium")

if ai_lock_setting == "Free" or is_user_premium:
    st.caption("💡 Ask any construction, estimation, or material question in ANY language or script (Marathi, English, Hindi, etc.):")
    user_ai_query = st.text_input("तुमचा प्रश्न किंवा शंका इथे लिहा (Type your question here):", placeholder="उदा. 1000 sq.ft slab steel calculation, kiti cement lagel...", key="civil_ai_input")
    
    if st.button("🚀 Ask Civil AI", key="ask_civil_ai_btn"):
        if user_ai_query.strip():
            # 5 Seconds Realistic Thinking Spinner & Delay
            with st.spinner("🤖 Civil AI is analyzing your question and calculating accurately... (कृपया ५ सेकंद वाट पाहा)"):
                time.sleep(5.0)
                
                api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
                ai_response_text = ""
                
                if HAS_GENAI and api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = f"""
                        You are an expert Senior Civil Engineer and Quantity Surveyor for Patil Infratech, founded by Kanhaiya. 
                        The user is asking a construction, estimation, or material calculation question in any language or script (Marathi, English, Hinglish, Hindi, etc.). 
                        Provide an accurate, standard, highly professional engineering response with exact formulas or material quantities if applicable. Match the user's language/script context.
                        User Query: {user_ai_query}
                        """
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        ai_response_text = response.text
                    except Exception as e:
                        ai_response_text = f"⚠️ Live AI connection notice: Standard fallback activated. (Error details: {e})"
                
                # Fallback standard calculation engine if API key is missing or encounters issue
                if not api_key or not ai_response_text or "Error" in ai_response_text:
                    q_text = user_ai_query.lower()
                    if "dry volume" in q_text or "factor" in q_text or "ड्राय व्हॉल्यूम" in q_text:
                        ai_response_text = "📐 **Patil Infratech Expert Answer:** The standard **Dry Volume Factor for Concrete is 1.54**. Wet concrete shrinks as it sets and compacts, so to calculate the required dry volume of raw materials (Cement, Sand, and Aggregate), we multiply the wet volume by 1.54."
                    elif "cement" in q_text or "सिमेंट" in q_text or "bags" in q_text:
                        ai_response_text = "🏗️ **Patil Infratech Expert Answer:** For a standard 1,000 sq.ft RCC slab structure (M20 grade, mix ratio 1:1.5:3), standard material calculation requires approximately **350 to 400 bags of cement**. (Using dry volume factor 1.54)."
                    elif "steel" in q_text or "स्टील" in q_text or "लोखंड" in q_text:
                        ai_response_text = "⚖️ **Patil Infratech Expert Answer:** For residential framed structures, standard steel reinforcement consumption ranges between **3.5 kg to 4.5 kg per sq.ft** depending on structural loading and spans."
                    elif "brick" in q_text or "वीट" in q_text or "विटा" in q_text:
                        ai_response_text = "🧱 **Patil Infratech Expert Answer:** For 1 cubic meter of standard brick masonry, approximately **500 standard bricks** and 0.30 m³ of dry mortar mix are professionally required."
                    else:
                        ai_response_text = f"👷‍♂️ **Patil Infratech Expert Engineer Analysis:** Regarding your query *\"{user_ai_query}\"*, standard engineering practice dictates accurate dimension inputs. Please utilize our dedicated **Rate Analysis** or **BBS Calculator** modules directly from the main menu for exact quantities."

                st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.95); border-left: 5px solid #FFB300; padding: 18px; border-radius: 14px; color: #f3f4f6; margin-top: 10px; line-height: 1.6;">
                        <b>🎯 Civil AI Expert Answer:</b><br><br>{ai_response_text}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ कृपया आधी तुमचा प्रश्न किंवा शंका लिहा / Please type your question first!")
else:
    st.markdown("""
        <div style="background: rgba(31, 41, 55, 0.6); border: 1px dashed #3b82f6; padding: 15px; border-radius: 14px; text-align: center;">
            <p style="color: #60a5fa; margin: 0; font-weight: 600;">🔒 Civil AI Assistant हे फीचर केवळ प्रिमियम (VIP) युझर्ससाठी आहे.</p>
            <p style="color: #9ca3af; margin: 5px 0 0 0; font-size: 13px;">प्रिमियम कोड टाकून किंवा ॲडमीनकडून कोड मागवून हे फिचर अनलॉक करा.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🎛️ DASHBOARD / ICON SELECTION SCREEN
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("### 🚀 तुम्हाला काय करायचे आहे ते निवडा:")
    
    ra_lock = locks_cfg.get("Rate Analysis", "Free")
    bbs_lock = locks_cfg.get("BBS", "Free")

    col_icon1, col_icon2 = st.columns(2)
    
    with col_icon1:
        ra_badge = "🆓 Free" if ra_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 20px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 50px; margin:0;">📊</h1>
                <h3 style="margin: 10px 0 5px 0; color: #f3f4f6;">Rate Analysis</h3>
                <p style="font-size: 12px; color: #9ca3af;">दर विश्लेषण (काँक्रीट व वीटकाम) [{ra_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Open Rate Analysis", key="btn_open_ra", use_container_width=True):
            if ra_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे! कृपया आधी प्रिमियम अनलॉक करा.")
            else:
                st.session_state.selected_module = "Rate Analysis"
                st.rerun()

    with col_icon2:
        bbs_badge = "🆓 Free" if bbs_lock == "Free" else "👑 Premium"
        st.markdown(f"""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 20px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 50px; margin:0;">🏗️</h1>
                <h3 style="margin: 10px 0 5px 0; color: #f3f4f6;">BBS</h3>
                <p style="font-size: 12px; color: #9ca3af;">Bar Bending Schedule [{bbs_badge}]</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏗️ Open BBS", key="btn_open_bbs", use_container_width=True):
            if bbs_lock == "Premium" and not is_user_premium:
                st.error("🔒 हे फीचर प्रिमियम युझर्ससाठी आहे! कृपया आधी प्रिमियम अनलॉक करा.")
            else:
                st.session_state.selected_module = "BBS"
                st.rerun()

# ==========================================
# 🛑 MODULE 1: RATE ANALYSIS MODULE
# ==========================================
elif st.session_state.selected_module == "Rate Analysis":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    
    master_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
    st.markdown(
        f"<div style='background: linear-gradient(90deg, #1f2937 0%, #111827 100%); padding: 12px; border-radius: 14px; text-align: center; font-size: 13px; font-weight: bold; color: #f3f4f6; margin-bottom: 15px; border-left: 5px solid #3b82f6; border: 1px solid rgba(255,255,255,0.08);'>"
        f"📢 आजचे मार्केट दर 🏷️ cement: ₹{master_rates['cement']}/bag | sand: ₹{master_rates['sand']}/m³ | aggregate: ₹{master_rates['aggregate']}/m³ | steel: ₹{master_rates['steel']}/Kg | brick: ₹{master_rates['bricks']}/nos"
        f"</div>", 
        unsafe_allow_html=True
    )

    main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)"])

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
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=400.0, key="cc_cem_r")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=2500.0, key="cc_snd_r")
        with v_col2:
            aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, value=2200.0, key="cc_agg_r")
            steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, value=65.0, key="cc_stl_r") if steel_percentage > 0 else 0.0

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
        user_note = st.text_area("या एस्टिमेशन संदर्भात काही नोट किंवा कमेंट लिहायची असल्यास इथे लिहा:", placeholder="उदा. ग्राउंड फ्लोअर वीटकाम...", key="bw_note")
        if st.button("💬 कमेंट सबमिट करा", key="cc_comm_btn"):
            if user_note.strip():
                st.session_state.current_comment = user_note.strip()
                user_db = load_db()
                if current_user_name in user_db:
                    user_db[current_user_name]["comment"] = user_note.strip()
                    save_db(user_db)
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
            msg_text += f"📅 *Date:* {datetime.datetime.now().strftime('%d-%m-%Y')}\n\n"
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
                        📄 Print / Download A3 PDF
                    </button>
                ''', unsafe_allow_html=True)

            user_db = load_db()
            if current_user_name in user_db:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_report = {
                    "timestamp": timestamp,
                    "user_note": st.session_state.current_comment,
                    "report_data": report_table
                }
                user_db[current_user_name]["history"].append(new_report)
                save_db(user_db)

    else:
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
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=400.0, key="bw_cr")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=2500.0, key="bw_sr")

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
                user_db = load_db()
                if current_user_name in user_db:
                    user_db[current_user_name]["comment"] = user_note.strip()
                    save_db(user_db)
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
            msg_text += f"📅 *Date:* {datetime.datetime.now().strftime('%d-%m-%Y')}\n\n"
            msg_text += f"📋 *DETAILS:*\n"
            msg_text += f"• Bricks: {total_bricks} Nos = ₹{total_brick_cost:.2f}\n"
            msg_text += f"• Cement: {cement_bags} Bags = ₹{total_cement_cost:.2f}\n"
            msg_text += f"• Sand: {sand_m3:.2f} m³ = ₹{total_sand_cost:.2f}\n"
            msg_text += f"• Labour: `{lab_cost:.2f}\n`"
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
                        📄 Print / Download A3 PDF
                    </button>
                ''', unsafe_allow_html=True)

            user_db = load_db()
            if current_user_name in user_db:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_report = {
                    "timestamp": timestamp,
                    "user_note": st.session_state.current_comment,
                    "report_data": report_table
                }
                user_db[current_user_name]["history"].append(new_report)
                save_db(user_db)

# ==========================================
# 🛑 MODULE 2: BBS (BAR BENDING SCHEDULE) MODULE
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

    master_rates = user_db.get("MASTER_MARKET_RATES", {"steel": 60.0})
    steel_rate_kg = st.number_input("आजचा स्टील दर (₹/Kg):", min_value=0.0, value=float(master_rates.get("steel", 60.0)), key="bbs_rate")

    st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
    user_note = st.text_area("या BBS बाबत काही नोंद लिहायची असल्यास इथे लिहा:", placeholder="उदा. Column C1 BBS Details...", key="bbs_note")
    if st.button("💬 कमेंट सबमिट करा", key="bbs_comment_btn"):
        if user_note.strip():
            st.session_state.current_comment = user_note.strip()
            user_db = load_db()
            if current_user_name in user_db:
                user_db[current_user_name]["comment"] = user_note.strip()
                save_db(user_db)
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
<p><strong>Prepared For:</strong> {current_user_name} | <strong>Component:</strong> {rcc_comp} | <strong>Date:</strong> {datetime.datetime.now().strftime('%d-%m-%Y')}</p>

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
        msg_text += f"📅 *Date:* {datetime.datetime.now().strftime('%d-%m-%Y')}\n"
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

        user_db = load_db()
        if current_user_name in user_db:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_report = {
                "timestamp": timestamp,
                "user_note": st.session_state.current_comment,
                "report_data": report_table
            }
            user_db[current_user_name]["history"].append(new_report)
            save_db(user_db)

[Gemini API Quickstart Guide](https://www.youtube.com/watch?v=vH2iMV2Y3dI)
http://googleusercontent.com/youtube_content/1
