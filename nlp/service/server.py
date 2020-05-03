import os
import sys
from sanic import Sanic, response
from sanic.response import json
from sanic_cors import CORS, cross_origin
import time

UPLOAD_FOLDER = 'service/uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'rtf', 'txt'}
MODEL_NAME = 'bert'

app = Sanic(__name__)
app.config.UPLOAD_FOLDER = UPLOAD_FOLDER
# CORS(app)

class Server:
    model = None
    def __init__(self, host, port, model):
        self.host = host
        self.port = port
        Server.model = model
        print(Server.model)

    @app.route('/api/v1/anonymize/file', methods = ['POST'])
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
            output = file_anonymization(os.path.join(app.config.UPLOAD_FOLDER, file.name))
            return response.text(output)
    
    @app.route('/api/v1/anonymize/text', methods = ['POST', 'OPTIONS'])
    @cross_origin(app)
    async def anonymize_text(request):
        response = text_anonymization(request.json)
        print(response)
        return json({ "received": True, "data": response }, content_type="application/json; charset=utf-8")

    @app.route('/api/v1/anonymize', methods = ['GET'])
    async def anonymize(request):
        return json({ "received": True, "data": request.json })
    
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

def file_anonymization(file_path, allow_modification=False):
    file_content = read_file(file_path)
    if allow_modification:
        write_file(file_path,file_content)
    else:
        properties = file_path.rsplit('.')
        t0 = time.time()
        predictions, _ = Server.model.predict(file_content)
        time_elapsed = time.time() - t0
        print("Time elapsed", time_elapsed)
        response = ""
        with open(properties[0] + "_anonymized." + properties[1], 'a', encoding='utf-8') as pfile:
            for sentence in predictions:
                for item in sentence:
                    for key in item:
                        if item.get(key, '') != 'O':
                            pfile.write(key + " {" f"{item.get(key, '')}" + "} ")
                            response += key + " {" f"{item.get(key, '')}" + "} "
                        else:
                            pfile.write(key + " ")
                            response += key + " "

        return response

def text_anonymization(content):
    t0 = time.time()
    predictions = Server.model.predict(content)
    time_elapsed = time.time() - t0
    print("Time elapsed", time_elapsed)
    return predictions
