# =========================================================
# SRI LANKA AI GOVERNMENT FORM ASSISTANT
# FINAL AI CHATBOT + VOICE VERSION
# =========================================================

import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np
from gtts import gTTS
import tempfile

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="AI Government Form Assistant",
    page_icon="🇱🇰",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🇱🇰 AI Government Form Assistant")
st.subheader("Tamil • Sinhala • English • Multi-Language Support")

st.write("""
Upload a government form and get:

- OCR text reading
- Translation
- AI guidance
- Missing field detection
- AI chatbot support
- Voice assistant
""")

# =========================================================
# LANGUAGE SELECTION
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
# IMAGE INPUT
# =========================================================

st.write("## 📄 Upload Form")

uploaded_file = st.file_uploader(
    "Upload JPG / PNG Form",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

# =========================================================
# PROCESS IMAGE
# =========================================================

if image is not None:

    st.image(
        image,
        caption="Uploaded Form",
        use_container_width=True
    )

    st.write("## 🔍 Reading Form Text...")

    extracted_text = ""

    # =====================================================
    # OCR
    # =====================================================

    try:

        extracted_text = pytesseract.image_to_string(
            image,
            lang='eng'
        )

        st.write("### 📄 Extracted Text")
        st.text(extracted_text)

    except Exception as e:

        st.error(f"OCR Error: {e}")

    # =====================================================
    # TRANSLATION
    # =====================================================

    st.write("## 🌐 Translation")

    try:

        translated_text = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(extracted_text)

        st.success(translated_text)

    except Exception as e:

        st.error(f"Translation Error: {e}")

    # =====================================================
    # FIELD GUIDANCE
    # =====================================================

    st.write("## 🤖 AI Field Guidance")

    field_guides = {

        "Surname": {
            "English": "Enter your family name.",
            "Tamil": "உங்கள் குடும்பப்பெயரை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ වාසගම ඇතුළත් කරන්න."
        },

        "NIC Number": {
            "English": "Enter your NIC number.",
            "Tamil": "உங்கள் அடையாள அட்டை எண்ணை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ හැඳුනුම්පත් අංකය ඇතුළත් කරන්න."
        },

        "Date of Birth": {
            "English": "Enter your birth date.",
            "Tamil": "உங்கள் பிறந்த தேதியை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ උපන්දිනය ඇතුළත් කරන්න."
        }
    }

    found_field = False

    for field, explanation in field_guides.items():

        if field.lower() in extracted_text.lower():

            found_field = True

            st.info(field)

            if selected_language in explanation:
                st.write(explanation[selected_language])
            else:
                st.write(explanation["English"])

    if not found_field:
        st.warning("No known fields detected.")

    # =====================================================
    # MISSING FIELD DETECTION
    # =====================================================

    st.write("## ⚠️ Missing Field Detection")

    required_fields = [
        "Surname",
        "NIC Number",
        "Date of Birth"
    ]

    missing = []

    for field in required_fields:

        if field.lower() not in extracted_text.lower():
            missing.append(field)

    if len(missing) == 0:

        st.success("✅ No important fields missing.")

    else:

        for m in missing:
            st.warning(f"Possible Missing Field: {m}")

# =========================================================
# SMART AI CHATBOT
# =========================================================

st.write("--------------------------------------------------")
st.write("## 🤖 Smart AI Assistant")

st.write("""
Ask questions like:
- What is NIC?
- How to fill surname?
- What is permanent address?
- Hello
""")

user_question = st.text_input(
    "💬 Ask Your Question"
)

ai_answer = ""

if user_question:

    question = user_question.lower()

    # =====================================================
    # AI ANSWERS
    # =====================================================

    if "nic" in question:

        if selected_language == "Tamil":
            ai_answer = "NIC என்பது தேசிய அடையாள அட்டை எண்."

        elif selected_language == "Sinhala":
            ai_answer = "NIC යනු ජාතික හැඳුනුම්පත් අංකයයි."

        else:
            ai_answer = "NIC means National Identity Card Number."

    elif "surname" in question:

        if selected_language == "Tamil":
            ai_answer = "Surname என்பது குடும்பப்பெயர்."

        elif selected_language == "Sinhala":
            ai_answer = "Surname යනු ඔබගේ වාසගමයි."

        else:
            ai_answer = "Surname means your family name."

    elif "address" in question:

        if selected_language == "Tamil":
            ai_answer = "Permanent Address என்பது உங்கள் நிரந்தர முகவரி."

        elif selected_language == "Sinhala":
            ai_answer = "Permanent Address යනු ඔබගේ ස්ථිර ලිපිනයයි."

        else:
            ai_answer = "Permanent Address means your home address."

    elif "birth" in question:

        if selected_language == "Tamil":
            ai_answer = "உங்கள் பிறந்த தேதியை சரியாக எழுதுங்கள்."

        elif selected_language == "Sinhala":
            ai_answer = "ඔබගේ උපන්දිනය නිවැරදිව ඇතුළත් කරන්න."

        else:
            ai_answer = "Enter your correct birth date."

    elif "hello" in question:

        if selected_language == "Tamil":
            ai_answer = "வணக்கம்! நான் உங்கள் AI உதவியாளர்."

        elif selected_language == "Sinhala":
            ai_answer = "ආයුබෝවන්! මම ඔබගේ AI සහායකයා."

        else:
            ai_answer = "Hello! I am your AI Government Form Assistant."

    elif "how to fill" in question:

        if selected_language == "Tamil":
            ai_answer = "ஒவ்வொரு புலத்தையும் கவனமாக நிரப்புங்கள்."

        elif selected_language == "Sinhala":
            ai_answer = "සෑම කොටසක්ම සැලකිලිමත්ව පුරවන්න."

        else:
            ai_answer = "Fill every field carefully."

    else:

        if selected_language == "Tamil":
            ai_answer = "மன்னிக்கவும். அந்த கேள்வி இன்னும் ஆதரிக்கப்படவில்லை."

        elif selected_language == "Sinhala":
            ai_answer = "සමාවන්න. එම ප්‍රශ්නයට තවම සහය නොමැත."

        else:
            ai_answer = "Sorry, I do not understand that question yet."

    # =====================================================
    # SHOW ANSWER
    # =====================================================

    st.success(ai_answer)

    # =====================================================
    # VOICE OUTPUT
    # =====================================================

    try:

        tts = gTTS(ai_answer)

        temp_audio = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp_audio.name)

        st.audio(temp_audio.name)

    except Exception as e:

        st.error(f"Voice Error: {e}")

# =========================================================
# FUTURE FEATURES
# =========================================================

st.write("--------------------------------------------------")

st.write("## 🚀 Future AI Features")

st.write("""
🎤 Voice Assistant  
🧠 Advanced AI Chatbot  
📄 PDF Form Reading  
✍️ Auto Form Filling  
🌐 Government Website Navigation  
📱 Mobile App Version  
🔊 Text-to-Speech Guidance  
📌 Smart Error Detection  
☁️ Cloud Database Support  
""")
           
