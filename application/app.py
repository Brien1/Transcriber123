import sys
import os
from flask import Flask, request, redirect, url_for,render_template,send_from_directory, send_file, abort
from werkzeug.utils import secure_filename
import pickle
import sklearn
import matplotlib as mpl
import matplotlib.pyplot as plt
import librosa

CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path += [PARENTDIR,]
# print(sys.path)
from model import postprocess, preprocess


UPLOAD_FOLDER = "user_loaded_content"
MYDIR = os.path.dirname(__file__)
MODEL1 = os.path.join(PARENTDIR,"model/model1.pkl")
MODEL2 = os.path.join(PARENTDIR,"model/model2.pkl")

app = Flask(__name__)
# print(app.static_url_path)
# app.static_url_path = PARENTDIR+"/static"
# print(app.static_url_path)
app.config["UPLOAD_FOLDER"] = MYDIR + "/user_loaded_content"

@app.route("/")
def index():
    return render_template("hello.html")

@app.route("/" , methods=['GET', 'POST'])
def upload_file():
    f= request.files.get("file1")
    uploaded_audio = app.config["UPLOAD_FOLDER"]+"/temp"
    f.save(uploaded_audio)
    output = run_file_in_trained_model(uploaded_audio)
    postprocess.show_predicted_image(output)
    return render_template("process.html", image = os.path.join(app.static_url_path,"new_image.png"))

def run_file_in_trained_model(uploaded_audio_path):
    """Returns base64 string.. representation of image

    Args:
        uploaded_audio_path (str): path to uploaded audio

    Returns:
        base64 string: decode for png/ jpg etc.
    """
    f1=pickle.load(open(MODEL1,"rb"))
    f2=pickle.load(open(MODEL2,"rb"))
    model_byte_string = f1+ f2
    loaded_model = pickle.loads(model_byte_string)    
    audio, sr = librosa.load(uploaded_audio_path)
    audio_list = []
    audio_list.append(audio)
    audio_list_resized = preprocess.resizeaudio(audio_list,False)
    output = loaded_model.predict(audio_list_resized)
    return output

@app.route('/<path:filename>')
def download_file(filename):
    try:
        filename=os.path.join(app.root_path, filename)
        return send_file(filename)
    except FileNotFoundError:
        abort(404)