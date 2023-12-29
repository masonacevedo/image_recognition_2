# app.py
import flask
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, 
     origins= ["masonacevedo.com", "https://masonacevedo.com", "https://www.masonacevedo.com", "www.masonacevedo.com"],
     allow_headers=["Content-Type","multipart/form-data","Authorization"],
     supports_credentials=True)
@app.route('/', methods = ["GET","POST", "OPTIONS"])
@cross_origin(origin = "*", headers = ["Content-Type", "Authorization"])
def hello():
    # if flask.request.method == "OPTIONS":
    #     return _build_cors_preflight_response()
    return flask.jsonify(prediction = ("bird"), probability = (0.69))

def _build_cors_preflight_response():
    response = flask.make_response()
    response.headers.add("Access-Control-Allow-Origin","https://www.masonacevedo.com")
    response.headers.add("Access-Control-Allow-Headers", '*')
    response.headers.add("Access-Control-Allow-Methods", '*')
    return response