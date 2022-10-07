from flask import flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"
