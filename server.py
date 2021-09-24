#  coding: utf-8 
import os, mimetypes, socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, ZiQing Ma
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

STATUS = {200: "HTTP/1.1 200 OK\r\n", 301: "HTTP/1.1 301 Moved Permanently\r\n",
                    404: "HTTP/1.1 404 Not Found\r\n", 405: "HTTP/1.1 405 Method Not Allowed\r\n"}


ALLOWED_TYPES = ["text/html", "text/css"]


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode().split()
        self.request_method = self.data[0]
        self.path = self.data[1]
        if self.request_method == "GET":
            self.parse(self.path)

        else:
            self.request.sendall(bytearray(STATUS[405].encode()))
            return


    def parse(self, path):
        serve_dir, serve_from = "/www", "www"
        path = serve_from + path
        if not os.path.exists(path):
            self.request.sendall(bytearray(STATUS[404].encode()))
            return
            
        dir = os.path.dirname(os.path.abspath("__file__")) + serve_dir
        if dir not in os.path.abspath(path):
            self.request.sendall(bytearray(STATUS[404].encode()))
            return

        if os.path.isdir(path) and path[-1] != "/":
            self.request.sendall(bytearray(STATUS[301].encode()))
            return

        if path[-1] == "/":
            path += "index.html"
        
        response = STATUS[200]
        content_type = mimetypes.guess_type(path)[0]
        if content_type in ALLOWED_TYPES:
            response += "Content-Type: {}; charset={}\n\n".format(content_type, "UTF-8")
        else:
            response += "Content-Type: application/octet-stream\n\n"
        response += open(path, 'r').read()
        self.request.sendall(bytearray(response.encode()))

    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
