import os
import flask
from flask.json import jsonify
from flask import request, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import uuid
import glob
import threading
import time
import pathlib

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = "files"
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

@app.route('/', methods = ['GET'])
def root_path() :
    return jsonify({"message" : "Hello world!"})

def check_allowed(filename) :
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def auto_delete(directory) :
    print("delete in progress, user is able to download the file in 60 seconds")
    time.sleep(60)
    os.remove(directory)
    print("complete")
    

@app.route('/upload/change-format', methods=['POST'])
def upload_file_change_format() :
    if request.method == 'POST' :
        try :
            f = request.files['file']
            format = request.form['format']
            if f and check_allowed(f.filename) and format.lower() in ALLOWED_EXTENSIONS:

                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded')) :
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded'))

                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'target')) :
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'target'))

                name_and_format = secure_filename(f.filename).split(".")
                file_uuid = str(uuid.uuid4())
                uploaded_filename = file_uuid + "." + name_and_format[1]
                uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded', uploaded_filename)
                f.save(uploaded_path)

                img = Image.open(uploaded_path)
                target_name = file_uuid + "." + format
                target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'target', target_name)
                rgb_mage = img.convert('RGB')
                rgb_mage.save(target_path)

                os.remove(uploaded_path)
                threading.Thread(target=auto_delete, args=(target_path,)).start()
                
                return jsonify({
                    "message" : "File is uploaded successfully",
                    "status": True,
                    "code": 200,
                    "data": file_uuid
                })
            else :
                return jsonify({
                    "message" : "Format file is not supported",
                    "status": False,
                    "code": 403,
                    "data": None
                })
        except :
             return jsonify({
                    "message" : "File is is too large",
                    "status": False,
                    "code": 413,
                    "data": None
                })

@app.route('/upload/compress-image', methods=['POST'])
def upload_file_compress_image() :
    if request.method == 'POST' :
        try :
            f = request.files['file']
            quality = int(request.form['quality'])

            if quality is None or (quality < 0 and quality > 100) :
                return jsonify({
                    "message" : "quality must be not null and in range between 0 and 100",
                    "status": False,
                    "code": 403,
                    "data": None
                })

            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded')) :
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded'))

            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'target')) :
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'target'))

            name_and_format = secure_filename(f.filename).split(".")
            file_uuid = str(uuid.uuid4())
            uploaded_filename = file_uuid + "." + name_and_format[1]
            uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_uploaded', uploaded_filename)
            f.save(uploaded_path)

            img = Image.open(uploaded_path)
            target_name = file_uuid + "." + name_and_format[1]
            target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'target', target_name)
            img.save(target_path, optimize=True, quality=quality)

            os.remove(uploaded_path)
            threading.Thread(target=auto_delete, args=(target_path,)).start()
            
            return jsonify({
                "message" : "File is uploaded successfully",
                "status": True,
                "code": 200,
                "data": file_uuid
            })
        except :
             return jsonify({
                    "message" : "File is is too large",
                    "status": False,
                    "code": 413,
                    "data": None
                })


@app.route('/download', methods = ['GET'])
def download_target() :
    if request.method == 'GET' :
        file_id = request.args.get("id")
        target_directory = os.path.join(app.config['UPLOAD_FOLDER'], 'target')
        directory = glob.glob(target_directory + "\\" + file_id + ".**", recursive=True)
        if len(directory) == 0 :
            return jsonify({
                "message" : "File not found",
                "status": False,
                "code": 404
            })
        return send_file(directory[0], as_attachment=True)

if __name__ == "__main__" :
    app.run()