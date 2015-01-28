#!/usr/bin/env python3

import socket

class Communication(object):
    
    serverSocket = ""
    serverInfo = () # (adress, portNumber)
    
    def __init__(self,inServerInfo):
        self.serverInfo = inServerInfo
    
    def connectToServer(self):
        try:
            self.serverSocket = socket.create_connection(self.serverInfo)
        except socket.error:
            print("Connection failed... Damn you world!")

    def test(self):
        self.serverSocket.send(b'Banan')


testObj = Communication(("localhost",48258))
testObj.connectToServer()
testObj.test()
