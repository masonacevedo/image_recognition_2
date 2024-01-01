# app.py
import flask
from flask import Flask
from flask_cors import CORS
from flask import request
from PIL import Image
from fastai.vision.all import load_learner, Resize, Normalize, PILImage
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
        if web_image_plugin_obj.mode == "RGBA":
            web_image_plugin_obj = web_image_plugin_obj.convert('RGB')
        
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
    
    # LOAD THE MODEL THIS WAY IF YOU'RE DEPLOYING IN A LINUX SERVER!
    model_path = pathlib.Path("fast_ai_model_with_normalization_with_architecture.pkl")
    model = load_learner(model_path)

    # LOAD THE MODEL THIS WAY IF YOU'RE DEVELOPING ON A WINDOWS MACHINE INSTEAD OF A LINUX MACHINE!
    # posix_backup = pathlib.PosixPath
    # try:
    #     pathlib.PosixPath = pathlib.WindowsPath
    #     model_path = pathlib.Path("fast_ai_model_with_normalization_with_architecture.pkl")
    
    #     model = load_learner(model_path)
    # finally:
    #     pathlib.PosixPath = posix_backup



    prediction = model.predict(normalized_resized_image)
    if prediction[0] == "bird":
        return {"prediction": prediction[0], "probability": 100 * float(prediction[2].max())}
    else:
        bird_index = 2
        bird_probability = prediction[2][bird_index]
        print("bird_probability:", bird_probability)
        prob_not_bird = sum(prediction[2]) - bird_probability
        print("prob_nor_bird:", prob_not_bird)
        return {"prediction": prediction[0], "probability": 100 * float(prob_not_bird)}

# if __name__ == "__main__":
#     app.run(debug= True)