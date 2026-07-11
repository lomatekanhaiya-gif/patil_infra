# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# पेजची रचना
st.set_page_config(page_title="PATIL INFRATECH", page_icon="📐", layout="centered")

# CSS जुगाड: number input मधील + आणि - बटणे लपवण्यासाठी
st.markdown("""
    <style>
    button[title="Increment"], button[title="Decrement"] {
        display: none !important;
    }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 गुगल शीट कनेक्शन (तुझ्या शीटची लिंक इथे जोडली आहे)
sheet_url = "https://docs.google.com/spreadsheets/d/1USfhxvfNqbOP92GxUHvnAokV3mPXDY7AawnFveSOkao/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# मुख्य टायटल आणि ब्रँडिंग
st.title("🏗️ PATIL INFRATECH")
st.subheader("📐 Quantity Surveyor & Cost Estimator")
st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech - kanha_1p)")
st.write("---")

# session_state ट्रॅकिंग
if 'name_saved' not in st.session_state:
    st.session_state.name_saved = ""
if 'current_comment' not in st.session_state:
    st.session_state.current_comment = "काही नाही"

# 🔐 १. नाव टाकणे सक्तीचे
if not st.session_state.name_saved:
    user_name = st.text_input("**ॲप्लिकेशन सुरू करण्यासाठी आपले नाव प्रविष्ट करा (Enter Your Name):**", placeholder="तुमचे नाव इथे टाईप करा...")
    
    # मोबाईल युझर्ससाठी खास सबमिट बटण
    if st.button("👉 नाव सबमिट करा (Submit Name)", type="primary"):
        if user_name.strip():
            st.session_state.name_saved = user_name.strip()
            st.rerun()
        else:
            st.warning("⚠️ कृपया पुढे जाण्यासाठी तुमचे नाव टाईप करा!")
    st.stop()

user_name = st.session_state.name_saved
st.success(f"🔓 स्वागत आहे, **{user_name}**! पाटील इन्फ्राटेक एस्टिमेटर अनलॉक झाला आहे.")
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

    st.markdown("#### [A] साहित्याची माहिती आणि दर (बॉक्स रिकामे आहेत)")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=None, placeholder="0.0")
        cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
        sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
    with v_col2:
        aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
        steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, step=None, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0

    st.markdown("#### [B] लेबर खर्च (बॉक्स रिकामे आहेत)")
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
    with l_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
    with l_col3:
        bb_qty = st.number_input("बार बेंडर संख्या (Days):", min_value=0.0, step=None, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0
        bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0") if steel_percentage > 0 else 0.0

    st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
    o_col1, o_col2 = st.columns(2)
    with o_col1:
        scaffolding_cost = st.number_input("स्कॅफोल्डिंग/सेंटरिंग खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
        contingency_cost = st.number_input("आकस्मिक खर्च (Contingencies) (₹):", min_value=0.0, value=None, placeholder="0.0")
    with o_col2:
        water_pct = st.number_input("वॉटर टक्केवारी (%):", min_value=0.0, value=None, placeholder="0.0")
        profit_pct = st.number_input("कंत्राटदार नफा टक्केवारी (%):", min_value=0.0, value=None, placeholder="0.0")

    st.write("---")
    # 💬 स्वतंत्र कमेंट बॉक्स आणि मोबाईल सबमिट बटण
    user_comment = st.text_area("💬 **काही विशेष नोंद किंवा कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
    if st.button("💬 कमेंट सबमिट करा (Submit Comment)"):
        if user_comment.strip():
            st.session_state.current_comment = user_comment.strip()
            st.toast("✅ कमेंट सेव्ह झाली!")

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary"):
        # डेटा गुगल शीटमध्ये कायमचा सेव्ह करणे
        try:
            df = conn.read(spreadsheet=sheet_url, ttl="0d")
            new_row = pd.DataFrame([{"नाव": user_name, "काम": "Concrete Work", "कमेंट": st.session_state.current_comment}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=sheet_url, data=updated_df)
        except:
            pass # बॅकएंड कनेक्टिव्हिटी एरर सेफ्टी

        # कॅल्क्युलेशन लॉजिक (सेफ्टी झिरो व्हॅल्यूजसह)
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
        base_total = mat_cost + lab_cost + sc_cost + ct_cost
        w_amt = base_total * (w_pct / 100)
        p_amt = base_total * (p_pct / 100)
        grand_total = base_total + w_amt + p_amt

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - CONCRETE WORK")
        st.markdown(f"""
        | Description | Quantity | Unit | Rate (₹) | Amount (₹) |
        | :--- | :--- | :--- | :--- | :--- |
        | Cement | {c_bags} | Bags | {c_rate:.2f} | {total_cement_cost:.2f} |
        | Sand | {s_m3:.2f} | m³ | {s_rate:.2f} | {total_sand_cost:.2f} |
        | Aggregate | {a_m3:.2f} | m³ | {a_rate:.2f} | {total_aggregate_cost:.2f} |
        | Steel | {steel_qty:.2f} | Kg | {st_rate:.2f} | {total_steel_cost:.2f} |
        | Mason | {m_qty} | Nos | {m_rate:.2f} | {m_qty*m_rate:.2f} |
        | Mazdoor | {mz_qty} | Nos | {mz_rate:.2f} | {mz_qty*mz_rate:.2f} |
        | **GRAND TOTAL** | | | | **₹ {grand_total:.2f}/-** |
        """)

# ==========================================
# 🛑 वीटकाम (BRICKWORK MODULE)
# ==========================================
else:
    st.subheader("🧱 Brickwork Estimation")
    b_col1 = st.columns(1)[0]
    mortar_choice = b_col1.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio) निवडा:", ["1:4 (सिमेंट : वाळू)", "1:3 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])
    
    if "1:3" in mortar_choice: c_part, s_part = 1, 3
    elif "1:4" in mortar_choice: c_part, s_part = 1, 4
    elif "1:5" in mortar_choice: c_part, s_part = 1, 5
    else: c_part, s_part = 1, 6

    st.markdown("#### [A] साहित्याची माहिती आणि दर (बॉक्स रिकामे आहेत)")
    bm_col1, bm_col2 = st.columns(2)
    with bm_col1:
        volume = st.number_input("वीटकामाचे एकूण घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=None, placeholder="0.0")
        brick_rate = st.number_input("विटांचा दर प्रति नग (Rate per 1 Brick in ₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
    with bm_col2:
        cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")
        sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=None, placeholder="0.0")

    st.markdown("#### [B] लेबर खर्च (बॉक्स रिकामे आहेत)")
    bl_col1, bl_col2 = st.columns(2)
    with bl_col1:
        mason_qty = st.number_input("मेसन संख्या (Brickwork Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mason_rate = st.number_input("मेसन प्रतिदिन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
    with bl_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Brickwork Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mazdoor_rate = st.number_input("मजदूर प्रतिदिन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")

    st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
    bo_col1, bo_col2 = st.columns(2)
    with bo_col1:
        scaffolding_cost = st.number_input("पाळत/स्कॅफोल्डिंग खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
        contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=None, placeholder="0.0")
    with bo_col2:
        water_pct = st.number_input("वॉटर चार्ज (%):", min_value=0.0, value=None, placeholder="0.0")
        profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=None, placeholder="0.0")

    st.write("---")
    # 💬 कमेंट बॉक्स
    user_comment = st.text_area("💬 **काही विशेष नोंद किंवा कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
    if st.button("💬 कमेंट सबमिट करा (Submit Comment)"):
        if user_comment.strip():
            st.session_state.current_comment = user_comment.strip()
            st.toast("✅ कमेंट सेव्ह झाली!")

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary"):
        # डेटा गुगल शीटमध्ये सेव्ह करणे
        try:
            df = conn.read(spreadsheet=sheet_url, ttl="0d")
            new_row = pd.DataFrame([{"नाव": user_name, "काम": "Brickwork", "कमेंट": st.session_state.current_comment}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=sheet_url, data=updated_df)
        except:
            pass

        vol_val = volume if volume else 0.0
        b_rate = brick_rate if brick_rate else 0.0
        c_rate = cement_rate if cement_rate else 0.0
        s_rate = sand_rate if sand_rate else 0.0
        m_qty = mason_qty if mason_qty else 0.0
        m_rate = mason_rate if mason_rate else 0.0
        mz_qty = mazdoor_qty if mazdoor_qty else 0.0
        mz_rate = mazdoor_rate if mazdoor_rate else 0.0
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
        lab_cost = (m_qty * m_rate) + (mz_qty * mz_rate)
        base_total = mat_cost + lab_cost + sc_cost + ct_cost
        w_amt = base_total * (w_pct / 100)
        p_amt = base_total * (p_pct / 100)
        grand_total = base_total + w_amt + p_amt

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - BRICKWORK")
        st.markdown(f"""
        | Description | Quantity | Unit | Rate (₹) | Amount (₹) |
        | :--- | :--- | :--- | :--- | :--- |
        | Bricks | {total_bricks} | Nos | {b_rate:.2f} | {total_brick_cost:.2f} |
        | Cement | {cement_bags} | Bags | {c_rate:.2f} | {total_cement_cost:.2f} |
        | Sand | {sand_m3:.2f} | m³ | {s_rate:.2f} | {total_sand_cost:.2f} |
        | Mason | {m_qty} | Nos | {m_rate:.2f} | {m_qty*m_rate:.2f} |
        | Mazdoor | {mz_qty} | Nos | {mz_rate:.2f} | {mz_qty*mz_rate:.2f} |
        | **GRAND TOTAL** | | | | **₹ {grand_total:.2f}/-** |
        """)

# ==========================================
# 🔐 ॲडमीन लॉगिन एरिया (थेट गुगल शीटमधून डेटा आणणार)
# ==========================================
st.write("---")
with st.expander("🛡️ Admin Login Area (फक्त कन्हाईसाठी)"):
    admin_id = st.text_input("Admin ID:", key="admin_id")
    admin_pass = st.text_input("Password:", type="password", key="admin_pass")
    
    if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
        st.success("🔓 लॉगिन यशस्वी! हा डेटा थेट तुझ्या ऑनलाईन गुगल शीटमधून येत आहे (रिफ्रेश केल्यावरही उडणार नाही):")
        try:
            admin_df = conn.read(spreadsheet=sheet_url, ttl="0d")
            st.dataframe(admin_df, use_container_width=True)
        except Exception as e:
            st.error("गुगल शीटमधून डेटा लोड करताना एरर आला. कृपया शेअर सेटिंग तपासा.")
    elif admin_id or admin_pass:
        st.error("❌ चुकीचा ID किंवा पासवर्ड!")
