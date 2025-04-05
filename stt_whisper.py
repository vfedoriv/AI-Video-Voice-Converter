import whisper
import re


def stt_whisper(audio_file):
    print("Speach to text conversion started...")
    try:
        model = whisper.load_model("small.en")
        result = model.transcribe(audio=audio_file, 
                                 word_timestamps=True)
        
        # Post-process segments to ensure sentence-level segmentation
        segments = result["segments"]
        sentence_segments = merge_segments_to_sentences(segments)

        print("Speach to text conversion completed successfully.")
        return result["text"], sentence_segments
    except Exception as e:
        print(f"An error occurred in stt_whisper: {e}")
        return None, None

def merge_segments_to_sentences(segments):
    """
    Merge Whisper segments to ensure each segment contains a full sentence.
    Handles cases where a segment contains multiple sentences and adjusts start and end times proportionally.
    """
    merged_segments = []
    sentence_endings = re.compile(r"(?<=[.!?])\s+")  # Regex to split text into sentences
    buffer = ""  # Buffer to hold incomplete sentences
    buffer_start = None  # Start time of the buffered text

    for segment in segments:
        text = segment["text"].strip()
        start = segment["start"]
        end = segment["end"]

        # Prepend any buffered text to the current segment
        if buffer:
            text = buffer + " " + text
            start = buffer_start
            buffer = ""
            buffer_start = None

        # Split the text into sentences
        sentences = sentence_endings.split(text)
        total_chars = sum(len(sentence.strip()) for sentence in sentences if sentence.strip())

        # If the last sentence is incomplete, buffer it for the next segment
        if not text.strip().endswith((".", "?", "!")):
            buffer = sentences.pop().strip()
            buffer_start = start + (len(text) - len(buffer)) / len(text) * (end - start)

        # Calculate proportional timing for each sentence
        sentence_start = start
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Calculate the proportional duration for this sentence
            sentence_chars = len(sentence)
            sentence_duration = (sentence_chars / total_chars) * (end - start)

            # Set the end time for the current sentence
            sentence_end = sentence_start + sentence_duration

            # Create a new segment for the sentence
            merged_segments.append({
                "start": sentence_start,
                "end": sentence_end,
                "text": sentence
            })

            # Update the start time for the next sentence
            sentence_start = sentence_end

    # If there's any remaining buffered text, add it as a final segment
    if buffer:
        merged_segments.append({
            "start": buffer_start,
            "end": segments[-1]["end"],
            "text": buffer
        })

    return merged_segments