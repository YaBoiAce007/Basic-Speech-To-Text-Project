import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")


st.title("Speech To Text App")


# Persistent variables across Streamlit reruns
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "corrected_text" not in st.session_state:
    st.session_state.corrected_text = ""


uploaded_file = st.file_uploader(
    "Upload audio file",
    type=["wav", "mp3", "m4a"]
)


if uploaded_file:

    st.audio(uploaded_file)


    if st.button("Transcribe"):

        try:

            response = requests.post(
                f"{API_URL}/transcribe",
                files={
                    "file": uploaded_file
                }
            )

            response.raise_for_status()

            result = response.json()


            final_text = ""

            st.subheader("Timestamped Transcript")


            for segment in result["segments"]:

                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                type = segment["type"]


                if type == "sound":
                    st.warning(
                        f"[{start:.2f}s - {end:.2f}s] {text}"
                    )

                else:
                    st.write(
                        f"[{start:.2f}s - {end:.2f}s] {text}"
                    )


                final_text += text + " "


            # Save transcript permanently for this session
            st.session_state.transcript = final_text
            st.session_state.corrected_text = final_text


        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# Display transcript if available
if st.session_state.transcript:

    st.subheader("Manual Correction")


    st.session_state.corrected_text = st.text_area(
        "Edit transcription errors:",
        value=st.session_state.corrected_text,
        height=200
    )


    if st.button("Save Correction"):

        st.success(
            "Corrected transcription saved!"
        )

        st.write(st.session_state.corrected_text)