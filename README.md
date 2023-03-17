# EXIF Viewer Website
#### Uses flask - python microframework for backend, Exif a python package to extract exif data from pictures

#### Uses pipenv to manage required python packages

#### The following guide assumes the target OS is linux. Please change commands accordingly if different OS is used.

## Installation of pipenv 
    pip install pipenv

## Installation of Flask and exif (no need to specify package names, it will be taken care of by pipenv by using the pipfile)
    cd ./Assignment4
    pipenv install

#### Check if installation is succesful by running the following commands
    pipenv shell
    python3
    import flask
#### If no erros were outputed, installation of flask is succesful.

#### Exit from the python shell
    exit()
    
## Running the Webserver
    flask --app readexif run

## Usage and Navigation of the website
#### Copy the following to your browser address bar
    localhost:5000
