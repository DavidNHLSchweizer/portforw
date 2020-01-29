import socketserver
import http.server
import requests
import argparse
import socket
import config
import os
import sys

def isFAVICONRequest(requestPath):
    FAVICONREQUEST = "/favicon.ico"
    return requestPath==FAVICONREQUEST

HTTPNOTFOUND = 404
DEFAULTPORT = 65432
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
    NextClientIndex = 0

    def getNextClientServerInfo(self):
        index = ForwardingHandler.NextClientIndex
        ForwardingHandler.NextClientIndex = (ForwardingHandler.NextClientIndex + 1) % len(ForwardingHandler.knownClientServers)
        return ForwardingHandler.knownClientServers[index]

    def getResponseFromClientServer(self, requestPath):
        client = self.getNextClientServerInfo()
        print("forwarding {} to {}:{}".format(requestPath, client.host, client.port))
        return requests.get('http://{}:{}{}'.format(client.host, client.port, requestPath))

    def sendResponse(self, response):
        self.send_response(response.status_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response.text))
        self.end_headers()
        self.wfile.write(str.encode(response.text))     

    def do_GET(self):     
        if isFAVICONRequest(self.path):
            self.send_response(HTTPNOTFOUND)
            return
        response = self.getResponseFromClientServer(self.path)
        if response:
            self.sendResponse(response)

class PortForwarder(object):
    def __init__(self, host, port):
        self.port = port
        self.server = socketserver.TCPServer((host, port), ForwardingHandler)      

    def addClientServer(self, host, port):
        ForwardingHandler.knownClientServers.append(clientServerInfo(host,port))

    def run(self):
        self.printPorts()
        self.server.serve_forever()

    def printPorts(self):
        print("serving at port", self.port)
        for i in range(len(ForwardingHandler.knownClientServers)):
            client = ForwardingHandler.knownClientServers[i]
            print('server index: {} port: {}.'.format(i, client.port))

    def readConfigurationFile(self,filename):
        ports = config.readConfigurationFile(filename)
        for port in ports:
            self.addClientServer('127.0.0.1', port)

port = parseArguments(DEFAULTPORT)
PF = PortForwarder('127.0.0.1', port)
PF.readConfigurationFile(os.path.join(sys.path[0], 'config.txt'))
PF.run()