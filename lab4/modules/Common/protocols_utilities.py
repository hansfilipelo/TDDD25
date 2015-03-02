import json
#//////////////////// Begin of: Global variables ////////////////////////////#
# Requests methods
_READ_ = "read"
_WRITE_ = "write"

_METHOD_LIST_ = [_READ_, _WRITE_]

# Result answers
_RESULT_ = "result"
_ERROR_ = "error"
_NAME_ = "name"

# Message components
_METHOD_ = "method"
_ARGS_ = "args"
_ERROR_NAME_ = "name"
#//////////////////// End of: Global variables //////////////////////////////#



#//////////////////// Begin of: Error classes ////////////////////////////#

class MsgFormatError(Exception):
    # Exception raised for errors in the message format
    pass

class MethodError(Exception):
    # Exception raised for using undefined method.
    pass

class ArgumentError(Exception):
    # Exception raised for using wrong arguments for a given method.
    pass

class DatabaseError(Exception):
    
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
        return
    raise MsgFormatError("Message not Json, received message: ",msg_in)
    
#//////////////////// End of: Functions to find errors if they exists ///////#



#//////////////////// Begin of: Functions to create or load request/reply ///#
def createRequest(method, args=[]):
    return json.dumps({_METHOD_: method, _ARGS_: args})

def loadRequest(requestIn):
    msgFormatCorrect(requestIn, True)
    data = json.loads(requestIn)
    print(data)
    if _METHOD_ in data:
        return data 
    if _ERROR_ in data:
        raise getattr(sys.modules[__name__], data[_ERROR_][_NAME_])(data[_ERROR_][_ARGS_])
    raise MethodError("Message is incorrect, recieved message: ", data)

def loadReply(replyIn):
    msgFormatCorrect(replyIn)
    data = json.loads(replyIn)
    if _RESULT_ in data:
        return data[_RESULT_]
    if _ERROR_ in data:
        raise getattr(sys.modules[__name__], data[_ERROR_][_NAME_])(data[_ERROR_][_ARGS_])
    raise MethodError("Message is incorrect, recieved message: ", data)

def createErrorReply(errorClass, argsIn):
    return json.dumps({_ERROR_: {_ERROR_NAME_ : errorClass, _ARGS_ : argsIn}})

def createResultReply(method_result):
    return json.dumps({_RESULT_: method_result})
#//////////////////// End of: Functions to create or load request/reply /////#
