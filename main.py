from bible.bible import Bible
from speech.speech import Speech
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash, send_file
from flask_bootstrap import Bootstrap5
import re
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfdjfkdfk?JKK55yc5kjKo8'
Bootstrap5(app=app)

def delete_audio():
  """
  Deletes a specified existant audio
  """
  filepath = "speech/output.mp3"
  os.remove(path=filepath)


@app.route('/', methods=['GET'])
def home():
  lang = request.args.get("lang", "en")
  #initialize object bible
  bible = Bible(language_code=lang)

  verse = bible.verse_of_the_day()

  if not verse == []:
    verse_reference = verse[0]
    verse_text = verse[1]

    # ToDo: Run the speech object
    speech = Speech(text=verse_text)
    audio_path = speech.save_audio()
  else:
    flash(bible.message, "warning")

  return render_template('home.html', verse_text=verse_text, verse_ref=verse_reference, lang=lang, audio_path=audio_path)


@app.route('/search', methods=['GET'])
def search():
  lang = request.args.get("hidden_lang", "en")
  query = request.args.get("query")

  #initialize object bible
  bible = Bible(language_code=lang)
  results = bible.search(query=query)

  if results == []:
    flash(bible.message, 'warning')

  return render_template('search.html', results=results, lang=lang)

@app.route('/audio/<ref>/<text>')
def audio(ref, text):
  try:
    # ToDo: Run the speech object  
    speech = Speech(text=text)
    audio_path = speech.save_audio()
    
    return render_template('audio.html', ref=ref, text=text, audio_path=audio_path)
  except Exception as e:
    flash("Sorry, Text to Speech failed!", "warning")
    redirect(url_for('search'))

  return render_template('audio.html', )

@app.route("/play-audio/<path>")
def play_audio(path):
    """Serve the temporary audio file"""
    return send_file(path, mimetype="audio/mpeg")

if __name__ == "__main__":
  app.run(debug=True)