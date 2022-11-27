from flask import Flask, request, render_template
from flask_cors import CORS
import json

import utils.tweepy as utp
import utils.nlp as nlp

app = Flask(__name__)

CORS(app)



@app.route('/')
def hello_world():
    return 'Hello, World!' # This does nothing but I don't wanna delete it lmfao

@app.route('/tweets', methods=['POST'])
def tweets_handler(): # function is called on 'Diversify' click
    input_data = json.loads(request.data)

    print('POST /tweets')
    print('Input:', input_data)

    url = input_data['url'] # the url of the current page, sent from popup.js

    # lines 27-35 basically identify wheather the current url is a tweet or not and give the text of the tweet
    # essentially a proof of concept that the extension can interact with Flask server and identify a tweet visited

    articles = []
    error = ''
    if utp.is_twitter_status(url):
        tweet_id = utp.get_tweet_id_from_url(url)
        text = utp.get_text_from_tweet_id(tweet_id)

        if nlp.containsURL(text):
            articles = nlp.getArticles(text)
        else:
            error = 'tweet contains no article'
    else:
        error = 'not a tweet status'

    output_data = { 'articles': articles, 'error': error}

    # TODO: Replace the above code with stuff that will recommend other news sources.
    # Please try to put the code away into a utils file, I don't want this app.py file to be very long for readability

    print("Output:", output_data)

    return output_data

@app.route('/sources', methods=['POST'])
def sources_handler():
    input_data = json.loads(request.data)

    print('POST /sources')
    print('Input:', input_data)

    username = input_data['username']

    output = utp.get_source_scores(username)

    # TODO: Actually generate the recommendations
    # Tue already has written this code on his computer at his apartment, he will add it once he moves back in!

    output_data = {'sources': output}

    print("Output:", output_data)

    return output_data


app.run(host='localhost',port=8000) # It's important that the parameters are exactly like this because of popup.js
