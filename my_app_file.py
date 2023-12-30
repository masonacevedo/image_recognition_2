# app.py
import flask
from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, origins= ["masonacevedo.com", "https://masonacevedo.com", "https://www.masonacevedo.com", "www.masonacevedo.com"])
# CORS(app)
@app.route('/', methods = ["GET", "POST", "OPTIONS"])
def hello():
    print("request_method:", request.method)
    response = flask.jsonify(prediction = ("bird"), probability = (0.69))
    return response