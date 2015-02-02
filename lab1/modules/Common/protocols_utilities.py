import json
from errors import *

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
#//////////////////// End of: Global variables //////////////////////////////#



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
    if data[_METHOD_] in _METHOD_LIST_:
        if data[_METHOD_] == _READ_ and isinstance(data[_ARGS_], str):
            return
        raise ArgumentError("Received data: ",data)
    raise MethodError("Received data:", data)
#//////////////////// End of: Functions to find errors if they exists ///////#



#//////////////////// Begin of: Functions to create or load request/reply ///#
def createRequest(method, args):
    return json.dumps({_METHOD_: method, _ARGS_: args})

def loadRequest(requestIn):
    try:
        msgFormatCorrect(requestIn)
        requestDataIsCorrect(requestIn)
        return json.loads(requestIn)
    except MsgFormatError as e:
        return "Message format error - " + e.expression + e.message
    except ArgumentError as e:
        return "Argument error - " + e.expression + e.message
    except MethodError as e:
        return "Method error - " + e.expression + e.message

def loadReply(replyIn):
    try:
        msgFormatCorrect(replyIn)
        requestDataIsCorrect(replyIn)
        return json.loads(replyIn)
    except MsgFormatError as e:
        return "Message format error - " + e.expression + e.message
    except ArgumentError as e:
        return "Argument error - " + e.expression + e.message
    except MethodError as e:
        return "Method error - " + e.expression + e.message


def createErrorReply(errors_dict):
    return json.dumps({_ERROR_: errors_dict})

def createResultReply(method_result):
    return json.dumps({_RESULT_: method_result})
#//////////////////// End of: Functions to create or load request/reply /////#
