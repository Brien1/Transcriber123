- git clone
    Type into your bash or console terminal
    ~~~
    git clone https://github.com/Brien1/Transcriber123.git
    ~~~
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
- import new model
- test procedure
