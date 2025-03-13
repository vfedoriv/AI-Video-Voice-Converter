import tts
import os
import numpy as np
import soundfile as sf

def generate_audio(text, output_audio_file):
    model = tts.TTS.load_model("tts_models/en/ljspeech/tacotron2-DDC")
    audio = model.tts(text)
    model.save_wav(audio, output_audio_file)

def calculate_mos(reference_audio_file, generated_audio_file):
    ref_audio, ref_sr = sf.read(reference_audio_file)
    gen_audio, gen_sr = sf.read(generated_audio_file)

    if ref_sr != gen_sr:
        raise ValueError("Sample rates of reference and generated audio do not match")

    ref_audio = ref_audio[:min(len(ref_audio), len(gen_audio))]
    gen_audio = gen_audio[:min(len(ref_audio), len(gen_audio))]

    mse = np.mean((ref_audio - gen_audio) ** 2)
    mos = 10 * np.log10(1 / mse)
    return mos

def test_tts_accuracy(test_text_dir, reference_audio_dir):
    total_mos = 0
    num_files = len(os.listdir(test_text_dir))

    for text_file in os.listdir(test_text_dir):
        text_path = os.path.join(test_text_dir, text_file)
        with open(text_path, "r") as f:
            text = f.read()

        output_audio_file = os.path.join(reference_audio_dir, f"{os.path.splitext(text_file)[0]}_generated.wav")
        generate_audio(text, output_audio_file)

        reference_audio_file = os.path.join(reference_audio_dir, f"{os.path.splitext(text_file)[0]}.wav")
        mos = calculate_mos(reference_audio_file, output_audio_file)
        total_mos += mos
        print(f"MOS for {text_file}: {mos}")

    average_mos = total_mos / num_files
    print(f"Average MOS: {average_mos}")

if __name__ == "__main__":
    test_text_dir = "test_text"
    reference_audio_dir = "reference_audio"
    test_tts_accuracy(test_text_dir, reference_audio_dir)
