Early stage of an app that takes piano audio and transcribes it into sheet music using a machine learning model. The site is hosted at https://music-transcription-app.herokuapp.com/
It's been developed using python, interactive python notebook (ipynb), Flask and Heroku.

-
    Type into your bash or console terminal
    ~~~
    git clone https://github.com/Brien1/Transcriber123.git
    ~~~
    To clone the repository

- install requirements
    ~~~
    pip install -r requirements.txt
    ~~~
- heroku user account
    https://signup.heroku.com/
    Follow instructions to create an account and verify your registered email address
- heroku CLI
    The Heroku Coimmand Line Interface (CLI), requires and installation of git, follow this link https://git-scm.com/book/en/v2/Getting-Started-Installing-Git to isntall.
    
    Mac 
    ~~~
    brew tap heroku/brew && brew install heroku
    ~~~

    Windows download
        64-bit installer https://cli-assets.heroku.com/heroku-x64.exe
        32-bit installer https://cli-assets.heroku.com/heroku-x86.exe
- heroku app creation
    To create an app type in your terminal within the directory of transcriber123
    ~~~
    heroku create app_name_here
    ~~~
    which will create an app named 'app_name_here'

- heroku buildpacks:
    The app currently uses 3 buildpacks:
    python
    ubunto
    ffmpeg (backend for loading audio)

    To add these to the newly created app:
    ~~~
    heroku buildpacks:set heroku/python
    heroku buildpacks:set https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku-community/apt.tgz
    heroku buildpacks:set https://github.com/merwane/heroku-buildpack-ffmpeg-latest.git
    ~~~
- heroku deployment
    When you're ready to deploy
    ~~~
    git push heroku main
    ~~~
- develop locally
    The development process is as follows. The 'application' folder holds app.py module which is the responsible for backend computing, including redirecting to pages, receiving uploaded files and rendering the model output. 
    Frontend pages are developed using jinja2 template syntax (https://jinja.palletsprojects.com/en/3.1.x/templates/). Links and redirects use flask syntax (https://flask.palletsprojects.com/en/1.1.x/quickstart/)
    ~~~
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    ~~~
    Above is a basic hello world page, witout using templates, just Flask
    ~~~
    @app.route("/" , methods=['GET', 'POST'])
    def upload_file():
        """Gets the file from post data, saves, runs it through the ML model and redirects to new page
        with model output (image)
        Returns:
            jinja2 rendering: process.html where image = output from model
        """
        f= request.files.get("file1")
        uploaded_audio = app.config["UPLOAD_FOLDER"]+"/temp"
        f.save(uploaded_audio)
        output = run_file_in_trained_model(uploaded_audio)
        postprocess.show_predicted_image(output)
        return render_template("process.html", image = os.path.join(app.static_url_path,"new_image.png"))
    ~~~
    Above is a method which returns a template rendering of process.html, which is a template sitting in the templates folder next to app.py module. 
- import new model
    model/get_model.py module calls another project where the model is being developed. 
    ~~~
    git clone https://gitlab2.eeecs.qub.ac.uk/40314811/final-project.git
    ~~~
- test procedure
    In the testing subdirectory, contains all the tests for the app.
    Please read https://flask.palletsprojects.com/en/1.1.x/testing/
    for an overview of testing. This project uses unit test instead of pytest in this article but the process is much the same -  use the self.client object in the AppTestCase class to .get or .post, to different @app.route("/") in the app.py module and make assertions on the return (which will usually be a redering of a jinja2 page through flask). Particular difficulties I faced with this was the method url_for() within the template is translated as an undeclared variable, so you need to pass the method as a variable if rendering the page. 
    ~~~
        from flask import url_for
        rendered_template = template.render({"url_for":url_for},image="/static/new_image.png")
    ~~~
- test coverage
    The requirements install coverage module. Running:
    ~~~
    coverage run testing/test_app.py
    ~~~
    Followed by:
    ~~~
    coverage report -m               
    ~~~
    Will show the percentage coverage of your tests.
