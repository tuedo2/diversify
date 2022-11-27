import re

import newspaper
from newspaper import Article
from newsapi import NewsApiClient

import spacy
import en_core_web_sm

news_ids = {
    'axios': ['axios'],
    'bbc': ['bbc-news', 'bbc-sport'],
    'csmonitor': [],
    'Forbes': [],
    'MarketWatch': [],
    'NewsNation': [],
    'Newsweek': ['newsweek'],
    'RealClearNews': [],
    'Reuters': ['reuters'],
    'TheHill': ['the-hill'],
    'WSJ': ['the-wall-street-journal']
}


NEWS_API_KEY = '52653260d37b4c7d9efd3731ac9156e3'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def containsURL(text):
    # TODO
    return False

# presumes article exists
def getArticlesFromText(text):
    pass # should return a list of some sort

def getBasicKeywordsSpacy(n,url):
    # Access the HTML of the url and scrape the data we need
    article = Article(url)
    article.download()
    article.parse()

    # SpaCy named entity recognition
    SP_nlp = en_core_web_sm.load()
    spacy_labels = SP_nlp(article.text)

    # return spacy_labels.ents
    items = [x.text for x in spacy_labels.ents]
    most_common = Counter(items).most_common(n)

    # formatting
    string = ""
    for word, n in most_common:
        string = string + '"' + word + '" OR '

    return string

def getArticlesUsingNLPBasicKeywords(tweet_txt):
    list_of_urls = re.findall(r'(https?://[^\s]+)', tweet_txt)
    response_list = []
    for url in list_of_urls:
        keywords_list = getBasicKeywordsSpacy(url)

        query_str = ""
        for i in range(len(keywords_list)):
            query_str += "+" + keywords_list[i]
            if i != len(keywords_list) - 1:
                query_str += " OR "

        top_headlines = newsapi.get_everything(q=query_str[0:len(query_str) - 1], sort_by='relevancy',
                                          language='en')

        response_list.append(top_headlines)
    return response_list
