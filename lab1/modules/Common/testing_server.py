#!/usr/bin/env python3

import os
import sys

_PATH_TO_MODULES_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "modules")
_PATH_TO_SERVER_ = os.path.join(_PATH_TO_MODULES_, "Server")
_PATH_TO_COMMON_ = os.path.join(_PATH_TO_MODULES_, "Common")

from communication import *
exec(open(os.path.join(_PATH_TO_COMMON_, "protocols_utilities.py")).read())





def testRequestToServer(method, args=0):
    print("-------Sending Request to Server--------")
    connection = Communication(("localhost", 44444))
    connection.connectToServer()
    request= createRequest(method, args)
    print("request: " + request)
    connection.send(request)
    reply = connection.read()
    print("reply:   " + reply[:-1])
    connection.disconnectFromServer()
    print("---------------------------------------\n")


def testErrorRequests(requestIn):
    print("-------Sending Error Request to Server--------")
    connection = Communication(("localhost", 44444))
    connection.connectToServer()
    print("request: " + requestIn)
    connection.send(requestIn)
    reply = connection.read()
    print("reply:   " + reply[:-1])
    connection.disconnectFromServer()
    print("----------------------------------------------\n")


testRequestToServer(_READ_)
testRequestToServer(_READ_)

testRequestToServer(_WRITE_, "Test Fortune to write")


testErrorRequests("{method, test}")
testErrorRequests('{"nethod" : "read"}')
testErrorRequests('{"method" : "rsead"}')