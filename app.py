# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import os

# पेजची रचना
st.set_page_config(page_title="PATIL INFRATECH", page_icon="📐", layout="centered")

# CSS जुगाड: + आणि - बटणे, तसेच उजव्या बाजूचा GitHub आयकॉन आणि मेनू पूर्णपणे लपवण्यासाठी
st.markdown("""
    <style>
    /* + आणि - बटणे लपवणे */
    button[title="Increment"], button[title="Decrement"] {
        display: none !important;
    }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    /* मुख्य स्ट्रीमलिट मेनू आणि गिटहब आयकॉन पूर्णपणे लपवणे */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .viewerBadge_link__1S12K {display: none !important;}
    button[title="View source code"] {display: none !important;}
    /* स्पिन बटणे घालवणे */
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 💾 डेटा कायमचा साठवण्यासाठी फाईलचा जुगाड
LOG_FILE = "user_database.txt"

def save_to_database(name, work_type, comment):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"नाव: {name} | काम: {work_type} | कमेंट: {comment}\n")

def read_database():
    if not os.path.exists(LOG_FILE):
        return []
    logs = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split(" | ")
                log_dict = {}
                for p in parts:
                    k, v = p.split(": ")
                    log_dict[k] = v
                logs.append(log_dict)
    return logs

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
    user_comment = st.text_area("💬 **काही विशेष नोंद किंवा कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
    if st.button("💬 कमेंट सबमिट करा (Submit Comment)", key="btn_concrete_comment"):
        if user_comment.strip():
            st.session_state.current_comment = user_comment.strip()
            st.success("✅ कमेंट सेव्ह झाली!")

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="btn_concrete_report"):
        save_to_database(user_name, "Concrete Work", st.session_state.current_comment)

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
        
        # Total (Material + Labour + Scaffolding + Contingency)
        total_base = mat_cost + lab_cost + sc_cost + ct_cost
        w_amt = total_base * (w_pct / 100)
        p_amt = total_base * (p_pct / 100)
        grand_total = total_base + w_amt + p_amt
        per_m3_rate = grand_total / vol_val if vol_val > 0 else 0.0

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - CONCRETE WORK")
        
        # फोटोमध्ये दिलेल्या फॉरमॅटनुसार टेबल
        st.markdown(f"""
        | Sr. No. | Description | Rate (₹) | Quantity | Unit | Amount (₹) |
        | :---: | :--- | :---: | :---: | :---: | :---: |
        | | **[A] Material** | | | | |
        | 1 | Cement | {c_rate:.2f} | {c_bags} | bag | {total_cement_cost:.2f} |
        | 2 | Sand | {s_rate:.2f} | {s_m3:.2f} | m³ | {total_sand_cost:.2f} |
        | 3 | Aggregate | {a_rate:.2f} | {a_m3:.2f} | m³ | {total_aggregate_cost:.2f} |
        | 4 | Steel | {st_rate:.2f} | {steel_qty:.2f} | Kg | {total_steel_cost:.2f} |
        | | **[B] Labour** | | | | |
        | 5 | Mason | {m_rate:.2f} | {m_qty} | day | {m_qty*m_rate:.2f} |
        | 6 | Mazdoor | {mz_rate:.2f} | {mz_qty} | day | {mz_qty*mz_rate:.2f} |
        | 7 | Bar Bender | {b_rate:.2f} | {b_qty} | day | {b_qty*b_rate:.2f} |
        | | **[C] Other Expenses** | | | | |
        | 8 | Scaffolding / Centering | - | - | L.S. | {sc_cost:.2f} |
        | 9 | Contingency | - | - | L.S. | {ct_cost:.2f} |
        | | **Total** | | | | **{total_base:.2f}** |
        | 10 | Water Charge ({w_pct}%) | | | @Total | {w_amt:.2f} |
        | 11 | Contractor Profit ({p_pct}%) | | | @Total | {p_amt:.2f} |
        | | **Grand Total** | | | | **₹ {grand_total:.2f}** |
        """)
        st.info(f"👉 **प्रति घनफळ दर (Rate per m³):** {grand_total:.2f} / {vol_val} = **₹ {per_m3_rate:.2f} Rs/m³**")

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
    bl_col1, bl_col2, bl_col3 = st.columns(3)
    with bl_col1:
        mason_qty = st.number_input("मेसन संख्या (Brickwork Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mason_rate = st.number_input("मेसन प्रतिदिन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
    with bl_col2:
        mazdoor_qty = st.number_input("मजदूर संख्या (Brickwork Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
        mazdoor_rate = st.number_input("मजदूर प्रतिदिन दर (₹/Day):", min_value=0.0, value=None, placeholder="0.0")
    with bl_col3:
        bhisti_qty = st.number_input("भिस्ती संख्या (Watering Days):", min_value=0.0, step=None, value=None, placeholder="0.0")
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
    user_comment = st.text_area("💬 **काही विशेष नोंद किंवा कमेंट लिहायची असल्यास इथे लिहा:**", placeholder="तुमची कमेंट लिहा...")
    if st.button("💬 कमेंट सबमिट करा (Submit Comment)", key="btn_brick_comment"):
        if user_comment.strip():
            st.session_state.current_comment = user_comment.strip()
            st.success("✅ कमेंट सेव्ह झाली!")

    if st.button("📊 GENERATE RATE ANALYSIS REPORT", type="primary", key="btn_brick_report"):
        save_to_database(user_name, "Brickwork", st.session_state.current_comment)

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
        
        # फोटोतल्या कॅल्क्युलेशनप्रमाणे Total काढणे
        total_base = mat_cost + lab_cost + sc_cost + ct_cost
        w_amt = total_base * (w_pct / 100)
        p_amt = total_base * (p_pct / 100)
        grand_total = total_base + w_amt + p_amt
        per_m3_rate = grand_total / vol_val if vol_val > 0 else 0.0

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - BRICKWORK")
        
        # फोटोमध्ये दिलेल्या रचनेनुसार नवीन टेबल फॉरमॅट
        st.markdown(f"""
        | Sr. No. | Description | Rate (₹) | Quantity | Unit | Amount (₹) |
        | :---: | :--- | :---: | :---: | :---: | :---: |
        | | **[A] Material** | | | | |
        | 1 | Bricks | {b_rate:.2f} | {total_bricks} | Nos | {total_brick_cost:.2f} |
        | 2 | Cement | {c_rate:.2f} | {cement_bags} | bag | {total_cement_cost:.2f} |
        | 3 | Sand | {s_rate:.2f} | {sand_m3:.2f} | m³ | {total_sand_cost:.2f} |
        | | **[B] Labour** | | | | |
        | 4 | Mason | {m_rate:.2f} | {m_qty} | day | {m_qty*m_rate:.2f} |
        | 5 | Mazdoor | {mz_rate:.2f} | {mz_qty} | day | {mz_qty*mz_rate:.2f} |
        | 6 | Bhisti | {bh_rate:.2f} | {bh_qty} | day | {bh_qty*bh_rate:.2f} |
        | | **[C] Other Expenses** | | | | |
        | 7 | Scaffolding | - | - | L.S. | {sc_cost:.2f} |
        | 8 | Contingency | - | - | L.S. | {ct_cost:.2f} |
        | | **Total** | | | | **{total_base:.2f}** |
        | 9 | Water Charge ({w_pct}%) | | | @Total | {w_amt:.2f} |
        | 10 | Contractor Profit ({p_pct}%) | | | @Total | {p_amt:.2f} |
        | | **Grand Total** | | | | **₹ {grand_total:.2f}** |
        """)
        st.markdown(f"**{grand_total:.2f} / {vol_val} = {per_m3_rate:.2f} Rs/m³**")

# ==========================================
# 🔐 ॲडमीन लॉगिन एरिया
# ==========================================
st.write("---")
with st.expander("🛡️ Admin Login Area (फक्त कन्हाईसाठी)"):
    admin_id = st.text_input("Admin ID:", key="admin_id")
    admin_pass = st.text_input("Password:", type="password", key="admin_pass")
    
    if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
        st.success("🔓 लॉगिन यशस्वी!")
        
        if st.button("🗑️ सर्व डेटा डिलीट करा (Clear All Logs)"):
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
            st.success("डेटा यशस्वीरित्या डिलीट केला!")
            st.rerun()
            
        logs = read_database()
        if logs:
            st.table(logs)
        else:
            st.info("अजूनपर्यंत कोणी रिपोर्ट जनरेट केलेला नाही किंवा डेटा रिकामी आहे.")
    elif admin_id or admin_pass:
        st.error("❌ चुकीचा ID किंवा पासवर्ड!")
