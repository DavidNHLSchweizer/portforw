import socketserver
import http.server
import requests
import argparse
import socket

PORT = 65432
def parseArguments(defaultPort):
    parser = argparse.ArgumentParser(description='simple port forwardert')
    parser.add_argument('--p',default=defaultPort,type=int,help='the port to use [{}]'.format(defaultPort))
    args=parser.parse_args()
    return args.p

class clientServerInfo(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

class ForwardingHandler(http.server.SimpleHTTPRequestHandler):
    knownClientServers = []
    CurrentClientIndex = 0
    recursive = False
    def selectClientServer(self):
        index = ForwardingHandler.CurrentClientIndex
        ForwardingHandler.CurrentClientIndex = (ForwardingHandler.CurrentClientIndex + 1) % len(ForwardingHandler.knownClientServers)        
        return ForwardingHandler.knownClientServers[index]
    def getResponseFromServer(self):
        client = self.selectClientServer()
        print('get response from {}:{}'.format(client.host,client.port))
        return requests.get('http://{}:{}'.format(client.host, client.port))
    def sendResponse(self, response):
        print("sending response (status): {}".format(response.status_code))
        self.send_response(response.status_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response.text))
        self.end_headers()
        self.wfile.write(str.encode(response.text))     
    def do_GET(self):     
        if ForwardingHandler.recursive:
            print ("recur")
            return
        if self.path=="/favicon.ico":
            print("favicon, ignoring")
            self.send_response(404)
            return
        ForwardingHandler.recursive = True
        print("get response")
        response = self.getResponseFromServer()
        print("next")
        if response:
            print("send response")
            self.sendResponse(response)
            print("end send")
            ForwardingHandler.recursive = False
        print("end get")

class PortForwarder(object):
    def __init__(self, host, port):
        self.server = socketserver.TCPServer((host, port), ForwardingHandler)
        print("serving at port", port)
    def addClientServer(self, host, port):
        ForwardingHandler.knownClientServers.append(clientServerInfo(host,port))
    def run(self):
        for i in range(len(ForwardingHandler.knownClientServers)):
            client = ForwardingHandler.knownClientServers[i]
            print('server index: {} port: {}.'.format(i, client.port))
        self.server.serve_forever()

port = parseArguments(PORT)
PF = PortForwarder('127.0.0.1', port)
PF.addClientServer('127.0.0.1', 8000)
PF.addClientServer('127.0.0.1', 8001)
PF.addClientServer('127.0.0.1', 8002)
PF.addClientServer('127.0.0.1', 8003)
PF.run()