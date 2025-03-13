from moviepy.editor import VideoFileClip, AudioFileClip

def update_audio_track(video_file, new_audio_file, output_video_file):
    try:
        video = VideoFileClip(video_file)
        new_audio = AudioFileClip(new_audio_file)
        video = video.set_audio(new_audio)
        video.write_videofile(output_video_file)
    except Exception as e:
        print(f"An error occurred: {e}")
