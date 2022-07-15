import sys
import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import pickle
import sklearn
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path += [PARENTDIR,]
print(PARENTDIR+"/new_image.png")
from model import postprocess, preprocess


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
    image_path = run_file_in_trained_model(uploaded_audio)


    return render_template("process.html", image = image_path)

def run_file_in_trained_model(uploaded_audio_path):
    loaded_model = pickle.load(open(MODEL, 'rb'))
    audio, sr = preprocess.loadaudio(uploaded_audio_path)
    audio_list = []
    audio_list.append(audio)
    audio_list_resized = preprocess.resizeaudio(audio_list,False)
    output = loaded_model.predict(audio_list_resized)
    return PARENTDIR + "/" + postprocess.show_predicted_image(output)

    
