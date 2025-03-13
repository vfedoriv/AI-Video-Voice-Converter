from pydub import AudioSegment
import noisereduce as nr

def reduce_noise(input_audio_file, output_audio_file):
    try:
        audio = AudioSegment.from_file(input_audio_file)
        samples = audio.get_array_of_samples()
        reduced_noise_samples = nr.reduce_noise(y=samples, sr=audio.frame_rate)
        reduced_noise_audio = audio._spawn(reduced_noise_samples)
        reduced_noise_audio.export(output_audio_file, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")
