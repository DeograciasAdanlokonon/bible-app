from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play # Can also play the audio - follow Elevenlabs Doc
import os
from audioplayer import AudioPlayer

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

      # Get the current directory of speech.py
      base_dir = os.path.dirname(__file__)

      try:
        # Save the audio to file
        filename = os.path.join(base_dir, "output.mp3")
        with open(filename, "wb") as f:
            f.write(audio_bytes)
      except Exception as e:
          raise (f"Error occured: {e}")

