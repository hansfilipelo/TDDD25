#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 31 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Server that serves clients trying to work with the database."""

import threading
import socket
import random
import argparse
import os
import sys

_PATH_TO_MODULES_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "modules")
_PATH_TO_SERVER_ = os.path.join(_PATH_TO_MODULES_, "Server")
_PATH_TO_COMMON_ = os.path.join(_PATH_TO_MODULES_, "Common")

sys.path.append(_PATH_TO_MODULES_)
from Server.database import Database
from Common.communication import *
exec(open(os.path.join(_PATH_TO_COMMON_, "protocols_utilities.py")).read())


# -----------------------------------------------------------------------------
# Initialize and read the command line arguments
# -----------------------------------------------------------------------------

rand = random.Random()
rand.seed()
description = """\
Server for a fortune database. It allows clients to access the database in
parallel.\
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "-p", "--port", metavar="PORT", dest="port", type=int,
    default=44445,
    help="Set the port to listen to. Values in [40001, 50000]. "
         "The default value is chosen at random."
)
parser.add_argument(
    "-f", "--file", metavar="FILE", dest="file", default="dbs/fortune.db",
    help="Set the database file. Default: dbs/fortune.db."
)
opts = parser.parse_args()

db_file = opts.file
server_address = ("", opts.port)

# -----------------------------------------------------------------------------
# Auxiliary classes
# -----------------------------------------------------------------------------


class Server(object):
    
    db = ""
    
    """Class that provides synchronous access to the database."""

    def __init__(self, db_file):
        self.db = Database(db_file)
    
    # Public methods
    def read(self):
        return(self.db.read())

    def write(self, fortune):
        return self.db.write(fortune)


class Request(threading.Thread):

    """ Class for handling incoming requests.
        Each request is handled in a separate thread.
    """

    def __init__(self, db_server, conn, addr):
        threading.Thread.__init__(self)
        self.db_server = db_server
        self.conn = conn
        self.addr = addr
        self.daemon = True
    
    def process_request(self, request):
        try:
            requestData = loadRequest(request)

            if requestData[_METHOD_] == _READ_:
                try:
                    return createResultReply(self.db_server.read())
                except DatabaseError as e:
                    return createErrorReply(type(e).__name__,"")
            
            if requestData[_METHOD_] == _WRITE_:
                result = self.db_server.write(requestData[_ARGS_])
                return createResultReply("Wrote fortune to database.")
        
        except MsgFormatError as e:
            return createErrorReply(type(e).__name__, e.expression+e.message)
        except ArgumentError as e:
            return createErrorReply(type(e).__name__, e.expression+e.message)
        except MethodError as e:
            return createErrorReply(type(e).__name__, e.expression+e.message)
        except DatabaseError as e:
            return createErrorReply(type(e).__name__)

        return 'Wuuut??'

    def run(self):
        try:
            # Treat the socket as a file stream.
            worker = self.conn.makefile(mode="rw")
            # Read the request in a serialized form (JSON).
            request = worker.readline()
            # Process the request.
            result = self.process_request(request)
            # Send the result.
            worker.write(result + '\n')
            worker.flush()
        except Exception as e:
            # Catch all errors in order to prevent the object from crashing
            # due to bad connections coming from outside.
            print("The connection to the caller has died:")
            print("\t{}: {}".format(type(e), e))
        finally:
            self.conn.close()

# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------

print("Listening to: {}:{}".format(socket.gethostname(), opts.port))
with open("srv_address.tmp", "w") as f:
    f.write("{}:{}\n".format(socket.gethostname(), opts.port))

sync_db = Server(db_file)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(1)

print("Press Ctrl-C to stop the server...")

try:
    while True:
        try:
            conn, addr = server.accept()
            print("Connection est.")
            req = Request(sync_db, conn, addr)
            print("Serving a request from {0}".format(addr))
            req.start()
        except socket.error:
            continue
except KeyboardInterrupt:
    pass
