from TTS.api import TTS

def tts_coqui(extracted_text, output_audio_file):
    try:
        model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC").to("cuda")
        model.tts_to_file(text = extracted_text, file_path = output_audio_file)
    except Exception as e:
        print(f"An error occurred in tts_coqui: {e}")

#print(TTS.list_models())
#tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to("cuda")
#print(tts)

