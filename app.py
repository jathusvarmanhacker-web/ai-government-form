# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT (HYBRID VERSION)
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
# LOAD API KEY (SAFE)
# =========================================================

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None

# =========================================================
# OFFLINE AI BOT (NO API REQUIRED)
# =========================================================

def offline_bot(question):
    q = question.lower()

    if "nic" in q:
        return "NIC is National Identity Card used in Sri Lanka."

    elif "passport" in q:
        return "Passport is an official travel document for international travel."

    elif "birth" in q:
        return "Birth certificate is an official record of birth details."

    elif "address" in q:
        return "Address means your residential location details."

    elif "form" in q:
        return "Government forms are documents used for official applications."

    elif "hello" in q:
        return "Hello! I am your Government Form Assistant."

    else:
        return "I am offline AI. Ask simple questions about NIC, passport, address, or forms."

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Government Form Assistant",
    page_icon="🇱🇰",
    layout="wide"
)

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
    st.title("🤖 AI Assistant")

    if api_key:
        st.success("🔗 Online Mode (ChatGPT)")
    else:
        st.warning("⚡ Offline Mode")

    st.info("""
🇱🇰 Government Form Assistant

✅ OCR Scanner  
✅ ChatGPT / Offline AI  
✅ Voice Input  
""")

# =========================================================
# TITLE
# =========================================================

st.title("🇱🇰 AI Government Form Assistant (Hybrid)")

# =========================================================
# LANGUAGE
# =========================================================

languages = {
    "English": "en",
    "Tamil": "ta",
    "Sinhala": "si",
    "Hindi": "hi"
}

selected_language = st.selectbox("🌐 Select Language", list(languages.keys()))
target_lang = languages[selected_language]

# =========================================================
# IMAGE OCR
# =========================================================

st.write("## 📄 Upload Form")

uploaded_file = st.file_uploader("Upload JPG / PNG", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file:
    image = Image.open(uploaded_file)

if image:
    st.image(image, use_container_width=True)

    try:
        extracted_text = pytesseract.image_to_string(image)
        st.text(extracted_text)

        translated_text = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(extracted_text)

        st.success(translated_text)

    except Exception as e:
        st.error(f"OCR Error: {e}")

# =========================================================
# VOICE INPUT
# =========================================================

st.write("## 🎤 Voice Input")

audio_bytes = audio_recorder()
voice_question = ""

if audio_bytes:
    st.audio(audio_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        voice_question = recognizer.recognize_google(audio)
        st.success(f"You said: {voice_question}")

    except Exception as e:
        st.error(f"Voice Error: {e}")

# =========================================================
# TEXT INPUT
# =========================================================

text_question = st.text_input("💬 Ask Your Question")

user_question = text_question or voice_question

# =========================================================
# AI RESPONSE (HYBRID LOGIC)
# =========================================================

if user_question:

    with st.spinner("Thinking..."):

        # -----------------------------
        # ONLINE MODE (CHATGPT)
        # -----------------------------
        if client:

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Sri Lankan government form assistant."},
                        {"role": "user", "content": user_question}
                    ]
                )

                ai_answer = response.choices[0].message.content

            except Exception as e:
                ai_answer = offline_bot(user_question)

        # -----------------------------
        # OFFLINE MODE
        # -----------------------------
        else:
            ai_answer = offline_bot(user_question)

        # =================================================
        # SHOW ANSWER
        # =================================================

        st.markdown(f"""
        <div class="chat-box">
        🤖 {ai_answer}
        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # TEXT TO SPEECH
        # =================================================

        try:
            tts = gTTS(text=ai_answer, lang=target_lang)
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)
            st.audio(temp_audio.name)

        except Exception as e:
            st.error(f"TTS Error: {e}")

# =========================================================
# FOOTER
# =========================================================

st.write("---")
st.markdown("🇱🇰 Made By Jathusvarman")
