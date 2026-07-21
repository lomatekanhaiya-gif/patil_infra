# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import json
import os
import datetime
import pandas as pd
import io
import time

# 🚨 Streamlit चा नियम: set_page_config नेहमी सर्वात आधी असावे!
st.set_page_config(page_title="PATIL INFRATECH", page_icon="🏗️", layout="centered")

# ==========================================
# 🎨 ULTRA-MOBILE & TOUCH-GLOW CUSTOM STYLING (CSS)
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

    /* Card Styling with Touch-Glow Effect */
    div.css-1r6slb0, div.stForm, div[data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.8) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease-in-out;
    }

    /* 🌟 Mobile Touch Glow Effects for Inputs & Focus */
    input:focus, select:focus, textarea:focus, div[data-baseweb="select"]:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.6) !important;
        outline: none !important;
        transition: all 0.2s ease-in-out;
    }

    /* Input Fields Styling */
    input, select, textarea {
        border-radius: 12px !important;
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        padding: 12px !important;
        font-size: 16px !important; /* Prevents auto-zoom on mobile Safari/Chrome */
    }

    /* Primary Action Buttons (Glow on Touch/Click) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ef4444 0%, #f87171 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    div.stButton > button[kind="primary"]:active, div.stButton > button[kind="primary"]:focus {
        transform: scale(0.98);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.8) !important;
    }

    /* Secondary Buttons Touch Glow */
    div.stButton > button {
        border-radius: 12px !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:active {
        transform: scale(0.96);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5) !important;
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

    /* Radio Buttons Touch Improvement */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- १. वेलकम स्क्रीन ॲनिमेशन ---
welcome_placeholder = st.empty()

if 'skip_welcome' not in st.session_state:
    st.session_state.skip_welcome = False

if not st.session_state.skip_welcome:
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
        
        if st.button("Skip", key="invisible_skip_btn"):
            st.session_state.skip_welcome = True
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>🏗️ WELCOME TO PATIL INFRATECH...</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #9ca3af;'>तुमचे स्वप्न, आमचे एस्टिमेशन!</h3>", unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        construction_stages = [
            "🧱 पाया खोदण्याचे काम सुरू आहे...",
            "🏗️ खांब आणि कॉलम उभे राहत आहेत...",
            "🧱 विटांचे बांधकाम (Brickwork) प्रगतीपथावर आहे...",
            "🏠 छताचे (Slab) काम पूर्ण होत आहे...",
            "✨ फिनिशिंग आणि रंगकाम पूर्ण झाले! घर तयार आहे! 🎉"
        ]
        st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech)")
        
        for i in range(5):
            status_text.markdown(f"<p style='text-align: center; font-size: 18px; font-weight: bold; color: #f3f4f6;'>{construction_stages[i]}</p>", unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 20)
            time.sleep(1.2)

    welcome_placeholder.empty()
    st.session_state.skip_welcome = True

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
if "active_report" not in st.session_state:
    st.session_state.active_report = None

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
            
            if st.button("💾 Save Master Market Rates", type="primary", key="save_master_rates_fixed"):
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
    st.session_state.active_report = None
    st.rerun()

# 📉 मास्टर मार्केट रेट्स बार
master_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
st.markdown(
    f"<div style='background: linear-gradient(90deg, #1f2937 0%, #111827 100%); padding: 12px; border-radius: 14px; text-align: center; font-size: 13px; font-weight: bold; color: #f3f4f6; margin-bottom: 15px; border-left: 5px solid #ef4444; border: 1px solid rgba(255,255,255,0.08); shadow: 0 0 10px rgba(0,0,0,0.5);'>"
    f"📢 आजचे मार्केट दर 🏷️ cement: ₹{master_rates['cement']}/bag | sand: ₹{master_rates['sand']}/m³ | aggregate: ₹{master_rates['aggregate']}/m³ | steel: ₹{master_rates['steel']}/Kg | brick: ₹{master_rates['bricks']}/nos"
    f"</div>", 
    unsafe_allow_html=True
)

current_user_data = user_db.get(current_user_name, {})
admin_msg = current_user_data.get("admin_message", None)
if admin_msg:
    st.markdown("### 📥 ॲडमीन कडून आलेला मेसेज (Inbox)")
    st.info(f"📢 **kanha:** {admin_msg}")
    st.write("---")

# २. मुख्य काम निवडणे
main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)"])

# ==========================================
# 🛑 काँक्रीट काम (CONCRETE WORK MODULE) - UNTOUCHED LOGIC
# ==========================================
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
        water_pct = st.number_input("वॉटर चार्ज टक्केवारी (%):", min_value=0.0, value=1.0, key="cc_wat_p")
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

# ==========================================
# 🛑 वीटकाम (BRICKWORK MODULE) - UNTOUCHED LOGIC
# ==========================================
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
        water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=1.0, key="bw_wp")
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
        
        st.session_state.active_report = {
            "type": "Brickwork",
            "grand_total": grand_total,
            "data": {
                "Description": ["Bricks", "Cement", "Sand", "GRAND TOTAL"],
                "Quantity": [total_bricks, cement_bags, round(sand_m3, 2), ""],
                "Unit": ["Nos", "Bags", "m³", ""],
                "Amount (INR)": [total_brick_cost, total_cement_cost, total_sand_cost, grand_total]
            },
            "txt": f"PATIL INFRATECH - BRICKWORK REPORT\nयुझर: {current_user_name}\nतारीख: {datetime.date.today()}\n----------------------------------------\n* विटा: {total_bricks} Nos\n* सिमेंट: {cement_bags} Bags\n* वाळू: {sand_m3:.2f} m3\n----------------------------------------\nGRAND TOTAL: INR {grand_total:.2f}/-"
        }

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
