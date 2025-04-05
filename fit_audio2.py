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
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)  # Load with the original sample rate

    # Calculate the target duration in seconds
    target_duration = end_time - start_time

    # Calculate the original duration
    original_duration = librosa.get_duration(y=y, sr=sr) * 1000.0  # Convert seconds to milliseconds

    # Check if the audio already fits within the target duration
    if ( original_duration <= (target_duration + 500) ):
        return AudioSegment.from_file(audio_file)  # No adjustment needed    

    # Time-stretch the audio to fit the target duration
    stretch_factor = original_duration / target_duration
    print(f"Original duration: {original_duration} ms, Target duration: {target_duration} ms, Stretch factor: {stretch_factor}")
    
    y_stretched = librosa.effects.time_stretch(y, rate=1/stretch_factor)

    # Save the adjusted audio to a temporary file
    temp_output_file = "temp_adjusted_audio.wav"
    sf.write(temp_output_file, y_stretched, sr)

    # Load the adjusted audio back into an AudioSegment object
    adjusted_audio = AudioSegment.from_file(temp_output_file)

    return adjusted_audio