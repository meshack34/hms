def success_response(status_code=None,data=None,msg='Operation Success!!'):
    print('Success Response')
    response={
    'success':True,
    'message':msg,
    'data':data,
    }
    if status_code:
        response["status_code"]=status_code
    return response