# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT (PRO UPGRADED VERSION)
# Made By Jathusvarman
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
# LOAD API KEY
# =========================================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# =========================================================
# LANGUAGE SYSTEM (UI + OUTPUT)
# =========================================================

UI_TEXT = {
    "English": {
        "title": "AI Government Form Assistant",
        "upload": "Upload Form",
        "voice": "Voice Input",
        "ask": "Ask Your Question",
        "sidebar": "AI Assistant",
        "online": "ONLINE MODE",
        "offline": "OFFLINE MODE",
    },
    "Tamil": {
        "title": "AI அரசு படிவ உதவியாளர்",
        "upload": "படிவத்தை பதிவேற்றவும்",
        "voice": "குரல் உள்ளீடு",
        "ask": "உங்கள் கேள்வியை கேளுங்கள்",
        "sidebar": "AI உதவியாளர்",
        "online": "ஆன்லைன் முறை",
        "offline": "ஆஃப்லைன் முறை",
    },
    "Sinhala": {
        "title": "AI රජයේ පෝරම සහායක",
        "upload": "පෝරමය උඩුගත කරන්න",
        "voice": "හඬ ආදානය",
        "ask": "ඔබේ ප්‍රශ්නය අසන්න",
        "sidebar": "AI සහායක",
        "online": "මාර්ගගත ක්‍රමය",
        "offline": "අක්‍රිය ක්‍රමය",
    },
    "Hindi": {
        "title": "AI सरकारी फॉर्म सहायक",
        "upload": "फॉर्म अपलोड करें",
        "voice": "आवाज़ इनपुट",
        "ask": "अपना प्रश्न पूछें",
        "sidebar": "AI सहायक",
        "online": "ऑनलाइन मोड",
        "offline": "ऑफलाइन मोड",
    }
}

# =========================================================
# OFFLINE BOT
# =========================================================

def offline_bot(question):
    q = question.lower()

    knowledge = {
        "name": "Full Name means your complete legal name.",
        "dob": "Date of Birth is your birth date (DD/MM/YYYY).",
        "address": "Address means your home location details.",
        "phone": "Phone Number is your contact number.",
        "email": "Email is used for communication.",
        "nationality": "Nationality means your country.",
        "gender": "Gender can be male, female, or other.",
        "occupation": "Occupation means job or student status.",
        "nic": "In Sri Lanka, ID is NIC (National Identity Card).",
        "signature": "Signature is your official confirmation mark."
    }

    for k in knowledge:
        if k in q:
            return knowledge[k]

    return "I can help with Name, NIC, Address, Email, Phone, DOB, and government form fields."

# =========================================================
# AI RESPONSE ENGINE (HYBRID)
# =========================================================

def get_ai_response(question, selected_language):

    if client:
        try:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a Sri Lankan Government Form Assistant.

RULES:
- Detect user input language automatically.
- Always respond in {selected_language}.
- Give simple, clear answers.
- Focus on government forms (NIC, Name, Address, DOB, Email, Phone).
"""
                    },
                    {
                        "role": "user",
                        "content": question
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

target_lang = {
    "English": "en",
    "Tamil": "ta",
    "Sinhala": "si",
    "Hindi": "hi"
}[selected_language]

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>
.stApp{
    background: linear-gradient(to right,#0f172a,#1e293b);
    color:white;
}
h1,h2,h3,h4,h5,h6,p,label{
    color:white;
}
.chat-box{
    background:#1e293b;
    padding:15px;
    border-radius:15px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title(ui["sidebar"])

    if client:
        st.success(ui["online"])
    else:
        st.warning(ui["offline"])

# =========================================================
# TITLE
# =========================================================

st.title(ui["title"])

# =========================================================
# OCR
# =========================================================

st.write("## 📄 " + ui["upload"])

uploaded_file = st.file_uploader("Upload JPG/PNG", type=["jpg","jpeg","png"])

image = None
if uploaded_file:
    image = Image.open(uploaded_file)

if image:
    st.image(image, use_container_width=True)

    try:
        text = pytesseract.image_to_string(image)
        st.text(text)

        translated = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)

        st.success(translated)

    except Exception as e:
        st.error(f"OCR Error: {e}")

# =========================================================
# VOICE
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

    except Exception as e:
        st.error(f"Voice Error: {e}")

# =========================================================
# TEXT INPUT
# =========================================================

text_question = st.text_input(ui["ask"])
user_question = text_question or voice_question

# =========================================================
# CHATBOT OUTPUT
# =========================================================

if user_question:

    with st.spinner("Thinking..."):
        answer = get_ai_response(user_question, selected_language)

        st.markdown(f"""
        <div class="chat-box">
        🤖 {answer}
        </div>
        """, unsafe_allow_html=True)

        try:
            tts = gTTS(text=answer, lang=target_lang)
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp.name)
            st.audio(temp.name)
        except:
            pass

# =========================================================
# FOOTER
# =========================================================

st.write("---")
st.markdown("🇱🇰 Made By Jathusvarman")
