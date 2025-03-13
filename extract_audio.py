from moviepy.editor import VideoFileClip

def extract_audio(video_file, output_audio_file):
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(output_audio_file)
    except Exception as e:
        print(f"An error occurred: {e}")
