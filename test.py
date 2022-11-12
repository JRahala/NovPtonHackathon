import flask
from flask import Flask

app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Jam", "Tharun", "Shlok", "Devan"]}

app.run(host = "0.0.0.0", port = 5500, debug = True)