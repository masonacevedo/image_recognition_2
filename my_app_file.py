# app.py
import flask
from flask import Flask
from flask_cors import CORS
from flask import request
from PIL import Image

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB
CORS(app, origins= ["masonacevedo.com", "https://masonacevedo.com", "https://www.masonacevedo.com", "www.masonacevedo.com"])
# CORS(app)

# @app.route('/', methods = ["GET", "POST", "OPTIONS"])
@app.route('/', methods = ["GET", "POST"])
def hello():
    if request.method == "POST":
        print("request.files:", request.files)
        # print("file:", file)
        image = request.files.get("user_image")
        print("image:", image,"\n\n\n\n")
        if image is None:
            return flask.jsonify(error = "No image provided! Please upload an image!"), 400
        
        web_image_plugin_obj = Image.open(image)
        web_image_plugin_obj.save("image.jpg")
        

        response_dict = {"prediction":"bird", 
                         "probability":12}
        response = flask.jsonify(response_dict)
        return response
    
    elif request.method == "GET":
        response_dict = {"GET request": 11.0}
        response = flask.jsonify(response_dict)
        return response
    else:
        raise Exception("It should be impossible to get here!")

if __name__ == "__main__":
    app.run(debug= True)