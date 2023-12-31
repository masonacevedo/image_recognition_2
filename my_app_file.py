# app.py
import flask
from flask import Flask
from flask_cors import CORS
from flask import request
from PIL import Image
from fastai.vision.all import *
import pathlib

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
        
        results_dict = classifyImage(web_image_plugin_obj)
        response = flask.jsonify(results_dict)
        return response
    
    elif request.method == "GET":
        response_dict = {"GET request": 11.0}
        response = flask.jsonify(response_dict)
        return response
    else:
        raise Exception("It should be impossible to get here!")

def classifyImage(web_image_plugin_obj):
    fastai_image = PILImage.create(web_image_plugin_obj)
    resized_image = Resize(192, method = 'squish')(fastai_image)
    mean = [0.4771, 0.4596, 0.4162]
    stddev = [0.2288, 0.2205, 0.2198]

    normalized_resized_image = Normalize.from_stats(mean, stddev)(resized_image)
    print("Got to the model loading part...")
    # fast_ai_model_with_normalization_with_architecture.pkl
    
    
    posix_backup = pathlib.PosixPath
    try:
        pathlib.PosixPath = pathlib.WindowsPath
        model_path = pathlib.Path("fast_ai_model_with_normalization_with_architecture.pkl")
    
        model = load_learner(model_path)
    finally:
        pathlib.PosixPath = posix_backup



    prediction = model.predict(normalized_resized_image)
    print("prediction[0]:", prediction[0])
    print("prediction[2].max():", prediction[2].max())
    return {"prediction": prediction[0], "probability": float(prediction[2].max())}

# if __name__ == "__main__":
#     app.run(debug= True)