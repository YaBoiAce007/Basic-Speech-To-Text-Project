import streamlit as st
import requests
from dotenv import load_dotenv
import os
import base64

load_dotenv()
API_URL = os.getenv("API_URL")

st.set_page_config(page_title="STT + TTS App", layout="centered")

# ------------------ HEADER ------------------
st.title("🎙️ Speech Processing App")
st.caption("Convert text ↔ speech with transcription + visualization")

st.divider()

# ------------------ TTS SECTION ------------------
with st.container():
    st.subheader("🗣️ Text to Speech")

    tts_text = st.text_area("Enter text to convert", height=120)

    col1, col2 = st.columns([1, 3])

    with col1:
        generate_btn = st.button("Generate")

    if generate_btn and tts_text.strip():

        with st.spinner("Generating audio..."):
            response = requests.post(
                f"{API_URL}/tts",
                params={"text": tts_text}
            )

        if response.status_code == 200:
            st.success("Audio generated successfully!")

            with open("audio.wav", "rb") as f:
                st.audio(f.read())

        else:
            st.error("Failed to generate audio")

st.divider()

# ------------------ SESSION STATE ------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "corrected_text" not in st.session_state:
    st.session_state.corrected_text = ""

# ------------------ FILE UPLOAD ------------------
with st.container():
    st.subheader("📂 Upload Audio")

    uploaded_file = st.file_uploader(
        "Supported formats: WAV, MP3, M4A",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file:
        st.audio(uploaded_file)

        if st.button("Transcribe Audio"):

            try:
                with st.spinner("Transcribing..."):
                    response = requests.post(
                        f"{API_URL}/transcribe",
                        files={"file": uploaded_file}
                    )

                response.raise_for_status()
                result = response.json()

                st.divider()
                st.subheader("📝 Timestamped Transcript")

                final_text = ""

                for segment in result["segments"]:
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"]
                    seg_type = segment["type"]

                    line = f"[{start:.2f}s - {end:.2f}s] {text}"

                    if seg_type == "sound":
                        st.warning(line)
                    else:
                        st.markdown(f"`{line}`")

                    final_text += text + " "

                st.session_state.transcript = final_text
                st.session_state.corrected_text = final_text

                # ------------------ VISUALS ------------------
                st.divider()
                st.subheader("📊 Audio Analysis")

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("Waveform")
                    wave_bytes = base64.b64decode(result["waveform"])
                    st.image(wave_bytes)

                with col2:
                    st.caption("Spectrogram")
                    spec_bytes = base64.b64decode(result["spectrogram"])
                    st.image(spec_bytes)

            except Exception as e:
                st.error(f"Error: {e}")

# ------------------ CORRECTION SECTION ------------------
if st.session_state.transcript:

    st.divider()
    st.subheader("✏️ Manual Correction")

    st.session_state.corrected_text = st.text_area(
        "Edit transcription:",
        value=st.session_state.corrected_text,
        height=180
    )

    if st.button("Save Correction"):
        st.success("Saved!")
        st.code(st.session_state.corrected_text, language="text")