# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT (FULL FINAL VERSION)
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
api_key = os.getenv("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")
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
        "select_lang": "Select Language",
        "sidebar": "AI Assistant",
        "online": "ONLINE MODE (ChatGPT)",
        "offline": "OFFLINE MODE",
    },
    "Tamil": {
        "title": "AI அரசு படிவ உதவியாளர்",
        "upload": "படிவத்தை பதிவேற்றவும்",
        "voice": "குரல் உள்ளீடு",
        "ask": "உங்கள் கேள்வியை கேளுங்கள்",
        "select_lang": "மொழியை தேர்வு செய்க",
        "sidebar": "AI உதவியாளர்",
        "online": "ஆன்லைன் முறை (ChatGPT)",
        "offline": "ஆஃப்லைன் முறை",
    },
    "Sinhala": {
        "title": "AI රජයේ පෝරම සහායක",
        "upload": "පෝරමය උඩුගත කරන්න",
        "voice": "හඬ ආදානය",
        "ask": "ඔබේ ප්‍රශ්නය අසන්න",
        "select_lang": "භාෂාව තෝරන්න",
        "sidebar": "AI සහායක",
        "online": "මාර්ගගත ක්‍රමය (ChatGPT)",
        "offline": "අක්‍රිය ක්‍රමය",
    },
    "Hindi": {
        "title": "AI सरकारी फॉर्म सहायक",
        "upload": "फॉर्म अपलोड करें",
        "voice": "आवाज़ इनपुट",
        "ask": "अपना प्रश्न पूछें",
        "select_lang": "भाषा चुनें",
        "sidebar": "AI सहायक",
        "online": "ऑनलाइन मोड (ChatGPT)",
        "offline": "ऑफलाइन मोड",
    }
}

# =========================================================
# OFFLINE BOT (FORM KNOWLEDGE)
# =========================================================

def offline_bot(question):
    q = question.lower()

    if "full name" in q or "name" in q:
        return "Full Name means your complete legal name."

    elif "date of birth" in q:
        return "Date of Birth is your birth date (DD/MM/YYYY)."

    elif "address" in q:
        return "Address means your home location details."

    elif "phone" in q:
        return "Phone Number is your contact number."

    elif "email" in q:
        return "Email is used for communication."

    elif "nationality" in q:
        return "Nationality means your country."

    elif "gender" in q:
        return "Gender can be male, female, or other."

    elif "occupation" in q:
        return "Occupation means job or student status."

    elif "nic" in q or "id" in q:
        return "In Sri Lanka, ID is NIC (National Identity Card)."

    elif "signature" in q:
        return "Signature is your official confirmation mark."

    elif "hello" in q:
        return "Hello! I am your Government Form Assistant."

    else:
        return "I can help with form fields like Name, DOB, NIC, Address, Email, Phone."

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
# UI STYLE
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
    margin-top:10px;
    color:white;
    font-size:18px;
}
.stTextInput input{
    background-color:#1e293b;
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

    st.info("🇱🇰 Government Form Assistant")

# =========================================================
# TITLE
# =========================================================

st.title(ui["title"])

# =========================================================
# OCR SECTION
# =========================================================

st.write("## 📄 " + ui["upload"])

uploaded_file = st.file_uploader("JPG / PNG", type=["jpg", "jpeg", "png"])

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
# VOICE INPUT
# =========================================================

st.write("## 🎤 " + ui["voice"])

audio_bytes = audio_recorder()
voice_question = ""

if audio_bytes:
    st.audio(audio_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    r = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
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
# AI RESPONSE (HYBRID)
# =========================================================

if user_question:

    with st.spinner("Thinking..."):

        if client:
            try:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a government form assistant."},
                        {"role": "user", "content": user_question}
                    ]
                )
                answer = res.choices[0].message.content

            except:
                answer = offline_bot(user_question)
        else:
            answer = offline_bot(user_question)

        st.markdown(f"""
        <div class="chat-box">
        🤖 {answer}
        </div>
        """, unsafe_allow_html=True)

        # TEXT TO SPEECH
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
