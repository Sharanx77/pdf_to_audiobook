import streamlit as st
import fitz  # PyMuPDF
from gtts import gTTS
import os
from io import BytesIO

# --- Core Conversion Function ---
# This function now uses gTTS, which is more reliable for web deployment.
def convert_pdf_to_speech(pdf_file):
    """
    Extracts text from a PDF file, converts it to speech using gTTS,
    and returns the audio data as bytes.
    """
    try:
        st.info("Extracting text from PDF...")
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
        doc.close()
        
        # Clean up text for better speech synthesis
        full_text = full_text.strip().replace('\n', ' ')
        
        if not full_text:
            st.warning("Could not find any text in the selected PDF file.")
            return None

        st.info("Converting text to speech... This may take a moment.")
        
        # Use gTTS to convert text to speech directly in memory
        tts = gTTS(text=full_text, lang='en')
        
        # Use a BytesIO object as an in-memory "file"
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0) # Go to the beginning of the in-memory file
        
        audio_bytes = audio_fp.read()
        st.success("Audiobook generated successfully!")
        return audio_bytes

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="PDF to Audiobook", page_icon="📖", layout="wide")

st.title("📖 PDF to Audiobook Converter 🔊")
st.markdown("Upload your PDF and click 'Generate Audiobook' to listen or download.")

# --- Sidebar for controls ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

    # NOTE: Speed and Volume sliders are removed as gTTS does not support them.
    
    convert_button = st.button("Generate Audiobook", type="primary", use_container_width=True)

# --- Main Area for Output ---
if convert_button and uploaded_file is not None:
    with st.spinner("Generating your audiobook... Please wait."):
        audio_data = convert_pdf_to_speech(uploaded_file)
        
        if audio_data:
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

