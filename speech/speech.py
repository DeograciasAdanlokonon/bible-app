from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play # Can also play the audio - follow Elevenlabs Doc
import os
import base64

load_dotenv()


class Speech:
    """Text-To-Speech using ElevenLabs library"""
    def __init__(self, text):
        self.text = text
        self.elevenlabs = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
        )
        self.audio = self.elevenlabs.text_to_speech.convert(
            text=self.text,
            voice_id="EXAVITQu4vr4xnSDxMaL",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

    def save_audio(self):
      """Saves the converted text_to_speech audio"""

      # Collect chunks into a single bytes object
      audio_bytes = b"".join(self.audio)
      # encode to base64
      encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

      return encoded_audio

