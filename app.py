# KANHA_1p - पाटील इन्फ्राटेक (Streamlit Web Application)
import streamlit as st
import math
import os
import json

# पेजची रचना
st.set_page_config(page_title="PATIL INFRATECH", page_icon="📐", layout="centered")

# CSS जुगाड: अनावश्यक गोष्टी लपवण्यासाठी
st.markdown("""
    <style>
    button[title="Increment"], button[title="Decrement"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# 💾 फाईल डेटाबेस मॅनेजमेंट
LOG_FILE = "user_database.txt"
AUTH_FILE = "user_auth.json"
INBOX_FILE = "admin_inbox.json"

# अकाऊंट्स लोड आणि सेव्ह करणे
def load_accounts():
    if not os.path.exists(AUTH_FILE): return {}
    with open(AUTH_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_account(email, password):
    accounts = load_accounts()
    accounts[email] = password
    with open(AUTH_FILE, "w", encoding="utf-8") as f: json.dump(accounts, f, ensure_ascii=False, indent=4)

def load_inbox():
    if not os.path.exists(INBOX_FILE): return {}
    with open(INBOX_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_inbox_message(email, message):
    inbox = load_inbox()
    if email not in inbox: inbox[email] = []
    inbox[email].append(message)
    with open(INBOX_FILE, "w", encoding="utf-8") as f: json.dump(inbox, f, ensure_ascii=False, indent=4)

def save_to_database(name, work_type, comment, email="नॉन-लॉगिन युझर"):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"नाव: {name} | ईमेल: {email} | काम: {work_type} | कमेंट: {comment}\n")

def read_database():
    if not os.path.exists(LOG_FILE): return []
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

# मुख्य टायटल
st.title("🏗️ PATIL INFRATECH")
st.caption("Concept & Logic by: Kanhaiya (Founder of Patil Infratech - kanha_1p)")

# session_state ट्रॅकिंग
if 'name_saved' not in st.session_state: st.session_state.name_saved = ""
if 'logged_in_email' not in st.session_state: st.session_state.logged_in_email = ""

# लॉगिन किंवा नाव टाकणे (Optional)
st.subheader("Login / Guest Access")
has_account = st.checkbox("🔐 लॉगिन करायचे आहे का?")
if has_account:
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        accounts = load_accounts()
        if email in accounts and accounts[email] == password:
            st.session_state.logged_in_email = email
            st.session_state.name_saved = email.split("@")[0]
            st.rerun()
        else:
            st.error("चुकीचे डिटेल्स!")
    if st.button("Register"):
        save_account(email, password)
        st.success("अकाउंट तयार झाले!")
else:
    name = st.text_input("नाव प्रविष्ट करा:")
    if st.button("Submit Name"):
        st.session_state.name_saved = name
        st.rerun()

# जर युझर लॉगिन असेल तर इनबॉक्स दाखवा
if st.session_state.logged_in_email:
    inbox = load_inbox()
    msgs = inbox.get(st.session_state.logged_in_email, [])
    if msgs:
        st.info(f"📥 तुमच्यासाठी मेसेज: {msgs[-1]}")

# ॲप लॉजिक (जोपर्यंत नाव किंवा लॉगिन नाही, तोपर्यंत ॲप दाखवू नका)
if st.session_state.name_saved or st.session_state.logged_in_email:
    st.write("---")
    # [येथे तुझे आधीचे Concrete आणि Brickwork कोड येतील, तो तसाच ठेवला आहे]
    st.info("ॲपचे मुख्य फीचर्स इथे येतील...") 

# ==========================================
# 🛡️ ॲडमीन लॉगिन एरिया (नेहमी शेवटी दिसणार)
# ==========================================
st.write("---")
with st.expander("🛡️ Admin Login Area (फक्त कन्हाईसाठी)"):
    admin_id = st.text_input("Admin ID:")
    admin_pass = st.text_input("Password:", type="password")
    
    if admin_id == "kanha_1p" and admin_pass == "@Dellg15":
        st.success("🔓 लॉगिन यशस्वी!")
        
        # १. सर्व युझर डेटा (ईमेल, पासवर्ड)
        st.markdown("### 🔑 सर्व युझर्सचे डिटेल्स")
        st.json(load_accounts())
        
        # २. मेसेज पाठवणे
        st.markdown("### ✉️ विशिष्ट युझरला मेसेज पाठवा")
        user_list = list(load_accounts().keys())
        target_user = st.selectbox("युझर निवडा:", user_list)
        msg_text = st.text_area("मेसेज:")
        if st.button("पाठवा"):
            save_inbox_message(target_user, msg_text)
            st.success("मेसेज पाठवला!")
            
        # ३. जुना लॉग डेटा
        st.markdown("### 📊 सर्व कॅल्क्युलेशन डेटा")
        logs = read_database()
        if st.button("🗑️ सर्व डेटा डिलीट करा"):
            if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
            st.rerun()
        st.table(logs)
    elif admin_id or admin_pass:
        st.error("❌ चुकीचा ID किंवा पासवर्ड!")
