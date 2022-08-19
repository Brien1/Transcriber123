import base64 as b64
import numpy as np
import fileinput
from http import client
import unittest
import sys, os
from urllib import response
from xmlrpc.client import ResponseError
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
ROOTDIR = os.path.dirname(PARENTDIR)
sys.path += [PARENTDIR,]
from application.app import app, run_file_in_trained_model
from jinja2 import Environment, PackageLoader, select_autoescape, FunctionLoader as fl, FileSystemLoader
from werkzeug.datastructures import FileStorage
from flask import render_template, url_for


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["SERVER_NAME"] = "localhost:5000"
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        
    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get("/")
        templateloader = FileSystemLoader(searchpath="./")
        templateenv = Environment(loader=templateloader)
        TEMPLATE_FILE = "application/templates/hello.html"
        template = templateenv.get_template(TEMPLATE_FILE)
        outputtext = template.render()  # this is where to put args to the template renderer
        assert response.status_code == 200
        assert outputtext == response.get_data(as_text=True)
 
    def uploadsound(self):
        file = os.path.join(CURRENTDIR, "A0-test.mp3")
        my_file = FileStorage(
        stream=open(file, "rb"),
        filename="A0-test.mp3",
        content_type="audio/mp3",)

        return self.client.post(
        "/",
        data={
            "file1": my_file,
        },
        content_type="multipart/form-data",
        follow_redirects = True,
        base_url='https://localhost:5000'
        )
        
    def test_uploadfile(self):
        env = Environment(
        autoescape=select_autoescape(),
        loader=FileSystemLoader(searchpath=PARENTDIR+"/application/templates/"),
        )   
        template = env.get_template("process.html",None)
        from flask import url_for
        rendered_template = template.render({"url_for":url_for},image="/static/new_image.png")
        response = self.uploadsound()
        from_file = rendered_template.replace("http://localhost:5000","")
        response_to_upload = (response.data).decode()
       
        assert from_file == response_to_upload
  
    def test_run_trained_model(self):
        file = os.path.join(CURRENTDIR, "A0-test.mp3")
        assert type(file) == type(str())
        output = run_file_in_trained_model(file)
        assert type(output) == type(np.array([3]))
        output_decoded = b64.b64decode(output)
        assert type(output_decoded) == type(bytes())
        
    def test_send_image(self):
        response = self.client.get("/download",query_string={"filename":"static/new_image.png"})
        print(response)
        print("")
        assert response.status_code == 200
        assert type(response.data) == type(bytes())


            
if __name__ == "__main__":
    unittest.main()
