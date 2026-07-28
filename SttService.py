from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import shutil
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

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
            "segments": segments
        }


    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)