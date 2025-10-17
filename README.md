📖 PDF to Audiobook Converter 🔊

A modern, web-based graphical user interface (GUI) application built with Streamlit that converts the text content of any uploaded PDF file into a downloadable MP3 audiobook using the Google Text-to-Speech (gTTS) service.

🎯 Objective

The primary goal of this project is to provide a seamless utility for users to transform digital documents (PDFs) into audio content, making large files easier to consume, especially for multitasking or accessibility purposes.

✨ Features

Based on the project guide, this application implements the following key features:

PDF Text Extraction: Uses PyMuPDF (fitz) to reliably load and extract text from the uploaded PDF document.

Text Cleaning: Automatically cleans extracted text by stripping whitespace and replacing newlines with spaces for natural reading flow.

Audio Conversion: Converts the cleaned text to high-quality audio using the cloud-based gTTS library.

MP3 Output: Generates and provides the resulting audiobook in the widely compatible MP3 format.

Interactive UI: A user-friendly interface built with Streamlit for file upload and configuration.

Language Control: Allows the user to select the language of the PDF content, ensuring correct pronunciation by gTTS.

Audio Playback & Download: Provides an immediate audio player to preview the audiobook and a button to download the MP3 file.

🛠️ Tools & Technologies

Tool

Purpose

Streamlit

Creates the interactive web application GUI.

PyMuPDF (fitz)

Efficiently extracts text content from PDF files.

gTTS

Handles the Text-to-Speech conversion (requires internet access).

Python

The core programming language for the application logic.

🚀 Installation and Setup

1. Clone the Repository

git clone [https://github.com/yourusername/pdf-audiobook-converter.git](https://github.com/yourusername/pdf-audiobook-converter.git)
cd pdf-audiobook-converter


2. Create a Virtual Environment (Recommended)

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


3. Install Dependencies

Install the required Python libraries using pip:

pip install streamlit PyMuPDF gTTS


(Note: comtypes is typically related to the deprecated pyttsx3 and is not needed for this gTTS implementation.)

💡 Usage

1. Run the Streamlit Application

Start the application from your terminal:

streamlit run app.py


(Assuming your main script is named app.py)

2. Access the App

A local URL (usually http://localhost:8501) will open in your default web browser.

3. Generate Audiobook

Upload: Click the "Select a PDF file" button in the sidebar and choose your document.

Configure: Select the appropriate language for the PDF content.

Generate: Click the "Generate Audiobook" button.

Listen & Download: Once processing is complete, an audio player will appear in the main area, along with a "Download MP3" button.

📂 Deliverables Structure

The final project repository should include the following file structure to be considered complete:

pdf-audiobook-converter/
├── app.py                      # Main Streamlit application code
├── README.md                   # This instruction file
├── requirements.txt            # List of required Python packages
├── .gitignore                  # Standard git ignore file
└── samples/
    ├── sample_document.pdf     # Example PDF file (Deliverable)
    └── sample_audiobook.mp3    # Example output audio file (Deliverable)


⚙️ Dependencies (requirements.txt)

streamlit>=1.0.0
PyMuPDF>=1.20.0
gTTS>=2.2.4


Be aware that gTTS requires a working internet connection to fetch the audio data from Google's servers.
