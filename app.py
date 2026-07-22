# ==========================================
# PATIL INFRATECH - Quantity Surveyor & Cost Estimator
# Concept & Logic by: Kanhaiya (Founder of Patil Infratech)
# ==========================================

import streamlit as st
import math
import json
import os
import datetime
import hashlib
import time


# ==========================================
# --- १. वेलकम स्क्रीन ॲनिमेशन ---
# ==========================================
if not st.session_state.welcome_completed:
    welcome_placeholder = st.empty()
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
            status_text.markdown(f"<p style='text-align: center; font-size: 17px; font-weight: bold; color: #f3f4f6;'>{construction_stages[i]}</p>", unsafe_allow_html=True)
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.4)

    welcome_placeholder.empty()
    st.session_state.welcome_completed = True
    st.rerun()

# 🚨 Streamlit नियम: set_page_config सर्वात आधी असावे!
st.set_page_config(
    page_title="PATIL INFRATECH",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🔒 FULL SECURITY & UI CLEANUP (HIDE GITHUB & STREAMLIT MENU)
# ==========================================
st.markdown("""
    <style>
    /* Streamlit चा उजव्या कोपऱ्यातील GitHub/Deploy लोगो आणि मेनू लपवा */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important; height: 0px !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important; height: 0px !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    /* Number Input +/- Buttons Hide */
    button[title="Increment"], button[title="Decrement"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }

    /* Ultra Modern Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Responsive Mobile Tables */
    .stMarkdown table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        width: 100%;
        border-collapse: collapse;
    }
    .stMarkdown th, .stMarkdown td {
        padding: 10px 14px !important;
        border: 1px solid #374151 !important;
    }

    /* Cards & Containers */
    div.stForm, div[data-testid="stExpander"] {
        background: rgba(17, 24, 39, 0.85) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
        border-radius: 18px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Inputs Theme */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    input, select, textarea {
        border-color: #374151 !important;
        border-radius: 12px !important;
        background-color: #1f2937 !important;
        color: #ffffff !important;
    }

    /* Primary Red Buttons */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
        width: 100%;
    }

    /* Normal Buttons */
    div.stButton > button:not([kind="primary"]) {
        border-radius: 12px !important;
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #374151 !important;
    }

    /* Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 20px 15px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 SECURE DATABASE MANAGEMENT & HASHING
# ==========================================
DB_FILE = "users_db.json"

# SHA-256 पासवर्ड हॅशिंग फंक्शन (सुरक्षेसाठी)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# MASTER ADMIN CREDENTIAL HASH (@Dellg15 चा सुरक्षित Hash)
ADMIN_ID_HASH = hash_password("kanha_1p")
ADMIN_PASS_HASH = hash_password("@Dellg15")

def load_db():
    db = {
        "MASTER_MARKET_RATES": {
            "cement": 400.0,
            "sand": 2500.0,
            "bricks": 8.0,
            "aggregate": 2200.0,
            "steel": 60.0
        }
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                loaded_db = json.load(f)
                if isinstance(loaded_db, dict):
                    db.update(loaded_db)
        except Exception:
            pass
    return db

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"डेटा सेव्ह करताना त्रुटी आली: {e}")

user_db = load_db()

# Session State Initializations
if "welcome_completed" not in st.session_state:
    st.session_state.welcome_completed = False
if "app_user_name" not in st.session_state:
    st.session_state.app_user_name = None
if "current_comment" not in st.session_state:
    st.session_state.current_comment = "काही नाही"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None

# ==========================================
# 🔝 मुख्य टायटल बॅनर
# ==========================================
st.markdown("""
    <div class="main-header">
        <h1 style='color: white; margin:0; font-size: 24px;'>🏗️ PATIL INFRATECH</h1>
        <p style='color: #e0e7ff; margin:3px 0 0 0; font-size: 13px;'>📐 Quantity Surveyor & Cost Estimator</p>
        <small style='color: #93c5fd;'>Concept & Logic by: Kanhaiya (Founder of Patil Infratech)</small>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 👤 युझर नाव प्रविष्ट करणे / लॉगइन
# ==========================================
if st.session_state.app_user_name is None:
    st.markdown("### 👤 ॲपमध्ये प्रवेश करण्यासाठी नाव प्रविष्ट करा")
    u_input = st.text_input("तुमचे नाव (Your Name):", placeholder="NAME", key="entry_user_name").strip()
    
    if st.button("ॲप उघडा (Enter App) 👉", type="primary"):
        if u_input:
            st.session_state.app_user_name = u_input
            user_db = load_db()
            
            if u_input not in user_db:
                new_welcome_msg = f"Welcome {u_input}! मी कन्हैया, आपले पाटील इन्फ्राटेक मध्ये हार्दिक स्वागत🥳"
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
    
    # 🛡️ हॅक-प्रूफ सुरक्षित ॲडमीन पॅनल
    with st.expander("🛡️ Admin Database Panel (Only Kanhaiya)"):
        admin_id = st.text_input("Admin ID:", key="adm_id")
        admin_pass = st.text_input("Password:", type="password", key="adm_pass")
        
        if admin_id or admin_pass:
            if hash_password(admin_id) == ADMIN_ID_HASH and hash_password(admin_pass) == ADMIN_PASS_HASH:
                st.success("🔓 डेटाबेस सुरक्षितपणे अनलॉक झाला!")
                user_db = load_db()
                
                st.markdown("### 📈 Update Master Market Rates")
                m_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
                
                adm_cem = st.number_input("Cement (प्रति बॅग ₹):", min_value=0.0, value=float(m_rates.get("cement", 400.0)), key="adm_cem")
                adm_snd = st.number_input("Sand (प्रति m³ ₹):", min_value=0.0, value=float(m_rates.get("sand", 2500.0)), key="adm_snd")
                adm_brk = st.number_input("Brick (प्रति नग ₹):", min_value=0.0, value=float(m_rates.get("bricks", 8.0)), key="adm_brk")
                adm_agg = st.number_input("Aggregate (प्रति m³ ₹):", min_value=0.0, value=float(m_rates.get("aggregate", 2200.0)), key="adm_agg")
                adm_ste = st.number_input("Steel (प्रति kg ₹):", min_value=0.0, value=float(m_rates.get("steel", 60.0)), key="adm_ste")
                
                if st.button("💾 Save Master Rates", key="save_master_rates"):
                    user_db["MASTER_MARKET_RATES"] = {
                        "cement": adm_cem, "sand": adm_snd, "bricks": adm_brk, "aggregate": adm_agg, "steel": adm_ste
                    }
                    save_db(user_db)
                    st.success("✅ मार्केट दर अपडेट झाले!")
                
                st.markdown("---")
                st.markdown("### 📋 युझर डेटाबेस MASTER LIST")
                
                for key in list(user_db.keys()):
                    if key == "MASTER_MARKET_RATES": continue
                    info = user_db[key]
                    if not isinstance(info, dict): continue
                    
                    u_name = info.get("id", key)
                    u_comm = info.get("comment", "काही नाही")
                    u_hist = info.get("history", [])
                    
                    st.markdown(f"**👤 युझर:** {u_name} | **कमेंट:** {u_comm}")
                    
                    if st.button(f"🗑️ Delete {u_name}", key=f"del_{key}"):
                        del user_db[key]
                        save_db(user_db)
                        st.error(f"❌ '{u_name}' डिलीट केला!")
                        st.rerun()
                    
                    new_msg = st.text_input(f"✍️ {u_name} साठी मेसेज:", key=f"msg_{key}")
                    if st.button(f"✉️ मेसेज पाठवा", key=f"btn_msg_{key}"):
                        if new_msg.strip():
                            user_db[key]["admin_message"] = new_msg.strip()
                            save_db(user_db)
                            st.success("✅ मेसेज पाठवला!")
                            st.rerun()
                    st.markdown("---")
            else:
                st.error("❌ चुकीचा Admin ID किंवा Password!")
    st.stop()

# ॲक्टिव्ह युझर
current_user_name = st.session_state.app_user_name
user_db = load_db()

col_u, col_lo = st.columns([3.5, 1.5])
col_u.success(f"👤 युझर: **{current_user_name}**")
if col_lo.button("🔄 नाव बदला"):
    st.session_state.app_user_name = None
    st.session_state.current_comment = "काही नाही"
    st.session_state.selected_module = None
    st.rerun()

current_user_data = user_db.get(current_user_name, {})
admin_msg = current_user_data.get("admin_message", None)
if admin_msg:
    st.info(f"📢 **kanha (Admin):** {admin_msg}")

# ==========================================
# 🎛️ DASHBOARD SELECTION SCREEN
# ==========================================
if st.session_state.selected_module is None:
    st.markdown("### 🚀 तुम्हाला काय करायचे आहे ते निवडा:")
    col_icon1, col_icon2 = st.columns(2)
    
    with col_icon1:
        st.markdown("""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 18px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 45px; margin:0;">📊</h1>
                <h3 style="margin: 8px 0 4px 0; color: #f3f4f6; font-size: 18px;">Rate Analysis</h3>
                <p style="font-size: 12px; color: #9ca3af; margin:0;">दर विश्लेषण (काँक्रीट व वीटकाम)</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Open Rate Analysis", key="btn_open_ra", use_container_width=True):
            st.session_state.selected_module = "Rate Analysis"
            st.rerun()

    with col_icon2:
        st.markdown("""
            <div style="text-align: center; background: rgba(31, 41, 55, 0.8); padding: 18px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h1 style="font-size: 45px; margin:0;">🏗️</h1>
                <h3 style="margin: 8px 0 4px 0; color: #f3f4f6; font-size: 18px;">BBS</h3>
                <p style="font-size: 12px; color: #9ca3af; margin:0;">Bar Bending Schedule</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏗️ Open BBS", key="btn_open_bbs", use_container_width=True):
            st.session_state.selected_module = "BBS"
            st.rerun()

# ==========================================
# 🛑 MODULE 1: RATE ANALYSIS MODULE
# ==========================================
elif st.session_state.selected_module == "Rate Analysis":
    if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_main"):
        st.session_state.selected_module = None
        st.rerun()
        
    master_rates = user_db.get("MASTER_MARKET_RATES", {"cement": 400.0, "sand": 2500.0, "bricks": 8.0, "aggregate": 2200.0, "steel": 60.0})
    st.caption(f"📢 **आजचे मार्केट दर:** Cement: ₹{master_rates['cement']}/bag | Sand: ₹{master_rates['sand']}/m³ | Agg: ₹{master_rates['aggregate']}/m³ | Steel: ₹{master_rates['steel']}/kg")

    main_choice = st.radio("**काम निवडा:**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)"], horizontal=True)

    if "Concrete Work" in main_choice:
        st.subheader("🧱 Concrete Work Estimation")
        c1, c2 = st.columns(2)
        with c1: grade = st.selectbox("काँक्रीट ग्रेड:", ["M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"])
        with c2: component = st.selectbox("घटक (Component):", ["Footing (0.8% Steel)", "Slab (1.0% Steel)", "Beam (2.0% Steel)", "Column (2.5% Steel)", "Plain Concrete (0% Steel)"])

        c_ratio, s_ratio, a_ratio = (1, 3, 6) if "M10" in grade else (1, 2, 4) if "M15" in grade else (1, 1.5, 3) if "M20" in grade else (1, 1, 2)
        steel_pct = 0.8 if "Footing" in component else 1.0 if "Slab" in component else 2.0 if "Beam" in component else 2.5 if "Column" in component else 0.0

        v1, v2 = st.columns(2)
        with v1:
            volume = st.number_input("घनफळ (Volume in m³):", min_value=0.1, value=1.0, key="cc_vol")
            cement_rate = st.number_input("सिमेंट दर/बॅग (₹):", min_value=0.0, value=float(master_rates['cement']), key="cc_cem_r")
            sand_rate = st.number_input("वाळू दर/m³ (₹):", min_value=0.0, value=float(master_rates['sand']), key="cc_snd_r")
        with v2:
            aggregate_rate = st.number_input("खडी दर/m³ (₹):", min_value=0.0, value=float(master_rates['aggregate']), key="cc_agg_r")
            steel_rate = st.number_input("स्टील दर/kg (₹):", min_value=0.0, value=float(master_rates['steel']), key="cc_stl_r") if steel_pct > 0 else 0.0

        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="cc_rep_btn"):
            dry_vol = volume * 1.54
            tot_parts = c_ratio + s_ratio + a_ratio
            c_bags = math.ceil(((c_ratio / tot_parts) * dry_vol) * 28.8)
            s_m3 = (s_ratio / tot_parts) * dry_vol
            a_m3 = (a_ratio / tot_parts) * dry_vol
            steel_qty = volume * (steel_pct / 100.0) * 7850

            tot_c = c_bags * cement_rate
            tot_s = s_m3 * sand_rate
            tot_a = a_m3 * aggregate_rate
            tot_st = steel_qty * steel_rate
            mat_cost = tot_c + tot_s + tot_a + tot_st

            st.success("🎉 रिपोर्ट तयार झाला आहे!")
            report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **Cement** | {c_bags} | Bags | {cement_rate:.2f} | {tot_c:.2f} |
| **Sand** | {s_m3:.2f} | m³ | {sand_rate:.2f} | {tot_s:.2f} |
| **Aggregate** | {a_m3:.2f} | m³ | {aggregate_rate:.2f} | {tot_a:.2f} |
| **Steel** | {steel_qty:.2f} | Kg | {steel_rate:.2f} | {tot_st:.2f} |
| **TOTAL MATERIAL COST** | - | - | - | **₹ {mat_cost:.2f}/-** |
"""
            st.markdown(report_table)

    else:
        st.subheader("🧱 Brickwork Estimation")
        mortar_choice = st.selectbox("मॉर्टर मिक्स गुणोत्तर:", ["1:3", "1:4", "1:5", "1:6"])
        c_p, s_p = map(int, mortar_choice.split(":"))

        bm1, bm2 = st.columns(2)
        with bm1:
            volume = st.number_input("वीटकामाचे घनफळ (m³):", min_value=0.1, value=1.0, key="bw_vol")
            brick_rate = st.number_input("विटांचा दर प्रति १००० नग (₹):", min_value=0.0, value=8000.0, key="bw_br")
        with bm2:
            cement_rate = st.number_input("सिमेंट दर/बॅग (₹):", min_value=0.0, value=float(master_rates['cement']), key="bw_cr")
            sand_rate = st.number_input("वाळू दर/m³ (₹):", min_value=0.0, value=float(master_rates['sand']), key="bw_sr")

        if st.button("📊 GENERATE BRICKWORK REPORT", type="primary", key="bw_rep_btn"):
            tot_bricks = math.ceil(volume * 500)
            dry_m_vol = volume * 0.30
            tot_m_parts = c_p + s_p
            c_bags = math.ceil(((c_p / tot_m_parts) * dry_m_vol) * 28.8)
            s_m3 = (s_p / tot_m_parts) * dry_m_vol

            tot_b_cost = (tot_bricks / 1000.0) * brick_rate
            tot_c_cost = c_bags * cement_rate
            tot_s_cost = s_m3 * sand_rate
            tot_cost = tot_b_cost + tot_c_cost + tot_s_cost

            st.success("🎉 वीटकाम रिपोर्ट तयार झाला आहे!")
            report_table = f"""
| Description | Quantity | Unit | Rate (₹) | Amount (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **Bricks** | {tot_bricks} | Nos | {(brick_rate/1000):.2f}/नग | {tot_b_cost:.2f} |
| **Cement** | {c_bags} | Bags | {cement_rate:.2f} | {tot_c_cost:.2f} |
| **Sand** | {s_m3:.2f} | m³ | {sand_rate:.2f} | {tot_s_cost:.2f} |
| **TOTAL ESTIMATE** | - | - | - | **₹ {tot_cost:.2f}/-** |
"""
            st.markdown(report_table)

# ==========================================
# 🛑 MODULE 2: BBS MODULE
# ==========================================
elif st.session_state.selected_module == "BBS":
    if st.button("⬅️ मुख्य मेनूवर जा", key="btn_back_bbs"):
        st.session_state.selected_module = None
        st.rerun()

    st.subheader("🏗️ Bar Bending Schedule (BBS Calculator)")
    rcc_component = st.selectbox("🧱 RCC घटक निवडा:", ["Footing (फुटिंग)", "Column (खांब/कॉलम)", "Beam (बीम)", "Slab (छत/स्लॅब)"])

    c_l, c_w, c_d = st.columns(3)
    val_L = c_l.number_input("लांबी L:", min_value=0.0, value=3.0, key="bbs_L")
    val_W = c_w.number_input("रुंदी B:", min_value=0.0, value=0.3, key="bbs_W")
    val_D = c_d.number_input("उंची/खोली H:", min_value=0.0, value=0.45, key="bbs_D")

    unit_type = st.radio("❓ **परिमाणे (Unit):**", ["Meters (m)", "Feet (ft)", "Inches (in)"], horizontal=True)
    
    # Internal Unit Conversion
    mult = 0.3048 if "Feet" in unit_type else 0.0254 if "Inches" in unit_type else 1.0
    L, W, D = val_L * mult, val_W * mult, val_D * mult

    hook_angle = "135° (Standard Seismic)"
    if "Column" in rcc_component or "Beam" in rcc_component:
        hook_angle = st.radio("🔗 **Hook Angle:**", ["135° (Seismic Hook - 10d)", "90° (Standard L - 9d)"], horizontal=True)

    def_cover = 50 if "Footing" in rcc_component else 40 if "Column" in rcc_component else 25 if "Beam" in rcc_component else 15
    cover_mm = st.number_input("क्लियर कव्हर (mm):", min_value=10, value=def_cover, step=5)
    cov_m = cover_mm / 1000.0

    if st.button("📊 GENERATE BBS REPORT", type="primary", key="gen_bbs_btn"):
        bbs_rows = []
        
        if "Footing" in rcc_component:
            dia = 12
            nos = math.ceil((W - 2*cov_m) / 0.15) + 1
            cut_len = (L - 2*cov_m) + 2*(D - 2*cov_m) - (4 * (dia/1000.0))
            tot_len = cut_len * nos
            wt = tot_len * ((dia**2) / 162.0)
            bbs_rows.append({"desc": f"Footing Main Mesh ({dia}mm)", "nos": nos, "dia": dia, "cut_len": cut_len, "tot_len": tot_len, "wt": wt})

        elif "Column" in rcc_component or "Beam" in rcc_component:
            dia_main = 16
            nos_main = 4
            cut_len_m = L + (2 * 50 * (dia_main/1000.0))
            tot_len_m = cut_len_m * nos_main
            wt_m = tot_len_m * ((dia_main**2) / 162.0)
            
            dia_st = 8
            h_len = (2 * 10 * (dia_st/1000.0)) if "135°" in hook_angle else (2 * 9 * (dia_st/1000.0))
            cut_len_st = (2 * ((W - 2*cov_m) + (D - 2*cov_m))) + h_len
            nos_st = math.ceil(L / 0.15) + 1
            tot_len_st = cut_len_st * nos_st
            wt_st = tot_len_st * ((dia_st**2) / 162.0)
            
            bbs_rows.append({"desc": f"Main Steel ({dia_main}mm)", "nos": nos_main, "dia": dia_main, "cut_len": cut_len_m, "tot_len": tot_len_m, "wt": wt_m})
            bbs_rows.append({"desc": f"Stirrup/Tie ({dia_st}mm)", "nos": nos_st, "dia": dia_st, "cut_len": cut_len_st, "tot_len": tot_len_st, "wt": wt_st})

        st.success("🎉 BBS रिपोर्ट तयार झाला आहे!")
        tot_wt = sum(r['wt'] for r in bbs_rows)
        
        table_md = "| Description | Nos | Dia (mm) | Cut Length (m) | Total Length (m) | Weight (kg) |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for r in bbs_rows:
            table_md += f"| **{r['desc']}** | {r['nos']} | {r['dia']} | {r['cut_len']:.2f} m | {r['tot_len']:.2f} m | **{r['wt']:.2f}** |\n"
        table_md += f"| **TOTAL WEIGHT** | - | - | - | - | **{tot_wt:.2f} Kg** |\n"
        
        st.markdown(table_md)
