import whisper
import jiwer
import os

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def calculate_wer(reference, hypothesis):
    wer = jiwer.wer(reference, hypothesis)
    return wer

def test_stt_accuracy(test_audio_dir, reference_transcriptions):
    total_wer = 0
    num_files = len(reference_transcriptions)

    for audio_file, reference in reference_transcriptions.items():
        audio_path = os.path.join(test_audio_dir, audio_file)
        hypothesis = transcribe_audio(audio_path)
        wer = calculate_wer(reference, hypothesis)
        total_wer += wer
        print(f"WER for {audio_file}: {wer}")

    average_wer = total_wer / num_files
    print(f"Average WER: {average_wer}")

if __name__ == "__main__":
    test_audio_dir = "test_audio"
    reference_transcriptions = {
        "test1.wav": "This is a test transcription.",
        "test2.wav": "Another test transcription.",
    }
    test_stt_accuracy(test_audio_dir, reference_transcriptions)
