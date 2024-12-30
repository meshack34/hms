def success_response(status_code=None, data=None, msg='Operation Success!'):
    response = {
        'success': True,
        'message': msg,
        'data': data
    }
    if status_code:
        response["status_code"] = status_code
    return response


def failure_response(status_code=None, data=None, msg='Operation Failure!'):
    response = {
        'success': False,
        'message': msg,
        'data': data
    }
    if status_code:
        response["status_code"] = status_code
    return response
