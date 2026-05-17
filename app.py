# =========================================================
# 🇱🇰 AI GOVERNMENT FORM ASSISTANT (CHATGPT VERSION)
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
from openai import OpenAI

# =========================================================
# OPENAI CHATGPT API
# =========================================================

client = OpenAI(api_key="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"
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Government Form Assistant",
    page_icon="🇱🇰",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
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
    st.info("""
🇱🇰 Sri Lanka Government Form Helper

✅ OCR Scanner  
✅ ChatGPT AI  
✅ Translation  
✅ Voice Assistant  
""")
    st.write("Made By Jathusvarman")

# =========================================================
# TITLE
# =========================================================

st.title("🇱🇰 AI Government Form Assistant")

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
# IMAGE UPLOAD + OCR
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
# CHATGPT RESPONSE
# =========================================================

if user_question:

    with st.spinner("Thinking..."):

        try:
            prompt = f"""
You are a Sri Lankan Government Form Assistant.

Answer clearly in {selected_language}.

User Question:
{user_question}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful government form assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            ai_answer = response.choices[0].message.content

            st.markdown(f"""
            <div class="chat-box">
            🤖 {ai_answer}
            </div>
            """, unsafe_allow_html=True)

            # TEXT TO SPEECH
            try:
                tts = gTTS(text=ai_answer, lang=target_lang)
                temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_audio.name)
                st.audio(temp_audio.name)

            except Exception as e:
                st.error(f"TTS Error: {e}")

        except Exception as e:
            st.error(f"AI Error: {e}")

# =========================================================
# FOOTER
# =========================================================

st.write("---")
st.markdown("🇱🇰 Made By Jathusvarman")
