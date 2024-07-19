import streamlit as st
import speech_recognition as sr
import os

def transcribe_speech(api_choice, language):
    # Initialize recognizer class
    r = sr.Recognizer()
    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")
        # Listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            if api_choice == "Google":
                # Using Google Speech Recognition
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                # Using CMU Sphinx
                text = r.recognize_sphinx(audio_text, language=language)
            elif api_choice == "Azure":
                # Using Microsoft Azure (requires additional setup)
                text = r.recognize_azure(audio_text, language=language)
            else:
                return "Unsupported API choice."
            
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

def save_transcription(text):
    if text:
        with open("transcription.txt", "w") as file:
            file.write(text)
        st.success("Transcription saved to 'transcription.txt'")

def main():
    st.title("Speech Recognition App")
    
    # API selection
    api_choice = st.selectbox(
        "Select Speech Recognition API",
        ["Google", "Sphinx", "Azure"]
    )
    
    # Language selection
    language = st.selectbox(
        "Select Language",
        ["en-US", "es-ES", "fr-FR"]  # Add more languages as needed
    )
    
    # Add a button to trigger speech recognition
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language)
        st.write("Transcription: ", text)
        save_transcription(text)
    
    # Add pause and resume functionality
    if st.button("Pause Recording"):
        st.info("Recording paused. Click 'Start Recording' to resume.")
    if st.button("Resume Recording"):
        st.info("Recording resumed.")
        
if __name__ == "__main__":
    main()
