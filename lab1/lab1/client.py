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
import json
import argparse
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../modules/Common")
exec(open("../modules/Common/protocols_utilities.py").read())
from communication import *

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
        
        nrOfRetries = 0
        while not (self.serverSock.connectToServer() and nrOfRetries < self.maxRetries):
            nrOfRetries += 1
        
        if nrOfRetries >= self.maxRetries:
            print("Failed to connect to server")
            sys.exit(1)
    
    # Public methods
    
    def read(self):
        self.serverSock.send(createRequest(_READ_,""))
        
        reply = self.serverSock.read()
        
        if msgFormatCorrect(reply) == _OK_:
            exitCode = requestDataIsCorrect(reply)
            
            if exitCode == _OK_:
                return readReply(reply)
            if exitCode == _ARGS_ERROR_:
                print("Argument error!")
                return
            print("Method error!")
            return
        print("Message format incorrect!")
    
    
    def write(self, fortune):
        self.serverSock.send(createRequest(_WRITE_,fortune))
        
        reply = self.serverSock.read()
        
        if msgFormatCorrect(reply) == _OK_:
            exitCode = requestDataIsCorrect(reply)
            
            if exitCode == _OK_:
                return readReply(reply)
            if exitCode == _ARGS_ERROR_:
                print("Argument error!")
                return
            print("Method error!")
            return
        print("Message format incorrect!")

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
            db.write(command[2:].strip())
        elif command == "h":
            menu()
