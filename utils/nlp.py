import re

import newspaper
from newspaper import Article
from newsapi import NewsApiClient

from collections import Counter

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
    url_list = re.findall(r'(https?://[^\s]+)', text)
    if not url_list:
        return False
    else:
        return True

def getBasicKeywords(url):
    article = Article(url)
    article.download()
    article.parse()

    keywords = article.keywords
    # keywords.append(article.title)

    return keywords

def getBasicKeywordsSpacy(url, n=10):
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
        keywords_list = getBasicKeywords(url)

        query_str = ""
        for i in range(len(keywords_list)):
            query_str += "+" + keywords_list[i]
            if i != len(keywords_list) - 1:
                query_str += " OR "

        if len(query_str) > 500:
            query_str = query_str[:500]

        top_headlines = newsapi.get_everything(q=query_str, sort_by='relevancy',
                                          language='en')

        response_list.append(top_headlines)
    return response_list

# presumes article exists
def getArticlesFromText(text, num_results=5):
    res = getArticlesUsingNLPBasicKeywords(text)
    article_list = res[0]['articles']
    if len(article_list) < num_results:
        num_results = len(article_list)

    images = [article_list[i]['urlToImage'] for i in range(num_results)]
    sources = [article_list[i]['source']['name'] for i in range(num_results)]
    titles = [article_list[i]['title'] for i in range(num_results)]
    urls = [article_list[i]['url'] for i in range(num_results)]

    return images, sources, titles, urls

