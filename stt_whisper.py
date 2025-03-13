import whisper


def stt_whisper(audio_file):
    try:
        model = whisper.load_model("small.en")
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
