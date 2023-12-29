# app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins= ["masonacevedo.com", "https://masonacevedo.com"])
@app.route('/')
def hello():
    return flask.jsonify(prediction = ("bird"), probability = (0.69))