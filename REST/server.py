from flask import Flask, escape, request

class Server:
    app = Flask(__name__)
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    @app.route('/api/v1/')
    def hello():
        name = request.args.get("name", "world")
        return f'Hello, {escape(name)}!'

    def Startup(self):
        self.app.run(host=self.host, port=self.port)