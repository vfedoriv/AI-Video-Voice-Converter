from pydub import AudioSegment

def convert_audio(input_audio_file, output_audio_file, output_format):
    try:
        audio = AudioSegment.from_file(input_audio_file)
        audio.export(output_audio_file, format=output_format)
    except Exception as e:
        print(f"An error occurred: {e}")
