from moviepy import VideoFileClip

def convert_video(input_video_file, output_video_file, output_format):
    try:
        video = VideoFileClip(input_video_file)
        video.write_videofile(output_video_file, codec=output_format)
    except Exception as e:
        print(f"An error occurred: {e}")
