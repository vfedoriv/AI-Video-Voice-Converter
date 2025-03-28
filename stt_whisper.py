import whisper


def stt_whisper(audio_file):
    print("Speach to text conversion started...")
    try:
        model = whisper.load_model("small.en")
        result = model.transcribe(audio=audio_file, word_timestamps=True)
        print("Speach to text conversion completed successfully.")
        return result["text"], result["segments"]
    except Exception as e:
        print(f"An error occurred in stt_whisper: {e}")
        return None, None
