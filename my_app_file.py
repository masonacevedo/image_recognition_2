# app.py
import flask
from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB
CORS(app, origins= ["masonacevedo.com", "https://masonacevedo.com", "https://www.masonacevedo.com", "www.masonacevedo.com"])
# CORS(app)
@app.route('/', methods = ["GET", "POST", "OPTIONS"])
def hello():
    if request.method == "POST":
        image = request.files.get("user_image")
        print("IMAGE:", image)
    response = flask.jsonify(prediction = ("bird"), probability = (0.69))
    return response