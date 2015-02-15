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
            self.serverStream = self.serverSocket.makefile(mode="rw")
            return True
        except socket.error:
            return False

    def disconnectFromServer(self):
        self.serverStream.close()
        self.serverSocket.close()

    def send(self,message):
        try:
            self.serverStream.write(message + '\n')
            self.serverStream.flush()
            return True
        except:
            return False

    def read(self):
        try:
            return self.serverStream.readline()
        except:
            return False

    def test(self):
        sendData = '{"method": "read"}'
        self.serverStream.write(sendData + '\n')
        self.serverStream.flush()