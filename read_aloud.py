from openai import OpenAI
from pydub.playback import play
from pydub import AudioSegment
from io import BytesIO
import sys
import subprocess
def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
def playtext (text):
    speech_file_path = "/home/denis/Documents/CVBuild/speech.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice="nova",
      input=text
    )
    response.stream_to_file(speech_file_path)
    # Play the audio

    audio = AudioSegment.from_mp3(speech_file_path)
    play(audio)

with open('openai.key','r') as key_file:
    key=key_file.read().strip()
client = OpenAI(api_key=key,)

text = sys.argv[1]

print(len(text),text)
if len(text)>4096:
    beep()
    quit(1)
playtext(text)

