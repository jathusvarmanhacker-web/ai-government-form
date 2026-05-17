# =========================================================
# SRI LANKA AI GOVERNMENT FORM ASSISTANT - FINAL VERSION
# =========================================================

import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
import cv2
import numpy as np

# =========================================================
# TESSERACT OCR PATH
# =========================================================

pytesseract.pytesseract.tesseract_cmd = \
r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
- Visual assistance
""")

# =========================================================
# LANGUAGE SELECTION
# =========================================================

languages = {
    "English": "en",
    "Tamil": "ta",
    "Sinhala": "si",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Japanese": "ja",
    "Chinese": "zh-cn"
}

selected_language = st.selectbox(
    "🌐 Select Language",
    list(languages.keys())
)

target_lang = languages[selected_language]

# =========================================================
# IMAGE INPUT METHOD
# =========================================================

st.write("## 📄 Upload or Capture Form")

option = st.radio(
    "Choose Input Method",
    ["Upload Image", "Use Camera"]
)

image = None

# =========================================================
# FILE UPLOAD
# =========================================================

if option == "Upload Image":

    uploaded_file = st.file_uploader(
        "Upload JPG / PNG Form",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# =========================================================
# CAMERA INPUT
# =========================================================

elif option == "Use Camera":

    camera_image = st.camera_input("📷 Take Form Photo")

    if camera_image is not None:
        image = Image.open(camera_image)

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
    # OCR TEXT EXTRACTION
    # =====================================================

    try:

        extracted_text = pytesseract.image_to_string(
            image,
            lang='eng+tam+sin'
        )

        st.write("### 📄 Extracted Text")
        st.text(extracted_text)

    except Exception as e:

        st.error("OCR Error")
        st.write(e)

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

        st.error("Translation Error")
        st.write(e)

    # =====================================================
    # FIELD EXPLANATIONS
    # =====================================================

    st.write("## 🤖 AI Field Guidance")

    field_guides = {

        "Surname": {
            "English": "Enter your family name.",
            "Tamil": "உங்கள் குடும்பப்பெயரை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ වාසගම ඇතුළත් කරන්න."
        },

        "Permanent Address": {
            "English": "Enter your permanent home address.",
            "Tamil": "உங்கள் நிரந்தர முகவரியை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ ස්ථිර ලිපිනය ඇතුළත් කරන්න."
        },

        "NIC Number": {
            "English": "Enter your National Identity Card number.",
            "Tamil": "உங்கள் தேசிய அடையாள அட்டை எண்ணை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ ජාතික හැඳුනුම්පත් අංකය ඇතුළත් කරන්න."
        },

        "Date of Birth": {
            "English": "Enter your birth date correctly.",
            "Tamil": "உங்கள் பிறந்த தேதியை சரியாக எழுதுங்கள்.",
            "Sinhala": "ඔබගේ උපන්දිනය නිවැරදිව ඇතුළත් කරන්න."
        },

        "Gender": {
            "English": "Select your gender.",
            "Tamil": "உங்கள் பாலினத்தைத் தேர்வு செய்யுங்கள்.",
            "Sinhala": "ඔබගේ ලිංගය තෝරන්න."
        },

        "Telephone": {
            "English": "Enter your phone number.",
            "Tamil": "உங்கள் தொலைபேசி எண்ணை எழுதுங்கள்.",
            "Sinhala": "ඔබගේ දුරකථන අංකය ඇතුළත් කරන්න."
        }
    }

    found_field = False

    for field, explanation in field_guides.items():

        if field.lower() in extracted_text.lower():

            found_field = True

            st.info(f"### {field}")

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
        "Permanent Address",
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

    # =====================================================
    # VISUAL GUIDANCE
    # =====================================================

    st.write("## 🖼️ Visual Guidance")

    img_cv = np.array(image)

    cv2.rectangle(
        img_cv,
        (50, 50),
        (350, 140),
        (0, 255, 0),
        3
    )

    cv2.putText(
        img_cv,
        "Fill Carefully",
        (60, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    st.image(
        img_cv,
        caption="Guided Form",
        use_container_width=True
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
📂 Save Completed Forms  
☁️ Cloud Database Support  
""")