from flask import Flask, request, render_template
from flask_cors import CORS
import json

import utils.tweepy as utp


app = Flask(__name__)

CORS(app)



@app.route("/")
def hello_world():
    return 'Hello, World!'

@app.route("/tweets", methods=["POST"])
def tweets_handler():
    input_data = json.loads(request.data)

    print('data', input_data)

    print("POST /tweets")
    print("Input:", input_data)

    text = input_data["text"] # the url of the current page

    # code that gets the tweet id, text and author from the url

    output_data = {"text": text}

    print("Output:", output_data)

    return output_data


app.run(host="localhost",port=8000)
