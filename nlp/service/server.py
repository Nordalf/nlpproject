import os
import sys
# from flask import Flask, escape, request, flash, redirect, url_for
from sanic import Sanic, response
from sanic.response import json

UPLOAD_FOLDER = 'service/uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'rtf', 'txt'}
MODEL_NAME = 'bert'

app = Sanic(__name__)
app.config.UPLOAD_FOLDER = UPLOAD_FOLDER

class Server:
    model = None
    def __init__(self, host, port, model):
        self.host = host
        self.port = port
        Server.model = model

    @app.route('/api/v1/anonymize', methods = ['POST'])
    def anonymize_file(request):
        if request.files["file"] is None:
            return response.redirect(request.url)

        file = request.files["file"][0]
        if file.name == '':
            return response.redirect(request.url)

        if file and allowed_file(file.name):
            if os.path.exists(os.path.join(app.config.UPLOAD_FOLDER, file.name)):
                print("File has already been uploaded once")
                return response.redirect(request.url)
            with open(os.path.join(app.config.UPLOAD_FOLDER, file.name), "wb") as uploaded_file:
                uploaded_file.write(file.body)
            output = anonymize_file(os.path.join(app.config.UPLOAD_FOLDER, file.name))
            return response.text(output)
            
    @app.route('/api/v1/anonymize', methods = ['GET'])
    async def anonymize_file(request):
        return response.html('''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
        ''')
    
    def Startup(self):
        app.run(host=self.host, port=self.port)


def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as uploaded_file:
        return uploaded_file.readlines()

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as uploaded_file:
        print(f'{content}', file=uploaded_file)

def anonymize_file(file_path, allow_modification=False):
    file_content = read_file(file_path)
    if allow_modification:
        write_file(file_path,file_content)
    else:
        properties = file_path.rsplit('.')
        predictions, _ = Server.model.predict(file_content)
        with open(properties[0] + "_anonymized." + properties[1], 'a', encoding='utf-8') as pfile:
            for sentence in predictions:
                for item in sentence:
                    for key in item:
                        if item.get(key, '') != 'O':
                            pfile.write(key + " {" f"{item.get(key, '')}" + "} ")
                        else:
                            pfile.write(key + " ")

        return predictions
