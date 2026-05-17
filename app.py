# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT (FINAL PRO VERSION)
# Made By Vilvarasan Jathusvarman
# =========================================================

import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import os
from dotenv import load_dotenv
from openai import OpenAI

# =========================================================
# API KEY
# =========================================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# =========================================================
# UI LANGUAGE SYSTEM
# =========================================================

UI_TEXT = {
    "English": {
        "title": "AI Government Form Assistant",
        "upload": "Upload Form",
        "voice": "Voice Input",
        "ask": "Ask Your Question",
        "form": "Government Form Data",
        "summary": "Show Form Summary",
        "sidebar": "AI Assistant"
    },
    "Tamil": {
        "title": "AI அரசு படிவ உதவியாளர்",
        "upload": "படிவத்தை பதிவேற்றவும்",
        "voice": "குரல் உள்ளீடு",
        "ask": "உங்கள் கேள்வி",
        "form": "அரசு படிவ தரவு",
        "summary": "படிவ சுருக்கம்",
        "sidebar": "AI உதவியாளர்"
    },
    "Sinhala": {
        "title": "AI රජයේ පෝරම සහායක",
        "upload": "පෝරමය උඩුගත කරන්න",
        "voice": "හඬ ආදානය",
        "ask": "ඔබේ ප්‍රශ්නය",
        "form": "රජයේ පෝරම දත්ත",
        "summary": "පෝරම සාරාංශය",
        "sidebar": "AI සහායක"
    },
    "Hindi": {
        "title": "AI सरकारी फॉर्म सहायक",
        "upload": "फॉर्म अपलोड करें",
        "voice": "आवाज़ इनपुट",
        "ask": "अपना प्रश्न",
        "form": "सरकारी फॉर्म डेटा",
        "summary": "फॉर्म सारांश",
        "sidebar": "AI सहायक"
    }
}

OWNER_NAME = "👤 Made By Vilvarasan Jathusvarman"

# =========================================================
# OFFLINE BOT
# =========================================================

def offline_bot(q):
    q = q.lower()

    if "name" in q:
        return "Full Name means your complete legal name."
    elif "dob" in q:
        return "Date of Birth is DD/MM/YYYY format."
    elif "nic" in q:
        return "NIC is National Identity Card number in Sri Lanka."
    elif "address" in q:
        return "Address is your home location."
    elif "phone" in q:
        return "Phone number is your contact number."
    elif "email" in q:
        return "Email is used for communication."
    else:
        return "Ask about Name, NIC, Address, DOB, Phone, Email."

# =========================================================
# AI ENGINE
# =========================================================

def get_ai_response(question, selected_language, form_data):

    if client:
        try:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a Government Form Assistant.

Rules:
- Respond in {selected_language}
- Use user form data if needed
- Be simple and clear
"""
                    },
                    {
                        "role": "user",
                        "content": f"Form Data: {form_data}\n\nQuestion: {question}"
                    }
                ]
            )
            return res.choices[0].message.content

        except:
            return offline_bot(question)

    return offline_bot(question)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Government Form Assistant",
    page_icon="🇱🇰",
    layout="wide"
)

# =========================================================
# LANGUAGE SELECT
# =========================================================

selected_language = st.selectbox("🌐 Language", list(UI_TEXT.keys()))
ui = UI_TEXT[selected_language]

# =========================================================
# UI STYLE
# =========================================================

st.markdown("""
<style>
.stApp{
    background: linear-gradient(to right,#0f172a,#1e293b);
    color:white;
}
h1,h2,h3,p,label{
    color:white;
}
.box{
    background:#1e293b;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR (OWNER ALWAYS SHOWN)
# =========================================================

with st.sidebar:
    st.title(ui["sidebar"])
    st.success(OWNER_NAME)

# =========================================================
# TITLE
# =========================================================

st.title(ui["title"])

# =========================================================
# 🧾 FORM DATA SYSTEM
# =========================================================

st.write("## 🧾 " + ui["form"])

full_name = st.text_input("Full Name")
dob = st.text_input("Date of Birth")
address = st.text_area("Address")
phone = st.text_input("Phone")
email = st.text_input("Email")
nic = st.text_input("NIC")
occupation = st.text_input("Occupation")

form_data = {
    "Full Name": full_name,
    "DOB": dob,
    "Address": address,
    "Phone": phone,
    "Email": email,
    "NIC": nic,
    "Occupation": occupation
}

if st.button(ui["summary"]):
    st.write("## 📄 Form Summary")
    for k, v in form_data.items():
        st.write(f"**{k}:** {v}")

# =========================================================
# OCR
# =========================================================

st.write("## 📄 " + ui["upload"])

uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

image = None
if uploaded_file:
    image = Image.open(uploaded_file)

if image:
    st.image(image, use_container_width=True)
    text = pytesseract.image_to_string(image)
    st.text(text)

# =========================================================
# VOICE INPUT
# =========================================================

st.write("## 🎤 " + ui["voice"])

audio_bytes = audio_recorder()
voice_question = ""

if audio_bytes:
    st.audio(audio_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        path = f.name

    r = sr.Recognizer()

    try:
        with sr.AudioFile(path) as source:
            audio = r.record(source)

        voice_question = r.recognize_google(audio)
        st.success(voice_question)

    except:
        st.error("Voice Error")

# =========================================================
# CHAT INPUT
# =========================================================

text_question = st.text_input(ui["ask"])
user_question = text_question or voice_question

# =========================================================
# AI RESPONSE
# =========================================================

if user_question:

    with st.spinner("Thinking..."):
        answer = get_ai_response(user_question, selected_language, form_data)

        st.markdown(f"""
        <div class="box">
        🤖 {answer}
        <br><br>
        {OWNER_NAME}
        </div>
        """, unsafe_allow_html=True)

        try:
            tts = gTTS(text=answer, lang="en")
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp.name)
            st.audio(temp.name)
        except:
            pass

# =========================================================
# FOOTER
# =========================================================

st.write("---")
st.markdown(f"🇱🇰 {OWNER_NAME}")
