# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math

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

# 🔐 युझर डेटाबेस इनिशियलाइज करणे (ॲप चालू असेपर्यंत डेटा साठवण्यासाठी)
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "9999999999": {"name": "कन्हाई पाटील", "password": "patiladmin123"}
    }

if "app_user" not in st.session_state:
    st.session_state.app_user = None  # सुरवातीला कोणीही लॉग इन नाही

# मुख्य टायटल आणि ब्रँडिंग
st.title("🏗️ PATIL INFRATECH")
st.subheader("📐 Quantity Surveyor & Cost Estimator")
st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech - kanha_1p)")
st.write("---")

# ==========================================
# 🔑 ऑप्शनल लॉगिन आणि साइन-अप सिस्टीम
# ==========================================
if st.session_state.app_user is None:
    st.markdown("### 🔐 लॉगिन करा किंवा नवीन खाते बनवा (पर्यायी)")
    tab1, tab2, tab3 = st.tabs(["🔑 लॉगिन (Login)", "📝 नवीन खाते (Sign Up)", "👤 Guest म्हणून पुढे जा"])
    
    with tab1:
        l_mobile = st.text_input("१० अंकी मोबाईल नंबर:", key="l_mob").strip()
        l_pass = st.text_input("पासवर्ड प्रविष्ट करा:", type="password", key="l_pwd")
        if st.button("लॉगिन करा", type="primary"):
            if l_mobile in st.session_state.user_db and st.session_state.user_db[l_mobile]["password"] == l_pass:
                st.session_state.app_user = st.session_state.user_db[l_mobile]["name"]
                st.success(f"🔓 लॉगिन यशस्वी! स्वागत आहे {st.session_state.app_user}")
                st.rerun()
            else:
                st.error("❌ चुकीचा मोबाईल नंबर किंवा पासवर्ड!")
                
    with tab2:
        r_name = st.text_input("तुमचे पूर्ण नाव (Full Name):", key="r_nm").strip()
        r_mobile = st.text_input("१० अंकी मोबाईल नंबर (Mobile No):", key="r_mob").strip()
        r_pass = st.text_input("नवीन पासवर्ड तयार करा:", type="password", key="r_pwd")
        if st.button("खाते तयार करा"):
            if not r_name or not r_mobile or not r_pass:
                st.warning("⚠️ कृपया सर्व रकाने भरा!")
            elif len(r_mobile) != 10 or not r_mobile.isdigit():
                st.error("❌ कृपया वैध १० अंकी मोबाईल नंबर टाका!")
            elif r_mobile in st.session_state.user_db:
                st.error("❌ हा मोबाईल नंबर आधीपासूनच रजिस्टर आहे!")
            else:
                st.session_state.user_db[r_mobile] = {"name": r_name, "password": r_pass}
                st.success("🎉 खाते यशस्वीरित्या तयार झाले! आता लॉगिन टॅबमध्ये जाऊन लॉगिन करा.")
                
    with tab3:
        st.info("💡 जर तुम्हाला खाते बनवायचे नसेल, तर तुम्ही थेट नाव टाकून ॲप वापरू शकता.")
        guest_name = st.text_input("**तुमचे नाव प्रविष्ट करा (Enter Name):**", placeholder="नाव टाईप करा...", key="gst_nm")
        if st.button("Guest म्हणून पुढे जा 👉", type="secondary"):
            if guest_name.strip():
                st.session_state.app_user = guest_name.strip()
                st.rerun()
            else:
                st.warning("⚠️ कृपया पुढे जाण्यासाठी नाव प्रविष्ट करा!")
                
    st.stop()  # लॉगिन किंवा नाव निश्चित होईपर्यंत खालील कोड रन होणार नाही

# सध्याचा ॲक्टिव्ह युझर
current_user = st.session_state.app_user

# लॉगआउट पर्याय (वरच्या बाजूला छोटा)
col_u, col_lo = st.columns([5, 1])
col_u.success(f"🔓 चालू युझर: **{current_user}**")
if col_lo.button("🚪 Logout"):
    st.session_state.app_user = None
    st.rerun()

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

    st.markdown("#### [A] साहित्याची माहिती आणि दर (थेट टाईप करा)")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        volume = st.number_input("एकूण काँक्रीट घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=1.0)
        cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=400.0)
        sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=2500.0)
    with v_col2:
        aggregate_rate = st.number_input("खडीचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=2200.0)
        steel_rate = st.number_input("स्टीलचा दर प्रति किलो (₹/Kg):", min_value=0.0, step=None, value=65.0) if steel_percentage > 0 else 0.0

    st.markdown("#### [B] लेबर खर्च (नसल्यास ० ठेवा)")
    l_col1, l_col2, l_col3 = st.columns(3)
    with l_col1:
        mason_qty = st.number_input("मेसन संख्या (Days):", min_value=0.0, step=None, value=0.0)
        mason_rate = st.number_input("मेसन दर (₹/Day):", min_value=0.0, value=600.0)
    with l_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Days):", min_value=0.0, step=None, value=0.0)
        mazdoor_rate = st.number_input("मजदूर दर (₹/Day):", min_value=0.0, value=400.0)
    with l_col3:
        bb_qty = st.number_input("बार बेंडर संख्या:", min_value=0.0, step=None, value=0.0)
        bb_rate = st.number_input("बार बेंडर दर (₹/Day):", min_value=0.0, value=550.0)

    st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
    o_col1, o_col2 = st.columns(2)
    with o_col1:
        scaffolding_cost = st.number_input("स्कॅफोल्डिंग/सेंटरिंग खर्च (₹):", min_value=0.0, value=0.0)
        contingency_cost = st.number_input("आकस्मिक खर्च (Contingencies) (₹):", min_value=0.0, value=0.0)
    with o_col2:
        water_pct = st.number_input("वॉटर चार्ज टक्केवारी (%):", min_value=0.0, value=1.0)
        profit_pct = st.number_input("कंत्राटदार नफा टक्केवारी (%):", min_value=0.0, value=10.0)

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary"):
        dry_volume = volume * 1.54
        total_parts = cement_ratio + sand_ratio + aggregate_ratio
        c_bags = math.ceil(((cement_ratio / total_parts) * dry_volume) * 28.8)
        s_m3 = (sand_ratio / total_parts) * dry_volume
        a_m3 = (aggregate_ratio / total_parts) * dry_volume
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
        st.info(f"👤 **Prepared For:** {current_user} | **घटक:** {component.split(' ')[0]} | **ग्रेड:** {grade.split(' ')[0]} | **एकूण घनफळ:** {volume} m³")
        
        st.markdown(f"""
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
        """)

# ==========================================
# 🛑 वीटकाम (BRICKWORK MODULE)
# ==========================================
else:
    st.subheader("🧱 Brickwork Estimation")
    
    b_col1 = st.columns(1)[0]
    mortar_choice = b_col1.selectbox("मॉर्टर मिक्स गुणोत्तर (Mortar Mix Ratio) निवडा:", 
                                     ["1:3 (सिमेंट : वाळू)", "1:4 (सिमेंट : वाळू)", "1:5 (सिमेंट : वाळू)", "1:6 (सिमेंट : वाळू)"])
    
    if "1:3" in mortar_choice: c_part, s_part = 1, 3
    elif "1:4" in mortar_choice: c_part, s_part = 1, 4
    elif "1:5" in mortar_choice: c_part, s_part = 1, 5
    else: c_part, s_part = 1, 6

    st.markdown("#### [A] साहित्याची माहिती आणि दर (थेट टाईप करा)")
    bm_col1, bm_col2 = st.columns(2)
    with bm_col1:
        volume = st.number_input("वीटकामाचे एकूण घनफळ भरा (Volume in m³):", min_value=0.0, step=None, value=1.0)
        brick_rate = st.number_input("विटांचा दर प्रति हजार नग (₹ per 1000 Bricks):", min_value=0.0, step=None, value=8000.0)
    with bm_col2:
        cement_rate = st.number_input("सिमेंट दर प्रति बॅग (₹):", min_value=0.0, step=None, value=400.0)
        sand_rate = st.number_input("वाळूचा दर प्रति m³ (₹):", min_value=0.0, step=None, value=2500.0)

    st.markdown("#### [B] लेबर खर्च (नसल्यास ० ठेवा)")
    bl_col1, bl_col2 = st.columns(2)
    with bl_col1:
        mason_qty = st.number_input("मेसन संख्या (Brickwork Days):", min_value=0.0, step=None, value=0.0)
        mason_rate = st.number_input("मेसन प्रतिदिन दर (₹/Day):", min_value=0.0, value=650.0)
    with bl_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Brickwork Days):", min_value=0.0, step=None, value=0.0)
        mazdoor_rate = st.number_input("मजदूर प्रतिदिन दर (₹/Day):", min_value=0.0, value=400.0)

    st.markdown("#### [C] अवांतर खर्च व टक्केवारी")
    bo_col1, bo_col2 = st.columns(2)
    with bo_col1:
        scaffolding_cost = st.number_input("पाळत/स्कॅफोल्डिंग खर्च (₹):", min_value=0.0, value=0.0)
        contingency_cost = st.number_input("आकस्मिक खर्च (₹):", min_value=0.0, value=0.0)
    with bo_col2:
        water_pct = st.number_input("वॉटर充電 charge (%):", min_value=0.0, value=1.0)
        profit_pct = st.number_input("कंत्राटदार नफा (%):", min_value=0.0, value=10.0)

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary"):
        total_bricks = math.ceil(volume * 500)
        dry_mortar_vol = volume * 0.30
        total_mortar_parts = c_part + s_part
        
        cement_vol = (c_part / total_mortar_parts) * dry_mortar_vol
        sand_m3 = (s_part / total_mortar_parts) * dry_mortar_vol
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

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - BRICKWORK")
        st.info(f"👤 **Prepared For:** {current_user} | **गुणोत्तर:** {mortar_choice.split(' ')[0]} | **एकूण घनफळ:** {volume} m³")
        
        st.markdown(f"""
        | Description | Quantity | Unit | Rate (₹) | Amount (₹) |
        | :--- | :--- | :--- | :--- | :--- |
        | **[A] MATERIAL** | | | | |
        | Bricks | {total_bricks} | Nos | {(brick_rate/1000):.2f} | {total_brick_cost:.2f} |
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
        """)
