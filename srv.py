import http.server

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

current_num = 0
last_message = "Engine is OK"
last_values = [0.0, 0.0]

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global current_num
        global last_message
        global last_values
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'values': last_values,
	        'message': last_message,
	        'num': current_num
        }).encode())
        return

    current_num = 0
    def do_POST(self):
        global current_num
        global last_message
        global last_values

        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len).decode()

        data = json.loads(post_body)

        self.send_response(200)
        self.end_headers()

        current_num += 1

        if ("command" in data):
            if (data["command"] == "changeMessage"):
                last_message = data['message']
            elif (data["command"] == "changeValues"):
                last_values = data['values']
        else:
            last_message = data['message']
            last_values = data['values']

        self.wfile.write(json.dumps({
            'answer': "ok",
            'message': last_message,
            'last_num': current_num
        }).encode())

        if ("message" in data):
            print("post ok, message = " + data["message"])
        return


server_address = ('', 8000)
httpd = http.server.HTTPServer(server_address, RequestHandler)
httpd.serve_forever()

