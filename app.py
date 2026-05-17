# =========================================================
# SRI LANKA AI GOVERNMENT FORM ASSISTANT
# WITH AI CHAT ASSISTANT
# =========================================================

import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
import numpy as np

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
- AI form assistant
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
# AI FORM ASSISTANT CHAT
# =========================================================

st.write("--------------------------------------------------")
st.write("## 🤖 AI Form Assistant")

st.write("""
Ask questions like:
- What is NIC?
- How to fill surname?
- What is permanent address?
- How to upload form?
""")

user_question = st.text_input(
    "💬 Ask Your Question"
)

if user_question:

    question = user_question.lower()

    if "nic" in question:

        if selected_language == "Tamil":
            st.success(
                "NIC என்பது தேசிய அடையாள அட்டை எண்."
            )

        elif selected_language == "Sinhala":
            st.success(
                "NIC යනු ජාතික හැඳුනුම්පත් අංකයයි."
            )

        else:
            st.success(
                "NIC means National Identity Card Number."
            )

    elif "surname" in question:

        if selected_language == "Tamil":
            st.success(
                "Surname என்பது குடும்பப்பெயர்."
            )

        elif selected_language == "Sinhala":
            st.success(
                "Surname යනු ඔබගේ වාසගමයි."
            )

        else:
            st.success(
                "Surname means your family name."
            )

    elif "address" in question:

        if selected_language == "Tamil":
            st.success(
                "Permanent Address என்பது உங்கள் நிரந்தர முகவரி."
            )

        elif selected_language == "Sinhala":
            st.success(
                "Permanent Address යනු ඔබගේ ස්ථිර ලිපිනයයි."
            )

        else:
            st.success(
                "Permanent Address means your home address."
            )

    elif "date of birth" in question:

        if selected_language == "Tamil":
            st.success(
                "உங்கள் பிறந்த தேதியை சரியாக எழுதுங்கள்."
            )

        elif selected_language == "Sinhala":
            st.success(
                "ඔබගේ උපන්දිනය නිවැරදිව ඇතුළත් කරන්න."
            )

        else:
            st.success(
                "Enter your birth date correctly."
            )

    elif "how to fill" in question:

        if selected_language == "Tamil":
            st.success(
                "ஒவ்வொரு புலத்தையும் கவனமாக நிரப்புங்கள்."
            )

        elif selected_language == "Sinhala":
            st.success(
                "සෑම කොටසක්ම සැලකිලිමත්ව පුරවන්න."
            )

        else:
            st.success(
                "Fill every field carefully with correct details."
            )

    elif "upload" in question:

        if selected_language == "Tamil":
            st.success(
                "JPG அல்லது PNG கோப்பை பதிவேற்றவும்."
            )

        elif selected_language == "Sinhala":
            st.success(
                "JPG හෝ PNG ගොනුවක් උඩුගත කරන්න."
            )

        else:
            st.success(
                "Upload a JPG or PNG form image."
            )

    else:

        if selected_language == "Tamil":
            st.info(
                "மன்னிக்கவும். அந்த கேள்வி இன்னும் ஆதரிக்கப்படவில்லை."
            )

        elif selected_language == "Sinhala":
            st.info(
                "සමාවන්න. එම ප්‍රශ්නයට තවම සහය නොමැත."
            )

        else:
            st.info(
                "Sorry, I do not understand that question yet."
            )

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
🔊 Text-to-Speech Guidance  
📌 Smart Error Detection  
☁️ Cloud Database Support                                                                                                             Made By V.Jathusvarman
""")
