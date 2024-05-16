import streamlit as st
from pydub import AudioSegment
import tempfile
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

# Configure Google API for audio summarization
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def summarize_audio(audio_file_path):
    """Summarize the audio using Google's Generative API."""
    
    # Initialize the GenerativeModel with the specified model
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    
    # Upload the audio file and get a reference to it
    audio_file = genai.upload_file(path=audio_file_path)
    
    # Generate the summary of the audio file using the model
    # The model is given a prompt ("Please summarize the following audio.") and the audio file
    response = model.generate_content(
        [
            "Please summarize the following audio.",
            audio_file
        ]
    )
    
    # Return the text of the generated summary
    return response.text

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    
    try:
        # Create a temporary file with the same extension as the uploaded file
        # The 'delete=False' argument ensures the file is not deleted when closed
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            
            # Write the contents of the uploaded file to the temporary file
            tmp_file.write(uploaded_file.getvalue())
            
            # Return the path of the temporary file
            return tmp_file.name
            
    except Exception as e:
        # If an error occurs, display an error message in the Streamlit app
        st.error(f"Error handling uploaded file: {e}")
        
        # Return None to indicate that the file could not be saved
        return None


# Streamlit app interface
st.title('Audio Summarization App')

with st.expander("About this app"):
    st.write("""
        This app uses Google's generative AI to summarize audio files. 
        Upload your audio file in WAV or MP3 format and get a concise summary of its content.
    """)

audio_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3'])
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)  # Save the uploaded file and get the path
    st.audio(audio_path)

    if st.button('Summarize Audio'):
        with st.spinner('Summarizing...'):
            summary_text = summarize_audio(audio_path)
            st.info(summary_text)
