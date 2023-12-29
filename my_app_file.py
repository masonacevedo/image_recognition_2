# app.py
import flask
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins= ["masonacevedo.com", "https://masonacevedo.com", "https://www.masonacevedo.com"])
@app.route('/', methods = ["POST"])
def hello():
    return flask.jsonify(prediction = ("bird"), probability = (0.69))