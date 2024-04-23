import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import shutil
from tempfile import NamedTemporaryFile

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') 

genai.configure(api_key=GOOGLE_API_KEY)

def process_audio(system_prompt, audio_file_path):
    your_file = genai.upload_file(path=audio_file_path)
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([system_prompt, your_file])
    print(response.text)
    return response.text

# Streamlit App Structure
st.title("Audio Prompt Processor")

system_prompt = st.text_area("Enter your system prompt:", height=100)  # Multi-line input
audio_file = st.file_uploader("Upload an audio file:")

if system_prompt and audio_file and st.button("Submit"):
    # Save the uploaded file locally
    # Save the uploaded file
    os.makedirs("audiofiles", exist_ok=True)

    # Determine the save path of the file
    filename = audio_file.name
    save_path = os.path.join("audiofiles", filename)

    # Save the uploaded file
    with open(save_path, "wb") as f:
        f.write(audio_file.getvalue()) 


    # # Process the audio using the saved path
    output_text = process_audio(system_prompt, save_path)
    st.markdown(output_text) 

    # # Clean up the temporary file
    os.remove(save_path)