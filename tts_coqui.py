import os
from pydub import AudioSegment
from TTS.api import TTS
from fit_audio import fit_audio_to_duration

def tts_coqui(extracted_text, timestamps, output_audio_file):
    print("Text to speach conversion started...")
    try:
        model = (TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to("cuda"))
        # model = (TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to("cuda"))
        segment_files = []
        for segment in timestamps:
            start_time = segment["start"] * 1000  # Convert seconds to milliseconds
            end_time = segment["end"] * 1000  # Convert seconds to milliseconds
            text = segment["text"]
            # Generate speech for each segment
            segment_audio_file = f"{output_audio_file}_{start_time}_{end_time}.wav"
            model.tts_to_file(text=text, file_path=segment_audio_file)

            # Fit the generated audio to the specified duration
            adjusted_audio = fit_audio_to_duration(segment_audio_file, start_time, end_time)
            adjusted_audio.export(segment_audio_file, format="wav")  # Overwrite the file
            segment_files.append(segment_audio_file)

        # Concatenate the generated audio segments
        concatenate_audio_segments(segment_files, output_audio_file)
        print("Text to speach conversion completed successfully.")
    except Exception as e:
        print(f"An error occurred in tts_coqui: {e}")

def concatenate_audio_segments(segment_files, output_audio_file):
    combined = AudioSegment.empty()
    for segment_file in segment_files:
        segment = AudioSegment.from_file(segment_file)
        combined += segment
    combined.export(output_audio_file, format="wav")
    # Delete the segment files
    #for segment_file in segment_files:
    #    os.remove(segment_file)