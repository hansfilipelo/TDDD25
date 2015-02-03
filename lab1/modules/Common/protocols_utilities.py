import json
#//////////////////// Begin of: Global variables ////////////////////////////#
# Requests methods
_READ_ = "read"
_WRITE_ = "write"

_METHOD_LIST_ = [_READ_, _WRITE_]

# Message components
_METHOD_ = "method"
_ARGS_ = "args"
_RESULT_ = "result"
_ERROR_ = "error"
_ERROR_NAME_ = "name"
#//////////////////// End of: Global variables //////////////////////////////#



#//////////////////// Begin of: Error classes ////////////////////////////#
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
#//////////////////// End of: Error classes //////////////////////////////#



#//////////////////// Begin of: Functions to find errors if they exists /////#
def isJson(json_in):
  try:
    json_out = json.loads(json_in)
  except:
    return False
  return json_out


def msgFormatCorrect(msg_in, is_request = False):
    dict = isJson(msg_in)
    if dict and ((_METHOD_ in dict) or (_RESULT_ in dict and len(dict)==1) or (_ERROR_ in dict and len(dict)==1)):
        return
    raise MsgFormatError("Received message: ",msg_in)
    


def requestDataIsCorrect(data):
    if (data[_METHOD_]) in _METHOD_LIST_:
        if data[_METHOD_] == _READ_ or data[_METHOD_] == _WRITE_ and isinstance(data[_ARGS_], str):
            return
        raise ArgumentError(str(data[_METHOD_]), str(data[_ARGS_]))
    raise MethodError(str(data[_METHOD_]), "Arguemnt must be wrong ofc!!")
#//////////////////// End of: Functions to find errors if they exists ///////#



#//////////////////// Begin of: Functions to create or load request/reply ///#
def createRequest(method, args=0):
    if args:
        return json.dumps({_METHOD_: method, _ARGS_: args})
    return json.dumps({_METHOD_: method})

def loadRequest(requestIn):
    print("We are here 1")
    msgFormatCorrect(requestIn, True)
    data = json.loads(requestIn)
    print("We are here 2")
    requestDataIsCorrect(data)
    return data

def loadReply(replyIn):
    print(replyIn)
    msgFormatCorrect(replyIn)
    data = json.loads(replyIn)
    requestDataIsCorrect(data)
    return data


def createErrorReply(errorClass, argsIn):
    return json.dumps({_ERROR_: {_ERROR_NAME_ : errorClass, _ARGS_ : argsIn}})

def createResultReply(method_result):
    return json.dumps({_RESULT_: method_result})
#//////////////////// End of: Functions to create or load request/reply /////#
