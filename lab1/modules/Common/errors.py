#!/usr/bin/env python3

class Error(Exception):
    """Base class for exceptions in protocol.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    pass

class MsgFormatError(Error):
    # Exception raised for errors in the message format.
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    

class MethodError(Error):
    # Exception raised for using undefined method.
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    
class ArgumentError(Error):
    # Exception raised for using wrong arguments for a given method.
    
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    
