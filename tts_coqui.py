import os
from pydub import AudioSegment
from TTS.api import TTS
from fit_audio import fit_audio_to_duration
from fit_audio2 import fit_audio_to_duration2

def tts_coqui(extracted_text, timestamps, output_audio_file):
    print("Text to speech conversion started...")
    try:
        # Initialize the TTS model
        # model = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to("cuda")
        # model = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True).to("cuda")
        model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to("cuda")
        
        # Get the list of available speakers
        available_speakers = model.speakers
        print(f"Available speakers: {available_speakers}")

        # Choose a speaker (e.g., the first one)
        if available_speakers:
            speaker = available_speakers[0]  # Replace with your desired speaker

        # Determine the total duration of the final audio
        total_duration = max(int(segment["end"] * 1000) for segment in timestamps)  # Convert seconds to milliseconds
        combined_audio = AudioSegment.silent(duration=total_duration)  # Start with a silent audio segment

        for segment in timestamps:
            start_time = int(segment["start"] * 1000)  # Convert seconds to milliseconds and ensure it's an integer
            end_time = int(segment["end"] * 1000)  # Convert seconds to milliseconds and ensure it's an integer
            text = segment["text"]
            print(f"Processing segment: (start: {start_time} ms, end: {end_time} ms, duration: {end_time - start_time} ms) - Text: {text}")

            # Generate speech for the segment
            segment_audio_file = f"{output_audio_file}_temp.wav"  # Temporary file for TTS output
            if available_speakers:
                model.tts_to_file(text=text, file_path=segment_audio_file, speaker=speaker)
            else:
                model.tts_to_file(text=text, file_path=segment_audio_file, split_sentences=False)

            # Fit the generated audio to the specified duration
            adjusted_audio = fit_audio_to_duration2(segment_audio_file, start_time, end_time)

            print(f"Adjusted audio Start time: {start_time} ms, Real End time: {start_time + len(adjusted_audio)} ms, duration: {len(adjusted_audio)} ms")
            print("====================================================")

            # Overlay the adjusted audio at the specified start time
            combined_audio = combined_audio.overlay(adjusted_audio, position=start_time)

            # Remove the temporary file
            os.remove(segment_audio_file)

        # Export the final combined audio
        combined_audio.export(output_audio_file, format="wav")
        print("Text to speech conversion completed successfully.")
    except Exception as e:
        print(f"An error occurred in tts_coqui: {e}")