import streamlit as st


def transcribe_audio(audio_file):
    return "hello"

def process_prompt(system_prompt, audio_transcript):
    prompt = f"System Prompt: {system_prompt}\nAudio Transcript: {audio_transcript}\nResponse:" 
    return prompt

# Streamlit App Structure
st.title("Audio Prompt Processor")

system_prompt = st.text_input("Enter your system prompt:")
audio_file = st.file_uploader("Upload an audio file:")

if system_prompt and audio_file:
    audio_transcript = transcribe_audio(audio_file)
    output_text = process_prompt(system_prompt, audio_transcript)
    st.text_area("Output", output_text) 
