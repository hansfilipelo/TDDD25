import json

#//////////////////// Begin of: Global variables ////////////////////////////#
# Requests methods
_READ_ = "read"
_WRITE_ = "write"

_METHOD_LIST_ = [_READ_, _WRITE_]

# Errors in Protocols
_MSG_FORMAT_ERROR_ = 0
_METHOD_ERROR_ = 1
_ARGS_ERROR_ = 2
_OK_ = 3

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


def msgFormatCorrect(msg_in, is_request):
    dict = isJson(msg_in)
    if dict and ((_METHOD_ in dict) or (_RESULT_ in dict and len(dict)==1) or (_ERROR_ in dict and len(dict)==1)):
        return _OK_
    return _MSG_FORMAT_ERROR_


def requestDataIsCorrect(data):
    if data[_METHOD_] in _METHOD_LIST_:
        if data[_METHOD_] == _READ_ and isinstance(data[_ARGS_], str):
            return _OK_
        return _ARGS_ERROR_
    return _METHOD_ERROR_
#//////////////////// End of: Functions to find errors if they exists ///////#



#//////////////////// Begin of: Functions to create or load request/reply ///#
def createRequest(method, args):
    return json.dumps({_METHOD_: method, _ARGS_: args})

def loadRequest(requestIn):
    return json.loads(requestIn)

def readReply(replyIn):
    return json.loads(replyIn)

def createErrorReply(errors_dict):
    return json.dumps({_ERROR_: errors_dict})

def createResultReply(method_result):
    return json.dumps({_RESULT_: method_result})
#//////////////////// End of: Functions to create or load request/reply /////#
