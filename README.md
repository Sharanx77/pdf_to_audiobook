# 🔊 PDF to Audiobook Converter

## Project Objective
This is a desktop application designed to convert the text content of a **Portable Document Format (PDF)** file into **spoken audio**, effectively creating a personalized audiobook from any text-based PDF. Users can play the audio directly or export it as an MP3 file.



---

## ✨ Features

* **PDF Text Extraction:** Utilizes **PyMuPDF** for reliable loading and extraction of text from PDF documents.
* **Text Cleaning:** Pre-processes the extracted text to handle line breaks, multiple spaces, and empty pages, ensuring a smooth and continuous listening experience.
* **Text-to-Speech (TTS):** Converts the cleaned text into speech using the **pyttsx3** library.
* **Playback Controls:** Offers options to immediately **Play** the generated audio.
* **Export Functionality:** Allows users to **Export** the audiobook as a standard **MP3** audio file.
* **User Interface:** Built with **Tkinter** for an intuitive and easy-to-use graphical interface.
* **Audio Customization:** Control options to adjust the **Volume** and **Speech Rate (Speed)** of the narration.

---

## 🛠️ Requirements & Installation

### Prerequisites

* Python 3.x
* A compatible operating system (Windows, macOS, or Linux).

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [your_repository_url_here]
    cd pdf-to-audiobook-converter
    ```

2.  **Install Dependencies:**
    The core libraries are **PyMuPDF** and **pyttsx3**.
    ```bash
    pip install PyMuPDF pyttsx3
    ```
    *(Note: Tkinter is usually included with standard Python installations.)*

3.  **Run the Application:**
    ```bash
    python app_main.py
    # (Replace app_main.py with the name of your primary Python script)
    ```

---

## 🚀 How to Use

1.  **Launch the App:** Execute the main Python script.
2.  **Upload PDF:** Click the "**Load PDF**" or "**Browse**" button to select the PDF file you wish to convert.
3.  **Set Controls:** Use the sliders or input fields to fine-tune the **Volume** and **Speech Speed** to your liking.
4.  **Listen:** Click "**Play Audio**" to start listening to the PDF content directly.
5.  **Save:** Click "**Export to MP3**" to save the full audio file to your desired location on your computer.

---

## 📂 Deliverables

The repository includes the following:

* **GUI Application Code:** The full source code for the converter.
* **`sample.pdf`:** A small sample PDF file for testing the conversion feature.
* **`sample_audio.mp3`:** An example of the output MP3 file generated from the sample PDF.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for full details.

### MIT License
