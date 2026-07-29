from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import shutil
from fastapi.middleware.cors import CORSMiddleware
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pyttsx3

app = FastAPI()

TTS_OUTPUT_PATH = "audio.wav"

@app.post("/tts")
async def text_to_speech(text: str):
    try:
        engine = pyttsx3.init()

        # Optional tuning
        engine.setProperty('rate', 170)   # speed
        engine.setProperty('volume', 1.0)

        # Save to fixed file
        engine.save_to_file(text, TTS_OUTPUT_PATH)
        engine.runAndWait()

        return {
            "message": "Audio generated",
            "file_path": TTS_OUTPUT_PATH
        }

    except Exception as e:
        return {"error": str(e)}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
model = whisper.load_model("base")


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name

    try:

        # Load audio
        y, sr = librosa.load(temp_path, sr=None)

        # ---- Waveform ----
        plt.figure()
        librosa.display.waveshow(y, sr=sr)
        plt.title("Waveform")

        wave_buf = BytesIO()
        plt.savefig(wave_buf, format="png")
        wave_buf.seek(0)
        wave_img = base64.b64encode(wave_buf.read()).decode("utf-8")
        plt.close()


        # ---- Log-Mel Spectrogram ----
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        log_S = librosa.power_to_db(S, ref=np.max)

        plt.figure()
        librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
        plt.title("Log-Mel Spectrogram")

        spec_buf = BytesIO()
        plt.savefig(spec_buf, format="png")
        spec_buf.seek(0)
        spec_img = base64.b64encode(spec_buf.read()).decode("utf-8")
        plt.close()

        # Whisper transcription
        result = model.transcribe(
            temp_path,
            fp16=False
        )

        segments = []

        for segment in result["segments"]:

            text = segment["text"].strip()

            # Detect possible non-speech events
            is_sound = (
                text.startswith("[")
                and text.endswith("]")
            )

            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": text,
                "type": "sound" if is_sound else "speech"
            })


        return {
                    "full_text": result["text"],
                    "segments": segments,
                    "waveform": wave_img,
                    "spectrogram": spec_img
                }


    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)