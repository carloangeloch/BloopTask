from fastapi import status
from fastapi.responses import JSONResponse
from typing import Literal, Dict, List


def create_response(type: Literal['data', 'error', 'success'] = 'success', message:str | Dict | List[Dict]  = 'message',status_code: int = 200):
    """
    Returns a JSONRespose based on type and status code'\n
    \ttype - type of a response. Default is success\n
    \t\t* data - for json responses\n
    \t\t* success - for sucess responses with no json\n
    \t\t* error - for exception error or other error responses\n
    \tmessage - can be a str, dict or list[dict]. default is 'message'\n
    \tstatus_code - HTTP response code. Default is 200 = 'OK'\n
    \t\tOther common status codes:\n
    \t\t\t201 - Created\n
    \t\t\t202 - Accepted\n
    \t\t\t400 - Bad Request\n
    \t\t\t401 - Unautorized\n
    \t\t\t403 - Forbidden\n
    \t\t\t404 - Not Found\n
    \t\t\t500 - Internal/Server Error\n
    \t\tsee https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status for more status codes
    """

    try:
        type_text = {}
        if type == 'error':
            type_text = {'Error': message}
        elif type == 'success':
            type_text = {'Success': message}

        return JSONResponse(message if type == 'data' else type_text, status_code=status_code)
    except TypeError as e:
        print(f'Error: {e}')