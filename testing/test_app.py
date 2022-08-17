import unittest
import sys, os
from xmlrpc.client import ResponseError
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
ROOTDIR = os.path.dirname(PARENTDIR)
sys.path += [PARENTDIR,]
from application.app import app
import jinja2

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get("/")
        templateloader = jinja2.FileSystemLoader(searchpath="./")
        templateenv = jinja2.Environment(loader=templateloader)
        TEMPLATE_FILE = "application/templates/hello.html"
        template = templateenv.get_template(TEMPLATE_FILE)
        outputtext = template.render()  # this is where to put args to the template renderer
        assert response.status_code == 200
        assert outputtext == response.get_data(as_text=True)

    def test_uploadfile(self):
        response = self.client.post("/", data={"file1" : "A0-test.mp3"})
        print("########" ,response, response.get_data(as_text=True))
        
if __name__ == "__main__":
    unittest.main()