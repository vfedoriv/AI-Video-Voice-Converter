from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment

def synchronize_audio(video_file, audio_file, output_video_file):
    try:
        video = VideoFileClip(video_file)
        audio = AudioSegment.from_file(audio_file)

        # Ensure audio and video have the same duration
        if len(audio) > video.duration * 1000:
            audio = audio[:int(video.duration * 1000)]
        elif len(audio) < video.duration * 1000:
            silence = AudioSegment.silent(duration=(video.duration * 1000) - len(audio))
            audio = audio + silence

        # Save the synchronized audio to a temporary file
        temp_audio_file = "./data/temp_audio.wav"
        audio.export(temp_audio_file, format="wav")

        # Replace the audio track in the video with the synchronized audio
        video.audio = AudioFileClip(temp_audio_file)
        video.write_videofile(output_video_file)
    except Exception as e:
        print(f"An error occurred in synchronize_audio : {e}")
