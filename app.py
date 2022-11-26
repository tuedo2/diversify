from flask import Flask, request, render_template
from flask_cors import CORS
import json

import utils.tweepy as utp


app = Flask(__name__)

CORS(app)



@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tweets', methods=['POST'])
def tweets_handler():
    input_data = json.loads(request.data)

    print('POST /tweets')
    print('Input:', input_data)

    url = input_data['url'] # the url of the current page

    output = ''
    if utp.is_twitter_status(url):
        output = utp.get_tweet_id_from_url(url)
    else:
        output = 'deez nuts'

    output_data = {'text': output}

    print("Output:", output_data)

    return output_data

@app.route('/sources', methods=['POST'])
def sources_handler():
    input_data = json.loads(request.data)

    print('POST /sources')
    print('Input:', input_data)

    username = input_data['username']

    output = utp.get_source_scores(username)

    output_data = {'sources': output}

    print("Output:", output_data)

    return output_data


app.run(host='localhost',port=8000)
