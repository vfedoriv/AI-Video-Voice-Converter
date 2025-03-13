import whisper
import os
import json

def train_stt_model(dataset_path, model_save_path):
    try:
        # Load the pre-trained Whisper model
        model = whisper.load_model("base")

        # Prepare the dataset
        audio_files = []
        transcriptions = []
        for root, _, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".wav"):
                    audio_files.append(os.path.join(root, file))
                    transcription_file = os.path.join(root, file.replace(".wav", ".json"))
                    with open(transcription_file, "r") as f:
                        transcriptions.append(json.load(f)["text"])

        # Train the model with the dataset
        model.train(audio_files, transcriptions)

        # Save the trained model
        model.save(model_save_path)
    except Exception as e:
        print(f"An error occurred: {e}")
