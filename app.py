# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT - PRO MAX VERSION
# Made By Vilvarasan Jathusvarman
# =========================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF
from openai import OpenAI

# =========================================================
# OPENAI SETUP (USE ENV VARIABLE IN REAL DEPLOYMENT)
# =========================================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================================================
# LOGIN SYSTEM
# =========================================================
USERS = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.session_state.user = u
        else:
            st.error("Invalid login")

if not st.session_state.logged_in:
    login()
    st.stop()

# =========================================================
# LANGUAGE SYSTEM
# =========================================================
LANGUAGES = {
    "English": "English",
    "Tamil": "Tamil",
    "Sinhala": "Sinhala",
    "Hindi": "Hindi"
}

lang = st.selectbox("🌐 Select Language", list(LANGUAGES.keys()))

OWNER = "Made By Vilvarasan Jathusvarman"

# =========================================================
# FORM SECTION
# =========================================================
st.title("🇱🇰 Government Form Assistant")

name = st.text_input("Full Name")
dob = st.text_input("Date of Birth")
address = st.text_area("Address")
phone = st.text_input("Phone Number")
email = st.text_input("Email")
nic = st.text_input("NIC Number")
occupation = st.text_input("Occupation")

data = {
    "Name": name,
    "DOB": dob,
    "Address": address,
    "Phone": phone,
    "Email": email,
    "NIC": nic,
    "Occupation": occupation,
    "User": st.session_state.user,
    "Time": str(datetime.now())
}

# =========================================================
# SAVE TO EXCEL DATABASE
# =========================================================
def save_to_db(d):
    file = "database.xlsx"
    df = pd.DataFrame([d])

    if os.path.exists(file):
        old = pd.read_excel(file)
        df = pd.concat([old, df], ignore_index=True)

    df.to_excel(file, index=False)

if st.button("💾 Save Data"):
    save_to_db(data)
    st.success("Saved successfully!")

# =========================================================
# PDF GENERATION
# =========================================================
def generate_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Government Form", ln=True)

    for k, v in d.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)

    pdf.cell(200, 10, txt=OWNER, ln=True)

    pdf.output("form.pdf")
    return "form.pdf"

if st.button("📄 Download PDF"):
    path = generate_pdf(data)
    st.download_button("Download PDF", open(path, "rb"), file_name="form.pdf")

# =========================================================
# AI CHATBOT (MULTILINGUAL OUTPUT)
# =========================================================
def ask_ai(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a Sri Lankan Government Form Assistant.

RULES:
- User input is English
- Output MUST be in {lang}
- Be simple, clear, helpful
- Never change meaning
"""
            },
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

st.write("## 🤖 AI Chatbot")

question = st.text_input("Ask your question (English input only)")

if question:
    answer = ask_ai(question)

    st.success(answer)
    st.info(OWNER)

# =========================================================
# FOOTER
# =========================================================
st.write("---")
st.markdown(f"🇱🇰 {OWNER}")
