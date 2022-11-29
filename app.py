from flask import Flask, request, render_template
from flask_cors import CORS
import json

import utils.twitter as utw
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

    ids, texts = [], []
    error = ''
    if utw.is_twitter_status(url):
        tweet_id = utw.get_tweet_id_from_url(url)
        text = utw.get_text_from_tweet_id(tweet_id)

        if nlp.containsURL(text):
            ids, texts = nlp.getTweetsFromText(text)
        else:
            error = 'tweet contains no article'
    else:
        error = 'not a tweet status'

    output_data = { 'ids': ids, 'texts': texts, 'error': error}

    print("Output:", output_data)

    return output_data

@app.route('/sources', methods=['POST'])
def sources_handler(): # Function is called on 'Load Recomendations' click
    input_data = json.loads(request.data)

    print('POST /sources')
    print('Input:', input_data)

    username = input_data['username']

    output = []
    error = ''
    try:
        output = utw.get_source_list(username)
    except Exception:
        error = 'Enter a valid username'

    output_data = {'sources': output, 'error': error}

    print("Output:", output_data)

    return output_data


app.run(host='localhost', port=8000) # It's important that the parameters are exactly like this because of popup.js
