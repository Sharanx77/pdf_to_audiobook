import streamlit as st
import fitz  # PyMuPDF
import pyttsx3
import os
import threading
from io import BytesIO

# --- Engine Initialization ---
# This needs to be done once and can be tricky with Streamlit's reruns.
# We use a lock to ensure it's initialized only once.
engine_lock = threading.Lock()

@st.cache_resource
def get_tts_engine():
    """Initializes the pyttsx3 engine."""
    try:
        # ** THE FIX IS HERE: Explicitly specify the SAPI5 driver for Windows **
        engine = pyttsx3.init(driverName='sapi5')
        return engine
    except Exception as e:
        st.error(f"Failed to initialize TTS engine: {e}")
        st.warning("Please ensure you have a TTS engine installed on your system (e.g., eSpeak on Linux, SAPI5 on Windows).")
        return None

# --- Core Conversion Function ---
def convert_pdf_to_speech(pdf_file, rate, volume, file_format='mp3'):
    """
    Extracts text from a PDF file, converts it to speech, and returns audio bytes.
    """
    try:
        st.info("Extracting text from PDF...")
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
        doc.close()
        
        full_text = full_text.strip().replace('\n', ' ')
        
        if not full_text:
            st.warning("Could not find any text in the selected PDF file.")
            return None

        st.info("Converting text to speech... This may take a moment.")
        
        # We save to a file and then read it into memory for st.audio and st.download_button
        temp_audio_file = f"temp_audio.{file_format}"
        
        engine = get_tts_engine()
        if engine is None:
            return None
            
        # Set properties within a thread-safe context
        with engine_lock:
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            engine.save_to_file(full_text, temp_audio_file)
            engine.runAndWait()

        # Read the generated file into a BytesIO object
        if os.path.exists(temp_audio_file):
            with open(temp_audio_file, "rb") as f:
                audio_bytes = f.read()
            os.remove(temp_audio_file)  # Clean up the temp file
            st.success("Audiobook generated successfully!")
            return audio_bytes
        else:
            st.error("Failed to create the audio file.")
            return None

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="PDF to Audiobook", page_icon="📖", layout="wide")

st.title("📖 PDF to Audiobook Converter 🔊")
st.markdown("Upload your PDF, adjust the settings, and generate an audiobook to listen to or download.")

# --- Sidebar for controls ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

    st.subheader("Audio Settings")
    rate = st.slider("Speed (words per minute)", 100, 300, 175, 10)
    volume = st.slider("Volume", 0.0, 1.0, 1.0, 0.1)
    
    convert_button = st.button("Generate Audiobook", type="primary", use_container_width=True)

# --- Main Area for Output ---
if convert_button and uploaded_file is not None:
    with st.spinner("Generating your audiobook... Please wait."):
        audio_data = convert_pdf_to_speech(uploaded_file, rate, volume)
        
        if audio_data:
            # Store audio data in session state to persist it
            st.session_state.audio_data = audio_data
            st.session_state.file_name = uploaded_file.name.replace('.pdf', '.mp3')
        else:
            # Clear any previous audio data if generation fails
            if 'audio_data' in st.session_state:
                del st.session_state.audio_data
            if 'file_name' in st.session_state:
                del st.session_state.file_name

# Display audio player and download button if audio data exists in session state
if 'audio_data' in st.session_state and st.session_state.audio_data:
    st.header("Your Audiobook is Ready!")
    
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
st.markdown("Made with ❤️ using Streamlit")
