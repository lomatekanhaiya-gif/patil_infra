# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import os
import json
import re
import pandas as pd
import io

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

# 💾 फाईल डेटाबेस मॅनेजमेंट (टेक्स्ट आणि जेसॉन फाईल्स)
LOG_FILE = "user_database.txt"
AUTH_FILE = "user_auth.json"
INBOX_FILE = "admin_inbox.json"

# ईमेल वैध आहे की नाही हे तपासण्याचे फंक्शन
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# अकाऊंट्स लोड आणि सेव्ह करणे
def load_accounts():
    if not os.path.exists(AUTH_FILE):
        return {}
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_account(email, password):
    accounts = load_accounts()
    accounts[email] = password
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

# इनबॉक्स मेसेजेस लोड आणि सेव्ह करणे
def load_inbox():
    if not os.path.exists(INBOX_FILE):
        return {}
    with open(INBOX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_inbox_message(email, message):
    inbox = load_inbox()
    if email not in inbox:
        inbox[email] = []
    inbox[email].append(message)
    with open(INBOX_FILE, "w", encoding="utf-8") as f:
        json.dump(inbox, f, ensure_ascii=False, indent=4)

# रिपोर्ट डेटा सेव्ह आणि रीड करणे
def save_to_database(name, work_type, comment, email="नॉन-लॉगिन युझर"):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"नाव: {name} | ईमेल: {email} | काम: {work_type} | कमेंट: {comment}\n")

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

# 📄 एक्सेल डेटा जनरेट करण्याचे फंक्शन (वॉटरमार्कसह)
def generate_excel(df_data, title):
    output = io.BytesIO()
    # डेटाफ्रेम तयार करू
    df = pd.DataFrame(df_data)
    
    # वॉटरमार्क आणि ब्रँडिंग रोज ॲड करू
    watermark_rows = [
        {"Sr. No.": "---", "Description": "🔒 WATERMARK: PATIL INFRATECH (kanha_1p) 🔒", "Rate (₹)": "---", "Quantity": "---", "Unit": "---", "Amount (₹)": "---"},
        {"Sr. No.": "---", "Description": f"📑 REPORT: {title}", "Rate (₹)": "---", "Quantity": "---", "Unit": "---", "Amount (₹)": "---"}
    ]
    df_watermarked = pd.concat([pd.DataFrame(watermark_rows), df], ignore_index=True)
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_watermarked.to_excel(writer, index=False, sheet_name="Rate Analysis")
    return output.getvalue()

# 📄 पीडीएफ (HTML आधारित डाउनलोड) जनरेट करण्याचे फंक्शन (वॉटरमार्कसह)
def generate_pdf_html(df_data, title):
    html = f"""
    <div style='border: 3px solid #333; padding: 20px; font-family: Arial; position: relative;'>
        <!-- अंधुक आणि मोठा वॉटरमार्क बॅकग्राउंडला -->
        <div style='position: absolute; top: 40%; left: 5%; font-size: 55px; color: rgba(200, 200, 200, 0.2); transform: rotate(-30deg); font-weight: bold; pointer-events: none; user-select: none;'>
            PATIL INFRATECH (kanha_1p)
        </div>
        <h2 style='text-align: center;'>🏗️ PATIL INFRATECH</h2>
        <h4 style='text-align: center;'>📐 Quantity Surveyor & Cost Estimator</h4>
        <hr>
        <h3>📊 REPORT: {title}</h3>
        <table border='1' style='width:100%; border-collapse: collapse; text-align: left;'>
            <tr style='background-color: #f2f2f2;'>
                <th>Sr. No.</th><th>Description</th><th>Rate (₹)</th><th>Quantity</th><th>Unit</th><th>Amount (₹)</th>
            </tr>
    """
    for row in df_data:
        html += f"""
        <tr>
            <td>{row['Sr. No.']}</td><td>{row['Description']}</td><td>{row['Rate (₹)']}</td><td>{row['Quantity']}</td><td>{row['Unit']}</td><td>{row['Amount (₹)']}</td>
        </tr>
        """
    html += """
        </table>
        <br>
        <p style='text-align: center; font-size: 12px; color: gray;'>🔒 Generated via Patil Infratech App - Malicious removal of watermark is strictly prohibited.</p>
    </div>
    """
    return html

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
if 'logged_in_email' not in st.session_state:
    st.session_state.logged_in_email = ""

# 🔐 १. नाव किंवा लॉगिन विचारणे (Compulsory Section)
if not st.session_state.name_saved and not st.session_state.logged_in_email:
    
    has_account = st.checkbox("🔐 **मला स्वतःचे खाते (Account) वापरायचे आहे / नवीन बनवायचे आहे**")
    
    if has_account:
        auth_mode = st.radio("निवडा:", ["लॉगिन करा (Login)", "नवीन खाते बनवा (Register)"])
        user_email = st.text_input("तुमचा ईमेल आयडी (Email as Username):", placeholder="example@gmail.com")
        user_pass = st.text_input("पासवर्ड (Password):", type="password", placeholder="तुमचा पासवर्ड टाका...")
        
        if auth_mode == "नवीन खाते बनवा (Register)":
            if st.button("🆕 खाते तयार करा", type="primary"):
                if is_valid_email(user_email.strip()):
                    if len(user_pass) >= 4:
                        save_account(user_email.strip(), user_pass)
                        st.success("🎉 खाते यशस्वीरित्या तयार झाले! आता 'लॉगिन करा' निवडून ॲप सुरू करा.")
                    else:
                        st.error("❌ पासवर्ड किमान ४ अंकी असावा!")
                else:
                    st.error("❌ Email is not valid! (कृपया वैध ईमेल आयडी प्रविष्ट करा)")
        
        else:
            if st.button("🔓 लॉगिन करा", type="primary"):
                user_email_clean = user_email.strip()
                if is_valid_email(user_email_clean):
                    accounts = load_accounts()
                    if user_email_clean in accounts and accounts[user_email_clean] == user_pass:
                        st.session_state.logged_in_email = user_email_clean
                        st.session_state.name_saved = user_email_clean.split("@")[0].upper()
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा ईमेल किंवा पासवर्ड!")
                else:
                    st.error("❌ Email is not valid! (कृपया वैध ईमेल आयडी टाका)")
                    
    else:
        user_name = st.text_input("**ॲप्लिकेशन सुरू करण्यासाठी आपले नाव प्रविष्ट करा (Enter Your Name):**", placeholder="तुमचे नाव इथे टाईप करा...")
        if st.button("👉 नाव सबमिट करा (Submit Name)", type="primary"):
            if user_name.strip():
                st.session_state.name_saved = user_name.strip()
                st.rerun()
            else:
                st.warning("⚠️ कृपया पुढे जाण्यासाठी तुमचे नाव टाईप करा!")
                
    st.stop()

# स्वागत मेसेज आणि वैयक्तिक ॲडमीन इनबॉक्स
if st.session_state.logged_in_email:
    st.success(f"🔓 स्वागत आहे, **{st.session_state.name_saved}** ({st.session_state.logged_in_email})! प्रीमियम फीचर्स अनलॉक झाले आहेत.")
    
    # 📥 युझरचा स्वतःचा इनबॉक्स (फक्त कन्हाईने पाठवलेले मेसेज दिसणार)
    inbox_data = load_inbox()
    user_messages = inbox_data.get(st.session_state.logged_in_email, [])
    
    with st.expander("📥 Admin Notice Box (कन्हाईकडून आलेले मेसेजेस / सबस्क्रिप्शन कोड)"):
        if user_messages:
            for msg in reversed(user_messages):
                st.info(f"💬 **Admin Message:** {msg}")
        else:
            st.write("🔔 अजून कोणताही मेसेज किंवा सबस्क्रिप्शन कोड आलेला नाही. (वार्षिक सबस्क्रिप्शन ₹५० साठी ॲडमीनशी संपर्क करा)")

    with st.expander("⏳ माझी पूर्व हिस्टरी (My Calculation History)"):
        all_logs = read_database()
        user_logs = [log for log in all_logs if log.get("ईमेल") == st.session_state.logged_in_email]
        if user_logs:
            st.table(user_logs)
        else:
            st.info("तुमची कोणतीही जुनी हिस्टरी सापडली नाही.")
else:
    st.success(f"🔓 स्वागत आहे, **{st.session_state.name_saved}**! पाटील इन्फ्राटेक एस्टिमेटर अनलॉक झाला आहे.")

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
        email_tag = st.session_state.logged_in_email if st.session_state.logged_in_email else "नॉन-लॉगिन युझर"
        save_to_database(st.session_state.name_saved, "Concrete Work", st.session_state.current_comment, email_tag)

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

        st.success("🎉 रिपोर्ट यशस्वीरित्या तयार झाला आहे!")
        st.markdown(f"### 📊 RATE ANALYSIS SHEET - CONCRETE WORK")
        
        table_markdown = f"""
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
        | | **Total** | | | | **{total_base:.2f}** |
        | 10 | Water Charge ({w_pct}%) | | | @Total | {w_amt:.2f} |
        | 11 | Contractor Profit ({p_pct}%) | | | @Total | {p_amt:.2f} |
        | | **Grand Total** | | | | **₹ {grand_total:.2f}** |
        """
        st.markdown(table_markdown)
        st.info(f"👉 **Rate per m³:** {grand_total:.2f} / {vol_val} = **₹ {per_m3_rate:.2f} Rs/m³**")

        # 📥 डाउनलोड सेक्शन (अट: युझर लॉगिन असणे बंधनकारक आहे)
        st.write("---")
        st.markdown("### 📥 Download Options (प्रीमियम फीचर्स)")
        if st.session_state.logged_in_email:
            # एक्सेल आणि पीडीएफ साठी डेटा स्ट्रक्चर तयार करू
            report_data = [
                {"Sr. No.": "1", "Description": "Cement", "Rate (₹)": c_rate, "Quantity": c_bags, "Unit": "bag", "Amount (₹)": total_cement_cost},
                {"Sr. No.": "2", "Description": "Sand", "Rate (₹)": s_rate, "Quantity": s_m3, "Unit": "m³", "Amount (₹)": total_sand_cost},
                {"Sr. No.": "3", "Description": "Aggregate", "Rate (₹)": a_rate, "Quantity": a_m3, "Unit": "m³", "Amount (₹)": total_aggregate_cost},
                {"Sr. No.": "4", "Description": "Steel", "Rate (₹)": st_rate, "Quantity": steel_qty, "Unit": "Kg", "Amount (₹)": total_steel_cost},
                {"Sr. No.": "5", "Description": "Mason", "Rate (₹)": m_rate, "Quantity": m_qty, "Unit": "day", "Amount (₹)": m_qty*m_rate},
                {"Sr. No.": "6", "Description": "Mazdoor", "Rate (₹)": mz_rate, "Quantity": mz_qty, "Unit": "day", "Amount (₹)": mz_qty*mz_rate},
                {"Sr. No.": "7", "Description": "Bar Bender", "Rate (₹)": b_rate, "Quantity": b_qty, "Unit": "day", "Amount (₹)": b_qty*b_rate},
                {"Sr. No.": "8", "Description": "Scaffolding", "Rate (₹)": "-", "Quantity": "-", "Unit": "L.S.", "Amount (₹)": sc_cost},
                {"Sr. No.": "9", "Description": "Contingency", "Rate (₹)": "-", "Quantity": "-", "Unit": "L.S.", "Amount (₹)": ct_cost},
                {"Sr. No.": "10", "Description": f"Water Charge ({w_pct}%)", "Rate (₹)": "-", "Quantity": "-", "Unit": "@Total", "Amount (₹)": w_amt},
                {"Sr. No.": "11", "Description": f"Contractor Profit ({p_pct}%)", "Rate (₹)": "-", "Quantity": "-", "Unit": "@Total", "Amount (₹)": p_amt},
                {"Sr. No.": "---", "Description": "GRAND TOTAL", "Rate (₹)": "-", "Quantity": "-", "Unit": "-", "Amount (₹)": grand_total}
            ]
            
            # १. एक्सेल डाउनलोड बटण
            excel_bytes = generate_excel(report_data, "Concrete Work Analysis")
            st.download_button(label="📥 Download Excel Sheet (With Watermark)", data=excel_bytes, file_name="Concrete_Rate_Analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            # २. पीडीएफ डाउनलोड बटण
            pdf_html = generate_pdf_html(report_data, "Concrete Work Analysis")
            st.download_button(label="📄 Download PDF Report (With Watermark)", data=pdf_html, file_name="Concrete_Rate_Analysis.html", mime="text/html")
        else:
            st.warning("🔒 डाउनलोड पर्याय फक्त लॉगिन असलेल्या युझर्ससाठीच उपलब्ध आहेत! कृपया डाउनलोड करण्यासाठी डाऊनलोड करण्यापूर्वी साईन-इन/खाते तयार करा.")

# ==========================================
# 🛑 वीटका
