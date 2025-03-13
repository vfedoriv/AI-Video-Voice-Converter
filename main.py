import os
from extract_audio import extract_audio
from stt_whisper import stt_whisper
from tts_coqui import tts_coqui
from update_audio_track import update_audio_track
from convert_audio import convert_audio
from reduce_noise import reduce_noise
from convert_video import convert_video
from synchronize_audio import synchronize_audio
from preprocess_audio import preprocess_audio
from detect_language import detect_language

def main(video_file, output_video_file):
    try:
        # Step 1: Extract audio from the video file
        audio_file = "extracted_audio.wav"
        extract_audio(video_file, audio_file)

        # Step 2: Preprocess the audio to enhance clarity and reduce background noise
        preprocessed_audio_file = "preprocessed_audio.wav"
        preprocess_audio(audio_file, preprocessed_audio_file)

        # Step 3: Detect the language of the audio
        language = detect_language(preprocessed_audio_file)

        # Step 4: Convert the extracted audio to text using STT
        text = stt_whisper(preprocessed_audio_file)

        # Step 5: Convert the text to speech using TTS
        tts_audio_file = "tts_audio.wav"
        tts_coqui(text, tts_audio_file)

        # Step 6: Synchronize the new audio with the video
        synchronized_audio_file = "synchronized_audio.wav"
        synchronize_audio(tts_audio_file, video_file, synchronized_audio_file)

        # Step 7: Update the video file with the new audio track
        update_audio_track(video_file, synchronized_audio_file, output_video_file)

        print("Process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_file = "input_video.mp4"
    output_video_file = "output_video.mp4"
    main(video_file, output_video_file)
