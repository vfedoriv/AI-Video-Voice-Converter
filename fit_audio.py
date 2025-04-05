from pydub import AudioSegment
from pydub.playback import play

def fit_audio_to_duration(audio_file, start_time, end_time):
    """
    Fit an audio file into a specific duration by time-stretching.

    Parameters:
    - audio_file: Path to the input audio file.
    - start_time: Start time in milliseconds.
    - end_time: End time in milliseconds.

    Returns:
    - Adjusted AudioSegment object.
    """
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Calculate the target duration
    target_duration = end_time - start_time

    # Calculate the stretch factor
    original_duration = len(audio)  # Original duration in milliseconds
    
    # Check if the audio already fits within the target duration
    if original_duration <= target_duration:
        return audio  # No adjustment needed

    stretch_factor = original_duration / target_duration

    # Adjust the playback speed
    adjusted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * stretch_factor)
    }).set_frame_rate(audio.frame_rate)

    return adjusted_audio
