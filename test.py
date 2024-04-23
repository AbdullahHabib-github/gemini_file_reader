import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
try:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
except Exception as e:
    st.write(f"Error loading API key: {e}")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.write(f"Error configuring API: {e}")
    st.stop()

def process_audio(system_prompt, audio_file_path):
    try:
        your_file = genai.upload_file(path=audio_file_path)
    except Exception as e:
        st.write(f"Error uploading file: {e}")
        return

    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    except Exception as e:
        st.write(f"Error loading model: {e}")
        return

    try:
        response = model.generate_content([system_prompt, your_file])
    except Exception as e:
        st.write(f"Error generating content: {e}")
        return

    print(response.text)
    return response.text

# Streamlit App Structure
st.title("Audio Prompt Processor")
system_prompt = st.text_area("Enter your system prompt:", height=100)
try:
    audio_file = st.file_uploader("Upload an audio file:")
except Exception as e:
    st.write(f"Error while uploading the file: {e}")
    st.stop()
  

if system_prompt and audio_file and st.button("Submit"):
    # Save the uploaded file locally
    try:
        os.makedirs("audiofiles", exist_ok=True)
    except Exception as e:
        st.write(f"Error creating directory: {e}")
        st.stop()

    try:
        filename = audio_file.name
        save_path = os.path.join("audiofiles", filename)
        with open(save_path, "wb") as f:
            f.write(audio_file.getvalue())
    except Exception as e:
        st.write(f"Error saving file: {e}")
        st.stop()

    try:
        output_text = process_audio(system_prompt, save_path)
        st.markdown(output_text)
    except Exception as e:
        st.write(f"Error processing audio: {e}")

    try:
        os.remove(save_path)
    except Exception as e:
        st.write(f"Error removing temporary file: {e}")