# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import json
import os
import datetime
import pandas as pd
import time

# 🚨 Streamlit नियम: set_page_config नेहमी सर्वात आधी असावे!
st.set_page_config(page_title="PATIL INFRATECH", page_icon="🏗️", layout="centered")

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
# 🎨 ULTRA-MOBILE & CLEAN THEME STYLING (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Streamlit Header/Footer Hide */
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    footer { visibility: hidden; }
    
    /* Number Input +/- Hide */
    button[title="Increment"], button[title="Decrement"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }

    /* Modern Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Table Mobile Responsive Scroll */
    .stMarkdown table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        width: 100%;
        border-collapse: collapse;
    }
    .stMarkdown th, .stMarkdown td {
        padding: 8px 12px !important;
        border: 1px solid #374151 !important;
    }

    /* Universal Screen Touch Glow */
    .stApp:active {
        box-shadow: inset 0 0 50px rgba(59, 130, 246, 0.2) !important;
    }

    /* Card Styling */
    div.stForm, div[data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.8) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Inputs Theme Gray/Blue Border */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="popover"],
    input, select, textarea {
        border-color: #374151 !important;
        border-radius: 12px !important;
        background-color: #1f2937 !important;
        color: #ffffff !important;
        outline: none !important;
    }

    /* Focus Theme Blue Glow */
    div[data-baseweb="select"]:focus-within > div,
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="base-input"]:focus-within,
    input:focus, select:focus, textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 18px rgba(59, 130, 246, 0.5) !important;
        outline: none !important;
    }

    /* Primary Buttons Red Gradient */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #dc2626 100%, #dc2626 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    div.stButton > button[kind="primary"]:active {
        transform: scale(0.98);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.8) !important;
    }

    /* Normal Buttons Dark Blue Accent */
    div.stButton > button:not([kind="primary"]) {
        border-radius: 12px !important;
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #374151 !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:not([kind="primary"]):active {
        transform: scale(0.96);
        box-shadow: 0 0 18px rgba(59, 130, 246, 0.5) !important;
    }

    /* Mobile Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 22px 15px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.35);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# 📂 फाईल डेटाबेस मॅनेजमेंट
DB_FILE = "users_db.json"

def load_db():
    db = {
        "9999999999": {
            "id": "kanha", 
            "password": "patiladmin123",
            "comment": "मास्टर ॲडमीन अकाउंट",
            "admin_message": "मास्टर ॲडमीन",
            "history": []
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

# सेशन स्टेट इनिशियलायझेशन
if "app_user_name" not in st.session_state:
    st.session_state.app_user_name = None
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None

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
                new_welcome_msg = f"Welcome {u_input} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये हार्दिक स्वागत🥳"
                user_db[u_input] = {
                    "id": u_input,
                    "comment": "काही नाही",
                    "admin_message": new_welcome_msg,
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
        if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
            st.success("🔓 डेटाबेस अनलॉक झाला!")
            user_db = load_db()
            
            st.markdown("### 📈 Update Master Market Rates (Today's Live Rates)")
            m_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
            
            adm_cem = st.number_input("cement (par bag ₹):", min_value=0.0, value=float(m_rates.get("cement", 400.0)), step=1.0, key="adm_cem_inp_fixed")
            adm_snd = st.number_input("sand (par m³ ₹):", min_value=0.0, value=float(m_rates.get("sand", 2500.0)), step=1.0, key="adm_snd_inp_fixed")
            adm_brk = st.number_input("brick (nos ₹):", min_value=0.0, value=float(m_rates.get("bricks", 8.0)), step=0.1, key="adm_brk_inp_fixed")
            adm_agg = st.number_input("aggregate (par m³ ₹):", min_value=0.0, value=float(m_rates.get("aggregate", 2200.0)), step=1.0, key="adm_agg_inp_fixed")
            adm_ste = st.number_input("steel दर (per kg ₹):", min_value=0.0, value=float(m_rates.get("steel", 60.0)), step=1.0, key="adm_ste_inp_fixed")
            
            if st.button("💾 Save Master Market Rates", key="save_master_rates_fixed"):
                user_db["MASTER_MARKET_RATES"] = {
                    "cement": adm_cem, "sand": adm_snd, "bricks": adm_brk, "aggregate": adm_agg, "steel": adm_ste
                }
                save_db(user_db)
                st.success("✅ आजचे मास्टर मार्केट दर (स्टीलसहित) डेटाबेसमध्ये यशस्वीरित्या अपडेट झाले!")
            
            st.markdown("---")
            st.markdown("### 📋 युझर डेटाबेस MASTER LIST")
            
            for mob in list(user_db.keys()):
                if mob in ["9999999999", "MASTER_MARKET_RATES"]: continue
                info = user_db[mob]
                if not isinstance(info, dict): continue
                    
                u_name = info.get("id", mob)
                u_comm = info.get("comment", "काही नाही")
                u_hist = info.get("history", [])
                
                user_info_table = f"""
|DateField | माहिती (User Details) |
| :--- | :--- |
| **👤 युझरचे नाव (Name)** | {u_name} |
| **💬 शेवटची युझर कमेंट** | {u_comm} |
"""
                st.markdown(user_info_table)
                
                if st.button(f"🗑️ Delete User: {u_name}", key=f"del_{mob}"):
                    del user_db[mob]
                    save_db(user_db)
                    st.error(f"❌ युझर '{u_name}' यशस्वीरित्या डिलीट केला आहे!")
                    st.rerun()
                
                current_msg = info.get("admin_message", "ॲडमीन कडून सध्या कोणताही मेसेज नाही.")
                st.caption(f"📩 सध्याचा मेसेज: {current_msg}")
                new_msg = st.text_input(f"✍️ {u_name} साठी नवीन मेसेज टाईप करा:", key=f"msg_{mob}")
                if st.button(f"✉️ मेसेज पाठवा ({u_name})", key=f"btn_msg_{mob}"):
                    if new_msg.strip():
                        user_db[mob]["admin_message"] = new_msg.strip()
                        save_db(user_db)
                        st.success(f"✅ '{u_name}' ला मेसेज यशस्वीरित्या पाठवला!")
                        st.rerun()
                
                with st.expander(f"📜 {u_name} चे जनरेट केलेले एस्टिमेशन रिपोर्ट्स ({len(u_hist)})"):
                    if u_hist:
                        for idx, hist in enumerate(u_hist, 1):
                            if isinstance(hist, dict):
                                st.markdown(f"🗓️ **रिपोर्ट क्रमांक {idx} | तारीख व वेळ: `{hist.get('timestamp', 'N/A')}`**")
                                st.markdown(f"* **या कामाची विशिष्ट कमेंट:** {hist.get('user_note', 'काही नाही')}")
                                st.markdown(hist.get("report_data", "डेटा उपलब्ध नाही"))
                                st.write("---")
                    else:
                        st.info("ℹ️ या युझरने अजून एकही रिपोर्ट जनरेट केलेला नाही.")
                st.markdown("---")
        elif admin_id or admin_pass:
            st.error("❌ चुकीचा Admin ID किंवा Password!")
            
    st.stop()

# सध्याचा ॲक्टिव्ह युझर
current_user_name = st.session_state.app_user_name
user_db = load_db()

# युझर हेडर व चेंज बटण
col_u, col_lo = st.columns([3.5, 1.5])
col_u.success(f"👤 युझर: **{current_user_name}**")
if col_lo.button("🔄 नाव बदला"):
    st.session_state.app_user_name = None
    st.session_state.current_comment = "काही नाही"
    st.session_state.selected_module = None
    st.session_state.welcome_completed = False
    st.rerun()

current_user_data = user_db.get(current_user_name, {})
admin_msg = current_user_data.get("admin_message", None)
if admin_msg:
    st.markdown("### 📥 ॲडमीन कडून आलेला मेसेज (Inbox)")
    st.info(f"📢 **kanha:** {admin_msg}")
    st.write("---")

# ==========================================
# 🎛️ DASHBOARD / ICON SELECTION SCREEN
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("### 🚀 तुम्हाला काय करायचे आहे ते निवडा:")
    
    col_icon1, col_icon2 = st.columns(2)
    
    with col_icon1:
        st.markdown("""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 20px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 50px; margin:0;">📊</h1>
                <h3 style="margin: 10px 0 5px 0; color: #f3f4f6;">Rate Analysis</h3>
                <p style="font-size: 12px; color: #9ca3af;">दर विश्लेषण (काँक्रीट व वीटकाम)</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Open Rate Analysis", key="btn_open_ra", use_container_width=True):
            st.session_state.selected_module = "Rate Analysis"
            st.rerun()

    with col_icon2:
        st.markdown("""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 20px; border-radius: 18px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 50px; margin:0;">🏗️</h1>
                <h3 style="margin: 10px 0 5px 0; color: #f3f4f6;">BBS</h3>
                <p style="font-size: 12px; color: #9ca3af;">Bar Bending Schedule</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏗️ Open BBS", key="btn_open_bbs", use_container_width=True):
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
        user_note = st.text_area("कृपया आपला मौल्यवान फीडबॅक अवश्य द्या🙏:", placeholder="अँप मध्ये नवीन फिचर्स हवे असतील तर नक्की कळवा", key="cc_note")
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
# 🛑 MODULE 2: BBS (BAR BENDING SCHEDULE) MODULE - EASY UNIT SELECTION
# ==========================================
elif st.session_state.selected_module == "BBS":
    if st.button("⬅️ मुख्य मेनूवर जा (Back to Main)", key="btn_back_to_main_bbs"):
        st.session_state.selected_module = None
        st.rerun()
        
    st.write("---")
    st.subheader("🏗️ Bar Bending Schedule (BBS Calculator)")
    st.caption("100% Precise Standard IS 2502 & IS 456 Calculations")

    # १. RCC घटक निवडणे
    rcc_component = st.selectbox("🧱 RCC घटक निवडा (Select RCC Component):", 
                                 ["Footing (फुटिंग)", "Column (खांब/कॉलम)", "Beam (बीम)", "Slab (छत/स्लॅब)"])

    st.markdown("#### 📐 घटकाची आकाराची माहिती (Enter L, B, H Dimensions)")
    
    # 💡 L, B, H साठी मोकळे इनपुट बॉक्सेस (Blank Values)
    col_l, col_w, col_d = st.columns(3)
    with col_l:
        val_L = st.number_input("लांबी L (Length):", min_value=0.0, value=None, placeholder="उदा. 10 किंवा 3", key="bbs_val_L")
    with col_w:
        val_W = st.number_input("रुंदी B (Width):", min_value=0.0, value=None, placeholder="उदा. 1.5 किंवा 0.3", key="bbs_val_W")
    with col_d:
        val_D = st.number_input("उंची / खोली H (Depth):", min_value=0.0, value=None, placeholder="उदा. 12 किंवा 0.45", key="bbs_val_D")

    # 💡 युनिट विचारणे (Meters, Feet, Inches)
    unit_type = st.radio("❓ **वरील L, B, H आकडे कशात आहेत? (Select Dimension Unit):**", 
                         ["Meters (m)", "Feet (ft)", "Inches (in)"], horizontal=True)

    # Auto Cover Values (Standard IS 456)
    if "Footing" in rcc_component: default_cover_mm = 50
    elif "Column" in rcc_component: default_cover_mm = 40
    elif "Beam" in rcc_component: default_cover_mm = 25
    else: default_cover_mm = 15 # Slab

    clear_cover_mm = st.number_input("क्लियर कव्हर (Clear Cover in mm):", min_value=10, value=default_cover_mm, step=5, key=f"bbs_cov_{rcc_component}")
    cover_m = clear_cover_mm / 1000.0

    # 🎯 ACCURATE UNIT CONVERSION TO METERS INTERNAL
    L, W, D = 0.0, 0.0, 0.0
    if val_L is not None and val_W is not None and val_D is not None:
        if "Meters" in unit_type:
            L, W, D = float(val_L), float(val_W), float(val_D)
        elif "Feet" in unit_type:
            L, W, D = float(val_L) * 0.3048, float(val_W) * 0.3048, float(val_D) * 0.3048
        elif "Inches" in unit_type:
            L, W, D = float(val_L) * 0.0254, float(val_W) * 0.0254, float(val_D) * 0.0254

    st.markdown("---")
    st.markdown("#### 🔩 स्टील बार तपशील (Bar Details)")

    bbs_rows = []
    calc_note_marathi = ""

    # ==================== 1. Footing Logic ====================
    if "Footing" in rcc_component:
        col_f_m1, col_f_m2 = st.columns(2)
        with col_f_m1:
            dia_main = st.selectbox("X-Direction Bar Dia (mm):", [8, 10, 12, 16, 20], index=2)
            spacing_main = st.number_input("X-Direction Spacing (mm):", min_value=50, value=150, step=25)
        with col_f_m2:
            dia_dist = st.selectbox("Y-Direction Bar Dia (mm):", [8, 10, 12, 16, 20], index=2)
            spacing_dist = st.number_input("Y-Direction Spacing (mm):", min_value=50, value=150, step=25)

        if st.button("📊 GENERATE BBS REPORT", type="primary", key="gen_bbs_footing"):
            if L <= 0 or W <= 0 or D <= 0:
                st.warning("⚠️ कृपया आधी L, B आणि H च्या सर्व व्हॅल्यू भरून घ्या!")
            else:
                d_m, d_d = dia_main / 1000.0, dia_dist / 1000.0

                eff_L = L - (2 * cover_m)
                nos_X = math.ceil((W - 2 * cover_m) / (spacing_main / 1000.0)) + 1
                bend_len_X = 2 * (D - 2 * cover_m)
                cut_len_m_X = eff_L + bend_len_X - (2 * 2 * d_m)
                tot_len_m_X = cut_len_m_X * nos_X
                wt_X = tot_len_m_X * ((dia_main ** 2) / 162.0)

                eff_W = W - (2 * cover_m)
                nos_Y = math.ceil((L - 2 * cover_m) / (spacing_dist / 1000.0)) + 1
                bend_len_Y = 2 * (D - 2 * cover_m)
                cut_len_m_Y = eff_W + bend_len_Y - (2 * 2 * d_d)
                tot_len_m_Y = cut_len_m_Y * nos_Y
                wt_Y = tot_len_m_Y * ((dia_dist ** 2) / 162.0)

                bbs_rows.append({"desc": f"Main Bar (X-Dir {dia_main}mm)", "nos": nos_X, "dia": dia_main, "cut_len_m": cut_len_m_X, "tot_len_m": tot_len_m_X, "wt": wt_X})
                bbs_rows.append({"desc": f"Distribution Bar (Y-Dir {dia_dist}mm)", "nos": nos_Y, "dia": dia_dist, "cut_len_m": cut_len_m_Y, "tot_len_m": tot_len_m_Y, "wt": wt_Y})

                calc_note_marathi = f"""
📌 **कॅल्क्युलेशन नोट (Footing Calculation Breakdown):**
* **इनपुट युनिट:** L, B, H चे आकडे तुम्ही **{unit_type}** मध्ये दिले होते. ॲपमध्ये अचूकतेसाठी त्याचे मीटरमध्ये रुपांतर करून कॅल्क्युलेशन केले आहे.
* **वापरलेले बार:** X-दिशा {dia_main}mm Main Bar & Y-दिशा {dia_dist}mm Distribution Bar.
* **काय Add केले (+):** फुटिंगचे दोन्ही बाजूंचे L-Bend म्हणजेच $2 \\times (Depth - 2 \\times Clear Cover)$.
* **काय Minus केले (-):** Clear Cover ({clear_cover_mm}mm) आणि ९०° Bends Deducation ($2 \\times 2d$).
* **एकूण वजन मोजण्याची पद्धत:** $\\text{{Weight (Kg)}} = \\frac{{d^2}}{{162}} \\times \\text{{Total Length (m)}}$.
"""

    # ==================== 2. Column Logic ====================
    elif "Column" in rcc_component:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            dia_col_main = st.selectbox("Main Bar Dia (mm):", [12, 16, 20, 25], index=1)
            bar_spacing_col = st.number_input("Main Bars Spacing / Gap (mm):", min_value=100, value=150, step=25)
        with col_c2:
            dia_stirrup = st.selectbox("Stirrup Dia (mm):", [6, 8, 10], index=1)
            spacing_stirrup = st.number_input("Stirrup Spacing (mm):", min_value=75, value=150, step=25)

        if st.button("📊 GENERATE BBS REPORT", type="primary", key="gen_bbs_column"):
            if L <= 0 or W <= 0 or D <= 0:
                st.warning("⚠️ कृपया आधी L, B आणि H च्या सर्व व्हॅल्यू भरून घ्या!")
            else:
                d_main, d_st = dia_col_main / 1000.0, dia_stirrup / 1000.0

                core_L = L - (2 * cover_m)
                core_W = W - (2 * cover_m)
                sp_m = bar_spacing_col / 1000.0
                
                side1_extra = max(0, math.floor(core_L / sp_m) - 1)
                side2_extra = max(0, math.floor(core_W / sp_m) - 1)
                nos_col_main = 4 + (2 * side1_extra) + (2 * side2_extra)

                ld_m = 50 * d_main
                cut_len_m_main = D + ld_m
                tot_len_m_main = cut_len_m_main * nos_col_main
                wt_main = tot_len_m_main * ((dia_col_main ** 2) / 162.0)

                a = L - (2 * cover_m)
                b = W - (2 * cover_m)
                hook_len = 2 * 10 * d_st
                bend_ded = (3 * 2 * d_st) + (2 * 3 * d_st)
                cut_len_m_st = (2 * (a + b)) + hook_len - bend_ded
                nos_st = math.ceil(D / (spacing_stirrup / 1000.0)) + 1
                tot_len_m_st = cut_len_m_st * nos_st
                wt_st = tot_len_m_st * ((dia_stirrup ** 2) / 162.0)

                bbs_rows.append({"desc": f"Main Bar ({dia_col_main}mm - {nos_col_main} Nos)", "nos": nos_col_main, "dia": dia_col_main, "cut_len_m": cut_len_m_main, "tot_len_m": tot_len_m_main, "wt": wt_main})
                bbs_rows.append({"desc": f"Stirrup ({dia_stirrup}mm)", "nos": nos_st, "dia": dia_stirrup, "cut_len_m": cut_len_m_st, "tot_len_m": tot_len_m_st, "wt": wt_st})

                calc_note_marathi = f"""
📌 **कॅल्क्युलेशन नोट (Column Calculation Breakdown):**
* **इनपुट युनिट:** L, B, H चे आकडे तुम्ही **{unit_type}** मध्ये दिले होते. ॲपमध्ये अचूकतेसाठी त्याचे मीटरमध्ये रुपांतर करून कॅल्क्युलेशन केले आहे.
* **वापरलेले बार:** {dia_col_main}mm Main Bar & {dia_stirrup}mm Stirrup.
* **काय Add केले (+):** Main Bar मध्ये Development Length ($L_d = 50d$) आणि Stirrup मध्ये $2 \\times 10d$ Hook Length.
* **काय Minus केले (-):** Stirrup साठी चारही बाजूंचे Clear Cover ({clear_cover_mm}mm) आणि Bends Deducation ($3 \\times 2d$ [९०°] + $2 \\times 3d$ [१३५°]).
* **ऑटो बार संख्या:** कॉलम साईझनुसार ऑटो {nos_col_main} Main Bars मोजले आहेत.
"""

    # ==================== 3. Beam Logic ====================
    elif "Beam" in rcc_component:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            dia_b_bot = st.selectbox("Main Bar Dia (mm):", [12, 16, 20, 25], index=1)
            dia_b_top = st.selectbox("Top Anchor Bar Dia (mm):", [10, 12, 16], index=1)
            main_spacing_beam = st.number_input("Main Bar Spacing (mm):", min_value=100, value=150, step=25)
        with col_b2:
            dia_b_st = st.selectbox("Stirrup Dia (mm):", [6, 8, 10], index=1)
            spacing_b_st = st.number_input("Stirrup Spacing (mm):", min_value=75, value=150, step=25)

        if st.button("📊 GENERATE BBS REPORT", type="primary", key="gen_bbs_beam"):
            if L <= 0 or W <= 0 or D <= 0:
                st.warning("⚠️ कृपया आधी L, B आणि H च्या सर्व व्हॅल्यू भरून घ्या!")
            else:
                d_bot, d_top, d_st = dia_b_bot / 1000.0, dia_b_top / 1000.0, dia_b_st / 1000.0

                core_width = W - (2 * cover_m)
                nos_b_bot = max(2, math.ceil(core_width / (main_spacing_beam / 1000.0)) + 1)
                nos_b_top = 2

                d_dev = 50 * d_bot
                cut_len_m_bot = L - (2 * cover_m) + (2 * d_dev) - (2 * 2 * d_bot)
                tot_len_bot = cut_len_m_bot * nos_b_bot
                wt_bot = tot_len_bot * ((dia_b_bot ** 2) / 162.0)

                cut_len_m_top = L - (2 * cover_m) + (2 * 12 * d_top)
                tot_len_top = cut_len_m_top * nos_b_top
                wt_top = tot_len_top * ((dia_b_top ** 2) / 162.0)

                a = W - (2 * cover_m)
                b = D - (2 * cover_m)
                cut_len_st = (2 * (a + b)) + (20 * d_st) - (5 * 2 * d_st)
                nos_st = math.ceil(L / (spacing_b_st / 1000.0)) + 1
                tot_len_st = cut_len_st * nos_st
                wt_st = tot_len_st * ((dia_b_st ** 2) / 162.0)

                bbs_rows.append({"desc": f"Main Bar ({dia_b_bot}mm Bottom)", "nos": nos_b_bot, "dia": dia_b_bot, "cut_len_m": cut_len_m_bot, "tot_len_m": tot_len_bot, "wt": wt_bot})
                bbs_rows.append({"desc": f"Distribution Bar ({dia_b_top}mm Top Anchor)", "nos": nos_b_top, "dia": dia_b_top, "cut_len_m": cut_len_m_top, "tot_len_m": tot_len_top, "wt": wt_top})
                bbs_rows.append({"desc": f"Stirrup ({dia_b_st}mm)", "nos": nos_st, "dia": dia_b_st, "cut_len_m": cut_len_st, "tot_len_m": tot_len_st, "wt": wt_st})

                calc_note_marathi = f"""
📌 **कॅल्क्युलेशन नोट (Beam Calculation Breakdown):**
* **इनपुट युनिट:** L, B, H चे आकडे तुम्ही **{unit_type}** मध्ये दिले होते. ॲपमध्ये अचूकतेसाठी त्याचे मीटरमध्ये रुपांतर करून कॅल्क्युलेशन केले आहे.
* **वापरलेले बार:** {dia_b_bot}mm Main Bar (Bottom), {dia_b_top}mm Top Anchor Bar & {dia_b_st}mm Stirrup.
* **काय Add केले (+):** Bottom Bar मध्ये Development Length ($2 \\times 50d$) आणि Top Bar मध्ये $2 \\times 12d$ Hooks.
* **काय Minus केले (-):** बीमच्या कडांचे Clear Cover ({clear_cover_mm}mm) आणि ९०° Bends Deducation ($2 \\times 2d$).
* **ऑटो बार संख्या:** रुंदीनुसार ऑटो {nos_b_bot} Bottom Main Bars मोजले आहेत.
"""

    # ==================== 4. Slab Logic ====================
    else:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            dia_s_main = st.selectbox("Main Crank Bar Dia (mm):", [8, 10, 12], index=1)
            spacing_s_main = st.number_input("Main Bar Spacing (mm):", min_value=100, value=150, step=25)
        with col_s2:
            dia_s_dist = st.selectbox("Distribution Bar Dia (mm):", [6, 8, 10], index=1)
            spacing_s_dist = st.number_input("Distribution Spacing (mm):", min_value=100, value=175, step=25)

        if st.button("📊 GENERATE BBS REPORT", type="primary", key="gen_bbs_slab"):
            if L <= 0 or W <= 0 or D <= 0:
                st.warning("⚠️ कृपया आधी L, B आणि H च्या सर्व व्हॅल्यू भरून घ्या!")
            else:
                d_main, d_dist = dia_s_main / 1000.0, dia_s_dist / 1000.0

                depth_d = D - (2 * cover_m) - d_main
                crank_len = 0.42 * depth_d 
                
                cut_len_s_main = L - (2 * cover_m) + (2 * crank_len) + (2 * 9 * d_main) - (4 * 1 * d_main) - (2 * 2 * d_main)
                nos_s_main = math.ceil(W / (spacing_s_main / 1000.0)) + 1
                tot_len_s_main = cut_len_s_main * nos_s_main
                wt_s_main = tot_len_s_main * ((dia_s_main ** 2) / 162.0)

                cut_len_s_dist = W - (2 * cover_m) + (2 * 9 * d_dist) - (2 * 2 * d_dist)
                nos_s_dist = math.ceil(L / (spacing_s_dist / 1000.0)) + 1
                tot_len_s_dist = cut_len_s_dist * nos_s_dist
                wt_s_dist = tot_len_s_dist * ((dia_s_dist ** 2) / 162.0)

                bbs_rows.append({"desc": f"Bentup Bar ({dia_s_main}mm Main Crank)", "nos": nos_s_main, "dia": dia_s_main, "cut_len_m": cut_len_s_main, "tot_len_m": tot_len_s_main, "wt": wt_s_main})
                bbs_rows.append({"desc": f"Distribution Bar ({dia_s_dist}mm Straight)", "nos": nos_s_dist, "dia": dia_s_dist, "cut_len_m": cut_len_s_dist, "tot_len_m": tot_len_s_dist, "wt": wt_s_dist})

                calc_note_marathi = f"""
📌 **कॅल्क्युलेशन नोट (Slab Calculation Breakdown):**
* **इनपुट युनिट:** L, B, H चे आकडे तुम्ही **{unit_type}** मध्ये दिले होते. ॲपमध्ये अचूकतेसाठी त्याचे मीटरमध्ये रुपांतर करून कॅल्क्युलेशन केले आहे.
* **वापरलेले बार:** {dia_s_main}mm Main Bentup Bar (45° Crank) & {dia_s_dist}mm Distribution Bar.
* **काय Add केले (+):** 45° Crank साठी वाढीव लांबी ($2 \\times 0.42d$) आणि दोन्ही टोकचे Hooks ($2 \\times 9d$).
* **काय Minus केले (-):** स्लॅबचे Clear Cover ({clear_cover_mm}mm) आणि Bends Deducation ($4 \\times 1d$ [45°] + $2 \\times 2d$ [90°]).
* **ऑटो बार संख्या:** Spacing नुसार {nos_s_main} Bentup Bars आणि {nos_s_dist} Distribution Bars मोजले आहेत.
"""

    # ==================== DISPLAY CLEAN TABLE FORMAT ====================
    if bbs_rows:
        st.success("🎉 BAR BENDING SCHEDULE (BBS) यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 BBS REPORT - {rcc_component.split(' ')[0].upper()}")
        st.info(f"👤 **Prepared For:** {current_user_name} | **Input Dimension Unit:** {unit_type}")

        total_weight_kg = sum(r["wt"] for r in bbs_rows)
        
        table_markdown = "| Description | Nos | Dia (mm) | Cutting Length (m) | Total Length (m) | Weight (kg) |\n"
        table_markdown += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"

        for row in bbs_rows:
            table_markdown += f"| **{row['desc']}** | {row['nos']} | {row['dia']} | {row['cut_len_m']:.3f} m | {row['tot_len_m']:.2f} m | **{row['wt']:.2f}** |\n"

        table_markdown += f"| **GRAND TOTAL WEIGHT (KG)** | - | - | - | - | **{total_weight_kg:.2f} Kg** |\n"
        table_markdown += f"| **GRAND TOTAL WEIGHT (TONNES)** | - | - | - | - | **{(total_weight_kg/1000.0):.3f} Ton** |\n"

        st.markdown(table_markdown)

        # 💡 मराठी टेक्निकल नोट डिस्प्ले
        if calc_note_marathi:
            st.info(calc_note_marathi)

        user_db = load_db()
        if current_user_name in user_db:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_report_save = table_markdown + "\n\n" + calc_note_marathi
            new_report = {
                "timestamp": timestamp,
                "user_note": f"BBS Report - {rcc_component}",
                "report_data": full_report_save
            }
            user_db[current_user_name]["history"].append(new_report)
            save_db(user_db)
