
from TTS.api import TTS
import time
import json
import random
import time
from pathlib import Path
import streamlit as st
import time
import html 

import gradio as gr
import uuid
import torch 
import librosa
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from scipy.io.wavfile import write

params = {
    "activate": True,
    "autoplay": True,
    "show_text": False,
    "remove_trailing_dots": False,
    "voice": "Rogger.wav",
    "language": "English",
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
    # "model_path":"./models/",
    # "config_path":"./models/config.json"
}

SUPPORTED_FORMATS = ['wav']
SAMPLE_RATE = 16000

speakers = {p.stem: str(p) for p in list(Path('targets').iterdir())}

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# device = torch.device('cuda:0')

# device = torch.device('cuda:0')
import os 
os.makedirs(os.path.join(".", "targets"), exist_ok=True)
os.makedirs(os.path.join(".", "outputs"), exist_ok=True)

@st.cache_resource 
# @st.experimental_singleton
def load_model():
    global tts
    print("[XTTS] Loading XTTS...")
    tts = TTS(model_name=params["model_name"]).to(device)
    # model_path=params["model_path"],
    # config_path=params["config_path"]).
    return tts

tts=load_model()

def get_available_voices():
    return sorted([voice.name for voice in Path(f"{this_dir}/targets").glob("*.wav")])

def random_sentence():
    with open(Path("harvard_sentences.txt")) as f:
        return random.choice(list(f))

st.title("TTS based Voice Cloning in 16 Languages.")
# st.image('logo.png', width=150)

st.header('Text to speech generation')

this_dir = str(Path(__file__).parent.resolve())
languages=None 
with open(Path(f"{this_dir}/languages.json"), encoding='utf8') as f:
    languages = json.load(f)

with st.sidebar:
    voice_list=get_available_voices()
    print (voice_list)
    st.title("Text to Voice")
    english = st.radio(
        label="Choose your language", options=languages, index=0, horizontal=True)
   
    default_speaker_name = "Rogger"
    speaker_name = st.selectbox('Select target speaker:', options=[None] + list(speakers.keys()), 
    index=[key for key in speakers.keys()].index(default_speaker_name) + 1 if default_speaker_name in speakers else 0)

    wav_tgt=None
    if speaker_name is not None:
        wav_tgt, _ = librosa.load(speakers[speaker_name],sr=22000)
        wav_tgt, _ = librosa.effects.trim(wav_tgt, top_db=20)

        st.write('Selected Target:')
        st.audio(wav_tgt, sample_rate=22000)

    # Upload the WAV file
   
    text = st.text_area('Enter text to convert to audio format',
    value="Hello")
    speed = st.slider('Speed', 0.1, 1.99, 0.8, 0.01)
    
st.caption ("Optional Microphone Recording. Download and rename your recording before using.")
audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")  

    def gen_voice(string,spk):
        string = html.unescape(string)
        # Generate a short UUID
        short_uuid = str(uuid.uuid4())[:8]
        fl_name='outputs/' + spk + "-" + short_uuid +'.wav'
        output_file = Path(fl_name)
        tts.tts_to_file(
            text=string,
            speed=speed,
            file_path=output_file,
            speaker_wav=[f"{this_dir}/targets/" +spk + ".wav"],
            language=languages[english]
        )

        return output_file

# Upload the WAV file
st.caption ("For the audio file, use the name of your Target, for instance ABIDA.wav")
new_tgt = st.file_uploader('Upload a new TARGET audio WAV file:', type=SUPPORTED_FORMATS, accept_multiple_files=False)
if new_tgt is not None:
    # Get the original file name
    file_name = new_tgt.name

    # Save the file to the file system
    file_path = os.path.join("./targets/", file_name)
    st.info(f"Original file name: {file_name}")
    
    # Extract the file name without the extension
    file_name_without_extension = os.path.splitext(file_name)[0]

    # Use librosa to load and process the WAV file
    wav_tgt, _ = librosa.load(new_tgt, sr=22000)
    wav_tgt, _ = librosa.effects.trim(wav_tgt, top_db=20)

    # Use scipy.io.wavfile.write to save the processed WAV file
    write('./targets/' + file_name_without_extension + '.wav', 22000, wav_tgt)

    st.success(f"New target saved successfully to {file_path}")
    
if st.button('Convert'):
    # Run TTS
    st.success('Converting ... please wait ...')
    output_file=gen_voice(text, speaker_name)
    # tts.tts_to_file(text=text, speed=speed, speaker=speaker, file_path="out.wav")

    st.write(f'Target voice:'+speaker_name)
    # st.success('Converted to audio successfully')
    
    audio_file = open(output_file, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
    # st.success("You can now play the audio by clicking on the play button.")
