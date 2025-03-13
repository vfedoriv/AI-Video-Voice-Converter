from pydub import AudioSegment
import noisereduce as nr

def preprocess_audio(input_audio_file, output_audio_file):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(input_audio_file)
        
        # Apply noise reduction
        samples = audio.get_array_of_samples()
        reduced_noise_samples = nr.reduce_noise(y=samples, sr=audio.frame_rate)
        reduced_noise_audio = audio._spawn(reduced_noise_samples)
        
        # Export the preprocessed audio file
        reduced_noise_audio.export(output_audio_file, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")
