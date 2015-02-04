#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 31 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Client reader/writer for a fortune database."""

import sys
import argparse
import os

_PATH_TO_MODULES_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "modules")
_PATH_TO_SERVER_ = os.path.join(_PATH_TO_MODULES_, "Server")
_PATH_TO_COMMON_ = os.path.join(_PATH_TO_MODULES_, "Common")

sys.path.append(_PATH_TO_MODULES_)
from Common.communication import *

exec(open(os.path.join(_PATH_TO_COMMON_, "protocols_utilities.py")).read())

# -----------------------------------------------------------------------------
# Initialize and read the command line arguments
# -----------------------------------------------------------------------------


def address(path):
    addr = path.split(":")
    if len(addr) == 2 and addr[1].isdigit():
        return((addr[0], int(addr[1])))
    else:
        msg = "{} is not a correct server address.".format(path)
        raise argparse.ArgumentTypeError(msg)

description = """\
Client for a fortune database. It reads a random fortune from the database.\
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "-w", "--write", metavar="FORTUNE", dest="fortune",
    help="Write a new fortune to the database."
)
parser.add_argument(
    "-i", "--interactive", action="store_true", dest="interactive",
    default=False, help="Interactive session with the fortune database."
)
parser.add_argument(
    "address", type=address, nargs=1, metavar="addr:port",
    help="Server address."
)
opts = parser.parse_args()
server_address = opts.address[0]

# -----------------------------------------------------------------------------
# Auxiliary classes
# -----------------------------------------------------------------------------


class ComunicationError(Exception):
    pass


class DatabaseProxy(object):
    
    """Class that simulates the behavior of the database class."""
    
    serverSock = ""
    maxRetries = 1
    
    def __init__(self, server_address):
        self.serverSock = Communication(server_address)
    
    # Public methods
    
    def read(self):
        # Connect to server
        nrOfRetries = 0
        while not (self.serverSock.connectToServer() and nrOfRetries < self.maxRetries):
            nrOfRetries += 1
        
        if nrOfRetries >= self.maxRetries:
            print("Failed to connect to server")
            return
        
        # Send to socket
        while not self.serverSock.send(createRequest(_READ_,"")):
            pass
        
        try:
            result = loadReply(self.serverSock.read())
            self.serverSock.disconnectFromServer()
            return result
        except MsgFormatError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except ArgumentError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except MethodError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except DatabaseError as e:
            return type(e).__name__
            
    
    
    def write(self, fortune):
        # Connect to server
        nrOfRetries = 0
        while not (self.serverSock.connectToServer() and nrOfRetries < self.maxRetries):
            nrOfRetries += 1
        
        if nrOfRetries >= self.maxRetries:
            print("Failed to connect to server")
            return
        
        while not self.serverSock.send(createRequest(_WRITE_,fortune)):
            pass
        try:
            result = loadReply(self.serverSock.read())
            if not result:
                return "No answer from server"
            self.serverSock.disconnectFromServer()
            return result
        except MsgFormatError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except ArgumentError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except MethodError as e:
            return type(e).__name__ + ": " + str(e.expression+e.message)
        except DatabaseError as e:
            return type(e).__name__

# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------

# Create the database object.
db = DatabaseProxy(server_address)

if not opts.interactive:
    # Run in the normal mode.
    if opts.fortune is not None:
        db.write(opts.fortune)
    else:
        print(db.read())

else:
    # Run in the interactive mode.
    def menu():
        print("""\
Choose one of the following commands:
    r            ::  read a random fortune from the database,
    w <FORTUNE>  ::  write a new fortune into the database,
    h            ::  print this menu,
    q            ::  exit.\
""")

    command = ""
    menu()
    while command != "q":
        sys.stdout.write("Command> ")
        command = input()
        if command == "r":
            print(db.read())
        elif (len(command) > 1 and command[0] == "w" and
                command[1] in [" ", "\t"]):
            print(db.write(command[2:].strip()))
        elif command == "h":
            menu()
