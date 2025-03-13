from langdetect import detect

def detect_language(audio_file):
    try:
        # Load the audio file and convert it to text using STT
        text = stt_whisper(audio_file)
        
        # Detect the language of the text
        language = detect(text)
        
        return language
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
