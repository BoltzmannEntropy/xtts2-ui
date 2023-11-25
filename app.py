
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
import platform

def is_mac_os():
    return platform.system() == 'Darwin'


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

SUPPORTED_FORMATS = ['wav', 'mp3', 'flac', 'ogg']
SAMPLE_RATE = 16000

speakers = {p.stem: str(p) for p in list(Path('targets').iterdir())}

device=None
if is_mac_os():
    print("This is macOS.")
    device = torch.device('cpu')
else:
    print("This is not macOS.")
    device = torch.device('cuda:0')

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

st.title("TTS based Voice Clonning in 16 Languages.")
st.image('logo.png', width=150)

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

    text = st.text_area('Enter text to convert to audio format',value="Well, I think I am much much better than Paul, or even Lennon. But let me know what you think.")
    speed = st.slider('Speed', 0.1, 1.99, 0.8, 0.01)

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

if st.button('Convert'):
    # Run TTS
    st.success('Converting ... please wait ...')
    output_file=gen_voice(text, speaker_name)
    st.write(f'Target voice:'+speaker_name)
    # st.success('Converted to audio successfully')
    audio_file = open(output_file, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
