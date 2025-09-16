import requests
import os
from dotenv import load_dotenv
import random
import re

load_dotenv()

BIBLE_ID = {
  'en': '9879dbb7cfe39e4d-01',
  'fr': 'a93a92589195411f-01',
  'es': '6b7f504f1b6050c1-01',
} # bible id base on the language selected


class Bible:
  """Object bible to call the Bible-API"""
  def __init__(self, language_code='en'):
    self.header = {'api-key': os.getenv("BIBLE_API_KEY")}
    self.url = f'https://api.scripture.api.bible/v1/bibles/{BIBLE_ID[language_code]}'
    self.message = ""

  def verse_of_the_day(self):
    """ Returns a random verse """

    try:
      # ToDo-1: Get a random book
      books = requests.get(url=f'{self.url}/books', headers=self.header).json()
      random_book_id = random.choice(books['data'])['id']
      
      # ToDo-2: Get a random chapter
      chapters = requests.get(url=f'{self.url}/books/{random_book_id}/chapters', headers=self.header).json()
      random_chapter_id = random.choice(chapters['data'])['id']

      # ToDo-3: Get a random verse
      verses = requests.get(url=f'{self.url}/chapters/{random_chapter_id}/verses', headers=self.header).json()
      random_verse_id = random.choice(verses['data'])['id']

      # ToDo-4: Get random verse content
      random_verse = requests.get(url=f'{self.url}/verses/{random_verse_id}', headers=self.header).json()
      content = random_verse['data']['content']
      reference = random_verse['data']['reference']
      
      return reference, self.clean_text(content)

    except Exception as e:
      self.message = f"Something went wrong during the request: {e}"
      return []


  def search(self, query):
    """
    Returns a searched verse

    query(str): The query of search
    """
    parameters = {
      'query': query
    }

    try:
      response = requests.get(url=f'{self.url}/search', headers=self.header, params=parameters)

      if response.status_code == 200:
        data = response.json()['data']
        results = []

        # first case: passages
        if "passages" in data and data["passages"]:
          for passage in data["passages"]:
              results.append({
                  "ref": passage.get("reference"),
                  "text": self.clean_text(passage.get("content"))
              })
              

        # second case: verses
        if "verses" in data and data["verses"]:
          for item in data["verses"]:
              results.append({
                  "ref": item.get("reference"),
                  "text": item.get("text")
              })

        if results:
            return results
        else:
            self.message = f"No results found for '{query}'"
            return []

      else:
        self.message = f"API error: {response.status_code}"
        return results

    except Exception as e:
      self.message = f"Something went wrong during the request: {e}"
    
  def clean_text(self, text):
      """ Cleans and returns a text without html characters """
      clean = re.sub(r'<span.*?>\d+</span>', '', text)
      clean = re.sub(r'</?p.*?>', '', clean).strip()
      return clean