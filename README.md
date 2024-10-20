### Motivation
After learning online, I added GUI and decided to share.

speak features:
* guess computer pick with three chances
* just speak! (rem unmute microphone, computer built-in microphone is fine)
* cli contains detailed status
* gui has main info [added] 

### Install Guide
copy and run (assume linux with python3):
```
sudo apt-get install -y portaudio19-dev 
python3 -m venv test
cd test
source bin/activate
git clone https://github.com/wendy-py/portaudio-speak.git
cd portaudio-speak
pip install SpeechRecognition PyAudio
python speak.py
```
