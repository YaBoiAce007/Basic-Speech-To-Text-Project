# Speech To Text Application 🎙️

A simple Speech-to-Text application built using **OpenAI Whisper**, **FastAPI**, and **Streamlit**.

The application allows users to upload audio files, transcribe them using Whisper, view timestamped segments, detect possible non-speech sounds, and manually correct transcription errors.

---

## Features ✨

- 🎧 Upload audio files (`.wav`, `.mp3`, `.m4a`)
- 📝 Automatic speech transcription using OpenAI Whisper
- ⏱️ Timestamped transcription segments
- 🔊 Detection of possible non-speech events (e.g. `[music]`, `[applause]`, `[laughter]`)
- ✏️ Manual correction of transcription errors
- 🗑️ Automatic cleanup of temporary audio files
- ⚡ FastAPI backend with a Streamlit frontend

---

## Tech Stack 🛠️

**Backend:** FastAPI, Uvicorn, OpenAI Whisper, PyTorch
**Frontend:** Streamlit, Requests
**Language:** Python 3.9+

---

## Project Structure 📁

```
Basic-Speech-To-Text-Project/
│
├── SttService.py      # FastAPI backend service
├── SttUI.py            # Streamlit frontend interface
├── requirements.txt    # Python dependencies
└── README.md
```

---

## How It Works ⚙️

1. User uploads an audio file through the Streamlit interface.
2. Streamlit sends the file to the FastAPI backend.
3. FastAPI temporarily stores the uploaded audio file.
4. Whisper processes the audio and generates a full transcription and timestamped segments.
5. The backend flags possible non-speech events such as `[music]`, `[applause]`, `[laughter]`.
6. The transcription is displayed in the UI, where it can be manually corrected.
7. Temporary files are deleted after processing.

---

## Prerequisites

- Python 3.9 or higher
- `ffmpeg` installed and available on your `PATH` (required by Whisper)
- (Optional) A CUDA-capable GPU for faster transcription

---

## Installation 🚀

**1. Clone the repository**

```bash
git clone https://github.com/YaBoiAce007/Basic-Speech-To-Text-Project.git
cd Basic-Speech-To-Text-Project
```

**2. Create a virtual environment (recommended)**

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the Application ▶️

The application has two parts that need to run at the same time — use two terminals.

**1. Start the FastAPI backend**

```bash
uvicorn SttService:app --host 0.0.0.0 --port 8081
```

The API will be available at: `http://127.0.0.1:8081`

**2. Start the Streamlit frontend**

In a second terminal:

```bash
streamlit run SttUI.py
```

The Streamlit interface will open automatically in your browser at `http://localhost:8501`.

---

## Author

Aniketh Gurung