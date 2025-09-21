from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play # Can also play the audio - follow Elevenlabs Doc
import os
import tempfile

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

      # Create a temp file
      temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
      with open(temp_file.name, "wb") as f:
        for chunk in self.audio:   # iterate generator
            f.write(chunk)

      return temp_file.name

