
import flask
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return 'Hello world - it is me Jam'

app.run(host = "0.0.0.0", port = 81, debug = True)