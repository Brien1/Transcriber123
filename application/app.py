import sys
import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import pickle
import sklearn
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.append(PARENTDIR)
from model import pre_process, post_process
print()
UPLOAD_FOLDER = "user_loaded_content"
MYDIR = os.path.dirname(__file__)
MODEL = os.path.join(PARENTDIR,"model/model.pkl")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(MYDIR,UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("hello.html")
@app.route("/" , methods=['GET', 'POST'])
def upload_file():
    f= request.files.get("file1")
    uploaded_audio = app.config["UPLOAD_FOLDER"]+"/temp"
    f.save(uploaded_audio)
    run_file_in_trained_model(uploaded_audio)


    return render_template("process.html")

def run_file_in_trained_model(uploaded_audio_path):
    loaded_model = pickle.load(open(MODEL, 'rb'))
    audio, sr = pre_process.loadaudio(uploaded_audio_path)
    audio_list = []
    audio_list.append(audio)
    audio_list_resized = pre_process.resizeaudio(audio_list,False)
    output = loaded_model.predict(audio_list_resized)
    post_process.show_predicted_image(output)

    
