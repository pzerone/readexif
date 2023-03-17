import os
from exif import Image
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path

root = Path(__file__).parent
UPLOAD_FOLDER = root / "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('filereport', name=filename))
    return render_template('index.html')

def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    finalcords = round(dd, 4)
    return finalcords
    
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/report/<name>')
def filereport(name):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], name),"rb") as rawimage:
        picture = Image(rawimage)
        attributeList = picture.list_all()
        attributes = {
            "datetime": "Unknown",
            "model": "Unknown",
            "latitude": "Unknown",
            "longitude": "Unknown",
            "make": "Unknown"
            }
        if 'gps_latitude' in attributeList and 'gps_longitude' in attributeList:
            templat = picture.gps_latitude
            templong = picture.gps_longitude
            finlat = dms_to_dd(templat[0], templat[1], templat[2])
            finlong = dms_to_dd(templong[0], templong[1], templong[2])
            attributes["latitude"] = finlat
            attributes["longitude"] = finlong
        if 'model' in attributeList:
            attributes["model"] = picture.model
        if 'datetime' in attributeList:
            attributes["datetime"] = picture.datetime
        if 'make' in attributeList:
            attributes["make"] = picture.make

    return render_template('report.html', attributes = attributes, filename = name)

