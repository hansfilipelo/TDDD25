#!/usr/bin/env python3

import socket
import time
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
        except socket.error:
            print("Connection failed... Damn you world!")

    def test(self):
        sendData = "\n"
        self.serverStream.write(sendData)
        self.serverStream.flush()


testObj = Communication(("localhost",48507))
testObj.connectToServer()
testObj.test()

testObj.connectToServer()
out = testObj.serverSocket.recv(2048)
testObj.serverSocket.close()
print("Answer: " + out.decode("utf-8"))

testObj.serverSocket.close()
