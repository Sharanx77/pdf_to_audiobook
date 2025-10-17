import streamlit as st
import fitz  # PyMuPDF
from gtts import gTTS
import os
from io import BytesIO

# --- Core Conversion Function ---
def convert_pdf_to_speech_gtts(pdf_file, lang='en'):
    """
    Extracts text from a PDF file, converts it to speech using gTTS, 
    and returns audio bytes.
    gTTS handles speech rate and volume internally based on its model.
    """
    try:
        st.info("Extracting text from PDF...")
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        # Loop through pages to extract text
        for page in doc:
            full_text += page.get_text("text")
        doc.close()
        
        # Basic text cleaning
        full_text = full_text.strip().replace('\n', ' ')
        
        if not full_text:
            st.warning("Could not find any text in the selected PDF file.")
            return None

        # gTTS has a character limit (around 5000), so we may need to handle chunks
        # However, for simplicity and typical usage, we'll process the full text first.
        # For very large files, a chunking mechanism would be necessary.
        
        st.info("Converting text to speech using gTTS... This may take a moment.")
        
        # Create the gTTS object
        tts = gTTS(text=full_text, lang=lang)
        
        # Save the audio data directly to a BytesIO object (in-memory file)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0) # Rewind the stream to the beginning
        
        audio_bytes = audio_fp.read()
        
        st.success("Audiobook generated successfully!")
        return audio_bytes

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error("Check if you have an active internet connection, as gTTS requires it.")
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="PDF to Audiobook (gTTS)", page_icon="📖", layout="wide")

st.title("📖 PDF to Audiobook Converter (gTTS) 🔊")
st.markdown("Upload your PDF, select the language, and generate an audiobook. **Requires an active internet connection.**")

# --- Sidebar for controls ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

    st.subheader("Audio Settings")
    # gTTS supports many languages. 'en' (English) is default.
    language = st.selectbox(
        "Select Language for TTS (Based on PDF content)",
        options=['en', 'hi', 'es', 'fr', 'de'], # Common language codes
        format_func=lambda x: f"{x} - {'en': 'English', 'hi': 'Hindi', 'es': 'Spanish', 'fr': 'French', 'de': 'German'}"
    )

    # Note: gTTS does not have direct controls for rate/volume like pyttsx3.
    st.markdown("_Note: gTTS uses cloud services and does not expose direct controls for WPM or Volume._")
    
    convert_button = st.button("Generate Audiobook", type="primary", use_container_width=True)

# --- Main Area for Output ---
if convert_button and uploaded_file is not None:
    # Clear session state for new conversion
    if 'audio_data' in st.session_state:
        del st.session_state.audio_data
        
    with st.spinner("Generating your audiobook... Please wait."):
        # Pass the language code to the conversion function
        audio_data = convert_pdf_to_speech_gtts(uploaded_file, lang=language)
        
        if audio_data:
            # Store audio data in session state to persist it
            st.session_state.audio_data = audio_data
            # Sanitize filename for download
            original_filename = uploaded_file.name
            file_name = original_filename.replace('.pdf', f'_{language}.mp3')
            st.session_state.file_name = file_name
        else:
            # Clear any previous audio data if generation fails
            if 'audio_data' in st.session_state:
                del st.session_state.audio_data

# Display audio player and download button if audio data exists in session state
if 'audio_data' in st.session_state and st.session_state.audio_data:
    st.header("Your Audiobook is Ready! ▶️")
    
    st.audio(st.session_state.audio_data, format="audio/mp3")

    st.download_button(
        label="💾 Download MP3",
        data=st.session_state.audio_data,
        file_name=st.session_state.file_name,
        mime="audio/mp3",
        use_container_width=True
    )
elif uploaded_file is None and convert_button:
    st.warning("Please upload a PDF file first.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and **gTTS**")



