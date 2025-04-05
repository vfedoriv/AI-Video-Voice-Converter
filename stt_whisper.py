import whisper


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
    """
    merged_segments = []
    current_segment = None

    for segment in segments:
        text = segment["text"].strip()
        start = segment["start"]
        end = segment["end"]

        # If no current segment, start a new one
        if current_segment is None:
            current_segment = {"start": start, "end": end, "text": text}
        else:
            # Check if the current segment ends with sentence-ending punctuation
            if current_segment["text"].strip().endswith((".", "?", "!")):
                # Finalize the current segment and start a new one
                merged_segments.append(current_segment)
                current_segment = {"start": start, "end": end, "text": text}
            else:
                # Merge the current segment with the new one
                current_segment["text"] += " " + text
                current_segment["end"] = end

    # Add the last segment if it exists
    if current_segment:
        merged_segments.append(current_segment)

    return merged_segments