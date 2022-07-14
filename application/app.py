import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = "user_loaded_content"
MYDIR = os.path.dirname(__file__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(MYDIR,UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("hello.html")
@app.route("/" , methods=['GET', 'POST'])
def upload_file():
    f= request.files.get("file1")
    #
    # f.save("/Users/brienhall/Documents/FinalProject/app/user_loaded_content/temp")
    f.save(app.config["UPLOAD_FOLDER"]+"/temp")
    
    # request.files[1].save(os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_content"))


    return render_template("process.html")



    
