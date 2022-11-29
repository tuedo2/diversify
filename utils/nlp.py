import re

import newspaper
from newspaper import Article

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

from utils.twitter import search_with_keywords

def containsURL(text):
    url_list = re.findall(r'(https?://[^\s]+)', text)
    if not url_list:
        return False
    else:
        return True


def getTitle(url):
    article = Article(url)
    article.download()
    article.parse()

    return article.title

# presumes article exists
def getTweetsFromText(text, num_results=5):
    list_of_urls = re.findall(r'(https?://[^\s]+)', text)

    url = list_of_urls[0] # i generally don't see news tweets with more than one link so just assuming here

    doc = nlp(getTitle(url))
    keywords = [ent.text for ent in doc.ents]

    data = search_with_keywords(keywords)

    if len(data) < num_results:
        num_results = len(data)

    ids = [str(data[i].id) for i in range(num_results)]
    texts = [data[i].text for i in range(num_results)]

    return ids, texts

