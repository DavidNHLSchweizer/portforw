import requests
import http.server
import socketserver
import argparse

def parseArguments(defaultPort, defaultColor):
    parser = argparse.ArgumentParser(description='simple echo server test')
    parser.add_argument('--p',default=defaultPort,type=int,help='the port to use [{}]'.format(defaultPort))
    parser.add_argument('--c',default=defaultColor,type=str,help='the background color to use [{}]'.format(defaultColor))
    parser.add_argument('--m',default='',type=str,help='the distinguishing message for the site)')    
    args=parser.parse_args()
    return args

PORT  = 8000
COLOR = 'blue'
MESSAGE = 'message'

SIMPLE_SITE = """
<html>
<head>
<title>Python Test</title>
</head>
<body style = "background-color:{};">
<h1>Wonderful Server!</h1>
<p>{}</p>
<b>
<p>port: {}</p>
<b>
<p> <a href="./link1"> link </a> </p>

</body>
</html>
"""

SIMPLE_SITE_LINK1 = """
<html>
<head>
<title>Python Test (link 1)</title>
</head>
<body style = "background-color:{};">
<h1>Wonderful Link!</h1>
<p>{}</p>
<b>
<p>port: {}</p>

</body>
</html>
"""


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    color = COLOR
    message= MESSAGE
    port = PORT

    def getHTMLPage(self, path):
        if path=="/":
            return SIMPLE_SITE.format(ServerHandler.color,ServerHandler.message, ServerHandler.port)
        elif path=="/link1":
            return SIMPLE_SITE_LINK1.format(ServerHandler.color,ServerHandler.message, ServerHandler.port)
        else:
            return ""

    def sendResponse(self, path):
        htmlString = self.getHTMLPage(path)
        if htmlString == "":
            self.send_response(404)
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(htmlString))
        self.end_headers()
        self.wfile.write(str.encode(htmlString))        
    def do_GET(self):   
        print(self.path)
        self.sendResponse(self.path)

args = parseArguments(PORT, COLOR)
ServerHandler.color = args.c
ServerHandler.message = args.m
ServerHandler.port = args.p

with socketserver.TCPServer(("", ServerHandler.port), ServerHandler) as httpd:
    print('serving as "{}" at port {} with color {}'.format(ServerHandler.message, ServerHandler.port, ServerHandler.color))
    httpd.serve_forever()
