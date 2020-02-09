import argparse
from server import Server
parser = argparse.ArgumentParser(description="With this tool, you can start an HTTP server, which handles requests of documents to be anonymized. You have the ability to specify port, host, GPU, CPU, and which models to use")

parser.add_argument('--host', action='store', type=str, help='The hostname / address the server has')
parser.add_argument('--port', action='store', type=int, help='The port for the server to listen on')

args = parser.parse_args()

server = Server(host=args.host, port=args.port)

server.Startup()