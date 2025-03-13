import tts

def tts_coqui(text, output_audio_file):
    try:
        model = tts.TTS.load_model("tts_models/en/ljspeech/tacotron2-DDC")
        audio = model.tts(text)
        model.save_wav(audio, output_audio_file)
    except Exception as e:
        print(f"An error occurred: {e}")
