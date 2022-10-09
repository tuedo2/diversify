from flask import Flask, request
from flask_cors import CORS

import tweepy

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALmvfQEAAAAAmOqOxjkagp35nYD4oL7QpsXxWUg%3DY7ZsHb7K7Wyi1VZT7yf29wfSVfrpesCqXbtBsUC0jA8Z8ZhzXu'


app = Flask(__name__)
CORS(app)

client = tweepy.Client(BEARER_TOKEN)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tweets", methods = ["POST"])
def tweet_handler():

    input_data = request.json

    print("=== New request to /tweets ===")
    print("Input Data:", input_data)
    print()

    tweetURL = input_data["tweetURL"]

    tweet_author = '@' + (tweetURL.split('/status/')[0]).split('/')[-1]
    tweet_id = tweetURL.split('/status/')[1]
    tweet_request = client.get_tweet(tweet_id)

    tweet_text = tweet_request.data.text
    output_data = { "tweet_author": tweet_author, "tweet_text": tweet_text }

    print("Output Data:", output_data)
    print()

    return output_data



app.run(host="0.0.0.0", port=8000)
