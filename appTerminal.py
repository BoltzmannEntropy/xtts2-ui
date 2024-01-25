import json
from pathlib import Path
from app import gen_voice, tts, update_speakers, languages

def generate_voices_from_file(file_path):
    # Load the texts from the JSON file
    with open(file_path, 'r') as f:
        texts = json.load(f)

    # Get the list of speakers
    speakers = update_speakers()

    # For each text, generate a voice for each speaker
    for text in texts:
        for speaker in speakers:
            gen_voice(text, speaker, speed=0.8, english="English")

if __name__ == "__main__":
    generate_voices_from_file(Path('texts.json'))