""" Flask application instantiated here. All http requests to whatever the server happens to be pass through here.
Returns rendering of html templates and injects code (variables, method names, parameters) into the html template with
Jinja syntax (python style code) to allow dynamic features in the templates.
Linked intrisically to static folder (objects like pictures, audio etc.) and templates (the skeletons the dynamic pages
are build upon) """

from crypt import methods
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
from model import postprocess, preprocess
UPLOAD_FOLDER = "user_loaded_content"
MYDIR = os.path.dirname(__file__)
MODEL1 = os.path.join(PARENTDIR,"model/model1.pkl")
MODEL2 = os.path.join(PARENTDIR,"model/model2.pkl")
ACCEPTED_FILE_TYPES = ["mp3" , "ogg" , "flac" , "m4a" ]


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = MYDIR + "/user_loaded_content"

@app.route("/")
def index(message = "None"):
    """Return Index page, with option message variable.  
    message is string format warning displayed under the upload button on hello.html
    """
    return render_template("hello.html", message = message)

@app.route("/" , methods=['GET', 'POST'])
def upload_file():
    """Gets the file from post data, saves, runs it through the ML model and redirects to new page
    with model output (image)
    Returns:
        jinja2 rendering: process.html where image = output from model
    """
    f= request.files.get("file1")
    temp_audio = os.path.join(app.config["UPLOAD_FOLDER"], "temp")
    extension = f.filename.split(".")[-1]
    tempaudio = "temp." + extension
    static_audio = os.path.join((MYDIR + app.static_url_path),tempaudio)
    f.save(temp_audio)
    f.save(static_audio)    
    try:
        output = run_file_in_trained_model(temp_audio)
        print(output)
        postprocess.show_predicted_image(output)
        return render_template("process.html", image = os.path.join(app.static_url_path,"new_image.png") , audio_path = os.path.join(app.static_url_path,tempaudio))
    except Exception:
        accepted_files = ""
        for n , i in enumerate(ACCEPTED_FILE_TYPES):
            if n < (len(ACCEPTED_FILE_TYPES)-1):
                accepted_files+= str(i) +", "
            else:
                accepted_files+=str(i)
        os.remove(temp_audio)
        os.remove(static_audio)
        if extension != "" and extension not in ACCEPTED_FILE_TYPES:
            return index(message= "Only "+ accepted_files+" formats currently accepted.")
        if extension == "":
            return index(message= "You did not select a file! \n "+ accepted_files+" formats currently accepted.")

        else:
            return index()
    
def run_file_in_trained_model(uploaded_audio_path):
    """Runs the temp.mp3 (save audio from upload) through ML model to get an output

    Args:
        uploaded_audio_path (str): path to uploaded audio

    Returns:
        base64 encoded numpy array: decode for png/ jpg etc.
    """
    f1=pickle.load(open(MODEL1,"rb"))
    f2=pickle.load(open(MODEL2,"rb"))
    model_byte_string = f1+ f2
    loaded_model = pickle.loads(model_byte_string) 
    
    audio, sr = librosa.load(uploaded_audio_path)
 
    audio_arranged = preprocess.arrange_waveform_to_start_of_clip(audio)
    audio_list = []
    audio_list.append(audio_arranged)
    audio_list_resized = preprocess.resizeaudio(audio_list,False)
    output = loaded_model.predict(audio_list_resized)
    return output

@app.route('/<path:filename>', methods=['GET'])
def download_file(filename):
    """Request image to display on page

    Args:
        filename (str): image file name

    Returns:
        str: address of image file
    """
    try:
        print(request.args.get('attachment'))
     
        filename=os.path.join(app.root_path, filename)
        return send_file(filename)
   
    except FileNotFoundError:
        abort(404)
        
@app.route('/download')        
def send_image():
    """ downloads the image (output from model) as an attachment into downloads folder

    Returns:
        ftp: initiates download
    """
    print(request.args.get('filename'))
    filename = request.args.get('filename')
    filename = filename.strip("/")
    filename=os.path.join(app.root_path, filename)
    print(filename)
    return send_file(filename,as_attachment=True)

@app.route('/getaudio', methods=['GET'])
def getaudio():
    audio_path = request.args.get("audio_path")
    audio_path = audio_path.strip("/")
    audio_path = os.path.join(app.root_path, audio_path)
    print("getting audio")
    print(audio_path)
    return audio_path