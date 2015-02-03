import json
#//////////////////// Begin of: Global variables ////////////////////////////#
# Requests methods
_READ_ = "read"
_WRITE_ = "write"

_METHOD_LIST_ = [_READ_, _WRITE_]

# Result answers
_RESULT_ = "result"
_ERROR_ = "error"

# Message components
_METHOD_ = "method"
_ARGS_ = "args"
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

class DatabaseError(Error):
    
    pass

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
    if dict:
        if dict and ((_METHOD_ in dict) or (_RESULT_ in dict and len(dict)==1) or (_ERROR_ in dict and len(dict)==1)):
            return
    raise MsgFormatError("Received message: ",msg_in)
    


def requestDataIsCorrect(data):
    if (data[_METHOD_]) in _METHOD_LIST_:
        if data[_METHOD_] == _READ_ or data[_METHOD_] == _WRITE_ and isinstance(data[_ARGS_], str):
            return
        raise ArgumentError(str(data[_METHOD_]), str(data[_ARGS_]))
    raise MethodError(str(data[_METHOD_]), "Argument must be wrong ofc!!")

def resultDataIsCorrect(data):
    if _ERROR_ in data:
        raise data[_ERROR_][_ERROR_NAME_](data[_ERROR_][_ARGS_])
    if not isinstance(data[_RESULT_], str):
        raise ArgumentError(str(data[_METHOD_]), str(data[_ARGS_]))
    return
#//////////////////// End of: Functions to find errors if they exists ///////#



#//////////////////// Begin of: Functions to create or load request/reply ///#
def createRequest(method, args=0):
    if args:
        return json.dumps({_METHOD_: method, _ARGS_: args})
    return json.dumps({_METHOD_: method})

def loadRequest(requestIn):
    msgFormatCorrect(requestIn, True)
    data = json.loads(requestIn)
    requestDataIsCorrect(data)
    return data

def loadReply(replyIn):
    msgFormatCorrect(replyIn)
    data = json.loads(replyIn)
    resultDataIsCorrect(data)
    return data[_RESULT_]


def createErrorReply(errorClass, argsIn):
    return json.dumps({_ERROR_: {_ERROR_NAME_ : errorClass, _ARGS_ : argsIn}})

def createResultReply(method_result):
    return json.dumps({_RESULT_: method_result})
#//////////////////// End of: Functions to create or load request/reply /////#
