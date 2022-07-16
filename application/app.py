import sys
import os
from flask import Flask, request, redirect, url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
import pickle
import sklearn
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path += [PARENTDIR,]
# print(sys.path)
from model import postprocess, preprocess


UPLOAD_FOLDER = "user_loaded_content"
MYDIR = os.path.dirname(__file__)
MODEL = os.path.join(PARENTDIR,"model/model.pkl")
app = Flask(__name__)
print(app.static_url_path)
app.static_url_path = PARENTDIR+"/static"
print(app.static_url_path)
app.config["UPLOAD_FOLDER"] = MYDIR + "/user_loaded_content"

@app.route("/")
def index():
    return render_template("hello.html")
@app.route("/" , methods=['GET', 'POST'])
def upload_file():
    f= request.files.get("file1")
    uploaded_audio = app.config["UPLOAD_FOLDER"]+"/temp"
    f.save(uploaded_audio)
    rendered_image_relative_path = run_file_in_trained_model(uploaded_audio)
    rendered_image_absolute_path = os.path.join(PARENTDIR , rendered_image_relative_path)

    return render_template("process.html", image = rendered_image_absolute_path)

def run_file_in_trained_model(uploaded_audio_path):
    loaded_model = pickle.load(open(MODEL, 'rb'))
    audio, sr = preprocess.loadaudio(uploaded_audio_path)
    audio_list = []
    audio_list.append(audio)
    audio_list_resized = preprocess.resizeaudio(audio_list,False)
    output = loaded_model.predict(audio_list_resized)
    return postprocess.show_predicted_image(output)

