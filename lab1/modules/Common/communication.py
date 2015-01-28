#!/usr/bin/env python3

import socket
import time

class Communication(object):
    
    serverSocket = ""
    serverInfo = () # (adress, portNumber)
    
    def __init__(self,inServerInfo):
        self.serverInfo = inServerInfo
    
    def connectToServer(self):
        try:
            self.serverSocket = socket.create_connection(self.serverInfo)
            self.serverSocket.settimeout(1)
        except socket.error:
            print("Connection failed... Damn you world!")

    def test(self):
        self.serverSocket.send(b'Banan')


testObj = Communication(("localhost",10000))
testObj.connectToServer()
testObj.test()

time.sleep(5)

out = testObj.serverSocket.recv(4096)
print("Answer: " + out.decode("utf-8"))

testObj.serverSocket.close()