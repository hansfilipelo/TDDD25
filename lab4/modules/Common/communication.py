#!/usr/bin/env python3

import socket
import json

class Communication(object):

    serverSocket = ""
    serverInfo = () # (adress, portNumber)
    serverStream = ""

    def __init__(self,inServerInfo):
        self.serverInfo = inServerInfo

    def connectToServer(self):
        try:
            self.serverSocket = socket.create_connection(self.serverInfo)
            self.serverSocket.settimeout(1)
            self.serverStream = self.serverSocket.makefile(mode="rw")
            return True
        except socket.error:
            return False

    def disconnectFromServer(self):
        self.serverStream.close()
        self.serverSocket.close()

    def send(self,message):
        
        self.serverStream.write(message + '\n')
        self.serverStream.flush()

    def read(self):
        try: 
            print("In comm")
            data = self.serverStream.readline()
            print("In comm 2")
            return data
        except Exception as e:
            print("Fail")
            print(type(e).__name__ + " - Arguments: " + e.args)
    
    def listen(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(self.serverInfo)
        self.serverSocket.listen(1)
        
    def accept(self):
        conn, addr = self.serverSocket.accept()
        self.serverStream = conn.makefile(mode="rw")
        return self.serverStream, addr
    
    def test(self):
        sendData = '{"method": "read"}'
        self.serverStream.write(sendData + '\n')
        self.serverStream.flush()