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
st.set_page_config(page_title="PATIL INFRATECH", page_icon="📐", layout="centered")

# --- १. अॅनिमेशन आणि सुरुवातीच्या सुंदर लूकसाठी रिकामी जागा तयार करणे ---
welcome_placeholder = st.empty()

# जर युझरने स्कीप बटण दाबले असेल, तर थेट लॉगिन सुरू होईल
if 'skip_welcome' not in st.session_state:
    st.session_state.skip_welcome = False

if not st.session_state.skip_welcome:
    with welcome_placeholder.container():
        # संपूर्ण स्क्रीनवर क्लिक करण्यासाठी अदृश्य (Transparent) बटण बनवणारे CSS
        st.markdown("""
            <style>
            div.stButton > button {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: transparent !important; border: none !important;
                color: transparent !important; z-index: 99999; cursor: pointer;
            }
            div.stButton > button:hover { background-color: transparent !important; border: none !important; }
            div.stButton > button:active { background-color: transparent !important; border: none !important; }
            </style>
        """, unsafe_allow_html=True)
        
        # स्क्रीनवर कुठेही टच/क्लिक केल्यास हे बटण ट्रिगर होईल
        if st.button("Skip", key="invisible_skip_btn"):
            st.session_state.skip_welcome = True
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        # सुंदर हेडिंग
        st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🏗️ WELCOME TO THE PATIL INFRATECH...</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #555555;'>तुमचे स्वप्न, आमचे एस्टिमेशन!</h3>", unsafe_allow_html=True)
        
        # घर बनताना दाखवणारे प्रोग्रेस बार अॅनिमेशन
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # एकूण १० सेकंदांचे टप्पे
        construction_stages = [
            "🧱 पाया खोदण्याचे काम सुरू आहे...",
            "🏗️ खांब आणि कॉलम उभे राहत आहेत...",
            "🧱 विटांचे बांधकाम (Brickwork) प्रगतीपथावर आहे...",
            "🏠 छताचे (Slab) काम पूर्ण होत आहे...",
            "✨ फिनिशिंग आणि रंगकाम पूर्ण झाले! घर तयार आहे! 🎉"
        ]
        st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech)")
        
        for i in range(5):
            status_text.markdown(f"<p style='text-align: center; font-size: 20px; font-weight: bold;'>{construction_stages[i]}</p>", unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 20)
            time.sleep(2)  # ५ टप्पे * २ सेकंद = एकूण १० सेकंद

    # १० सेकंद पूर्ण झाल्यावर स्क्रीन क्लिअर करणे
    welcome_placeholder.empty()
    st.session_state.skip_welcome = True

# CSS जुगाड: टॉप हेडर, फुटर आणि नंबर इनपुट मधील +/- बटणे लपवण्यासाठी
st.markdown("""
    <style>
    /* Streamlit चा टॉप हेडर गायब करणे */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    /* खालचा फुटर काढून टाकणे */
    footer {
        visibility: hidden;
    }
    /* number input मधील + आणि - बटणे लपवण्यासाठी */
    button[title="Increment"], button[title="Decrement"] {
        display: none !important;
    }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 📂 कायमस्वरूपी फाईल डेटाबेस मॅनेजमेंट
DB_FILE = "users_db.json"

def load_db():
    db = {
        "9999999999": {
            "id": "kanha", 
            "password": "patiladmin123",
            "comment": "मास्टर ॲडमीन अकाउंट",
            "admin_message": "मास्टर ॲडमीन",
            "saved_rates": {},
            "history": []
        },
        "MASTER_MARKET_RATES": {
            "cement": 400.0,
            "sand": 2500.0,
            "bricks": 8.0,
            "aggregate": 2200.0
        }
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                old_db = json.load(f)
                if isinstance(old_db, dict):
                    for key, val in old_db.items():
                        db[key] = val
        except:
            pass
    if "MASTER_MARKET_RATES" not in db:
        db["MASTER_MARKET_RATES"] = {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0}
    return db

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

# डेटाबेस लोड करा
user_db = load_db()

# सेशन स्टेट इनिशियलायझेशन
if "app_user_mobile" not in st.session_state:
    st.session_state.app_user_mobile = None
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "active_report" not in st.session_state:
    st.session_state.active_report = None
if "applied_market_rates" not in st.session_state:
    st.session_state.applied_market_rates = False

# मुख्य टायटल
st.title("🏗️ PATIL INFRATECH")
st.subheader("📐 Quantity Surveyor & Cost Estimator")
st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech)")
st.write("---")

# ==========================================
# 🔑 लॉगिन आणि साइन-अप सिस्टीम
# ==========================================
if st.session_state.app_user_mobile is None:
    st.markdown("### 🔐 लॉगिन करा किंवा नवीन खाते बनवा (पर्यायी)")
    tab1, tab2, tab3 = st.tabs(["🔑 लॉगिन (Login)", "📝 नवीन खाते (Sign Up)", "👤 Guest म्हणून पुढे जा"])
    
    with tab1:
        l_mobile = st.text_input("१० अंकी मोबाईल नंबर:", key="l_mob").strip()
        l_pass = st.text_input("पासवर्ड प्रविष्ट करा:", type="password", key="l_pwd")
        if st.button("लॉगिन करा", type="primary"):
            user_db = load_db()
            if not l_mobile or not l_pass:
                st.warning("⚠️ कृपया मोबाईल नंबर आणि पासवर्ड दोन्ही भरा!")
            elif l_mobile in user_db:
                if user_db[l_mobile].get("password") == l_pass:
                    st.session_state.app_user_mobile = l_mobile
                    
                    # 🔄 लॉगिन करताना मेसेज अपडेट करणे (नवीन कडक मेसेज 🥳)
                    u_name = user_db[l_mobile].get("id", "युझर")
                    new_welcome_msg = f"Wellcome {u_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये हार्दिक स्वागत🥳"
                    user_db[l_mobile]["admin_message"] = new_welcome_msg
                    save_db(user_db)
                    
                    st.success(f"🔓 लॉगिन यशस्वी! स्वागत आहे {u_name}")
                    st.rerun()
                else:
                    st.error("❌ चुकीचा पासवर्ड! कृपया पुन्हा तपासा.")
            else:
                st.error("❌ हा मोबाईल नंबर रजिस्टर नाही! आधी 'नवीन खाते' टॅबमध्ये जाऊन रजिस्ट्रेशन करा.")
                
    with tab2:
        r_name = st.text_input("तुमचे पूर्ण नाव (Full Name):", key="r_nm").strip()
        r_mobile = st.text_input("१० अंकी मोबाईल नंबर (Mobile No):", key="r_mob").strip()
        r_pass = st.text_input("नवीन पासवर्ड तयार करा:", type="password", key="r_pwd")
        if st.button("खाते तयार करा"):
            user_db = load_db()
            if not r_name or not r_mobile or not r_pass:
                st.warning("⚠️ कृपया सर्व रकाने भरा!")
            elif len(r_mobile) != 10 or not r_mobile.isdigit():
                st.error("❌ कृपया वैध १० अंकी मोबाईल नंबर टाका!")
            elif r_mobile in user_db:
                st.error("❌ हा मोबाईल नंबर आधीपासूनच रजिस्टर आहे!")
            else:
                # 🔄 साईन अप करतानाच नवीन ऑटोमॅटिक मेसेज सेट करणे 🥳
                new_welcome_msg = f"Wellcome {r_name} मी कन्हैया आपले पाटील इन्फ्राटेक मध्ये हार्दिक स्वागत🥳"
                user_db[r_mobile] = {
                    "id": r_name, 
                    "password": r_pass,
                    "comment": "काही नाही",
                    "admin_message": new_welcome_msg,
                    "saved_rates": {},
                    "history": []
                }
                save_db(user_db)
                st.success("🎉 खाते यशस्वीरित्या तयार झाले! अब बाजूच्या 'लॉगिन' टॅबमध्ये जाऊन लॉग इन करा.")
                
    with tab3:
        guest_name = st.text_input("तुमचे नाव प्रविष्ट करा (Enter Name):", placeholder="नाव टाईप करा...", key="gst_nm")
        if st.button("Guest म्हणून पुढे जा 👉", type="secondary"):
            if guest_name.strip():
                st.session_state.app_user_mobile = "GUEST_" + guest_name.strip()
                st.rerun()
            else:
                st.warning("⚠️ कृपया पुढे जाण्यासाठी नाव प्रविष्ट करा!")
                
    # 🛡️ सुरक्षित ॲडमीन पॅनल
    st.write("---")
    with st.expander("🛡️ Admin Database Panel (only kanhaiya)"):
        admin_id = st.text_input("Admin ID:", key="adm_id")
        admin_pass = st.text_input("Password:", type="password", key="adm_pass")
        if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
            st.success("🔓 डेटाबेस अनलॉक झाला!")
            user_db = load_db()
            
            # 📈 ॲडमीन मास्टर मार्केट रेट्स अपडेट विभाग
            st.markdown("### 📈 Update Master Market Rates (Today's Live Rates)")
            m_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0})
            adm_cem = st.number_input("मास्टर सिमेंट दर (प्रति बॅग ₹):", min_value=0.0, value=float(m_rates["cement"]), step=1.0)
            adm_snd = st.number_input("मास्टर वाळू दर (प्रति m³ ₹):", min_value=0.0, value=float(m_rates["sand"]), step=1.0)
            adm_brk = st.number_input("मास्टर विटा दर (प्रति नग ₹):", min_value=0.0, value=float(m_rates["bricks"]), step=0.1)
            adm_agg = st.number_input("मास्टर खडी दर (प्रति m³ ₹):", min_value=0.0, value=float(m_rates["aggregate"]), step=1.0)
            
            if st.button("💾 Save Master Market Rates", type="primary"):
                user_db["MASTER_MARKET_RATES"] = {"cement": adm_cem, "sand": adm_snd, "bricks": adm_brk, "aggregate": adm_agg}
                save_db(user_db)
                st.success("✅ आजचे मास्टर मार्केट दर डेटाबेसमध्ये यशस्वीरित्या अपडेट झाले!")
            
            st.markdown("---")
            st.markdown("### 📋 युझर डेटाबेस MASTER LIST")
            
            for mob in list(user_db.keys()):
                if mob in ["9999999999", "MASTER_MARKET_RATES"]: continue
                info = user_db[mob]
                if not isinstance(info, dict):
                    continue
                    
                u_name = info.get("id", "नाव उपलब्ध नाही")
                u_pass = info.get("password", "पासवर्ड उपलब्ध नाही")
                u_comm = info.get("comment", "काही नाही")
                u_hist = info.get("history", [])
                
                user_info_table = f"""
| फील्ड (Field) | माहिती (User Details) |
| :--- | :--- |
| **👤 युझरचे नाव (Name)** | {u_name} |
| **📱 मोबाईल नंबर (Mobile)** | `{mob}` |
| **🔑 पासवर्ड (Password)** | `{u_pass}` |
| **💬 शेवकडची युझर कमेंट** | {u_comm} |
"""
                st.markdown(user_info_table)
                
                if st.button(f"🗑️ Delete User: {u_name} ({mob})", key=f"del_{mob}"):
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
                    else:
                        st.warning("⚠️ कृपया आधी मेसेज टाईप करा!")
                
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

# सध्याचा ॲक्टिव्ह युझर आणि त्याचे सेव्ह केलेले दर लोड करणे
user_mob_key = st.session_state.app_user_mobile
user_db = load_db()

if user_mob_key.startswith("GUEST_"):
    current_user_name = user_mob_key.replace("GUEST_", "")
    saved_rates = {}
else:
    if user_mob_key in user_db:
        current_user_name = user_db[user_mob_key].get("id", "User")
        saved_rates = user_db[user_mob_key].get("saved_rates", {})
    else:
        current_user_name = "User"
        saved_rates = {}

# लॉगआऊट पर्याय
col_u, col_lo = st.columns([5, 1])
col_u.success(f"🔓 चालू युझर: **{current_user_name}** ({'Guest' if user_mob_key.startswith('GUEST_') else user_mob_key})")
if col_lo.button("🚪 Logout"):
    st.session_state.app_user_mobile = None
    st.session_state.current_comment = "काही नाही"
    st.session_state.active_report = None
    st.session_state.applied_market_rates = False
    st.rerun()

st.write("---")

# ==========================================
# 📊 SIDEBAR: TODAY'S MARKET RATE INTEGRATION
# ==========================================
master_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0})
with st.sidebar:
    st.markdown("### 📈 Today's Market Rate")
    st.write(f" bricks **विटा (Bricks):** ₹{master_rates['bricks']:.2f} /नग")
    st.write(f" cement **सिमेंट (Cement):** ₹{master_rates['cement']:.2f} /बॅग")
    st.write(f" sand **वाळू (Sand):** ₹{master_rates['sand']:.2f} /m³")
    st.write(f" agg **खडी (Aggregate):** ₹{master_rates['aggregate']:.2f} /m³")
    st.write("---")
    if st.button("⚡ Apply Today's Market Rates", type="primary", key="apply_market_rates_btn"):
        st.session_state.applied_market_rates = True
        st.success("✅ ॲडमीन मार्केट दर लागू केले गेले! खाली तपासून रिपोर्ट जनरेट करा.")

if not user_mob_key.startswith("GUEST_"):
    current_user_data = user_db.get(user_mob_key, {})
    admin_msg = current_user_data.get("admin_message", None)
    if admin_msg:
        st.markdown("### 📥 ॲडमीन कडून आलेला मेसेज (inbox)")
        st.info(f"📢 **kanha:** {admin_msg}")
        st.write("---")

# २. मुख्य काम निवडणे
main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)"])

# ==========================================
# 🛑 काँक्रीट काम (CONCRETE WORK MODULE)
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

    # 🔄 Fetch & Apply Market Rates Logic for Concrete
    def_cc_cem = master_rates["cement"] if st.session_state.applied_market_rates else saved_rates.get("c_cem_rate", 400.0)
    def_cc_snd = master_rates["sand"] if st.session_state.applied_market_rates else saved_rates.get("c_sand_rate", 2500.0)
    def_cc_agg = master_rates["aggregate"] if st.session_state.applied_market_rates else saved_rates.get("c_agg_rate", 2200.0)

    st.markdown("#### [A] साहित्याची माहिती आणि दर (थेट टाईप करा)")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, value=float(saved_rates.get("c_vol", 1.0)), step=0.001, key="cc_vol")
        cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, value=float(def_cc_cem), step=1.0, key="cc_cem_r")
        sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, value=float(def_cc_snd), step=1.0, key="cc_snd_r")
    with v_col2:
        aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, value=float(def_cc_agg), step=1.0, key="cc_agg_r")
        steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, value=float(saved_rates.get("c_steel_rate", 65.0)), step=1.0, key="cc_stl_r") if steel_percentage > 0 else 0.0

    st.markdown("#### [B] लेबर खर्च (नसल्यास ० ठेवा)")
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, value=float(saved_rates.get("c_mas_qty", 0.0)), step=1.0, key="cc_msn_q")
        mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=float(saved_rates.get("c_mas_rate", 600.0)), step=1.0, key="cc_msn_r")
    with l_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, value=float(saved_rates.get("c_maz_qty", 0.0)), step=1.0, key="cc_mzd_q")
        mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=float(saved_rates.get("c_maz_rate", 400.0)), step=1.0, key="cc_mzd_r")
    with l_col3:
        bb_qty = st.number_input("बार बेंडर संख्या:", min_value=0.0, value=float(saved_rates.get("c_bb_qty", 0.0)), step=1.0, key="cc_bb_q")
        bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=float(saved_rates.get("c_bb_rate", 550.0)), step=1.0, key="cc_bb_r")

    st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
    o_col1, o_col2 = st.columns(2)
    with o_col1:
        scaffolding_cost = st.number_input("स्कॅफोल्डिंग/सेंटरिंग खर्च (₹):", min_value=0.0, value=float(saved_rates.get("c_scaf", 0.0)), step=1.0, key="cc_scaf")
        contingency_cost = st.number_input("आकस्मिक खर्च (Contingencies) (₹):", min_value=0.0, value=float(saved_rates.get("c_cont", 0.0)), step=1.0, key="cc_cont")
    with o_col2:
        water_pct = st.number_input("वॉटर चार्ज टक्केवारी (%):", min_value=0.0, value=float(saved_rates.get("c_wat_pct", 1.0)), step=0.1, key="cc_wat_p")
        profit_pct = st.number_input("कंत्राटदार नफा टक्केवारी (%):", min_value=0.0, value=float(saved_rates.get("c_prof_pct", 10.0)), step=0.1, key="cc_prof_p")

    st.markdown("#### 💬 कमेंट पॅनल (Comment Panel)")
    user_note = st.text_area("कृपया आपला मौल्यवान फीडबॅक अवश्य द्या🙏:", placeholder="अँप मध्ये नवीन फिचर्स हवे असतील तर नक्की कळवा", key="cc_note")
    if st.button("💬 कमेंट सबमिट करा", key="cc_comm_btn"):
        if user_note.strip():
            st.session_state.current_comment = user_note.strip()
