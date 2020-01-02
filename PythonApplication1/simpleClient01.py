#!/usr/bin/env python3

import socket
import argparse

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def parseArguments(defaultPort):
    parser = argparse.ArgumentParser(description='simple echo server test')
    parser.add_argument('--p',default=defaultPort,type=int,help='the port to use [{}]'.format(defaultPort))
    args=parser.parse_args()
    return args.p

port = parseArguments(PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received: ', repr(data))