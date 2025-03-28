from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment

def synchronize_audio(video_file, audio_file, output_video_file):
    print("Audio synchronization started...")
    try:
        video = VideoFileClip(video_file)
        audio = AudioSegment.from_file(audio_file)

        # Calculate the duration difference
        video_duration_ms = video.duration * 1000
        audio_duration_ms = len(audio)

        if audio_duration_ms > video_duration_ms:
            # Compress audio to fit video length
            audio = audio.speedup(playback_speed=audio_duration_ms / video_duration_ms)
        elif audio_duration_ms < video_duration_ms:
            # Expand audio to fit video length
            audio = audio.set_frame_rate(int(audio.frame_rate * (video_duration_ms / audio_duration_ms)))


        # Save the synchronized audio to a temporary file
        temp_audio_file = "./data/temp_audio.wav"
        audio.export(temp_audio_file, format="wav")

        # Replace the audio track in the video with the synchronized audio
        video.audio = AudioFileClip(temp_audio_file)
        video.write_videofile(output_video_file)
        print("Audio synchronization  completed successfully.")
    except Exception as e:
        print(f"An error occurred in synchronize_audio : {e}")
