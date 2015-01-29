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
        sendData = 'balle'
        self.serverStream.write('sendData' + '\n')
        self.serverStream.flush()


testObj = Communication(("localhost",46089))
testObj.connectToServer()
testObj.test()

out = testObj.serverStream.readline()
testObj.serverSocket.close()
print("Answer: " + out)

testObj.serverSocket.close()

