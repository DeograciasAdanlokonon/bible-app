from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play # Can also play the audio - follow Elevenlabs Doc
import pyttsx3
import os
import tempfile

load_dotenv()


class SpeechPyttsx:
   """ Text-To-Speech using Pyttsx3 """
   def __init__(self):
    self.engine = pyttsx3.init()

   def save_to_file(self, text): 
      """Generate audio and save to a temp .mp3 file"""
      temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
      self.engine.save_to_file(text, temp_file.name)
      self.engine.runAndWait()
      return temp_file.name


class SpeechElevenLabs:
    """Text-To-Speech using ElevenLabs (free API-KEY only on local dev)"""
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

    def save_to_file(self):
      """Saves the converted text_to_speech audio"""

      # Create a temp file
      temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
      with open(temp_file.name, "wb") as f:
        for chunk in self.audio:   # iterate generator
            f.write(chunk)

      return temp_file.name

