# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import os
import json

# पेजची रचना
st.set_page_config(page_title="PATIL INFRATECH", page_icon="📐", layout="centered")

# CSS जुगाड: + आणि - बटणे, तसेच उजव्या बाजूचा GitHub आयकॉन आणि मेनू पूर्णपणे लपवण्यासाठी
st.markdown("""
    <style>
    button[title="Increment"], button[title="Decrement"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .viewerBadge_link__1S12K {display: none !important;}
    button[title="View source code"] {display: none !important;}
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# 💾 डेटाबेस फाईलचा जुगाड (सर्व युझर, इनबॉक्स आणि हिस्टरी एकाच फाईलमध्ये)
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        # सुरुवातीला रिकामी रचना तयार करणे
        default_db = {"users": {}, "global_logs": []}
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_db, f, indent=4)
        return default_db
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"users": {}, "global_logs": []}

def save_db(db_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=4)

# मुख्य टायटल
st.title("🏗️ PATIL INFRATECH")
st.subheader("📐 Quantity Surveyor & Cost Estimator")
st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech - kanha_1p)")
st.write("---")

# Session State ट्रॅकिंग
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'current_comment' not in st.session_state:
    st.session_state.current_comment = "काही नाही"

db = load_db()

# ==========================================
# 🔐 लॉगिन आणि साइन-अप सिस्टीम (LOGIN SYSTEM)
# ==========================================
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 लॉगिन (Login)", "📝 नवीन खाते बनवा (Sign Up)"])
    
    with tab1:
        st.markdown("### आपले खाते लॉगिन करा")
        login_email = st.text_input("इमेल आयडी (Email):", key="login_email_input").strip().lower()
        login_pass = st.text_input("पासवर्ड (Password):", type="password", key="login_pass_input")
        
        if st.button("लॉगिन करा", type="primary", key="login_btn"):
            if login_email in db["users"] and db["users"][login_email]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.current_user = login_email
                st.success("🔓 लॉगिन यशस्वी!")
                st.rerun()
            else:
                st.error("❌ चुकीचा इमेल किंवा पासवर्ड! कृपया पुन्हा तपासा.")
                
    with tab2:
        st.markdown("### नवीन रजिस्ट्रेशन")
        reg_name = st.text_input("तुमचे पूर्ण नाव (Full Name):").strip()
        reg_email = st.text_input("इमेल आयडी (Email ID):").strip().lower()
        reg_pass = st.text_input("नवीन पासवर्ड तयार करा:", type="password")
        
        if st.button("खाते तयार करा", key="signup_btn"):
            if not reg_name or not reg_email or not reg_pass:
                st.warning("⚠️ कृपया सर्व रकाने भरा!")
            elif reg_email in db["users"]:
                st.error("❌ हा इमेल आधीपासूनच रजिस्टर आहे!")
            else:
                # नवीन युझरची रचना तयार करणे
                db["users"][reg_email] = {
                    "name": reg_name,
                    "password": reg_pass,
                    "messages": ["पाटील इन्फ्राटेक ॲपमध्ये आपले स्वागत आहे!"],
                    "history": []
                }
                save_db(db)
                st.success("🎉 खाते यशस्वीरित्या तयार झाले! आता लॉगिन टॅबमध्ये जाऊन लॉगिन करा.")
    st.stop()

# युझर लॉगिन झाल्यानंतरचा डेटा
user_email = st.session_state.current_user
user_name = db["users"][user_email]["name"]

# लॉगआउट बटण टॉपला
col_user, col_logout = st.columns([4, 1])
col_user.success(f"🔓 स्वागत आहे, **{user_name}** ({user_email})")
if col_logout.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.rerun()

# मुख्य मेनू ऑप्शन्स (Estimation, Inbox, History)
menu_choice = st.sidebar.radio("📋 मुख्य मेनू", ["📐 Estimation Work", "✉️ माझी इनबॉक्स (Inbox)", "📜 माझी हिस्टरी (History)"])

# ==========================================
# ✉️ इनबॉक्स विभाग (PERSONAL INBOX)
# ==========================================
if menu_choice == "✉️ माझी इनबॉक्स (Inbox)":
    st.header("✉️ तुमचा वैयक्तिक इनबॉक्स")
    user_msgs = db["users"][user_email].get("messages", [])
    if user_msgs:
        for i, msg in enumerate(reversed(user_msgs), 1):
            st.info(f"📩 **मेसेज {i}:** {msg}")
    else:
        st.info("अजून कोणताही मेसेज आलेला नाही.")

# ==========================================
# 📜 हिस्टरी विभाग (PERSONAL HISTORY)
# ==========================================
elif menu_choice == "📜 माझी हिस्टरी (History)":
    st.header("📜 तुमची मागील कामे (History)")
    user_history = db["users"][user_email].get("history", [])
    if user_history:
        for idx, item in enumerate(reversed(user_history), 1):
            with st.expander(f"📋 काम {idx}: {item['काम']} ({item['तारीख']})"):
                st.write(f"**कमेंट:** {item['कमेंट']}")
                st.markdown(item["टेबल_डेटा"])
    else:
        st.info("तुम्ही अजून कोणतेही एस्टिमेशन केलेले नाही.")

# ==========================================
# 📐 मुख्य एस्टिमेशन काम (ESTIMATION WORK)
# ==========================================
elif menu_choice == "📐 Estimation Work":
    main_choice = st.radio("**काय काम करायचे आहे ते निवडा :**", ["Concrete Work (काँक्रीट काम)", "Brickwork (वीटकाम)"])

    # --- Concrete Work ---
    if "Concrete Work" in main_choice:
        st.subheader("🧱 Concrete Work Estimation")
        col1, col2 = st.columns(2)
        with col1:
            grade = st.selectbox("काँक्रीट ग्रेड निवडा:", ["M10 (1:3:6)", "M15 (1:2:4)", "M20 (1:1.5:3)", "M25 (1:1:2)"])
        with col2:
            component = st.selectbox("आरसीसी घटक निवडा:", ["Footing (0.8% Steel)", "Slab (1.0% Steel)", "Beam (2.0% Steel)", "Column (2.5% Steel)", "Plain Concrete (0% Steel)"])

        if "M10" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 3, 6
        elif "M15" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 2, 4
        elif "M20" in grade: cement_ratio, sand_ratio, aggregate_ratio = 1, 1.5, 3
        else: cement_ratio, sand_ratio, aggregate_ratio = 1, 1, 2

        steel_percentage = 0.8 if "Footing" in component else 1.0 if "Slab" in component else 2.0 if "Beam" in component else 2.5 if "Column" in component else 0.0

        st.markdown("#### [A] साहित्याची माहिती आणि दर")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=None, placeholder="0.0")
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
        with v_col2:
            aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
            steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, step=None, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0

        st.markdown("#### [B] लेबर खर्च")
        l_col1, l_col2, l_col3 = st.columns(3)
        with l_col1:
            mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, value=None, placeholder="0.0")
            mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
        with l_col2:
            mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, value=None, placeholder="0.0")
            mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
        with l_col3:
            bb_qty = st.number_input("बार बेंडर संख्या (Days):", min_value=0.0, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0
            bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0

        st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
        o_col1, o_col2 = st.columns(2)
        with o_col1:
            scaffolding_cost = st.number_input("स्कॅफोल्डिंग/सेंटरिंग खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
            contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
        with o_col2:
            water_pct = st.number_input("वॉटर टक्केवारी (%):", min_value=0.0, value=None, placeholder="0.0")
            profit_pct = st.number_input("कंत्राटदार नफा टक्केवारी (%):", min_value=0.0, value=None, placeholder="0.0")

        st.write("---")
        user_comment = st.text_area("💬 **कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
        if st.button("💬 कमेंट सबमिट करा (Submit Comment)", key="btn_concrete_comment"):
            if user_comment.strip():
                st.session_state.current_comment = user_comment.strip()
                st.success("✅ कमेंट सेव्ह झाली!")

        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="btn_concrete_report"):
            vol_val = volume if volume else 0.0
            c_rate = cement_rate if cement_rate else 0.0
            s_rate = sand_rate if sand_rate else 0.0
            a_rate = aggregate_rate if aggregate_rate else 0.0
            st_rate = steel_rate if steel_rate else 0.0
            m_qty = mason_qty if mason_qty else 0.0
            m_rate = mason_rate if mason_rate else 0.0
            mz_qty = mazdoor_qty if mazdoor_qty else 0.0
            mz_rate = mazdoor_rate if mazdoor_rate else 0.0
            b_qty = bb_qty if bb_qty else 0.0
            b_rate = bb_rate if bb_rate else 0.0
            sc_cost = scaffolding_cost if scaffolding_cost else 0.0
            ct_cost = contingency_cost if contingency_cost else 0.0
            w_pct = water_pct if water_pct else 0.0
            p_pct = profit_pct if profit_pct else 0.0

            dry_volume = vol_val * 1.54
            total_parts = cement_ratio + sand_ratio + aggregate_ratio
            c_bags = math.ceil(((cement_ratio / total_parts) * dry_volume) * 28.8) if total_parts > 0 else 0
            s_m3 = (sand_ratio / total_parts) * dry_volume if total_parts > 0 else 0.0
            a_m3 = (aggregate_ratio / total_parts) * dry_volume if total_parts > 0 else 0.0
            steel_qty = vol_val * (steel_percentage / 100) * 7850 if steel_percentage > 0 else 0.0

            total_cement_cost = c_bags * c_rate
            total_sand_cost = s_m3 * s_rate
            total_aggregate_cost = a_m3 * a_rate
            total_steel_cost = steel_qty * st_rate

            mat_cost = total_cement_cost + total_aggregate_cost + total_sand_cost + total_steel_cost
            lab_cost = (m_qty * m_rate) + (mz_qty * mz_rate) + (b_qty * b_rate)
            total_base = mat_cost + lab_cost + sc_cost + ct_cost
            w_amt = total_base * (w_pct / 100)
            p_amt = total_base * (p_pct / 100)
            grand_total = total_base + w_amt + p_amt
            per_m3_rate = grand_total / vol_val if vol_val > 0 else 0.0

            table_md = f"""
| Sr. No. | Description | Rate (₹) | Quantity | Unit | Amount (₹) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | Cement | {c_rate:.2f} | {c_bags} | bag | {total_cement_cost:.2f} |
| 2 | Sand | {s_rate:.2f} | {s_m3:.2f} | m³ | {total_sand_cost:.2f} |
| 3 | Aggregate | {a_rate:.2f} | {a_m3:.2f} | m³ | {total_aggregate_cost:.2f} |
| 4 | Steel | {st_rate:.2f} | {steel_qty:.2f} | Kg | {total_steel_cost:.2f} |
| 5 | Mason | {m_rate:.2f} | {m_qty} | day | {m_qty*m_rate:.2f} |
| 6 | Mazdoor | {mz_rate:.2f} | {mz_qty} | day | {mz_qty*mz_rate:.2f} |
| 7 | Bar Bender | {b_rate:.2f} | {b_qty} | day | {b_qty*b_rate:.2f} |
| 8 | Scaffolding / Centering | - | - | L.S. | {sc_cost:.2f} |
| 9 | Contingency | - | - | L.S. | {ct_cost:.2f} |
| | **Grand Total** | | | | **₹ {grand_total:.2f}** |
| | **Rate per m³** | | | | **₹ {per_m3_rate:.2f}** |
"""
            # वैयक्तिक हिस्टरी आणि ग्लोबल लॉगमध्ये डेटा सेव्ह करणे
            import datetime
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            history_entry = {"काम": "Concrete Work", "कमेंट": st.session_state.current_comment, "तारीख": now_str, "टेबल_डेटा": table_md}
            db["users"][user_email]["history"].append(history_entry)
            
            db["global_logs"].append({"नाव": user_name, "इमेल": user_email, "काम": "Concrete Work", "कमेंट": st.session_state.current_comment, "तारीख": now_str})
            save_db(db)

            st.success("🎉 रिपोर्ट तयार झाला आणि तुमच्या हिस्टरीमध्ये सेव्ह झाला!")
            st.markdown(table_md)

    # --- Brickwork ---
    else:
        st.subheader("🧱 Brickwork Estimation")
        mortar_choice = st.selectbox("मॉर्टर मिक्स गुणोत्तर निवडा:", ["1:4 (सिमेंट : वाळू)", "1:3 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])
        c_part, s_part = (1, 3) if "1:3" in mortar_choice else (1, 4) if "1:4" in mortar_choice else (1, 5) if "1:5" in mortar_choice else (1, 6)

        st.markdown("#### [A] साहित्याची माहिती आणि दर")
        bm_col1, bm_col2 = st.columns(2)
        with bm_col1:
            volume = st.number_input("वीटकामाचे एकूण घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=None, placeholder="0.0")
            brick_rate = st.number_input("विटांचा दर प्रति नग (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
        with bm_col2:
            cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
            sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")

        st.markdown("#### [B] लेबर खर्च")
        bl_col1, bl_col2, bl_col3 = st.columns(3)
        with bl_col1:
            mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, value=None, placeholder="0.0")
            mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
        with bl_col2:
            mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, value=None, placeholder="0.0")
            mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
        with bl_col3:
            bhisti_qty = st.number_input("भिस्ती संख्या (Days):", min_value=0.0, value=None, placeholder="0.0")
            bhisti_rate = st.number_input("भिस्ती दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")

        st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
        bo_col1, bo_col2 = st.columns(2)
        with bo_col1:
            scaffolding_cost = st.number_input("पाळत/स्कॅफोल्डिंग खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
            contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
        with bo_col2:
            water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=None, placeholder="0.0")
            profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=None, placeholder="0.0")

        st.write("---")
        user_comment = st.text_area("💬 **कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
        if st.button("💬 कमेंट सबमिट करा (Submit Comment)", key="btn_brick_comment"):
            if user_comment.strip():
                st.session_state.current_comment = user_comment.strip()
                st.success("✅ कमेंट सेव्ह झाली!")

        if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="btn_brick_report"):
            vol_val = volume if volume else 0.0
            b_rate = brick_rate if brick_rate else 0.0
            c_rate = cement_rate if cement_rate else 0.0
            s_rate = sand_rate if sand_rate else 0.0
            m_qty = mason_qty if mason_qty else 0.0
            m_rate = mason_rate if mason_rate else 0.0
            mz_qty = mazdoor_qty if mazdoor_qty else 0.0
            mz_rate = mazdoor_rate if mazdoor_rate else 0.0
            bh_qty = bhisti_qty if bhisti_qty else 0.0
            bh_rate = bhisti_rate if bhisti_rate else 0.0
            sc_cost = scaffolding_cost if scaffolding_cost else 0.0
            ct_cost = contingency_cost if contingency_cost else 0.0
            w_pct = water_pct if water_pct else 0.0
            p_pct = profit_pct if profit_pct else 0.0

            total_bricks = math.ceil(vol_val * 500)
            dry_mortar_vol = vol_val * 0.30
            total_mortar_parts = c_part + s_part
            cement_vol = (c_part / total_mortar_parts) * dry_mortar_vol if total_mortar_parts > 0 else 0.0
            sand_m3 = (s_part / total_mortar_parts) * dry_mortar_vol if total_mortar_parts > 0 else 0.0
            cement_bags = math.ceil(cement_vol * 28.8)

            total_brick_cost = total_bricks * b_rate
            total_cement_cost = cement_bags * c_rate
            total_sand_cost = sand_m3 * s_rate

            mat_cost = total_brick_cost + total_cement_cost + total_sand_cost
            lab_cost = (m_qty * m_rate) + (mz_qty * mz_rate) + (bh_qty * bh_rate)
            total_base = mat_cost + lab_cost + sc_cost + ct_cost
            w_amt = total_base * (w_pct / 100)
            p_amt = total_base * (p_pct / 100)
            grand_total = total_base + w_amt + p_amt
            per_m3_rate = grand_total / vol_val if vol_val > 0 else 0.0

            table_md = f"""
| Sr. No. | Description | Rate (₹) | Quantity | Unit | Amount (₹) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | Bricks | {b_rate:.2f} | {total_bricks} | Nos | {total_brick_cost:.2f} |
| 2 | Cement | {c_rate:.2f} | {cement_bags} | bag | {total_cement_cost:.2f} |
| 3 | Sand | {s_rate:.2f} | {sand_m3:.2f} | m³ | {total_sand_cost:.2f} |
| 4 | Mason | {m_rate:.2f} | {m_qty} | day | {m_qty*m_rate:.2f} |
| 5 | Mazdoor | {mz_rate:.2f} | {mz_qty} | day | {mz_qty*mz_rate:.2f} |
| 6 | Bhisti | {bh_rate:.2f} | {bh_qty} | day | {bh_qty*bh_rate:.2f} |
| 7 | Scaffolding | - | - | L.S. | {sc_cost:.2f} |
| 8 | Contingency | - | - | L.S. | {ct_cost:.2f} |
| | **Grand Total** | | | | **₹ {grand_total:.2f}** |
| | **Rate per m³** | | | | **₹ {per_m3_rate:.2f}** |
"""
            import datetime
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            history_entry = {"काम": "Brickwork", "कमेंट": st.session_state.current_comment, "तारीख": now_str, "टेबल_डेटा": table_md}
            db["users"][user_email]["history"].append(history_entry)
            
            db["global_logs"].append({"नाव": user_name, "इमेल": user_email, "काम": "Brickwork", "कमेंट": st.session_state.current_comment, "तारीख": now_str})
            save_db(db)

            st.success("🎉 रिपोर्ट तयार झाला आणि तुमच्या हिस्टरीमध्ये सेव्ह झाला!")
            st.markdown(table_md)

# ==========================================
# 🛡️ ॲडमीन लॉगिन एरिया (ALWAYS AT THE BOTTOM)
# ==========================================
st.write("---")
with st.expander("🛡️ Admin Login Area (फक्त कन्हाईसाठी)"):
    admin_id = st.text_input("Admin ID:", key="admin_id_field")
    admin_pass = st.text_input("Password:", type="password", key="admin_pass_field")
    
    if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
        st.success("🔓 ॲडमीन पॅनल अनलॉक झाले!")
        
        st.markdown("### 🔑 सर्व युझर खाती (User Accounts)")
        
        if db["users"]:
            for u_email, u_data in list(db["users"].items()):
                col_u_info, col_u_del = st.columns([4, 1])
                col_u_info.code(f"नाव: {u_data['name']} | Email: {u_email} | Pass: {u_data['password']}")
                
                if col_u_del.button("🗑️ डिलीट", key=f"del_user_{u_email}"):
                    del db["users"][u_email]
                    save_db(db)
                    st.success(f"युझर {u_email} डिलीट केला!")
                    st.rerun()
        else:
            st.info("अजून एकही युझर रजिस्टर नाही.")
        
        st.markdown("### ✉️ विशिष्ट युझरला मेसेज पाठवा")
        user_list = list(db["users"].keys())
        if user_list:
            target_user = st.selectbox("युझर निवडा:", user_list, key="admin_target_user")
            msg_text = st.text_area("मेसेज टाईप करा:", key="admin_msg_text")
            if st.button("मेसेज पाठवा", key="admin_send_msg_btn"):
                if msg_text.strip():
                    db["users"][target_user]["messages"].append(msg_text.strip())
                    save_db(db)
                    st.success(f"📬 {target_user} ला मेसेज पाठवला!")
                else:
                    st.warning("रिकामी मेसेज पाठवता येणार नाही.")
        else:
            st.info("मेसेज पाठवण्यासाठी युझर उपलब्ध नाहीत.")
            
        st.markdown("### 📊 सर्व युझर्सचा लॉग डेटा (Global Logs)")
        if db.get("global_logs"):
            if st.button("🗑️ सर्व लॉग हिस्टरी क्लियर करा", key="clear_all_logs"):
                db["global_logs"] = []
                save_db(db)
                st.success("सर्व लॉग डेटा डिलीट केला!")
                st.rerun()
            st.table(db["global_logs"])
        else:
            st.info("अजून कोणताही एस्टिमेशन लॉग डेटा नाही.")
            
    elif admin_id or admin_pass:
        st.error("❌ चुकीचा ID किंवा पासवर्ड!")
