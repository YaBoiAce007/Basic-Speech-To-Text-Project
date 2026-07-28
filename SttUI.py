import streamlit as st
import requests

st.title("Speech to Text App")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Transcribe"):

        try:

            response = requests.post(
                "http://127.0.0.1:8081/transcribe",
                files={"file": uploaded_file}
            )

            # Raises exception for bad status codes (4xx, 5xx)
            response.raise_for_status()

            result = response.json()
            st.subheader("Transcription:")
            st.write(result["text"])
        
            
        except Exception as e:

            st.error(f"Something went wrong: {e}")