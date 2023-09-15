import os
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

ACCOUNTNAME = 'moxusa512@gmail.com'
SERVICE_ACCOUNT_FILE = '/home/denis/Documents/pushit-325000-e72447d8f2a9.json'  # Adjusted path

def text_to_speech(text):
    # Set up Google Cloud credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE

    # Initialize a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-G",  # This line sets the specific voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    # Play the audio
    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)


if __name__ == "__main__":
    import sys

    text = sys.argv[1]
    text = text.replace("▶", "  ")
    text = text.replace("▹", "  ")
    text_to_speech(text)