"""
Streamlit Frontend for Simple RAG System
Simplified UI - No sidebar, just query input and response
"""
import streamlit as st
import httpx
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "https://hardkpentium101-indicrag.hf.space")

st.set_page_config(
    page_title="Simple RAG",
    page_icon="🤖",
    layout="centered"
)

# Page title
st.title("🤖 indicRAG System")
st.markdown("Ask questions in any supported Indic language. The system will respond in the same language.")

# Supported languages
SUPPORTED_LANGUAGES = [
    {"code": "hi", "name": "Hindi", "native": "हिंदी"},
    {"code": "bn", "name": "Bengali", "native": "বাংলা"},
    {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
    {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
    {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
    {"code": "mr", "name": "Marathi", "native": "मराठी"},
    {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
    {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
    {"code": "te", "name": "Telugu", "native": "తెలుగు"},
]

# Language selection
st.subheader("Select Language")
language_options = [f"{lang['native']} ({lang['name']})" for lang in SUPPORTED_LANGUAGES]
selected_language = st.selectbox(
    "Choose a language",
    options=language_options,
    index=0,
    label_visibility="collapsed"
)

# Get language code from selection
selected_lang_code = SUPPORTED_LANGUAGES[language_options.index(selected_language)]["code"]

# Query input
st.subheader("Ask Your Question")
query = st.text_area(
    "Enter your question",
    height=100,
    placeholder=f"Type your question in {selected_language}...",
    label_visibility="collapsed"
)

# Submit button
col1, col2 = st.columns([1, 4])
with col1:
    submit_button = st.button("🔍 Search", type="primary", use_container_width=True)

# Process query
if submit_button and query.strip():
    with st.spinner("Searching and generating answer..."):
        try:
            # Make API request with extended timeout for CPU inference
            response = httpx.post(
                f"{BACKEND_URL}/query",
                json={
                    "query": query,
                    "top_k": 5,
                    "language": selected_lang_code
                },
                timeout=httpx.Timeout(300.0, connect=30.0, read=300.0)
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display answer
                st.subheader("Answer")
                st.write(result["answer"])
                
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except httpx.ConnectError:
            st.error(f"Could not connect to backend at {BACKEND_URL}. Make sure the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <style>
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
    }
    </style>
    <div class="footer">
        indicRAG System - Powered by Sarvam-1 and Qdrant
    </div>
    """,
    unsafe_allow_html=True
)
