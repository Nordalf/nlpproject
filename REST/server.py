import os
from flask import Flask, escape, request, flash, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
# The extentions allowed to be anonymized
ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'rtf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    @app.route('/api/v1/anonymize', methods = ['GET','POST'])
    def anonymize_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                return redirect(url_for('anonymize_file', filename=file.filename))
                
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
        '''

    def Startup(self):
        app.run(host=self.host, port=self.port)


def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
