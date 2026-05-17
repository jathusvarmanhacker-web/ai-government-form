# =========================================================
# 🇱🇰 ADVANCED AI GOVERNMENT FORM ASSISTANT
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
import google.generativeai as genai

# =========================================================
# GEMINI AI API
# =========================================================

# ⚠️ PUT YOUR NEW API KEY HERE
genai.configure(api_key="AIzaSyDCtzP6_skl5A9S1W2NlGAI08NDN0n5--I")

# ✅ FIXED MODEL
model = genai.GenerativeModel("gemini-1.5-flash")

# =========================================================
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

.stTextInput > div > div > input{
    background-color:#1e293b;
    color:white;
    border-radius:10px;
}

.stButton button{
    border-radius:10px;
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
✅ AI Chatbot
✅ Translation
✅ Voice Assistant
✅ Multi Language
""")

    st.write("---")

    st.write("Made By Jathusvarman")

# =========================================================
# TITLE
# =========================================================

st.title("🇱🇰 AI Government Form Assistant")

st.subheader("Tamil • Sinhala • English • Hindi")

st.write("""
Upload government forms and ask questions using text or voice.
""")

# =========================================================
# LANGUAGE
# =========================================================

languages = {
    "English": "en",
    "Tamil": "ta",
    "Sinhala": "si",
    "Hindi": "hi"
}

selected_language = st.selectbox(
    "🌐 Select Language",
    list(languages.keys())
)

target_lang = languages[selected_language]

# =========================================================
# FILE UPLOAD
# =========================================================

st.write("## 📄 Upload Government Form")

uploaded_file = st.file_uploader(
    "Upload JPG / PNG Image",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

# =========================================================
# OCR SECTION
# =========================================================

if image is not None:

    st.image(
        image,
        caption="Uploaded Form",
        use_container_width=True
    )

    st.write("## 🔍 Extracting Text")

    try:

        extracted_text = pytesseract.image_to_string(
            image,
            lang='eng'
        )

        st.write("### 📄 Extracted Text")

        st.text(extracted_text)

        # =================================================
        # TRANSLATION
        # =================================================

        st.write("## 🌐 Translation")

        translated_text = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(extracted_text)

        st.success(translated_text)

    except Exception as e:

        st.error(f"OCR Error: {e}")

# =========================================================
# AI CHATBOT
# =========================================================

st.write("---")

st.write("## 🤖 Smart AI Assistant")

st.write("""
Examples:
- What is NIC?
- What is surname?
- Explain passport
- What is permanent address?
- How to fill government forms?
""")

# =========================================================
# VOICE INPUT
# =========================================================

st.write("## 🎤 Voice Input")

audio_bytes = audio_recorder(
    text="Click To Record",
    recording_color="#ff0000",
    neutral_color="#00ff00",
    icon_name="microphone",
    icon_size="2x"
)

voice_question = ""

if audio_bytes:

    st.audio(audio_bytes, format="audio/wav")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as f:

        f.write(audio_bytes)

        audio_path = f.name

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

        voice_question = recognizer.recognize_google(
            audio,
            language=target_lang
        )

        st.success(f"You said: {voice_question}")

    except Exception as e:

        st.error(f"Voice Recognition Error: {e}")

# =========================================================
# TEXT INPUT
# =========================================================

text_question = st.text_input(
    "💬 Ask Your Question"
)

user_question = ""

if text_question:
    user_question = text_question

elif voice_question:
    user_question = voice_question

# =========================================================
# AI RESPONSE
# =========================================================

if user_question:

    with st.spinner("Thinking..."):

        try:

            prompt = f"""
You are a helpful Sri Lankan Government Form AI Assistant.

Answer clearly in {selected_language} language.

Help users understand:
- NIC
- Passport
- Birth certificate
- Government applications
- Address fields
- Personal details
- School forms
- Official forms

User Question:
{user_question}
"""

            response = model.generate_content(prompt)

            ai_answer = response.text

            st.markdown(f"""
<div class="chat-box">
🤖 {ai_answer}
</div>
""", unsafe_allow_html=True)

            # =============================================
            # TEXT TO SPEECH
            # =============================================

            try:

                tts = gTTS(
                    text=ai_answer,
                    lang=target_lang
                )

                temp_audio = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                )

                tts.save(temp_audio.name)

                st.audio(temp_audio.name)

            except Exception as e:

                st.error(f"Voice Output Error: {e}")

        except Exception as e:

            st.error(f"AI Error: {e}")

# =========================================================
# FUTURE FEATURES
# =========================================================

st.write("---")

st.write("## 🚀 Future Features")

st.write("""
🧠 Real-time AI support
📄 PDF support
📱 Mobile app
☁️ Database storage
🔊 Better voice assistant
🌐 Sinhala OCR
📷 Camera scanner
""")

# =========================================================
# FOOTER
# =========================================================

st.write("---")

st.markdown("""
<center>
<h4>🇱🇰 AI Government Form Assistant</h4>
<p>Made By Jathusvarman</p>
</center>
""", unsafe_allow_html=True)
