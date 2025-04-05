import os
import librosa
import soundfile as sf
from pydub import AudioSegment

def fit_audio_to_duration2(audio_file, start_time, end_time):
    """
    Fit an audio file into a specific duration by time-stretching using librosa.

    Parameters:
    - audio_file: Path to the input audio file.
    - start_time: Start time in milliseconds.
    - end_time: End time in milliseconds.

    Returns:
    - Adjusted AudioSegment object.
    """

    segment = AudioSegment.from_file(audio_file)

    segment_duration_ms = len(segment)  # Duration in milliseconds

    

    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)  # Load with the original sample rate
    print(f"Audio file loaded. Sample rate: {sr}, Duration: {len(y) / sr:.2f} seconds")

    # Calculate the target duration in milliseconds
    target_duration_ms = end_time - start_time  # Target duration in milliseconds

    # Calculate the original duration in milliseconds
    librosa_original_duration_ms = librosa.get_duration(y=y, sr=sr) * 1000  # Convert seconds to milliseconds
    print(f"Original duration from librosa: {librosa_original_duration_ms:.2f} ms, Segment duration: {segment_duration_ms:.2f} ms")
    if librosa_original_duration_ms > segment_duration_ms:        
        segment_duration_ms = librosa_original_duration_ms

    # Check if the audio already fits within the target duration
    if segment_duration_ms - target_duration_ms < 0:
        print(f"Audio already fits within the target duration. Original duration: {segment_duration_ms:.2f} ms, Target duration: {target_duration_ms:.2f} ms")
        return AudioSegment.from_file(audio_file)  # No adjustment needed    

    # Time-stretch the audio to fit the target duration
    rate = segment_duration_ms / target_duration_ms  # Add a small value to avoid adgusted duration be greater than expected
    # rate = 1 / stretch_factor
    print(f"Original duration: {segment_duration_ms:.2f} ms, Target duration: {target_duration_ms:.2f} ms, Rate: {rate:.4f}")
    
    y_stretched = librosa.effects.time_stretch(y, rate=rate)

    # Save the adjusted audio to a temporary file
    temp_output_file = "temp_adjusted_audio.wav"
    # os.remove(temp_output_file)
    sf.write(temp_output_file, y_stretched, sr)

    # Load the adjusted audio back into an AudioSegment object
    adjusted_audio = AudioSegment.from_file(temp_output_file)

    return adjusted_audio