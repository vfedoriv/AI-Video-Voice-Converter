from moviepy import VideoFileClip

def extract_audio(video_file, output_audio_file):
    print("Audio file extraction started...")
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(output_audio_file)
        print("Audio file extracted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
