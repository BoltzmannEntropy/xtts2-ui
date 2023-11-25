# XTTS-2-UI: A User Interface for XTTS-2 Text-Based Voice Cloning

This repository contains the essential code for cloning any voice using just text and a 10-second audio sample of the target voice.

## Model 
The model used is `tts_models/multilingual/multi-dataset/xtts_v2`. For more details, refer to [Hugging Face - XTTS-v2](https://huggingface.co/coqui/XTTS-v2) and its specific version [XTTS-v2 Version 2.0.2](https://huggingface.co/coqui/XTTS-v2/tree/v2.0.2).

For information on preventing model re-downloading, please consult [Issue 4723 on GitHub](https://github.com/oobabooga/text-generation-webui/issues/4723#issuecomment-1826120220).

<h1 align="center">    
  <img src="https://github.com/BoltzmannEntropy/xtts2-ui/blob/main/resources/ui.png?raw=true" width="30%"></a>  
</h1>

Download paths:
- MacOS: `/Users/USR/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2`
- Windows: `C:\Users\ YOUR-USER-ACCOUNT \AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2`
- Linux: `/home/${USER}/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2`

## Target Voices Dataset
The dataset consists of a single folder named `targets`, pre-populated with several voices for testing purposes.

To add more voices, create a 24KHz WAV file of approximately 10 seconds and place it under the `targets` folder. 
You can use yt-dlp to download a voice from YouTube for cloning:
```
yt-dlp -x --audio-format wav "https://www.youtube.com/watch?"
```


## Setup

1. Create a Python environment using conda as per the provided instructions.
2. Activate the newly created environment: `conda activate llvc`.
3. Install `torch` and `torchaudio` from [PyTorch Official Site](https://pytorch.org/get-started/locally/).
4. Models will be downloaded automatically upon first use.

## Inference

To run the application:

```
pip install TTS==0.20.* streamlit
streamlit run app.py
```
On initial use, you will need to agree to the terms:

```
[XTTS] Loading XTTS...
 > tts_models/multilingual/multi-dataset/xtts_v2 has been updated, clearing model cache...
 > You must agree to the terms of service to use this model.
 | > Please see the terms of service at https://coqui.ai/cpml.txt
 | > "I have read, understood and agreed to the Terms and Conditions." - [y/n]
 | | >
 ```

## Examples:

English:
<audio controls>
  <source src="<audio controls>
  <source src="./outputs/Rogger-12bb0bce.wav" type="audio/wav">
  Your browser does not support the audio element.
</audio>


## Credits
Many of the modules written in `minimal_rvc/` are based on the following repositories:
- https://github.com/ddPn08/rvc-webui
- https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- https://github.com/teftef6220/Voice_Separation_and_Selection
