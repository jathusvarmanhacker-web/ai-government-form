# =========================================================
# SRI LANKA AI GOVERNMENT FORM ASSISTANT
# FIXED VERSION
# =========================================================

import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np

# =========================================================
# TEST MESSAGE
# =========================================================

st.write("APP STARTED")

# =========================================================
# TESSERACT OCR PATH
# =========================================================



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

    # =====================================================
    # OCR
    # =====================================================

    extracted_text = ""

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
# FUTURE FEATURES
# =========================================================

st.write("--------------------------------------------------")

st.write("## 🚀 Future AI Features")

st.write("""
🎤 Voice Assistant  
🧠 AI Chatbot  
📄 PDF Form Reading  
✍️ Auto Form Filling  
🌐 Government Website Navigation  
📱 Mobile App Version  
""")
